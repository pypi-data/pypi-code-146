'''
The static-website module is able to deploy your pre-packaged static website content into an S3 Bucket, fronted by Cloudfront. This module uses an Origin Access Identity to ensure your Bucket can only be accessed via Cloudfront and is configured to only allow HTTPS requests by default. Custom runtime configurations can also be specified which will emit a runtime-config.json file along with your website content. Typically this includes resource Arns, Id's etc which may need to be referenced from your website. This package uses sane defaults and at a minimum only requires the path to your website assets.

Below is a conceptual view of the default architecture this module creates:

```
Cloudfront Distribution (HTTPS only) -> S3 Bucket (Private via OAI)
|_ WAF V2 ACL                                |_ index.html (+ other website files and assets)
                                             |_ runtime-config.json
```

A typical use case is to create a static website with AuthN. To accomplish this, we can leverage the UserIdentity to create the User Pool (Cognito by default) and Identity Pool. We can then pipe the respective pool id's as runtimeOptions into the StaticWebsite. After the website is deployed, these values can be interrogated from the runtime-config.json deployed alongside the website in order to perform authentication within the app using something like the [Amplify Auth API](https://docs.amplify.aws/lib/client-configuration/configuring-amplify-categories/q/platform/js/#authentication-amazon-cognito).

```python
const userIdentity = new UserIdentity(this, 'UserIdentity');
new StaticWebsite(this, 'StaticWebsite', {
    websiteContentPath: '<relative>/<path>/<to>/<built>/<website>',
    runtimeOptions: {
        jsonPayload: {
            region: Stack.of(this).region,
            identityPoolId: userIdentity.identityPool.identityPoolId,
            userPoolId: userIdentity.userPool?.userPoolId,
            userPoolWebClientId: userIdentity.userPoolClient?.userPoolClientId,
        }
    },
});
```
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

from ._jsii import *

import aws_cdk.aws_cloudfront
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import aws_cdk.aws_s3_deployment
import constructs


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.CidrAllowList",
    jsii_struct_bases=[],
    name_mapping={"cidr_ranges": "cidrRanges", "cidr_type": "cidrType"},
)
class CidrAllowList:
    def __init__(
        self,
        *,
        cidr_ranges: typing.Sequence[builtins.str],
        cidr_type: builtins.str,
    ) -> None:
        '''(experimental) Representation of a CIDR range.

        :param cidr_ranges: (experimental) Specify an IPv4 address by using CIDR notation. For example: To configure AWS WAF to allow, block, or count requests that originated from the IP address 192.0.2.44, specify 192.0.2.44/32 . To configure AWS WAF to allow, block, or count requests that originated from IP addresses from 192.0.2.0 to 192.0.2.255, specify 192.0.2.0/24 . For more information about CIDR notation, see the Wikipedia entry Classless Inter-Domain Routing . Specify an IPv6 address by using CIDR notation. For example: To configure AWS WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify 1111:0000:0000:0000:0000:0000:0000:0111/128 . To configure AWS WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify 1111:0000:0000:0000:0000:0000:0000:0000/64 .
        :param cidr_type: (experimental) Type of CIDR range.

        :stability: experimental
        '''
        if __debug__:
            def stub(
                *,
                cidr_ranges: typing.Sequence[builtins.str],
                cidr_type: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument cidr_ranges", value=cidr_ranges, expected_type=type_hints["cidr_ranges"])
            check_type(argname="argument cidr_type", value=cidr_type, expected_type=type_hints["cidr_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "cidr_ranges": cidr_ranges,
            "cidr_type": cidr_type,
        }

    @builtins.property
    def cidr_ranges(self) -> typing.List[builtins.str]:
        '''(experimental) Specify an IPv4 address by using CIDR notation.

        For example:
        To configure AWS WAF to allow, block, or count requests that originated from the IP address 192.0.2.44, specify 192.0.2.44/32 .
        To configure AWS WAF to allow, block, or count requests that originated from IP addresses from 192.0.2.0 to 192.0.2.255, specify 192.0.2.0/24 .

        For more information about CIDR notation, see the Wikipedia entry Classless Inter-Domain Routing .

        Specify an IPv6 address by using CIDR notation. For example:
        To configure AWS WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify 1111:0000:0000:0000:0000:0000:0000:0111/128 .
        To configure AWS WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify 1111:0000:0000:0000:0000:0000:0000:0000/64 .

        :stability: experimental
        '''
        result = self._values.get("cidr_ranges")
        assert result is not None, "Required property 'cidr_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cidr_type(self) -> builtins.str:
        '''(experimental) Type of CIDR range.

        :stability: experimental
        '''
        result = self._values.get("cidr_type")
        assert result is not None, "Required property 'cidr_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CidrAllowList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.CloudFrontWebAclProps",
    jsii_struct_bases=[],
    name_mapping={"cidr_allow_list": "cidrAllowList", "managed_rules": "managedRules"},
)
class CloudFrontWebAclProps:
    def __init__(
        self,
        *,
        cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[str, typing.Any]]] = None,
        managed_rules: typing.Optional[typing.Sequence[typing.Union["ManagedRule", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties to configure the web acl.

        :param cidr_allow_list: (experimental) List of cidr ranges to allow. Default: - undefined
        :param managed_rules: (experimental) List of managed rules to apply to the web acl. Default: - [{ vendor: "AWS", name: "AWSManagedRulesCommonRuleSet" }]

        :stability: experimental
        '''
        if isinstance(cidr_allow_list, dict):
            cidr_allow_list = CidrAllowList(**cidr_allow_list)
        if __debug__:
            def stub(
                *,
                cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[str, typing.Any]]] = None,
                managed_rules: typing.Optional[typing.Sequence[typing.Union[ManagedRule, typing.Dict[str, typing.Any]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument cidr_allow_list", value=cidr_allow_list, expected_type=type_hints["cidr_allow_list"])
            check_type(argname="argument managed_rules", value=managed_rules, expected_type=type_hints["managed_rules"])
        self._values: typing.Dict[str, typing.Any] = {}
        if cidr_allow_list is not None:
            self._values["cidr_allow_list"] = cidr_allow_list
        if managed_rules is not None:
            self._values["managed_rules"] = managed_rules

    @builtins.property
    def cidr_allow_list(self) -> typing.Optional[CidrAllowList]:
        '''(experimental) List of cidr ranges to allow.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("cidr_allow_list")
        return typing.cast(typing.Optional[CidrAllowList], result)

    @builtins.property
    def managed_rules(self) -> typing.Optional[typing.List["ManagedRule"]]:
        '''(experimental) List of managed rules to apply to the web acl.

        :default: - [{ vendor: "AWS", name: "AWSManagedRulesCommonRuleSet" }]

        :stability: experimental
        '''
        result = self._values.get("managed_rules")
        return typing.cast(typing.Optional[typing.List["ManagedRule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFrontWebAclProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontWebAcl(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/static-website.CloudfrontWebAcl",
):
    '''(experimental) This construct creates a WAFv2 Web ACL for cloudfront in the us-east-1 region (required for cloudfront) no matter the region of the parent cdk stack.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[str, typing.Any]]] = None,
        managed_rules: typing.Optional[typing.Sequence[typing.Union["ManagedRule", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cidr_allow_list: (experimental) List of cidr ranges to allow. Default: - undefined
        :param managed_rules: (experimental) List of managed rules to apply to the web acl. Default: - [{ vendor: "AWS", name: "AWSManagedRulesCommonRuleSet" }]

        :stability: experimental
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                cidr_allow_list: typing.Optional[typing.Union[CidrAllowList, typing.Dict[str, typing.Any]]] = None,
                managed_rules: typing.Optional[typing.Sequence[typing.Union[ManagedRule, typing.Dict[str, typing.Any]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudFrontWebAclProps(
            cidr_allow_list=cidr_allow_list, managed_rules=managed_rules
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="webAclArn")
    def web_acl_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "webAclArn"))

    @builtins.property
    @jsii.member(jsii_name="webAclId")
    def web_acl_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "webAclId"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.ManagedRule",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "vendor": "vendor"},
)
class ManagedRule:
    def __init__(self, *, name: builtins.str, vendor: builtins.str) -> None:
        '''(experimental) Represents a WAF V2 managed rule.

        :param name: (experimental) The name of the managed rule group. You use this, along with the vendor name, to identify the rule group.
        :param vendor: (experimental) The name of the managed rule group vendor. You use this, along with the rule group name, to identify the rule group.

        :stability: experimental
        '''
        if __debug__:
            def stub(*, name: builtins.str, vendor: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vendor", value=vendor, expected_type=type_hints["vendor"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "vendor": vendor,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the managed rule group.

        You use this, along with the vendor name, to identify the rule group.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vendor(self) -> builtins.str:
        '''(experimental) The name of the managed rule group vendor.

        You use this, along with the rule group name, to identify the rule group.

        :stability: experimental
        '''
        result = self._values.get("vendor")
        assert result is not None, "Required property 'vendor' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.RuntimeOptions",
    jsii_struct_bases=[],
    name_mapping={"json_payload": "jsonPayload", "json_file_name": "jsonFileName"},
)
class RuntimeOptions:
    def __init__(
        self,
        *,
        json_payload: typing.Any,
        json_file_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Dynamic configuration which gets resolved only during deployment.

        :param json_payload: (experimental) Arbitrary JSON payload containing runtime values to deploy. Typically this contains resourceArns, etc which are only known at deploy time.
        :param json_file_name: (experimental) File name to store runtime configuration (jsonPayload). Must follow pattern: '*.json' Default: "runtime-config.json"

        :stability: experimental

        Example::

            // Will store a JSON file called runtime-config.json in the root of the StaticWebsite S3 bucket containing any
            // and all resolved values.
            const runtimeConfig = {jsonPayload: {bucketArn: s3Bucket.bucketArn}};
            new StaticWebsite(scope, 'StaticWebsite', {websiteContentPath: 'path/to/website', runtimeConfig});
        '''
        if __debug__:
            def stub(
                *,
                json_payload: typing.Any,
                json_file_name: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument json_payload", value=json_payload, expected_type=type_hints["json_payload"])
            check_type(argname="argument json_file_name", value=json_file_name, expected_type=type_hints["json_file_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "json_payload": json_payload,
        }
        if json_file_name is not None:
            self._values["json_file_name"] = json_file_name

    @builtins.property
    def json_payload(self) -> typing.Any:
        '''(experimental) Arbitrary JSON payload containing runtime values to deploy.

        Typically this contains resourceArns, etc which
        are only known at deploy time.

        :stability: experimental

        Example::

            { userPoolId: some.userPool.userPoolId, someResourceArn: some.resource.Arn }
        '''
        result = self._values.get("json_payload")
        assert result is not None, "Required property 'json_payload' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def json_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) File name to store runtime configuration (jsonPayload).

        Must follow pattern: '*.json'

        :default: "runtime-config.json"

        :stability: experimental
        '''
        result = self._values.get("json_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuntimeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StaticWebsite(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/static-website.StaticWebsite",
):
    '''(experimental) Deploys a Static Website using by default a private S3 bucket as an origin and Cloudfront as the entrypoint.

    This construct configures a webAcl containing rules that are generally applicable to web applications. This
    provides protection against exploitation of a wide range of vulnerabilities, including some of the high risk
    and commonly occurring vulnerabilities described in OWASP publications such as OWASP Top 10.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        website_content_path: builtins.str,
        default_website_bucket_encryption: typing.Optional[aws_cdk.aws_s3.BucketEncryption] = None,
        default_website_bucket_encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
        distribution_props: typing.Optional[typing.Union[aws_cdk.aws_cloudfront.DistributionProps, typing.Dict[str, typing.Any]]] = None,
        runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[str, typing.Any]]] = None,
        web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[str, typing.Any]]] = None,
        website_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param website_content_path: (experimental) Path to the directory containing the static website files and assets. This directory must contain an index.html file.
        :param default_website_bucket_encryption: (experimental) Bucket encryption to use for the default bucket. Supported options are KMS or S3MANAGED. Note: If planning to use KMS, ensure you associate a Lambda Edge function to sign requests to S3 as OAI does not currently support KMS encryption. Refer to {@link https://aws.amazon.com/blogs/networking-and-content-delivery/serving-sse-kms-encrypted-content-from-s3-using-cloudfront/} Default: - "S3MANAGED"
        :param default_website_bucket_encryption_key: (experimental) A predefined KMS customer encryption key to use for the default bucket that gets created. Note: This is only used if the websiteBucket is left undefined, otherwise all settings from the provided websiteBucket will be used.
        :param distribution_props: (experimental) Custom distribution properties. Note: defaultBehaviour.origin is a required parameter, however it will not be used as this construct will wire it on your behalf. You will need to pass in an instance of StaticWebsiteOrigin (NoOp) to keep the compiler happy.
        :param runtime_options: (experimental) Dynamic configuration which gets resolved only during deployment.
        :param web_acl_props: (experimental) Limited configuration settings for the generated webAcl. For more advanced settings, create your own ACL and pass in the webAclId as a param to distributionProps. Note: If pass in your own ACL, make sure the SCOPE is CLOUDFRONT and it is created in us-east-1.
        :param website_bucket: (experimental) Predefined bucket to deploy the website into.

        :stability: experimental
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                website_content_path: builtins.str,
                default_website_bucket_encryption: typing.Optional[aws_cdk.aws_s3.BucketEncryption] = None,
                default_website_bucket_encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
                distribution_props: typing.Optional[typing.Union[aws_cdk.aws_cloudfront.DistributionProps, typing.Dict[str, typing.Any]]] = None,
                runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[str, typing.Any]]] = None,
                web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[str, typing.Any]]] = None,
                website_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StaticWebsiteProps(
            website_content_path=website_content_path,
            default_website_bucket_encryption=default_website_bucket_encryption,
            default_website_bucket_encryption_key=default_website_bucket_encryption_key,
            distribution_props=distribution_props,
            runtime_options=runtime_options,
            web_acl_props=web_acl_props,
            website_bucket=website_bucket,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucketDeployment")
    def bucket_deployment(self) -> aws_cdk.aws_s3_deployment.BucketDeployment:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3_deployment.BucketDeployment, jsii.get(self, "bucketDeployment"))

    @builtins.property
    @jsii.member(jsii_name="cloudFrontDistribution")
    def cloud_front_distribution(self) -> aws_cdk.aws_cloudfront.Distribution:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_cloudfront.Distribution, jsii.get(self, "cloudFrontDistribution"))

    @builtins.property
    @jsii.member(jsii_name="websiteBucket")
    def website_bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.IBucket, jsii.get(self, "websiteBucket"))


@jsii.implements(aws_cdk.aws_cloudfront.IOrigin)
class StaticWebsiteOrigin(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/static-website.StaticWebsiteOrigin",
):
    '''(experimental) If passing in distributionProps, the default behaviour.origin is a required parameter. An instance of this class can be passed in to make the compiler happy.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.Construct,
        *,
        origin_id: builtins.str,
    ) -> aws_cdk.aws_cloudfront.OriginBindConfig:
        '''(experimental) The method called when a given Origin is added (for the first time) to a Distribution.

        :param _scope: -
        :param origin_id: The identifier of this Origin, as assigned by the Distribution this Origin has been used added to.

        :stability: experimental
        '''
        if __debug__:
            def stub(_scope: constructs.Construct, *, origin_id: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        _options = aws_cdk.aws_cloudfront.OriginBindOptions(origin_id=origin_id)

        return typing.cast(aws_cdk.aws_cloudfront.OriginBindConfig, jsii.invoke(self, "bind", [_scope, _options]))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/static-website.StaticWebsiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "website_content_path": "websiteContentPath",
        "default_website_bucket_encryption": "defaultWebsiteBucketEncryption",
        "default_website_bucket_encryption_key": "defaultWebsiteBucketEncryptionKey",
        "distribution_props": "distributionProps",
        "runtime_options": "runtimeOptions",
        "web_acl_props": "webAclProps",
        "website_bucket": "websiteBucket",
    },
)
class StaticWebsiteProps:
    def __init__(
        self,
        *,
        website_content_path: builtins.str,
        default_website_bucket_encryption: typing.Optional[aws_cdk.aws_s3.BucketEncryption] = None,
        default_website_bucket_encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
        distribution_props: typing.Optional[typing.Union[aws_cdk.aws_cloudfront.DistributionProps, typing.Dict[str, typing.Any]]] = None,
        runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[str, typing.Any]]] = None,
        web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[str, typing.Any]]] = None,
        website_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
    ) -> None:
        '''(experimental) Properties for configuring the StaticWebsite.

        :param website_content_path: (experimental) Path to the directory containing the static website files and assets. This directory must contain an index.html file.
        :param default_website_bucket_encryption: (experimental) Bucket encryption to use for the default bucket. Supported options are KMS or S3MANAGED. Note: If planning to use KMS, ensure you associate a Lambda Edge function to sign requests to S3 as OAI does not currently support KMS encryption. Refer to {@link https://aws.amazon.com/blogs/networking-and-content-delivery/serving-sse-kms-encrypted-content-from-s3-using-cloudfront/} Default: - "S3MANAGED"
        :param default_website_bucket_encryption_key: (experimental) A predefined KMS customer encryption key to use for the default bucket that gets created. Note: This is only used if the websiteBucket is left undefined, otherwise all settings from the provided websiteBucket will be used.
        :param distribution_props: (experimental) Custom distribution properties. Note: defaultBehaviour.origin is a required parameter, however it will not be used as this construct will wire it on your behalf. You will need to pass in an instance of StaticWebsiteOrigin (NoOp) to keep the compiler happy.
        :param runtime_options: (experimental) Dynamic configuration which gets resolved only during deployment.
        :param web_acl_props: (experimental) Limited configuration settings for the generated webAcl. For more advanced settings, create your own ACL and pass in the webAclId as a param to distributionProps. Note: If pass in your own ACL, make sure the SCOPE is CLOUDFRONT and it is created in us-east-1.
        :param website_bucket: (experimental) Predefined bucket to deploy the website into.

        :stability: experimental
        '''
        if isinstance(distribution_props, dict):
            distribution_props = aws_cdk.aws_cloudfront.DistributionProps(**distribution_props)
        if isinstance(runtime_options, dict):
            runtime_options = RuntimeOptions(**runtime_options)
        if isinstance(web_acl_props, dict):
            web_acl_props = CloudFrontWebAclProps(**web_acl_props)
        if __debug__:
            def stub(
                *,
                website_content_path: builtins.str,
                default_website_bucket_encryption: typing.Optional[aws_cdk.aws_s3.BucketEncryption] = None,
                default_website_bucket_encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
                distribution_props: typing.Optional[typing.Union[aws_cdk.aws_cloudfront.DistributionProps, typing.Dict[str, typing.Any]]] = None,
                runtime_options: typing.Optional[typing.Union[RuntimeOptions, typing.Dict[str, typing.Any]]] = None,
                web_acl_props: typing.Optional[typing.Union[CloudFrontWebAclProps, typing.Dict[str, typing.Any]]] = None,
                website_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument website_content_path", value=website_content_path, expected_type=type_hints["website_content_path"])
            check_type(argname="argument default_website_bucket_encryption", value=default_website_bucket_encryption, expected_type=type_hints["default_website_bucket_encryption"])
            check_type(argname="argument default_website_bucket_encryption_key", value=default_website_bucket_encryption_key, expected_type=type_hints["default_website_bucket_encryption_key"])
            check_type(argname="argument distribution_props", value=distribution_props, expected_type=type_hints["distribution_props"])
            check_type(argname="argument runtime_options", value=runtime_options, expected_type=type_hints["runtime_options"])
            check_type(argname="argument web_acl_props", value=web_acl_props, expected_type=type_hints["web_acl_props"])
            check_type(argname="argument website_bucket", value=website_bucket, expected_type=type_hints["website_bucket"])
        self._values: typing.Dict[str, typing.Any] = {
            "website_content_path": website_content_path,
        }
        if default_website_bucket_encryption is not None:
            self._values["default_website_bucket_encryption"] = default_website_bucket_encryption
        if default_website_bucket_encryption_key is not None:
            self._values["default_website_bucket_encryption_key"] = default_website_bucket_encryption_key
        if distribution_props is not None:
            self._values["distribution_props"] = distribution_props
        if runtime_options is not None:
            self._values["runtime_options"] = runtime_options
        if web_acl_props is not None:
            self._values["web_acl_props"] = web_acl_props
        if website_bucket is not None:
            self._values["website_bucket"] = website_bucket

    @builtins.property
    def website_content_path(self) -> builtins.str:
        '''(experimental) Path to the directory containing the static website files and assets.

        This directory must contain an index.html file.

        :stability: experimental
        '''
        result = self._values.get("website_content_path")
        assert result is not None, "Required property 'website_content_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_website_bucket_encryption(
        self,
    ) -> typing.Optional[aws_cdk.aws_s3.BucketEncryption]:
        '''(experimental) Bucket encryption to use for the default bucket.

        Supported options are KMS or S3MANAGED.

        Note: If planning to use KMS, ensure you associate a Lambda Edge function to sign requests to S3 as OAI does not currently support KMS encryption. Refer to {@link https://aws.amazon.com/blogs/networking-and-content-delivery/serving-sse-kms-encrypted-content-from-s3-using-cloudfront/}

        :default: - "S3MANAGED"

        :stability: experimental
        '''
        result = self._values.get("default_website_bucket_encryption")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketEncryption], result)

    @builtins.property
    def default_website_bucket_encryption_key(
        self,
    ) -> typing.Optional[aws_cdk.aws_kms.Key]:
        '''(experimental) A predefined KMS customer encryption key to use for the default bucket that gets created.

        Note: This is only used if the websiteBucket is left undefined, otherwise all settings from the provided websiteBucket will be used.

        :stability: experimental
        '''
        result = self._values.get("default_website_bucket_encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.Key], result)

    @builtins.property
    def distribution_props(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudfront.DistributionProps]:
        '''(experimental) Custom distribution properties.

        Note: defaultBehaviour.origin is a required parameter, however it will not be used as this construct will wire it on your behalf.
        You will need to pass in an instance of StaticWebsiteOrigin (NoOp) to keep the compiler happy.

        :stability: experimental
        '''
        result = self._values.get("distribution_props")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.DistributionProps], result)

    @builtins.property
    def runtime_options(self) -> typing.Optional[RuntimeOptions]:
        '''(experimental) Dynamic configuration which gets resolved only during deployment.

        :stability: experimental
        '''
        result = self._values.get("runtime_options")
        return typing.cast(typing.Optional[RuntimeOptions], result)

    @builtins.property
    def web_acl_props(self) -> typing.Optional[CloudFrontWebAclProps]:
        '''(experimental) Limited configuration settings for the generated webAcl.

        For more advanced settings, create your own ACL and pass in the webAclId as a param to distributionProps.

        Note: If pass in your own ACL, make sure the SCOPE is CLOUDFRONT and it is created in us-east-1.

        :stability: experimental
        '''
        result = self._values.get("web_acl_props")
        return typing.cast(typing.Optional[CloudFrontWebAclProps], result)

    @builtins.property
    def website_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        '''(experimental) Predefined bucket to deploy the website into.

        :stability: experimental
        '''
        result = self._values.get("website_bucket")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.IBucket], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticWebsiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CidrAllowList",
    "CloudFrontWebAclProps",
    "CloudfrontWebAcl",
    "ManagedRule",
    "RuntimeOptions",
    "StaticWebsite",
    "StaticWebsiteOrigin",
    "StaticWebsiteProps",
]

publication.publish()
