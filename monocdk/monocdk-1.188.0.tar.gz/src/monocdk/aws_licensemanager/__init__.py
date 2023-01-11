'''
# AWS::LicenseManager Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as licensemanager
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for LicenseManager construct libraries](https://constructs.dev/search?q=licensemanager)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::LicenseManager resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LicenseManager.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::LicenseManager](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LicenseManager.html).

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
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnGrant(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_licensemanager.CfnGrant",
):
    '''A CloudFormation ``AWS::LicenseManager::Grant``.

    Specifies a grant.

    A grant shares the use of license entitlements with specific AWS accounts . For more information, see `Granted licenses <https://docs.aws.amazon.com/license-manager/latest/userguide/granted-licenses.html>`_ in the *AWS License Manager User Guide* .

    :cloudformationResource: AWS::LicenseManager::Grant
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_licensemanager as licensemanager
        
        cfn_grant = licensemanager.CfnGrant(self, "MyCfnGrant",
            allowed_operations=["allowedOperations"],
            grant_name="grantName",
            home_region="homeRegion",
            license_arn="licenseArn",
            principals=["principals"],
            status="status"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        allowed_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
        grant_name: typing.Optional[builtins.str] = None,
        home_region: typing.Optional[builtins.str] = None,
        license_arn: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::LicenseManager::Grant``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param allowed_operations: Allowed operations for the grant.
        :param grant_name: Grant name.
        :param home_region: Home Region of the grant.
        :param license_arn: License ARN.
        :param principals: The grant principals. You can specify one of the following as an Amazon Resource Name (ARN):. - An AWS account, which includes only the account specified. - An organizational unit (OU), which includes all accounts in the OU. - An organization, which will include all accounts across your organization.
        :param status: Granted license status.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd624642ce311f4fb39f245b80fa5bf613df4686d63602355f15f000d819fdc2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGrantProps(
            allowed_operations=allowed_operations,
            grant_name=grant_name,
            home_region=home_region,
            license_arn=license_arn,
            principals=principals,
            status=status,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57cba39a2e423a7163aaec7c837e95f222ffd038a0b16924c5fcd7a2a94f796f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b832c3211fe923bf8e229a0245a918f2bc7055a4a608d8e9ac06f3280427695)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrGrantArn")
    def attr_grant_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the grant.

        :cloudformationAttribute: GrantArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGrantArn"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The grant version.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="allowedOperations")
    def allowed_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Allowed operations for the grant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-allowedoperations
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOperations"))

    @allowed_operations.setter
    def allowed_operations(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3e6046c739c8a187e95494b18f2fe1b1c11aa4fee24cac533f3627ce2f08eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOperations", value)

    @builtins.property
    @jsii.member(jsii_name="grantName")
    def grant_name(self) -> typing.Optional[builtins.str]:
        '''Grant name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grantName"))

    @grant_name.setter
    def grant_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c55385e8dd1871739c070bccc975080a241b8ea33d6c8a63dc2c05eba00bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grantName", value)

    @builtins.property
    @jsii.member(jsii_name="homeRegion")
    def home_region(self) -> typing.Optional[builtins.str]:
        '''Home Region of the grant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-homeregion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homeRegion"))

    @home_region.setter
    def home_region(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee670a4b44ef75de6b1bd5c93123c1c3c9dfc939bd41274823e50deee3289e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homeRegion", value)

    @builtins.property
    @jsii.member(jsii_name="licenseArn")
    def license_arn(self) -> typing.Optional[builtins.str]:
        '''License ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-licensearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseArn"))

    @license_arn.setter
    def license_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139af3699211da54a604eba0acab66c57336f1f82bd1c75599b63ff1850c31e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseArn", value)

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The grant principals. You can specify one of the following as an Amazon Resource Name (ARN):.

        - An AWS account, which includes only the account specified.
        - An organizational unit (OU), which includes all accounts in the OU.
        - An organization, which will include all accounts across your organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-principals
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "principals"))

    @principals.setter
    def principals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6dd9f23c9f2a20dac079cff7c995a2e309484daea950f88c531220da61035c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''Granted license status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081a53a105fb0c457900616b378a8b78a9e195f227ddf8039010408bd40f7943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="monocdk.aws_licensemanager.CfnGrantProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_operations": "allowedOperations",
        "grant_name": "grantName",
        "home_region": "homeRegion",
        "license_arn": "licenseArn",
        "principals": "principals",
        "status": "status",
    },
)
class CfnGrantProps:
    def __init__(
        self,
        *,
        allowed_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
        grant_name: typing.Optional[builtins.str] = None,
        home_region: typing.Optional[builtins.str] = None,
        license_arn: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnGrant``.

        :param allowed_operations: Allowed operations for the grant.
        :param grant_name: Grant name.
        :param home_region: Home Region of the grant.
        :param license_arn: License ARN.
        :param principals: The grant principals. You can specify one of the following as an Amazon Resource Name (ARN):. - An AWS account, which includes only the account specified. - An organizational unit (OU), which includes all accounts in the OU. - An organization, which will include all accounts across your organization.
        :param status: Granted license status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_licensemanager as licensemanager
            
            cfn_grant_props = licensemanager.CfnGrantProps(
                allowed_operations=["allowedOperations"],
                grant_name="grantName",
                home_region="homeRegion",
                license_arn="licenseArn",
                principals=["principals"],
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5da90eb27f508549ec76bfe34cc740453e4eefea3546518a8ff33b03ee0e318)
            check_type(argname="argument allowed_operations", value=allowed_operations, expected_type=type_hints["allowed_operations"])
            check_type(argname="argument grant_name", value=grant_name, expected_type=type_hints["grant_name"])
            check_type(argname="argument home_region", value=home_region, expected_type=type_hints["home_region"])
            check_type(argname="argument license_arn", value=license_arn, expected_type=type_hints["license_arn"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_operations is not None:
            self._values["allowed_operations"] = allowed_operations
        if grant_name is not None:
            self._values["grant_name"] = grant_name
        if home_region is not None:
            self._values["home_region"] = home_region
        if license_arn is not None:
            self._values["license_arn"] = license_arn
        if principals is not None:
            self._values["principals"] = principals
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def allowed_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Allowed operations for the grant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-allowedoperations
        '''
        result = self._values.get("allowed_operations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def grant_name(self) -> typing.Optional[builtins.str]:
        '''Grant name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantname
        '''
        result = self._values.get("grant_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def home_region(self) -> typing.Optional[builtins.str]:
        '''Home Region of the grant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-homeregion
        '''
        result = self._values.get("home_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_arn(self) -> typing.Optional[builtins.str]:
        '''License ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-licensearn
        '''
        result = self._values.get("license_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The grant principals. You can specify one of the following as an Amazon Resource Name (ARN):.

        - An AWS account, which includes only the account specified.
        - An organizational unit (OU), which includes all accounts in the OU.
        - An organization, which will include all accounts across your organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-principals
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Granted license status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGrantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLicense(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_licensemanager.CfnLicense",
):
    '''A CloudFormation ``AWS::LicenseManager::License``.

    Specifies a granted license.

    Granted licenses are licenses for products that your organization purchased from AWS Marketplace or directly from a seller who integrated their software with managed entitlements. For more information, see `Granted licenses <https://docs.aws.amazon.com/license-manager/latest/userguide/granted-licenses.html>`_ in the *AWS License Manager User Guide* .

    :cloudformationResource: AWS::LicenseManager::License
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_licensemanager as licensemanager
        
        cfn_license = licensemanager.CfnLicense(self, "MyCfnLicense",
            consumption_configuration=licensemanager.CfnLicense.ConsumptionConfigurationProperty(
                borrow_configuration=licensemanager.CfnLicense.BorrowConfigurationProperty(
                    allow_early_check_in=False,
                    max_time_to_live_in_minutes=123
                ),
                provisional_configuration=licensemanager.CfnLicense.ProvisionalConfigurationProperty(
                    max_time_to_live_in_minutes=123
                ),
                renew_type="renewType"
            ),
            entitlements=[licensemanager.CfnLicense.EntitlementProperty(
                name="name",
                unit="unit",
        
                # the properties below are optional
                allow_check_in=False,
                max_count=123,
                overage=False,
                value="value"
            )],
            home_region="homeRegion",
            issuer=licensemanager.CfnLicense.IssuerDataProperty(
                name="name",
        
                # the properties below are optional
                sign_key="signKey"
            ),
            license_name="licenseName",
            product_name="productName",
            validity=licensemanager.CfnLicense.ValidityDateFormatProperty(
                begin="begin",
                end="end"
            ),
        
            # the properties below are optional
            beneficiary="beneficiary",
            license_metadata=[licensemanager.CfnLicense.MetadataProperty(
                name="name",
                value="value"
            )],
            product_sku="productSku",
            status="status"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        consumption_configuration: typing.Union[typing.Union["CfnLicense.ConsumptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        entitlements: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLicense.EntitlementProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        home_region: builtins.str,
        issuer: typing.Union[typing.Union["CfnLicense.IssuerDataProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        license_name: builtins.str,
        product_name: builtins.str,
        validity: typing.Union[typing.Union["CfnLicense.ValidityDateFormatProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        beneficiary: typing.Optional[builtins.str] = None,
        license_metadata: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLicense.MetadataProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        product_sku: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::LicenseManager::License``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param consumption_configuration: Configuration for consumption of the license.
        :param entitlements: License entitlements.
        :param home_region: Home Region of the license.
        :param issuer: License issuer.
        :param license_name: License name.
        :param product_name: Product name.
        :param validity: Date and time range during which the license is valid, in ISO8601-UTC format.
        :param beneficiary: License beneficiary.
        :param license_metadata: License metadata.
        :param product_sku: Product SKU.
        :param status: License status.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__393f9e9a5ba9e0b7d63370ad23c3f1c1fdb2f0633aafe31c8f33eb6753fbec95)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLicenseProps(
            consumption_configuration=consumption_configuration,
            entitlements=entitlements,
            home_region=home_region,
            issuer=issuer,
            license_name=license_name,
            product_name=product_name,
            validity=validity,
            beneficiary=beneficiary,
            license_metadata=license_metadata,
            product_sku=product_sku,
            status=status,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5077c18265273de5a0d22de6bf87a3f173202cdde8c4baccc223ecdebc0a92ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e092e7b09267a1de703b0b70cc1c85de19138d4fa56b8613e310f81fe204793d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLicenseArn")
    def attr_license_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the license.

        :cloudformationAttribute: LicenseArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLicenseArn"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The license version.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="consumptionConfiguration")
    def consumption_configuration(
        self,
    ) -> typing.Union["CfnLicense.ConsumptionConfigurationProperty", _IResolvable_a771d0ef]:
        '''Configuration for consumption of the license.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-consumptionconfiguration
        '''
        return typing.cast(typing.Union["CfnLicense.ConsumptionConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "consumptionConfiguration"))

    @consumption_configuration.setter
    def consumption_configuration(
        self,
        value: typing.Union["CfnLicense.ConsumptionConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e58336cbaf82c3d438d3d1cffb7043d0ef78ed901d57e6b71607d75a04bd5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumptionConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="entitlements")
    def entitlements(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLicense.EntitlementProperty", _IResolvable_a771d0ef]]]:
        '''License entitlements.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-entitlements
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLicense.EntitlementProperty", _IResolvable_a771d0ef]]], jsii.get(self, "entitlements"))

    @entitlements.setter
    def entitlements(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLicense.EntitlementProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bca8ed084b1ba027ef4c948e1c0c3bd7245530aa8e07ca1a106bcc209ca38a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entitlements", value)

    @builtins.property
    @jsii.member(jsii_name="homeRegion")
    def home_region(self) -> builtins.str:
        '''Home Region of the license.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-homeregion
        '''
        return typing.cast(builtins.str, jsii.get(self, "homeRegion"))

    @home_region.setter
    def home_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c286ce7f74d65142cf153861bd47c086f0aedafee14549c595f229b93ebd3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homeRegion", value)

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(
        self,
    ) -> typing.Union["CfnLicense.IssuerDataProperty", _IResolvable_a771d0ef]:
        '''License issuer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-issuer
        '''
        return typing.cast(typing.Union["CfnLicense.IssuerDataProperty", _IResolvable_a771d0ef], jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(
        self,
        value: typing.Union["CfnLicense.IssuerDataProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055792b7e93ccbc475210b840caca28a5c9357322dddd13b4308031ce203c7d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value)

    @builtins.property
    @jsii.member(jsii_name="licenseName")
    def license_name(self) -> builtins.str:
        '''License name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensename
        '''
        return typing.cast(builtins.str, jsii.get(self, "licenseName"))

    @license_name.setter
    def license_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585ba2445b79e2e25f776e347a0acc6dbe38a6fc535589ddeacbcd934c091bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseName", value)

    @builtins.property
    @jsii.member(jsii_name="productName")
    def product_name(self) -> builtins.str:
        '''Product name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productname
        '''
        return typing.cast(builtins.str, jsii.get(self, "productName"))

    @product_name.setter
    def product_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f9b27f4732af10ea97636a0fad50e3657c50e9a26a0fae226c23abf1232a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productName", value)

    @builtins.property
    @jsii.member(jsii_name="validity")
    def validity(
        self,
    ) -> typing.Union["CfnLicense.ValidityDateFormatProperty", _IResolvable_a771d0ef]:
        '''Date and time range during which the license is valid, in ISO8601-UTC format.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-validity
        '''
        return typing.cast(typing.Union["CfnLicense.ValidityDateFormatProperty", _IResolvable_a771d0ef], jsii.get(self, "validity"))

    @validity.setter
    def validity(
        self,
        value: typing.Union["CfnLicense.ValidityDateFormatProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f9f76df056f49e5b1e842fc41b063af0eae64a2dac5d73f20629388c70cd85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validity", value)

    @builtins.property
    @jsii.member(jsii_name="beneficiary")
    def beneficiary(self) -> typing.Optional[builtins.str]:
        '''License beneficiary.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-beneficiary
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "beneficiary"))

    @beneficiary.setter
    def beneficiary(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63eff1b31b9bd318f2003ea79b6c963b0fedeae46bcdcda8bae7498a50721253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beneficiary", value)

    @builtins.property
    @jsii.member(jsii_name="licenseMetadata")
    def license_metadata(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLicense.MetadataProperty", _IResolvable_a771d0ef]]]]:
        '''License metadata.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensemetadata
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLicense.MetadataProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "licenseMetadata"))

    @license_metadata.setter
    def license_metadata(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLicense.MetadataProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98338e739372e84155794b73f5df167dad9dc577e1d8ae51f0753dfcfcd4d1cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseMetadata", value)

    @builtins.property
    @jsii.member(jsii_name="productSku")
    def product_sku(self) -> typing.Optional[builtins.str]:
        '''Product SKU.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productsku
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productSku"))

    @product_sku.setter
    def product_sku(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6723664b4908ab7d98be8f5722d0d77ba703a69037a0eb855e152fbbd4fe5213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productSku", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''License status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa5e25090cc369a5375d4d322d772d9c7f6734b5d3dee889e31b140851db69f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_licensemanager.CfnLicense.BorrowConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_early_check_in": "allowEarlyCheckIn",
            "max_time_to_live_in_minutes": "maxTimeToLiveInMinutes",
        },
    )
    class BorrowConfigurationProperty:
        def __init__(
            self,
            *,
            allow_early_check_in: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            max_time_to_live_in_minutes: jsii.Number,
        ) -> None:
            '''Details about a borrow configuration.

            :param allow_early_check_in: Indicates whether early check-ins are allowed.
            :param max_time_to_live_in_minutes: Maximum time for the borrow configuration, in minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-borrowconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_licensemanager as licensemanager
                
                borrow_configuration_property = licensemanager.CfnLicense.BorrowConfigurationProperty(
                    allow_early_check_in=False,
                    max_time_to_live_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a47b43d757f363290102ff6e8457eebd5a907717675db855bcca3ffc2f5cd697)
                check_type(argname="argument allow_early_check_in", value=allow_early_check_in, expected_type=type_hints["allow_early_check_in"])
                check_type(argname="argument max_time_to_live_in_minutes", value=max_time_to_live_in_minutes, expected_type=type_hints["max_time_to_live_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "allow_early_check_in": allow_early_check_in,
                "max_time_to_live_in_minutes": max_time_to_live_in_minutes,
            }

        @builtins.property
        def allow_early_check_in(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Indicates whether early check-ins are allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-borrowconfiguration.html#cfn-licensemanager-license-borrowconfiguration-allowearlycheckin
            '''
            result = self._values.get("allow_early_check_in")
            assert result is not None, "Required property 'allow_early_check_in' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def max_time_to_live_in_minutes(self) -> jsii.Number:
            '''Maximum time for the borrow configuration, in minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-borrowconfiguration.html#cfn-licensemanager-license-borrowconfiguration-maxtimetoliveinminutes
            '''
            result = self._values.get("max_time_to_live_in_minutes")
            assert result is not None, "Required property 'max_time_to_live_in_minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BorrowConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_licensemanager.CfnLicense.ConsumptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "borrow_configuration": "borrowConfiguration",
            "provisional_configuration": "provisionalConfiguration",
            "renew_type": "renewType",
        },
    )
    class ConsumptionConfigurationProperty:
        def __init__(
            self,
            *,
            borrow_configuration: typing.Optional[typing.Union[typing.Union["CfnLicense.BorrowConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            provisional_configuration: typing.Optional[typing.Union[typing.Union["CfnLicense.ProvisionalConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            renew_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details about a consumption configuration.

            :param borrow_configuration: Details about a borrow configuration.
            :param provisional_configuration: Details about a provisional configuration.
            :param renew_type: Renewal frequency.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_licensemanager as licensemanager
                
                consumption_configuration_property = licensemanager.CfnLicense.ConsumptionConfigurationProperty(
                    borrow_configuration=licensemanager.CfnLicense.BorrowConfigurationProperty(
                        allow_early_check_in=False,
                        max_time_to_live_in_minutes=123
                    ),
                    provisional_configuration=licensemanager.CfnLicense.ProvisionalConfigurationProperty(
                        max_time_to_live_in_minutes=123
                    ),
                    renew_type="renewType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0708081d2cd749918b6523bef5426616ef71732b91dd3387f0ffafe4612f2668)
                check_type(argname="argument borrow_configuration", value=borrow_configuration, expected_type=type_hints["borrow_configuration"])
                check_type(argname="argument provisional_configuration", value=provisional_configuration, expected_type=type_hints["provisional_configuration"])
                check_type(argname="argument renew_type", value=renew_type, expected_type=type_hints["renew_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if borrow_configuration is not None:
                self._values["borrow_configuration"] = borrow_configuration
            if provisional_configuration is not None:
                self._values["provisional_configuration"] = provisional_configuration
            if renew_type is not None:
                self._values["renew_type"] = renew_type

        @builtins.property
        def borrow_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnLicense.BorrowConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Details about a borrow configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html#cfn-licensemanager-license-consumptionconfiguration-borrowconfiguration
            '''
            result = self._values.get("borrow_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnLicense.BorrowConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def provisional_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnLicense.ProvisionalConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Details about a provisional configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html#cfn-licensemanager-license-consumptionconfiguration-provisionalconfiguration
            '''
            result = self._values.get("provisional_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnLicense.ProvisionalConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def renew_type(self) -> typing.Optional[builtins.str]:
            '''Renewal frequency.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html#cfn-licensemanager-license-consumptionconfiguration-renewtype
            '''
            result = self._values.get("renew_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConsumptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_licensemanager.CfnLicense.EntitlementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "unit": "unit",
            "allow_check_in": "allowCheckIn",
            "max_count": "maxCount",
            "overage": "overage",
            "value": "value",
        },
    )
    class EntitlementProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            unit: builtins.str,
            allow_check_in: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            max_count: typing.Optional[jsii.Number] = None,
            overage: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a resource entitled for use with a license.

            :param name: Entitlement name.
            :param unit: Entitlement unit.
            :param allow_check_in: Indicates whether check-ins are allowed.
            :param max_count: Maximum entitlement count. Use if the unit is not None.
            :param overage: Indicates whether overages are allowed.
            :param value: Entitlement resource. Use only if the unit is None.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_licensemanager as licensemanager
                
                entitlement_property = licensemanager.CfnLicense.EntitlementProperty(
                    name="name",
                    unit="unit",
                
                    # the properties below are optional
                    allow_check_in=False,
                    max_count=123,
                    overage=False,
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb7d744e6f850d943b6e5ab370aee711330a1fae649173adec0f7a315bef410e)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument allow_check_in", value=allow_check_in, expected_type=type_hints["allow_check_in"])
                check_type(argname="argument max_count", value=max_count, expected_type=type_hints["max_count"])
                check_type(argname="argument overage", value=overage, expected_type=type_hints["overage"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "unit": unit,
            }
            if allow_check_in is not None:
                self._values["allow_check_in"] = allow_check_in
            if max_count is not None:
                self._values["max_count"] = max_count
            if overage is not None:
                self._values["overage"] = overage
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> builtins.str:
            '''Entitlement name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def unit(self) -> builtins.str:
            '''Entitlement unit.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-unit
            '''
            result = self._values.get("unit")
            assert result is not None, "Required property 'unit' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allow_check_in(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether check-ins are allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-allowcheckin
            '''
            result = self._values.get("allow_check_in")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def max_count(self) -> typing.Optional[jsii.Number]:
            '''Maximum entitlement count.

            Use if the unit is not None.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-maxcount
            '''
            result = self._values.get("max_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def overage(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Indicates whether overages are allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-overage
            '''
            result = self._values.get("overage")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Entitlement resource.

            Use only if the unit is None.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntitlementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_licensemanager.CfnLicense.IssuerDataProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "sign_key": "signKey"},
    )
    class IssuerDataProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            sign_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details associated with the issuer of a license.

            :param name: Issuer name.
            :param sign_key: Asymmetric KMS key from AWS Key Management Service . The KMS key must have a key usage of sign and verify, and support the RSASSA-PSS SHA-256 signing algorithm.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-issuerdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_licensemanager as licensemanager
                
                issuer_data_property = licensemanager.CfnLicense.IssuerDataProperty(
                    name="name",
                
                    # the properties below are optional
                    sign_key="signKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e6f6d2cd6327c2869e7ddd43643146d61adbffbca1556e7eab53567a81289bb)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument sign_key", value=sign_key, expected_type=type_hints["sign_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if sign_key is not None:
                self._values["sign_key"] = sign_key

        @builtins.property
        def name(self) -> builtins.str:
            '''Issuer name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-issuerdata.html#cfn-licensemanager-license-issuerdata-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sign_key(self) -> typing.Optional[builtins.str]:
            '''Asymmetric KMS key from AWS Key Management Service .

            The KMS key must have a key usage of sign and verify, and support the RSASSA-PSS SHA-256 signing algorithm.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-issuerdata.html#cfn-licensemanager-license-issuerdata-signkey
            '''
            result = self._values.get("sign_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IssuerDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_licensemanager.CfnLicense.MetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class MetadataProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''Describes key/value pairs.

            :param name: The key name.
            :param value: The value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-metadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_licensemanager as licensemanager
                
                metadata_property = licensemanager.CfnLicense.MetadataProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6f5b1b387bf41d3e9a94d2f3ce744d67ab0f22281cfb662be1638ebfbb9ad7d)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The key name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-metadata.html#cfn-licensemanager-license-metadata-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-metadata.html#cfn-licensemanager-license-metadata-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_licensemanager.CfnLicense.ProvisionalConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"max_time_to_live_in_minutes": "maxTimeToLiveInMinutes"},
    )
    class ProvisionalConfigurationProperty:
        def __init__(self, *, max_time_to_live_in_minutes: jsii.Number) -> None:
            '''Details about a provisional configuration.

            :param max_time_to_live_in_minutes: Maximum time for the provisional configuration, in minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-provisionalconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_licensemanager as licensemanager
                
                provisional_configuration_property = licensemanager.CfnLicense.ProvisionalConfigurationProperty(
                    max_time_to_live_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae85a048710f64199822692c8a37ebb1b996ddf875dafadaeb0e2dd031ba2e0d)
                check_type(argname="argument max_time_to_live_in_minutes", value=max_time_to_live_in_minutes, expected_type=type_hints["max_time_to_live_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "max_time_to_live_in_minutes": max_time_to_live_in_minutes,
            }

        @builtins.property
        def max_time_to_live_in_minutes(self) -> jsii.Number:
            '''Maximum time for the provisional configuration, in minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-provisionalconfiguration.html#cfn-licensemanager-license-provisionalconfiguration-maxtimetoliveinminutes
            '''
            result = self._values.get("max_time_to_live_in_minutes")
            assert result is not None, "Required property 'max_time_to_live_in_minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionalConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_licensemanager.CfnLicense.ValidityDateFormatProperty",
        jsii_struct_bases=[],
        name_mapping={"begin": "begin", "end": "end"},
    )
    class ValidityDateFormatProperty:
        def __init__(self, *, begin: builtins.str, end: builtins.str) -> None:
            '''Date and time range during which the license is valid, in ISO8601-UTC format.

            :param begin: Start of the time range.
            :param end: End of the time range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-validitydateformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_licensemanager as licensemanager
                
                validity_date_format_property = licensemanager.CfnLicense.ValidityDateFormatProperty(
                    begin="begin",
                    end="end"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__386681857f3e29bece1ac555de759e14c46ca4cbde614efaa5d6467d58d3dd27)
                check_type(argname="argument begin", value=begin, expected_type=type_hints["begin"])
                check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "begin": begin,
                "end": end,
            }

        @builtins.property
        def begin(self) -> builtins.str:
            '''Start of the time range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-validitydateformat.html#cfn-licensemanager-license-validitydateformat-begin
            '''
            result = self._values.get("begin")
            assert result is not None, "Required property 'begin' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def end(self) -> builtins.str:
            '''End of the time range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-validitydateformat.html#cfn-licensemanager-license-validitydateformat-end
            '''
            result = self._values.get("end")
            assert result is not None, "Required property 'end' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidityDateFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_licensemanager.CfnLicenseProps",
    jsii_struct_bases=[],
    name_mapping={
        "consumption_configuration": "consumptionConfiguration",
        "entitlements": "entitlements",
        "home_region": "homeRegion",
        "issuer": "issuer",
        "license_name": "licenseName",
        "product_name": "productName",
        "validity": "validity",
        "beneficiary": "beneficiary",
        "license_metadata": "licenseMetadata",
        "product_sku": "productSku",
        "status": "status",
    },
)
class CfnLicenseProps:
    def __init__(
        self,
        *,
        consumption_configuration: typing.Union[typing.Union[CfnLicense.ConsumptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        entitlements: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLicense.EntitlementProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        home_region: builtins.str,
        issuer: typing.Union[typing.Union[CfnLicense.IssuerDataProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        license_name: builtins.str,
        product_name: builtins.str,
        validity: typing.Union[typing.Union[CfnLicense.ValidityDateFormatProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        beneficiary: typing.Optional[builtins.str] = None,
        license_metadata: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLicense.MetadataProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        product_sku: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLicense``.

        :param consumption_configuration: Configuration for consumption of the license.
        :param entitlements: License entitlements.
        :param home_region: Home Region of the license.
        :param issuer: License issuer.
        :param license_name: License name.
        :param product_name: Product name.
        :param validity: Date and time range during which the license is valid, in ISO8601-UTC format.
        :param beneficiary: License beneficiary.
        :param license_metadata: License metadata.
        :param product_sku: Product SKU.
        :param status: License status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_licensemanager as licensemanager
            
            cfn_license_props = licensemanager.CfnLicenseProps(
                consumption_configuration=licensemanager.CfnLicense.ConsumptionConfigurationProperty(
                    borrow_configuration=licensemanager.CfnLicense.BorrowConfigurationProperty(
                        allow_early_check_in=False,
                        max_time_to_live_in_minutes=123
                    ),
                    provisional_configuration=licensemanager.CfnLicense.ProvisionalConfigurationProperty(
                        max_time_to_live_in_minutes=123
                    ),
                    renew_type="renewType"
                ),
                entitlements=[licensemanager.CfnLicense.EntitlementProperty(
                    name="name",
                    unit="unit",
            
                    # the properties below are optional
                    allow_check_in=False,
                    max_count=123,
                    overage=False,
                    value="value"
                )],
                home_region="homeRegion",
                issuer=licensemanager.CfnLicense.IssuerDataProperty(
                    name="name",
            
                    # the properties below are optional
                    sign_key="signKey"
                ),
                license_name="licenseName",
                product_name="productName",
                validity=licensemanager.CfnLicense.ValidityDateFormatProperty(
                    begin="begin",
                    end="end"
                ),
            
                # the properties below are optional
                beneficiary="beneficiary",
                license_metadata=[licensemanager.CfnLicense.MetadataProperty(
                    name="name",
                    value="value"
                )],
                product_sku="productSku",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d4716d0616f67cb562264f161dd90c1e8acd67b0dec5602216b296d7258748)
            check_type(argname="argument consumption_configuration", value=consumption_configuration, expected_type=type_hints["consumption_configuration"])
            check_type(argname="argument entitlements", value=entitlements, expected_type=type_hints["entitlements"])
            check_type(argname="argument home_region", value=home_region, expected_type=type_hints["home_region"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument license_name", value=license_name, expected_type=type_hints["license_name"])
            check_type(argname="argument product_name", value=product_name, expected_type=type_hints["product_name"])
            check_type(argname="argument validity", value=validity, expected_type=type_hints["validity"])
            check_type(argname="argument beneficiary", value=beneficiary, expected_type=type_hints["beneficiary"])
            check_type(argname="argument license_metadata", value=license_metadata, expected_type=type_hints["license_metadata"])
            check_type(argname="argument product_sku", value=product_sku, expected_type=type_hints["product_sku"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumption_configuration": consumption_configuration,
            "entitlements": entitlements,
            "home_region": home_region,
            "issuer": issuer,
            "license_name": license_name,
            "product_name": product_name,
            "validity": validity,
        }
        if beneficiary is not None:
            self._values["beneficiary"] = beneficiary
        if license_metadata is not None:
            self._values["license_metadata"] = license_metadata
        if product_sku is not None:
            self._values["product_sku"] = product_sku
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def consumption_configuration(
        self,
    ) -> typing.Union[CfnLicense.ConsumptionConfigurationProperty, _IResolvable_a771d0ef]:
        '''Configuration for consumption of the license.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-consumptionconfiguration
        '''
        result = self._values.get("consumption_configuration")
        assert result is not None, "Required property 'consumption_configuration' is missing"
        return typing.cast(typing.Union[CfnLicense.ConsumptionConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def entitlements(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLicense.EntitlementProperty, _IResolvable_a771d0ef]]]:
        '''License entitlements.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-entitlements
        '''
        result = self._values.get("entitlements")
        assert result is not None, "Required property 'entitlements' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLicense.EntitlementProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def home_region(self) -> builtins.str:
        '''Home Region of the license.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-homeregion
        '''
        result = self._values.get("home_region")
        assert result is not None, "Required property 'home_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer(
        self,
    ) -> typing.Union[CfnLicense.IssuerDataProperty, _IResolvable_a771d0ef]:
        '''License issuer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-issuer
        '''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(typing.Union[CfnLicense.IssuerDataProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def license_name(self) -> builtins.str:
        '''License name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensename
        '''
        result = self._values.get("license_name")
        assert result is not None, "Required property 'license_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_name(self) -> builtins.str:
        '''Product name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productname
        '''
        result = self._values.get("product_name")
        assert result is not None, "Required property 'product_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def validity(
        self,
    ) -> typing.Union[CfnLicense.ValidityDateFormatProperty, _IResolvable_a771d0ef]:
        '''Date and time range during which the license is valid, in ISO8601-UTC format.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-validity
        '''
        result = self._values.get("validity")
        assert result is not None, "Required property 'validity' is missing"
        return typing.cast(typing.Union[CfnLicense.ValidityDateFormatProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def beneficiary(self) -> typing.Optional[builtins.str]:
        '''License beneficiary.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-beneficiary
        '''
        result = self._values.get("beneficiary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_metadata(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLicense.MetadataProperty, _IResolvable_a771d0ef]]]]:
        '''License metadata.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensemetadata
        '''
        result = self._values.get("license_metadata")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLicense.MetadataProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def product_sku(self) -> typing.Optional[builtins.str]:
        '''Product SKU.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productsku
        '''
        result = self._values.get("product_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''License status.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLicenseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnGrant",
    "CfnGrantProps",
    "CfnLicense",
    "CfnLicenseProps",
]

publication.publish()

def _typecheckingstub__cd624642ce311f4fb39f245b80fa5bf613df4686d63602355f15f000d819fdc2(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    allowed_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
    grant_name: typing.Optional[builtins.str] = None,
    home_region: typing.Optional[builtins.str] = None,
    license_arn: typing.Optional[builtins.str] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cba39a2e423a7163aaec7c837e95f222ffd038a0b16924c5fcd7a2a94f796f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b832c3211fe923bf8e229a0245a918f2bc7055a4a608d8e9ac06f3280427695(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3e6046c739c8a187e95494b18f2fe1b1c11aa4fee24cac533f3627ce2f08eb(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c55385e8dd1871739c070bccc975080a241b8ea33d6c8a63dc2c05eba00bfb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee670a4b44ef75de6b1bd5c93123c1c3c9dfc939bd41274823e50deee3289e2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139af3699211da54a604eba0acab66c57336f1f82bd1c75599b63ff1850c31e4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6dd9f23c9f2a20dac079cff7c995a2e309484daea950f88c531220da61035c(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081a53a105fb0c457900616b378a8b78a9e195f227ddf8039010408bd40f7943(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5da90eb27f508549ec76bfe34cc740453e4eefea3546518a8ff33b03ee0e318(
    *,
    allowed_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
    grant_name: typing.Optional[builtins.str] = None,
    home_region: typing.Optional[builtins.str] = None,
    license_arn: typing.Optional[builtins.str] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393f9e9a5ba9e0b7d63370ad23c3f1c1fdb2f0633aafe31c8f33eb6753fbec95(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    consumption_configuration: typing.Union[typing.Union[CfnLicense.ConsumptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    entitlements: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLicense.EntitlementProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    home_region: builtins.str,
    issuer: typing.Union[typing.Union[CfnLicense.IssuerDataProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    license_name: builtins.str,
    product_name: builtins.str,
    validity: typing.Union[typing.Union[CfnLicense.ValidityDateFormatProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    beneficiary: typing.Optional[builtins.str] = None,
    license_metadata: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLicense.MetadataProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    product_sku: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5077c18265273de5a0d22de6bf87a3f173202cdde8c4baccc223ecdebc0a92ea(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e092e7b09267a1de703b0b70cc1c85de19138d4fa56b8613e310f81fe204793d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e58336cbaf82c3d438d3d1cffb7043d0ef78ed901d57e6b71607d75a04bd5c(
    value: typing.Union[CfnLicense.ConsumptionConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bca8ed084b1ba027ef4c948e1c0c3bd7245530aa8e07ca1a106bcc209ca38a3(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLicense.EntitlementProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c286ce7f74d65142cf153861bd47c086f0aedafee14549c595f229b93ebd3b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055792b7e93ccbc475210b840caca28a5c9357322dddd13b4308031ce203c7d8(
    value: typing.Union[CfnLicense.IssuerDataProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585ba2445b79e2e25f776e347a0acc6dbe38a6fc535589ddeacbcd934c091bb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f9b27f4732af10ea97636a0fad50e3657c50e9a26a0fae226c23abf1232a44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f9f76df056f49e5b1e842fc41b063af0eae64a2dac5d73f20629388c70cd85(
    value: typing.Union[CfnLicense.ValidityDateFormatProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63eff1b31b9bd318f2003ea79b6c963b0fedeae46bcdcda8bae7498a50721253(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98338e739372e84155794b73f5df167dad9dc577e1d8ae51f0753dfcfcd4d1cd(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnLicense.MetadataProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6723664b4908ab7d98be8f5722d0d77ba703a69037a0eb855e152fbbd4fe5213(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa5e25090cc369a5375d4d322d772d9c7f6734b5d3dee889e31b140851db69f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47b43d757f363290102ff6e8457eebd5a907717675db855bcca3ffc2f5cd697(
    *,
    allow_early_check_in: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    max_time_to_live_in_minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0708081d2cd749918b6523bef5426616ef71732b91dd3387f0ffafe4612f2668(
    *,
    borrow_configuration: typing.Optional[typing.Union[typing.Union[CfnLicense.BorrowConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    provisional_configuration: typing.Optional[typing.Union[typing.Union[CfnLicense.ProvisionalConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    renew_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7d744e6f850d943b6e5ab370aee711330a1fae649173adec0f7a315bef410e(
    *,
    name: builtins.str,
    unit: builtins.str,
    allow_check_in: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    max_count: typing.Optional[jsii.Number] = None,
    overage: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6f6d2cd6327c2869e7ddd43643146d61adbffbca1556e7eab53567a81289bb(
    *,
    name: builtins.str,
    sign_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f5b1b387bf41d3e9a94d2f3ce744d67ab0f22281cfb662be1638ebfbb9ad7d(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae85a048710f64199822692c8a37ebb1b996ddf875dafadaeb0e2dd031ba2e0d(
    *,
    max_time_to_live_in_minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386681857f3e29bece1ac555de759e14c46ca4cbde614efaa5d6467d58d3dd27(
    *,
    begin: builtins.str,
    end: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d4716d0616f67cb562264f161dd90c1e8acd67b0dec5602216b296d7258748(
    *,
    consumption_configuration: typing.Union[typing.Union[CfnLicense.ConsumptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    entitlements: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLicense.EntitlementProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    home_region: builtins.str,
    issuer: typing.Union[typing.Union[CfnLicense.IssuerDataProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    license_name: builtins.str,
    product_name: builtins.str,
    validity: typing.Union[typing.Union[CfnLicense.ValidityDateFormatProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    beneficiary: typing.Optional[builtins.str] = None,
    license_metadata: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLicense.MetadataProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    product_sku: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
