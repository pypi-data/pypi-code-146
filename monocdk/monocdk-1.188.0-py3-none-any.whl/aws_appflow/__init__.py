'''
# AWS::AppFlow Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as appflow
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for AppFlow construct libraries](https://constructs.dev/search?q=appflow)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::AppFlow resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppFlow.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::AppFlow](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppFlow.html).

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
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnConnector(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appflow.CfnConnector",
):
    '''A CloudFormation ``AWS::AppFlow::Connector``.

    Creates a new connector profile associated with your AWS account . There is a soft quota of 100 connector profiles per AWS account . If you need more connector profiles than this quota allows, you can submit a request to the Amazon AppFlow team through the Amazon AppFlow support channel. In each connector profile that you create, you can provide the credentials and properties for only one connector.

    :cloudformationResource: AWS::AppFlow::Connector
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appflow as appflow
        
        cfn_connector = appflow.CfnConnector(self, "MyCfnConnector",
            connector_provisioning_config=appflow.CfnConnector.ConnectorProvisioningConfigProperty(
                lambda_=appflow.CfnConnector.LambdaConnectorProvisioningConfigProperty(
                    lambda_arn="lambdaArn"
                )
            ),
            connector_provisioning_type="connectorProvisioningType",
        
            # the properties below are optional
            connector_label="connectorLabel",
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        connector_provisioning_config: typing.Union[typing.Union["CfnConnector.ConnectorProvisioningConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        connector_provisioning_type: builtins.str,
        connector_label: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppFlow::Connector``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param connector_provisioning_config: The configuration required for registering the connector.
        :param connector_provisioning_type: The provisioning type used to register the connector.
        :param connector_label: The label used for registering the connector.
        :param description: A description of the connector entity field.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ff4f04437a5f46fcbff59e0b0cf6117ebfbf772738ac5c08138a28bdf620d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectorProps(
            connector_provisioning_config=connector_provisioning_config,
            connector_provisioning_type=connector_provisioning_type,
            connector_label=connector_label,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0882db8ad760095ecc0b5001a8b537d1bd8503f9215369ff372c1b18b42fcc42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9504e45eeca5b33c866ee918a80463eb915bb61edc39ffd82b5a062cf8132774)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrConnectorArn")
    def attr_connector_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ConnectorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConnectorArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="connectorProvisioningConfig")
    def connector_provisioning_config(
        self,
    ) -> typing.Union["CfnConnector.ConnectorProvisioningConfigProperty", _IResolvable_a771d0ef]:
        '''The configuration required for registering the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-connectorprovisioningconfig
        '''
        return typing.cast(typing.Union["CfnConnector.ConnectorProvisioningConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "connectorProvisioningConfig"))

    @connector_provisioning_config.setter
    def connector_provisioning_config(
        self,
        value: typing.Union["CfnConnector.ConnectorProvisioningConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f1c2e1c90fa69616b64ffcea077cf403987bde575c5c5a6a9b2a239f093a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorProvisioningConfig", value)

    @builtins.property
    @jsii.member(jsii_name="connectorProvisioningType")
    def connector_provisioning_type(self) -> builtins.str:
        '''The provisioning type used to register the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-connectorprovisioningtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectorProvisioningType"))

    @connector_provisioning_type.setter
    def connector_provisioning_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd7283c4d8e58d8e3fe091b9ddc8024865cbc39907b2f8d61b1c6f34afbddb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorProvisioningType", value)

    @builtins.property
    @jsii.member(jsii_name="connectorLabel")
    def connector_label(self) -> typing.Optional[builtins.str]:
        '''The label used for registering the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-connectorlabel
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorLabel"))

    @connector_label.setter
    def connector_label(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb16193d92abc6f931ddccebd12527d9a255e7ffd3e0f1af2a30bec07e5ff74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorLabel", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the connector entity field.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5dd008065fe32cae21697cdc754bd328c2f80d9ee37b7101693be01ed1c25bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnector.ConnectorProvisioningConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_": "lambda"},
    )
    class ConnectorProvisioningConfigProperty:
        def __init__(
            self,
            *,
            lambda_: typing.Optional[typing.Union[typing.Union["CfnConnector.LambdaConnectorProvisioningConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains information about the configuration of the connector being registered.

            :param lambda_: Contains information about the configuration of the lambda which is being registered as the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connector-connectorprovisioningconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                connector_provisioning_config_property = appflow.CfnConnector.ConnectorProvisioningConfigProperty(
                    lambda_=appflow.CfnConnector.LambdaConnectorProvisioningConfigProperty(
                        lambda_arn="lambdaArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a02544e9c3ae67993f60880468a4b7ac6afae6e70f8edfe8b4a9514095cc1f6)
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_ is not None:
                self._values["lambda_"] = lambda_

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union["CfnConnector.LambdaConnectorProvisioningConfigProperty", _IResolvable_a771d0ef]]:
            '''Contains information about the configuration of the lambda which is being registered as the connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connector-connectorprovisioningconfig.html#cfn-appflow-connector-connectorprovisioningconfig-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union["CfnConnector.LambdaConnectorProvisioningConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProvisioningConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnector.LambdaConnectorProvisioningConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_arn": "lambdaArn"},
    )
    class LambdaConnectorProvisioningConfigProperty:
        def __init__(self, *, lambda_arn: builtins.str) -> None:
            '''Contains information about the configuration of the lambda which is being registered as the connector.

            :param lambda_arn: Lambda ARN of the connector being registered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connector-lambdaconnectorprovisioningconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                lambda_connector_provisioning_config_property = appflow.CfnConnector.LambdaConnectorProvisioningConfigProperty(
                    lambda_arn="lambdaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3afb2c79f0291a3aa005582e06df074853105a886415dc3c775319f3b936760f)
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "lambda_arn": lambda_arn,
            }

        @builtins.property
        def lambda_arn(self) -> builtins.str:
            '''Lambda ARN of the connector being registered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connector-lambdaconnectorprovisioningconfig.html#cfn-appflow-connector-lambdaconnectorprovisioningconfig-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            assert result is not None, "Required property 'lambda_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConnectorProvisioningConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnConnectorProfile(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appflow.CfnConnectorProfile",
):
    '''A CloudFormation ``AWS::AppFlow::ConnectorProfile``.

    The ``AWS::AppFlow::ConnectorProfile`` resource is an Amazon AppFlow resource type that specifies the configuration profile for an instance of a connector. This includes the provided name, credentials ARN, connection-mode, and so on. The fields that are common to all types of connector profiles are explicitly specified under the ``Properties`` field. The rest of the connector-specific properties are specified under ``Properties/ConnectorProfileConfig`` .
    .. epigraph::

       If you want to use AWS CloudFormation to create a connector profile for connectors that implement OAuth (such as Salesforce, Slack, Zendesk, and Google Analytics), you must fetch the access and refresh tokens. You can do this by implementing your own UI for OAuth, or by retrieving the tokens from elsewhere. Alternatively, you can use the Amazon AppFlow console to create the connector profile, and then use that connector profile in the flow creation CloudFormation template.

    :cloudformationResource: AWS::AppFlow::ConnectorProfile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appflow as appflow
        
        cfn_connector_profile = appflow.CfnConnectorProfile(self, "MyCfnConnectorProfile",
            connection_mode="connectionMode",
            connector_profile_name="connectorProfileName",
            connector_type="connectorType",
        
            # the properties below are optional
            connector_label="connectorLabel",
            connector_profile_config=appflow.CfnConnectorProfile.ConnectorProfileConfigProperty(
                connector_profile_credentials=appflow.CfnConnectorProfile.ConnectorProfileCredentialsProperty(
                    amplitude=appflow.CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty(
                        api_key="apiKey",
                        secret_key="secretKey"
                    ),
                    custom_connector=appflow.CfnConnectorProfile.CustomConnectorProfileCredentialsProperty(
                        authentication_type="authenticationType",
        
                        # the properties below are optional
                        api_key=appflow.CfnConnectorProfile.ApiKeyCredentialsProperty(
                            api_key="apiKey",
        
                            # the properties below are optional
                            api_secret_key="apiSecretKey"
                        ),
                        basic=appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        custom=appflow.CfnConnectorProfile.CustomAuthCredentialsProperty(
                            custom_authentication_type="customAuthenticationType",
        
                            # the properties below are optional
                            credentials_map={
                                "credentials_map_key": "credentialsMap"
                            }
                        ),
                        oauth2=appflow.CfnConnectorProfile.OAuth2CredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            o_auth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        )
                    ),
                    datadog=appflow.CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty(
                        api_key="apiKey",
                        application_key="applicationKey"
                    ),
                    dynatrace=appflow.CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty(
                        api_token="apiToken"
                    ),
                    google_analytics=appflow.CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty(
                        client_id="clientId",
                        client_secret="clientSecret",
        
                        # the properties below are optional
                        access_token="accessToken",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    ),
                    infor_nexus=appflow.CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty(
                        access_key_id="accessKeyId",
                        datakey="datakey",
                        secret_access_key="secretAccessKey",
                        user_id="userId"
                    ),
                    marketo=appflow.CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty(
                        client_id="clientId",
                        client_secret="clientSecret",
        
                        # the properties below are optional
                        access_token="accessToken",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    ),
                    redshift=appflow.CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    salesforce=appflow.CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_credentials_arn="clientCredentialsArn",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    ),
                    sapo_data=appflow.CfnConnectorProfile.SAPODataConnectorProfileCredentialsProperty(
                        basic_auth_credentials=appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        o_auth_credentials=appflow.CfnConnectorProfile.OAuthCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        )
                    ),
                    service_now=appflow.CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    singular=appflow.CfnConnectorProfile.SingularConnectorProfileCredentialsProperty(
                        api_key="apiKey"
                    ),
                    slack=appflow.CfnConnectorProfile.SlackConnectorProfileCredentialsProperty(
                        client_id="clientId",
                        client_secret="clientSecret",
        
                        # the properties below are optional
                        access_token="accessToken",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    ),
                    snowflake=appflow.CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    trendmicro=appflow.CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty(
                        api_secret_key="apiSecretKey"
                    ),
                    veeva=appflow.CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    zendesk=appflow.CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty(
                        client_id="clientId",
                        client_secret="clientSecret",
        
                        # the properties below are optional
                        access_token="accessToken",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    )
                ),
                connector_profile_properties=appflow.CfnConnectorProfile.ConnectorProfilePropertiesProperty(
                    custom_connector=appflow.CfnConnectorProfile.CustomConnectorProfilePropertiesProperty(
                        o_auth2_properties=appflow.CfnConnectorProfile.OAuth2PropertiesProperty(
                            o_auth2_grant_type="oAuth2GrantType",
                            token_url="tokenUrl",
                            token_url_custom_properties={
                                "token_url_custom_properties_key": "tokenUrlCustomProperties"
                            }
                        ),
                        profile_properties={
                            "profile_properties_key": "profileProperties"
                        }
                    ),
                    datadog=appflow.CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    dynatrace=appflow.CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    infor_nexus=appflow.CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    marketo=appflow.CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    redshift=appflow.CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty(
                        bucket_name="bucketName",
                        role_arn="roleArn",
        
                        # the properties below are optional
                        bucket_prefix="bucketPrefix",
                        cluster_identifier="clusterIdentifier",
                        data_api_role_arn="dataApiRoleArn",
                        database_name="databaseName",
                        database_url="databaseUrl",
                        is_redshift_serverless=False,
                        workgroup_name="workgroupName"
                    ),
                    salesforce=appflow.CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl",
                        is_sandbox_environment=False
                    ),
                    sapo_data=appflow.CfnConnectorProfile.SAPODataConnectorProfilePropertiesProperty(
                        application_host_url="applicationHostUrl",
                        application_service_path="applicationServicePath",
                        client_number="clientNumber",
                        logon_language="logonLanguage",
                        o_auth_properties=appflow.CfnConnectorProfile.OAuthPropertiesProperty(
                            auth_code_url="authCodeUrl",
                            o_auth_scopes=["oAuthScopes"],
                            token_url="tokenUrl"
                        ),
                        port_number=123,
                        private_link_service_name="privateLinkServiceName"
                    ),
                    service_now=appflow.CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    slack=appflow.CfnConnectorProfile.SlackConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    snowflake=appflow.CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty(
                        bucket_name="bucketName",
                        stage="stage",
                        warehouse="warehouse",
        
                        # the properties below are optional
                        account_name="accountName",
                        bucket_prefix="bucketPrefix",
                        private_link_service_name="privateLinkServiceName",
                        region="region"
                    ),
                    veeva=appflow.CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    zendesk=appflow.CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    )
                )
            ),
            kms_arn="kmsArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        connection_mode: builtins.str,
        connector_profile_name: builtins.str,
        connector_type: builtins.str,
        connector_label: typing.Optional[builtins.str] = None,
        connector_profile_config: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ConnectorProfileConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kms_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppFlow::ConnectorProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param connection_mode: Indicates the connection mode and if it is public or private.
        :param connector_profile_name: The name of the connector profile. The name is unique for each ``ConnectorProfile`` in the AWS account .
        :param connector_type: The type of connector, such as Salesforce, Amplitude, and so on.
        :param connector_label: The label for the connector profile being created.
        :param connector_profile_config: Defines the connector-specific configuration and credentials.
        :param kms_arn: The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption. This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8eb9502d20e93fc189f7b2c3397d6075e3da66c825abe8f3fc545bfc2b68533)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectorProfileProps(
            connection_mode=connection_mode,
            connector_profile_name=connector_profile_name,
            connector_type=connector_type,
            connector_label=connector_label,
            connector_profile_config=connector_profile_config,
            kms_arn=kms_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83945d45cae5d4442413b691bbef4a2cc6ea3bcb7867de7e42d65f56f265d06a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff3d8a30485056bf5ff54f3922f7355f9fdaf4550de4d1a19eea40a1a32c77ba)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrConnectorProfileArn")
    def attr_connector_profile_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the connector profile.

        :cloudformationAttribute: ConnectorProfileArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConnectorProfileArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCredentialsArn")
    def attr_credentials_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the connector profile credentials.

        :cloudformationAttribute: CredentialsArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCredentialsArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="connectionMode")
    def connection_mode(self) -> builtins.str:
        '''Indicates the connection mode and if it is public or private.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectionmode
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionMode"))

    @connection_mode.setter
    def connection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13dce0806e50b0c8a980d1e52eddbd108f50898a1a9b7f8a69288a8c27c40686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionMode", value)

    @builtins.property
    @jsii.member(jsii_name="connectorProfileName")
    def connector_profile_name(self) -> builtins.str:
        '''The name of the connector profile.

        The name is unique for each ``ConnectorProfile`` in the AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorprofilename
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectorProfileName"))

    @connector_profile_name.setter
    def connector_profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96290196aecdcbfa9845ff2f03c4aff4a0d9e703da8fc60bd1626ef516282700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorProfileName", value)

    @builtins.property
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        '''The type of connector, such as Salesforce, Amplitude, and so on.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectortype
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @connector_type.setter
    def connector_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b1c508a5eb34e541fc61971f6d20d8c5ccaf98ebb183bcb83ab1391839b40d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorType", value)

    @builtins.property
    @jsii.member(jsii_name="connectorLabel")
    def connector_label(self) -> typing.Optional[builtins.str]:
        '''The label for the connector profile being created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorlabel
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorLabel"))

    @connector_label.setter
    def connector_label(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26a793c6d824532222f46a24570db10c51428def9ce77de59116253746bdfd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorLabel", value)

    @builtins.property
    @jsii.member(jsii_name="connectorProfileConfig")
    def connector_profile_config(
        self,
    ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfileConfigProperty", _IResolvable_a771d0ef]]:
        '''Defines the connector-specific configuration and credentials.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorprofileconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfileConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "connectorProfileConfig"))

    @connector_profile_config.setter
    def connector_profile_config(
        self,
        value: typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfileConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd9e5f28bfe7655bc3f14ae38a70630107300c5c2ef80f7f56505175fd8e1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorProfileConfig", value)

    @builtins.property
    @jsii.member(jsii_name="kmsArn")
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption.

        This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-kmsarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsArn"))

    @kms_arn.setter
    def kms_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54deec5ddc1adf2d40f83ae02eeb29948d7b6bb941112ddf2bbd52f0fbdb2ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsArn", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey", "secret_key": "secretKey"},
    )
    class AmplitudeConnectorProfileCredentialsProperty:
        def __init__(self, *, api_key: builtins.str, secret_key: builtins.str) -> None:
            '''The connector-specific credentials required when using Amplitude.

            :param api_key: A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.
            :param secret_key: The Secret Access Key portion of the credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-amplitudeconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                amplitude_connector_profile_credentials_property = appflow.CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty(
                    api_key="apiKey",
                    secret_key="secretKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97a5da9cdcffbb8dafa69e9abd47ef20fb1d346d576ee543060843e8391d5a6f)
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
                check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "api_key": api_key,
                "secret_key": secret_key,
            }

        @builtins.property
        def api_key(self) -> builtins.str:
            '''A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-amplitudeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-amplitudeconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            assert result is not None, "Required property 'api_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def secret_key(self) -> builtins.str:
            '''The Secret Access Key portion of the credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-amplitudeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-amplitudeconnectorprofilecredentials-secretkey
            '''
            result = self._values.get("secret_key")
            assert result is not None, "Required property 'secret_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmplitudeConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ApiKeyCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey", "api_secret_key": "apiSecretKey"},
    )
    class ApiKeyCredentialsProperty:
        def __init__(
            self,
            *,
            api_key: builtins.str,
            api_secret_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The API key credentials required for API key authentication.

            :param api_key: The API key required for API key authentication.
            :param api_secret_key: The API secret key required for API key authentication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-apikeycredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                api_key_credentials_property = appflow.CfnConnectorProfile.ApiKeyCredentialsProperty(
                    api_key="apiKey",
                
                    # the properties below are optional
                    api_secret_key="apiSecretKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a9b3badcf958489c36f45067a3b2a9daa22fbbae2e8d83e66eb562de42fa8e4)
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
                check_type(argname="argument api_secret_key", value=api_secret_key, expected_type=type_hints["api_secret_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "api_key": api_key,
            }
            if api_secret_key is not None:
                self._values["api_secret_key"] = api_secret_key

        @builtins.property
        def api_key(self) -> builtins.str:
            '''The API key required for API key authentication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-apikeycredentials.html#cfn-appflow-connectorprofile-apikeycredentials-apikey
            '''
            result = self._values.get("api_key")
            assert result is not None, "Required property 'api_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def api_secret_key(self) -> typing.Optional[builtins.str]:
            '''The API secret key required for API key authentication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-apikeycredentials.html#cfn-appflow-connectorprofile-apikeycredentials-apisecretkey
            '''
            result = self._values.get("api_secret_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiKeyCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.BasicAuthCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class BasicAuthCredentialsProperty:
        def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
            '''The basic auth credentials required for basic authentication.

            :param password: The password to use to connect to a resource.
            :param username: The username to use to connect to a resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-basicauthcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                basic_auth_credentials_property = appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87d718b1d9e79c164ef87c9bfdd498477219637f73093fed2b95b31e04448ecd)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
                "username": username,
            }

        @builtins.property
        def password(self) -> builtins.str:
            '''The password to use to connect to a resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-basicauthcredentials.html#cfn-appflow-connectorprofile-basicauthcredentials-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''The username to use to connect to a resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-basicauthcredentials.html#cfn-appflow-connectorprofile-basicauthcredentials-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
    )
    class ConnectorOAuthRequestProperty:
        def __init__(
            self,
            *,
            auth_code: typing.Optional[builtins.str] = None,
            redirect_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :param auth_code: The code provided by the connector when it has been authenticated via the connected app.
            :param redirect_uri: The URL to which the authentication server redirects the browser after authorization has been granted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectoroauthrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                connector_oAuth_request_property = appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                    auth_code="authCode",
                    redirect_uri="redirectUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4dc62cb1e080157692013247ff6dbb7ef7c466ebb410a6f5039e941e2beded0f)
                check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
                check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_code is not None:
                self._values["auth_code"] = auth_code
            if redirect_uri is not None:
                self._values["redirect_uri"] = redirect_uri

        @builtins.property
        def auth_code(self) -> typing.Optional[builtins.str]:
            '''The code provided by the connector when it has been authenticated via the connected app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectoroauthrequest.html#cfn-appflow-connectorprofile-connectoroauthrequest-authcode
            '''
            result = self._values.get("auth_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def redirect_uri(self) -> typing.Optional[builtins.str]:
            '''The URL to which the authentication server redirects the browser after authorization has been granted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectoroauthrequest.html#cfn-appflow-connectorprofile-connectoroauthrequest-redirecturi
            '''
            result = self._values.get("redirect_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorOAuthRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ConnectorProfileConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_profile_credentials": "connectorProfileCredentials",
            "connector_profile_properties": "connectorProfileProperties",
        },
    )
    class ConnectorProfileConfigProperty:
        def __init__(
            self,
            *,
            connector_profile_credentials: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            connector_profile_properties: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Defines the connector-specific configuration and credentials for the connector profile.

            :param connector_profile_credentials: The connector-specific credentials required by each connector.
            :param connector_profile_properties: The connector-specific properties of the profile configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                connector_profile_config_property = appflow.CfnConnectorProfile.ConnectorProfileConfigProperty(
                    connector_profile_credentials=appflow.CfnConnectorProfile.ConnectorProfileCredentialsProperty(
                        amplitude=appflow.CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty(
                            api_key="apiKey",
                            secret_key="secretKey"
                        ),
                        custom_connector=appflow.CfnConnectorProfile.CustomConnectorProfileCredentialsProperty(
                            authentication_type="authenticationType",
                
                            # the properties below are optional
                            api_key=appflow.CfnConnectorProfile.ApiKeyCredentialsProperty(
                                api_key="apiKey",
                
                                # the properties below are optional
                                api_secret_key="apiSecretKey"
                            ),
                            basic=appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                                password="password",
                                username="username"
                            ),
                            custom=appflow.CfnConnectorProfile.CustomAuthCredentialsProperty(
                                custom_authentication_type="customAuthenticationType",
                
                                # the properties below are optional
                                credentials_map={
                                    "credentials_map_key": "credentialsMap"
                                }
                            ),
                            oauth2=appflow.CfnConnectorProfile.OAuth2CredentialsProperty(
                                access_token="accessToken",
                                client_id="clientId",
                                client_secret="clientSecret",
                                o_auth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                    auth_code="authCode",
                                    redirect_uri="redirectUri"
                                ),
                                refresh_token="refreshToken"
                            )
                        ),
                        datadog=appflow.CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty(
                            api_key="apiKey",
                            application_key="applicationKey"
                        ),
                        dynatrace=appflow.CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty(
                            api_token="apiToken"
                        ),
                        google_analytics=appflow.CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty(
                            client_id="clientId",
                            client_secret="clientSecret",
                
                            # the properties below are optional
                            access_token="accessToken",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        ),
                        infor_nexus=appflow.CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty(
                            access_key_id="accessKeyId",
                            datakey="datakey",
                            secret_access_key="secretAccessKey",
                            user_id="userId"
                        ),
                        marketo=appflow.CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty(
                            client_id="clientId",
                            client_secret="clientSecret",
                
                            # the properties below are optional
                            access_token="accessToken",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        ),
                        redshift=appflow.CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        salesforce=appflow.CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_credentials_arn="clientCredentialsArn",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        ),
                        sapo_data=appflow.CfnConnectorProfile.SAPODataConnectorProfileCredentialsProperty(
                            basic_auth_credentials=appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                                password="password",
                                username="username"
                            ),
                            o_auth_credentials=appflow.CfnConnectorProfile.OAuthCredentialsProperty(
                                access_token="accessToken",
                                client_id="clientId",
                                client_secret="clientSecret",
                                connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                    auth_code="authCode",
                                    redirect_uri="redirectUri"
                                ),
                                refresh_token="refreshToken"
                            )
                        ),
                        service_now=appflow.CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        singular=appflow.CfnConnectorProfile.SingularConnectorProfileCredentialsProperty(
                            api_key="apiKey"
                        ),
                        slack=appflow.CfnConnectorProfile.SlackConnectorProfileCredentialsProperty(
                            client_id="clientId",
                            client_secret="clientSecret",
                
                            # the properties below are optional
                            access_token="accessToken",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        ),
                        snowflake=appflow.CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        trendmicro=appflow.CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty(
                            api_secret_key="apiSecretKey"
                        ),
                        veeva=appflow.CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        zendesk=appflow.CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty(
                            client_id="clientId",
                            client_secret="clientSecret",
                
                            # the properties below are optional
                            access_token="accessToken",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        )
                    ),
                    connector_profile_properties=appflow.CfnConnectorProfile.ConnectorProfilePropertiesProperty(
                        custom_connector=appflow.CfnConnectorProfile.CustomConnectorProfilePropertiesProperty(
                            o_auth2_properties=appflow.CfnConnectorProfile.OAuth2PropertiesProperty(
                                o_auth2_grant_type="oAuth2GrantType",
                                token_url="tokenUrl",
                                token_url_custom_properties={
                                    "token_url_custom_properties_key": "tokenUrlCustomProperties"
                                }
                            ),
                            profile_properties={
                                "profile_properties_key": "profileProperties"
                            }
                        ),
                        datadog=appflow.CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        dynatrace=appflow.CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        infor_nexus=appflow.CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        marketo=appflow.CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        redshift=appflow.CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty(
                            bucket_name="bucketName",
                            role_arn="roleArn",
                
                            # the properties below are optional
                            bucket_prefix="bucketPrefix",
                            cluster_identifier="clusterIdentifier",
                            data_api_role_arn="dataApiRoleArn",
                            database_name="databaseName",
                            database_url="databaseUrl",
                            is_redshift_serverless=False,
                            workgroup_name="workgroupName"
                        ),
                        salesforce=appflow.CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl",
                            is_sandbox_environment=False
                        ),
                        sapo_data=appflow.CfnConnectorProfile.SAPODataConnectorProfilePropertiesProperty(
                            application_host_url="applicationHostUrl",
                            application_service_path="applicationServicePath",
                            client_number="clientNumber",
                            logon_language="logonLanguage",
                            o_auth_properties=appflow.CfnConnectorProfile.OAuthPropertiesProperty(
                                auth_code_url="authCodeUrl",
                                o_auth_scopes=["oAuthScopes"],
                                token_url="tokenUrl"
                            ),
                            port_number=123,
                            private_link_service_name="privateLinkServiceName"
                        ),
                        service_now=appflow.CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        slack=appflow.CfnConnectorProfile.SlackConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        snowflake=appflow.CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty(
                            bucket_name="bucketName",
                            stage="stage",
                            warehouse="warehouse",
                
                            # the properties below are optional
                            account_name="accountName",
                            bucket_prefix="bucketPrefix",
                            private_link_service_name="privateLinkServiceName",
                            region="region"
                        ),
                        veeva=appflow.CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        zendesk=appflow.CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a422ca98001869d49822eae9b9d000f3de74c14ac977dc6db143d85f28ab712)
                check_type(argname="argument connector_profile_credentials", value=connector_profile_credentials, expected_type=type_hints["connector_profile_credentials"])
                check_type(argname="argument connector_profile_properties", value=connector_profile_properties, expected_type=type_hints["connector_profile_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_profile_credentials is not None:
                self._values["connector_profile_credentials"] = connector_profile_credentials
            if connector_profile_properties is not None:
                self._values["connector_profile_properties"] = connector_profile_properties

        @builtins.property
        def connector_profile_credentials(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required by each connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileconfig.html#cfn-appflow-connectorprofile-connectorprofileconfig-connectorprofilecredentials
            '''
            result = self._values.get("connector_profile_credentials")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def connector_profile_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties of the profile configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileconfig.html#cfn-appflow-connectorprofile-connectorprofileconfig-connectorprofileproperties
            '''
            result = self._values.get("connector_profile_properties")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProfileConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amplitude": "amplitude",
            "custom_connector": "customConnector",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "google_analytics": "googleAnalytics",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "redshift": "redshift",
            "salesforce": "salesforce",
            "sapo_data": "sapoData",
            "service_now": "serviceNow",
            "singular": "singular",
            "slack": "slack",
            "snowflake": "snowflake",
            "trendmicro": "trendmicro",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class ConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            amplitude: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            custom_connector: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.CustomConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            datadog: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dynatrace: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            google_analytics: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            infor_nexus: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            marketo: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            redshift: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            salesforce: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sapo_data: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.SAPODataConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            service_now: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            singular: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.SingularConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            slack: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.SlackConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            snowflake: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            trendmicro: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            veeva: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            zendesk: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The connector-specific credentials required by a connector.

            :param amplitude: The connector-specific credentials required when using Amplitude.
            :param custom_connector: The connector-specific profile credentials that are required when using the custom connector.
            :param datadog: The connector-specific credentials required when using Datadog.
            :param dynatrace: The connector-specific credentials required when using Dynatrace.
            :param google_analytics: The connector-specific credentials required when using Google Analytics.
            :param infor_nexus: The connector-specific credentials required when using Infor Nexus.
            :param marketo: The connector-specific credentials required when using Marketo.
            :param redshift: The connector-specific credentials required when using Amazon Redshift.
            :param salesforce: The connector-specific credentials required when using Salesforce.
            :param sapo_data: The connector-specific profile credentials required when using SAPOData.
            :param service_now: The connector-specific credentials required when using ServiceNow.
            :param singular: The connector-specific credentials required when using Singular.
            :param slack: The connector-specific credentials required when using Slack.
            :param snowflake: The connector-specific credentials required when using Snowflake.
            :param trendmicro: The connector-specific credentials required when using Trend Micro.
            :param veeva: The connector-specific credentials required when using Veeva.
            :param zendesk: The connector-specific credentials required when using Zendesk.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                connector_profile_credentials_property = appflow.CfnConnectorProfile.ConnectorProfileCredentialsProperty(
                    amplitude=appflow.CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty(
                        api_key="apiKey",
                        secret_key="secretKey"
                    ),
                    custom_connector=appflow.CfnConnectorProfile.CustomConnectorProfileCredentialsProperty(
                        authentication_type="authenticationType",
                
                        # the properties below are optional
                        api_key=appflow.CfnConnectorProfile.ApiKeyCredentialsProperty(
                            api_key="apiKey",
                
                            # the properties below are optional
                            api_secret_key="apiSecretKey"
                        ),
                        basic=appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        custom=appflow.CfnConnectorProfile.CustomAuthCredentialsProperty(
                            custom_authentication_type="customAuthenticationType",
                
                            # the properties below are optional
                            credentials_map={
                                "credentials_map_key": "credentialsMap"
                            }
                        ),
                        oauth2=appflow.CfnConnectorProfile.OAuth2CredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            o_auth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        )
                    ),
                    datadog=appflow.CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty(
                        api_key="apiKey",
                        application_key="applicationKey"
                    ),
                    dynatrace=appflow.CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty(
                        api_token="apiToken"
                    ),
                    google_analytics=appflow.CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty(
                        client_id="clientId",
                        client_secret="clientSecret",
                
                        # the properties below are optional
                        access_token="accessToken",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    ),
                    infor_nexus=appflow.CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty(
                        access_key_id="accessKeyId",
                        datakey="datakey",
                        secret_access_key="secretAccessKey",
                        user_id="userId"
                    ),
                    marketo=appflow.CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty(
                        client_id="clientId",
                        client_secret="clientSecret",
                
                        # the properties below are optional
                        access_token="accessToken",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    ),
                    redshift=appflow.CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    salesforce=appflow.CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty(
                        access_token="accessToken",
                        client_credentials_arn="clientCredentialsArn",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    ),
                    sapo_data=appflow.CfnConnectorProfile.SAPODataConnectorProfileCredentialsProperty(
                        basic_auth_credentials=appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        o_auth_credentials=appflow.CfnConnectorProfile.OAuthCredentialsProperty(
                            access_token="accessToken",
                            client_id="clientId",
                            client_secret="clientSecret",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        )
                    ),
                    service_now=appflow.CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    singular=appflow.CfnConnectorProfile.SingularConnectorProfileCredentialsProperty(
                        api_key="apiKey"
                    ),
                    slack=appflow.CfnConnectorProfile.SlackConnectorProfileCredentialsProperty(
                        client_id="clientId",
                        client_secret="clientSecret",
                
                        # the properties below are optional
                        access_token="accessToken",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    ),
                    snowflake=appflow.CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    trendmicro=appflow.CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty(
                        api_secret_key="apiSecretKey"
                    ),
                    veeva=appflow.CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    zendesk=appflow.CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty(
                        client_id="clientId",
                        client_secret="clientSecret",
                
                        # the properties below are optional
                        access_token="accessToken",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec7aeb38b062444edd1e912ad69a5f20a6aaf8dc09a2ef57a8ea0f5866948c6f)
                check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
                check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
                check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
                check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
                check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
                check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
                check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
                check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
                check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
                check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amplitude is not None:
                self._values["amplitude"] = amplitude
            if custom_connector is not None:
                self._values["custom_connector"] = custom_connector
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if google_analytics is not None:
                self._values["google_analytics"] = google_analytics
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if redshift is not None:
                self._values["redshift"] = redshift
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if sapo_data is not None:
                self._values["sapo_data"] = sapo_data
            if service_now is not None:
                self._values["service_now"] = service_now
            if singular is not None:
                self._values["singular"] = singular
            if slack is not None:
                self._values["slack"] = slack
            if snowflake is not None:
                self._values["snowflake"] = snowflake
            if trendmicro is not None:
                self._values["trendmicro"] = trendmicro
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def amplitude(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Amplitude.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-amplitude
            '''
            result = self._values.get("amplitude")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def custom_connector(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.CustomConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific profile credentials that are required when using the custom connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-customconnector
            '''
            result = self._values.get("custom_connector")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.CustomConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def datadog(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Datadog.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Dynatrace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def google_analytics(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Google Analytics.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-googleanalytics
            '''
            result = self._values.get("google_analytics")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def infor_nexus(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Infor Nexus.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Marketo.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def redshift(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Amazon Redshift.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-redshift
            '''
            result = self._values.get("redshift")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Salesforce.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sapo_data(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SAPODataConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific profile credentials required when using SAPOData.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-sapodata
            '''
            result = self._values.get("sapo_data")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SAPODataConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using ServiceNow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def singular(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SingularConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Singular.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-singular
            '''
            result = self._values.get("singular")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SingularConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SlackConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SlackConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def snowflake(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Snowflake.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-snowflake
            '''
            result = self._values.get("snowflake")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def trendmicro(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Trend Micro.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-trendmicro
            '''
            result = self._values.get("trendmicro")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def veeva(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Veeva.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific credentials required when using Zendesk.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_connector": "customConnector",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "redshift": "redshift",
            "salesforce": "salesforce",
            "sapo_data": "sapoData",
            "service_now": "serviceNow",
            "slack": "slack",
            "snowflake": "snowflake",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class ConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            custom_connector: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.CustomConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            datadog: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dynatrace: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            infor_nexus: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            marketo: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            redshift: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            salesforce: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sapo_data: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.SAPODataConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            service_now: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            slack: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.SlackConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            snowflake: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            veeva: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            zendesk: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The connector-specific profile properties required by each connector.

            :param custom_connector: The properties required by the custom connector.
            :param datadog: The connector-specific properties required by Datadog.
            :param dynatrace: The connector-specific properties required by Dynatrace.
            :param infor_nexus: The connector-specific properties required by Infor Nexus.
            :param marketo: The connector-specific properties required by Marketo.
            :param redshift: The connector-specific properties required by Amazon Redshift.
            :param salesforce: The connector-specific properties required by Salesforce.
            :param sapo_data: The connector-specific profile properties required when using SAPOData.
            :param service_now: The connector-specific properties required by serviceNow.
            :param slack: The connector-specific properties required by Slack.
            :param snowflake: The connector-specific properties required by Snowflake.
            :param veeva: The connector-specific properties required by Veeva.
            :param zendesk: The connector-specific properties required by Zendesk.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                connector_profile_properties_property = appflow.CfnConnectorProfile.ConnectorProfilePropertiesProperty(
                    custom_connector=appflow.CfnConnectorProfile.CustomConnectorProfilePropertiesProperty(
                        o_auth2_properties=appflow.CfnConnectorProfile.OAuth2PropertiesProperty(
                            o_auth2_grant_type="oAuth2GrantType",
                            token_url="tokenUrl",
                            token_url_custom_properties={
                                "token_url_custom_properties_key": "tokenUrlCustomProperties"
                            }
                        ),
                        profile_properties={
                            "profile_properties_key": "profileProperties"
                        }
                    ),
                    datadog=appflow.CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    dynatrace=appflow.CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    infor_nexus=appflow.CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    marketo=appflow.CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    redshift=appflow.CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty(
                        bucket_name="bucketName",
                        role_arn="roleArn",
                
                        # the properties below are optional
                        bucket_prefix="bucketPrefix",
                        cluster_identifier="clusterIdentifier",
                        data_api_role_arn="dataApiRoleArn",
                        database_name="databaseName",
                        database_url="databaseUrl",
                        is_redshift_serverless=False,
                        workgroup_name="workgroupName"
                    ),
                    salesforce=appflow.CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl",
                        is_sandbox_environment=False
                    ),
                    sapo_data=appflow.CfnConnectorProfile.SAPODataConnectorProfilePropertiesProperty(
                        application_host_url="applicationHostUrl",
                        application_service_path="applicationServicePath",
                        client_number="clientNumber",
                        logon_language="logonLanguage",
                        o_auth_properties=appflow.CfnConnectorProfile.OAuthPropertiesProperty(
                            auth_code_url="authCodeUrl",
                            o_auth_scopes=["oAuthScopes"],
                            token_url="tokenUrl"
                        ),
                        port_number=123,
                        private_link_service_name="privateLinkServiceName"
                    ),
                    service_now=appflow.CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    slack=appflow.CfnConnectorProfile.SlackConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    snowflake=appflow.CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty(
                        bucket_name="bucketName",
                        stage="stage",
                        warehouse="warehouse",
                
                        # the properties below are optional
                        account_name="accountName",
                        bucket_prefix="bucketPrefix",
                        private_link_service_name="privateLinkServiceName",
                        region="region"
                    ),
                    veeva=appflow.CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    ),
                    zendesk=appflow.CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty(
                        instance_url="instanceUrl"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59f8ebf6fe45477f0a0cf775b1b4f239df8c61f354af4bba207ec4bcda2af3c1)
                check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
                check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
                check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
                check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
                check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
                check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_connector is not None:
                self._values["custom_connector"] = custom_connector
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if redshift is not None:
                self._values["redshift"] = redshift
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if sapo_data is not None:
                self._values["sapo_data"] = sapo_data
            if service_now is not None:
                self._values["service_now"] = service_now
            if slack is not None:
                self._values["slack"] = slack
            if snowflake is not None:
                self._values["snowflake"] = snowflake
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def custom_connector(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.CustomConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required by the custom connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-customconnector
            '''
            result = self._values.get("custom_connector")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.CustomConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def datadog(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by Datadog.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by Dynatrace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def infor_nexus(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by Infor Nexus.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by Marketo.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def redshift(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by Amazon Redshift.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-redshift
            '''
            result = self._values.get("redshift")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by Salesforce.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sapo_data(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SAPODataConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific profile properties required when using SAPOData.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-sapodata
            '''
            result = self._values.get("sapo_data")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SAPODataConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by serviceNow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SlackConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SlackConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def snowflake(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by Snowflake.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-snowflake
            '''
            result = self._values.get("snowflake")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def veeva(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by Veeva.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The connector-specific properties required by Zendesk.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.CustomAuthCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_authentication_type": "customAuthenticationType",
            "credentials_map": "credentialsMap",
        },
    )
    class CustomAuthCredentialsProperty:
        def __init__(
            self,
            *,
            custom_authentication_type: builtins.str,
            credentials_map: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''The custom credentials required for custom authentication.

            :param custom_authentication_type: The custom authentication type that the connector uses.
            :param credentials_map: A map that holds custom authentication credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customauthcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                custom_auth_credentials_property = appflow.CfnConnectorProfile.CustomAuthCredentialsProperty(
                    custom_authentication_type="customAuthenticationType",
                
                    # the properties below are optional
                    credentials_map={
                        "credentials_map_key": "credentialsMap"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e2ef138c3cdf30e92501b90e20140d75856db130ce044fbd2dd5304fc11f97d)
                check_type(argname="argument custom_authentication_type", value=custom_authentication_type, expected_type=type_hints["custom_authentication_type"])
                check_type(argname="argument credentials_map", value=credentials_map, expected_type=type_hints["credentials_map"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "custom_authentication_type": custom_authentication_type,
            }
            if credentials_map is not None:
                self._values["credentials_map"] = credentials_map

        @builtins.property
        def custom_authentication_type(self) -> builtins.str:
            '''The custom authentication type that the connector uses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customauthcredentials.html#cfn-appflow-connectorprofile-customauthcredentials-customauthenticationtype
            '''
            result = self._values.get("custom_authentication_type")
            assert result is not None, "Required property 'custom_authentication_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def credentials_map(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''A map that holds custom authentication credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customauthcredentials.html#cfn-appflow-connectorprofile-customauthcredentials-credentialsmap
            '''
            result = self._values.get("credentials_map")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomAuthCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.CustomConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_type": "authenticationType",
            "api_key": "apiKey",
            "basic": "basic",
            "custom": "custom",
            "oauth2": "oauth2",
        },
    )
    class CustomConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            authentication_type: builtins.str,
            api_key: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ApiKeyCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            basic: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.BasicAuthCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            custom: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.CustomAuthCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            oauth2: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.OAuth2CredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The connector-specific profile credentials that are required when using the custom connector.

            :param authentication_type: The authentication type that the custom connector uses for authenticating while creating a connector profile.
            :param api_key: The API keys required for the authentication of the user.
            :param basic: The basic credentials that are required for the authentication of the user.
            :param custom: If the connector uses the custom authentication mechanism, this holds the required credentials.
            :param oauth2: The OAuth 2.0 credentials required for the authentication of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                custom_connector_profile_credentials_property = appflow.CfnConnectorProfile.CustomConnectorProfileCredentialsProperty(
                    authentication_type="authenticationType",
                
                    # the properties below are optional
                    api_key=appflow.CfnConnectorProfile.ApiKeyCredentialsProperty(
                        api_key="apiKey",
                
                        # the properties below are optional
                        api_secret_key="apiSecretKey"
                    ),
                    basic=appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    custom=appflow.CfnConnectorProfile.CustomAuthCredentialsProperty(
                        custom_authentication_type="customAuthenticationType",
                
                        # the properties below are optional
                        credentials_map={
                            "credentials_map_key": "credentialsMap"
                        }
                    ),
                    oauth2=appflow.CfnConnectorProfile.OAuth2CredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        o_auth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__626190f5d8426cdea17382f3d5c6061ac2a86c0ce668de1cb231ed845d8cbf4a)
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
                check_type(argname="argument basic", value=basic, expected_type=type_hints["basic"])
                check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
                check_type(argname="argument oauth2", value=oauth2, expected_type=type_hints["oauth2"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "authentication_type": authentication_type,
            }
            if api_key is not None:
                self._values["api_key"] = api_key
            if basic is not None:
                self._values["basic"] = basic
            if custom is not None:
                self._values["custom"] = custom
            if oauth2 is not None:
                self._values["oauth2"] = oauth2

        @builtins.property
        def authentication_type(self) -> builtins.str:
            '''The authentication type that the custom connector uses for authenticating while creating a connector profile.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html#cfn-appflow-connectorprofile-customconnectorprofilecredentials-authenticationtype
            '''
            result = self._values.get("authentication_type")
            assert result is not None, "Required property 'authentication_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def api_key(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ApiKeyCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The API keys required for the authentication of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html#cfn-appflow-connectorprofile-customconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ApiKeyCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def basic(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.BasicAuthCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The basic credentials that are required for the authentication of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html#cfn-appflow-connectorprofile-customconnectorprofilecredentials-basic
            '''
            result = self._values.get("basic")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.BasicAuthCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def custom(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.CustomAuthCredentialsProperty", _IResolvable_a771d0ef]]:
            '''If the connector uses the custom authentication mechanism, this holds the required credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html#cfn-appflow-connectorprofile-customconnectorprofilecredentials-custom
            '''
            result = self._values.get("custom")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.CustomAuthCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def oauth2(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.OAuth2CredentialsProperty", _IResolvable_a771d0ef]]:
            '''The OAuth 2.0 credentials required for the authentication of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofilecredentials.html#cfn-appflow-connectorprofile-customconnectorprofilecredentials-oauth2
            '''
            result = self._values.get("oauth2")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.OAuth2CredentialsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.CustomConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "o_auth2_properties": "oAuth2Properties",
            "profile_properties": "profileProperties",
        },
    )
    class CustomConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            o_auth2_properties: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.OAuth2PropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            profile_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''The profile properties required by the custom connector.

            :param o_auth2_properties: The OAuth 2.0 properties required for OAuth 2.0 authentication.
            :param profile_properties: A map of properties that are required to create a profile for the custom connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                custom_connector_profile_properties_property = appflow.CfnConnectorProfile.CustomConnectorProfilePropertiesProperty(
                    o_auth2_properties=appflow.CfnConnectorProfile.OAuth2PropertiesProperty(
                        o_auth2_grant_type="oAuth2GrantType",
                        token_url="tokenUrl",
                        token_url_custom_properties={
                            "token_url_custom_properties_key": "tokenUrlCustomProperties"
                        }
                    ),
                    profile_properties={
                        "profile_properties_key": "profileProperties"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd60cc1132f08652aa01f35297d8b30ba83efb7bf211120e20503f4749cf2fcc)
                check_type(argname="argument o_auth2_properties", value=o_auth2_properties, expected_type=type_hints["o_auth2_properties"])
                check_type(argname="argument profile_properties", value=profile_properties, expected_type=type_hints["profile_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if o_auth2_properties is not None:
                self._values["o_auth2_properties"] = o_auth2_properties
            if profile_properties is not None:
                self._values["profile_properties"] = profile_properties

        @builtins.property
        def o_auth2_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.OAuth2PropertiesProperty", _IResolvable_a771d0ef]]:
            '''The OAuth 2.0 properties required for OAuth 2.0 authentication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofileproperties.html#cfn-appflow-connectorprofile-customconnectorprofileproperties-oauth2properties
            '''
            result = self._values.get("o_auth2_properties")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.OAuth2PropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def profile_properties(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''A map of properties that are required to create a profile for the custom connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-customconnectorprofileproperties.html#cfn-appflow-connectorprofile-customconnectorprofileproperties-profileproperties
            '''
            result = self._values.get("profile_properties")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey", "application_key": "applicationKey"},
    )
    class DatadogConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            api_key: builtins.str,
            application_key: builtins.str,
        ) -> None:
            '''The connector-specific credentials required by Datadog.

            :param api_key: A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.
            :param application_key: Application keys, in conjunction with your API key, give you full access to Datadog’s programmatic API. Application keys are associated with the user account that created them. The application key is used to log all requests made to the API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                datadog_connector_profile_credentials_property = appflow.CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty(
                    api_key="apiKey",
                    application_key="applicationKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fba67988cea79a2c26e774cf5d4010ac43b7bc4e040be48cb066498c64378b79)
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
                check_type(argname="argument application_key", value=application_key, expected_type=type_hints["application_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "api_key": api_key,
                "application_key": application_key,
            }

        @builtins.property
        def api_key(self) -> builtins.str:
            '''A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofilecredentials.html#cfn-appflow-connectorprofile-datadogconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            assert result is not None, "Required property 'api_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def application_key(self) -> builtins.str:
            '''Application keys, in conjunction with your API key, give you full access to Datadog’s programmatic API.

            Application keys are associated with the user account that created them. The application key is used to log all requests made to the API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofilecredentials.html#cfn-appflow-connectorprofile-datadogconnectorprofilecredentials-applicationkey
            '''
            result = self._values.get("application_key")
            assert result is not None, "Required property 'application_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatadogConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class DatadogConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''The connector-specific profile properties required by Datadog.

            :param instance_url: The location of the Datadog resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                datadog_connector_profile_properties_property = appflow.CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__adf53a8bc9044d0b82d700d8652d0170a9ae3c3eb6977b19294a2b5bb882e77e)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''The location of the Datadog resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofileproperties.html#cfn-appflow-connectorprofile-datadogconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatadogConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_token": "apiToken"},
    )
    class DynatraceConnectorProfileCredentialsProperty:
        def __init__(self, *, api_token: builtins.str) -> None:
            '''The connector-specific profile credentials required by Dynatrace.

            :param api_token: The API tokens used by Dynatrace API to authenticate various API calls.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                dynatrace_connector_profile_credentials_property = appflow.CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty(
                    api_token="apiToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ded83bd3a51c78fbe3cc7d64a788a133417929b90ac0e52bac9910b1eb73cabd)
                check_type(argname="argument api_token", value=api_token, expected_type=type_hints["api_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "api_token": api_token,
            }

        @builtins.property
        def api_token(self) -> builtins.str:
            '''The API tokens used by Dynatrace API to authenticate various API calls.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-dynatraceconnectorprofilecredentials-apitoken
            '''
            result = self._values.get("api_token")
            assert result is not None, "Required property 'api_token' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class DynatraceConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''The connector-specific profile properties required by Dynatrace.

            :param instance_url: The location of the Dynatrace resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                dynatrace_connector_profile_properties_property = appflow.CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3cd802cadff541625986a8610ad585e0e0885a2c93cdb93ecaed2b4daa21ec1b)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''The location of the Dynatrace resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofileproperties.html#cfn-appflow-connectorprofile-dynatraceconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "access_token": "accessToken",
            "connector_o_auth_request": "connectorOAuthRequest",
            "refresh_token": "refreshToken",
        },
    )
    class GoogleAnalyticsConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            client_id: builtins.str,
            client_secret: builtins.str,
            access_token: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required by Google Analytics.

            :param client_id: The identifier for the desired client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param access_token: The credentials used to access protected Google Analytics resources.
            :param connector_o_auth_request: Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.
            :param refresh_token: The credentials used to acquire new access tokens. This is required only for OAuth2 access tokens, and is not required for OAuth1 access tokens.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                google_analytics_connector_profile_credentials_property = appflow.CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty(
                    client_id="clientId",
                    client_secret="clientSecret",
                
                    # the properties below are optional
                    access_token="accessToken",
                    connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    ),
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60ae4c2cbbf024279993481f99b917147bea4760342de59936ff72b6fa247769)
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "client_id": client_id,
                "client_secret": client_secret,
            }
            if access_token is not None:
                self._values["access_token"] = access_token
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def client_id(self) -> builtins.str:
            '''The identifier for the desired client.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Google Analytics resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to acquire new access tokens.

            This is required only for OAuth2 access tokens, and is not required for OAuth1 access tokens.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GoogleAnalyticsConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_key_id": "accessKeyId",
            "datakey": "datakey",
            "secret_access_key": "secretAccessKey",
            "user_id": "userId",
        },
    )
    class InforNexusConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_key_id: builtins.str,
            datakey: builtins.str,
            secret_access_key: builtins.str,
            user_id: builtins.str,
        ) -> None:
            '''The connector-specific profile credentials required by Infor Nexus.

            :param access_key_id: The Access Key portion of the credentials.
            :param datakey: The encryption keys used to encrypt data.
            :param secret_access_key: The secret key used to sign requests.
            :param user_id: The identifier for the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                infor_nexus_connector_profile_credentials_property = appflow.CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty(
                    access_key_id="accessKeyId",
                    datakey="datakey",
                    secret_access_key="secretAccessKey",
                    user_id="userId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__292d15a0a6dca37cfff025faba0949c388e17965cfdfbe3b86dc3282ea1e0801)
                check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
                check_type(argname="argument datakey", value=datakey, expected_type=type_hints["datakey"])
                check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
                check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "access_key_id": access_key_id,
                "datakey": datakey,
                "secret_access_key": secret_access_key,
                "user_id": user_id,
            }

        @builtins.property
        def access_key_id(self) -> builtins.str:
            '''The Access Key portion of the credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-accesskeyid
            '''
            result = self._values.get("access_key_id")
            assert result is not None, "Required property 'access_key_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def datakey(self) -> builtins.str:
            '''The encryption keys used to encrypt data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-datakey
            '''
            result = self._values.get("datakey")
            assert result is not None, "Required property 'datakey' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def secret_access_key(self) -> builtins.str:
            '''The secret key used to sign requests.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-secretaccesskey
            '''
            result = self._values.get("secret_access_key")
            assert result is not None, "Required property 'secret_access_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_id(self) -> builtins.str:
            '''The identifier for the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-userid
            '''
            result = self._values.get("user_id")
            assert result is not None, "Required property 'user_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InforNexusConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class InforNexusConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''The connector-specific profile properties required by Infor Nexus.

            :param instance_url: The location of the Infor Nexus resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                infor_nexus_connector_profile_properties_property = appflow.CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c55ae28aeb412ac0719da12895b200cdeb5bc9bcce4c9e0f972e4b84384e1bed)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''The location of the Infor Nexus resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofileproperties.html#cfn-appflow-connectorprofile-infornexusconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InforNexusConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "access_token": "accessToken",
            "connector_o_auth_request": "connectorOAuthRequest",
        },
    )
    class MarketoConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            client_id: builtins.str,
            client_secret: builtins.str,
            access_token: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The connector-specific profile credentials required by Marketo.

            :param client_id: The identifier for the desired client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param access_token: The credentials used to access protected Marketo resources.
            :param connector_o_auth_request: Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                marketo_connector_profile_credentials_property = appflow.CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty(
                    client_id="clientId",
                    client_secret="clientSecret",
                
                    # the properties below are optional
                    access_token="accessToken",
                    connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db046ca0fa9202b2c1faaeb64a39a0d25d00a4e95f41d0041b8a01b5b78d0ec6)
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "client_id": client_id,
                "client_secret": client_secret,
            }
            if access_token is not None:
                self._values["access_token"] = access_token
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request

        @builtins.property
        def client_id(self) -> builtins.str:
            '''The identifier for the desired client.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Marketo resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class MarketoConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''The connector-specific profile properties required when using Marketo.

            :param instance_url: The location of the Marketo resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                marketo_connector_profile_properties_property = appflow.CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b131698bc4a407e9f60ba1ddb62bdba8b516303805ebcba22a843a70765879fd)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''The location of the Marketo resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofileproperties.html#cfn-appflow-connectorprofile-marketoconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.OAuth2CredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "o_auth_request": "oAuthRequest",
            "refresh_token": "refreshToken",
        },
    )
    class OAuth2CredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            o_auth_request: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The OAuth 2.0 credentials required for OAuth 2.0 authentication.

            :param access_token: The access token used to access the connector on your behalf.
            :param client_id: The identifier for the desired client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param o_auth_request: ``CfnConnectorProfile.OAuth2CredentialsProperty.OAuthRequest``.
            :param refresh_token: The refresh token used to refresh an expired access token.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                o_auth2_credentials_property = appflow.CfnConnectorProfile.OAuth2CredentialsProperty(
                    access_token="accessToken",
                    client_id="clientId",
                    client_secret="clientSecret",
                    o_auth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    ),
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b1c6c60f9315a221004c26519158fa97d114b541cb2d7ff44ba2b136753b9b3)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument o_auth_request", value=o_auth_request, expected_type=type_hints["o_auth_request"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if o_auth_request is not None:
                self._values["o_auth_request"] = o_auth_request
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The access token used to access the connector on your behalf.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html#cfn-appflow-connectorprofile-oauth2credentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the desired client.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html#cfn-appflow-connectorprofile-oauth2credentials-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html#cfn-appflow-connectorprofile-oauth2credentials-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.OAuth2CredentialsProperty.OAuthRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html#cfn-appflow-connectorprofile-oauth2credentials-oauthrequest
            '''
            result = self._values.get("o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The refresh token used to refresh an expired access token.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2credentials.html#cfn-appflow-connectorprofile-oauth2credentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuth2CredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.OAuth2PropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "o_auth2_grant_type": "oAuth2GrantType",
            "token_url": "tokenUrl",
            "token_url_custom_properties": "tokenUrlCustomProperties",
        },
    )
    class OAuth2PropertiesProperty:
        def __init__(
            self,
            *,
            o_auth2_grant_type: typing.Optional[builtins.str] = None,
            token_url: typing.Optional[builtins.str] = None,
            token_url_custom_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''The OAuth 2.0 properties required for OAuth 2.0 authentication.

            :param o_auth2_grant_type: The OAuth 2.0 grant type used by connector for OAuth 2.0 authentication.
            :param token_url: The token URL required for OAuth 2.0 authentication.
            :param token_url_custom_properties: Associates your token URL with a map of properties that you define. Use this parameter to provide any additional details that the connector requires to authenticate your request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2properties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                o_auth2_properties_property = appflow.CfnConnectorProfile.OAuth2PropertiesProperty(
                    o_auth2_grant_type="oAuth2GrantType",
                    token_url="tokenUrl",
                    token_url_custom_properties={
                        "token_url_custom_properties_key": "tokenUrlCustomProperties"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3abb37c6b0692ac7dfae871fd061da42edef854094dbcd29dcb47ba308c8984)
                check_type(argname="argument o_auth2_grant_type", value=o_auth2_grant_type, expected_type=type_hints["o_auth2_grant_type"])
                check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
                check_type(argname="argument token_url_custom_properties", value=token_url_custom_properties, expected_type=type_hints["token_url_custom_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if o_auth2_grant_type is not None:
                self._values["o_auth2_grant_type"] = o_auth2_grant_type
            if token_url is not None:
                self._values["token_url"] = token_url
            if token_url_custom_properties is not None:
                self._values["token_url_custom_properties"] = token_url_custom_properties

        @builtins.property
        def o_auth2_grant_type(self) -> typing.Optional[builtins.str]:
            '''The OAuth 2.0 grant type used by connector for OAuth 2.0 authentication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2properties.html#cfn-appflow-connectorprofile-oauth2properties-oauth2granttype
            '''
            result = self._values.get("o_auth2_grant_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_url(self) -> typing.Optional[builtins.str]:
            '''The token URL required for OAuth 2.0 authentication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2properties.html#cfn-appflow-connectorprofile-oauth2properties-tokenurl
            '''
            result = self._values.get("token_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_url_custom_properties(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''Associates your token URL with a map of properties that you define.

            Use this parameter to provide any additional details that the connector requires to authenticate your request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauth2properties.html#cfn-appflow-connectorprofile-oauth2properties-tokenurlcustomproperties
            '''
            result = self._values.get("token_url_custom_properties")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuth2PropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.OAuthCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "connector_o_auth_request": "connectorOAuthRequest",
            "refresh_token": "refreshToken",
        },
    )
    class OAuthCredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The OAuth credentials required for OAuth type authentication.

            :param access_token: The access token used to access protected SAPOData resources.
            :param client_id: The identifier for the desired client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param connector_o_auth_request: ``CfnConnectorProfile.OAuthCredentialsProperty.ConnectorOAuthRequest``.
            :param refresh_token: The refresh token used to refresh expired access token.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                o_auth_credentials_property = appflow.CfnConnectorProfile.OAuthCredentialsProperty(
                    access_token="accessToken",
                    client_id="clientId",
                    client_secret="clientSecret",
                    connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    ),
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77655d54a586d4ebf0175695038d81926f62ea76baf85a07885b64458e706dfe)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The access token used to access protected SAPOData resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html#cfn-appflow-connectorprofile-oauthcredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the desired client.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html#cfn-appflow-connectorprofile-oauthcredentials-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html#cfn-appflow-connectorprofile-oauthcredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.OAuthCredentialsProperty.ConnectorOAuthRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html#cfn-appflow-connectorprofile-oauthcredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The refresh token used to refresh expired access token.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthcredentials.html#cfn-appflow-connectorprofile-oauthcredentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuthCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.OAuthPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_code_url": "authCodeUrl",
            "o_auth_scopes": "oAuthScopes",
            "token_url": "tokenUrl",
        },
    )
    class OAuthPropertiesProperty:
        def __init__(
            self,
            *,
            auth_code_url: typing.Optional[builtins.str] = None,
            o_auth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
            token_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The OAuth properties required for OAuth type authentication.

            :param auth_code_url: The authorization code url required to redirect to SAP Login Page to fetch authorization code for OAuth type authentication.
            :param o_auth_scopes: The OAuth scopes required for OAuth type authentication.
            :param token_url: The token url required to fetch access/refresh tokens using authorization code and also to refresh expired access token using refresh token.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                o_auth_properties_property = appflow.CfnConnectorProfile.OAuthPropertiesProperty(
                    auth_code_url="authCodeUrl",
                    o_auth_scopes=["oAuthScopes"],
                    token_url="tokenUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf1a2d110e424078c861bd1321e5ebcdacd77a32007566431501f33d9de42434)
                check_type(argname="argument auth_code_url", value=auth_code_url, expected_type=type_hints["auth_code_url"])
                check_type(argname="argument o_auth_scopes", value=o_auth_scopes, expected_type=type_hints["o_auth_scopes"])
                check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_code_url is not None:
                self._values["auth_code_url"] = auth_code_url
            if o_auth_scopes is not None:
                self._values["o_auth_scopes"] = o_auth_scopes
            if token_url is not None:
                self._values["token_url"] = token_url

        @builtins.property
        def auth_code_url(self) -> typing.Optional[builtins.str]:
            '''The authorization code url required to redirect to SAP Login Page to fetch authorization code for OAuth type authentication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthproperties.html#cfn-appflow-connectorprofile-oauthproperties-authcodeurl
            '''
            result = self._values.get("auth_code_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def o_auth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The OAuth scopes required for OAuth type authentication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthproperties.html#cfn-appflow-connectorprofile-oauthproperties-oauthscopes
            '''
            result = self._values.get("o_auth_scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def token_url(self) -> typing.Optional[builtins.str]:
            '''The token url required to fetch access/refresh tokens using authorization code and also to refresh expired access token using refresh token.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-oauthproperties.html#cfn-appflow-connectorprofile-oauthproperties-tokenurl
            '''
            result = self._values.get("token_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuthPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class RedshiftConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Amazon Redshift.

            :param password: The password that corresponds to the user name.
            :param username: The name of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                redshift_connector_profile_credentials_property = appflow.CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7fe1f40330a114802768f1b30b4825e4cfec41252a5dc3a939b846e97303cd8a)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password that corresponds to the user name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofilecredentials.html#cfn-appflow-connectorprofile-redshiftconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The name of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofilecredentials.html#cfn-appflow-connectorprofile-redshiftconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "role_arn": "roleArn",
            "bucket_prefix": "bucketPrefix",
            "cluster_identifier": "clusterIdentifier",
            "data_api_role_arn": "dataApiRoleArn",
            "database_name": "databaseName",
            "database_url": "databaseUrl",
            "is_redshift_serverless": "isRedshiftServerless",
            "workgroup_name": "workgroupName",
        },
    )
    class RedshiftConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            role_arn: builtins.str,
            bucket_prefix: typing.Optional[builtins.str] = None,
            cluster_identifier: typing.Optional[builtins.str] = None,
            data_api_role_arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            database_url: typing.Optional[builtins.str] = None,
            is_redshift_serverless: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            workgroup_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties when using Amazon Redshift.

            :param bucket_name: A name for the associated Amazon S3 bucket.
            :param role_arn: The Amazon Resource Name (ARN) of IAM role that grants Amazon Redshift read-only access to Amazon S3. For more information, and for the polices that you attach to this role, see `Allow Amazon Redshift to access your Amazon AppFlow data in Amazon S3 <https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_service-role-policies.html#redshift-access-s3>`_ .
            :param bucket_prefix: The object key for the destination bucket in which Amazon AppFlow places the files.
            :param cluster_identifier: The unique ID that's assigned to an Amazon Redshift cluster.
            :param data_api_role_arn: The Amazon Resource Name (ARN) of an IAM role that permits Amazon AppFlow to access your Amazon Redshift database through the Data API. For more information, and for the polices that you attach to this role, see `Allow Amazon AppFlow to access Amazon Redshift databases with the Data API <https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_service-role-policies.html#access-redshift>`_ .
            :param database_name: The name of an Amazon Redshift database.
            :param database_url: The JDBC URL of the Amazon Redshift cluster.
            :param is_redshift_serverless: Indicates whether the connector profile defines a connection to an Amazon Redshift Serverless data warehouse.
            :param workgroup_name: The name of an Amazon Redshift workgroup.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                redshift_connector_profile_properties_property = appflow.CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty(
                    bucket_name="bucketName",
                    role_arn="roleArn",
                
                    # the properties below are optional
                    bucket_prefix="bucketPrefix",
                    cluster_identifier="clusterIdentifier",
                    data_api_role_arn="dataApiRoleArn",
                    database_name="databaseName",
                    database_url="databaseUrl",
                    is_redshift_serverless=False,
                    workgroup_name="workgroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__906416d8d62fdb2bbd22f109b5196f53f284f1adf51ebcba3c0da500b89f9fda)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
                check_type(argname="argument data_api_role_arn", value=data_api_role_arn, expected_type=type_hints["data_api_role_arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument database_url", value=database_url, expected_type=type_hints["database_url"])
                check_type(argname="argument is_redshift_serverless", value=is_redshift_serverless, expected_type=type_hints["is_redshift_serverless"])
                check_type(argname="argument workgroup_name", value=workgroup_name, expected_type=type_hints["workgroup_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
                "role_arn": role_arn,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if cluster_identifier is not None:
                self._values["cluster_identifier"] = cluster_identifier
            if data_api_role_arn is not None:
                self._values["data_api_role_arn"] = data_api_role_arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if database_url is not None:
                self._values["database_url"] = database_url
            if is_redshift_serverless is not None:
                self._values["is_redshift_serverless"] = is_redshift_serverless
            if workgroup_name is not None:
                self._values["workgroup_name"] = workgroup_name

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''A name for the associated Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of IAM role that grants Amazon Redshift read-only access to Amazon S3.

            For more information, and for the polices that you attach to this role, see `Allow Amazon Redshift to access your Amazon AppFlow data in Amazon S3 <https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_service-role-policies.html#redshift-access-s3>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the destination bucket in which Amazon AppFlow places the files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cluster_identifier(self) -> typing.Optional[builtins.str]:
            '''The unique ID that's assigned to an Amazon Redshift cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-clusteridentifier
            '''
            result = self._values.get("cluster_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_api_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an IAM role that permits Amazon AppFlow to access your Amazon Redshift database through the Data API.

            For more information, and for the polices that you attach to this role, see `Allow Amazon AppFlow to access Amazon Redshift databases with the Data API <https://docs.aws.amazon.com/appflow/latest/userguide/security_iam_service-role-policies.html#access-redshift>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-dataapirolearn
            '''
            result = self._values.get("data_api_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of an Amazon Redshift database.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_url(self) -> typing.Optional[builtins.str]:
            '''The JDBC URL of the Amazon Redshift cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-databaseurl
            '''
            result = self._values.get("database_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_redshift_serverless(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether the connector profile defines a connection to an Amazon Redshift Serverless data warehouse.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-isredshiftserverless
            '''
            result = self._values.get("is_redshift_serverless")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def workgroup_name(self) -> typing.Optional[builtins.str]:
            '''The name of an Amazon Redshift workgroup.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-workgroupname
            '''
            result = self._values.get("workgroup_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SAPODataConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "basic_auth_credentials": "basicAuthCredentials",
            "o_auth_credentials": "oAuthCredentials",
        },
    )
    class SAPODataConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            basic_auth_credentials: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.BasicAuthCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            o_auth_credentials: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.OAuthCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using SAPOData.

            :param basic_auth_credentials: The SAPOData basic authentication credentials.
            :param o_auth_credentials: The SAPOData OAuth type authentication credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                s_aPOData_connector_profile_credentials_property = appflow.CfnConnectorProfile.SAPODataConnectorProfileCredentialsProperty(
                    basic_auth_credentials=appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    o_auth_credentials=appflow.CfnConnectorProfile.OAuthCredentialsProperty(
                        access_token="accessToken",
                        client_id="clientId",
                        client_secret="clientSecret",
                        connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                            auth_code="authCode",
                            redirect_uri="redirectUri"
                        ),
                        refresh_token="refreshToken"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d39d24382f990d02f6143725bc22a8d7d6e7664d5f75d236bcaee863f132a45)
                check_type(argname="argument basic_auth_credentials", value=basic_auth_credentials, expected_type=type_hints["basic_auth_credentials"])
                check_type(argname="argument o_auth_credentials", value=o_auth_credentials, expected_type=type_hints["o_auth_credentials"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if basic_auth_credentials is not None:
                self._values["basic_auth_credentials"] = basic_auth_credentials
            if o_auth_credentials is not None:
                self._values["o_auth_credentials"] = o_auth_credentials

        @builtins.property
        def basic_auth_credentials(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.BasicAuthCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The SAPOData basic authentication credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofilecredentials.html#cfn-appflow-connectorprofile-sapodataconnectorprofilecredentials-basicauthcredentials
            '''
            result = self._values.get("basic_auth_credentials")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.BasicAuthCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def o_auth_credentials(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.OAuthCredentialsProperty", _IResolvable_a771d0ef]]:
            '''The SAPOData OAuth type authentication credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofilecredentials.html#cfn-appflow-connectorprofile-sapodataconnectorprofilecredentials-oauthcredentials
            '''
            result = self._values.get("o_auth_credentials")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.OAuthCredentialsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAPODataConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SAPODataConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_host_url": "applicationHostUrl",
            "application_service_path": "applicationServicePath",
            "client_number": "clientNumber",
            "logon_language": "logonLanguage",
            "o_auth_properties": "oAuthProperties",
            "port_number": "portNumber",
            "private_link_service_name": "privateLinkServiceName",
        },
    )
    class SAPODataConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            application_host_url: typing.Optional[builtins.str] = None,
            application_service_path: typing.Optional[builtins.str] = None,
            client_number: typing.Optional[builtins.str] = None,
            logon_language: typing.Optional[builtins.str] = None,
            o_auth_properties: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.OAuthPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            port_number: typing.Optional[jsii.Number] = None,
            private_link_service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required when using SAPOData.

            :param application_host_url: The location of the SAPOData resource.
            :param application_service_path: The application path to catalog service.
            :param client_number: The client number for the client creating the connection.
            :param logon_language: The logon language of SAPOData instance.
            :param o_auth_properties: The SAPOData OAuth properties required for OAuth type authentication.
            :param port_number: The port number of the SAPOData instance.
            :param private_link_service_name: The SAPOData Private Link service name to be used for private data transfers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                s_aPOData_connector_profile_properties_property = appflow.CfnConnectorProfile.SAPODataConnectorProfilePropertiesProperty(
                    application_host_url="applicationHostUrl",
                    application_service_path="applicationServicePath",
                    client_number="clientNumber",
                    logon_language="logonLanguage",
                    o_auth_properties=appflow.CfnConnectorProfile.OAuthPropertiesProperty(
                        auth_code_url="authCodeUrl",
                        o_auth_scopes=["oAuthScopes"],
                        token_url="tokenUrl"
                    ),
                    port_number=123,
                    private_link_service_name="privateLinkServiceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b30fbed7b65e64022968e1bf0deaec358fa031306a0c9a1797c7b8d576d7c3cb)
                check_type(argname="argument application_host_url", value=application_host_url, expected_type=type_hints["application_host_url"])
                check_type(argname="argument application_service_path", value=application_service_path, expected_type=type_hints["application_service_path"])
                check_type(argname="argument client_number", value=client_number, expected_type=type_hints["client_number"])
                check_type(argname="argument logon_language", value=logon_language, expected_type=type_hints["logon_language"])
                check_type(argname="argument o_auth_properties", value=o_auth_properties, expected_type=type_hints["o_auth_properties"])
                check_type(argname="argument port_number", value=port_number, expected_type=type_hints["port_number"])
                check_type(argname="argument private_link_service_name", value=private_link_service_name, expected_type=type_hints["private_link_service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_host_url is not None:
                self._values["application_host_url"] = application_host_url
            if application_service_path is not None:
                self._values["application_service_path"] = application_service_path
            if client_number is not None:
                self._values["client_number"] = client_number
            if logon_language is not None:
                self._values["logon_language"] = logon_language
            if o_auth_properties is not None:
                self._values["o_auth_properties"] = o_auth_properties
            if port_number is not None:
                self._values["port_number"] = port_number
            if private_link_service_name is not None:
                self._values["private_link_service_name"] = private_link_service_name

        @builtins.property
        def application_host_url(self) -> typing.Optional[builtins.str]:
            '''The location of the SAPOData resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-applicationhosturl
            '''
            result = self._values.get("application_host_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def application_service_path(self) -> typing.Optional[builtins.str]:
            '''The application path to catalog service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-applicationservicepath
            '''
            result = self._values.get("application_service_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_number(self) -> typing.Optional[builtins.str]:
            '''The client number for the client creating the connection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-clientnumber
            '''
            result = self._values.get("client_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logon_language(self) -> typing.Optional[builtins.str]:
            '''The logon language of SAPOData instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-logonlanguage
            '''
            result = self._values.get("logon_language")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def o_auth_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.OAuthPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The SAPOData OAuth properties required for OAuth type authentication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-oauthproperties
            '''
            result = self._values.get("o_auth_properties")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.OAuthPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def port_number(self) -> typing.Optional[jsii.Number]:
            '''The port number of the SAPOData instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-portnumber
            '''
            result = self._values.get("port_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def private_link_service_name(self) -> typing.Optional[builtins.str]:
            '''The SAPOData Private Link service name to be used for private data transfers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-sapodataconnectorprofileproperties.html#cfn-appflow-connectorprofile-sapodataconnectorprofileproperties-privatelinkservicename
            '''
            result = self._values.get("private_link_service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAPODataConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_credentials_arn": "clientCredentialsArn",
            "connector_o_auth_request": "connectorOAuthRequest",
            "refresh_token": "refreshToken",
        },
    )
    class SalesforceConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_credentials_arn: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Salesforce.

            :param access_token: The credentials used to access protected Salesforce resources.
            :param client_credentials_arn: The secret manager ARN, which contains the client ID and client secret of the connected app.
            :param connector_o_auth_request: Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.
            :param refresh_token: The credentials used to acquire new access tokens.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                salesforce_connector_profile_credentials_property = appflow.CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty(
                    access_token="accessToken",
                    client_credentials_arn="clientCredentialsArn",
                    connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    ),
                    refresh_token="refreshToken"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__472b57cd8fd56668ca08b10a90d67d5b9092be899fbc14dcc68d28924d850019)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument client_credentials_arn", value=client_credentials_arn, expected_type=type_hints["client_credentials_arn"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_credentials_arn is not None:
                self._values["client_credentials_arn"] = client_credentials_arn
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Salesforce resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_credentials_arn(self) -> typing.Optional[builtins.str]:
            '''The secret manager ARN, which contains the client ID and client secret of the connected app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-clientcredentialsarn
            '''
            result = self._values.get("client_credentials_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to acquire new access tokens.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_url": "instanceUrl",
            "is_sandbox_environment": "isSandboxEnvironment",
        },
    )
    class SalesforceConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
            is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The connector-specific profile properties required when using Salesforce.

            :param instance_url: The location of the Salesforce resource.
            :param is_sandbox_environment: Indicates whether the connector profile applies to a sandbox or production environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                salesforce_connector_profile_properties_property = appflow.CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl",
                    is_sandbox_environment=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__416405de6dfe84b3d6e753ebac22fb34732acd07c382ce25e307ae98debd59c4)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
                check_type(argname="argument is_sandbox_environment", value=is_sandbox_environment, expected_type=type_hints["is_sandbox_environment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url
            if is_sandbox_environment is not None:
                self._values["is_sandbox_environment"] = is_sandbox_environment

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The location of the Salesforce resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofileproperties.html#cfn-appflow-connectorprofile-salesforceconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_sandbox_environment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether the connector profile applies to a sandbox or production environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofileproperties.html#cfn-appflow-connectorprofile-salesforceconnectorprofileproperties-issandboxenvironment
            '''
            result = self._values.get("is_sandbox_environment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class ServiceNowConnectorProfileCredentialsProperty:
        def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
            '''The connector-specific profile credentials required when using ServiceNow.

            :param password: The password that corresponds to the user name.
            :param username: The name of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                service_now_connector_profile_credentials_property = appflow.CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d684f6048a67e7410593dc9206f103be70f5fe79df8348ed9dd46f1f62973eb)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
                "username": username,
            }

        @builtins.property
        def password(self) -> builtins.str:
            '''The password that corresponds to the user name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofilecredentials.html#cfn-appflow-connectorprofile-servicenowconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''The name of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofilecredentials.html#cfn-appflow-connectorprofile-servicenowconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class ServiceNowConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''The connector-specific profile properties required when using ServiceNow.

            :param instance_url: The location of the ServiceNow resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                service_now_connector_profile_properties_property = appflow.CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec490d1810108c4d518dc3577d17d88d2b87e28fef582e3cd27b0b6cbe872575)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''The location of the ServiceNow resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofileproperties.html#cfn-appflow-connectorprofile-servicenowconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SingularConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey"},
    )
    class SingularConnectorProfileCredentialsProperty:
        def __init__(self, *, api_key: builtins.str) -> None:
            '''The connector-specific profile credentials required when using Singular.

            :param api_key: A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-singularconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                singular_connector_profile_credentials_property = appflow.CfnConnectorProfile.SingularConnectorProfileCredentialsProperty(
                    api_key="apiKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e3ababce2e8ec288c1139f68fb0f67e76c59f9f47828884af20ca4321b832e9)
                check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "api_key": api_key,
            }

        @builtins.property
        def api_key(self) -> builtins.str:
            '''A unique alphanumeric identifier used to authenticate a user, developer, or calling program to your API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-singularconnectorprofilecredentials.html#cfn-appflow-connectorprofile-singularconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            assert result is not None, "Required property 'api_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingularConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SlackConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "access_token": "accessToken",
            "connector_o_auth_request": "connectorOAuthRequest",
        },
    )
    class SlackConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            client_id: builtins.str,
            client_secret: builtins.str,
            access_token: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Slack.

            :param client_id: The identifier for the client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param access_token: The credentials used to access protected Slack resources.
            :param connector_o_auth_request: Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                slack_connector_profile_credentials_property = appflow.CfnConnectorProfile.SlackConnectorProfileCredentialsProperty(
                    client_id="clientId",
                    client_secret="clientSecret",
                
                    # the properties below are optional
                    access_token="accessToken",
                    connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6bcf949576d5850339ca29cddfeb922df4b84c1bf934e74f907d363ee85ba80)
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "client_id": client_id,
                "client_secret": client_secret,
            }
            if access_token is not None:
                self._values["access_token"] = access_token
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request

        @builtins.property
        def client_id(self) -> builtins.str:
            '''The identifier for the client.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Slack resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SlackConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class SlackConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''The connector-specific profile properties required when using Slack.

            :param instance_url: The location of the Slack resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                slack_connector_profile_properties_property = appflow.CfnConnectorProfile.SlackConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a231bd1fb30bc7a464c6400efae6e9810c2ec20af0c18c8299ff73fb230d7df1)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''The location of the Slack resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofileproperties.html#cfn-appflow-connectorprofile-slackconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class SnowflakeConnectorProfileCredentialsProperty:
        def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
            '''The connector-specific profile credentials required when using Snowflake.

            :param password: The password that corresponds to the user name.
            :param username: The name of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                snowflake_connector_profile_credentials_property = appflow.CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d95fc3c354a6bce5504786d7d7a1dab9bb06ac1ba07d5eeadf1e8dd05d68fdde)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
                "username": username,
            }

        @builtins.property
        def password(self) -> builtins.str:
            '''The password that corresponds to the user name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-snowflakeconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''The name of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-snowflakeconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "stage": "stage",
            "warehouse": "warehouse",
            "account_name": "accountName",
            "bucket_prefix": "bucketPrefix",
            "private_link_service_name": "privateLinkServiceName",
            "region": "region",
        },
    )
    class SnowflakeConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            stage: builtins.str,
            warehouse: builtins.str,
            account_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            private_link_service_name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The connector-specific profile properties required when using Snowflake.

            :param bucket_name: The name of the Amazon S3 bucket associated with Snowflake.
            :param stage: The name of the Amazon S3 stage that was created while setting up an Amazon S3 stage in the Snowflake account. This is written in the following format: < Database>< Schema>.
            :param warehouse: The name of the Snowflake warehouse.
            :param account_name: The name of the account.
            :param bucket_prefix: The bucket path that refers to the Amazon S3 bucket associated with Snowflake.
            :param private_link_service_name: The Snowflake Private Link service name to be used for private data transfers.
            :param region: The AWS Region of the Snowflake account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                snowflake_connector_profile_properties_property = appflow.CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty(
                    bucket_name="bucketName",
                    stage="stage",
                    warehouse="warehouse",
                
                    # the properties below are optional
                    account_name="accountName",
                    bucket_prefix="bucketPrefix",
                    private_link_service_name="privateLinkServiceName",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__380486fef1f3337d8e5198073dd1b40621287933f1b1253647ff12830af36452)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
                check_type(argname="argument warehouse", value=warehouse, expected_type=type_hints["warehouse"])
                check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument private_link_service_name", value=private_link_service_name, expected_type=type_hints["private_link_service_name"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
                "stage": stage,
                "warehouse": warehouse,
            }
            if account_name is not None:
                self._values["account_name"] = account_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if private_link_service_name is not None:
                self._values["private_link_service_name"] = private_link_service_name
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The name of the Amazon S3 bucket associated with Snowflake.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def stage(self) -> builtins.str:
            '''The name of the Amazon S3 stage that was created while setting up an Amazon S3 stage in the Snowflake account.

            This is written in the following format: < Database>< Schema>.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-stage
            '''
            result = self._values.get("stage")
            assert result is not None, "Required property 'stage' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def warehouse(self) -> builtins.str:
            '''The name of the Snowflake warehouse.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-warehouse
            '''
            result = self._values.get("warehouse")
            assert result is not None, "Required property 'warehouse' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def account_name(self) -> typing.Optional[builtins.str]:
            '''The name of the account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-accountname
            '''
            result = self._values.get("account_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The bucket path that refers to the Amazon S3 bucket associated with Snowflake.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_link_service_name(self) -> typing.Optional[builtins.str]:
            '''The Snowflake Private Link service name to be used for private data transfers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-privatelinkservicename
            '''
            result = self._values.get("private_link_service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region of the Snowflake account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_secret_key": "apiSecretKey"},
    )
    class TrendmicroConnectorProfileCredentialsProperty:
        def __init__(self, *, api_secret_key: builtins.str) -> None:
            '''The connector-specific profile credentials required when using Trend Micro.

            :param api_secret_key: The Secret Access Key portion of the credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-trendmicroconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                trendmicro_connector_profile_credentials_property = appflow.CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty(
                    api_secret_key="apiSecretKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d5f3419a654523c1ce16503a1541d0d771e83e8cf7330290347bad21e769fe6)
                check_type(argname="argument api_secret_key", value=api_secret_key, expected_type=type_hints["api_secret_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "api_secret_key": api_secret_key,
            }

        @builtins.property
        def api_secret_key(self) -> builtins.str:
            '''The Secret Access Key portion of the credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-trendmicroconnectorprofilecredentials.html#cfn-appflow-connectorprofile-trendmicroconnectorprofilecredentials-apisecretkey
            '''
            result = self._values.get("api_secret_key")
            assert result is not None, "Required property 'api_secret_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrendmicroConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class VeevaConnectorProfileCredentialsProperty:
        def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
            '''The connector-specific profile credentials required when using Veeva.

            :param password: The password that corresponds to the user name.
            :param username: The name of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                veeva_connector_profile_credentials_property = appflow.CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__248eb382a50e7d296f2bb207c285178097f63d711fa318fde5bca273b09190c2)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
                "username": username,
            }

        @builtins.property
        def password(self) -> builtins.str:
            '''The password that corresponds to the user name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofilecredentials.html#cfn-appflow-connectorprofile-veevaconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''The name of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofilecredentials.html#cfn-appflow-connectorprofile-veevaconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VeevaConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class VeevaConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''The connector-specific profile properties required when using Veeva.

            :param instance_url: The location of the Veeva resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                veeva_connector_profile_properties_property = appflow.CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c93b9947f5f31ca49b7d62349aceeed18ec9c7261eff6086f5ae74366ed74cf)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''The location of the Veeva resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofileproperties.html#cfn-appflow-connectorprofile-veevaconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VeevaConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "access_token": "accessToken",
            "connector_o_auth_request": "connectorOAuthRequest",
        },
    )
    class ZendeskConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            client_id: builtins.str,
            client_secret: builtins.str,
            access_token: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The connector-specific profile credentials required when using Zendesk.

            :param client_id: The identifier for the desired client.
            :param client_secret: The client secret used by the OAuth client to authenticate to the authorization server.
            :param access_token: The credentials used to access protected Zendesk resources.
            :param connector_o_auth_request: Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                zendesk_connector_profile_credentials_property = appflow.CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty(
                    client_id="clientId",
                    client_secret="clientSecret",
                
                    # the properties below are optional
                    access_token="accessToken",
                    connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                        auth_code="authCode",
                        redirect_uri="redirectUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbaf615a04b7e602f15c770ff91d95063ee5dda4b7d15b81786506f63360cf85)
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument connector_o_auth_request", value=connector_o_auth_request, expected_type=type_hints["connector_o_auth_request"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "client_id": client_id,
                "client_secret": client_secret,
            }
            if access_token is not None:
                self._values["access_token"] = access_token
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request

        @builtins.property
        def client_id(self) -> builtins.str:
            '''The identifier for the desired client.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''The client secret used by the OAuth client to authenticate to the authorization server.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The credentials used to access protected Zendesk resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''Used by select connectors for which the OAuth workflow is supported, such as Salesforce, Google Analytics, Marketo, Zendesk, and Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class ZendeskConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''The connector-specific profile properties required when using Zendesk.

            :param instance_url: The location of the Zendesk resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofileproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                zendesk_connector_profile_properties_property = appflow.CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty(
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e794eb1bb8458dc0a1bf8a4f7d62829dd68fbaffee0d864f7f545de837ef82d)
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''The location of the Zendesk resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofileproperties.html#cfn-appflow-connectorprofile-zendeskconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appflow.CfnConnectorProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_mode": "connectionMode",
        "connector_profile_name": "connectorProfileName",
        "connector_type": "connectorType",
        "connector_label": "connectorLabel",
        "connector_profile_config": "connectorProfileConfig",
        "kms_arn": "kmsArn",
    },
)
class CfnConnectorProfileProps:
    def __init__(
        self,
        *,
        connection_mode: builtins.str,
        connector_profile_name: builtins.str,
        connector_type: builtins.str,
        connector_label: typing.Optional[builtins.str] = None,
        connector_profile_config: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorProfileConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kms_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnConnectorProfile``.

        :param connection_mode: Indicates the connection mode and if it is public or private.
        :param connector_profile_name: The name of the connector profile. The name is unique for each ``ConnectorProfile`` in the AWS account .
        :param connector_type: The type of connector, such as Salesforce, Amplitude, and so on.
        :param connector_label: The label for the connector profile being created.
        :param connector_profile_config: Defines the connector-specific configuration and credentials.
        :param kms_arn: The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption. This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appflow as appflow
            
            cfn_connector_profile_props = appflow.CfnConnectorProfileProps(
                connection_mode="connectionMode",
                connector_profile_name="connectorProfileName",
                connector_type="connectorType",
            
                # the properties below are optional
                connector_label="connectorLabel",
                connector_profile_config=appflow.CfnConnectorProfile.ConnectorProfileConfigProperty(
                    connector_profile_credentials=appflow.CfnConnectorProfile.ConnectorProfileCredentialsProperty(
                        amplitude=appflow.CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty(
                            api_key="apiKey",
                            secret_key="secretKey"
                        ),
                        custom_connector=appflow.CfnConnectorProfile.CustomConnectorProfileCredentialsProperty(
                            authentication_type="authenticationType",
            
                            # the properties below are optional
                            api_key=appflow.CfnConnectorProfile.ApiKeyCredentialsProperty(
                                api_key="apiKey",
            
                                # the properties below are optional
                                api_secret_key="apiSecretKey"
                            ),
                            basic=appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                                password="password",
                                username="username"
                            ),
                            custom=appflow.CfnConnectorProfile.CustomAuthCredentialsProperty(
                                custom_authentication_type="customAuthenticationType",
            
                                # the properties below are optional
                                credentials_map={
                                    "credentials_map_key": "credentialsMap"
                                }
                            ),
                            oauth2=appflow.CfnConnectorProfile.OAuth2CredentialsProperty(
                                access_token="accessToken",
                                client_id="clientId",
                                client_secret="clientSecret",
                                o_auth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                    auth_code="authCode",
                                    redirect_uri="redirectUri"
                                ),
                                refresh_token="refreshToken"
                            )
                        ),
                        datadog=appflow.CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty(
                            api_key="apiKey",
                            application_key="applicationKey"
                        ),
                        dynatrace=appflow.CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty(
                            api_token="apiToken"
                        ),
                        google_analytics=appflow.CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty(
                            client_id="clientId",
                            client_secret="clientSecret",
            
                            # the properties below are optional
                            access_token="accessToken",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        ),
                        infor_nexus=appflow.CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty(
                            access_key_id="accessKeyId",
                            datakey="datakey",
                            secret_access_key="secretAccessKey",
                            user_id="userId"
                        ),
                        marketo=appflow.CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty(
                            client_id="clientId",
                            client_secret="clientSecret",
            
                            # the properties below are optional
                            access_token="accessToken",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        ),
                        redshift=appflow.CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        salesforce=appflow.CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty(
                            access_token="accessToken",
                            client_credentials_arn="clientCredentialsArn",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            ),
                            refresh_token="refreshToken"
                        ),
                        sapo_data=appflow.CfnConnectorProfile.SAPODataConnectorProfileCredentialsProperty(
                            basic_auth_credentials=appflow.CfnConnectorProfile.BasicAuthCredentialsProperty(
                                password="password",
                                username="username"
                            ),
                            o_auth_credentials=appflow.CfnConnectorProfile.OAuthCredentialsProperty(
                                access_token="accessToken",
                                client_id="clientId",
                                client_secret="clientSecret",
                                connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                    auth_code="authCode",
                                    redirect_uri="redirectUri"
                                ),
                                refresh_token="refreshToken"
                            )
                        ),
                        service_now=appflow.CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        singular=appflow.CfnConnectorProfile.SingularConnectorProfileCredentialsProperty(
                            api_key="apiKey"
                        ),
                        slack=appflow.CfnConnectorProfile.SlackConnectorProfileCredentialsProperty(
                            client_id="clientId",
                            client_secret="clientSecret",
            
                            # the properties below are optional
                            access_token="accessToken",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        ),
                        snowflake=appflow.CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        trendmicro=appflow.CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty(
                            api_secret_key="apiSecretKey"
                        ),
                        veeva=appflow.CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        zendesk=appflow.CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty(
                            client_id="clientId",
                            client_secret="clientSecret",
            
                            # the properties below are optional
                            access_token="accessToken",
                            connector_oAuth_request=appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty(
                                auth_code="authCode",
                                redirect_uri="redirectUri"
                            )
                        )
                    ),
                    connector_profile_properties=appflow.CfnConnectorProfile.ConnectorProfilePropertiesProperty(
                        custom_connector=appflow.CfnConnectorProfile.CustomConnectorProfilePropertiesProperty(
                            o_auth2_properties=appflow.CfnConnectorProfile.OAuth2PropertiesProperty(
                                o_auth2_grant_type="oAuth2GrantType",
                                token_url="tokenUrl",
                                token_url_custom_properties={
                                    "token_url_custom_properties_key": "tokenUrlCustomProperties"
                                }
                            ),
                            profile_properties={
                                "profile_properties_key": "profileProperties"
                            }
                        ),
                        datadog=appflow.CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        dynatrace=appflow.CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        infor_nexus=appflow.CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        marketo=appflow.CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        redshift=appflow.CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty(
                            bucket_name="bucketName",
                            role_arn="roleArn",
            
                            # the properties below are optional
                            bucket_prefix="bucketPrefix",
                            cluster_identifier="clusterIdentifier",
                            data_api_role_arn="dataApiRoleArn",
                            database_name="databaseName",
                            database_url="databaseUrl",
                            is_redshift_serverless=False,
                            workgroup_name="workgroupName"
                        ),
                        salesforce=appflow.CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl",
                            is_sandbox_environment=False
                        ),
                        sapo_data=appflow.CfnConnectorProfile.SAPODataConnectorProfilePropertiesProperty(
                            application_host_url="applicationHostUrl",
                            application_service_path="applicationServicePath",
                            client_number="clientNumber",
                            logon_language="logonLanguage",
                            o_auth_properties=appflow.CfnConnectorProfile.OAuthPropertiesProperty(
                                auth_code_url="authCodeUrl",
                                o_auth_scopes=["oAuthScopes"],
                                token_url="tokenUrl"
                            ),
                            port_number=123,
                            private_link_service_name="privateLinkServiceName"
                        ),
                        service_now=appflow.CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        slack=appflow.CfnConnectorProfile.SlackConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        snowflake=appflow.CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty(
                            bucket_name="bucketName",
                            stage="stage",
                            warehouse="warehouse",
            
                            # the properties below are optional
                            account_name="accountName",
                            bucket_prefix="bucketPrefix",
                            private_link_service_name="privateLinkServiceName",
                            region="region"
                        ),
                        veeva=appflow.CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        ),
                        zendesk=appflow.CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty(
                            instance_url="instanceUrl"
                        )
                    )
                ),
                kms_arn="kmsArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ccb75d0f6887e2084432b99a23188877b656380a81b84f28ac00ef302fbc660)
            check_type(argname="argument connection_mode", value=connection_mode, expected_type=type_hints["connection_mode"])
            check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
            check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
            check_type(argname="argument connector_label", value=connector_label, expected_type=type_hints["connector_label"])
            check_type(argname="argument connector_profile_config", value=connector_profile_config, expected_type=type_hints["connector_profile_config"])
            check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_mode": connection_mode,
            "connector_profile_name": connector_profile_name,
            "connector_type": connector_type,
        }
        if connector_label is not None:
            self._values["connector_label"] = connector_label
        if connector_profile_config is not None:
            self._values["connector_profile_config"] = connector_profile_config
        if kms_arn is not None:
            self._values["kms_arn"] = kms_arn

    @builtins.property
    def connection_mode(self) -> builtins.str:
        '''Indicates the connection mode and if it is public or private.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectionmode
        '''
        result = self._values.get("connection_mode")
        assert result is not None, "Required property 'connection_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_profile_name(self) -> builtins.str:
        '''The name of the connector profile.

        The name is unique for each ``ConnectorProfile`` in the AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorprofilename
        '''
        result = self._values.get("connector_profile_name")
        assert result is not None, "Required property 'connector_profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_type(self) -> builtins.str:
        '''The type of connector, such as Salesforce, Amplitude, and so on.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectortype
        '''
        result = self._values.get("connector_type")
        assert result is not None, "Required property 'connector_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_label(self) -> typing.Optional[builtins.str]:
        '''The label for the connector profile being created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorlabel
        '''
        result = self._values.get("connector_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connector_profile_config(
        self,
    ) -> typing.Optional[typing.Union[CfnConnectorProfile.ConnectorProfileConfigProperty, _IResolvable_a771d0ef]]:
        '''Defines the connector-specific configuration and credentials.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorprofileconfig
        '''
        result = self._values.get("connector_profile_config")
        return typing.cast(typing.Optional[typing.Union[CfnConnectorProfile.ConnectorProfileConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption.

        This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-kmsarn
        '''
        result = self._values.get("kms_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appflow.CfnConnectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "connector_provisioning_config": "connectorProvisioningConfig",
        "connector_provisioning_type": "connectorProvisioningType",
        "connector_label": "connectorLabel",
        "description": "description",
    },
)
class CfnConnectorProps:
    def __init__(
        self,
        *,
        connector_provisioning_config: typing.Union[typing.Union[CfnConnector.ConnectorProvisioningConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        connector_provisioning_type: builtins.str,
        connector_label: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnConnector``.

        :param connector_provisioning_config: The configuration required for registering the connector.
        :param connector_provisioning_type: The provisioning type used to register the connector.
        :param connector_label: The label used for registering the connector.
        :param description: A description of the connector entity field.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appflow as appflow
            
            cfn_connector_props = appflow.CfnConnectorProps(
                connector_provisioning_config=appflow.CfnConnector.ConnectorProvisioningConfigProperty(
                    lambda_=appflow.CfnConnector.LambdaConnectorProvisioningConfigProperty(
                        lambda_arn="lambdaArn"
                    )
                ),
                connector_provisioning_type="connectorProvisioningType",
            
                # the properties below are optional
                connector_label="connectorLabel",
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742c870b9ce78a5ebed778edde9e07534348334977ac3ac52a5d66d9257138c3)
            check_type(argname="argument connector_provisioning_config", value=connector_provisioning_config, expected_type=type_hints["connector_provisioning_config"])
            check_type(argname="argument connector_provisioning_type", value=connector_provisioning_type, expected_type=type_hints["connector_provisioning_type"])
            check_type(argname="argument connector_label", value=connector_label, expected_type=type_hints["connector_label"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connector_provisioning_config": connector_provisioning_config,
            "connector_provisioning_type": connector_provisioning_type,
        }
        if connector_label is not None:
            self._values["connector_label"] = connector_label
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def connector_provisioning_config(
        self,
    ) -> typing.Union[CfnConnector.ConnectorProvisioningConfigProperty, _IResolvable_a771d0ef]:
        '''The configuration required for registering the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-connectorprovisioningconfig
        '''
        result = self._values.get("connector_provisioning_config")
        assert result is not None, "Required property 'connector_provisioning_config' is missing"
        return typing.cast(typing.Union[CfnConnector.ConnectorProvisioningConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def connector_provisioning_type(self) -> builtins.str:
        '''The provisioning type used to register the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-connectorprovisioningtype
        '''
        result = self._values.get("connector_provisioning_type")
        assert result is not None, "Required property 'connector_provisioning_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_label(self) -> typing.Optional[builtins.str]:
        '''The label used for registering the connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-connectorlabel
        '''
        result = self._values.get("connector_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the connector entity field.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connector.html#cfn-appflow-connector-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFlow(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appflow.CfnFlow",
):
    '''A CloudFormation ``AWS::AppFlow::Flow``.

    The ``AWS::AppFlow::Flow`` resource is an Amazon AppFlow resource type that specifies a new flow.
    .. epigraph::

       If you want to use AWS CloudFormation to create a connector profile for connectors that implement OAuth (such as Salesforce, Slack, Zendesk, and Google Analytics), you must fetch the access and refresh tokens. You can do this by implementing your own UI for OAuth, or by retrieving the tokens from elsewhere. Alternatively, you can use the Amazon AppFlow console to create the connector profile, and then use that connector profile in the flow creation CloudFormation template.

    :cloudformationResource: AWS::AppFlow::Flow
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appflow as appflow
        
        cfn_flow = appflow.CfnFlow(self, "MyCfnFlow",
            destination_flow_config_list=[appflow.CfnFlow.DestinationFlowConfigProperty(
                connector_type="connectorType",
                destination_connector_properties=appflow.CfnFlow.DestinationConnectorPropertiesProperty(
                    custom_connector=appflow.CfnFlow.CustomConnectorDestinationPropertiesProperty(
                        entity_name="entityName",
        
                        # the properties below are optional
                        custom_properties={
                            "custom_properties_key": "customProperties"
                        },
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        write_operation_type="writeOperationType"
                    ),
                    event_bridge=appflow.CfnFlow.EventBridgeDestinationPropertiesProperty(
                        object="object",
        
                        # the properties below are optional
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        )
                    ),
                    lookout_metrics=appflow.CfnFlow.LookoutMetricsDestinationPropertiesProperty(
                        object="object"
                    ),
                    marketo=appflow.CfnFlow.MarketoDestinationPropertiesProperty(
                        object="object",
        
                        # the properties below are optional
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        )
                    ),
                    redshift=appflow.CfnFlow.RedshiftDestinationPropertiesProperty(
                        intermediate_bucket_name="intermediateBucketName",
                        object="object",
        
                        # the properties below are optional
                        bucket_prefix="bucketPrefix",
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        )
                    ),
                    s3=appflow.CfnFlow.S3DestinationPropertiesProperty(
                        bucket_name="bucketName",
        
                        # the properties below are optional
                        bucket_prefix="bucketPrefix",
                        s3_output_format_config=appflow.CfnFlow.S3OutputFormatConfigProperty(
                            aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                                aggregation_type="aggregationType",
                                target_file_size=123
                            ),
                            file_type="fileType",
                            prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                                path_prefix_hierarchy=["pathPrefixHierarchy"],
                                prefix_format="prefixFormat",
                                prefix_type="prefixType"
                            ),
                            preserve_source_data_typing=False
                        )
                    ),
                    salesforce=appflow.CfnFlow.SalesforceDestinationPropertiesProperty(
                        object="object",
        
                        # the properties below are optional
                        data_transfer_api="dataTransferApi",
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        write_operation_type="writeOperationType"
                    ),
                    sapo_data=appflow.CfnFlow.SAPODataDestinationPropertiesProperty(
                        object_path="objectPath",
        
                        # the properties below are optional
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        success_response_handling_config=appflow.CfnFlow.SuccessResponseHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix"
                        ),
                        write_operation_type="writeOperationType"
                    ),
                    snowflake=appflow.CfnFlow.SnowflakeDestinationPropertiesProperty(
                        intermediate_bucket_name="intermediateBucketName",
                        object="object",
        
                        # the properties below are optional
                        bucket_prefix="bucketPrefix",
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        )
                    ),
                    upsolver=appflow.CfnFlow.UpsolverDestinationPropertiesProperty(
                        bucket_name="bucketName",
                        s3_output_format_config=appflow.CfnFlow.UpsolverS3OutputFormatConfigProperty(
                            prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                                path_prefix_hierarchy=["pathPrefixHierarchy"],
                                prefix_format="prefixFormat",
                                prefix_type="prefixType"
                            ),
        
                            # the properties below are optional
                            aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                                aggregation_type="aggregationType",
                                target_file_size=123
                            ),
                            file_type="fileType"
                        ),
        
                        # the properties below are optional
                        bucket_prefix="bucketPrefix"
                    ),
                    zendesk=appflow.CfnFlow.ZendeskDestinationPropertiesProperty(
                        object="object",
        
                        # the properties below are optional
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        write_operation_type="writeOperationType"
                    )
                ),
        
                # the properties below are optional
                api_version="apiVersion",
                connector_profile_name="connectorProfileName"
            )],
            flow_name="flowName",
            source_flow_config=appflow.CfnFlow.SourceFlowConfigProperty(
                connector_type="connectorType",
                source_connector_properties=appflow.CfnFlow.SourceConnectorPropertiesProperty(
                    amplitude=appflow.CfnFlow.AmplitudeSourcePropertiesProperty(
                        object="object"
                    ),
                    custom_connector=appflow.CfnFlow.CustomConnectorSourcePropertiesProperty(
                        entity_name="entityName",
        
                        # the properties below are optional
                        custom_properties={
                            "custom_properties_key": "customProperties"
                        }
                    ),
                    datadog=appflow.CfnFlow.DatadogSourcePropertiesProperty(
                        object="object"
                    ),
                    dynatrace=appflow.CfnFlow.DynatraceSourcePropertiesProperty(
                        object="object"
                    ),
                    google_analytics=appflow.CfnFlow.GoogleAnalyticsSourcePropertiesProperty(
                        object="object"
                    ),
                    infor_nexus=appflow.CfnFlow.InforNexusSourcePropertiesProperty(
                        object="object"
                    ),
                    marketo=appflow.CfnFlow.MarketoSourcePropertiesProperty(
                        object="object"
                    ),
                    s3=appflow.CfnFlow.S3SourcePropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
        
                        # the properties below are optional
                        s3_input_format_config=appflow.CfnFlow.S3InputFormatConfigProperty(
                            s3_input_file_type="s3InputFileType"
                        )
                    ),
                    salesforce=appflow.CfnFlow.SalesforceSourcePropertiesProperty(
                        object="object",
        
                        # the properties below are optional
                        data_transfer_api="dataTransferApi",
                        enable_dynamic_field_update=False,
                        include_deleted_records=False
                    ),
                    sapo_data=appflow.CfnFlow.SAPODataSourcePropertiesProperty(
                        object_path="objectPath"
                    ),
                    service_now=appflow.CfnFlow.ServiceNowSourcePropertiesProperty(
                        object="object"
                    ),
                    singular=appflow.CfnFlow.SingularSourcePropertiesProperty(
                        object="object"
                    ),
                    slack=appflow.CfnFlow.SlackSourcePropertiesProperty(
                        object="object"
                    ),
                    trendmicro=appflow.CfnFlow.TrendmicroSourcePropertiesProperty(
                        object="object"
                    ),
                    veeva=appflow.CfnFlow.VeevaSourcePropertiesProperty(
                        object="object",
        
                        # the properties below are optional
                        document_type="documentType",
                        include_all_versions=False,
                        include_renditions=False,
                        include_source_files=False
                    ),
                    zendesk=appflow.CfnFlow.ZendeskSourcePropertiesProperty(
                        object="object"
                    )
                ),
        
                # the properties below are optional
                api_version="apiVersion",
                connector_profile_name="connectorProfileName",
                incremental_pull_config=appflow.CfnFlow.IncrementalPullConfigProperty(
                    datetime_type_field_name="datetimeTypeFieldName"
                )
            ),
            tasks=[appflow.CfnFlow.TaskProperty(
                source_fields=["sourceFields"],
                task_type="taskType",
        
                # the properties below are optional
                connector_operator=appflow.CfnFlow.ConnectorOperatorProperty(
                    amplitude="amplitude",
                    custom_connector="customConnector",
                    datadog="datadog",
                    dynatrace="dynatrace",
                    google_analytics="googleAnalytics",
                    infor_nexus="inforNexus",
                    marketo="marketo",
                    s3="s3",
                    salesforce="salesforce",
                    sapo_data="sapoData",
                    service_now="serviceNow",
                    singular="singular",
                    slack="slack",
                    trendmicro="trendmicro",
                    veeva="veeva",
                    zendesk="zendesk"
                ),
                destination_field="destinationField",
                task_properties=[appflow.CfnFlow.TaskPropertiesObjectProperty(
                    key="key",
                    value="value"
                )]
            )],
            trigger_config=appflow.CfnFlow.TriggerConfigProperty(
                trigger_type="triggerType",
        
                # the properties below are optional
                trigger_properties=appflow.CfnFlow.ScheduledTriggerPropertiesProperty(
                    schedule_expression="scheduleExpression",
        
                    # the properties below are optional
                    data_pull_mode="dataPullMode",
                    first_execution_from=123,
                    flow_error_deactivation_threshold=123,
                    schedule_end_time=123,
                    schedule_offset=123,
                    schedule_start_time=123,
                    time_zone="timeZone"
                )
            ),
        
            # the properties below are optional
            description="description",
            kms_arn="kmsArn",
            metadata_catalog_config=appflow.CfnFlow.MetadataCatalogConfigProperty(
                glue_data_catalog=appflow.CfnFlow.GlueDataCatalogProperty(
                    database_name="databaseName",
                    role_arn="roleArn",
                    table_prefix="tablePrefix"
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        destination_flow_config_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFlow.DestinationFlowConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        flow_name: builtins.str,
        source_flow_config: typing.Union[typing.Union["CfnFlow.SourceFlowConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        tasks: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFlow.TaskProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        trigger_config: typing.Union[typing.Union["CfnFlow.TriggerConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        metadata_catalog_config: typing.Optional[typing.Union[typing.Union["CfnFlow.MetadataCatalogConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppFlow::Flow``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_flow_config_list: The configuration that controls how Amazon AppFlow places data in the destination connector.
        :param flow_name: The specified name of the flow. Spaces are not allowed. Use underscores (_) or hyphens (-) only.
        :param source_flow_config: Contains information about the configuration of the source connector used in the flow.
        :param tasks: A list of tasks that Amazon AppFlow performs while transferring the data in the flow run.
        :param trigger_config: The trigger settings that determine how and when Amazon AppFlow runs the specified flow.
        :param description: A user-entered description of the flow.
        :param kms_arn: The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption. This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.
        :param metadata_catalog_config: ``AWS::AppFlow::Flow.MetadataCatalogConfig``.
        :param tags: The tags used to organize, track, or control access for your flow.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a29e3eeb5e5c052af42caaa40bfc5fa9ab3f3ffa666275a8fa4f69e20f59ecc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFlowProps(
            destination_flow_config_list=destination_flow_config_list,
            flow_name=flow_name,
            source_flow_config=source_flow_config,
            tasks=tasks,
            trigger_config=trigger_config,
            description=description,
            kms_arn=kms_arn,
            metadata_catalog_config=metadata_catalog_config,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6410a78806435da2c1aa97db2d2d301f6d6c8da55b903cf03611f7390e461161)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68e7b4d9f259ccd73fe979110cec8e960301139ed48fd58dd36961d95922fd7a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrFlowArn")
    def attr_flow_arn(self) -> builtins.str:
        '''The flow's Amazon Resource Name (ARN).

        :cloudformationAttribute: FlowArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFlowArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags used to organize, track, or control access for your flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="destinationFlowConfigList")
    def destination_flow_config_list(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.DestinationFlowConfigProperty", _IResolvable_a771d0ef]]]:
        '''The configuration that controls how Amazon AppFlow places data in the destination connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-destinationflowconfiglist
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.DestinationFlowConfigProperty", _IResolvable_a771d0ef]]], jsii.get(self, "destinationFlowConfigList"))

    @destination_flow_config_list.setter
    def destination_flow_config_list(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.DestinationFlowConfigProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303dcae9337390c21aeaa62833b4b4c92a196572c71ba898724f63e60140878e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationFlowConfigList", value)

    @builtins.property
    @jsii.member(jsii_name="flowName")
    def flow_name(self) -> builtins.str:
        '''The specified name of the flow.

        Spaces are not allowed. Use underscores (_) or hyphens (-) only.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-flowname
        '''
        return typing.cast(builtins.str, jsii.get(self, "flowName"))

    @flow_name.setter
    def flow_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3941d423f68cf70da9f60b09912f505dc349ce2c945820fb5b07b8b0ab8d51f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flowName", value)

    @builtins.property
    @jsii.member(jsii_name="sourceFlowConfig")
    def source_flow_config(
        self,
    ) -> typing.Union["CfnFlow.SourceFlowConfigProperty", _IResolvable_a771d0ef]:
        '''Contains information about the configuration of the source connector used in the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-sourceflowconfig
        '''
        return typing.cast(typing.Union["CfnFlow.SourceFlowConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "sourceFlowConfig"))

    @source_flow_config.setter
    def source_flow_config(
        self,
        value: typing.Union["CfnFlow.SourceFlowConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aecd640c011b84bccc6fea3cfac6a7e6ee5250777d80d57b8025852ce6588a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFlowConfig", value)

    @builtins.property
    @jsii.member(jsii_name="tasks")
    def tasks(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskProperty", _IResolvable_a771d0ef]]]:
        '''A list of tasks that Amazon AppFlow performs while transferring the data in the flow run.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-tasks
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskProperty", _IResolvable_a771d0ef]]], jsii.get(self, "tasks"))

    @tasks.setter
    def tasks(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6aca99025097d768f44c9b04d3117c40a983a63a97b44aa57d5bc63aeba19a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tasks", value)

    @builtins.property
    @jsii.member(jsii_name="triggerConfig")
    def trigger_config(
        self,
    ) -> typing.Union["CfnFlow.TriggerConfigProperty", _IResolvable_a771d0ef]:
        '''The trigger settings that determine how and when Amazon AppFlow runs the specified flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-triggerconfig
        '''
        return typing.cast(typing.Union["CfnFlow.TriggerConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "triggerConfig"))

    @trigger_config.setter
    def trigger_config(
        self,
        value: typing.Union["CfnFlow.TriggerConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b53656ef317c12440802a02f88035fb13b58980deaf42dfd07a0f972d9ef90a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerConfig", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A user-entered description of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4471ca08541e13485a6594fb9d31d02a1260d7582748b029c8fce706961d5e3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="kmsArn")
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption.

        This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-kmsarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsArn"))

    @kms_arn.setter
    def kms_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e066fde0756ae35d101b0afaa40541384e780baf6df93ba55b7a0599f33ad86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsArn", value)

    @builtins.property
    @jsii.member(jsii_name="metadataCatalogConfig")
    def metadata_catalog_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFlow.MetadataCatalogConfigProperty", _IResolvable_a771d0ef]]:
        '''``AWS::AppFlow::Flow.MetadataCatalogConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-metadatacatalogconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFlow.MetadataCatalogConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "metadataCatalogConfig"))

    @metadata_catalog_config.setter
    def metadata_catalog_config(
        self,
        value: typing.Optional[typing.Union["CfnFlow.MetadataCatalogConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e6ca8921c77880f28fcf5284732766b6296d226e5ac1c35feef24076c870fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataCatalogConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.AggregationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation_type": "aggregationType",
            "target_file_size": "targetFileSize",
        },
    )
    class AggregationConfigProperty:
        def __init__(
            self,
            *,
            aggregation_type: typing.Optional[builtins.str] = None,
            target_file_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The aggregation settings that you can use to customize the output format of your flow data.

            :param aggregation_type: Specifies whether Amazon AppFlow aggregates the flow records into a single file, or leave them unaggregated.
            :param target_file_size: The desired file size, in MB, for each output file that Amazon AppFlow writes to the flow destination. For each file, Amazon AppFlow attempts to achieve the size that you specify. The actual file sizes might differ from this target based on the number and size of the records that each file contains.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-aggregationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                aggregation_config_property = appflow.CfnFlow.AggregationConfigProperty(
                    aggregation_type="aggregationType",
                    target_file_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f510e57471eda2e5d7abf40ba7799f618a39fd62448753cd69010f0c1b68ba6)
                check_type(argname="argument aggregation_type", value=aggregation_type, expected_type=type_hints["aggregation_type"])
                check_type(argname="argument target_file_size", value=target_file_size, expected_type=type_hints["target_file_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregation_type is not None:
                self._values["aggregation_type"] = aggregation_type
            if target_file_size is not None:
                self._values["target_file_size"] = target_file_size

        @builtins.property
        def aggregation_type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether Amazon AppFlow aggregates the flow records into a single file, or leave them unaggregated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-aggregationconfig.html#cfn-appflow-flow-aggregationconfig-aggregationtype
            '''
            result = self._values.get("aggregation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_file_size(self) -> typing.Optional[jsii.Number]:
            '''The desired file size, in MB, for each output file that Amazon AppFlow writes to the flow destination.

            For each file, Amazon AppFlow attempts to achieve the size that you specify. The actual file sizes might differ from this target based on the number and size of the records that each file contains.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-aggregationconfig.html#cfn-appflow-flow-aggregationconfig-targetfilesize
            '''
            result = self._values.get("target_file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AggregationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.AmplitudeSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class AmplitudeSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when Amplitude is being used as a source.

            :param object: The object specified in the Amplitude flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-amplitudesourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                amplitude_source_properties_property = appflow.CfnFlow.AmplitudeSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__333f84c2013d82782a87ff6ba9d75382ecaa7ace6cce000d4cb69a0e347d875f)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Amplitude flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-amplitudesourceproperties.html#cfn-appflow-flow-amplitudesourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmplitudeSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ConnectorOperatorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amplitude": "amplitude",
            "custom_connector": "customConnector",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "google_analytics": "googleAnalytics",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "s3": "s3",
            "salesforce": "salesforce",
            "sapo_data": "sapoData",
            "service_now": "serviceNow",
            "singular": "singular",
            "slack": "slack",
            "trendmicro": "trendmicro",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class ConnectorOperatorProperty:
        def __init__(
            self,
            *,
            amplitude: typing.Optional[builtins.str] = None,
            custom_connector: typing.Optional[builtins.str] = None,
            datadog: typing.Optional[builtins.str] = None,
            dynatrace: typing.Optional[builtins.str] = None,
            google_analytics: typing.Optional[builtins.str] = None,
            infor_nexus: typing.Optional[builtins.str] = None,
            marketo: typing.Optional[builtins.str] = None,
            s3: typing.Optional[builtins.str] = None,
            salesforce: typing.Optional[builtins.str] = None,
            sapo_data: typing.Optional[builtins.str] = None,
            service_now: typing.Optional[builtins.str] = None,
            singular: typing.Optional[builtins.str] = None,
            slack: typing.Optional[builtins.str] = None,
            trendmicro: typing.Optional[builtins.str] = None,
            veeva: typing.Optional[builtins.str] = None,
            zendesk: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The operation to be performed on the provided source fields.

            :param amplitude: The operation to be performed on the provided Amplitude source fields.
            :param custom_connector: Operators supported by the custom connector.
            :param datadog: The operation to be performed on the provided Datadog source fields.
            :param dynatrace: The operation to be performed on the provided Dynatrace source fields.
            :param google_analytics: The operation to be performed on the provided Google Analytics source fields.
            :param infor_nexus: The operation to be performed on the provided Infor Nexus source fields.
            :param marketo: The operation to be performed on the provided Marketo source fields.
            :param s3: The operation to be performed on the provided Amazon S3 source fields.
            :param salesforce: The operation to be performed on the provided Salesforce source fields.
            :param sapo_data: The operation to be performed on the provided SAPOData source fields.
            :param service_now: The operation to be performed on the provided ServiceNow source fields.
            :param singular: The operation to be performed on the provided Singular source fields.
            :param slack: The operation to be performed on the provided Slack source fields.
            :param trendmicro: The operation to be performed on the provided Trend Micro source fields.
            :param veeva: The operation to be performed on the provided Veeva source fields.
            :param zendesk: The operation to be performed on the provided Zendesk source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                connector_operator_property = appflow.CfnFlow.ConnectorOperatorProperty(
                    amplitude="amplitude",
                    custom_connector="customConnector",
                    datadog="datadog",
                    dynatrace="dynatrace",
                    google_analytics="googleAnalytics",
                    infor_nexus="inforNexus",
                    marketo="marketo",
                    s3="s3",
                    salesforce="salesforce",
                    sapo_data="sapoData",
                    service_now="serviceNow",
                    singular="singular",
                    slack="slack",
                    trendmicro="trendmicro",
                    veeva="veeva",
                    zendesk="zendesk"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2bae7a1401a59026a310dd47b48386a01301301fdf23c8bfc8af45b341b809a3)
                check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
                check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
                check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
                check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
                check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
                check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
                check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
                check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
                check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amplitude is not None:
                self._values["amplitude"] = amplitude
            if custom_connector is not None:
                self._values["custom_connector"] = custom_connector
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if google_analytics is not None:
                self._values["google_analytics"] = google_analytics
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if sapo_data is not None:
                self._values["sapo_data"] = sapo_data
            if service_now is not None:
                self._values["service_now"] = service_now
            if singular is not None:
                self._values["singular"] = singular
            if slack is not None:
                self._values["slack"] = slack
            if trendmicro is not None:
                self._values["trendmicro"] = trendmicro
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def amplitude(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Amplitude source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-amplitude
            '''
            result = self._values.get("amplitude")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_connector(self) -> typing.Optional[builtins.str]:
            '''Operators supported by the custom connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-customconnector
            '''
            result = self._values.get("custom_connector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def datadog(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Datadog source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dynatrace(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Dynatrace source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def google_analytics(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Google Analytics source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-googleanalytics
            '''
            result = self._values.get("google_analytics")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def infor_nexus(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Infor Nexus source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def marketo(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Marketo source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Amazon S3 source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def salesforce(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Salesforce source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sapo_data(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided SAPOData source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-sapodata
            '''
            result = self._values.get("sapo_data")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_now(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided ServiceNow source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def singular(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Singular source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-singular
            '''
            result = self._values.get("singular")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slack(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Slack source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trendmicro(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Trend Micro source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-trendmicro
            '''
            result = self._values.get("trendmicro")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def veeva(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Veeva source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zendesk(self) -> typing.Optional[builtins.str]:
            '''The operation to be performed on the provided Zendesk source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorOperatorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.CustomConnectorDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "entity_name": "entityName",
            "custom_properties": "customProperties",
            "error_handling_config": "errorHandlingConfig",
            "id_field_names": "idFieldNames",
            "write_operation_type": "writeOperationType",
        },
    )
    class CustomConnectorDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            entity_name: builtins.str,
            custom_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
            error_handling_config: typing.Optional[typing.Union[typing.Union["CfnFlow.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            write_operation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when the custom connector is being used as a destination.

            :param entity_name: The entity specified in the custom connector as a destination in the flow.
            :param custom_properties: The custom properties that are specific to the connector when it's used as a destination in the flow.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the custom connector as destination.
            :param id_field_names: The name of the field that Amazon AppFlow uses as an ID when performing a write operation such as update, delete, or upsert.
            :param write_operation_type: Specifies the type of write operation to be performed in the custom connector when it's used as destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                custom_connector_destination_properties_property = appflow.CfnFlow.CustomConnectorDestinationPropertiesProperty(
                    entity_name="entityName",
                
                    # the properties below are optional
                    custom_properties={
                        "custom_properties_key": "customProperties"
                    },
                    error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    id_field_names=["idFieldNames"],
                    write_operation_type="writeOperationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c8d3f37050c188e7c5decca80efb64b67ea330c8e4327166144cb1b5b2ed031)
                check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
                check_type(argname="argument custom_properties", value=custom_properties, expected_type=type_hints["custom_properties"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
                check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "entity_name": entity_name,
            }
            if custom_properties is not None:
                self._values["custom_properties"] = custom_properties
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if id_field_names is not None:
                self._values["id_field_names"] = id_field_names
            if write_operation_type is not None:
                self._values["write_operation_type"] = write_operation_type

        @builtins.property
        def entity_name(self) -> builtins.str:
            '''The entity specified in the custom connector as a destination in the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html#cfn-appflow-flow-customconnectordestinationproperties-entityname
            '''
            result = self._values.get("entity_name")
            assert result is not None, "Required property 'entity_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def custom_properties(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''The custom properties that are specific to the connector when it's used as a destination in the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html#cfn-appflow-flow-customconnectordestinationproperties-customproperties
            '''
            result = self._values.get("custom_properties")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the custom connector as destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html#cfn-appflow-flow-customconnectordestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The name of the field that Amazon AppFlow uses as an ID when performing a write operation such as update, delete, or upsert.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html#cfn-appflow-flow-customconnectordestinationproperties-idfieldnames
            '''
            result = self._values.get("id_field_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def write_operation_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of write operation to be performed in the custom connector when it's used as destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectordestinationproperties.html#cfn-appflow-flow-customconnectordestinationproperties-writeoperationtype
            '''
            result = self._values.get("write_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomConnectorDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.CustomConnectorSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "entity_name": "entityName",
            "custom_properties": "customProperties",
        },
    )
    class CustomConnectorSourcePropertiesProperty:
        def __init__(
            self,
            *,
            entity_name: builtins.str,
            custom_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''The properties that are applied when the custom connector is being used as a source.

            :param entity_name: The entity specified in the custom connector as a source in the flow.
            :param custom_properties: Custom properties that are required to use the custom connector as a source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectorsourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                custom_connector_source_properties_property = appflow.CfnFlow.CustomConnectorSourcePropertiesProperty(
                    entity_name="entityName",
                
                    # the properties below are optional
                    custom_properties={
                        "custom_properties_key": "customProperties"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40d6ac27e49c2dd0458091139952cd62cb3292e9da5dc884e4ce91b1b9a2bc0f)
                check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
                check_type(argname="argument custom_properties", value=custom_properties, expected_type=type_hints["custom_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "entity_name": entity_name,
            }
            if custom_properties is not None:
                self._values["custom_properties"] = custom_properties

        @builtins.property
        def entity_name(self) -> builtins.str:
            '''The entity specified in the custom connector as a source in the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectorsourceproperties.html#cfn-appflow-flow-customconnectorsourceproperties-entityname
            '''
            result = self._values.get("entity_name")
            assert result is not None, "Required property 'entity_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def custom_properties(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''Custom properties that are required to use the custom connector as a source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-customconnectorsourceproperties.html#cfn-appflow-flow-customconnectorsourceproperties-customproperties
            '''
            result = self._values.get("custom_properties")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomConnectorSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.DatadogSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class DatadogSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when Datadog is being used as a source.

            :param object: The object specified in the Datadog flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-datadogsourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                datadog_source_properties_property = appflow.CfnFlow.DatadogSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94a9fff97e3b1089c64e09c2cd137e1970a19b0a7d009f33488cdebea7ec6626)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Datadog flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-datadogsourceproperties.html#cfn-appflow-flow-datadogsourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatadogSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.DestinationConnectorPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_connector": "customConnector",
            "event_bridge": "eventBridge",
            "lookout_metrics": "lookoutMetrics",
            "marketo": "marketo",
            "redshift": "redshift",
            "s3": "s3",
            "salesforce": "salesforce",
            "sapo_data": "sapoData",
            "snowflake": "snowflake",
            "upsolver": "upsolver",
            "zendesk": "zendesk",
        },
    )
    class DestinationConnectorPropertiesProperty:
        def __init__(
            self,
            *,
            custom_connector: typing.Optional[typing.Union[typing.Union["CfnFlow.CustomConnectorDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            event_bridge: typing.Optional[typing.Union[typing.Union["CfnFlow.EventBridgeDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            lookout_metrics: typing.Optional[typing.Union[typing.Union["CfnFlow.LookoutMetricsDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            marketo: typing.Optional[typing.Union[typing.Union["CfnFlow.MarketoDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            redshift: typing.Optional[typing.Union[typing.Union["CfnFlow.RedshiftDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            s3: typing.Optional[typing.Union[typing.Union["CfnFlow.S3DestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            salesforce: typing.Optional[typing.Union[typing.Union["CfnFlow.SalesforceDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sapo_data: typing.Optional[typing.Union[typing.Union["CfnFlow.SAPODataDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            snowflake: typing.Optional[typing.Union[typing.Union["CfnFlow.SnowflakeDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            upsolver: typing.Optional[typing.Union[typing.Union["CfnFlow.UpsolverDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            zendesk: typing.Optional[typing.Union[typing.Union["CfnFlow.ZendeskDestinationPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''This stores the information that is required to query a particular connector.

            :param custom_connector: The properties that are required to query the custom Connector.
            :param event_bridge: The properties required to query Amazon EventBridge.
            :param lookout_metrics: The properties required to query Amazon Lookout for Metrics.
            :param marketo: The properties required to query Marketo.
            :param redshift: The properties required to query Amazon Redshift.
            :param s3: The properties required to query Amazon S3.
            :param salesforce: The properties required to query Salesforce.
            :param sapo_data: The properties required to query SAPOData.
            :param snowflake: The properties required to query Snowflake.
            :param upsolver: The properties required to query Upsolver.
            :param zendesk: The properties required to query Zendesk.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                destination_connector_properties_property = appflow.CfnFlow.DestinationConnectorPropertiesProperty(
                    custom_connector=appflow.CfnFlow.CustomConnectorDestinationPropertiesProperty(
                        entity_name="entityName",
                
                        # the properties below are optional
                        custom_properties={
                            "custom_properties_key": "customProperties"
                        },
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        write_operation_type="writeOperationType"
                    ),
                    event_bridge=appflow.CfnFlow.EventBridgeDestinationPropertiesProperty(
                        object="object",
                
                        # the properties below are optional
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        )
                    ),
                    lookout_metrics=appflow.CfnFlow.LookoutMetricsDestinationPropertiesProperty(
                        object="object"
                    ),
                    marketo=appflow.CfnFlow.MarketoDestinationPropertiesProperty(
                        object="object",
                
                        # the properties below are optional
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        )
                    ),
                    redshift=appflow.CfnFlow.RedshiftDestinationPropertiesProperty(
                        intermediate_bucket_name="intermediateBucketName",
                        object="object",
                
                        # the properties below are optional
                        bucket_prefix="bucketPrefix",
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        )
                    ),
                    s3=appflow.CfnFlow.S3DestinationPropertiesProperty(
                        bucket_name="bucketName",
                
                        # the properties below are optional
                        bucket_prefix="bucketPrefix",
                        s3_output_format_config=appflow.CfnFlow.S3OutputFormatConfigProperty(
                            aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                                aggregation_type="aggregationType",
                                target_file_size=123
                            ),
                            file_type="fileType",
                            prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                                path_prefix_hierarchy=["pathPrefixHierarchy"],
                                prefix_format="prefixFormat",
                                prefix_type="prefixType"
                            ),
                            preserve_source_data_typing=False
                        )
                    ),
                    salesforce=appflow.CfnFlow.SalesforceDestinationPropertiesProperty(
                        object="object",
                
                        # the properties below are optional
                        data_transfer_api="dataTransferApi",
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        write_operation_type="writeOperationType"
                    ),
                    sapo_data=appflow.CfnFlow.SAPODataDestinationPropertiesProperty(
                        object_path="objectPath",
                
                        # the properties below are optional
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        success_response_handling_config=appflow.CfnFlow.SuccessResponseHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix"
                        ),
                        write_operation_type="writeOperationType"
                    ),
                    snowflake=appflow.CfnFlow.SnowflakeDestinationPropertiesProperty(
                        intermediate_bucket_name="intermediateBucketName",
                        object="object",
                
                        # the properties below are optional
                        bucket_prefix="bucketPrefix",
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        )
                    ),
                    upsolver=appflow.CfnFlow.UpsolverDestinationPropertiesProperty(
                        bucket_name="bucketName",
                        s3_output_format_config=appflow.CfnFlow.UpsolverS3OutputFormatConfigProperty(
                            prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                                path_prefix_hierarchy=["pathPrefixHierarchy"],
                                prefix_format="prefixFormat",
                                prefix_type="prefixType"
                            ),
                
                            # the properties below are optional
                            aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                                aggregation_type="aggregationType",
                                target_file_size=123
                            ),
                            file_type="fileType"
                        ),
                
                        # the properties below are optional
                        bucket_prefix="bucketPrefix"
                    ),
                    zendesk=appflow.CfnFlow.ZendeskDestinationPropertiesProperty(
                        object="object",
                
                        # the properties below are optional
                        error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                            fail_on_first_error=False
                        ),
                        id_field_names=["idFieldNames"],
                        write_operation_type="writeOperationType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbbcb54157230c34afc753ec9e1ac4c545ae4d9ac4f10efe680101457e884d47)
                check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
                check_type(argname="argument event_bridge", value=event_bridge, expected_type=type_hints["event_bridge"])
                check_type(argname="argument lookout_metrics", value=lookout_metrics, expected_type=type_hints["lookout_metrics"])
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
                check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
                check_type(argname="argument upsolver", value=upsolver, expected_type=type_hints["upsolver"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_connector is not None:
                self._values["custom_connector"] = custom_connector
            if event_bridge is not None:
                self._values["event_bridge"] = event_bridge
            if lookout_metrics is not None:
                self._values["lookout_metrics"] = lookout_metrics
            if marketo is not None:
                self._values["marketo"] = marketo
            if redshift is not None:
                self._values["redshift"] = redshift
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if sapo_data is not None:
                self._values["sapo_data"] = sapo_data
            if snowflake is not None:
                self._values["snowflake"] = snowflake
            if upsolver is not None:
                self._values["upsolver"] = upsolver
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def custom_connector(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.CustomConnectorDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties that are required to query the custom Connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-customconnector
            '''
            result = self._values.get("custom_connector")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.CustomConnectorDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def event_bridge(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.EventBridgeDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required to query Amazon EventBridge.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-eventbridge
            '''
            result = self._values.get("event_bridge")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.EventBridgeDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def lookout_metrics(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.LookoutMetricsDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required to query Amazon Lookout for Metrics.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-lookoutmetrics
            '''
            result = self._values.get("lookout_metrics")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.LookoutMetricsDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.MarketoDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required to query Marketo.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.MarketoDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def redshift(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.RedshiftDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required to query Amazon Redshift.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-redshift
            '''
            result = self._values.get("redshift")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.RedshiftDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.S3DestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required to query Amazon S3.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.S3DestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SalesforceDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required to query Salesforce.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SalesforceDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sapo_data(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SAPODataDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required to query SAPOData.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-sapodata
            '''
            result = self._values.get("sapo_data")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SAPODataDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def snowflake(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SnowflakeDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required to query Snowflake.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-snowflake
            '''
            result = self._values.get("snowflake")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SnowflakeDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def upsolver(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.UpsolverDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required to query Upsolver.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-upsolver
            '''
            result = self._values.get("upsolver")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.UpsolverDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ZendeskDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties required to query Zendesk.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ZendeskDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConnectorPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.DestinationFlowConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_type": "connectorType",
            "destination_connector_properties": "destinationConnectorProperties",
            "api_version": "apiVersion",
            "connector_profile_name": "connectorProfileName",
        },
    )
    class DestinationFlowConfigProperty:
        def __init__(
            self,
            *,
            connector_type: builtins.str,
            destination_connector_properties: typing.Union[typing.Union["CfnFlow.DestinationConnectorPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            api_version: typing.Optional[builtins.str] = None,
            connector_profile_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the configuration of destination connectors present in the flow.

            :param connector_type: The type of destination connector, such as Sales force, Amazon S3, and so on. *Allowed Values* : ``EventBridge | Redshift | S3 | Salesforce | Snowflake``
            :param destination_connector_properties: This stores the information that is required to query a particular connector.
            :param api_version: The API version that the destination connector uses.
            :param connector_profile_name: The name of the connector profile. This name must be unique for each connector profile in the AWS account .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                destination_flow_config_property = appflow.CfnFlow.DestinationFlowConfigProperty(
                    connector_type="connectorType",
                    destination_connector_properties=appflow.CfnFlow.DestinationConnectorPropertiesProperty(
                        custom_connector=appflow.CfnFlow.CustomConnectorDestinationPropertiesProperty(
                            entity_name="entityName",
                
                            # the properties below are optional
                            custom_properties={
                                "custom_properties_key": "customProperties"
                            },
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            write_operation_type="writeOperationType"
                        ),
                        event_bridge=appflow.CfnFlow.EventBridgeDestinationPropertiesProperty(
                            object="object",
                
                            # the properties below are optional
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            )
                        ),
                        lookout_metrics=appflow.CfnFlow.LookoutMetricsDestinationPropertiesProperty(
                            object="object"
                        ),
                        marketo=appflow.CfnFlow.MarketoDestinationPropertiesProperty(
                            object="object",
                
                            # the properties below are optional
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            )
                        ),
                        redshift=appflow.CfnFlow.RedshiftDestinationPropertiesProperty(
                            intermediate_bucket_name="intermediateBucketName",
                            object="object",
                
                            # the properties below are optional
                            bucket_prefix="bucketPrefix",
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            )
                        ),
                        s3=appflow.CfnFlow.S3DestinationPropertiesProperty(
                            bucket_name="bucketName",
                
                            # the properties below are optional
                            bucket_prefix="bucketPrefix",
                            s3_output_format_config=appflow.CfnFlow.S3OutputFormatConfigProperty(
                                aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                                    aggregation_type="aggregationType",
                                    target_file_size=123
                                ),
                                file_type="fileType",
                                prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                                    path_prefix_hierarchy=["pathPrefixHierarchy"],
                                    prefix_format="prefixFormat",
                                    prefix_type="prefixType"
                                ),
                                preserve_source_data_typing=False
                            )
                        ),
                        salesforce=appflow.CfnFlow.SalesforceDestinationPropertiesProperty(
                            object="object",
                
                            # the properties below are optional
                            data_transfer_api="dataTransferApi",
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            write_operation_type="writeOperationType"
                        ),
                        sapo_data=appflow.CfnFlow.SAPODataDestinationPropertiesProperty(
                            object_path="objectPath",
                
                            # the properties below are optional
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            success_response_handling_config=appflow.CfnFlow.SuccessResponseHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix"
                            ),
                            write_operation_type="writeOperationType"
                        ),
                        snowflake=appflow.CfnFlow.SnowflakeDestinationPropertiesProperty(
                            intermediate_bucket_name="intermediateBucketName",
                            object="object",
                
                            # the properties below are optional
                            bucket_prefix="bucketPrefix",
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            )
                        ),
                        upsolver=appflow.CfnFlow.UpsolverDestinationPropertiesProperty(
                            bucket_name="bucketName",
                            s3_output_format_config=appflow.CfnFlow.UpsolverS3OutputFormatConfigProperty(
                                prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                                    path_prefix_hierarchy=["pathPrefixHierarchy"],
                                    prefix_format="prefixFormat",
                                    prefix_type="prefixType"
                                ),
                
                                # the properties below are optional
                                aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                                    aggregation_type="aggregationType",
                                    target_file_size=123
                                ),
                                file_type="fileType"
                            ),
                
                            # the properties below are optional
                            bucket_prefix="bucketPrefix"
                        ),
                        zendesk=appflow.CfnFlow.ZendeskDestinationPropertiesProperty(
                            object="object",
                
                            # the properties below are optional
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            write_operation_type="writeOperationType"
                        )
                    ),
                
                    # the properties below are optional
                    api_version="apiVersion",
                    connector_profile_name="connectorProfileName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94052587a94fbd68cffa3b927906ab33367359151648bce7d72e971bdf4efbb2)
                check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
                check_type(argname="argument destination_connector_properties", value=destination_connector_properties, expected_type=type_hints["destination_connector_properties"])
                check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
                check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "connector_type": connector_type,
                "destination_connector_properties": destination_connector_properties,
            }
            if api_version is not None:
                self._values["api_version"] = api_version
            if connector_profile_name is not None:
                self._values["connector_profile_name"] = connector_profile_name

        @builtins.property
        def connector_type(self) -> builtins.str:
            '''The type of destination connector, such as Sales force, Amazon S3, and so on.

            *Allowed Values* : ``EventBridge | Redshift | S3 | Salesforce | Snowflake``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-connectortype
            '''
            result = self._values.get("connector_type")
            assert result is not None, "Required property 'connector_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def destination_connector_properties(
            self,
        ) -> typing.Union["CfnFlow.DestinationConnectorPropertiesProperty", _IResolvable_a771d0ef]:
            '''This stores the information that is required to query a particular connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-destinationconnectorproperties
            '''
            result = self._values.get("destination_connector_properties")
            assert result is not None, "Required property 'destination_connector_properties' is missing"
            return typing.cast(typing.Union["CfnFlow.DestinationConnectorPropertiesProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def api_version(self) -> typing.Optional[builtins.str]:
            '''The API version that the destination connector uses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-apiversion
            '''
            result = self._values.get("api_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_profile_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connector profile.

            This name must be unique for each connector profile in the AWS account .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-connectorprofilename
            '''
            result = self._values.get("connector_profile_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationFlowConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.DynatraceSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class DynatraceSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when Dynatrace is being used as a source.

            :param object: The object specified in the Dynatrace flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-dynatracesourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                dynatrace_source_properties_property = appflow.CfnFlow.DynatraceSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e00986a8531c33079ebdc1d864270c7da97f2ef8b2eb991543bd83b424ff73b2)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Dynatrace flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-dynatracesourceproperties.html#cfn-appflow-flow-dynatracesourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ErrorHandlingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "fail_on_first_error": "failOnFirstError",
        },
    )
    class ErrorHandlingConfigProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            fail_on_first_error: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :param bucket_name: Specifies the name of the Amazon S3 bucket.
            :param bucket_prefix: Specifies the Amazon S3 bucket prefix.
            :param fail_on_first_error: Specifies if the flow should fail after the first instance of a failure when attempting to place data in the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                error_handling_config_property = appflow.CfnFlow.ErrorHandlingConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    fail_on_first_error=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe610b6f7899b376c5f5cf2b1174b8f6fa5089598754d8409551f868e9423448)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument fail_on_first_error", value=fail_on_first_error, expected_type=type_hints["fail_on_first_error"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if fail_on_first_error is not None:
                self._values["fail_on_first_error"] = fail_on_first_error

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Specifies the name of the Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html#cfn-appflow-flow-errorhandlingconfig-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''Specifies the Amazon S3 bucket prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html#cfn-appflow-flow-errorhandlingconfig-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fail_on_first_error(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies if the flow should fail after the first instance of a failure when attempting to place data in the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html#cfn-appflow-flow-errorhandlingconfig-failonfirsterror
            '''
            result = self._values.get("fail_on_first_error")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorHandlingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.EventBridgeDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object": "object",
            "error_handling_config": "errorHandlingConfig",
        },
    )
    class EventBridgeDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            object: builtins.str,
            error_handling_config: typing.Optional[typing.Union[typing.Union["CfnFlow.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The properties that are applied when Amazon EventBridge is being used as a destination.

            :param object: The object specified in the Amazon EventBridge flow destination.
            :param error_handling_config: The object specified in the Amplitude flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-eventbridgedestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                event_bridge_destination_properties_property = appflow.CfnFlow.EventBridgeDestinationPropertiesProperty(
                    object="object",
                
                    # the properties below are optional
                    error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be1fa81722b4ab8c8337bffafe926c81784b5b2b3e7188c84d5f4ffa6b02f13c)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Amazon EventBridge flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-eventbridgedestinationproperties.html#cfn-appflow-flow-eventbridgedestinationproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''The object specified in the Amplitude flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-eventbridgedestinationproperties.html#cfn-appflow-flow-eventbridgedestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.GlueDataCatalogProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_name": "databaseName",
            "role_arn": "roleArn",
            "table_prefix": "tablePrefix",
        },
    )
    class GlueDataCatalogProperty:
        def __init__(
            self,
            *,
            database_name: builtins.str,
            role_arn: builtins.str,
            table_prefix: builtins.str,
        ) -> None:
            '''
            :param database_name: ``CfnFlow.GlueDataCatalogProperty.DatabaseName``.
            :param role_arn: ``CfnFlow.GlueDataCatalogProperty.RoleArn``.
            :param table_prefix: ``CfnFlow.GlueDataCatalogProperty.TablePrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-gluedatacatalog.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                glue_data_catalog_property = appflow.CfnFlow.GlueDataCatalogProperty(
                    database_name="databaseName",
                    role_arn="roleArn",
                    table_prefix="tablePrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b8627d1babee7f65f296693bb422153e01c8dd719cf94878c5db73fb6d9576ea)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "database_name": database_name,
                "role_arn": role_arn,
                "table_prefix": table_prefix,
            }

        @builtins.property
        def database_name(self) -> builtins.str:
            '''``CfnFlow.GlueDataCatalogProperty.DatabaseName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-gluedatacatalog.html#cfn-appflow-flow-gluedatacatalog-databasename
            '''
            result = self._values.get("database_name")
            assert result is not None, "Required property 'database_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''``CfnFlow.GlueDataCatalogProperty.RoleArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-gluedatacatalog.html#cfn-appflow-flow-gluedatacatalog-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def table_prefix(self) -> builtins.str:
            '''``CfnFlow.GlueDataCatalogProperty.TablePrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-gluedatacatalog.html#cfn-appflow-flow-gluedatacatalog-tableprefix
            '''
            result = self._values.get("table_prefix")
            assert result is not None, "Required property 'table_prefix' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueDataCatalogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.GoogleAnalyticsSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class GoogleAnalyticsSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when Google Analytics is being used as a source.

            :param object: The object specified in the Google Analytics flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-googleanalyticssourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                google_analytics_source_properties_property = appflow.CfnFlow.GoogleAnalyticsSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7330f49790ab7f1dd63ad225eb5b147b7443421aff90c9d1896a1b10166ef0df)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Google Analytics flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-googleanalyticssourceproperties.html#cfn-appflow-flow-googleanalyticssourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GoogleAnalyticsSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.IncrementalPullConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"datetime_type_field_name": "datetimeTypeFieldName"},
    )
    class IncrementalPullConfigProperty:
        def __init__(
            self,
            *,
            datetime_type_field_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration used when importing incremental records from the source.

            :param datetime_type_field_name: A field that specifies the date time or timestamp field as the criteria to use when importing incremental records from the source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-incrementalpullconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                incremental_pull_config_property = appflow.CfnFlow.IncrementalPullConfigProperty(
                    datetime_type_field_name="datetimeTypeFieldName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90b934240d253719aa264a533d4c3b2b87aab1e5506d4a674631de412614ab15)
                check_type(argname="argument datetime_type_field_name", value=datetime_type_field_name, expected_type=type_hints["datetime_type_field_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if datetime_type_field_name is not None:
                self._values["datetime_type_field_name"] = datetime_type_field_name

        @builtins.property
        def datetime_type_field_name(self) -> typing.Optional[builtins.str]:
            '''A field that specifies the date time or timestamp field as the criteria to use when importing incremental records from the source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-incrementalpullconfig.html#cfn-appflow-flow-incrementalpullconfig-datetimetypefieldname
            '''
            result = self._values.get("datetime_type_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IncrementalPullConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.InforNexusSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class InforNexusSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when Infor Nexus is being used as a source.

            :param object: The object specified in the Infor Nexus flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-infornexussourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                infor_nexus_source_properties_property = appflow.CfnFlow.InforNexusSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54fe00e26bc12c3a7aeaf2a61c2dd069aa260c3faff8341531b3291980376c91)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Infor Nexus flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-infornexussourceproperties.html#cfn-appflow-flow-infornexussourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InforNexusSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.LookoutMetricsDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class LookoutMetricsDestinationPropertiesProperty:
        def __init__(self, *, object: typing.Optional[builtins.str] = None) -> None:
            '''The properties that are applied when Amazon Lookout for Metrics is used as a destination.

            :param object: The object specified in the Amazon Lookout for Metrics flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-lookoutmetricsdestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                lookout_metrics_destination_properties_property = appflow.CfnFlow.LookoutMetricsDestinationPropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a950d336f3a8d36e0a4e1ee6fe0c5b1b4ffdb03679b615896f9603b7ebd42ef)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object is not None:
                self._values["object"] = object

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The object specified in the Amazon Lookout for Metrics flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-lookoutmetricsdestinationproperties.html#cfn-appflow-flow-lookoutmetricsdestinationproperties-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LookoutMetricsDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.MarketoDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object": "object",
            "error_handling_config": "errorHandlingConfig",
        },
    )
    class MarketoDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            object: builtins.str,
            error_handling_config: typing.Optional[typing.Union[typing.Union["CfnFlow.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The properties that Amazon AppFlow applies when you use Marketo as a flow destination.

            :param object: The object specified in the Marketo flow destination.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketodestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                marketo_destination_properties_property = appflow.CfnFlow.MarketoDestinationPropertiesProperty(
                    object="object",
                
                    # the properties below are optional
                    error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__058ac5ad26c35ae3470a019a6301ebc8685522b1ab68359be4cad94a85bfb523)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Marketo flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketodestinationproperties.html#cfn-appflow-flow-marketodestinationproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketodestinationproperties.html#cfn-appflow-flow-marketodestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.MarketoSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class MarketoSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when Marketo is being used as a source.

            :param object: The object specified in the Marketo flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketosourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                marketo_source_properties_property = appflow.CfnFlow.MarketoSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__389474f6f1601bd5590fbb5b19bcb38f1bf454c696677736a6fe5c554129c4e3)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Marketo flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketosourceproperties.html#cfn-appflow-flow-marketosourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.MetadataCatalogConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"glue_data_catalog": "glueDataCatalog"},
    )
    class MetadataCatalogConfigProperty:
        def __init__(
            self,
            *,
            glue_data_catalog: typing.Optional[typing.Union[typing.Union["CfnFlow.GlueDataCatalogProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies the configuration that Amazon AppFlow uses when it catalogs your data.

            When Amazon AppFlow catalogs your data, it stores metadata in a data catalog.

            :param glue_data_catalog: Specifies the configuration that Amazon AppFlow uses when it catalogs your data with the AWS Glue Data Catalog .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-metadatacatalogconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                metadata_catalog_config_property = appflow.CfnFlow.MetadataCatalogConfigProperty(
                    glue_data_catalog=appflow.CfnFlow.GlueDataCatalogProperty(
                        database_name="databaseName",
                        role_arn="roleArn",
                        table_prefix="tablePrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5333a0f2cf102f80173da134345cdc5b979535301620812aa2184cb07e16f7d)
                check_type(argname="argument glue_data_catalog", value=glue_data_catalog, expected_type=type_hints["glue_data_catalog"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if glue_data_catalog is not None:
                self._values["glue_data_catalog"] = glue_data_catalog

        @builtins.property
        def glue_data_catalog(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.GlueDataCatalogProperty", _IResolvable_a771d0ef]]:
            '''Specifies the configuration that Amazon AppFlow uses when it catalogs your data with the AWS Glue Data Catalog .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-metadatacatalogconfig.html#cfn-appflow-flow-metadatacatalogconfig-gluedatacatalog
            '''
            result = self._values.get("glue_data_catalog")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.GlueDataCatalogProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataCatalogConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.PrefixConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "path_prefix_hierarchy": "pathPrefixHierarchy",
            "prefix_format": "prefixFormat",
            "prefix_type": "prefixType",
        },
    )
    class PrefixConfigProperty:
        def __init__(
            self,
            *,
            path_prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
            prefix_format: typing.Optional[builtins.str] = None,
            prefix_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies elements that Amazon AppFlow includes in the file and folder names in the flow destination.

            :param path_prefix_hierarchy: Specifies whether the destination file path includes either or both of the following elements:. - **EXECUTION_ID** - The ID that Amazon AppFlow assigns to the flow run. - **SCHEMA_VERSION** - The version number of your data schema. Amazon AppFlow assigns this version number. The version number increases by one when you change any of the following settings in your flow configuration: - Source-to-destination field mappings - Field data types - Partition keys
            :param prefix_format: Determines the level of granularity for the date and time that's included in the prefix.
            :param prefix_type: Determines the format of the prefix, and whether it applies to the file name, file path, or both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                prefix_config_property = appflow.CfnFlow.PrefixConfigProperty(
                    path_prefix_hierarchy=["pathPrefixHierarchy"],
                    prefix_format="prefixFormat",
                    prefix_type="prefixType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe807b70844271724d9e74132427ef742073ad7e9310506532e594a065842e9c)
                check_type(argname="argument path_prefix_hierarchy", value=path_prefix_hierarchy, expected_type=type_hints["path_prefix_hierarchy"])
                check_type(argname="argument prefix_format", value=prefix_format, expected_type=type_hints["prefix_format"])
                check_type(argname="argument prefix_type", value=prefix_type, expected_type=type_hints["prefix_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if path_prefix_hierarchy is not None:
                self._values["path_prefix_hierarchy"] = path_prefix_hierarchy
            if prefix_format is not None:
                self._values["prefix_format"] = prefix_format
            if prefix_type is not None:
                self._values["prefix_type"] = prefix_type

        @builtins.property
        def path_prefix_hierarchy(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies whether the destination file path includes either or both of the following elements:.

            - **EXECUTION_ID** - The ID that Amazon AppFlow assigns to the flow run.
            - **SCHEMA_VERSION** - The version number of your data schema. Amazon AppFlow assigns this version number. The version number increases by one when you change any of the following settings in your flow configuration:
            - Source-to-destination field mappings
            - Field data types
            - Partition keys

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html#cfn-appflow-flow-prefixconfig-pathprefixhierarchy
            '''
            result = self._values.get("path_prefix_hierarchy")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def prefix_format(self) -> typing.Optional[builtins.str]:
            '''Determines the level of granularity for the date and time that's included in the prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html#cfn-appflow-flow-prefixconfig-prefixformat
            '''
            result = self._values.get("prefix_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix_type(self) -> typing.Optional[builtins.str]:
            '''Determines the format of the prefix, and whether it applies to the file name, file path, or both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html#cfn-appflow-flow-prefixconfig-prefixtype
            '''
            result = self._values.get("prefix_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrefixConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.RedshiftDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "intermediate_bucket_name": "intermediateBucketName",
            "object": "object",
            "bucket_prefix": "bucketPrefix",
            "error_handling_config": "errorHandlingConfig",
        },
    )
    class RedshiftDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            intermediate_bucket_name: builtins.str,
            object: builtins.str,
            bucket_prefix: typing.Optional[builtins.str] = None,
            error_handling_config: typing.Optional[typing.Union[typing.Union["CfnFlow.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The properties that are applied when Amazon Redshift is being used as a destination.

            :param intermediate_bucket_name: The intermediate bucket that Amazon AppFlow uses when moving data into Amazon Redshift.
            :param object: The object specified in the Amazon Redshift flow destination.
            :param bucket_prefix: The object key for the bucket in which Amazon AppFlow places the destination files.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the Amazon Redshift destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                redshift_destination_properties_property = appflow.CfnFlow.RedshiftDestinationPropertiesProperty(
                    intermediate_bucket_name="intermediateBucketName",
                    object="object",
                
                    # the properties below are optional
                    bucket_prefix="bucketPrefix",
                    error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0cff64b64c9128d2fb298e4baa58910381f4c6d360790808501593257ea3456)
                check_type(argname="argument intermediate_bucket_name", value=intermediate_bucket_name, expected_type=type_hints["intermediate_bucket_name"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "intermediate_bucket_name": intermediate_bucket_name,
                "object": object,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config

        @builtins.property
        def intermediate_bucket_name(self) -> builtins.str:
            '''The intermediate bucket that Amazon AppFlow uses when moving data into Amazon Redshift.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-intermediatebucketname
            '''
            result = self._values.get("intermediate_bucket_name")
            assert result is not None, "Required property 'intermediate_bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Amazon Redshift flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the bucket in which Amazon AppFlow places the destination files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the Amazon Redshift destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.S3DestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "s3_output_format_config": "s3OutputFormatConfig",
        },
    )
    class S3DestinationPropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            bucket_prefix: typing.Optional[builtins.str] = None,
            s3_output_format_config: typing.Optional[typing.Union[typing.Union["CfnFlow.S3OutputFormatConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The properties that are applied when Amazon S3 is used as a destination.

            :param bucket_name: The Amazon S3 bucket name in which Amazon AppFlow places the transferred data.
            :param bucket_prefix: The object key for the destination bucket in which Amazon AppFlow places the files.
            :param s3_output_format_config: The configuration that determines how Amazon AppFlow should format the flow output data when Amazon S3 is used as the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                s3_destination_properties_property = appflow.CfnFlow.S3DestinationPropertiesProperty(
                    bucket_name="bucketName",
                
                    # the properties below are optional
                    bucket_prefix="bucketPrefix",
                    s3_output_format_config=appflow.CfnFlow.S3OutputFormatConfigProperty(
                        aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                            aggregation_type="aggregationType",
                            target_file_size=123
                        ),
                        file_type="fileType",
                        prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                            path_prefix_hierarchy=["pathPrefixHierarchy"],
                            prefix_format="prefixFormat",
                            prefix_type="prefixType"
                        ),
                        preserve_source_data_typing=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02c7a4861db207389a59210e3d58a59ed0429584c3732b7368f3ee94ae03cc04)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument s3_output_format_config", value=s3_output_format_config, expected_type=type_hints["s3_output_format_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if s3_output_format_config is not None:
                self._values["s3_output_format_config"] = s3_output_format_config

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The Amazon S3 bucket name in which Amazon AppFlow places the transferred data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html#cfn-appflow-flow-s3destinationproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the destination bucket in which Amazon AppFlow places the files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html#cfn-appflow-flow-s3destinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_output_format_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.S3OutputFormatConfigProperty", _IResolvable_a771d0ef]]:
            '''The configuration that determines how Amazon AppFlow should format the flow output data when Amazon S3 is used as the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html#cfn-appflow-flow-s3destinationproperties-s3outputformatconfig
            '''
            result = self._values.get("s3_output_format_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.S3OutputFormatConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.S3InputFormatConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_input_file_type": "s3InputFileType"},
    )
    class S3InputFormatConfigProperty:
        def __init__(
            self,
            *,
            s3_input_file_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When you use Amazon S3 as the source, the configuration format that you provide the flow input data.

            :param s3_input_file_type: The file type that Amazon AppFlow gets from your Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3inputformatconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                s3_input_format_config_property = appflow.CfnFlow.S3InputFormatConfigProperty(
                    s3_input_file_type="s3InputFileType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d84bcadb90cc9c9d021f2d7040ac3a4d7ef5688aeb18fb00a5efca87c55b554a)
                check_type(argname="argument s3_input_file_type", value=s3_input_file_type, expected_type=type_hints["s3_input_file_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_input_file_type is not None:
                self._values["s3_input_file_type"] = s3_input_file_type

        @builtins.property
        def s3_input_file_type(self) -> typing.Optional[builtins.str]:
            '''The file type that Amazon AppFlow gets from your Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3inputformatconfig.html#cfn-appflow-flow-s3inputformatconfig-s3inputfiletype
            '''
            result = self._values.get("s3_input_file_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3InputFormatConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.S3OutputFormatConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation_config": "aggregationConfig",
            "file_type": "fileType",
            "prefix_config": "prefixConfig",
            "preserve_source_data_typing": "preserveSourceDataTyping",
        },
    )
    class S3OutputFormatConfigProperty:
        def __init__(
            self,
            *,
            aggregation_config: typing.Optional[typing.Union[typing.Union["CfnFlow.AggregationConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            file_type: typing.Optional[builtins.str] = None,
            prefix_config: typing.Optional[typing.Union[typing.Union["CfnFlow.PrefixConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            preserve_source_data_typing: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The configuration that determines how Amazon AppFlow should format the flow output data when Amazon S3 is used as the destination.

            :param aggregation_config: The aggregation settings that you can use to customize the output format of your flow data.
            :param file_type: Indicates the file type that Amazon AppFlow places in the Amazon S3 bucket.
            :param prefix_config: Determines the prefix that Amazon AppFlow applies to the folder name in the Amazon S3 bucket. You can name folders according to the flow frequency and date.
            :param preserve_source_data_typing: ``CfnFlow.S3OutputFormatConfigProperty.PreserveSourceDataTyping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                s3_output_format_config_property = appflow.CfnFlow.S3OutputFormatConfigProperty(
                    aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                        aggregation_type="aggregationType",
                        target_file_size=123
                    ),
                    file_type="fileType",
                    prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                        path_prefix_hierarchy=["pathPrefixHierarchy"],
                        prefix_format="prefixFormat",
                        prefix_type="prefixType"
                    ),
                    preserve_source_data_typing=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ebf7b7e6a439a254fa59b7671858e0a6aaf563655c691af16b5ca4a725e891a5)
                check_type(argname="argument aggregation_config", value=aggregation_config, expected_type=type_hints["aggregation_config"])
                check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
                check_type(argname="argument prefix_config", value=prefix_config, expected_type=type_hints["prefix_config"])
                check_type(argname="argument preserve_source_data_typing", value=preserve_source_data_typing, expected_type=type_hints["preserve_source_data_typing"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregation_config is not None:
                self._values["aggregation_config"] = aggregation_config
            if file_type is not None:
                self._values["file_type"] = file_type
            if prefix_config is not None:
                self._values["prefix_config"] = prefix_config
            if preserve_source_data_typing is not None:
                self._values["preserve_source_data_typing"] = preserve_source_data_typing

        @builtins.property
        def aggregation_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.AggregationConfigProperty", _IResolvable_a771d0ef]]:
            '''The aggregation settings that you can use to customize the output format of your flow data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-aggregationconfig
            '''
            result = self._values.get("aggregation_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.AggregationConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def file_type(self) -> typing.Optional[builtins.str]:
            '''Indicates the file type that Amazon AppFlow places in the Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-filetype
            '''
            result = self._values.get("file_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.PrefixConfigProperty", _IResolvable_a771d0ef]]:
            '''Determines the prefix that Amazon AppFlow applies to the folder name in the Amazon S3 bucket.

            You can name folders according to the flow frequency and date.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-prefixconfig
            '''
            result = self._values.get("prefix_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.PrefixConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def preserve_source_data_typing(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFlow.S3OutputFormatConfigProperty.PreserveSourceDataTyping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-preservesourcedatatyping
            '''
            result = self._values.get("preserve_source_data_typing")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3OutputFormatConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.S3SourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "s3_input_format_config": "s3InputFormatConfig",
        },
    )
    class S3SourcePropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            bucket_prefix: builtins.str,
            s3_input_format_config: typing.Optional[typing.Union[typing.Union["CfnFlow.S3InputFormatConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The properties that are applied when Amazon S3 is being used as the flow source.

            :param bucket_name: The Amazon S3 bucket name where the source files are stored.
            :param bucket_prefix: The object key for the Amazon S3 bucket in which the source files are stored.
            :param s3_input_format_config: When you use Amazon S3 as the source, the configuration format that you provide the flow input data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                s3_source_properties_property = appflow.CfnFlow.S3SourcePropertiesProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                
                    # the properties below are optional
                    s3_input_format_config=appflow.CfnFlow.S3InputFormatConfigProperty(
                        s3_input_file_type="s3InputFileType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58f1c227c28403417018ff3eca1cfd15f7fe47a3d0489b982e89862031f06b25)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument s3_input_format_config", value=s3_input_format_config, expected_type=type_hints["s3_input_format_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
                "bucket_prefix": bucket_prefix,
            }
            if s3_input_format_config is not None:
                self._values["s3_input_format_config"] = s3_input_format_config

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The Amazon S3 bucket name where the source files are stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html#cfn-appflow-flow-s3sourceproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> builtins.str:
            '''The object key for the Amazon S3 bucket in which the source files are stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html#cfn-appflow-flow-s3sourceproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            assert result is not None, "Required property 'bucket_prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_input_format_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.S3InputFormatConfigProperty", _IResolvable_a771d0ef]]:
            '''When you use Amazon S3 as the source, the configuration format that you provide the flow input data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html#cfn-appflow-flow-s3sourceproperties-s3inputformatconfig
            '''
            result = self._values.get("s3_input_format_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.S3InputFormatConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3SourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SAPODataDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object_path": "objectPath",
            "error_handling_config": "errorHandlingConfig",
            "id_field_names": "idFieldNames",
            "success_response_handling_config": "successResponseHandlingConfig",
            "write_operation_type": "writeOperationType",
        },
    )
    class SAPODataDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            object_path: builtins.str,
            error_handling_config: typing.Optional[typing.Union[typing.Union["CfnFlow.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            success_response_handling_config: typing.Optional[typing.Union[typing.Union["CfnFlow.SuccessResponseHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            write_operation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when using SAPOData as a flow destination.

            :param object_path: The object path specified in the SAPOData flow destination.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.
            :param id_field_names: A list of field names that can be used as an ID field when performing a write operation.
            :param success_response_handling_config: Determines how Amazon AppFlow handles the success response that it gets from the connector after placing data. For example, this setting would determine where to write the response from a destination connector upon a successful insert operation.
            :param write_operation_type: The possible write operations in the destination connector. When this value is not provided, this defaults to the ``INSERT`` operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                s_aPOData_destination_properties_property = appflow.CfnFlow.SAPODataDestinationPropertiesProperty(
                    object_path="objectPath",
                
                    # the properties below are optional
                    error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    id_field_names=["idFieldNames"],
                    success_response_handling_config=appflow.CfnFlow.SuccessResponseHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix"
                    ),
                    write_operation_type="writeOperationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7657b4410036725667a928e0439e362b9a0f634f91d5af6255341206302d1307)
                check_type(argname="argument object_path", value=object_path, expected_type=type_hints["object_path"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
                check_type(argname="argument success_response_handling_config", value=success_response_handling_config, expected_type=type_hints["success_response_handling_config"])
                check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object_path": object_path,
            }
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if id_field_names is not None:
                self._values["id_field_names"] = id_field_names
            if success_response_handling_config is not None:
                self._values["success_response_handling_config"] = success_response_handling_config
            if write_operation_type is not None:
                self._values["write_operation_type"] = write_operation_type

        @builtins.property
        def object_path(self) -> builtins.str:
            '''The object path specified in the SAPOData flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html#cfn-appflow-flow-sapodatadestinationproperties-objectpath
            '''
            result = self._values.get("object_path")
            assert result is not None, "Required property 'object_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html#cfn-appflow-flow-sapodatadestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of field names that can be used as an ID field when performing a write operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html#cfn-appflow-flow-sapodatadestinationproperties-idfieldnames
            '''
            result = self._values.get("id_field_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def success_response_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SuccessResponseHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''Determines how Amazon AppFlow handles the success response that it gets from the connector after placing data.

            For example, this setting would determine where to write the response from a destination connector upon a successful insert operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html#cfn-appflow-flow-sapodatadestinationproperties-successresponsehandlingconfig
            '''
            result = self._values.get("success_response_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SuccessResponseHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def write_operation_type(self) -> typing.Optional[builtins.str]:
            '''The possible write operations in the destination connector.

            When this value is not provided, this defaults to the ``INSERT`` operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatadestinationproperties.html#cfn-appflow-flow-sapodatadestinationproperties-writeoperationtype
            '''
            result = self._values.get("write_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAPODataDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SAPODataSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object_path": "objectPath"},
    )
    class SAPODataSourcePropertiesProperty:
        def __init__(self, *, object_path: builtins.str) -> None:
            '''The properties that are applied when using SAPOData as a flow source.

            :param object_path: The object path specified in the SAPOData flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatasourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                s_aPOData_source_properties_property = appflow.CfnFlow.SAPODataSourcePropertiesProperty(
                    object_path="objectPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__041d9138357a1a1234cab91e5fc76b79df1b59bb9cee37c96270c0c259e888ae)
                check_type(argname="argument object_path", value=object_path, expected_type=type_hints["object_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object_path": object_path,
            }

        @builtins.property
        def object_path(self) -> builtins.str:
            '''The object path specified in the SAPOData flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sapodatasourceproperties.html#cfn-appflow-flow-sapodatasourceproperties-objectpath
            '''
            result = self._values.get("object_path")
            assert result is not None, "Required property 'object_path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAPODataSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SalesforceDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object": "object",
            "data_transfer_api": "dataTransferApi",
            "error_handling_config": "errorHandlingConfig",
            "id_field_names": "idFieldNames",
            "write_operation_type": "writeOperationType",
        },
    )
    class SalesforceDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            object: builtins.str,
            data_transfer_api: typing.Optional[builtins.str] = None,
            error_handling_config: typing.Optional[typing.Union[typing.Union["CfnFlow.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            write_operation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Salesforce is being used as a destination.

            :param object: The object specified in the Salesforce flow destination.
            :param data_transfer_api: Specifies which Salesforce API is used by Amazon AppFlow when your flow transfers data to Salesforce. - **AUTOMATIC** - The default. Amazon AppFlow selects which API to use based on the number of records that your flow transfers to Salesforce. If your flow transfers fewer than 1,000 records, Amazon AppFlow uses Salesforce REST API. If your flow transfers 1,000 records or more, Amazon AppFlow uses Salesforce Bulk API 2.0. Each of these Salesforce APIs structures data differently. If Amazon AppFlow selects the API automatically, be aware that, for recurring flows, the data output might vary from one flow run to the next. For example, if a flow runs daily, it might use REST API on one day to transfer 900 records, and it might use Bulk API 2.0 on the next day to transfer 1,100 records. For each of these flow runs, the respective Salesforce API formats the data differently. Some of the differences include how dates are formatted and null values are represented. Also, Bulk API 2.0 doesn't transfer Salesforce compound fields. By choosing this option, you optimize flow performance for both small and large data transfers, but the tradeoff is inconsistent formatting in the output. - **BULKV2** - Amazon AppFlow uses only Salesforce Bulk API 2.0. This API runs asynchronous data transfers, and it's optimal for large sets of data. By choosing this option, you ensure that your flow writes consistent output, but you optimize performance only for large data transfers. Note that Bulk API 2.0 does not transfer Salesforce compound fields. - **REST_SYNC** - Amazon AppFlow uses only Salesforce REST API. By choosing this option, you ensure that your flow writes consistent output, but you decrease performance for large data transfers that are better suited for Bulk API 2.0. In some cases, if your flow attempts to transfer a vary large set of data, it might fail with a timed out error.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the Salesforce destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.
            :param id_field_names: The name of the field that Amazon AppFlow uses as an ID when performing a write operation such as update or delete.
            :param write_operation_type: This specifies the type of write operation to be performed in Salesforce. When the value is ``UPSERT`` , then ``idFieldNames`` is required.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                salesforce_destination_properties_property = appflow.CfnFlow.SalesforceDestinationPropertiesProperty(
                    object="object",
                
                    # the properties below are optional
                    data_transfer_api="dataTransferApi",
                    error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    id_field_names=["idFieldNames"],
                    write_operation_type="writeOperationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbc49be76541f78ae7d0704ff39b52b0ead403952e8a817d19676b73fc334448)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument data_transfer_api", value=data_transfer_api, expected_type=type_hints["data_transfer_api"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
                check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }
            if data_transfer_api is not None:
                self._values["data_transfer_api"] = data_transfer_api
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if id_field_names is not None:
                self._values["id_field_names"] = id_field_names
            if write_operation_type is not None:
                self._values["write_operation_type"] = write_operation_type

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Salesforce flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def data_transfer_api(self) -> typing.Optional[builtins.str]:
            '''Specifies which Salesforce API is used by Amazon AppFlow when your flow transfers data to Salesforce.

            - **AUTOMATIC** - The default. Amazon AppFlow selects which API to use based on the number of records that your flow transfers to Salesforce. If your flow transfers fewer than 1,000 records, Amazon AppFlow uses Salesforce REST API. If your flow transfers 1,000 records or more, Amazon AppFlow uses Salesforce Bulk API 2.0.

            Each of these Salesforce APIs structures data differently. If Amazon AppFlow selects the API automatically, be aware that, for recurring flows, the data output might vary from one flow run to the next. For example, if a flow runs daily, it might use REST API on one day to transfer 900 records, and it might use Bulk API 2.0 on the next day to transfer 1,100 records. For each of these flow runs, the respective Salesforce API formats the data differently. Some of the differences include how dates are formatted and null values are represented. Also, Bulk API 2.0 doesn't transfer Salesforce compound fields.

            By choosing this option, you optimize flow performance for both small and large data transfers, but the tradeoff is inconsistent formatting in the output.

            - **BULKV2** - Amazon AppFlow uses only Salesforce Bulk API 2.0. This API runs asynchronous data transfers, and it's optimal for large sets of data. By choosing this option, you ensure that your flow writes consistent output, but you optimize performance only for large data transfers.

            Note that Bulk API 2.0 does not transfer Salesforce compound fields.

            - **REST_SYNC** - Amazon AppFlow uses only Salesforce REST API. By choosing this option, you ensure that your flow writes consistent output, but you decrease performance for large data transfers that are better suited for Bulk API 2.0. In some cases, if your flow attempts to transfer a vary large set of data, it might fail with a timed out error.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-datatransferapi
            '''
            result = self._values.get("data_transfer_api")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the Salesforce destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The name of the field that Amazon AppFlow uses as an ID when performing a write operation such as update or delete.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-idfieldnames
            '''
            result = self._values.get("id_field_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def write_operation_type(self) -> typing.Optional[builtins.str]:
            '''This specifies the type of write operation to be performed in Salesforce.

            When the value is ``UPSERT`` , then ``idFieldNames`` is required.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-writeoperationtype
            '''
            result = self._values.get("write_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SalesforceSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object": "object",
            "data_transfer_api": "dataTransferApi",
            "enable_dynamic_field_update": "enableDynamicFieldUpdate",
            "include_deleted_records": "includeDeletedRecords",
        },
    )
    class SalesforceSourcePropertiesProperty:
        def __init__(
            self,
            *,
            object: builtins.str,
            data_transfer_api: typing.Optional[builtins.str] = None,
            enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            include_deleted_records: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The properties that are applied when Salesforce is being used as a source.

            :param object: The object specified in the Salesforce flow source.
            :param data_transfer_api: Specifies which Salesforce API is used by Amazon AppFlow when your flow transfers data from Salesforce. - **AUTOMATIC** - The default. Amazon AppFlow selects which API to use based on the number of records that your flow transfers from Salesforce. If your flow transfers fewer than 1,000,000 records, Amazon AppFlow uses Salesforce REST API. If your flow transfers 1,000,000 records or more, Amazon AppFlow uses Salesforce Bulk API 2.0. Each of these Salesforce APIs structures data differently. If Amazon AppFlow selects the API automatically, be aware that, for recurring flows, the data output might vary from one flow run to the next. For example, if a flow runs daily, it might use REST API on one day to transfer 900,000 records, and it might use Bulk API 2.0 on the next day to transfer 1,100,000 records. For each of these flow runs, the respective Salesforce API formats the data differently. Some of the differences include how dates are formatted and null values are represented. Also, Bulk API 2.0 doesn't transfer Salesforce compound fields. By choosing this option, you optimize flow performance for both small and large data transfers, but the tradeoff is inconsistent formatting in the output. - **BULKV2** - Amazon AppFlow uses only Salesforce Bulk API 2.0. This API runs asynchronous data transfers, and it's optimal for large sets of data. By choosing this option, you ensure that your flow writes consistent output, but you optimize performance only for large data transfers. Note that Bulk API 2.0 does not transfer Salesforce compound fields. - **REST_SYNC** - Amazon AppFlow uses only Salesforce REST API. By choosing this option, you ensure that your flow writes consistent output, but you decrease performance for large data transfers that are better suited for Bulk API 2.0. In some cases, if your flow attempts to transfer a vary large set of data, it might fail wituh a timed out error.
            :param enable_dynamic_field_update: The flag that enables dynamic fetching of new (recently added) fields in the Salesforce objects while running a flow.
            :param include_deleted_records: Indicates whether Amazon AppFlow includes deleted files in the flow run.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                salesforce_source_properties_property = appflow.CfnFlow.SalesforceSourcePropertiesProperty(
                    object="object",
                
                    # the properties below are optional
                    data_transfer_api="dataTransferApi",
                    enable_dynamic_field_update=False,
                    include_deleted_records=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__82e3295c4d0e1986be65d007de88364ddc4285a81aabce26509a9c4f6fdb0388)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument data_transfer_api", value=data_transfer_api, expected_type=type_hints["data_transfer_api"])
                check_type(argname="argument enable_dynamic_field_update", value=enable_dynamic_field_update, expected_type=type_hints["enable_dynamic_field_update"])
                check_type(argname="argument include_deleted_records", value=include_deleted_records, expected_type=type_hints["include_deleted_records"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }
            if data_transfer_api is not None:
                self._values["data_transfer_api"] = data_transfer_api
            if enable_dynamic_field_update is not None:
                self._values["enable_dynamic_field_update"] = enable_dynamic_field_update
            if include_deleted_records is not None:
                self._values["include_deleted_records"] = include_deleted_records

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Salesforce flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def data_transfer_api(self) -> typing.Optional[builtins.str]:
            '''Specifies which Salesforce API is used by Amazon AppFlow when your flow transfers data from Salesforce.

            - **AUTOMATIC** - The default. Amazon AppFlow selects which API to use based on the number of records that your flow transfers from Salesforce. If your flow transfers fewer than 1,000,000 records, Amazon AppFlow uses Salesforce REST API. If your flow transfers 1,000,000 records or more, Amazon AppFlow uses Salesforce Bulk API 2.0.

            Each of these Salesforce APIs structures data differently. If Amazon AppFlow selects the API automatically, be aware that, for recurring flows, the data output might vary from one flow run to the next. For example, if a flow runs daily, it might use REST API on one day to transfer 900,000 records, and it might use Bulk API 2.0 on the next day to transfer 1,100,000 records. For each of these flow runs, the respective Salesforce API formats the data differently. Some of the differences include how dates are formatted and null values are represented. Also, Bulk API 2.0 doesn't transfer Salesforce compound fields.

            By choosing this option, you optimize flow performance for both small and large data transfers, but the tradeoff is inconsistent formatting in the output.

            - **BULKV2** - Amazon AppFlow uses only Salesforce Bulk API 2.0. This API runs asynchronous data transfers, and it's optimal for large sets of data. By choosing this option, you ensure that your flow writes consistent output, but you optimize performance only for large data transfers.

            Note that Bulk API 2.0 does not transfer Salesforce compound fields.

            - **REST_SYNC** - Amazon AppFlow uses only Salesforce REST API. By choosing this option, you ensure that your flow writes consistent output, but you decrease performance for large data transfers that are better suited for Bulk API 2.0. In some cases, if your flow attempts to transfer a vary large set of data, it might fail wituh a timed out error.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-datatransferapi
            '''
            result = self._values.get("data_transfer_api")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_dynamic_field_update(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''The flag that enables dynamic fetching of new (recently added) fields in the Salesforce objects while running a flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-enabledynamicfieldupdate
            '''
            result = self._values.get("enable_dynamic_field_update")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def include_deleted_records(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether Amazon AppFlow includes deleted files in the flow run.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-includedeletedrecords
            '''
            result = self._values.get("include_deleted_records")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ScheduledTriggerPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "schedule_expression": "scheduleExpression",
            "data_pull_mode": "dataPullMode",
            "first_execution_from": "firstExecutionFrom",
            "flow_error_deactivation_threshold": "flowErrorDeactivationThreshold",
            "schedule_end_time": "scheduleEndTime",
            "schedule_offset": "scheduleOffset",
            "schedule_start_time": "scheduleStartTime",
            "time_zone": "timeZone",
        },
    )
    class ScheduledTriggerPropertiesProperty:
        def __init__(
            self,
            *,
            schedule_expression: builtins.str,
            data_pull_mode: typing.Optional[builtins.str] = None,
            first_execution_from: typing.Optional[jsii.Number] = None,
            flow_error_deactivation_threshold: typing.Optional[jsii.Number] = None,
            schedule_end_time: typing.Optional[jsii.Number] = None,
            schedule_offset: typing.Optional[jsii.Number] = None,
            schedule_start_time: typing.Optional[jsii.Number] = None,
            time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration details of a schedule-triggered flow as defined by the user.

            Currently, these settings only apply to the ``Scheduled`` trigger type.

            :param schedule_expression: The scheduling expression that determines the rate at which the schedule will run, for example ``rate(5minutes)`` .
            :param data_pull_mode: Specifies whether a scheduled flow has an incremental data transfer or a complete data transfer for each flow run.
            :param first_execution_from: Specifies the date range for the records to import from the connector in the first flow run.
            :param flow_error_deactivation_threshold: ``CfnFlow.ScheduledTriggerPropertiesProperty.FlowErrorDeactivationThreshold``.
            :param schedule_end_time: The time at which the scheduled flow ends. The time is formatted as a timestamp that follows the ISO 8601 standard, such as ``2022-04-27T13:00:00-07:00`` .
            :param schedule_offset: Specifies the optional offset that is added to the time interval for a schedule-triggered flow.
            :param schedule_start_time: The time at which the scheduled flow starts. The time is formatted as a timestamp that follows the ISO 8601 standard, such as ``2022-04-26T13:00:00-07:00`` .
            :param time_zone: Specifies the time zone used when referring to the dates and times of a scheduled flow, such as ``America/New_York`` . This time zone is only a descriptive label. It doesn't affect how Amazon AppFlow interprets the timestamps that you specify to schedule the flow. If you want to schedule a flow by using times in a particular time zone, indicate the time zone as a UTC offset in your timestamps. For example, the UTC offsets for the ``America/New_York`` timezone are ``-04:00`` EDT and ``-05:00 EST`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                scheduled_trigger_properties_property = appflow.CfnFlow.ScheduledTriggerPropertiesProperty(
                    schedule_expression="scheduleExpression",
                
                    # the properties below are optional
                    data_pull_mode="dataPullMode",
                    first_execution_from=123,
                    flow_error_deactivation_threshold=123,
                    schedule_end_time=123,
                    schedule_offset=123,
                    schedule_start_time=123,
                    time_zone="timeZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d9ada7e145ed6ee0ce866bdeb981968ca75dcc922c908e14dc16b37b40f0c7e)
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
                check_type(argname="argument data_pull_mode", value=data_pull_mode, expected_type=type_hints["data_pull_mode"])
                check_type(argname="argument first_execution_from", value=first_execution_from, expected_type=type_hints["first_execution_from"])
                check_type(argname="argument flow_error_deactivation_threshold", value=flow_error_deactivation_threshold, expected_type=type_hints["flow_error_deactivation_threshold"])
                check_type(argname="argument schedule_end_time", value=schedule_end_time, expected_type=type_hints["schedule_end_time"])
                check_type(argname="argument schedule_offset", value=schedule_offset, expected_type=type_hints["schedule_offset"])
                check_type(argname="argument schedule_start_time", value=schedule_start_time, expected_type=type_hints["schedule_start_time"])
                check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "schedule_expression": schedule_expression,
            }
            if data_pull_mode is not None:
                self._values["data_pull_mode"] = data_pull_mode
            if first_execution_from is not None:
                self._values["first_execution_from"] = first_execution_from
            if flow_error_deactivation_threshold is not None:
                self._values["flow_error_deactivation_threshold"] = flow_error_deactivation_threshold
            if schedule_end_time is not None:
                self._values["schedule_end_time"] = schedule_end_time
            if schedule_offset is not None:
                self._values["schedule_offset"] = schedule_offset
            if schedule_start_time is not None:
                self._values["schedule_start_time"] = schedule_start_time
            if time_zone is not None:
                self._values["time_zone"] = time_zone

        @builtins.property
        def schedule_expression(self) -> builtins.str:
            '''The scheduling expression that determines the rate at which the schedule will run, for example ``rate(5minutes)`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            assert result is not None, "Required property 'schedule_expression' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def data_pull_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether a scheduled flow has an incremental data transfer or a complete data transfer for each flow run.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-datapullmode
            '''
            result = self._values.get("data_pull_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def first_execution_from(self) -> typing.Optional[jsii.Number]:
            '''Specifies the date range for the records to import from the connector in the first flow run.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-firstexecutionfrom
            '''
            result = self._values.get("first_execution_from")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def flow_error_deactivation_threshold(self) -> typing.Optional[jsii.Number]:
            '''``CfnFlow.ScheduledTriggerPropertiesProperty.FlowErrorDeactivationThreshold``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-flowerrordeactivationthreshold
            '''
            result = self._values.get("flow_error_deactivation_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedule_end_time(self) -> typing.Optional[jsii.Number]:
            '''The time at which the scheduled flow ends.

            The time is formatted as a timestamp that follows the ISO 8601 standard, such as ``2022-04-27T13:00:00-07:00`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-scheduleendtime
            '''
            result = self._values.get("schedule_end_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedule_offset(self) -> typing.Optional[jsii.Number]:
            '''Specifies the optional offset that is added to the time interval for a schedule-triggered flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-scheduleoffset
            '''
            result = self._values.get("schedule_offset")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedule_start_time(self) -> typing.Optional[jsii.Number]:
            '''The time at which the scheduled flow starts.

            The time is formatted as a timestamp that follows the ISO 8601 standard, such as ``2022-04-26T13:00:00-07:00`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-schedulestarttime
            '''
            result = self._values.get("schedule_start_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def time_zone(self) -> typing.Optional[builtins.str]:
            '''Specifies the time zone used when referring to the dates and times of a scheduled flow, such as ``America/New_York`` .

            This time zone is only a descriptive label. It doesn't affect how Amazon AppFlow interprets the timestamps that you specify to schedule the flow.

            If you want to schedule a flow by using times in a particular time zone, indicate the time zone as a UTC offset in your timestamps. For example, the UTC offsets for the ``America/New_York`` timezone are ``-04:00`` EDT and ``-05:00 EST`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-timezone
            '''
            result = self._values.get("time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduledTriggerPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ServiceNowSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class ServiceNowSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when ServiceNow is being used as a source.

            :param object: The object specified in the ServiceNow flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-servicenowsourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                service_now_source_properties_property = appflow.CfnFlow.ServiceNowSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a061e2c155d302b314cbae30a2ad44c905f42c3a5a528542788d8447396c2447)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the ServiceNow flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-servicenowsourceproperties.html#cfn-appflow-flow-servicenowsourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SingularSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class SingularSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when Singular is being used as a source.

            :param object: The object specified in the Singular flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-singularsourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                singular_source_properties_property = appflow.CfnFlow.SingularSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__866767ce0b7bc8b3c571e82b88bd14212763f5d5b8f9bd8c73c24d107eba3989)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Singular flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-singularsourceproperties.html#cfn-appflow-flow-singularsourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingularSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SlackSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class SlackSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when Slack is being used as a source.

            :param object: The object specified in the Slack flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-slacksourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                slack_source_properties_property = appflow.CfnFlow.SlackSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16517a0e6a52c6cb221fb336b0ef598de20d5c52a9061ae97f7e913c467cc7d9)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Slack flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-slacksourceproperties.html#cfn-appflow-flow-slacksourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SnowflakeDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "intermediate_bucket_name": "intermediateBucketName",
            "object": "object",
            "bucket_prefix": "bucketPrefix",
            "error_handling_config": "errorHandlingConfig",
        },
    )
    class SnowflakeDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            intermediate_bucket_name: builtins.str,
            object: builtins.str,
            bucket_prefix: typing.Optional[builtins.str] = None,
            error_handling_config: typing.Optional[typing.Union[typing.Union["CfnFlow.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The properties that are applied when Snowflake is being used as a destination.

            :param intermediate_bucket_name: The intermediate bucket that Amazon AppFlow uses when moving data into Snowflake.
            :param object: The object specified in the Snowflake flow destination.
            :param bucket_prefix: The object key for the destination bucket in which Amazon AppFlow places the files.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the Snowflake destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                snowflake_destination_properties_property = appflow.CfnFlow.SnowflakeDestinationPropertiesProperty(
                    intermediate_bucket_name="intermediateBucketName",
                    object="object",
                
                    # the properties below are optional
                    bucket_prefix="bucketPrefix",
                    error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04c850effc6f3445201cd85e3e0f6ef097d018aa7ae4fa78d3987ea543fdbbd1)
                check_type(argname="argument intermediate_bucket_name", value=intermediate_bucket_name, expected_type=type_hints["intermediate_bucket_name"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "intermediate_bucket_name": intermediate_bucket_name,
                "object": object,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config

        @builtins.property
        def intermediate_bucket_name(self) -> builtins.str:
            '''The intermediate bucket that Amazon AppFlow uses when moving data into Snowflake.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-intermediatebucketname
            '''
            result = self._values.get("intermediate_bucket_name")
            assert result is not None, "Required property 'intermediate_bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Snowflake flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the destination bucket in which Amazon AppFlow places the files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the Snowflake destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SourceConnectorPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amplitude": "amplitude",
            "custom_connector": "customConnector",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "google_analytics": "googleAnalytics",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "s3": "s3",
            "salesforce": "salesforce",
            "sapo_data": "sapoData",
            "service_now": "serviceNow",
            "singular": "singular",
            "slack": "slack",
            "trendmicro": "trendmicro",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class SourceConnectorPropertiesProperty:
        def __init__(
            self,
            *,
            amplitude: typing.Optional[typing.Union[typing.Union["CfnFlow.AmplitudeSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            custom_connector: typing.Optional[typing.Union[typing.Union["CfnFlow.CustomConnectorSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            datadog: typing.Optional[typing.Union[typing.Union["CfnFlow.DatadogSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            dynatrace: typing.Optional[typing.Union[typing.Union["CfnFlow.DynatraceSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            google_analytics: typing.Optional[typing.Union[typing.Union["CfnFlow.GoogleAnalyticsSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            infor_nexus: typing.Optional[typing.Union[typing.Union["CfnFlow.InforNexusSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            marketo: typing.Optional[typing.Union[typing.Union["CfnFlow.MarketoSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            s3: typing.Optional[typing.Union[typing.Union["CfnFlow.S3SourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            salesforce: typing.Optional[typing.Union[typing.Union["CfnFlow.SalesforceSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sapo_data: typing.Optional[typing.Union[typing.Union["CfnFlow.SAPODataSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            service_now: typing.Optional[typing.Union[typing.Union["CfnFlow.ServiceNowSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            singular: typing.Optional[typing.Union[typing.Union["CfnFlow.SingularSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            slack: typing.Optional[typing.Union[typing.Union["CfnFlow.SlackSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            trendmicro: typing.Optional[typing.Union[typing.Union["CfnFlow.TrendmicroSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            veeva: typing.Optional[typing.Union[typing.Union["CfnFlow.VeevaSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            zendesk: typing.Optional[typing.Union[typing.Union["CfnFlow.ZendeskSourcePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Specifies the information that is required to query a particular connector.

            :param amplitude: Specifies the information that is required for querying Amplitude.
            :param custom_connector: The properties that are applied when the custom connector is being used as a source.
            :param datadog: Specifies the information that is required for querying Datadog.
            :param dynatrace: Specifies the information that is required for querying Dynatrace.
            :param google_analytics: Specifies the information that is required for querying Google Analytics.
            :param infor_nexus: Specifies the information that is required for querying Infor Nexus.
            :param marketo: Specifies the information that is required for querying Marketo.
            :param s3: Specifies the information that is required for querying Amazon S3.
            :param salesforce: Specifies the information that is required for querying Salesforce.
            :param sapo_data: The properties that are applied when using SAPOData as a flow source.
            :param service_now: Specifies the information that is required for querying ServiceNow.
            :param singular: Specifies the information that is required for querying Singular.
            :param slack: Specifies the information that is required for querying Slack.
            :param trendmicro: Specifies the information that is required for querying Trend Micro.
            :param veeva: Specifies the information that is required for querying Veeva.
            :param zendesk: Specifies the information that is required for querying Zendesk.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                source_connector_properties_property = appflow.CfnFlow.SourceConnectorPropertiesProperty(
                    amplitude=appflow.CfnFlow.AmplitudeSourcePropertiesProperty(
                        object="object"
                    ),
                    custom_connector=appflow.CfnFlow.CustomConnectorSourcePropertiesProperty(
                        entity_name="entityName",
                
                        # the properties below are optional
                        custom_properties={
                            "custom_properties_key": "customProperties"
                        }
                    ),
                    datadog=appflow.CfnFlow.DatadogSourcePropertiesProperty(
                        object="object"
                    ),
                    dynatrace=appflow.CfnFlow.DynatraceSourcePropertiesProperty(
                        object="object"
                    ),
                    google_analytics=appflow.CfnFlow.GoogleAnalyticsSourcePropertiesProperty(
                        object="object"
                    ),
                    infor_nexus=appflow.CfnFlow.InforNexusSourcePropertiesProperty(
                        object="object"
                    ),
                    marketo=appflow.CfnFlow.MarketoSourcePropertiesProperty(
                        object="object"
                    ),
                    s3=appflow.CfnFlow.S3SourcePropertiesProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                
                        # the properties below are optional
                        s3_input_format_config=appflow.CfnFlow.S3InputFormatConfigProperty(
                            s3_input_file_type="s3InputFileType"
                        )
                    ),
                    salesforce=appflow.CfnFlow.SalesforceSourcePropertiesProperty(
                        object="object",
                
                        # the properties below are optional
                        data_transfer_api="dataTransferApi",
                        enable_dynamic_field_update=False,
                        include_deleted_records=False
                    ),
                    sapo_data=appflow.CfnFlow.SAPODataSourcePropertiesProperty(
                        object_path="objectPath"
                    ),
                    service_now=appflow.CfnFlow.ServiceNowSourcePropertiesProperty(
                        object="object"
                    ),
                    singular=appflow.CfnFlow.SingularSourcePropertiesProperty(
                        object="object"
                    ),
                    slack=appflow.CfnFlow.SlackSourcePropertiesProperty(
                        object="object"
                    ),
                    trendmicro=appflow.CfnFlow.TrendmicroSourcePropertiesProperty(
                        object="object"
                    ),
                    veeva=appflow.CfnFlow.VeevaSourcePropertiesProperty(
                        object="object",
                
                        # the properties below are optional
                        document_type="documentType",
                        include_all_versions=False,
                        include_renditions=False,
                        include_source_files=False
                    ),
                    zendesk=appflow.CfnFlow.ZendeskSourcePropertiesProperty(
                        object="object"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3378cd727c580ef9d24acb7bfa9d5ba2e4aab3872dd5185ef986071f594a1140)
                check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
                check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
                check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
                check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
                check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
                check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
                check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
                check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
                check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
                check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
                check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
                check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
                check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
                check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
                check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amplitude is not None:
                self._values["amplitude"] = amplitude
            if custom_connector is not None:
                self._values["custom_connector"] = custom_connector
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if google_analytics is not None:
                self._values["google_analytics"] = google_analytics
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if sapo_data is not None:
                self._values["sapo_data"] = sapo_data
            if service_now is not None:
                self._values["service_now"] = service_now
            if singular is not None:
                self._values["singular"] = singular
            if slack is not None:
                self._values["slack"] = slack
            if trendmicro is not None:
                self._values["trendmicro"] = trendmicro
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def amplitude(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.AmplitudeSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Amplitude.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-amplitude
            '''
            result = self._values.get("amplitude")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.AmplitudeSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def custom_connector(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.CustomConnectorSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties that are applied when the custom connector is being used as a source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-customconnector
            '''
            result = self._values.get("custom_connector")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.CustomConnectorSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def datadog(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.DatadogSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Datadog.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.DatadogSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.DynatraceSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Dynatrace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.DynatraceSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def google_analytics(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.GoogleAnalyticsSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Google Analytics.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-googleanalytics
            '''
            result = self._values.get("google_analytics")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.GoogleAnalyticsSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def infor_nexus(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.InforNexusSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Infor Nexus.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.InforNexusSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.MarketoSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Marketo.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.MarketoSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.S3SourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Amazon S3.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.S3SourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SalesforceSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Salesforce.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SalesforceSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sapo_data(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SAPODataSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''The properties that are applied when using SAPOData as a flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-sapodata
            '''
            result = self._values.get("sapo_data")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SAPODataSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ServiceNowSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying ServiceNow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ServiceNowSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def singular(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SingularSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Singular.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-singular
            '''
            result = self._values.get("singular")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SingularSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SlackSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Slack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SlackSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def trendmicro(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.TrendmicroSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Trend Micro.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-trendmicro
            '''
            result = self._values.get("trendmicro")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.TrendmicroSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def veeva(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.VeevaSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Veeva.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.VeevaSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ZendeskSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the information that is required for querying Zendesk.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ZendeskSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConnectorPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SourceFlowConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_type": "connectorType",
            "source_connector_properties": "sourceConnectorProperties",
            "api_version": "apiVersion",
            "connector_profile_name": "connectorProfileName",
            "incremental_pull_config": "incrementalPullConfig",
        },
    )
    class SourceFlowConfigProperty:
        def __init__(
            self,
            *,
            connector_type: builtins.str,
            source_connector_properties: typing.Union[typing.Union["CfnFlow.SourceConnectorPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            api_version: typing.Optional[builtins.str] = None,
            connector_profile_name: typing.Optional[builtins.str] = None,
            incremental_pull_config: typing.Optional[typing.Union[typing.Union["CfnFlow.IncrementalPullConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains information about the configuration of the source connector used in the flow.

            :param connector_type: The type of source connector, such as Salesforce, Amplitude, and so on. *Allowed Values* : S3 | Amplitude | Datadog | Dynatrace | Googleanalytics | Infornexus | Salesforce | Servicenow | Singular | Slack | Trendmicro | Veeva | Zendesk
            :param source_connector_properties: Specifies the information that is required to query a particular source connector.
            :param api_version: The API version of the connector when it's used as a source in the flow.
            :param connector_profile_name: The name of the connector profile. This name must be unique for each connector profile in the AWS account .
            :param incremental_pull_config: Defines the configuration for a scheduled incremental data pull. If a valid configuration is provided, the fields specified in the configuration are used when querying for the incremental data pull.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                source_flow_config_property = appflow.CfnFlow.SourceFlowConfigProperty(
                    connector_type="connectorType",
                    source_connector_properties=appflow.CfnFlow.SourceConnectorPropertiesProperty(
                        amplitude=appflow.CfnFlow.AmplitudeSourcePropertiesProperty(
                            object="object"
                        ),
                        custom_connector=appflow.CfnFlow.CustomConnectorSourcePropertiesProperty(
                            entity_name="entityName",
                
                            # the properties below are optional
                            custom_properties={
                                "custom_properties_key": "customProperties"
                            }
                        ),
                        datadog=appflow.CfnFlow.DatadogSourcePropertiesProperty(
                            object="object"
                        ),
                        dynatrace=appflow.CfnFlow.DynatraceSourcePropertiesProperty(
                            object="object"
                        ),
                        google_analytics=appflow.CfnFlow.GoogleAnalyticsSourcePropertiesProperty(
                            object="object"
                        ),
                        infor_nexus=appflow.CfnFlow.InforNexusSourcePropertiesProperty(
                            object="object"
                        ),
                        marketo=appflow.CfnFlow.MarketoSourcePropertiesProperty(
                            object="object"
                        ),
                        s3=appflow.CfnFlow.S3SourcePropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
                
                            # the properties below are optional
                            s3_input_format_config=appflow.CfnFlow.S3InputFormatConfigProperty(
                                s3_input_file_type="s3InputFileType"
                            )
                        ),
                        salesforce=appflow.CfnFlow.SalesforceSourcePropertiesProperty(
                            object="object",
                
                            # the properties below are optional
                            data_transfer_api="dataTransferApi",
                            enable_dynamic_field_update=False,
                            include_deleted_records=False
                        ),
                        sapo_data=appflow.CfnFlow.SAPODataSourcePropertiesProperty(
                            object_path="objectPath"
                        ),
                        service_now=appflow.CfnFlow.ServiceNowSourcePropertiesProperty(
                            object="object"
                        ),
                        singular=appflow.CfnFlow.SingularSourcePropertiesProperty(
                            object="object"
                        ),
                        slack=appflow.CfnFlow.SlackSourcePropertiesProperty(
                            object="object"
                        ),
                        trendmicro=appflow.CfnFlow.TrendmicroSourcePropertiesProperty(
                            object="object"
                        ),
                        veeva=appflow.CfnFlow.VeevaSourcePropertiesProperty(
                            object="object",
                
                            # the properties below are optional
                            document_type="documentType",
                            include_all_versions=False,
                            include_renditions=False,
                            include_source_files=False
                        ),
                        zendesk=appflow.CfnFlow.ZendeskSourcePropertiesProperty(
                            object="object"
                        )
                    ),
                
                    # the properties below are optional
                    api_version="apiVersion",
                    connector_profile_name="connectorProfileName",
                    incremental_pull_config=appflow.CfnFlow.IncrementalPullConfigProperty(
                        datetime_type_field_name="datetimeTypeFieldName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a4f9234c873099d73c2b858e2c6c924cc145c47dfbf38427f49442b8deb6fa5)
                check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
                check_type(argname="argument source_connector_properties", value=source_connector_properties, expected_type=type_hints["source_connector_properties"])
                check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
                check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
                check_type(argname="argument incremental_pull_config", value=incremental_pull_config, expected_type=type_hints["incremental_pull_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "connector_type": connector_type,
                "source_connector_properties": source_connector_properties,
            }
            if api_version is not None:
                self._values["api_version"] = api_version
            if connector_profile_name is not None:
                self._values["connector_profile_name"] = connector_profile_name
            if incremental_pull_config is not None:
                self._values["incremental_pull_config"] = incremental_pull_config

        @builtins.property
        def connector_type(self) -> builtins.str:
            '''The type of source connector, such as Salesforce, Amplitude, and so on.

            *Allowed Values* : S3 | Amplitude | Datadog | Dynatrace | Googleanalytics | Infornexus | Salesforce | Servicenow | Singular | Slack | Trendmicro | Veeva | Zendesk

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-connectortype
            '''
            result = self._values.get("connector_type")
            assert result is not None, "Required property 'connector_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source_connector_properties(
            self,
        ) -> typing.Union["CfnFlow.SourceConnectorPropertiesProperty", _IResolvable_a771d0ef]:
            '''Specifies the information that is required to query a particular source connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-sourceconnectorproperties
            '''
            result = self._values.get("source_connector_properties")
            assert result is not None, "Required property 'source_connector_properties' is missing"
            return typing.cast(typing.Union["CfnFlow.SourceConnectorPropertiesProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def api_version(self) -> typing.Optional[builtins.str]:
            '''The API version of the connector when it's used as a source in the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-apiversion
            '''
            result = self._values.get("api_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_profile_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connector profile.

            This name must be unique for each connector profile in the AWS account .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-connectorprofilename
            '''
            result = self._values.get("connector_profile_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def incremental_pull_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.IncrementalPullConfigProperty", _IResolvable_a771d0ef]]:
            '''Defines the configuration for a scheduled incremental data pull.

            If a valid configuration is provided, the fields specified in the configuration are used when querying for the incremental data pull.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-incrementalpullconfig
            '''
            result = self._values.get("incremental_pull_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.IncrementalPullConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceFlowConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SuccessResponseHandlingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "bucket_prefix": "bucketPrefix"},
    )
    class SuccessResponseHandlingConfigProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Determines how Amazon AppFlow handles the success response that it gets from the connector after placing data.

            For example, this setting would determine where to write the response from the destination connector upon a successful insert operation.

            :param bucket_name: The name of the Amazon S3 bucket.
            :param bucket_prefix: The Amazon S3 bucket prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-successresponsehandlingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                success_response_handling_config_property = appflow.CfnFlow.SuccessResponseHandlingConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f157805877d013d4f9a57c63e74ae0e585184e780befcb208dda0206902fa01)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-successresponsehandlingconfig.html#cfn-appflow-flow-successresponsehandlingconfig-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-successresponsehandlingconfig.html#cfn-appflow-flow-successresponsehandlingconfig-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SuccessResponseHandlingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.TaskPropertiesObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TaskPropertiesObjectProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''A map used to store task-related information.

            The execution service looks for particular information based on the ``TaskType`` .

            :param key: The task property key. *Allowed Values* : ``VALUE | VALUES | DATA_TYPE | UPPER_BOUND | LOWER_BOUND | SOURCE_DATA_TYPE | DESTINATION_DATA_TYPE | VALIDATION_ACTION | MASK_VALUE | MASK_LENGTH | TRUNCATE_LENGTH | MATH_OPERATION_FIELDS_ORDER | CONCAT_FORMAT | SUBFIELD_CATEGORY_MAP`` | ``EXCLUDE_SOURCE_FIELDS_LIST``
            :param value: The task property value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-taskpropertiesobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                task_properties_object_property = appflow.CfnFlow.TaskPropertiesObjectProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ab41b4b9ff7e622a3ecb5af9692c152aa0206c867c4f69cc71f8632314fcae9)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The task property key.

            *Allowed Values* : ``VALUE | VALUES | DATA_TYPE | UPPER_BOUND | LOWER_BOUND | SOURCE_DATA_TYPE | DESTINATION_DATA_TYPE | VALIDATION_ACTION | MASK_VALUE | MASK_LENGTH | TRUNCATE_LENGTH | MATH_OPERATION_FIELDS_ORDER | CONCAT_FORMAT | SUBFIELD_CATEGORY_MAP`` | ``EXCLUDE_SOURCE_FIELDS_LIST``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-taskpropertiesobject.html#cfn-appflow-flow-taskpropertiesobject-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The task property value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-taskpropertiesobject.html#cfn-appflow-flow-taskpropertiesobject-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskPropertiesObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.TaskProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_fields": "sourceFields",
            "task_type": "taskType",
            "connector_operator": "connectorOperator",
            "destination_field": "destinationField",
            "task_properties": "taskProperties",
        },
    )
    class TaskProperty:
        def __init__(
            self,
            *,
            source_fields: typing.Sequence[builtins.str],
            task_type: builtins.str,
            connector_operator: typing.Optional[typing.Union[typing.Union["CfnFlow.ConnectorOperatorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            destination_field: typing.Optional[builtins.str] = None,
            task_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFlow.TaskPropertiesObjectProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''A class for modeling different type of tasks.

            Task implementation varies based on the ``TaskType`` .

            :param source_fields: The source fields to which a particular task is applied.
            :param task_type: Specifies the particular task implementation that Amazon AppFlow performs. *Allowed values* : ``Arithmetic`` | ``Filter`` | ``Map`` | ``Map_all`` | ``Mask`` | ``Merge`` | ``Truncate`` | ``Validate``
            :param connector_operator: The operation to be performed on the provided source fields.
            :param destination_field: A field in a destination connector, or a field value against which Amazon AppFlow validates a source field.
            :param task_properties: A map used to store task-related information. The execution service looks for particular information based on the ``TaskType`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                task_property = appflow.CfnFlow.TaskProperty(
                    source_fields=["sourceFields"],
                    task_type="taskType",
                
                    # the properties below are optional
                    connector_operator=appflow.CfnFlow.ConnectorOperatorProperty(
                        amplitude="amplitude",
                        custom_connector="customConnector",
                        datadog="datadog",
                        dynatrace="dynatrace",
                        google_analytics="googleAnalytics",
                        infor_nexus="inforNexus",
                        marketo="marketo",
                        s3="s3",
                        salesforce="salesforce",
                        sapo_data="sapoData",
                        service_now="serviceNow",
                        singular="singular",
                        slack="slack",
                        trendmicro="trendmicro",
                        veeva="veeva",
                        zendesk="zendesk"
                    ),
                    destination_field="destinationField",
                    task_properties=[appflow.CfnFlow.TaskPropertiesObjectProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07eaf0dbbae9ff1c353003786e1be5a4e0968dae55caa457da2430212a949236)
                check_type(argname="argument source_fields", value=source_fields, expected_type=type_hints["source_fields"])
                check_type(argname="argument task_type", value=task_type, expected_type=type_hints["task_type"])
                check_type(argname="argument connector_operator", value=connector_operator, expected_type=type_hints["connector_operator"])
                check_type(argname="argument destination_field", value=destination_field, expected_type=type_hints["destination_field"])
                check_type(argname="argument task_properties", value=task_properties, expected_type=type_hints["task_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "source_fields": source_fields,
                "task_type": task_type,
            }
            if connector_operator is not None:
                self._values["connector_operator"] = connector_operator
            if destination_field is not None:
                self._values["destination_field"] = destination_field
            if task_properties is not None:
                self._values["task_properties"] = task_properties

        @builtins.property
        def source_fields(self) -> typing.List[builtins.str]:
            '''The source fields to which a particular task is applied.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-sourcefields
            '''
            result = self._values.get("source_fields")
            assert result is not None, "Required property 'source_fields' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def task_type(self) -> builtins.str:
            '''Specifies the particular task implementation that Amazon AppFlow performs.

            *Allowed values* : ``Arithmetic`` | ``Filter`` | ``Map`` | ``Map_all`` | ``Mask`` | ``Merge`` | ``Truncate`` | ``Validate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-tasktype
            '''
            result = self._values.get("task_type")
            assert result is not None, "Required property 'task_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def connector_operator(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ConnectorOperatorProperty", _IResolvable_a771d0ef]]:
            '''The operation to be performed on the provided source fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-connectoroperator
            '''
            result = self._values.get("connector_operator")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ConnectorOperatorProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def destination_field(self) -> typing.Optional[builtins.str]:
            '''A field in a destination connector, or a field value against which Amazon AppFlow validates a source field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-destinationfield
            '''
            result = self._values.get("destination_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def task_properties(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskPropertiesObjectProperty", _IResolvable_a771d0ef]]]]:
            '''A map used to store task-related information.

            The execution service looks for particular information based on the ``TaskType`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-taskproperties
            '''
            result = self._values.get("task_properties")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskPropertiesObjectProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.TrendmicroSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class TrendmicroSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when using Trend Micro as a flow source.

            :param object: The object specified in the Trend Micro flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-trendmicrosourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                trendmicro_source_properties_property = appflow.CfnFlow.TrendmicroSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06ba28f6151f0b9cdcb2afdde4332e0fbcfe04eadfc59a9e424ea1789cd9686d)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Trend Micro flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-trendmicrosourceproperties.html#cfn-appflow-flow-trendmicrosourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrendmicroSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.TriggerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trigger_type": "triggerType",
            "trigger_properties": "triggerProperties",
        },
    )
    class TriggerConfigProperty:
        def __init__(
            self,
            *,
            trigger_type: builtins.str,
            trigger_properties: typing.Optional[typing.Union[typing.Union["CfnFlow.ScheduledTriggerPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The trigger settings that determine how and when Amazon AppFlow runs the specified flow.

            :param trigger_type: Specifies the type of flow trigger. This can be ``OnDemand`` , ``Scheduled`` , or ``Event`` .
            :param trigger_properties: Specifies the configuration details of a schedule-triggered flow as defined by the user. Currently, these settings only apply to the ``Scheduled`` trigger type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-triggerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                trigger_config_property = appflow.CfnFlow.TriggerConfigProperty(
                    trigger_type="triggerType",
                
                    # the properties below are optional
                    trigger_properties=appflow.CfnFlow.ScheduledTriggerPropertiesProperty(
                        schedule_expression="scheduleExpression",
                
                        # the properties below are optional
                        data_pull_mode="dataPullMode",
                        first_execution_from=123,
                        flow_error_deactivation_threshold=123,
                        schedule_end_time=123,
                        schedule_offset=123,
                        schedule_start_time=123,
                        time_zone="timeZone"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e73213e14a9b6c30e52c321e4e38f3c636cd411e91e09864eb93aeb44d0dce3b)
                check_type(argname="argument trigger_type", value=trigger_type, expected_type=type_hints["trigger_type"])
                check_type(argname="argument trigger_properties", value=trigger_properties, expected_type=type_hints["trigger_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "trigger_type": trigger_type,
            }
            if trigger_properties is not None:
                self._values["trigger_properties"] = trigger_properties

        @builtins.property
        def trigger_type(self) -> builtins.str:
            '''Specifies the type of flow trigger.

            This can be ``OnDemand`` , ``Scheduled`` , or ``Event`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-triggerconfig.html#cfn-appflow-flow-triggerconfig-triggertype
            '''
            result = self._values.get("trigger_type")
            assert result is not None, "Required property 'trigger_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def trigger_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ScheduledTriggerPropertiesProperty", _IResolvable_a771d0ef]]:
            '''Specifies the configuration details of a schedule-triggered flow as defined by the user.

            Currently, these settings only apply to the ``Scheduled`` trigger type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-triggerconfig.html#cfn-appflow-flow-triggerconfig-triggerproperties
            '''
            result = self._values.get("trigger_properties")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ScheduledTriggerPropertiesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.UpsolverDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "s3_output_format_config": "s3OutputFormatConfig",
            "bucket_prefix": "bucketPrefix",
        },
    )
    class UpsolverDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            s3_output_format_config: typing.Union[typing.Union["CfnFlow.UpsolverS3OutputFormatConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            bucket_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Upsolver is used as a destination.

            :param bucket_name: The Upsolver Amazon S3 bucket name in which Amazon AppFlow places the transferred data.
            :param s3_output_format_config: The configuration that determines how data is formatted when Upsolver is used as the flow destination.
            :param bucket_prefix: The object key for the destination Upsolver Amazon S3 bucket in which Amazon AppFlow places the files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                upsolver_destination_properties_property = appflow.CfnFlow.UpsolverDestinationPropertiesProperty(
                    bucket_name="bucketName",
                    s3_output_format_config=appflow.CfnFlow.UpsolverS3OutputFormatConfigProperty(
                        prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                            path_prefix_hierarchy=["pathPrefixHierarchy"],
                            prefix_format="prefixFormat",
                            prefix_type="prefixType"
                        ),
                
                        # the properties below are optional
                        aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                            aggregation_type="aggregationType",
                            target_file_size=123
                        ),
                        file_type="fileType"
                    ),
                
                    # the properties below are optional
                    bucket_prefix="bucketPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__220d9c452eca21c99b2192e5bfdb02e955894042ada097db7fd93bac0b6d26f6)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument s3_output_format_config", value=s3_output_format_config, expected_type=type_hints["s3_output_format_config"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
                "s3_output_format_config": s3_output_format_config,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The Upsolver Amazon S3 bucket name in which Amazon AppFlow places the transferred data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html#cfn-appflow-flow-upsolverdestinationproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_output_format_config(
            self,
        ) -> typing.Union["CfnFlow.UpsolverS3OutputFormatConfigProperty", _IResolvable_a771d0ef]:
            '''The configuration that determines how data is formatted when Upsolver is used as the flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html#cfn-appflow-flow-upsolverdestinationproperties-s3outputformatconfig
            '''
            result = self._values.get("s3_output_format_config")
            assert result is not None, "Required property 's3_output_format_config' is missing"
            return typing.cast(typing.Union["CfnFlow.UpsolverS3OutputFormatConfigProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key for the destination Upsolver Amazon S3 bucket in which Amazon AppFlow places the files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html#cfn-appflow-flow-upsolverdestinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpsolverDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.UpsolverS3OutputFormatConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "prefix_config": "prefixConfig",
            "aggregation_config": "aggregationConfig",
            "file_type": "fileType",
        },
    )
    class UpsolverS3OutputFormatConfigProperty:
        def __init__(
            self,
            *,
            prefix_config: typing.Union[typing.Union["CfnFlow.PrefixConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            aggregation_config: typing.Optional[typing.Union[typing.Union["CfnFlow.AggregationConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            file_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that determines how Amazon AppFlow formats the flow output data when Upsolver is used as the destination.

            :param prefix_config: Specifies elements that Amazon AppFlow includes in the file and folder names in the flow destination.
            :param aggregation_config: The aggregation settings that you can use to customize the output format of your flow data.
            :param file_type: Indicates the file type that Amazon AppFlow places in the Upsolver Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                upsolver_s3_output_format_config_property = appflow.CfnFlow.UpsolverS3OutputFormatConfigProperty(
                    prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                        path_prefix_hierarchy=["pathPrefixHierarchy"],
                        prefix_format="prefixFormat",
                        prefix_type="prefixType"
                    ),
                
                    # the properties below are optional
                    aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                        aggregation_type="aggregationType",
                        target_file_size=123
                    ),
                    file_type="fileType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d96c2b5f28ca72db19de71c46435a5da2000c65f0ab8c40d4ab286d557edd8c9)
                check_type(argname="argument prefix_config", value=prefix_config, expected_type=type_hints["prefix_config"])
                check_type(argname="argument aggregation_config", value=aggregation_config, expected_type=type_hints["aggregation_config"])
                check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "prefix_config": prefix_config,
            }
            if aggregation_config is not None:
                self._values["aggregation_config"] = aggregation_config
            if file_type is not None:
                self._values["file_type"] = file_type

        @builtins.property
        def prefix_config(
            self,
        ) -> typing.Union["CfnFlow.PrefixConfigProperty", _IResolvable_a771d0ef]:
            '''Specifies elements that Amazon AppFlow includes in the file and folder names in the flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html#cfn-appflow-flow-upsolvers3outputformatconfig-prefixconfig
            '''
            result = self._values.get("prefix_config")
            assert result is not None, "Required property 'prefix_config' is missing"
            return typing.cast(typing.Union["CfnFlow.PrefixConfigProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def aggregation_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.AggregationConfigProperty", _IResolvable_a771d0ef]]:
            '''The aggregation settings that you can use to customize the output format of your flow data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html#cfn-appflow-flow-upsolvers3outputformatconfig-aggregationconfig
            '''
            result = self._values.get("aggregation_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.AggregationConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def file_type(self) -> typing.Optional[builtins.str]:
            '''Indicates the file type that Amazon AppFlow places in the Upsolver Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html#cfn-appflow-flow-upsolvers3outputformatconfig-filetype
            '''
            result = self._values.get("file_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpsolverS3OutputFormatConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.VeevaSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object": "object",
            "document_type": "documentType",
            "include_all_versions": "includeAllVersions",
            "include_renditions": "includeRenditions",
            "include_source_files": "includeSourceFiles",
        },
    )
    class VeevaSourcePropertiesProperty:
        def __init__(
            self,
            *,
            object: builtins.str,
            document_type: typing.Optional[builtins.str] = None,
            include_all_versions: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            include_renditions: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            include_source_files: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The properties that are applied when using Veeva as a flow source.

            :param object: The object specified in the Veeva flow source.
            :param document_type: The document type specified in the Veeva document extract flow.
            :param include_all_versions: Boolean value to include All Versions of files in Veeva document extract flow.
            :param include_renditions: Boolean value to include file renditions in Veeva document extract flow.
            :param include_source_files: Boolean value to include source files in Veeva document extract flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                veeva_source_properties_property = appflow.CfnFlow.VeevaSourcePropertiesProperty(
                    object="object",
                
                    # the properties below are optional
                    document_type="documentType",
                    include_all_versions=False,
                    include_renditions=False,
                    include_source_files=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9243e1f4370d9f2c91ee392c0cdff977925796dcf0d92a5fee0655dfd64a7fb2)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument document_type", value=document_type, expected_type=type_hints["document_type"])
                check_type(argname="argument include_all_versions", value=include_all_versions, expected_type=type_hints["include_all_versions"])
                check_type(argname="argument include_renditions", value=include_renditions, expected_type=type_hints["include_renditions"])
                check_type(argname="argument include_source_files", value=include_source_files, expected_type=type_hints["include_source_files"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }
            if document_type is not None:
                self._values["document_type"] = document_type
            if include_all_versions is not None:
                self._values["include_all_versions"] = include_all_versions
            if include_renditions is not None:
                self._values["include_renditions"] = include_renditions
            if include_source_files is not None:
                self._values["include_source_files"] = include_source_files

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Veeva flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def document_type(self) -> typing.Optional[builtins.str]:
            '''The document type specified in the Veeva document extract flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-documenttype
            '''
            result = self._values.get("document_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_all_versions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Boolean value to include All Versions of files in Veeva document extract flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-includeallversions
            '''
            result = self._values.get("include_all_versions")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def include_renditions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Boolean value to include file renditions in Veeva document extract flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-includerenditions
            '''
            result = self._values.get("include_renditions")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def include_source_files(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Boolean value to include source files in Veeva document extract flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-includesourcefiles
            '''
            result = self._values.get("include_source_files")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VeevaSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ZendeskDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object": "object",
            "error_handling_config": "errorHandlingConfig",
            "id_field_names": "idFieldNames",
            "write_operation_type": "writeOperationType",
        },
    )
    class ZendeskDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            object: builtins.str,
            error_handling_config: typing.Optional[typing.Union[typing.Union["CfnFlow.ErrorHandlingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            write_operation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The properties that are applied when Zendesk is used as a destination.

            :param object: The object specified in the Zendesk flow destination.
            :param error_handling_config: The settings that determine how Amazon AppFlow handles an error when placing data in the destination. For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.
            :param id_field_names: A list of field names that can be used as an ID field when performing a write operation.
            :param write_operation_type: The possible write operations in the destination connector. When this value is not provided, this defaults to the ``INSERT`` operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendeskdestinationproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                zendesk_destination_properties_property = appflow.CfnFlow.ZendeskDestinationPropertiesProperty(
                    object="object",
                
                    # the properties below are optional
                    error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                        bucket_name="bucketName",
                        bucket_prefix="bucketPrefix",
                        fail_on_first_error=False
                    ),
                    id_field_names=["idFieldNames"],
                    write_operation_type="writeOperationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70d98bc38b9a1a47e9780fc455cd0dc6b753d247c250d6c2c3fbbbea4e410234)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
                check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
                check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if id_field_names is not None:
                self._values["id_field_names"] = id_field_names
            if write_operation_type is not None:
                self._values["write_operation_type"] = write_operation_type

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Zendesk flow destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendeskdestinationproperties.html#cfn-appflow-flow-zendeskdestinationproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''The settings that determine how Amazon AppFlow handles an error when placing data in the destination.

            For example, this setting would determine if the flow should fail after one insertion error, or continue and attempt to insert every record regardless of the initial failure. ``ErrorHandlingConfig`` is a part of the destination connector details.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendeskdestinationproperties.html#cfn-appflow-flow-zendeskdestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of field names that can be used as an ID field when performing a write operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendeskdestinationproperties.html#cfn-appflow-flow-zendeskdestinationproperties-idfieldnames
            '''
            result = self._values.get("id_field_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def write_operation_type(self) -> typing.Optional[builtins.str]:
            '''The possible write operations in the destination connector.

            When this value is not provided, this defaults to the ``INSERT`` operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendeskdestinationproperties.html#cfn-appflow-flow-zendeskdestinationproperties-writeoperationtype
            '''
            result = self._values.get("write_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ZendeskSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class ZendeskSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''The properties that are applied when using Zendesk as a flow source.

            :param object: The object specified in the Zendesk flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendesksourceproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appflow as appflow
                
                zendesk_source_properties_property = appflow.CfnFlow.ZendeskSourcePropertiesProperty(
                    object="object"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f16f6d9214ed83e91799141c7a085c85eb72506b3663bf64a450ec9271b83bb)
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''The object specified in the Zendesk flow source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendesksourceproperties.html#cfn-appflow-flow-zendesksourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appflow.CfnFlowProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_flow_config_list": "destinationFlowConfigList",
        "flow_name": "flowName",
        "source_flow_config": "sourceFlowConfig",
        "tasks": "tasks",
        "trigger_config": "triggerConfig",
        "description": "description",
        "kms_arn": "kmsArn",
        "metadata_catalog_config": "metadataCatalogConfig",
        "tags": "tags",
    },
)
class CfnFlowProps:
    def __init__(
        self,
        *,
        destination_flow_config_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFlow.DestinationFlowConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        flow_name: builtins.str,
        source_flow_config: typing.Union[typing.Union[CfnFlow.SourceFlowConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        tasks: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFlow.TaskProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        trigger_config: typing.Union[typing.Union[CfnFlow.TriggerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        metadata_catalog_config: typing.Optional[typing.Union[typing.Union[CfnFlow.MetadataCatalogConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFlow``.

        :param destination_flow_config_list: The configuration that controls how Amazon AppFlow places data in the destination connector.
        :param flow_name: The specified name of the flow. Spaces are not allowed. Use underscores (_) or hyphens (-) only.
        :param source_flow_config: Contains information about the configuration of the source connector used in the flow.
        :param tasks: A list of tasks that Amazon AppFlow performs while transferring the data in the flow run.
        :param trigger_config: The trigger settings that determine how and when Amazon AppFlow runs the specified flow.
        :param description: A user-entered description of the flow.
        :param kms_arn: The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption. This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.
        :param metadata_catalog_config: ``AWS::AppFlow::Flow.MetadataCatalogConfig``.
        :param tags: The tags used to organize, track, or control access for your flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appflow as appflow
            
            cfn_flow_props = appflow.CfnFlowProps(
                destination_flow_config_list=[appflow.CfnFlow.DestinationFlowConfigProperty(
                    connector_type="connectorType",
                    destination_connector_properties=appflow.CfnFlow.DestinationConnectorPropertiesProperty(
                        custom_connector=appflow.CfnFlow.CustomConnectorDestinationPropertiesProperty(
                            entity_name="entityName",
            
                            # the properties below are optional
                            custom_properties={
                                "custom_properties_key": "customProperties"
                            },
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            write_operation_type="writeOperationType"
                        ),
                        event_bridge=appflow.CfnFlow.EventBridgeDestinationPropertiesProperty(
                            object="object",
            
                            # the properties below are optional
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            )
                        ),
                        lookout_metrics=appflow.CfnFlow.LookoutMetricsDestinationPropertiesProperty(
                            object="object"
                        ),
                        marketo=appflow.CfnFlow.MarketoDestinationPropertiesProperty(
                            object="object",
            
                            # the properties below are optional
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            )
                        ),
                        redshift=appflow.CfnFlow.RedshiftDestinationPropertiesProperty(
                            intermediate_bucket_name="intermediateBucketName",
                            object="object",
            
                            # the properties below are optional
                            bucket_prefix="bucketPrefix",
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            )
                        ),
                        s3=appflow.CfnFlow.S3DestinationPropertiesProperty(
                            bucket_name="bucketName",
            
                            # the properties below are optional
                            bucket_prefix="bucketPrefix",
                            s3_output_format_config=appflow.CfnFlow.S3OutputFormatConfigProperty(
                                aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                                    aggregation_type="aggregationType",
                                    target_file_size=123
                                ),
                                file_type="fileType",
                                prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                                    path_prefix_hierarchy=["pathPrefixHierarchy"],
                                    prefix_format="prefixFormat",
                                    prefix_type="prefixType"
                                ),
                                preserve_source_data_typing=False
                            )
                        ),
                        salesforce=appflow.CfnFlow.SalesforceDestinationPropertiesProperty(
                            object="object",
            
                            # the properties below are optional
                            data_transfer_api="dataTransferApi",
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            write_operation_type="writeOperationType"
                        ),
                        sapo_data=appflow.CfnFlow.SAPODataDestinationPropertiesProperty(
                            object_path="objectPath",
            
                            # the properties below are optional
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            success_response_handling_config=appflow.CfnFlow.SuccessResponseHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix"
                            ),
                            write_operation_type="writeOperationType"
                        ),
                        snowflake=appflow.CfnFlow.SnowflakeDestinationPropertiesProperty(
                            intermediate_bucket_name="intermediateBucketName",
                            object="object",
            
                            # the properties below are optional
                            bucket_prefix="bucketPrefix",
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            )
                        ),
                        upsolver=appflow.CfnFlow.UpsolverDestinationPropertiesProperty(
                            bucket_name="bucketName",
                            s3_output_format_config=appflow.CfnFlow.UpsolverS3OutputFormatConfigProperty(
                                prefix_config=appflow.CfnFlow.PrefixConfigProperty(
                                    path_prefix_hierarchy=["pathPrefixHierarchy"],
                                    prefix_format="prefixFormat",
                                    prefix_type="prefixType"
                                ),
            
                                # the properties below are optional
                                aggregation_config=appflow.CfnFlow.AggregationConfigProperty(
                                    aggregation_type="aggregationType",
                                    target_file_size=123
                                ),
                                file_type="fileType"
                            ),
            
                            # the properties below are optional
                            bucket_prefix="bucketPrefix"
                        ),
                        zendesk=appflow.CfnFlow.ZendeskDestinationPropertiesProperty(
                            object="object",
            
                            # the properties below are optional
                            error_handling_config=appflow.CfnFlow.ErrorHandlingConfigProperty(
                                bucket_name="bucketName",
                                bucket_prefix="bucketPrefix",
                                fail_on_first_error=False
                            ),
                            id_field_names=["idFieldNames"],
                            write_operation_type="writeOperationType"
                        )
                    ),
            
                    # the properties below are optional
                    api_version="apiVersion",
                    connector_profile_name="connectorProfileName"
                )],
                flow_name="flowName",
                source_flow_config=appflow.CfnFlow.SourceFlowConfigProperty(
                    connector_type="connectorType",
                    source_connector_properties=appflow.CfnFlow.SourceConnectorPropertiesProperty(
                        amplitude=appflow.CfnFlow.AmplitudeSourcePropertiesProperty(
                            object="object"
                        ),
                        custom_connector=appflow.CfnFlow.CustomConnectorSourcePropertiesProperty(
                            entity_name="entityName",
            
                            # the properties below are optional
                            custom_properties={
                                "custom_properties_key": "customProperties"
                            }
                        ),
                        datadog=appflow.CfnFlow.DatadogSourcePropertiesProperty(
                            object="object"
                        ),
                        dynatrace=appflow.CfnFlow.DynatraceSourcePropertiesProperty(
                            object="object"
                        ),
                        google_analytics=appflow.CfnFlow.GoogleAnalyticsSourcePropertiesProperty(
                            object="object"
                        ),
                        infor_nexus=appflow.CfnFlow.InforNexusSourcePropertiesProperty(
                            object="object"
                        ),
                        marketo=appflow.CfnFlow.MarketoSourcePropertiesProperty(
                            object="object"
                        ),
                        s3=appflow.CfnFlow.S3SourcePropertiesProperty(
                            bucket_name="bucketName",
                            bucket_prefix="bucketPrefix",
            
                            # the properties below are optional
                            s3_input_format_config=appflow.CfnFlow.S3InputFormatConfigProperty(
                                s3_input_file_type="s3InputFileType"
                            )
                        ),
                        salesforce=appflow.CfnFlow.SalesforceSourcePropertiesProperty(
                            object="object",
            
                            # the properties below are optional
                            data_transfer_api="dataTransferApi",
                            enable_dynamic_field_update=False,
                            include_deleted_records=False
                        ),
                        sapo_data=appflow.CfnFlow.SAPODataSourcePropertiesProperty(
                            object_path="objectPath"
                        ),
                        service_now=appflow.CfnFlow.ServiceNowSourcePropertiesProperty(
                            object="object"
                        ),
                        singular=appflow.CfnFlow.SingularSourcePropertiesProperty(
                            object="object"
                        ),
                        slack=appflow.CfnFlow.SlackSourcePropertiesProperty(
                            object="object"
                        ),
                        trendmicro=appflow.CfnFlow.TrendmicroSourcePropertiesProperty(
                            object="object"
                        ),
                        veeva=appflow.CfnFlow.VeevaSourcePropertiesProperty(
                            object="object",
            
                            # the properties below are optional
                            document_type="documentType",
                            include_all_versions=False,
                            include_renditions=False,
                            include_source_files=False
                        ),
                        zendesk=appflow.CfnFlow.ZendeskSourcePropertiesProperty(
                            object="object"
                        )
                    ),
            
                    # the properties below are optional
                    api_version="apiVersion",
                    connector_profile_name="connectorProfileName",
                    incremental_pull_config=appflow.CfnFlow.IncrementalPullConfigProperty(
                        datetime_type_field_name="datetimeTypeFieldName"
                    )
                ),
                tasks=[appflow.CfnFlow.TaskProperty(
                    source_fields=["sourceFields"],
                    task_type="taskType",
            
                    # the properties below are optional
                    connector_operator=appflow.CfnFlow.ConnectorOperatorProperty(
                        amplitude="amplitude",
                        custom_connector="customConnector",
                        datadog="datadog",
                        dynatrace="dynatrace",
                        google_analytics="googleAnalytics",
                        infor_nexus="inforNexus",
                        marketo="marketo",
                        s3="s3",
                        salesforce="salesforce",
                        sapo_data="sapoData",
                        service_now="serviceNow",
                        singular="singular",
                        slack="slack",
                        trendmicro="trendmicro",
                        veeva="veeva",
                        zendesk="zendesk"
                    ),
                    destination_field="destinationField",
                    task_properties=[appflow.CfnFlow.TaskPropertiesObjectProperty(
                        key="key",
                        value="value"
                    )]
                )],
                trigger_config=appflow.CfnFlow.TriggerConfigProperty(
                    trigger_type="triggerType",
            
                    # the properties below are optional
                    trigger_properties=appflow.CfnFlow.ScheduledTriggerPropertiesProperty(
                        schedule_expression="scheduleExpression",
            
                        # the properties below are optional
                        data_pull_mode="dataPullMode",
                        first_execution_from=123,
                        flow_error_deactivation_threshold=123,
                        schedule_end_time=123,
                        schedule_offset=123,
                        schedule_start_time=123,
                        time_zone="timeZone"
                    )
                ),
            
                # the properties below are optional
                description="description",
                kms_arn="kmsArn",
                metadata_catalog_config=appflow.CfnFlow.MetadataCatalogConfigProperty(
                    glue_data_catalog=appflow.CfnFlow.GlueDataCatalogProperty(
                        database_name="databaseName",
                        role_arn="roleArn",
                        table_prefix="tablePrefix"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49fae84181907d0113c9ca6d78c7a436fd453b222cfd8f0a7daa9e9b34e69bb)
            check_type(argname="argument destination_flow_config_list", value=destination_flow_config_list, expected_type=type_hints["destination_flow_config_list"])
            check_type(argname="argument flow_name", value=flow_name, expected_type=type_hints["flow_name"])
            check_type(argname="argument source_flow_config", value=source_flow_config, expected_type=type_hints["source_flow_config"])
            check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
            check_type(argname="argument trigger_config", value=trigger_config, expected_type=type_hints["trigger_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
            check_type(argname="argument metadata_catalog_config", value=metadata_catalog_config, expected_type=type_hints["metadata_catalog_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_flow_config_list": destination_flow_config_list,
            "flow_name": flow_name,
            "source_flow_config": source_flow_config,
            "tasks": tasks,
            "trigger_config": trigger_config,
        }
        if description is not None:
            self._values["description"] = description
        if kms_arn is not None:
            self._values["kms_arn"] = kms_arn
        if metadata_catalog_config is not None:
            self._values["metadata_catalog_config"] = metadata_catalog_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_flow_config_list(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.DestinationFlowConfigProperty, _IResolvable_a771d0ef]]]:
        '''The configuration that controls how Amazon AppFlow places data in the destination connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-destinationflowconfiglist
        '''
        result = self._values.get("destination_flow_config_list")
        assert result is not None, "Required property 'destination_flow_config_list' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.DestinationFlowConfigProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def flow_name(self) -> builtins.str:
        '''The specified name of the flow.

        Spaces are not allowed. Use underscores (_) or hyphens (-) only.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-flowname
        '''
        result = self._values.get("flow_name")
        assert result is not None, "Required property 'flow_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_flow_config(
        self,
    ) -> typing.Union[CfnFlow.SourceFlowConfigProperty, _IResolvable_a771d0ef]:
        '''Contains information about the configuration of the source connector used in the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-sourceflowconfig
        '''
        result = self._values.get("source_flow_config")
        assert result is not None, "Required property 'source_flow_config' is missing"
        return typing.cast(typing.Union[CfnFlow.SourceFlowConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def tasks(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.TaskProperty, _IResolvable_a771d0ef]]]:
        '''A list of tasks that Amazon AppFlow performs while transferring the data in the flow run.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-tasks
        '''
        result = self._values.get("tasks")
        assert result is not None, "Required property 'tasks' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.TaskProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def trigger_config(
        self,
    ) -> typing.Union[CfnFlow.TriggerConfigProperty, _IResolvable_a771d0ef]:
        '''The trigger settings that determine how and when Amazon AppFlow runs the specified flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-triggerconfig
        '''
        result = self._values.get("trigger_config")
        assert result is not None, "Required property 'trigger_config' is missing"
        return typing.cast(typing.Union[CfnFlow.TriggerConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A user-entered description of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN (Amazon Resource Name) of the Key Management Service (KMS) key you provide for encryption.

        This is required if you do not want to use the Amazon AppFlow-managed KMS key. If you don't provide anything here, Amazon AppFlow uses the Amazon AppFlow-managed KMS key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-kmsarn
        '''
        result = self._values.get("kms_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_catalog_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFlow.MetadataCatalogConfigProperty, _IResolvable_a771d0ef]]:
        '''``AWS::AppFlow::Flow.MetadataCatalogConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-metadatacatalogconfig
        '''
        result = self._values.get("metadata_catalog_config")
        return typing.cast(typing.Optional[typing.Union[CfnFlow.MetadataCatalogConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags used to organize, track, or control access for your flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnConnector",
    "CfnConnectorProfile",
    "CfnConnectorProfileProps",
    "CfnConnectorProps",
    "CfnFlow",
    "CfnFlowProps",
]

publication.publish()

def _typecheckingstub__e8ff4f04437a5f46fcbff59e0b0cf6117ebfbf772738ac5c08138a28bdf620d9(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    connector_provisioning_config: typing.Union[typing.Union[CfnConnector.ConnectorProvisioningConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    connector_provisioning_type: builtins.str,
    connector_label: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0882db8ad760095ecc0b5001a8b537d1bd8503f9215369ff372c1b18b42fcc42(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9504e45eeca5b33c866ee918a80463eb915bb61edc39ffd82b5a062cf8132774(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f1c2e1c90fa69616b64ffcea077cf403987bde575c5c5a6a9b2a239f093a73(
    value: typing.Union[CfnConnector.ConnectorProvisioningConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd7283c4d8e58d8e3fe091b9ddc8024865cbc39907b2f8d61b1c6f34afbddb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb16193d92abc6f931ddccebd12527d9a255e7ffd3e0f1af2a30bec07e5ff74c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5dd008065fe32cae21697cdc754bd328c2f80d9ee37b7101693be01ed1c25bb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a02544e9c3ae67993f60880468a4b7ac6afae6e70f8edfe8b4a9514095cc1f6(
    *,
    lambda_: typing.Optional[typing.Union[typing.Union[CfnConnector.LambdaConnectorProvisioningConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afb2c79f0291a3aa005582e06df074853105a886415dc3c775319f3b936760f(
    *,
    lambda_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8eb9502d20e93fc189f7b2c3397d6075e3da66c825abe8f3fc545bfc2b68533(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    connection_mode: builtins.str,
    connector_profile_name: builtins.str,
    connector_type: builtins.str,
    connector_label: typing.Optional[builtins.str] = None,
    connector_profile_config: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorProfileConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kms_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83945d45cae5d4442413b691bbef4a2cc6ea3bcb7867de7e42d65f56f265d06a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3d8a30485056bf5ff54f3922f7355f9fdaf4550de4d1a19eea40a1a32c77ba(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13dce0806e50b0c8a980d1e52eddbd108f50898a1a9b7f8a69288a8c27c40686(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96290196aecdcbfa9845ff2f03c4aff4a0d9e703da8fc60bd1626ef516282700(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b1c508a5eb34e541fc61971f6d20d8c5ccaf98ebb183bcb83ab1391839b40d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26a793c6d824532222f46a24570db10c51428def9ce77de59116253746bdfd0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd9e5f28bfe7655bc3f14ae38a70630107300c5c2ef80f7f56505175fd8e1fc(
    value: typing.Optional[typing.Union[CfnConnectorProfile.ConnectorProfileConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54deec5ddc1adf2d40f83ae02eeb29948d7b6bb941112ddf2bbd52f0fbdb2ee(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a5da9cdcffbb8dafa69e9abd47ef20fb1d346d576ee543060843e8391d5a6f(
    *,
    api_key: builtins.str,
    secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9b3badcf958489c36f45067a3b2a9daa22fbbae2e8d83e66eb562de42fa8e4(
    *,
    api_key: builtins.str,
    api_secret_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d718b1d9e79c164ef87c9bfdd498477219637f73093fed2b95b31e04448ecd(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc62cb1e080157692013247ff6dbb7ef7c466ebb410a6f5039e941e2beded0f(
    *,
    auth_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a422ca98001869d49822eae9b9d000f3de74c14ac977dc6db143d85f28ab712(
    *,
    connector_profile_credentials: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    connector_profile_properties: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7aeb38b062444edd1e912ad69a5f20a6aaf8dc09a2ef57a8ea0f5866948c6f(
    *,
    amplitude: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    custom_connector: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.CustomConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    datadog: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dynatrace: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    google_analytics: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    infor_nexus: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    marketo: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    redshift: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    salesforce: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sapo_data: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.SAPODataConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    service_now: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    singular: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.SingularConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    slack: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.SlackConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    snowflake: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    trendmicro: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    veeva: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    zendesk: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f8ebf6fe45477f0a0cf775b1b4f239df8c61f354af4bba207ec4bcda2af3c1(
    *,
    custom_connector: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.CustomConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    datadog: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dynatrace: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    infor_nexus: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    marketo: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    redshift: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    salesforce: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sapo_data: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.SAPODataConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    service_now: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    slack: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.SlackConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    snowflake: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    veeva: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    zendesk: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2ef138c3cdf30e92501b90e20140d75856db130ce044fbd2dd5304fc11f97d(
    *,
    custom_authentication_type: builtins.str,
    credentials_map: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626190f5d8426cdea17382f3d5c6061ac2a86c0ce668de1cb231ed845d8cbf4a(
    *,
    authentication_type: builtins.str,
    api_key: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ApiKeyCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    basic: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.BasicAuthCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    custom: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.CustomAuthCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    oauth2: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.OAuth2CredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd60cc1132f08652aa01f35297d8b30ba83efb7bf211120e20503f4749cf2fcc(
    *,
    o_auth2_properties: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.OAuth2PropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    profile_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba67988cea79a2c26e774cf5d4010ac43b7bc4e040be48cb066498c64378b79(
    *,
    api_key: builtins.str,
    application_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf53a8bc9044d0b82d700d8652d0170a9ae3c3eb6977b19294a2b5bb882e77e(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded83bd3a51c78fbe3cc7d64a788a133417929b90ac0e52bac9910b1eb73cabd(
    *,
    api_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd802cadff541625986a8610ad585e0e0885a2c93cdb93ecaed2b4daa21ec1b(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ae4c2cbbf024279993481f99b917147bea4760342de59936ff72b6fa247769(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292d15a0a6dca37cfff025faba0949c388e17965cfdfbe3b86dc3282ea1e0801(
    *,
    access_key_id: builtins.str,
    datakey: builtins.str,
    secret_access_key: builtins.str,
    user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55ae28aeb412ac0719da12895b200cdeb5bc9bcce4c9e0f972e4b84384e1bed(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db046ca0fa9202b2c1faaeb64a39a0d25d00a4e95f41d0041b8a01b5b78d0ec6(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b131698bc4a407e9f60ba1ddb62bdba8b516303805ebcba22a843a70765879fd(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1c6c60f9315a221004c26519158fa97d114b541cb2d7ff44ba2b136753b9b3(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    o_auth_request: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3abb37c6b0692ac7dfae871fd061da42edef854094dbcd29dcb47ba308c8984(
    *,
    o_auth2_grant_type: typing.Optional[builtins.str] = None,
    token_url: typing.Optional[builtins.str] = None,
    token_url_custom_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77655d54a586d4ebf0175695038d81926f62ea76baf85a07885b64458e706dfe(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1a2d110e424078c861bd1321e5ebcdacd77a32007566431501f33d9de42434(
    *,
    auth_code_url: typing.Optional[builtins.str] = None,
    o_auth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    token_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe1f40330a114802768f1b30b4825e4cfec41252a5dc3a939b846e97303cd8a(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906416d8d62fdb2bbd22f109b5196f53f284f1adf51ebcba3c0da500b89f9fda(
    *,
    bucket_name: builtins.str,
    role_arn: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    cluster_identifier: typing.Optional[builtins.str] = None,
    data_api_role_arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    database_url: typing.Optional[builtins.str] = None,
    is_redshift_serverless: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    workgroup_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d39d24382f990d02f6143725bc22a8d7d6e7664d5f75d236bcaee863f132a45(
    *,
    basic_auth_credentials: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.BasicAuthCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    o_auth_credentials: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.OAuthCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30fbed7b65e64022968e1bf0deaec358fa031306a0c9a1797c7b8d576d7c3cb(
    *,
    application_host_url: typing.Optional[builtins.str] = None,
    application_service_path: typing.Optional[builtins.str] = None,
    client_number: typing.Optional[builtins.str] = None,
    logon_language: typing.Optional[builtins.str] = None,
    o_auth_properties: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.OAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    port_number: typing.Optional[jsii.Number] = None,
    private_link_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472b57cd8fd56668ca08b10a90d67d5b9092be899fbc14dcc68d28924d850019(
    *,
    access_token: typing.Optional[builtins.str] = None,
    client_credentials_arn: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    refresh_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416405de6dfe84b3d6e753ebac22fb34732acd07c382ce25e307ae98debd59c4(
    *,
    instance_url: typing.Optional[builtins.str] = None,
    is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d684f6048a67e7410593dc9206f103be70f5fe79df8348ed9dd46f1f62973eb(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec490d1810108c4d518dc3577d17d88d2b87e28fef582e3cd27b0b6cbe872575(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3ababce2e8ec288c1139f68fb0f67e76c59f9f47828884af20ca4321b832e9(
    *,
    api_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6bcf949576d5850339ca29cddfeb922df4b84c1bf934e74f907d363ee85ba80(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a231bd1fb30bc7a464c6400efae6e9810c2ec20af0c18c8299ff73fb230d7df1(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95fc3c354a6bce5504786d7d7a1dab9bb06ac1ba07d5eeadf1e8dd05d68fdde(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380486fef1f3337d8e5198073dd1b40621287933f1b1253647ff12830af36452(
    *,
    bucket_name: builtins.str,
    stage: builtins.str,
    warehouse: builtins.str,
    account_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    private_link_service_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5f3419a654523c1ce16503a1541d0d771e83e8cf7330290347bad21e769fe6(
    *,
    api_secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248eb382a50e7d296f2bb207c285178097f63d711fa318fde5bca273b09190c2(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c93b9947f5f31ca49b7d62349aceeed18ec9c7261eff6086f5ae74366ed74cf(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbaf615a04b7e602f15c770ff91d95063ee5dda4b7d15b81786506f63360cf85(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    connector_o_auth_request: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorOAuthRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e794eb1bb8458dc0a1bf8a4f7d62829dd68fbaffee0d864f7f545de837ef82d(
    *,
    instance_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ccb75d0f6887e2084432b99a23188877b656380a81b84f28ac00ef302fbc660(
    *,
    connection_mode: builtins.str,
    connector_profile_name: builtins.str,
    connector_type: builtins.str,
    connector_label: typing.Optional[builtins.str] = None,
    connector_profile_config: typing.Optional[typing.Union[typing.Union[CfnConnectorProfile.ConnectorProfileConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kms_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742c870b9ce78a5ebed778edde9e07534348334977ac3ac52a5d66d9257138c3(
    *,
    connector_provisioning_config: typing.Union[typing.Union[CfnConnector.ConnectorProvisioningConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    connector_provisioning_type: builtins.str,
    connector_label: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a29e3eeb5e5c052af42caaa40bfc5fa9ab3f3ffa666275a8fa4f69e20f59ecc(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    destination_flow_config_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFlow.DestinationFlowConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    flow_name: builtins.str,
    source_flow_config: typing.Union[typing.Union[CfnFlow.SourceFlowConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    tasks: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFlow.TaskProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    trigger_config: typing.Union[typing.Union[CfnFlow.TriggerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    metadata_catalog_config: typing.Optional[typing.Union[typing.Union[CfnFlow.MetadataCatalogConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6410a78806435da2c1aa97db2d2d301f6d6c8da55b903cf03611f7390e461161(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e7b4d9f259ccd73fe979110cec8e960301139ed48fd58dd36961d95922fd7a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303dcae9337390c21aeaa62833b4b4c92a196572c71ba898724f63e60140878e(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.DestinationFlowConfigProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3941d423f68cf70da9f60b09912f505dc349ce2c945820fb5b07b8b0ab8d51f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aecd640c011b84bccc6fea3cfac6a7e6ee5250777d80d57b8025852ce6588a5(
    value: typing.Union[CfnFlow.SourceFlowConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6aca99025097d768f44c9b04d3117c40a983a63a97b44aa57d5bc63aeba19a(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.TaskProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53656ef317c12440802a02f88035fb13b58980deaf42dfd07a0f972d9ef90a2(
    value: typing.Union[CfnFlow.TriggerConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4471ca08541e13485a6594fb9d31d02a1260d7582748b029c8fce706961d5e3c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e066fde0756ae35d101b0afaa40541384e780baf6df93ba55b7a0599f33ad86(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e6ca8921c77880f28fcf5284732766b6296d226e5ac1c35feef24076c870fb(
    value: typing.Optional[typing.Union[CfnFlow.MetadataCatalogConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f510e57471eda2e5d7abf40ba7799f618a39fd62448753cd69010f0c1b68ba6(
    *,
    aggregation_type: typing.Optional[builtins.str] = None,
    target_file_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333f84c2013d82782a87ff6ba9d75382ecaa7ace6cce000d4cb69a0e347d875f(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bae7a1401a59026a310dd47b48386a01301301fdf23c8bfc8af45b341b809a3(
    *,
    amplitude: typing.Optional[builtins.str] = None,
    custom_connector: typing.Optional[builtins.str] = None,
    datadog: typing.Optional[builtins.str] = None,
    dynatrace: typing.Optional[builtins.str] = None,
    google_analytics: typing.Optional[builtins.str] = None,
    infor_nexus: typing.Optional[builtins.str] = None,
    marketo: typing.Optional[builtins.str] = None,
    s3: typing.Optional[builtins.str] = None,
    salesforce: typing.Optional[builtins.str] = None,
    sapo_data: typing.Optional[builtins.str] = None,
    service_now: typing.Optional[builtins.str] = None,
    singular: typing.Optional[builtins.str] = None,
    slack: typing.Optional[builtins.str] = None,
    trendmicro: typing.Optional[builtins.str] = None,
    veeva: typing.Optional[builtins.str] = None,
    zendesk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8d3f37050c188e7c5decca80efb64b67ea330c8e4327166144cb1b5b2ed031(
    *,
    entity_name: builtins.str,
    custom_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    error_handling_config: typing.Optional[typing.Union[typing.Union[CfnFlow.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d6ac27e49c2dd0458091139952cd62cb3292e9da5dc884e4ce91b1b9a2bc0f(
    *,
    entity_name: builtins.str,
    custom_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a9fff97e3b1089c64e09c2cd137e1970a19b0a7d009f33488cdebea7ec6626(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbcb54157230c34afc753ec9e1ac4c545ae4d9ac4f10efe680101457e884d47(
    *,
    custom_connector: typing.Optional[typing.Union[typing.Union[CfnFlow.CustomConnectorDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    event_bridge: typing.Optional[typing.Union[typing.Union[CfnFlow.EventBridgeDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    lookout_metrics: typing.Optional[typing.Union[typing.Union[CfnFlow.LookoutMetricsDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    marketo: typing.Optional[typing.Union[typing.Union[CfnFlow.MarketoDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    redshift: typing.Optional[typing.Union[typing.Union[CfnFlow.RedshiftDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    s3: typing.Optional[typing.Union[typing.Union[CfnFlow.S3DestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    salesforce: typing.Optional[typing.Union[typing.Union[CfnFlow.SalesforceDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sapo_data: typing.Optional[typing.Union[typing.Union[CfnFlow.SAPODataDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    snowflake: typing.Optional[typing.Union[typing.Union[CfnFlow.SnowflakeDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    upsolver: typing.Optional[typing.Union[typing.Union[CfnFlow.UpsolverDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    zendesk: typing.Optional[typing.Union[typing.Union[CfnFlow.ZendeskDestinationPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94052587a94fbd68cffa3b927906ab33367359151648bce7d72e971bdf4efbb2(
    *,
    connector_type: builtins.str,
    destination_connector_properties: typing.Union[typing.Union[CfnFlow.DestinationConnectorPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    api_version: typing.Optional[builtins.str] = None,
    connector_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00986a8531c33079ebdc1d864270c7da97f2ef8b2eb991543bd83b424ff73b2(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe610b6f7899b376c5f5cf2b1174b8f6fa5089598754d8409551f868e9423448(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_error: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1fa81722b4ab8c8337bffafe926c81784b5b2b3e7188c84d5f4ffa6b02f13c(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[typing.Union[CfnFlow.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8627d1babee7f65f296693bb422153e01c8dd719cf94878c5db73fb6d9576ea(
    *,
    database_name: builtins.str,
    role_arn: builtins.str,
    table_prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7330f49790ab7f1dd63ad225eb5b147b7443421aff90c9d1896a1b10166ef0df(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b934240d253719aa264a533d4c3b2b87aab1e5506d4a674631de412614ab15(
    *,
    datetime_type_field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fe00e26bc12c3a7aeaf2a61c2dd069aa260c3faff8341531b3291980376c91(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a950d336f3a8d36e0a4e1ee6fe0c5b1b4ffdb03679b615896f9603b7ebd42ef(
    *,
    object: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058ac5ad26c35ae3470a019a6301ebc8685522b1ab68359be4cad94a85bfb523(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[typing.Union[CfnFlow.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389474f6f1601bd5590fbb5b19bcb38f1bf454c696677736a6fe5c554129c4e3(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5333a0f2cf102f80173da134345cdc5b979535301620812aa2184cb07e16f7d(
    *,
    glue_data_catalog: typing.Optional[typing.Union[typing.Union[CfnFlow.GlueDataCatalogProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe807b70844271724d9e74132427ef742073ad7e9310506532e594a065842e9c(
    *,
    path_prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefix_format: typing.Optional[builtins.str] = None,
    prefix_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0cff64b64c9128d2fb298e4baa58910381f4c6d360790808501593257ea3456(
    *,
    intermediate_bucket_name: builtins.str,
    object: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[typing.Union[CfnFlow.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c7a4861db207389a59210e3d58a59ed0429584c3732b7368f3ee94ae03cc04(
    *,
    bucket_name: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    s3_output_format_config: typing.Optional[typing.Union[typing.Union[CfnFlow.S3OutputFormatConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84bcadb90cc9c9d021f2d7040ac3a4d7ef5688aeb18fb00a5efca87c55b554a(
    *,
    s3_input_file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf7b7e6a439a254fa59b7671858e0a6aaf563655c691af16b5ca4a725e891a5(
    *,
    aggregation_config: typing.Optional[typing.Union[typing.Union[CfnFlow.AggregationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    file_type: typing.Optional[builtins.str] = None,
    prefix_config: typing.Optional[typing.Union[typing.Union[CfnFlow.PrefixConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    preserve_source_data_typing: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f1c227c28403417018ff3eca1cfd15f7fe47a3d0489b982e89862031f06b25(
    *,
    bucket_name: builtins.str,
    bucket_prefix: builtins.str,
    s3_input_format_config: typing.Optional[typing.Union[typing.Union[CfnFlow.S3InputFormatConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7657b4410036725667a928e0439e362b9a0f634f91d5af6255341206302d1307(
    *,
    object_path: builtins.str,
    error_handling_config: typing.Optional[typing.Union[typing.Union[CfnFlow.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    success_response_handling_config: typing.Optional[typing.Union[typing.Union[CfnFlow.SuccessResponseHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041d9138357a1a1234cab91e5fc76b79df1b59bb9cee37c96270c0c259e888ae(
    *,
    object_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc49be76541f78ae7d0704ff39b52b0ead403952e8a817d19676b73fc334448(
    *,
    object: builtins.str,
    data_transfer_api: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[typing.Union[CfnFlow.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e3295c4d0e1986be65d007de88364ddc4285a81aabce26509a9c4f6fdb0388(
    *,
    object: builtins.str,
    data_transfer_api: typing.Optional[builtins.str] = None,
    enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    include_deleted_records: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9ada7e145ed6ee0ce866bdeb981968ca75dcc922c908e14dc16b37b40f0c7e(
    *,
    schedule_expression: builtins.str,
    data_pull_mode: typing.Optional[builtins.str] = None,
    first_execution_from: typing.Optional[jsii.Number] = None,
    flow_error_deactivation_threshold: typing.Optional[jsii.Number] = None,
    schedule_end_time: typing.Optional[jsii.Number] = None,
    schedule_offset: typing.Optional[jsii.Number] = None,
    schedule_start_time: typing.Optional[jsii.Number] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a061e2c155d302b314cbae30a2ad44c905f42c3a5a528542788d8447396c2447(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866767ce0b7bc8b3c571e82b88bd14212763f5d5b8f9bd8c73c24d107eba3989(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16517a0e6a52c6cb221fb336b0ef598de20d5c52a9061ae97f7e913c467cc7d9(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c850effc6f3445201cd85e3e0f6ef097d018aa7ae4fa78d3987ea543fdbbd1(
    *,
    intermediate_bucket_name: builtins.str,
    object: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[typing.Union[CfnFlow.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3378cd727c580ef9d24acb7bfa9d5ba2e4aab3872dd5185ef986071f594a1140(
    *,
    amplitude: typing.Optional[typing.Union[typing.Union[CfnFlow.AmplitudeSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    custom_connector: typing.Optional[typing.Union[typing.Union[CfnFlow.CustomConnectorSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    datadog: typing.Optional[typing.Union[typing.Union[CfnFlow.DatadogSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dynatrace: typing.Optional[typing.Union[typing.Union[CfnFlow.DynatraceSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    google_analytics: typing.Optional[typing.Union[typing.Union[CfnFlow.GoogleAnalyticsSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    infor_nexus: typing.Optional[typing.Union[typing.Union[CfnFlow.InforNexusSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    marketo: typing.Optional[typing.Union[typing.Union[CfnFlow.MarketoSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    s3: typing.Optional[typing.Union[typing.Union[CfnFlow.S3SourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    salesforce: typing.Optional[typing.Union[typing.Union[CfnFlow.SalesforceSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sapo_data: typing.Optional[typing.Union[typing.Union[CfnFlow.SAPODataSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    service_now: typing.Optional[typing.Union[typing.Union[CfnFlow.ServiceNowSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    singular: typing.Optional[typing.Union[typing.Union[CfnFlow.SingularSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    slack: typing.Optional[typing.Union[typing.Union[CfnFlow.SlackSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    trendmicro: typing.Optional[typing.Union[typing.Union[CfnFlow.TrendmicroSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    veeva: typing.Optional[typing.Union[typing.Union[CfnFlow.VeevaSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    zendesk: typing.Optional[typing.Union[typing.Union[CfnFlow.ZendeskSourcePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4f9234c873099d73c2b858e2c6c924cc145c47dfbf38427f49442b8deb6fa5(
    *,
    connector_type: builtins.str,
    source_connector_properties: typing.Union[typing.Union[CfnFlow.SourceConnectorPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    api_version: typing.Optional[builtins.str] = None,
    connector_profile_name: typing.Optional[builtins.str] = None,
    incremental_pull_config: typing.Optional[typing.Union[typing.Union[CfnFlow.IncrementalPullConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f157805877d013d4f9a57c63e74ae0e585184e780befcb208dda0206902fa01(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab41b4b9ff7e622a3ecb5af9692c152aa0206c867c4f69cc71f8632314fcae9(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07eaf0dbbae9ff1c353003786e1be5a4e0968dae55caa457da2430212a949236(
    *,
    source_fields: typing.Sequence[builtins.str],
    task_type: builtins.str,
    connector_operator: typing.Optional[typing.Union[typing.Union[CfnFlow.ConnectorOperatorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    destination_field: typing.Optional[builtins.str] = None,
    task_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFlow.TaskPropertiesObjectProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ba28f6151f0b9cdcb2afdde4332e0fbcfe04eadfc59a9e424ea1789cd9686d(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73213e14a9b6c30e52c321e4e38f3c636cd411e91e09864eb93aeb44d0dce3b(
    *,
    trigger_type: builtins.str,
    trigger_properties: typing.Optional[typing.Union[typing.Union[CfnFlow.ScheduledTriggerPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220d9c452eca21c99b2192e5bfdb02e955894042ada097db7fd93bac0b6d26f6(
    *,
    bucket_name: builtins.str,
    s3_output_format_config: typing.Union[typing.Union[CfnFlow.UpsolverS3OutputFormatConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96c2b5f28ca72db19de71c46435a5da2000c65f0ab8c40d4ab286d557edd8c9(
    *,
    prefix_config: typing.Union[typing.Union[CfnFlow.PrefixConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    aggregation_config: typing.Optional[typing.Union[typing.Union[CfnFlow.AggregationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9243e1f4370d9f2c91ee392c0cdff977925796dcf0d92a5fee0655dfd64a7fb2(
    *,
    object: builtins.str,
    document_type: typing.Optional[builtins.str] = None,
    include_all_versions: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    include_renditions: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    include_source_files: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d98bc38b9a1a47e9780fc455cd0dc6b753d247c250d6c2c3fbbbea4e410234(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[typing.Union[CfnFlow.ErrorHandlingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f16f6d9214ed83e91799141c7a085c85eb72506b3663bf64a450ec9271b83bb(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49fae84181907d0113c9ca6d78c7a436fd453b222cfd8f0a7daa9e9b34e69bb(
    *,
    destination_flow_config_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFlow.DestinationFlowConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    flow_name: builtins.str,
    source_flow_config: typing.Union[typing.Union[CfnFlow.SourceFlowConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    tasks: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFlow.TaskProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    trigger_config: typing.Union[typing.Union[CfnFlow.TriggerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    metadata_catalog_config: typing.Optional[typing.Union[typing.Union[CfnFlow.MetadataCatalogConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
