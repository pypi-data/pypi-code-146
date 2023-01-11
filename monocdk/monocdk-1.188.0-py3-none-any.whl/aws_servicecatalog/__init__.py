'''
# AWS Service Catalog Construct Library

[AWS Service Catalog](https://docs.aws.amazon.com/servicecatalog/latest/dg/what-is-service-catalog.html)
enables organizations to create and manage catalogs of products for their end users that are approved for use on AWS.

## Table Of Contents

* [Portfolio](#portfolio)

  * [Granting access to a portfolio](#granting-access-to-a-portfolio)
  * [Sharing a portfolio with another AWS account](#sharing-a-portfolio-with-another-aws-account)
* [Product](#product)

  * [Creating a product from a local asset](#creating-a-product-from-local-asset)
  * [Creating a product from a stack](#creating-a-product-from-a-stack)
  * [Creating a Product from a stack with a history of previous versions](#creating-a-product-from-a-stack-with-a-history-of-all-previous-versions)
  * [Adding a product to a portfolio](#adding-a-product-to-a-portfolio)
* [TagOptions](#tag-options)
* [Constraints](#constraints)

  * [Tag update constraint](#tag-update-constraint)
  * [Notify on stack events](#notify-on-stack-events)
  * [CloudFormation template parameters constraint](#cloudformation-template-parameters-constraint)
  * [Set launch role](#set-launch-role)
  * [Deploy with StackSets](#deploy-with-stacksets)

The `@aws-cdk/aws-servicecatalog` package contains resources that enable users to automate governance and management of their AWS resources at scale.

```python
import monocdk as servicecatalog
```

## Portfolio

AWS Service Catalog portfolios allow administrators to organize, manage, and distribute cloud resources for their end users.
Using the CDK, a new portfolio can be created with the `Portfolio` construct:

```python
servicecatalog.Portfolio(self, "Portfolio",
    display_name="MyPortfolio",
    provider_name="MyTeam"
)
```

You can also specify optional metadata properties such as `description` and `messageLanguage`
to help better catalog and manage your portfolios.

```python
servicecatalog.Portfolio(self, "Portfolio",
    display_name="MyFirstPortfolio",
    provider_name="SCAdmin",
    description="Portfolio for a project",
    message_language=servicecatalog.MessageLanguage.EN
)
```

Read more at [Creating and Managing Portfolios](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/catalogs_portfolios.html).

To reference an existing portfolio into your CDK application, use the `Portfolio.fromPortfolioArn()` factory method:

```python
portfolio = servicecatalog.Portfolio.from_portfolio_arn(self, "ReferencedPortfolio", "arn:aws:catalog:region:account-id:portfolio/port-abcdefghi")
```

### Granting access to a portfolio

You can grant access to and manage the `IAM` users, groups, or roles that have access to the products within a portfolio.
Entities with granted access will be able to utilize the portfolios resources and products via the console or AWS CLI.
Once resources are deployed end users will be able to access them via the console or service catalog CLI.

```python
import monocdk as iam

# portfolio: servicecatalog.Portfolio


user = iam.User(self, "User")
portfolio.give_access_to_user(user)

role = iam.Role(self, "Role",
    assumed_by=iam.AccountRootPrincipal()
)
portfolio.give_access_to_role(role)

group = iam.Group(self, "Group")
portfolio.give_access_to_group(group)
```

### Sharing a portfolio with another AWS account

You can use account-to-account sharing to distribute a reference to your portfolio to other AWS accounts by passing the recipient account number.
After the share is initiated, the recipient account can accept the share via CLI or console by importing the portfolio ID.
Changes made to the shared portfolio will automatically propagate to recipients.

```python
# portfolio: servicecatalog.Portfolio

portfolio.share_with_account("012345678901")
```

## Product

Products are version friendly infrastructure-as-code templates that admins create and add to portfolios for end users to provision and create AWS resources.
Service Catalog supports products from AWS Marketplace or ones defined by a CloudFormation template.
The CDK currently only supports adding products of type CloudFormation.
Using the CDK, a new Product can be created with the `CloudFormationProduct` construct.
You can use `CloudFormationTemplate.fromUrl` to create a Product from a CloudFormation template directly from a URL that points to the template in S3, GitHub, or CodeCommit:

```python
product = servicecatalog.CloudFormationProduct(self, "MyFirstProduct",
    product_name="My Product",
    owner="Product Owner",
    product_versions=[servicecatalog.aws_servicecatalog.CloudFormationProductVersion(
        product_version_name="v1",
        cloud_formation_template=servicecatalog.CloudFormationTemplate.from_url("https://raw.githubusercontent.com/awslabs/aws-cloudformation-templates/master/aws/services/ServiceCatalog/Product.yaml")
    )
    ]
)
```

### Creating a product from a local asset

A `CloudFormationProduct` can also be created by using a CloudFormation template held locally on disk using Assets.
Assets are files that are uploaded to an S3 Bucket before deployment.
`CloudFormationTemplate.fromAsset` can be utilized to create a Product by passing the path to a local template file on your disk:

```python
import path as path


product = servicecatalog.CloudFormationProduct(self, "Product",
    product_name="My Product",
    owner="Product Owner",
    product_versions=[servicecatalog.aws_servicecatalog.CloudFormationProductVersion(
        product_version_name="v1",
        cloud_formation_template=servicecatalog.CloudFormationTemplate.from_url("https://raw.githubusercontent.com/awslabs/aws-cloudformation-templates/master/aws/services/ServiceCatalog/Product.yaml")
    ), servicecatalog.aws_servicecatalog.CloudFormationProductVersion(
        product_version_name="v2",
        cloud_formation_template=servicecatalog.CloudFormationTemplate.from_asset(path.join(__dirname, "development-environment.template.json"))
    )
    ]
)
```

### Creating a product from a stack

You can create a Service Catalog `CloudFormationProduct` entirely defined with CDK code using a service catalog `ProductStack`.
A separate child stack for your product is created and you can add resources like you would for any other CDK stack,
such as an S3 Bucket, IAM roles, and EC2 instances. This stack is passed in as a product version to your
product.  This will not create a separate CloudFormation stack during deployment.

```python
import monocdk as s3
import monocdk as cdk


class S3BucketProduct(servicecatalog.ProductStack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        s3.Bucket(self, "BucketProduct")

product = servicecatalog.CloudFormationProduct(self, "Product",
    product_name="My Product",
    owner="Product Owner",
    product_versions=[s3.aws_servicecatalog.CloudFormationProductVersion(
        product_version_name="v1",
        cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(S3BucketProduct(self, "S3BucketProduct"))
    )
    ]
)
```

### Creating a Product from a stack with a history of previous versions

The default behavior of Service Catalog is to overwrite each product version upon deployment.
This applies to Product Stacks as well, where only the latest changes to your Product Stack will
be deployed.
To keep a history of the revisions of a ProductStack available in Service Catalog,
you would need to define a ProductStack for each historical copy.

You can instead create a `ProductStackHistory` to maintain snapshots of all previous versions.
The `ProductStackHistory` can be created by passing the base `productStack`,
a `currentVersionName` for your current version and a `locked` boolean.
The `locked` boolean which when set to true will prevent your `currentVersionName`
from being overwritten when there is an existing snapshot for that version.

```python
import monocdk as s3
import monocdk as cdk


class S3BucketProduct(servicecatalog.ProductStack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        s3.Bucket(self, "BucketProduct")

product_stack_history = servicecatalog.ProductStackHistory(self, "ProductStackHistory",
    product_stack=S3BucketProduct(self, "S3BucketProduct"),
    current_version_name="v1",
    current_version_locked=True
)
```

We can deploy the current version `v1` by using `productStackHistory.currentVersion()`

```python
import monocdk as s3
import monocdk as cdk


class S3BucketProduct(servicecatalog.ProductStack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        s3.Bucket(self, "BucketProductV2")

product_stack_history = servicecatalog.ProductStackHistory(self, "ProductStackHistory",
    product_stack=S3BucketProduct(self, "S3BucketProduct"),
    current_version_name="v2",
    current_version_locked=True
)

product = servicecatalog.CloudFormationProduct(self, "MyFirstProduct",
    product_name="My Product",
    owner="Product Owner",
    product_versions=[
        product_stack_history.current_version()
    ]
)
```

Using `ProductStackHistory` all deployed templates for the ProductStack will be written to disk,
so that they will still be available in the future as the definition of the `ProductStack` subclass changes over time.
**It is very important** that you commit these old versions to source control as these versions
determine whether a version has already been deployed and can also be deployed themselves.

After using `ProductStackHistory` to deploy version `v1` of your `ProductStack`, we
make changes to the `ProductStack` and update the `currentVersionName` to `v2`.
We still want our `v1` version to still be deployed, so we reference it by calling `productStackHistory.versionFromSnapshot('v1')`.

```python
import monocdk as s3
import monocdk as cdk


class S3BucketProduct(servicecatalog.ProductStack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        s3.Bucket(self, "BucketProductV2")

product_stack_history = servicecatalog.ProductStackHistory(self, "ProductStackHistory",
    product_stack=S3BucketProduct(self, "S3BucketProduct"),
    current_version_name="v2",
    current_version_locked=True
)

product = servicecatalog.CloudFormationProduct(self, "MyFirstProduct",
    product_name="My Product",
    owner="Product Owner",
    product_versions=[
        product_stack_history.current_version(),
        product_stack_history.version_from_snapshot("v1")
    ]
)
```

### Adding a product to a portfolio

You add products to a portfolio to organize and distribute your catalog at scale.  Adding a product to a portfolio creates an association,
and the product will become visible within the portfolio side in both the Service Catalog console and AWS CLI.
You can add a product to multiple portfolios depending on your organizational structure and how you would like to group access to products.

```python
# portfolio: servicecatalog.Portfolio
# product: servicecatalog.CloudFormationProduct


portfolio.add_product(product)
```

## Tag Options

TagOptions allow administrators to easily manage tags on provisioned products by providing a template for a selection of tags that end users choose from.
TagOptions are created by specifying a tag key with a set of allowed values and can be associated with both portfolios and products.
When launching a product, both the TagOptions associated with the product and the containing portfolio are made available.

At the moment, TagOptions can only be deactivated in the console.

```python
# portfolio: servicecatalog.Portfolio
# product: servicecatalog.CloudFormationProduct


tag_options_for_portfolio = servicecatalog.TagOptions(self, "OrgTagOptions",
    allowed_values_for_tags={
        "Group": ["finance", "engineering", "marketing", "research"],
        "CostCenter": ["01", "02", "03"]
    }
)
portfolio.associate_tag_options(tag_options_for_portfolio)

tag_options_for_product = servicecatalog.TagOptions(self, "ProductTagOptions",
    allowed_values_for_tags={
        "Environment": ["dev", "alpha", "prod"]
    }
)
product.associate_tag_options(tag_options_for_product)
```

## Constraints

Constraints are governance gestures that you place on product-portfolio associations that allow you to manage minimal launch permissions, notifications, and other optional actions that end users can perform on products.
Using the CDK, if you do not explicitly associate a product to a portfolio and add a constraint, it will automatically add an association for you.

There are rules around how constraints are applied to portfolio-product associations.
For example, you can only have a single "launch role" constraint applied to a portfolio-product association.
If a misconfigured constraint is added, `synth` will fail with an error message.

Read more at [Service Catalog Constraints](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/constraints.html).

### Tag update constraint

Tag update constraints allow or disallow end users to update tags on resources associated with an AWS Service Catalog product upon provisioning.
By default, if a Tag Update constraint is not configured, tag updating is not permitted.
If tag updating is allowed, then new tags associated with the product or portfolio will be applied to provisioned resources during a provisioned product update.

```python
# portfolio: servicecatalog.Portfolio
# product: servicecatalog.CloudFormationProduct


portfolio.add_product(product)
portfolio.constrain_tag_updates(product)
```

If you want to disable this feature later on, you can update it by setting the "allow" parameter to `false`:

```python
# portfolio: servicecatalog.Portfolio
# product: servicecatalog.CloudFormationProduct


# to disable tag updates:
portfolio.constrain_tag_updates(product,
    allow=False
)
```

### Notify on stack events

Allows users to subscribe an AWS `SNS` topic to a provisioned product's CloudFormation stack events.
When an end user provisions a product it creates a CloudFormation stack that notifies the subscribed topic on creation, edit, and delete events.
An individual `SNS` topic may only have a single subscription to any given portfolio-product association.

```python
import monocdk as sns

# portfolio: servicecatalog.Portfolio
# product: servicecatalog.CloudFormationProduct


topic1 = sns.Topic(self, "Topic1")
portfolio.notify_on_stack_events(product, topic1)

topic2 = sns.Topic(self, "Topic2")
portfolio.notify_on_stack_events(product, topic2,
    description="description for topic2"
)
```

### CloudFormation template parameters constraint

CloudFormation template parameter constraints allow you to configure the provisioning parameters that are available to end users when they launch a product.
Template constraint rules consist of one or more assertions that define the default and/or allowable values for a product’s provisioning parameters.
You can configure multiple parameter constraints to govern the different provisioning parameters within your products.
For example, a rule might define the `EC2` instance types that users can choose from when launching a product that includes one or more `EC2` instances.
Parameter rules have an optional `condition` field that allow for rule application to consider conditional evaluations.
If a `condition` is specified, all  assertions will be applied if the condition evaluates to true.
For information on rule-specific intrinsic functions to define rule conditions and assertions,
see [AWS Rule Functions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-rules.html).

```python
import monocdk as cdk

# portfolio: servicecatalog.Portfolio
# product: servicecatalog.CloudFormationProduct


portfolio.constrain_cloud_formation_parameters(product,
    rule=cdk.aws_servicecatalog.TemplateRule(
        rule_name="testInstanceType",
        condition=cdk.Fn.condition_equals(cdk.Fn.ref("Environment"), "test"),
        assertions=[cdk.aws_servicecatalog.TemplateRuleAssertion(
            assert=cdk.Fn.condition_contains(["t2.micro", "t2.small"], cdk.Fn.ref("InstanceType")),
            description="For test environment, the instance type should be small"
        )]
    )
)
```

### Set launch role

Allows you to configure a specific `IAM` role that Service Catalog assumes on behalf of the end user when launching a product.
By setting a launch role constraint, you can maintain least permissions for an end user when launching a product.
For example, a launch role can grant permissions for specific resource creation like an `S3` bucket that the user.
The launch role must be assumed by the Service Catalog principal.
You can only have one launch role set for a portfolio-product association,
and you cannot set a launch role on a product that already has a StackSets deployment configured.

```python
import monocdk as iam

# portfolio: servicecatalog.Portfolio
# product: servicecatalog.CloudFormationProduct


launch_role = iam.Role(self, "LaunchRole",
    assumed_by=iam.ServicePrincipal("servicecatalog.amazonaws.com")
)

portfolio.set_launch_role(product, launch_role)
```

You can also set the launch role using just the name of a role which is locally deployed in end user accounts.
This is useful for when roles and users are separately managed outside of the CDK.
The given role must exist in both the account that creates the launch role constraint,
as well as in any end user accounts that wish to provision a product with the launch role.

You can do this by passing in the role with an explicitly set name:

```python
import monocdk as iam

# portfolio: servicecatalog.Portfolio
# product: servicecatalog.CloudFormationProduct


launch_role = iam.Role(self, "LaunchRole",
    role_name="MyRole",
    assumed_by=iam.ServicePrincipal("servicecatalog.amazonaws.com")
)

portfolio.set_local_launch_role(product, launch_role)
```

Or you can simply pass in a role name and CDK will create a role with that name that trusts service catalog in the account:

```python
import monocdk as iam

# portfolio: servicecatalog.Portfolio
# product: servicecatalog.CloudFormationProduct


role_name = "MyRole"
launch_role = portfolio.set_local_launch_role_name(product, role_name)
```

See [Launch Constraint](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/constraints-launch.html) documentation
to understand the permissions that launch roles need.

### Deploy with StackSets

A StackSets deployment constraint allows you to configure product deployment options using
[AWS CloudFormation StackSets](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/using-stacksets.html).
You can specify one or more accounts and regions into which stack instances will launch when the product is provisioned.
There is an additional field `allowStackSetInstanceOperations` that sets ability for end users to create, edit, or delete the stacks created by the StackSet.
By default, this field is set to `false`.
When launching a StackSets product, end users can select from the list of accounts and regions configured in the constraint to determine where the Stack Instances will deploy and the order of deployment.
You can only define one StackSets deployment configuration per portfolio-product association,
and you cannot both set a launch role and StackSets deployment configuration for an assocation.

```python
import monocdk as iam

# portfolio: servicecatalog.Portfolio
# product: servicecatalog.CloudFormationProduct


admin_role = iam.Role(self, "AdminRole",
    assumed_by=iam.AccountRootPrincipal()
)

portfolio.deploy_with_stack_sets(product,
    accounts=["012345678901", "012345678902", "012345678903"],
    regions=["us-west-1", "us-east-1", "us-west-2", "us-east-1"],
    admin_role=admin_role,
    execution_role_name="SCStackSetExecutionRole",  # Name of role deployed in end users accounts.
    allow_stack_set_instance_operations=True
)
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

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    AssetHashType as _AssetHashType_49193809,
    BundlingOptions as _BundlingOptions_ab115a99,
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    ICfnRuleConditionExpression as _ICfnRuleConditionExpression_5f18240f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    IgnoreMode as _IgnoreMode_31d8bf46,
    Resource as _Resource_abff4495,
    ResourceProps as _ResourceProps_9b554c0f,
    Stack as _Stack_9f43e4a3,
    SymlinkFollowMode as _SymlinkFollowMode_abf4527a,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..assets import FollowMode as _FollowMode_98b05cc5
from ..aws_iam import (
    IGrantable as _IGrantable_4c5a91d1,
    IGroup as _IGroup_8a32caf8,
    IRole as _IRole_59af6f50,
    IUser as _IUser_9d11d57d,
)
from ..aws_s3_assets import AssetOptions as _AssetOptions_bd2996da
from ..aws_sns import ITopic as _ITopic_465e36b9


@jsii.implements(_IInspectable_82c04a63)
class CfnAcceptedPortfolioShare(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnAcceptedPortfolioShare",
):
    '''A CloudFormation ``AWS::ServiceCatalog::AcceptedPortfolioShare``.

    Accepts an offer to share the specified portfolio.

    :cloudformationResource: AWS::ServiceCatalog::AcceptedPortfolioShare
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_accepted_portfolio_share = servicecatalog.CfnAcceptedPortfolioShare(self, "MyCfnAcceptedPortfolioShare",
            portfolio_id="portfolioId",
        
            # the properties below are optional
            accept_language="acceptLanguage"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        portfolio_id: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::AcceptedPortfolioShare``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param portfolio_id: The portfolio identifier.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb685df489c56024f8584f078468fe872941fb5734b5485ed201af4e721ed19)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAcceptedPortfolioShareProps(
            portfolio_id=portfolio_id, accept_language=accept_language
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a594d112c33c8a7678141e5512d38e6f1738953f348d84b057f4c7f9aa369cb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f063f1cc3014b1e4639b28b313fb1c35feb9697f829e6dc0f778b4724d87a49)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html#cfn-servicecatalog-acceptedportfolioshare-portfolioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))

    @portfolio_id.setter
    def portfolio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd011ab55e173816627584592626db7d1d9bf2e4ddfe30b86058c9bbe6581ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portfolioId", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html#cfn-servicecatalog-acceptedportfolioshare-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4cf33d08399271a317321a1c29080e72fefb142166f8119dc2e8bd73602381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnAcceptedPortfolioShareProps",
    jsii_struct_bases=[],
    name_mapping={"portfolio_id": "portfolioId", "accept_language": "acceptLanguage"},
)
class CfnAcceptedPortfolioShareProps:
    def __init__(
        self,
        *,
        portfolio_id: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAcceptedPortfolioShare``.

        :param portfolio_id: The portfolio identifier.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_accepted_portfolio_share_props = servicecatalog.CfnAcceptedPortfolioShareProps(
                portfolio_id="portfolioId",
            
                # the properties below are optional
                accept_language="acceptLanguage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc161e45ef01366620d0107e45cb474853606638759a39226147b5128acab75)
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "portfolio_id": portfolio_id,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language

    @builtins.property
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html#cfn-servicecatalog-acceptedportfolioshare-portfolioid
        '''
        result = self._values.get("portfolio_id")
        assert result is not None, "Required property 'portfolio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html#cfn-servicecatalog-acceptedportfolioshare-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAcceptedPortfolioShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnCloudFormationProduct(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnCloudFormationProduct",
):
    '''A CloudFormation ``AWS::ServiceCatalog::CloudFormationProduct``.

    Specifies a product.

    :cloudformationResource: AWS::ServiceCatalog::CloudFormationProduct
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        # info: Any
        
        cfn_cloud_formation_product = servicecatalog.CfnCloudFormationProduct(self, "MyCfnCloudFormationProduct",
            name="name",
            owner="owner",
            provisioning_artifact_parameters=[servicecatalog.CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty(
                info=info,
        
                # the properties below are optional
                description="description",
                disable_template_validation=False,
                name="name"
            )],
        
            # the properties below are optional
            accept_language="acceptLanguage",
            description="description",
            distributor="distributor",
            replace_provisioning_artifacts=False,
            support_description="supportDescription",
            support_email="supportEmail",
            support_url="supportUrl",
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
        name: builtins.str,
        owner: builtins.str,
        provisioning_artifact_parameters: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        distributor: typing.Optional[builtins.str] = None,
        replace_provisioning_artifacts: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        support_description: typing.Optional[builtins.str] = None,
        support_email: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::CloudFormationProduct``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the product.
        :param owner: The owner of the product.
        :param provisioning_artifact_parameters: The configuration of the provisioning artifact (also known as a version).
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the product.
        :param distributor: The distributor of the product.
        :param replace_provisioning_artifacts: This property is turned off by default. If turned off, you can update provisioning artifacts or product attributes (such as description, distributor, name, owner, and more) and the associated provisioning artifacts will retain the same unique identifier. Provisioning artifacts are matched within the CloudFormationProduct resource, and only those that have been updated will be changed. Provisioning artifacts are matched by a combinaton of provisioning artifact template URL and name. If turned on, provisioning artifacts will be given a new unique identifier when you update the product or provisioning artifacts.
        :param support_description: The support information about the product.
        :param support_email: The contact email for product support.
        :param support_url: The contact URL for product support. ``^https?:\\/\\//`` / is the pattern used to validate SupportUrl.
        :param tags: One or more tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32cad7358dc48114856f78b9238c514f92f486640d9319eeb7127576712e01f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCloudFormationProductProps(
            name=name,
            owner=owner,
            provisioning_artifact_parameters=provisioning_artifact_parameters,
            accept_language=accept_language,
            description=description,
            distributor=distributor,
            replace_provisioning_artifacts=replace_provisioning_artifacts,
            support_description=support_description,
            support_email=support_email,
            support_url=support_url,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4709033ec20ff41693d6395749a0f777254b68e8600cda3f186f665288584416)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd43bdde6c7f8345cdb7ef2aed7dd78a02e1a29fad2298531ba12239c9501ea6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrProductName")
    def attr_product_name(self) -> builtins.str:
        '''The name of the product.

        :cloudformationAttribute: ProductName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProductName"))

    @builtins.property
    @jsii.member(jsii_name="attrProvisioningArtifactIds")
    def attr_provisioning_artifact_ids(self) -> builtins.str:
        '''The IDs of the provisioning artifacts.

        :cloudformationAttribute: ProvisioningArtifactIds
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProvisioningArtifactIds"))

    @builtins.property
    @jsii.member(jsii_name="attrProvisioningArtifactNames")
    def attr_provisioning_artifact_names(self) -> builtins.str:
        '''The names of the provisioning artifacts.

        :cloudformationAttribute: ProvisioningArtifactNames
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProvisioningArtifactNames"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''One or more tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94bac71d02c79d66842f08d94855cd9e2fd2d92f22bd1d1f12f99ee88b5518e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        '''The owner of the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-owner
        '''
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42cb8cc3df90c31867c0600eefb74a22f4fda9a2135df6f6453d9e3062bfe2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value)

    @builtins.property
    @jsii.member(jsii_name="provisioningArtifactParameters")
    def provisioning_artifact_parameters(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty", _IResolvable_a771d0ef]]]:
        '''The configuration of the provisioning artifact (also known as a version).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactparameters
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty", _IResolvable_a771d0ef]]], jsii.get(self, "provisioningArtifactParameters"))

    @provisioning_artifact_parameters.setter
    def provisioning_artifact_parameters(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac2d5706abd7a999aff9b2574cf3355c851c2952cafd12cefa8dd4451618e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningArtifactParameters", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f6f0ce7af309724786f8527e605d07933f179d669d6e1122b589589020e6f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1735f7671b290d9fa5b672bee0f1ce22d8ac2db43d4514bf66b793293362834c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="distributor")
    def distributor(self) -> typing.Optional[builtins.str]:
        '''The distributor of the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-distributor
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distributor"))

    @distributor.setter
    def distributor(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0df9c79c44d4293504a7e33afbb958ab5638c675d3d06867bafbd290091d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributor", value)

    @builtins.property
    @jsii.member(jsii_name="replaceProvisioningArtifacts")
    def replace_provisioning_artifacts(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''This property is turned off by default.

        If turned off, you can update provisioning artifacts or product attributes (such as description, distributor, name, owner, and more) and the associated provisioning artifacts will retain the same unique identifier. Provisioning artifacts are matched within the CloudFormationProduct resource, and only those that have been updated will be changed. Provisioning artifacts are matched by a combinaton of provisioning artifact template URL and name.

        If turned on, provisioning artifacts will be given a new unique identifier when you update the product or provisioning artifacts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-replaceprovisioningartifacts
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "replaceProvisioningArtifacts"))

    @replace_provisioning_artifacts.setter
    def replace_provisioning_artifacts(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f109e8f99080405dc4ad742d34af2790365f6d4487757cf510c81934d6902a65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replaceProvisioningArtifacts", value)

    @builtins.property
    @jsii.member(jsii_name="supportDescription")
    def support_description(self) -> typing.Optional[builtins.str]:
        '''The support information about the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supportdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportDescription"))

    @support_description.setter
    def support_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd335ddbf12141b271489844380936290547469f639a8b67bd0f6328aac0b23c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportDescription", value)

    @builtins.property
    @jsii.member(jsii_name="supportEmail")
    def support_email(self) -> typing.Optional[builtins.str]:
        '''The contact email for product support.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supportemail
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportEmail"))

    @support_email.setter
    def support_email(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1caa6ae9c26a7fa52ba2c3dad08028190f96747b02e6f48fdbcde66cda81df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportEmail", value)

    @builtins.property
    @jsii.member(jsii_name="supportUrl")
    def support_url(self) -> typing.Optional[builtins.str]:
        '''The contact URL for product support.

        ``^https?:\\/\\//`` / is the pattern used to validate SupportUrl.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supporturl
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportUrl"))

    @support_url.setter
    def support_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0422bc0b2864b71a4cdfbd8b9e223a6a1cf9f5d6aa441682224609ac5e15a93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportUrl", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_servicecatalog.CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "info": "info",
            "description": "description",
            "disable_template_validation": "disableTemplateValidation",
            "name": "name",
        },
    )
    class ProvisioningArtifactPropertiesProperty:
        def __init__(
            self,
            *,
            info: typing.Any,
            description: typing.Optional[builtins.str] = None,
            disable_template_validation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a provisioning artifact (also known as a version) for a product.

            :param info: Specify the template source with one of the following options, but not both. Keys accepted: [ ``LoadTemplateFromURL`` , ``ImportFromPhysicalId`` ] The URL of the AWS CloudFormation template in Amazon S3 or GitHub in JSON format. Specify the URL in JSON format as follows: ``"LoadTemplateFromURL": "https://s3.amazonaws.com/cf-templates-ozkq9d3hgiq2-us-east-1/..."`` ``ImportFromPhysicalId`` : The physical id of the resource that contains the template. Currently only supports AWS CloudFormation stack arn. Specify the physical id in JSON format as follows: ``ImportFromPhysicalId: “arn:aws:cloudformation:[us-east-1]:[accountId]:stack/[StackName]/[resourceId]``
            :param description: The description of the provisioning artifact, including how it differs from the previous provisioning artifact.
            :param disable_template_validation: If set to true, AWS Service Catalog stops validating the specified provisioning artifact even if it is invalid.
            :param name: The name of the provisioning artifact (for example, v1 v2beta). No spaces are allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_servicecatalog as servicecatalog
                
                # info: Any
                
                provisioning_artifact_properties_property = servicecatalog.CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty(
                    info=info,
                
                    # the properties below are optional
                    description="description",
                    disable_template_validation=False,
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c1dcf62559e2918572877ef85a560c4c0674eaabd8857c89ef9a439f3033027)
                check_type(argname="argument info", value=info, expected_type=type_hints["info"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument disable_template_validation", value=disable_template_validation, expected_type=type_hints["disable_template_validation"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "info": info,
            }
            if description is not None:
                self._values["description"] = description
            if disable_template_validation is not None:
                self._values["disable_template_validation"] = disable_template_validation
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def info(self) -> typing.Any:
            '''Specify the template source with one of the following options, but not both.

            Keys accepted: [ ``LoadTemplateFromURL`` , ``ImportFromPhysicalId`` ]

            The URL of the AWS CloudFormation template in Amazon S3 or GitHub in JSON format. Specify the URL in JSON format as follows:

            ``"LoadTemplateFromURL": "https://s3.amazonaws.com/cf-templates-ozkq9d3hgiq2-us-east-1/..."``

            ``ImportFromPhysicalId`` : The physical id of the resource that contains the template. Currently only supports AWS CloudFormation stack arn. Specify the physical id in JSON format as follows: ``ImportFromPhysicalId: “arn:aws:cloudformation:[us-east-1]:[accountId]:stack/[StackName]/[resourceId]``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-info
            '''
            result = self._values.get("info")
            assert result is not None, "Required property 'info' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the provisioning artifact, including how it differs from the previous provisioning artifact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disable_template_validation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''If set to true, AWS Service Catalog stops validating the specified provisioning artifact even if it is invalid.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-disabletemplatevalidation
            '''
            result = self._values.get("disable_template_validation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the provisioning artifact (for example, v1 v2beta).

            No spaces are allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisioningArtifactPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnCloudFormationProductProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "owner": "owner",
        "provisioning_artifact_parameters": "provisioningArtifactParameters",
        "accept_language": "acceptLanguage",
        "description": "description",
        "distributor": "distributor",
        "replace_provisioning_artifacts": "replaceProvisioningArtifacts",
        "support_description": "supportDescription",
        "support_email": "supportEmail",
        "support_url": "supportUrl",
        "tags": "tags",
    },
)
class CfnCloudFormationProductProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        owner: builtins.str,
        provisioning_artifact_parameters: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        distributor: typing.Optional[builtins.str] = None,
        replace_provisioning_artifacts: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        support_description: typing.Optional[builtins.str] = None,
        support_email: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCloudFormationProduct``.

        :param name: The name of the product.
        :param owner: The owner of the product.
        :param provisioning_artifact_parameters: The configuration of the provisioning artifact (also known as a version).
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the product.
        :param distributor: The distributor of the product.
        :param replace_provisioning_artifacts: This property is turned off by default. If turned off, you can update provisioning artifacts or product attributes (such as description, distributor, name, owner, and more) and the associated provisioning artifacts will retain the same unique identifier. Provisioning artifacts are matched within the CloudFormationProduct resource, and only those that have been updated will be changed. Provisioning artifacts are matched by a combinaton of provisioning artifact template URL and name. If turned on, provisioning artifacts will be given a new unique identifier when you update the product or provisioning artifacts.
        :param support_description: The support information about the product.
        :param support_email: The contact email for product support.
        :param support_url: The contact URL for product support. ``^https?:\\/\\//`` / is the pattern used to validate SupportUrl.
        :param tags: One or more tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            # info: Any
            
            cfn_cloud_formation_product_props = servicecatalog.CfnCloudFormationProductProps(
                name="name",
                owner="owner",
                provisioning_artifact_parameters=[servicecatalog.CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty(
                    info=info,
            
                    # the properties below are optional
                    description="description",
                    disable_template_validation=False,
                    name="name"
                )],
            
                # the properties below are optional
                accept_language="acceptLanguage",
                description="description",
                distributor="distributor",
                replace_provisioning_artifacts=False,
                support_description="supportDescription",
                support_email="supportEmail",
                support_url="supportUrl",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fa67596851c515b37a8c4ff84fb8c54e715b89840507c8bf46ced4e237f364)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument provisioning_artifact_parameters", value=provisioning_artifact_parameters, expected_type=type_hints["provisioning_artifact_parameters"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument distributor", value=distributor, expected_type=type_hints["distributor"])
            check_type(argname="argument replace_provisioning_artifacts", value=replace_provisioning_artifacts, expected_type=type_hints["replace_provisioning_artifacts"])
            check_type(argname="argument support_description", value=support_description, expected_type=type_hints["support_description"])
            check_type(argname="argument support_email", value=support_email, expected_type=type_hints["support_email"])
            check_type(argname="argument support_url", value=support_url, expected_type=type_hints["support_url"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "owner": owner,
            "provisioning_artifact_parameters": provisioning_artifact_parameters,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description
        if distributor is not None:
            self._values["distributor"] = distributor
        if replace_provisioning_artifacts is not None:
            self._values["replace_provisioning_artifacts"] = replace_provisioning_artifacts
        if support_description is not None:
            self._values["support_description"] = support_description
        if support_email is not None:
            self._values["support_email"] = support_email
        if support_url is not None:
            self._values["support_url"] = support_url
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''The owner of the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-owner
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provisioning_artifact_parameters(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty, _IResolvable_a771d0ef]]]:
        '''The configuration of the provisioning artifact (also known as a version).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactparameters
        '''
        result = self._values.get("provisioning_artifact_parameters")
        assert result is not None, "Required property 'provisioning_artifact_parameters' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distributor(self) -> typing.Optional[builtins.str]:
        '''The distributor of the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-distributor
        '''
        result = self._values.get("distributor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replace_provisioning_artifacts(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''This property is turned off by default.

        If turned off, you can update provisioning artifacts or product attributes (such as description, distributor, name, owner, and more) and the associated provisioning artifacts will retain the same unique identifier. Provisioning artifacts are matched within the CloudFormationProduct resource, and only those that have been updated will be changed. Provisioning artifacts are matched by a combinaton of provisioning artifact template URL and name.

        If turned on, provisioning artifacts will be given a new unique identifier when you update the product or provisioning artifacts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-replaceprovisioningartifacts
        '''
        result = self._values.get("replace_provisioning_artifacts")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def support_description(self) -> typing.Optional[builtins.str]:
        '''The support information about the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supportdescription
        '''
        result = self._values.get("support_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_email(self) -> typing.Optional[builtins.str]:
        '''The contact email for product support.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supportemail
        '''
        result = self._values.get("support_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_url(self) -> typing.Optional[builtins.str]:
        '''The contact URL for product support.

        ``^https?:\\/\\//`` / is the pattern used to validate SupportUrl.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supporturl
        '''
        result = self._values.get("support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''One or more tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCloudFormationProductProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnCloudFormationProvisionedProduct(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnCloudFormationProvisionedProduct",
):
    '''A CloudFormation ``AWS::ServiceCatalog::CloudFormationProvisionedProduct``.

    Provisions the specified product.

    A provisioned product is a resourced instance of a product. For example, provisioning a product based on a AWS CloudFormation template launches a AWS CloudFormation stack and its underlying resources. You can check the status of this request using `DescribeRecord <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_DescribeRecord.html>`_ .

    If the request contains a tag key with an empty list of values, there is a tag conflict for that key. Do not include conflicted keys as tags, or this causes the error "Parameter validation failed: Missing required parameter in Tags[ *N* ]: *Value* ".

    :cloudformationResource: AWS::ServiceCatalog::CloudFormationProvisionedProduct
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_cloud_formation_provisioned_product = servicecatalog.CfnCloudFormationProvisionedProduct(self, "MyCfnCloudFormationProvisionedProduct",
            accept_language="acceptLanguage",
            notification_arns=["notificationArns"],
            path_id="pathId",
            path_name="pathName",
            product_id="productId",
            product_name="productName",
            provisioned_product_name="provisionedProductName",
            provisioning_artifact_id="provisioningArtifactId",
            provisioning_artifact_name="provisioningArtifactName",
            provisioning_parameters=[servicecatalog.CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty(
                key="key",
                value="value"
            )],
            provisioning_preferences=servicecatalog.CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty(
                stack_set_accounts=["stackSetAccounts"],
                stack_set_failure_tolerance_count=123,
                stack_set_failure_tolerance_percentage=123,
                stack_set_max_concurrency_count=123,
                stack_set_max_concurrency_percentage=123,
                stack_set_operation_type="stackSetOperationType",
                stack_set_regions=["stackSetRegions"]
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
        accept_language: typing.Optional[builtins.str] = None,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path_id: typing.Optional[builtins.str] = None,
        path_name: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        product_name: typing.Optional[builtins.str] = None,
        provisioned_product_name: typing.Optional[builtins.str] = None,
        provisioning_artifact_id: typing.Optional[builtins.str] = None,
        provisioning_artifact_name: typing.Optional[builtins.str] = None,
        provisioning_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        provisioning_preferences: typing.Optional[typing.Union[typing.Union["CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::CloudFormationProvisionedProduct``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param notification_arns: Passed to AWS CloudFormation . The SNS topic ARNs to which to publish stack-related events.
        :param path_id: The path identifier of the product. This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ . .. epigraph:: You must provide the name or ID, but not both.
        :param path_name: The name of the path. This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ . .. epigraph:: You must provide the name or ID, but not both.
        :param product_id: The product identifier. .. epigraph:: You must specify either the ID or the name of the product, but not both.
        :param product_name: A user-friendly name for the provisioned product. This value must be unique for the AWS account and cannot be updated after the product is provisioned. Each time a stack is created or updated, if ``ProductName`` is provided it will successfully resolve to ``ProductId`` as long as only one product exists in the account or Region with that ``ProductName`` . .. epigraph:: You must specify either the name or the ID of the product, but not both.
        :param provisioned_product_name: A user-friendly name for the provisioned product. This value must be unique for the AWS account and cannot be updated after the product is provisioned.
        :param provisioning_artifact_id: The identifier of the provisioning artifact (also known as a version). .. epigraph:: You must specify either the ID or the name of the provisioning artifact, but not both.
        :param provisioning_artifact_name: The name of the provisioning artifact (also known as a version) for the product. This name must be unique for the product. .. epigraph:: You must specify either the name or the ID of the provisioning artifact, but not both. You must also specify either the name or the ID of the product, but not both.
        :param provisioning_parameters: Parameters specified by the administrator that are required for provisioning the product.
        :param provisioning_preferences: StackSet preferences that are required for provisioning the product or updating a provisioned product.
        :param tags: One or more tags. .. epigraph:: Requires the provisioned product to have an `ResourceUpdateConstraint <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html>`_ resource with ``TagUpdatesOnProvisionedProduct`` set to ``ALLOWED`` to allow tag updates. If ``RESOURCE_UPDATE`` constraint is not present, tags updates are ignored.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5cdf2f6d31986e586e0370596d1bf4e2f8f63a7a22782662dc406b1c2821803)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCloudFormationProvisionedProductProps(
            accept_language=accept_language,
            notification_arns=notification_arns,
            path_id=path_id,
            path_name=path_name,
            product_id=product_id,
            product_name=product_name,
            provisioned_product_name=provisioned_product_name,
            provisioning_artifact_id=provisioning_artifact_id,
            provisioning_artifact_name=provisioning_artifact_name,
            provisioning_parameters=provisioning_parameters,
            provisioning_preferences=provisioning_preferences,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd772f3aec3eecff526c370e71882091d82549c0538a95bf3a6a00c793cff81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfa15c208374c1d975fee78bbcbaf43155172e03a50d6be47f9de98a9cf2df40)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCloudformationStackArn")
    def attr_cloudformation_stack_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the CloudFormation stack, such as ``arn:aws:cloudformation:eu-west-1:123456789012:stack/SC-499278721343-pp-hfyszaotincww/8f3df460-346a-11e8-9444-503abe701c29`` .

        :cloudformationAttribute: CloudformationStackArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCloudformationStackArn"))

    @builtins.property
    @jsii.member(jsii_name="attrOutputs")
    def attr_outputs(self) -> _IResolvable_a771d0ef:
        '''The output of the product you are provisioning.

        For example, the DNS of an EC2 instance.

        :cloudformationAttribute: Outputs
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrOutputs"))

    @builtins.property
    @jsii.member(jsii_name="attrProvisionedProductId")
    def attr_provisioned_product_id(self) -> builtins.str:
        '''The ID of the provisioned product.

        :cloudformationAttribute: ProvisionedProductId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProvisionedProductId"))

    @builtins.property
    @jsii.member(jsii_name="attrRecordId")
    def attr_record_id(self) -> builtins.str:
        '''The ID of the record, such as ``rec-rjeatvy434trk`` .

        :cloudformationAttribute: RecordId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRecordId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''One or more tags.

        .. epigraph::

           Requires the provisioned product to have an `ResourceUpdateConstraint <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html>`_ resource with ``TagUpdatesOnProvisionedProduct`` set to ``ALLOWED`` to allow tag updates. If ``RESOURCE_UPDATE`` constraint is not present, tags updates are ignored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f9a53b9c44c1bac61c4a56a8f4de52b50c3091239021bce241e8fc6d9f4062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Passed to AWS CloudFormation .

        The SNS topic ARNs to which to publish stack-related events.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-notificationarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationArns"))

    @notification_arns.setter
    def notification_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233482fcfa1eefbbaa22fd2475d6b587133bea32dc599f2ccad985cbb87da925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationArns", value)

    @builtins.property
    @jsii.member(jsii_name="pathId")
    def path_id(self) -> typing.Optional[builtins.str]:
        '''The path identifier of the product.

        This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ .
        .. epigraph::

           You must provide the name or ID, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-pathid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathId"))

    @path_id.setter
    def path_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b389399c02209eb56af05384e6e61138cb7d4765374ce1284a02e850502e2f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathId", value)

    @builtins.property
    @jsii.member(jsii_name="pathName")
    def path_name(self) -> typing.Optional[builtins.str]:
        '''The name of the path.

        This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ .
        .. epigraph::

           You must provide the name or ID, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-pathname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathName"))

    @path_name.setter
    def path_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6cbc15f02e92b6dfcc798a060ec258fc1b231e6a4b8493f5c03de4cb8dc4187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathName", value)

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product identifier.

        .. epigraph::

           You must specify either the ID or the name of the product, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-productid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcda3750f994a44ece3b4e21ab06359e5aab38630826c4eea0ad0689470a81f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value)

    @builtins.property
    @jsii.member(jsii_name="productName")
    def product_name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly name for the provisioned product.

        This value must be unique for the AWS account and cannot be updated after the product is provisioned.

        Each time a stack is created or updated, if ``ProductName`` is provided it will successfully resolve to ``ProductId`` as long as only one product exists in the account or Region with that ``ProductName`` .
        .. epigraph::

           You must specify either the name or the ID of the product, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-productname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productName"))

    @product_name.setter
    def product_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aef01a453134a34ec9c688286808598351db7e27ec9c657d2ebcb5a7da44d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productName", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedProductName")
    def provisioned_product_name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly name for the provisioned product.

        This value must be unique for the AWS account and cannot be updated after the product is provisioned.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisionedproductname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provisionedProductName"))

    @provisioned_product_name.setter
    def provisioned_product_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515f7712d787f2e88c49a8cd030474ad8faee4aba2bf48f779eb9c2d0282af62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedProductName", value)

    @builtins.property
    @jsii.member(jsii_name="provisioningArtifactId")
    def provisioning_artifact_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the provisioning artifact (also known as a version).

        .. epigraph::

           You must specify either the ID or the name of the provisioning artifact, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningartifactid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provisioningArtifactId"))

    @provisioning_artifact_id.setter
    def provisioning_artifact_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a082e13f4b9b5df4d1826bdab2c82de578905a4e81c37753809c128a43ec1d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningArtifactId", value)

    @builtins.property
    @jsii.member(jsii_name="provisioningArtifactName")
    def provisioning_artifact_name(self) -> typing.Optional[builtins.str]:
        '''The name of the provisioning artifact (also known as a version) for the product.

        This name must be unique for the product.
        .. epigraph::

           You must specify either the name or the ID of the provisioning artifact, but not both. You must also specify either the name or the ID of the product, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningartifactname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provisioningArtifactName"))

    @provisioning_artifact_name.setter
    def provisioning_artifact_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133037dce530aba0bd62160004f3f6320364d6c3c3840d76e7eb814b94baf03b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningArtifactName", value)

    @builtins.property
    @jsii.member(jsii_name="provisioningParameters")
    def provisioning_parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty", _IResolvable_a771d0ef]]]]:
        '''Parameters specified by the administrator that are required for provisioning the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningparameters
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "provisioningParameters"))

    @provisioning_parameters.setter
    def provisioning_parameters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa95e9be68bac7b93538bf80ceca916aa3d01b03c95739ac4137c769eba050d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningParameters", value)

    @builtins.property
    @jsii.member(jsii_name="provisioningPreferences")
    def provisioning_preferences(
        self,
    ) -> typing.Optional[typing.Union["CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty", _IResolvable_a771d0ef]]:
        '''StackSet preferences that are required for provisioning the product or updating a provisioned product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty", _IResolvable_a771d0ef]], jsii.get(self, "provisioningPreferences"))

    @provisioning_preferences.setter
    def provisioning_preferences(
        self,
        value: typing.Optional[typing.Union["CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a76e672cafd782295227b9e6afd1d950fc994b4d3b80e5ea7e338d24b14980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningPreferences", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_servicecatalog.CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ProvisioningParameterProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''Information about a parameter used to provision a product.

            :param key: The parameter key.
            :param value: The parameter value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_servicecatalog as servicecatalog
                
                provisioning_parameter_property = servicecatalog.CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__96057e2186b4eff04d05e767a288e525283e66d8c6693ecc3be1c9131b51920a)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The parameter key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningparameter.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningparameter-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The parameter value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningparameter.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningparameter-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisioningParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_servicecatalog.CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "stack_set_accounts": "stackSetAccounts",
            "stack_set_failure_tolerance_count": "stackSetFailureToleranceCount",
            "stack_set_failure_tolerance_percentage": "stackSetFailureTolerancePercentage",
            "stack_set_max_concurrency_count": "stackSetMaxConcurrencyCount",
            "stack_set_max_concurrency_percentage": "stackSetMaxConcurrencyPercentage",
            "stack_set_operation_type": "stackSetOperationType",
            "stack_set_regions": "stackSetRegions",
        },
    )
    class ProvisioningPreferencesProperty:
        def __init__(
            self,
            *,
            stack_set_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            stack_set_failure_tolerance_count: typing.Optional[jsii.Number] = None,
            stack_set_failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
            stack_set_max_concurrency_count: typing.Optional[jsii.Number] = None,
            stack_set_max_concurrency_percentage: typing.Optional[jsii.Number] = None,
            stack_set_operation_type: typing.Optional[builtins.str] = None,
            stack_set_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The user-defined preferences that will be applied when updating a provisioned product.

            Not all preferences are applicable to all provisioned product type

            One or more AWS accounts that will have access to the provisioned product.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            The AWS accounts specified should be within the list of accounts in the ``STACKSET`` constraint. To get the list of accounts in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation.

            If no values are specified, the default value is all accounts from the ``STACKSET`` constraint.

            :param stack_set_accounts: One or more AWS accounts where the provisioned product will be available. Applicable only to a ``CFN_STACKSET`` provisioned product type. The specified accounts should be within the list of accounts from the ``STACKSET`` constraint. To get the list of accounts in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation. If no values are specified, the default value is all acounts from the ``STACKSET`` constraint.
            :param stack_set_failure_tolerance_count: The number of accounts, per Region, for which this operation can fail before AWS Service Catalog stops the operation in that Region. If the operation is stopped in a Region, AWS Service Catalog doesn't attempt the operation in any subsequent Regions. Applicable only to a ``CFN_STACKSET`` provisioned product type. Conditional: You must specify either ``StackSetFailureToleranceCount`` or ``StackSetFailureTolerancePercentage`` , but not both. The default value is ``0`` if no value is specified.
            :param stack_set_failure_tolerance_percentage: The percentage of accounts, per Region, for which this stack operation can fail before AWS Service Catalog stops the operation in that Region. If the operation is stopped in a Region, AWS Service Catalog doesn't attempt the operation in any subsequent Regions. When calculating the number of accounts based on the specified percentage, AWS Service Catalog rounds down to the next whole number. Applicable only to a ``CFN_STACKSET`` provisioned product type. Conditional: You must specify either ``StackSetFailureToleranceCount`` or ``StackSetFailureTolerancePercentage`` , but not both.
            :param stack_set_max_concurrency_count: The maximum number of accounts in which to perform this operation at one time. This is dependent on the value of ``StackSetFailureToleranceCount`` . ``StackSetMaxConcurrentCount`` is at most one more than the ``StackSetFailureToleranceCount`` . Note that this setting lets you specify the maximum for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling. Applicable only to a ``CFN_STACKSET`` provisioned product type. Conditional: You must specify either ``StackSetMaxConcurrentCount`` or ``StackSetMaxConcurrentPercentage`` , but not both.
            :param stack_set_max_concurrency_percentage: The maximum percentage of accounts in which to perform this operation at one time. When calculating the number of accounts based on the specified percentage, AWS Service Catalog rounds down to the next whole number. This is true except in cases where rounding down would result is zero. In this case, AWS Service Catalog sets the number as ``1`` instead. Note that this setting lets you specify the maximum for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling. Applicable only to a ``CFN_STACKSET`` provisioned product type. Conditional: You must specify either ``StackSetMaxConcurrentCount`` or ``StackSetMaxConcurrentPercentage`` , but not both.
            :param stack_set_operation_type: Determines what action AWS Service Catalog performs to a stack set or a stack instance represented by the provisioned product. The default value is ``UPDATE`` if nothing is specified. Applicable only to a ``CFN_STACKSET`` provisioned product type. - **CREATE** - Creates a new stack instance in the stack set represented by the provisioned product. In this case, only new stack instances are created based on accounts and Regions; if new ProductId or ProvisioningArtifactID are passed, they will be ignored. - **UPDATE** - Updates the stack set represented by the provisioned product and also its stack instances. - **DELETE** - Deletes a stack instance in the stack set represented by the provisioned product.
            :param stack_set_regions: One or more AWS Regions where the provisioned product will be available. Applicable only to a ``CFN_STACKSET`` provisioned product type. The specified Regions should be within the list of Regions from the ``STACKSET`` constraint. To get the list of Regions in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation. If no values are specified, the default value is all Regions from the ``STACKSET`` constraint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_servicecatalog as servicecatalog
                
                provisioning_preferences_property = servicecatalog.CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty(
                    stack_set_accounts=["stackSetAccounts"],
                    stack_set_failure_tolerance_count=123,
                    stack_set_failure_tolerance_percentage=123,
                    stack_set_max_concurrency_count=123,
                    stack_set_max_concurrency_percentage=123,
                    stack_set_operation_type="stackSetOperationType",
                    stack_set_regions=["stackSetRegions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f993219da7057d53fa76a310e0ba2a8a553f28e500c74566d14adf1b7f7dce6)
                check_type(argname="argument stack_set_accounts", value=stack_set_accounts, expected_type=type_hints["stack_set_accounts"])
                check_type(argname="argument stack_set_failure_tolerance_count", value=stack_set_failure_tolerance_count, expected_type=type_hints["stack_set_failure_tolerance_count"])
                check_type(argname="argument stack_set_failure_tolerance_percentage", value=stack_set_failure_tolerance_percentage, expected_type=type_hints["stack_set_failure_tolerance_percentage"])
                check_type(argname="argument stack_set_max_concurrency_count", value=stack_set_max_concurrency_count, expected_type=type_hints["stack_set_max_concurrency_count"])
                check_type(argname="argument stack_set_max_concurrency_percentage", value=stack_set_max_concurrency_percentage, expected_type=type_hints["stack_set_max_concurrency_percentage"])
                check_type(argname="argument stack_set_operation_type", value=stack_set_operation_type, expected_type=type_hints["stack_set_operation_type"])
                check_type(argname="argument stack_set_regions", value=stack_set_regions, expected_type=type_hints["stack_set_regions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stack_set_accounts is not None:
                self._values["stack_set_accounts"] = stack_set_accounts
            if stack_set_failure_tolerance_count is not None:
                self._values["stack_set_failure_tolerance_count"] = stack_set_failure_tolerance_count
            if stack_set_failure_tolerance_percentage is not None:
                self._values["stack_set_failure_tolerance_percentage"] = stack_set_failure_tolerance_percentage
            if stack_set_max_concurrency_count is not None:
                self._values["stack_set_max_concurrency_count"] = stack_set_max_concurrency_count
            if stack_set_max_concurrency_percentage is not None:
                self._values["stack_set_max_concurrency_percentage"] = stack_set_max_concurrency_percentage
            if stack_set_operation_type is not None:
                self._values["stack_set_operation_type"] = stack_set_operation_type
            if stack_set_regions is not None:
                self._values["stack_set_regions"] = stack_set_regions

        @builtins.property
        def stack_set_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more AWS accounts where the provisioned product will be available.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            The specified accounts should be within the list of accounts from the ``STACKSET`` constraint. To get the list of accounts in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation.

            If no values are specified, the default value is all acounts from the ``STACKSET`` constraint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetaccounts
            '''
            result = self._values.get("stack_set_accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def stack_set_failure_tolerance_count(self) -> typing.Optional[jsii.Number]:
            '''The number of accounts, per Region, for which this operation can fail before AWS Service Catalog stops the operation in that Region.

            If the operation is stopped in a Region, AWS Service Catalog doesn't attempt the operation in any subsequent Regions.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            Conditional: You must specify either ``StackSetFailureToleranceCount`` or ``StackSetFailureTolerancePercentage`` , but not both.

            The default value is ``0`` if no value is specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetfailuretolerancecount
            '''
            result = self._values.get("stack_set_failure_tolerance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stack_set_failure_tolerance_percentage(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The percentage of accounts, per Region, for which this stack operation can fail before AWS Service Catalog stops the operation in that Region.

            If the operation is stopped in a Region, AWS Service Catalog doesn't attempt the operation in any subsequent Regions.

            When calculating the number of accounts based on the specified percentage, AWS Service Catalog rounds down to the next whole number.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            Conditional: You must specify either ``StackSetFailureToleranceCount`` or ``StackSetFailureTolerancePercentage`` , but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetfailuretolerancepercentage
            '''
            result = self._values.get("stack_set_failure_tolerance_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stack_set_max_concurrency_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of accounts in which to perform this operation at one time.

            This is dependent on the value of ``StackSetFailureToleranceCount`` . ``StackSetMaxConcurrentCount`` is at most one more than the ``StackSetFailureToleranceCount`` .

            Note that this setting lets you specify the maximum for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            Conditional: You must specify either ``StackSetMaxConcurrentCount`` or ``StackSetMaxConcurrentPercentage`` , but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetmaxconcurrencycount
            '''
            result = self._values.get("stack_set_max_concurrency_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stack_set_max_concurrency_percentage(self) -> typing.Optional[jsii.Number]:
            '''The maximum percentage of accounts in which to perform this operation at one time.

            When calculating the number of accounts based on the specified percentage, AWS Service Catalog rounds down to the next whole number. This is true except in cases where rounding down would result is zero. In this case, AWS Service Catalog sets the number as ``1`` instead.

            Note that this setting lets you specify the maximum for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            Conditional: You must specify either ``StackSetMaxConcurrentCount`` or ``StackSetMaxConcurrentPercentage`` , but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetmaxconcurrencypercentage
            '''
            result = self._values.get("stack_set_max_concurrency_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stack_set_operation_type(self) -> typing.Optional[builtins.str]:
            '''Determines what action AWS Service Catalog performs to a stack set or a stack instance represented by the provisioned product.

            The default value is ``UPDATE`` if nothing is specified.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            - **CREATE** - Creates a new stack instance in the stack set represented by the provisioned product. In this case, only new stack instances are created based on accounts and Regions; if new ProductId or ProvisioningArtifactID are passed, they will be ignored.
            - **UPDATE** - Updates the stack set represented by the provisioned product and also its stack instances.
            - **DELETE** - Deletes a stack instance in the stack set represented by the provisioned product.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetoperationtype
            '''
            result = self._values.get("stack_set_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stack_set_regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more AWS Regions where the provisioned product will be available.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            The specified Regions should be within the list of Regions from the ``STACKSET`` constraint. To get the list of Regions in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation.

            If no values are specified, the default value is all Regions from the ``STACKSET`` constraint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetregions
            '''
            result = self._values.get("stack_set_regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisioningPreferencesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnCloudFormationProvisionedProductProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "notification_arns": "notificationArns",
        "path_id": "pathId",
        "path_name": "pathName",
        "product_id": "productId",
        "product_name": "productName",
        "provisioned_product_name": "provisionedProductName",
        "provisioning_artifact_id": "provisioningArtifactId",
        "provisioning_artifact_name": "provisioningArtifactName",
        "provisioning_parameters": "provisioningParameters",
        "provisioning_preferences": "provisioningPreferences",
        "tags": "tags",
    },
)
class CfnCloudFormationProvisionedProductProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path_id: typing.Optional[builtins.str] = None,
        path_name: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        product_name: typing.Optional[builtins.str] = None,
        provisioned_product_name: typing.Optional[builtins.str] = None,
        provisioning_artifact_id: typing.Optional[builtins.str] = None,
        provisioning_artifact_name: typing.Optional[builtins.str] = None,
        provisioning_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        provisioning_preferences: typing.Optional[typing.Union[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCloudFormationProvisionedProduct``.

        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param notification_arns: Passed to AWS CloudFormation . The SNS topic ARNs to which to publish stack-related events.
        :param path_id: The path identifier of the product. This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ . .. epigraph:: You must provide the name or ID, but not both.
        :param path_name: The name of the path. This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ . .. epigraph:: You must provide the name or ID, but not both.
        :param product_id: The product identifier. .. epigraph:: You must specify either the ID or the name of the product, but not both.
        :param product_name: A user-friendly name for the provisioned product. This value must be unique for the AWS account and cannot be updated after the product is provisioned. Each time a stack is created or updated, if ``ProductName`` is provided it will successfully resolve to ``ProductId`` as long as only one product exists in the account or Region with that ``ProductName`` . .. epigraph:: You must specify either the name or the ID of the product, but not both.
        :param provisioned_product_name: A user-friendly name for the provisioned product. This value must be unique for the AWS account and cannot be updated after the product is provisioned.
        :param provisioning_artifact_id: The identifier of the provisioning artifact (also known as a version). .. epigraph:: You must specify either the ID or the name of the provisioning artifact, but not both.
        :param provisioning_artifact_name: The name of the provisioning artifact (also known as a version) for the product. This name must be unique for the product. .. epigraph:: You must specify either the name or the ID of the provisioning artifact, but not both. You must also specify either the name or the ID of the product, but not both.
        :param provisioning_parameters: Parameters specified by the administrator that are required for provisioning the product.
        :param provisioning_preferences: StackSet preferences that are required for provisioning the product or updating a provisioned product.
        :param tags: One or more tags. .. epigraph:: Requires the provisioned product to have an `ResourceUpdateConstraint <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html>`_ resource with ``TagUpdatesOnProvisionedProduct`` set to ``ALLOWED`` to allow tag updates. If ``RESOURCE_UPDATE`` constraint is not present, tags updates are ignored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_cloud_formation_provisioned_product_props = servicecatalog.CfnCloudFormationProvisionedProductProps(
                accept_language="acceptLanguage",
                notification_arns=["notificationArns"],
                path_id="pathId",
                path_name="pathName",
                product_id="productId",
                product_name="productName",
                provisioned_product_name="provisionedProductName",
                provisioning_artifact_id="provisioningArtifactId",
                provisioning_artifact_name="provisioningArtifactName",
                provisioning_parameters=[servicecatalog.CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty(
                    key="key",
                    value="value"
                )],
                provisioning_preferences=servicecatalog.CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty(
                    stack_set_accounts=["stackSetAccounts"],
                    stack_set_failure_tolerance_count=123,
                    stack_set_failure_tolerance_percentage=123,
                    stack_set_max_concurrency_count=123,
                    stack_set_max_concurrency_percentage=123,
                    stack_set_operation_type="stackSetOperationType",
                    stack_set_regions=["stackSetRegions"]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d74d7302604d6f1567269adcc84c2c44abe22094fcc16d4b6930fdf9868dbe5)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument path_id", value=path_id, expected_type=type_hints["path_id"])
            check_type(argname="argument path_name", value=path_name, expected_type=type_hints["path_name"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument product_name", value=product_name, expected_type=type_hints["product_name"])
            check_type(argname="argument provisioned_product_name", value=provisioned_product_name, expected_type=type_hints["provisioned_product_name"])
            check_type(argname="argument provisioning_artifact_id", value=provisioning_artifact_id, expected_type=type_hints["provisioning_artifact_id"])
            check_type(argname="argument provisioning_artifact_name", value=provisioning_artifact_name, expected_type=type_hints["provisioning_artifact_name"])
            check_type(argname="argument provisioning_parameters", value=provisioning_parameters, expected_type=type_hints["provisioning_parameters"])
            check_type(argname="argument provisioning_preferences", value=provisioning_preferences, expected_type=type_hints["provisioning_preferences"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if path_id is not None:
            self._values["path_id"] = path_id
        if path_name is not None:
            self._values["path_name"] = path_name
        if product_id is not None:
            self._values["product_id"] = product_id
        if product_name is not None:
            self._values["product_name"] = product_name
        if provisioned_product_name is not None:
            self._values["provisioned_product_name"] = provisioned_product_name
        if provisioning_artifact_id is not None:
            self._values["provisioning_artifact_id"] = provisioning_artifact_id
        if provisioning_artifact_name is not None:
            self._values["provisioning_artifact_name"] = provisioning_artifact_name
        if provisioning_parameters is not None:
            self._values["provisioning_parameters"] = provisioning_parameters
        if provisioning_preferences is not None:
            self._values["provisioning_preferences"] = provisioning_preferences
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Passed to AWS CloudFormation .

        The SNS topic ARNs to which to publish stack-related events.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-notificationarns
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def path_id(self) -> typing.Optional[builtins.str]:
        '''The path identifier of the product.

        This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ .
        .. epigraph::

           You must provide the name or ID, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-pathid
        '''
        result = self._values.get("path_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_name(self) -> typing.Optional[builtins.str]:
        '''The name of the path.

        This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ .
        .. epigraph::

           You must provide the name or ID, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-pathname
        '''
        result = self._values.get("path_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product identifier.

        .. epigraph::

           You must specify either the ID or the name of the product, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-productid
        '''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly name for the provisioned product.

        This value must be unique for the AWS account and cannot be updated after the product is provisioned.

        Each time a stack is created or updated, if ``ProductName`` is provided it will successfully resolve to ``ProductId`` as long as only one product exists in the account or Region with that ``ProductName`` .
        .. epigraph::

           You must specify either the name or the ID of the product, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-productname
        '''
        result = self._values.get("product_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_product_name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly name for the provisioned product.

        This value must be unique for the AWS account and cannot be updated after the product is provisioned.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisionedproductname
        '''
        result = self._values.get("provisioned_product_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_artifact_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the provisioning artifact (also known as a version).

        .. epigraph::

           You must specify either the ID or the name of the provisioning artifact, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningartifactid
        '''
        result = self._values.get("provisioning_artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_artifact_name(self) -> typing.Optional[builtins.str]:
        '''The name of the provisioning artifact (also known as a version) for the product.

        This name must be unique for the product.
        .. epigraph::

           You must specify either the name or the ID of the provisioning artifact, but not both. You must also specify either the name or the ID of the product, but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningartifactname
        '''
        result = self._values.get("provisioning_artifact_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty, _IResolvable_a771d0ef]]]]:
        '''Parameters specified by the administrator that are required for provisioning the product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningparameters
        '''
        result = self._values.get("provisioning_parameters")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def provisioning_preferences(
        self,
    ) -> typing.Optional[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty, _IResolvable_a771d0ef]]:
        '''StackSet preferences that are required for provisioning the product or updating a provisioned product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences
        '''
        result = self._values.get("provisioning_preferences")
        return typing.cast(typing.Optional[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''One or more tags.

        .. epigraph::

           Requires the provisioned product to have an `ResourceUpdateConstraint <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html>`_ resource with ``TagUpdatesOnProvisionedProduct`` set to ``ALLOWED`` to allow tag updates. If ``RESOURCE_UPDATE`` constraint is not present, tags updates are ignored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCloudFormationProvisionedProductProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLaunchNotificationConstraint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnLaunchNotificationConstraint",
):
    '''A CloudFormation ``AWS::ServiceCatalog::LaunchNotificationConstraint``.

    Specifies a notification constraint.

    :cloudformationResource: AWS::ServiceCatalog::LaunchNotificationConstraint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_launch_notification_constraint = servicecatalog.CfnLaunchNotificationConstraint(self, "MyCfnLaunchNotificationConstraint",
            notification_arns=["notificationArns"],
            portfolio_id="portfolioId",
            product_id="productId",
        
            # the properties below are optional
            accept_language="acceptLanguage",
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        notification_arns: typing.Sequence[builtins.str],
        portfolio_id: builtins.str,
        product_id: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::LaunchNotificationConstraint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param notification_arns: The notification ARNs.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536950d77e09c8d6b305a53d8cbfea275535b25572087dca563e95d37b9310dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLaunchNotificationConstraintProps(
            notification_arns=notification_arns,
            portfolio_id=portfolio_id,
            product_id=product_id,
            accept_language=accept_language,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7fb9aa8135ecbe5a18780164e4c20f57928b860b2ff5837978995b63187471)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b926cb591c6ea74154daadf733e5f61a552829ba7a6d0740f8abd0a835adf73f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.List[builtins.str]:
        '''The notification ARNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-notificationarns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notificationArns"))

    @notification_arns.setter
    def notification_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82aa67d98dabc54f3e69e96d580aa1e07ea11764169e1ac1af9b8063ce40d92f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationArns", value)

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-portfolioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))

    @portfolio_id.setter
    def portfolio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__087b604954b3203787d894de82c10ee243af370e7491788ac12913c9db57ae5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portfolioId", value)

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-productid
        '''
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01292e2dd81e21d9c04fef071430746156ec4169f4c6f78725df409a9489e416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe0941a42f3afdee20524cecf1f3be46c4eb5ca2a5c63705faab1325f7b554e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__753b38e923b3c20baf477587a5b38887ecfef4daa75a78badecf051d96c8c4a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnLaunchNotificationConstraintProps",
    jsii_struct_bases=[],
    name_mapping={
        "notification_arns": "notificationArns",
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "accept_language": "acceptLanguage",
        "description": "description",
    },
)
class CfnLaunchNotificationConstraintProps:
    def __init__(
        self,
        *,
        notification_arns: typing.Sequence[builtins.str],
        portfolio_id: builtins.str,
        product_id: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLaunchNotificationConstraint``.

        :param notification_arns: The notification ARNs.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_launch_notification_constraint_props = servicecatalog.CfnLaunchNotificationConstraintProps(
                notification_arns=["notificationArns"],
                portfolio_id="portfolioId",
                product_id="productId",
            
                # the properties below are optional
                accept_language="acceptLanguage",
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944a6e12125ce8626b0c3ad98aba051689e1c03e22b22e48719e6dfc31f414c6)
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notification_arns": notification_arns,
            "portfolio_id": portfolio_id,
            "product_id": product_id,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def notification_arns(self) -> typing.List[builtins.str]:
        '''The notification ARNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-notificationarns
        '''
        result = self._values.get("notification_arns")
        assert result is not None, "Required property 'notification_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-portfolioid
        '''
        result = self._values.get("portfolio_id")
        assert result is not None, "Required property 'portfolio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-productid
        '''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchNotificationConstraintProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLaunchRoleConstraint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnLaunchRoleConstraint",
):
    '''A CloudFormation ``AWS::ServiceCatalog::LaunchRoleConstraint``.

    Specifies a launch constraint.

    :cloudformationResource: AWS::ServiceCatalog::LaunchRoleConstraint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_launch_role_constraint = servicecatalog.CfnLaunchRoleConstraint(self, "MyCfnLaunchRoleConstraint",
            portfolio_id="portfolioId",
            product_id="productId",
        
            # the properties below are optional
            accept_language="acceptLanguage",
            description="description",
            local_role_name="localRoleName",
            role_arn="roleArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        portfolio_id: builtins.str,
        product_id: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        local_role_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::LaunchRoleConstraint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.
        :param local_role_name: You are required to specify either the ``RoleArn`` or the ``LocalRoleName`` but can't use both. If you specify the ``LocalRoleName`` property, when an account uses the launch constraint, the IAM role with that name in the account will be used. This allows launch-role constraints to be account-agnostic so the administrator can create fewer resources per shared account. The given role name must exist in the account used to create the launch constraint and the account of the user who launches a product with this launch constraint.
        :param role_arn: The ARN of the launch role. You are required to specify ``RoleArn`` or ``LocalRoleName`` but can't use both.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05474fb990f6c00862dbea2a1bc3f7641413d61ce3b1b0bafcd78717df1a0866)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLaunchRoleConstraintProps(
            portfolio_id=portfolio_id,
            product_id=product_id,
            accept_language=accept_language,
            description=description,
            local_role_name=local_role_name,
            role_arn=role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cf4878028c39be0daca339199b9eda3392900fca6861245efdcf4c8d721e85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67fe07ce0cae03c8be07819826ee43978161b0fad0405580385e3eb1aff449a1)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-portfolioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))

    @portfolio_id.setter
    def portfolio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fde64297da69793d9f3012c057879745f5fdf36645939644f496b23aa12d9e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portfolioId", value)

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-productid
        '''
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf1a778ddc0356546011a8781117a0c2fad00467445f8d262ba7a0f16853d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b831588e1ef45448e176e4f54386fd80016739da617bc77ce177b18a2c3dd75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__724fab7f84c64c90ed0ced8bff0755619f3c7ba2d812d403377cb3348d17e0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="localRoleName")
    def local_role_name(self) -> typing.Optional[builtins.str]:
        '''You are required to specify either the ``RoleArn`` or the ``LocalRoleName`` but can't use both.

        If you specify the ``LocalRoleName`` property, when an account uses the launch constraint, the IAM role with that name in the account will be used. This allows launch-role constraints to be account-agnostic so the administrator can create fewer resources per shared account.

        The given role name must exist in the account used to create the launch constraint and the account of the user who launches a product with this launch constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-localrolename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localRoleName"))

    @local_role_name.setter
    def local_role_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9be6ebc03ea1089221c54d9e3cd24e8271b4d641e75e07ae7dd902f4d3ba0209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localRoleName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the launch role.

        You are required to specify ``RoleArn`` or ``LocalRoleName`` but can't use both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96fefa847437c7d256b8544ccb7bff368bc24fcfae7553d4353fa9417bb0bd6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnLaunchRoleConstraintProps",
    jsii_struct_bases=[],
    name_mapping={
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "accept_language": "acceptLanguage",
        "description": "description",
        "local_role_name": "localRoleName",
        "role_arn": "roleArn",
    },
)
class CfnLaunchRoleConstraintProps:
    def __init__(
        self,
        *,
        portfolio_id: builtins.str,
        product_id: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        local_role_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLaunchRoleConstraint``.

        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.
        :param local_role_name: You are required to specify either the ``RoleArn`` or the ``LocalRoleName`` but can't use both. If you specify the ``LocalRoleName`` property, when an account uses the launch constraint, the IAM role with that name in the account will be used. This allows launch-role constraints to be account-agnostic so the administrator can create fewer resources per shared account. The given role name must exist in the account used to create the launch constraint and the account of the user who launches a product with this launch constraint.
        :param role_arn: The ARN of the launch role. You are required to specify ``RoleArn`` or ``LocalRoleName`` but can't use both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_launch_role_constraint_props = servicecatalog.CfnLaunchRoleConstraintProps(
                portfolio_id="portfolioId",
                product_id="productId",
            
                # the properties below are optional
                accept_language="acceptLanguage",
                description="description",
                local_role_name="localRoleName",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c8372b1b8f9f069fa8ddf6cc2e753a8d4de263c1e160495123c44d364a3cd1)
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument local_role_name", value=local_role_name, expected_type=type_hints["local_role_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "portfolio_id": portfolio_id,
            "product_id": product_id,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description
        if local_role_name is not None:
            self._values["local_role_name"] = local_role_name
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-portfolioid
        '''
        result = self._values.get("portfolio_id")
        assert result is not None, "Required property 'portfolio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-productid
        '''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_role_name(self) -> typing.Optional[builtins.str]:
        '''You are required to specify either the ``RoleArn`` or the ``LocalRoleName`` but can't use both.

        If you specify the ``LocalRoleName`` property, when an account uses the launch constraint, the IAM role with that name in the account will be used. This allows launch-role constraints to be account-agnostic so the administrator can create fewer resources per shared account.

        The given role name must exist in the account used to create the launch constraint and the account of the user who launches a product with this launch constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-localrolename
        '''
        result = self._values.get("local_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the launch role.

        You are required to specify ``RoleArn`` or ``LocalRoleName`` but can't use both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchRoleConstraintProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLaunchTemplateConstraint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnLaunchTemplateConstraint",
):
    '''A CloudFormation ``AWS::ServiceCatalog::LaunchTemplateConstraint``.

    Specifies a template constraint.

    :cloudformationResource: AWS::ServiceCatalog::LaunchTemplateConstraint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_launch_template_constraint = servicecatalog.CfnLaunchTemplateConstraint(self, "MyCfnLaunchTemplateConstraint",
            portfolio_id="portfolioId",
            product_id="productId",
            rules="rules",
        
            # the properties below are optional
            accept_language="acceptLanguage",
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        portfolio_id: builtins.str,
        product_id: builtins.str,
        rules: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::LaunchTemplateConstraint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param rules: The constraint rules.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c000292e2b24b6a46f364a1914cc442c300264ea81691c2b2019e4dc000a11aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLaunchTemplateConstraintProps(
            portfolio_id=portfolio_id,
            product_id=product_id,
            rules=rules,
            accept_language=accept_language,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6b6d9a86db133245acfab3bd54867c70ae6896664bda05c66b97b54779b149)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa443fd16f071f5c43562d815f0808a0078ae98db79ce13aa81074c95b91df51)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-portfolioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))

    @portfolio_id.setter
    def portfolio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547fd0d7074d8a3a4cf84b071d2532b6abd79faba6bacfb5d78c3aaafb452bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portfolioId", value)

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-productid
        '''
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fdeeced9857ebc0143d5ebb501ceddd6891df4f21de4b8ffea9e94c3c34d3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value)

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> builtins.str:
        '''The constraint rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-rules
        '''
        return typing.cast(builtins.str, jsii.get(self, "rules"))

    @rules.setter
    def rules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c0067043fe338491f6c0a55df24a5671321eb9e0eace62dc8c94f4425320e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rules", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f5912cbcc72d1e588166d7d20b6b646174a26b888dde629a62d6634d368cc28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35fc69cd0430b3984b7a86136781941489a5745760cf50ab9276207893f3c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnLaunchTemplateConstraintProps",
    jsii_struct_bases=[],
    name_mapping={
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "rules": "rules",
        "accept_language": "acceptLanguage",
        "description": "description",
    },
)
class CfnLaunchTemplateConstraintProps:
    def __init__(
        self,
        *,
        portfolio_id: builtins.str,
        product_id: builtins.str,
        rules: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLaunchTemplateConstraint``.

        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param rules: The constraint rules.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_launch_template_constraint_props = servicecatalog.CfnLaunchTemplateConstraintProps(
                portfolio_id="portfolioId",
                product_id="productId",
                rules="rules",
            
                # the properties below are optional
                accept_language="acceptLanguage",
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ab40a16c7614d726a380d127488d83123103eb5866c9f819c0891692a4a427)
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "portfolio_id": portfolio_id,
            "product_id": product_id,
            "rules": rules,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-portfolioid
        '''
        result = self._values.get("portfolio_id")
        assert result is not None, "Required property 'portfolio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-productid
        '''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(self) -> builtins.str:
        '''The constraint rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-rules
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchTemplateConstraintProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPortfolio(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnPortfolio",
):
    '''A CloudFormation ``AWS::ServiceCatalog::Portfolio``.

    Specifies a portfolio.

    :cloudformationResource: AWS::ServiceCatalog::Portfolio
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_portfolio = servicecatalog.CfnPortfolio(self, "MyCfnPortfolio",
            display_name="displayName",
            provider_name="providerName",
        
            # the properties below are optional
            accept_language="acceptLanguage",
            description="description",
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
        display_name: builtins.str,
        provider_name: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::Portfolio``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param display_name: The name to use for display purposes.
        :param provider_name: The name of the portfolio provider.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the portfolio.
        :param tags: One or more tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d37a11b9127d74d008e969f20eea44cec91241a8c8e801e91effd5264b9dc1c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPortfolioProps(
            display_name=display_name,
            provider_name=provider_name,
            accept_language=accept_language,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d42533342281f403893516e3e4684d779fdb1c62dc9018b859a2526f35a61c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06c365ad6284f59bb8cf4af323651fe7aa19340d3fb94fedc488895fff21255f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrPortfolioName")
    def attr_portfolio_name(self) -> builtins.str:
        '''The name of the portfolio.

        :cloudformationAttribute: PortfolioName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPortfolioName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''One or more tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        '''The name to use for display purposes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-displayname
        '''
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a2e2a6cb2a627428107a332cce31845354dff45dfa49504fe030553fc714f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        '''The name of the portfolio provider.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-providername
        '''
        return typing.cast(builtins.str, jsii.get(self, "providerName"))

    @provider_name.setter
    def provider_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aefb58d20a1045a2fdafdee143c51a6d60b1d9860c25d9dfc2c229a2716e5e76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerName", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e34fab4ec83942117254e7b2dbb6c6a3a18e90c4eb8cf5e37b33d6d5e1e8ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the portfolio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2256828f6c1b69e94fa0c961db073c0ecae0b7140f4ff6c2011f77b1da676d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnPortfolioPrincipalAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnPortfolioPrincipalAssociation",
):
    '''A CloudFormation ``AWS::ServiceCatalog::PortfolioPrincipalAssociation``.

    Associates the specified principal ARN with the specified portfolio.

    If you share the portfolio with principal name sharing enabled, the ``PrincipalARN`` association is included in the share.

    The ``PortfolioID`` , ``PrincipalARN`` , and ``PrincipalType`` parameters are required.

    You can associate a maximum of 10 Principals with a portfolio using ``PrincipalType`` as ``IAM_PATTERN``
    .. epigraph::

       When you associate a principal with portfolio, a potential privilege escalation path may occur when that portfolio is then shared with other accounts. For a user in a recipient account who is *not* an AWS Service Catalog Admin, but still has the ability to create Principals (Users/Groups/Roles), that user could create a role that matches a principal name association for the portfolio. Although this user may not know which principal names are associated through AWS Service Catalog , they may be able to guess the user. If this potential escalation path is a concern, then AWS Service Catalog recommends using ``PrincipalType`` as ``IAM`` . With this configuration, the ``PrincipalARN`` must already exist in the recipient account before it can be associated.

    :cloudformationResource: AWS::ServiceCatalog::PortfolioPrincipalAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_portfolio_principal_association = servicecatalog.CfnPortfolioPrincipalAssociation(self, "MyCfnPortfolioPrincipalAssociation",
            portfolio_id="portfolioId",
            principal_arn="principalArn",
            principal_type="principalType",
        
            # the properties below are optional
            accept_language="acceptLanguage"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        portfolio_id: builtins.str,
        principal_arn: builtins.str,
        principal_type: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::PortfolioPrincipalAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param portfolio_id: The portfolio identifier.
        :param principal_arn: The ARN of the principal (IAM user, role, or group). This field allows an ARN with no ``accountID`` if ``PrincipalType`` is ``IAM_PATTERN`` . You can associate multiple ``IAM`` patterns even if the account has no principal with that name. This is useful in Principal Name Sharing if you want to share a principal without creating it in the account that owns the portfolio.
        :param principal_type: The principal type. The supported value is ``IAM`` if you use a fully defined ARN, or ``IAM_PATTERN`` if you use an ARN with no ``accountID`` .
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1badb8b93aebd4e7bd7c4ec52efd4a76e94eb4bbf9f1a1e06464cd0164385a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPortfolioPrincipalAssociationProps(
            portfolio_id=portfolio_id,
            principal_arn=principal_arn,
            principal_type=principal_type,
            accept_language=accept_language,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f9a65d802deb12803710648a5c02c798b42b9fc9a05cc48c3929e286eca45d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__715dd6496700390bd3a26156b82fd2ec669ef7fe550a5cf87d0737e9c30fceb7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-portfolioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))

    @portfolio_id.setter
    def portfolio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb14c43a4f6e5a507eaf39642305c31306b1008cea413e92a47a937b4c4594a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portfolioId", value)

    @builtins.property
    @jsii.member(jsii_name="principalArn")
    def principal_arn(self) -> builtins.str:
        '''The ARN of the principal (IAM user, role, or group).

        This field allows an ARN with no ``accountID`` if ``PrincipalType`` is ``IAM_PATTERN`` .

        You can associate multiple ``IAM`` patterns even if the account has no principal with that name. This is useful in Principal Name Sharing if you want to share a principal without creating it in the account that owns the portfolio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-principalarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "principalArn"))

    @principal_arn.setter
    def principal_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74be550dd3f924e09496a876da171df1056d214f55356d34df43bf40a2a4e095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalArn", value)

    @builtins.property
    @jsii.member(jsii_name="principalType")
    def principal_type(self) -> builtins.str:
        '''The principal type.

        The supported value is ``IAM`` if you use a fully defined ARN, or ``IAM_PATTERN`` if you use an ARN with no ``accountID`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-principaltype
        '''
        return typing.cast(builtins.str, jsii.get(self, "principalType"))

    @principal_type.setter
    def principal_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec49b4e446dcf7bd2ed7caeb4b80984501357025ca4d4e43fba8ebce3055c4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principalType", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02df720192a545192ae25318764c92213dd491a228e08ac7fd0a68a0819354c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnPortfolioPrincipalAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "portfolio_id": "portfolioId",
        "principal_arn": "principalArn",
        "principal_type": "principalType",
        "accept_language": "acceptLanguage",
    },
)
class CfnPortfolioPrincipalAssociationProps:
    def __init__(
        self,
        *,
        portfolio_id: builtins.str,
        principal_arn: builtins.str,
        principal_type: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPortfolioPrincipalAssociation``.

        :param portfolio_id: The portfolio identifier.
        :param principal_arn: The ARN of the principal (IAM user, role, or group). This field allows an ARN with no ``accountID`` if ``PrincipalType`` is ``IAM_PATTERN`` . You can associate multiple ``IAM`` patterns even if the account has no principal with that name. This is useful in Principal Name Sharing if you want to share a principal without creating it in the account that owns the portfolio.
        :param principal_type: The principal type. The supported value is ``IAM`` if you use a fully defined ARN, or ``IAM_PATTERN`` if you use an ARN with no ``accountID`` .
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_portfolio_principal_association_props = servicecatalog.CfnPortfolioPrincipalAssociationProps(
                portfolio_id="portfolioId",
                principal_arn="principalArn",
                principal_type="principalType",
            
                # the properties below are optional
                accept_language="acceptLanguage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b746d64f4b431c05582088f413f1fe0214bc5d94d42cd25b180beb911c8b01dd)
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument principal_arn", value=principal_arn, expected_type=type_hints["principal_arn"])
            check_type(argname="argument principal_type", value=principal_type, expected_type=type_hints["principal_type"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "portfolio_id": portfolio_id,
            "principal_arn": principal_arn,
            "principal_type": principal_type,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language

    @builtins.property
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-portfolioid
        '''
        result = self._values.get("portfolio_id")
        assert result is not None, "Required property 'portfolio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal_arn(self) -> builtins.str:
        '''The ARN of the principal (IAM user, role, or group).

        This field allows an ARN with no ``accountID`` if ``PrincipalType`` is ``IAM_PATTERN`` .

        You can associate multiple ``IAM`` patterns even if the account has no principal with that name. This is useful in Principal Name Sharing if you want to share a principal without creating it in the account that owns the portfolio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-principalarn
        '''
        result = self._values.get("principal_arn")
        assert result is not None, "Required property 'principal_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def principal_type(self) -> builtins.str:
        '''The principal type.

        The supported value is ``IAM`` if you use a fully defined ARN, or ``IAM_PATTERN`` if you use an ARN with no ``accountID`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-principaltype
        '''
        result = self._values.get("principal_type")
        assert result is not None, "Required property 'principal_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortfolioPrincipalAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPortfolioProductAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnPortfolioProductAssociation",
):
    '''A CloudFormation ``AWS::ServiceCatalog::PortfolioProductAssociation``.

    Associates the specified product with the specified portfolio.

    A delegated admin is authorized to invoke this command.

    :cloudformationResource: AWS::ServiceCatalog::PortfolioProductAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_portfolio_product_association = servicecatalog.CfnPortfolioProductAssociation(self, "MyCfnPortfolioProductAssociation",
            portfolio_id="portfolioId",
            product_id="productId",
        
            # the properties below are optional
            accept_language="acceptLanguage",
            source_portfolio_id="sourcePortfolioId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        portfolio_id: builtins.str,
        product_id: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        source_portfolio_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::PortfolioProductAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param source_portfolio_id: The identifier of the source portfolio.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa08d7fc1d2dcbb13e794462f72361998bde7254193599c9cfcf138ab56197dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPortfolioProductAssociationProps(
            portfolio_id=portfolio_id,
            product_id=product_id,
            accept_language=accept_language,
            source_portfolio_id=source_portfolio_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4e566706318c289f939fa97d0a5642393bb12a0349e51b3d45592022cbaa09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29420bfb225760a406de0eb2840a36ac5df116fa371f460637bf0193f25bc7b4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-portfolioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))

    @portfolio_id.setter
    def portfolio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d058c54f8f9f665f65d2bd5b011578cc3548bf36f9d6c08aec04f33b052f629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portfolioId", value)

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-productid
        '''
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16e6d44f7b7d755f53fb09d665ed549dd3b92036bb438e636dab31136bf18b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61db5eeb19c2ada6dd48081c34e81cf1127bc7079e4ade7b74999f18dbd8bead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="sourcePortfolioId")
    def source_portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the source portfolio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-sourceportfolioid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourcePortfolioId"))

    @source_portfolio_id.setter
    def source_portfolio_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398214301ea0f6e5131e1d62c63a28d6a052a448cb1ada36486413678fe04139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcePortfolioId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnPortfolioProductAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "accept_language": "acceptLanguage",
        "source_portfolio_id": "sourcePortfolioId",
    },
)
class CfnPortfolioProductAssociationProps:
    def __init__(
        self,
        *,
        portfolio_id: builtins.str,
        product_id: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        source_portfolio_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPortfolioProductAssociation``.

        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param source_portfolio_id: The identifier of the source portfolio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_portfolio_product_association_props = servicecatalog.CfnPortfolioProductAssociationProps(
                portfolio_id="portfolioId",
                product_id="productId",
            
                # the properties below are optional
                accept_language="acceptLanguage",
                source_portfolio_id="sourcePortfolioId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06fa922bb2fafdf69c6cc3c50ef7e2f1c6f72e5ec950bb7b0c5b79b93477235b)
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument source_portfolio_id", value=source_portfolio_id, expected_type=type_hints["source_portfolio_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "portfolio_id": portfolio_id,
            "product_id": product_id,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if source_portfolio_id is not None:
            self._values["source_portfolio_id"] = source_portfolio_id

    @builtins.property
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-portfolioid
        '''
        result = self._values.get("portfolio_id")
        assert result is not None, "Required property 'portfolio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-productid
        '''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the source portfolio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-sourceportfolioid
        '''
        result = self._values.get("source_portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortfolioProductAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnPortfolioProps",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "provider_name": "providerName",
        "accept_language": "acceptLanguage",
        "description": "description",
        "tags": "tags",
    },
)
class CfnPortfolioProps:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        provider_name: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPortfolio``.

        :param display_name: The name to use for display purposes.
        :param provider_name: The name of the portfolio provider.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the portfolio.
        :param tags: One or more tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_portfolio_props = servicecatalog.CfnPortfolioProps(
                display_name="displayName",
                provider_name="providerName",
            
                # the properties below are optional
                accept_language="acceptLanguage",
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f21ac5a461a8f8745b78871c28703eab5a1f377797b2b9e07901b97eecf944)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "provider_name": provider_name,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The name to use for display purposes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-displayname
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_name(self) -> builtins.str:
        '''The name of the portfolio provider.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-providername
        '''
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the portfolio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''One or more tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortfolioProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPortfolioShare(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnPortfolioShare",
):
    '''A CloudFormation ``AWS::ServiceCatalog::PortfolioShare``.

    Shares the specified portfolio with the specified account.

    :cloudformationResource: AWS::ServiceCatalog::PortfolioShare
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_portfolio_share = servicecatalog.CfnPortfolioShare(self, "MyCfnPortfolioShare",
            account_id="accountId",
            portfolio_id="portfolioId",
        
            # the properties below are optional
            accept_language="acceptLanguage",
            share_tag_options=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        account_id: builtins.str,
        portfolio_id: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        share_tag_options: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::PortfolioShare``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_id: The AWS account ID. For example, ``123456789012`` .
        :param portfolio_id: The portfolio identifier.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param share_tag_options: Indicates whether TagOptions sharing is enabled or disabled for the portfolio share.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0037fe68380000e31dd0e10d0d0a03c7157f49c7758bfd556a2d921739783ee5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPortfolioShareProps(
            account_id=account_id,
            portfolio_id=portfolio_id,
            accept_language=accept_language,
            share_tag_options=share_tag_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217e2be7179854152fc979402390a792ec64635700831fbd73c47cbff68056ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f11922ffa82c9a056bbe13f3100ff9ad654982867f72d675ddd9b88862f1847)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        '''The AWS account ID.

        For example, ``123456789012`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-accountid
        '''
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a8c7413cfb24a2e5ca0d96930f48974ef9aabfbd93907bce9b85f29db0ead4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-portfolioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))

    @portfolio_id.setter
    def portfolio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0daa77a66cbe5ba7ddedc04ac46f2660cefaaf04366c9fe2e8d79a38527893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portfolioId", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20ea98fc22fee61257435182ab11e6e24ebbef57fc91b69dbad873d54a78b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="shareTagOptions")
    def share_tag_options(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether TagOptions sharing is enabled or disabled for the portfolio share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-sharetagoptions
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "shareTagOptions"))

    @share_tag_options.setter
    def share_tag_options(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c93238824888a8a207df23d909c6619e27c543b02375de19aae5521d2b5c55f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareTagOptions", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnPortfolioShareProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "portfolio_id": "portfolioId",
        "accept_language": "acceptLanguage",
        "share_tag_options": "shareTagOptions",
    },
)
class CfnPortfolioShareProps:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        portfolio_id: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        share_tag_options: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPortfolioShare``.

        :param account_id: The AWS account ID. For example, ``123456789012`` .
        :param portfolio_id: The portfolio identifier.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param share_tag_options: Indicates whether TagOptions sharing is enabled or disabled for the portfolio share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_portfolio_share_props = servicecatalog.CfnPortfolioShareProps(
                account_id="accountId",
                portfolio_id="portfolioId",
            
                # the properties below are optional
                accept_language="acceptLanguage",
                share_tag_options=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a2e151cd846989e98a12c172a20f55522edb38e50dbeb4fd9ef8ffa5c8bcd7)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument share_tag_options", value=share_tag_options, expected_type=type_hints["share_tag_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "portfolio_id": portfolio_id,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if share_tag_options is not None:
            self._values["share_tag_options"] = share_tag_options

    @builtins.property
    def account_id(self) -> builtins.str:
        '''The AWS account ID.

        For example, ``123456789012`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-accountid
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-portfolioid
        '''
        result = self._values.get("portfolio_id")
        assert result is not None, "Required property 'portfolio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_tag_options(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether TagOptions sharing is enabled or disabled for the portfolio share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-sharetagoptions
        '''
        result = self._values.get("share_tag_options")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortfolioShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResourceUpdateConstraint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnResourceUpdateConstraint",
):
    '''A CloudFormation ``AWS::ServiceCatalog::ResourceUpdateConstraint``.

    Specifies a ``RESOURCE_UPDATE`` constraint.

    :cloudformationResource: AWS::ServiceCatalog::ResourceUpdateConstraint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_resource_update_constraint = servicecatalog.CfnResourceUpdateConstraint(self, "MyCfnResourceUpdateConstraint",
            portfolio_id="portfolioId",
            product_id="productId",
            tag_update_on_provisioned_product="tagUpdateOnProvisionedProduct",
        
            # the properties below are optional
            accept_language="acceptLanguage",
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        portfolio_id: builtins.str,
        product_id: builtins.str,
        tag_update_on_provisioned_product: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::ResourceUpdateConstraint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param tag_update_on_provisioned_product: If set to ``ALLOWED`` , lets users change tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource. If set to ``NOT_ALLOWED`` , prevents users from changing tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8e6158705a78f206429684c920f37b0dbf6052c1f9718d0eb64b9805f36590a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceUpdateConstraintProps(
            portfolio_id=portfolio_id,
            product_id=product_id,
            tag_update_on_provisioned_product=tag_update_on_provisioned_product,
            accept_language=accept_language,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0f56c32700892ddafb4ee8a148540f156341594d7aab50e99646e179dd34fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fa5fc9999ca2e23b38cfbd12cb69d8871659fef8119452ddf32c11433cca7df)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-portfolioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))

    @portfolio_id.setter
    def portfolio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db1d6ee955c9f11c9320451431e45e2514a3a55c901dfe4769139a99b7e28ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portfolioId", value)

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-productid
        '''
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e20a17ece5fe0bf2be1d46c102f023c8a459cd13aad9c24e5148cc601346948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value)

    @builtins.property
    @jsii.member(jsii_name="tagUpdateOnProvisionedProduct")
    def tag_update_on_provisioned_product(self) -> builtins.str:
        '''If set to ``ALLOWED`` , lets users change tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource.

        If set to ``NOT_ALLOWED`` , prevents users from changing tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-tagupdateonprovisionedproduct
        '''
        return typing.cast(builtins.str, jsii.get(self, "tagUpdateOnProvisionedProduct"))

    @tag_update_on_provisioned_product.setter
    def tag_update_on_provisioned_product(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ac28643a3e86add7678f137c5035ffc535b6d59f0cdcb976824ba76fa51646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagUpdateOnProvisionedProduct", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16150eb7325e26ebbe9edc0272ef11ae36d30132fcb8b7c408573cd13abc744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1542e426cf2609bfbbda2c53a397fd7b952616b2d10feea1f77a238967f6ded4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnResourceUpdateConstraintProps",
    jsii_struct_bases=[],
    name_mapping={
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "tag_update_on_provisioned_product": "tagUpdateOnProvisionedProduct",
        "accept_language": "acceptLanguage",
        "description": "description",
    },
)
class CfnResourceUpdateConstraintProps:
    def __init__(
        self,
        *,
        portfolio_id: builtins.str,
        product_id: builtins.str,
        tag_update_on_provisioned_product: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnResourceUpdateConstraint``.

        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param tag_update_on_provisioned_product: If set to ``ALLOWED`` , lets users change tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource. If set to ``NOT_ALLOWED`` , prevents users from changing tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_resource_update_constraint_props = servicecatalog.CfnResourceUpdateConstraintProps(
                portfolio_id="portfolioId",
                product_id="productId",
                tag_update_on_provisioned_product="tagUpdateOnProvisionedProduct",
            
                # the properties below are optional
                accept_language="acceptLanguage",
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af61d79ae3ba512a69bd69176ec8fc3b61af69ee93fe2b05bfca75bdb1b73ee2)
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument tag_update_on_provisioned_product", value=tag_update_on_provisioned_product, expected_type=type_hints["tag_update_on_provisioned_product"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "portfolio_id": portfolio_id,
            "product_id": product_id,
            "tag_update_on_provisioned_product": tag_update_on_provisioned_product,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-portfolioid
        '''
        result = self._values.get("portfolio_id")
        assert result is not None, "Required property 'portfolio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-productid
        '''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_update_on_provisioned_product(self) -> builtins.str:
        '''If set to ``ALLOWED`` , lets users change tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource.

        If set to ``NOT_ALLOWED`` , prevents users from changing tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-tagupdateonprovisionedproduct
        '''
        result = self._values.get("tag_update_on_provisioned_product")
        assert result is not None, "Required property 'tag_update_on_provisioned_product' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceUpdateConstraintProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnServiceAction(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnServiceAction",
):
    '''A CloudFormation ``AWS::ServiceCatalog::ServiceAction``.

    Creates a self-service action.

    :cloudformationResource: AWS::ServiceCatalog::ServiceAction
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_service_action = servicecatalog.CfnServiceAction(self, "MyCfnServiceAction",
            definition=[servicecatalog.CfnServiceAction.DefinitionParameterProperty(
                key="key",
                value="value"
            )],
            definition_type="definitionType",
            name="name",
        
            # the properties below are optional
            accept_language="acceptLanguage",
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        definition: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnServiceAction.DefinitionParameterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        definition_type: builtins.str,
        name: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::ServiceAction``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param definition: A map that defines the self-service action.
        :param definition_type: The self-service action definition type. For example, ``SSM_AUTOMATION`` .
        :param name: The self-service action name.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The self-service action description.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf8be5b8ba333f2436f119d0f45c48ba97103f215d2ea4a68dbc32bd9e11cbb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceActionProps(
            definition=definition,
            definition_type=definition_type,
            name=name,
            accept_language=accept_language,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80abf54b60353986671baa97c7fd85893e88c0f2f1f9dee5d48d50c9f5c8f95e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc2a8976aef07498ac0135f199a9c4bd3870aedc8bc7b6a3ca13c4634366157c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The self-service action identifier.

        For example, ``act-fs7abcd89wxyz`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnServiceAction.DefinitionParameterProperty", _IResolvable_a771d0ef]]]:
        '''A map that defines the self-service action.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-definition
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnServiceAction.DefinitionParameterProperty", _IResolvable_a771d0ef]]], jsii.get(self, "definition"))

    @definition.setter
    def definition(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnServiceAction.DefinitionParameterProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b3fcea1911c803c6266707e4e2b01fd6ef977ec5153518ed46e2d93c0e8ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value)

    @builtins.property
    @jsii.member(jsii_name="definitionType")
    def definition_type(self) -> builtins.str:
        '''The self-service action definition type.

        For example, ``SSM_AUTOMATION`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-definitiontype
        '''
        return typing.cast(builtins.str, jsii.get(self, "definitionType"))

    @definition_type.setter
    def definition_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5f81e9c5829266b0517e5715fa9c224a84df07e53e95df2b5fcb6ee85a3573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The self-service action name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a57005347b85d83abd6ee49918068bbbc0099724de48bb013c724a51f2bf79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d25096bae88fa61ff09ade07169f322e20d6e560fb41a599d72c1bd136ed8e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The self-service action description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f35cf81f8b0205bfa795f16bd4c5d272496f43b05bc0b6e78d0c003ada1b829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_servicecatalog.CfnServiceAction.DefinitionParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class DefinitionParameterProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''The list of parameters in JSON format.

            For example: ``[{\\"Name\\":\\"InstanceId\\",\\"Type\\":\\"TARGET\\"}] or [{\\"Name\\":\\"InstanceId\\",\\"Type\\":\\"TEXT_VALUE\\"}]`` .

            :param key: The parameter key.
            :param value: The value of the parameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-serviceaction-definitionparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_servicecatalog as servicecatalog
                
                definition_parameter_property = servicecatalog.CfnServiceAction.DefinitionParameterProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92929363008293a458cfbdca39df3247b6894a8c7f81f4295fe98333efa8fe97)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The parameter key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-serviceaction-definitionparameter.html#cfn-servicecatalog-serviceaction-definitionparameter-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value of the parameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-serviceaction-definitionparameter.html#cfn-servicecatalog-serviceaction-definitionparameter-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnServiceActionAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnServiceActionAssociation",
):
    '''A CloudFormation ``AWS::ServiceCatalog::ServiceActionAssociation``.

    A self-service action association consisting of the Action ID, the Product ID, and the Provisioning Artifact ID.

    :cloudformationResource: AWS::ServiceCatalog::ServiceActionAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_service_action_association = servicecatalog.CfnServiceActionAssociation(self, "MyCfnServiceActionAssociation",
            product_id="productId",
            provisioning_artifact_id="provisioningArtifactId",
            service_action_id="serviceActionId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        product_id: builtins.str,
        provisioning_artifact_id: builtins.str,
        service_action_id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::ServiceActionAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param product_id: The product identifier. For example, ``prod-abcdzk7xy33qa`` .
        :param provisioning_artifact_id: The identifier of the provisioning artifact. For example, ``pa-4abcdjnxjj6ne`` .
        :param service_action_id: The self-service action identifier. For example, ``act-fs7abcd89wxyz`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c2760f77e70f16e0a62b11aca2382a45f0e2ea6bb9204d1e0a791890cc976fb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceActionAssociationProps(
            product_id=product_id,
            provisioning_artifact_id=provisioning_artifact_id,
            service_action_id=service_action_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfc3ddab4eda9045a7c80cf641629541ec3c74d3fa1f989dbaf60f231d47aee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a4e15ad3233bf31d9dad33f8a1e746d572cb67a7f5f00edb8df546d8cae8acd)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''The product identifier.

        For example, ``prod-abcdzk7xy33qa`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html#cfn-servicecatalog-serviceactionassociation-productid
        '''
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2edaa252dc1e1983d48219b0493d2255176c17b02eee8738f26e0284518e09b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value)

    @builtins.property
    @jsii.member(jsii_name="provisioningArtifactId")
    def provisioning_artifact_id(self) -> builtins.str:
        '''The identifier of the provisioning artifact.

        For example, ``pa-4abcdjnxjj6ne`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html#cfn-servicecatalog-serviceactionassociation-provisioningartifactid
        '''
        return typing.cast(builtins.str, jsii.get(self, "provisioningArtifactId"))

    @provisioning_artifact_id.setter
    def provisioning_artifact_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfcead32cf03c02dfe6bdadc9e4cf5e771aa6873592569583050faa84fe240fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningArtifactId", value)

    @builtins.property
    @jsii.member(jsii_name="serviceActionId")
    def service_action_id(self) -> builtins.str:
        '''The self-service action identifier.

        For example, ``act-fs7abcd89wxyz`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html#cfn-servicecatalog-serviceactionassociation-serviceactionid
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceActionId"))

    @service_action_id.setter
    def service_action_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6780b9ef94f370a00cf41190bedc1cd2c1f8a40359531d6e3f938373d24df7b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceActionId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnServiceActionAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "product_id": "productId",
        "provisioning_artifact_id": "provisioningArtifactId",
        "service_action_id": "serviceActionId",
    },
)
class CfnServiceActionAssociationProps:
    def __init__(
        self,
        *,
        product_id: builtins.str,
        provisioning_artifact_id: builtins.str,
        service_action_id: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnServiceActionAssociation``.

        :param product_id: The product identifier. For example, ``prod-abcdzk7xy33qa`` .
        :param provisioning_artifact_id: The identifier of the provisioning artifact. For example, ``pa-4abcdjnxjj6ne`` .
        :param service_action_id: The self-service action identifier. For example, ``act-fs7abcd89wxyz`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_service_action_association_props = servicecatalog.CfnServiceActionAssociationProps(
                product_id="productId",
                provisioning_artifact_id="provisioningArtifactId",
                service_action_id="serviceActionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac0b8f611f8b9d4177f96dfffd7b911307e7001fff77e808b56c9864209b4f4)
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument provisioning_artifact_id", value=provisioning_artifact_id, expected_type=type_hints["provisioning_artifact_id"])
            check_type(argname="argument service_action_id", value=service_action_id, expected_type=type_hints["service_action_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "product_id": product_id,
            "provisioning_artifact_id": provisioning_artifact_id,
            "service_action_id": service_action_id,
        }

    @builtins.property
    def product_id(self) -> builtins.str:
        '''The product identifier.

        For example, ``prod-abcdzk7xy33qa`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html#cfn-servicecatalog-serviceactionassociation-productid
        '''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provisioning_artifact_id(self) -> builtins.str:
        '''The identifier of the provisioning artifact.

        For example, ``pa-4abcdjnxjj6ne`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html#cfn-servicecatalog-serviceactionassociation-provisioningartifactid
        '''
        result = self._values.get("provisioning_artifact_id")
        assert result is not None, "Required property 'provisioning_artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_action_id(self) -> builtins.str:
        '''The self-service action identifier.

        For example, ``act-fs7abcd89wxyz`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html#cfn-servicecatalog-serviceactionassociation-serviceactionid
        '''
        result = self._values.get("service_action_id")
        assert result is not None, "Required property 'service_action_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceActionAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnServiceActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "definition_type": "definitionType",
        "name": "name",
        "accept_language": "acceptLanguage",
        "description": "description",
    },
)
class CfnServiceActionProps:
    def __init__(
        self,
        *,
        definition: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnServiceAction.DefinitionParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        definition_type: builtins.str,
        name: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceAction``.

        :param definition: A map that defines the self-service action.
        :param definition_type: The self-service action definition type. For example, ``SSM_AUTOMATION`` .
        :param name: The self-service action name.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The self-service action description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_service_action_props = servicecatalog.CfnServiceActionProps(
                definition=[servicecatalog.CfnServiceAction.DefinitionParameterProperty(
                    key="key",
                    value="value"
                )],
                definition_type="definitionType",
                name="name",
            
                # the properties below are optional
                accept_language="acceptLanguage",
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e66e58ae63bf70496e65aa8d5c06769c460f04a4568ac60085dd7965d029854)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument definition_type", value=definition_type, expected_type=type_hints["definition_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
            "definition_type": definition_type,
            "name": name,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def definition(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnServiceAction.DefinitionParameterProperty, _IResolvable_a771d0ef]]]:
        '''A map that defines the self-service action.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-definition
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnServiceAction.DefinitionParameterProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def definition_type(self) -> builtins.str:
        '''The self-service action definition type.

        For example, ``SSM_AUTOMATION`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-definitiontype
        '''
        result = self._values.get("definition_type")
        assert result is not None, "Required property 'definition_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The self-service action name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The self-service action description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnStackSetConstraint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnStackSetConstraint",
):
    '''A CloudFormation ``AWS::ServiceCatalog::StackSetConstraint``.

    Specifies a StackSet constraint.

    :cloudformationResource: AWS::ServiceCatalog::StackSetConstraint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_stack_set_constraint = servicecatalog.CfnStackSetConstraint(self, "MyCfnStackSetConstraint",
            account_list=["accountList"],
            admin_role="adminRole",
            description="description",
            execution_role="executionRole",
            portfolio_id="portfolioId",
            product_id="productId",
            region_list=["regionList"],
            stack_instance_control="stackInstanceControl",
        
            # the properties below are optional
            accept_language="acceptLanguage"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        account_list: typing.Sequence[builtins.str],
        admin_role: builtins.str,
        description: builtins.str,
        execution_role: builtins.str,
        portfolio_id: builtins.str,
        product_id: builtins.str,
        region_list: typing.Sequence[builtins.str],
        stack_instance_control: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::StackSetConstraint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_list: One or more AWS accounts that will have access to the provisioned product.
        :param admin_role: AdminRole ARN.
        :param description: The description of the constraint.
        :param execution_role: ExecutionRole name.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param region_list: One or more AWS Regions where the provisioned product will be available. Applicable only to a ``CFN_STACKSET`` provisioned product type. The specified Regions should be within the list of Regions from the ``STACKSET`` constraint. To get the list of Regions in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation. If no values are specified, the default value is all Regions from the ``STACKSET`` constraint.
        :param stack_instance_control: Permission to create, update, and delete stack instances. Choose from ALLOWED and NOT_ALLOWED.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdf8c8d0fce64cad689104d45f34c83e06b8f7c4f098b6f5634c85151e46262)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStackSetConstraintProps(
            account_list=account_list,
            admin_role=admin_role,
            description=description,
            execution_role=execution_role,
            portfolio_id=portfolio_id,
            product_id=product_id,
            region_list=region_list,
            stack_instance_control=stack_instance_control,
            accept_language=accept_language,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ebf471413b4dda09e27e8789910307f6b3f3e02711e2f06acc50ac325b93c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d5b6faad3c18cf05fe43a223fe30b010a7142330f7a3b22cce61698dd5d1ca5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="accountList")
    def account_list(self) -> typing.List[builtins.str]:
        '''One or more AWS accounts that will have access to the provisioned product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-accountlist
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountList"))

    @account_list.setter
    def account_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde8f51f324956b66ffc8f1d082306fa75417eaca857f1c958ff87fd3648052d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountList", value)

    @builtins.property
    @jsii.member(jsii_name="adminRole")
    def admin_role(self) -> builtins.str:
        '''AdminRole ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-adminrole
        '''
        return typing.cast(builtins.str, jsii.get(self, "adminRole"))

    @admin_role.setter
    def admin_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3998db215eb7bf13492e6a7ef460b2f6ad6685b1f56ae31fad5c673acaee37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminRole", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b242f34e080958c6ce538a7db003756d3ee4016b7e712bc2b0d0e85014ca0c03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> builtins.str:
        '''ExecutionRole name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-executionrole
        '''
        return typing.cast(builtins.str, jsii.get(self, "executionRole"))

    @execution_role.setter
    def execution_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16bd4423c71bef04f5b7f0646fcb205d43b3140d474581a0dcf5438e061830c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRole", value)

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-portfolioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))

    @portfolio_id.setter
    def portfolio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab832a39b7da19ff791f11d7963db7c12a78a1a2c2bd74747c6f8ec634012ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portfolioId", value)

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-productid
        '''
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547b1e4945be35c7161a3528def29c53de8a6c7c51f8ad0aafa96c35186b4de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value)

    @builtins.property
    @jsii.member(jsii_name="regionList")
    def region_list(self) -> typing.List[builtins.str]:
        '''One or more AWS Regions where the provisioned product will be available.

        Applicable only to a ``CFN_STACKSET`` provisioned product type.

        The specified Regions should be within the list of Regions from the ``STACKSET`` constraint. To get the list of Regions in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation.

        If no values are specified, the default value is all Regions from the ``STACKSET`` constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-regionlist
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regionList"))

    @region_list.setter
    def region_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d9f66bdb6a7444ac1d6fe3e72d4dd7900b30252fa16642733af135ad5d214dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionList", value)

    @builtins.property
    @jsii.member(jsii_name="stackInstanceControl")
    def stack_instance_control(self) -> builtins.str:
        '''Permission to create, update, and delete stack instances.

        Choose from ALLOWED and NOT_ALLOWED.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-stackinstancecontrol
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackInstanceControl"))

    @stack_instance_control.setter
    def stack_instance_control(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4f8ebc972013becd0cf5d5fecfec4bb7c92ce2fcd246daa44abc2fe2b140aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackInstanceControl", value)

    @builtins.property
    @jsii.member(jsii_name="acceptLanguage")
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-acceptlanguage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceptLanguage"))

    @accept_language.setter
    def accept_language(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88e3bc2ff5d3ebab865fca73b4f81fe1b2bba690fe88ef9ae93dd00120b1a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptLanguage", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnStackSetConstraintProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_list": "accountList",
        "admin_role": "adminRole",
        "description": "description",
        "execution_role": "executionRole",
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "region_list": "regionList",
        "stack_instance_control": "stackInstanceControl",
        "accept_language": "acceptLanguage",
    },
)
class CfnStackSetConstraintProps:
    def __init__(
        self,
        *,
        account_list: typing.Sequence[builtins.str],
        admin_role: builtins.str,
        description: builtins.str,
        execution_role: builtins.str,
        portfolio_id: builtins.str,
        product_id: builtins.str,
        region_list: typing.Sequence[builtins.str],
        stack_instance_control: builtins.str,
        accept_language: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnStackSetConstraint``.

        :param account_list: One or more AWS accounts that will have access to the provisioned product.
        :param admin_role: AdminRole ARN.
        :param description: The description of the constraint.
        :param execution_role: ExecutionRole name.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param region_list: One or more AWS Regions where the provisioned product will be available. Applicable only to a ``CFN_STACKSET`` provisioned product type. The specified Regions should be within the list of Regions from the ``STACKSET`` constraint. To get the list of Regions in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation. If no values are specified, the default value is all Regions from the ``STACKSET`` constraint.
        :param stack_instance_control: Permission to create, update, and delete stack instances. Choose from ALLOWED and NOT_ALLOWED.
        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_stack_set_constraint_props = servicecatalog.CfnStackSetConstraintProps(
                account_list=["accountList"],
                admin_role="adminRole",
                description="description",
                execution_role="executionRole",
                portfolio_id="portfolioId",
                product_id="productId",
                region_list=["regionList"],
                stack_instance_control="stackInstanceControl",
            
                # the properties below are optional
                accept_language="acceptLanguage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6705a483626b5c7fd621c817cee336faf357b47264cc41cc519eb87ce948ad98)
            check_type(argname="argument account_list", value=account_list, expected_type=type_hints["account_list"])
            check_type(argname="argument admin_role", value=admin_role, expected_type=type_hints["admin_role"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument region_list", value=region_list, expected_type=type_hints["region_list"])
            check_type(argname="argument stack_instance_control", value=stack_instance_control, expected_type=type_hints["stack_instance_control"])
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_list": account_list,
            "admin_role": admin_role,
            "description": description,
            "execution_role": execution_role,
            "portfolio_id": portfolio_id,
            "product_id": product_id,
            "region_list": region_list,
            "stack_instance_control": stack_instance_control,
        }
        if accept_language is not None:
            self._values["accept_language"] = accept_language

    @builtins.property
    def account_list(self) -> typing.List[builtins.str]:
        '''One or more AWS accounts that will have access to the provisioned product.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-accountlist
        '''
        result = self._values.get("account_list")
        assert result is not None, "Required property 'account_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def admin_role(self) -> builtins.str:
        '''AdminRole ARN.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-adminrole
        '''
        result = self._values.get("admin_role")
        assert result is not None, "Required property 'admin_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''The description of the constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_role(self) -> builtins.str:
        '''ExecutionRole name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-executionrole
        '''
        result = self._values.get("execution_role")
        assert result is not None, "Required property 'execution_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def portfolio_id(self) -> builtins.str:
        '''The portfolio identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-portfolioid
        '''
        result = self._values.get("portfolio_id")
        assert result is not None, "Required property 'portfolio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_id(self) -> builtins.str:
        '''The product identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-productid
        '''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region_list(self) -> typing.List[builtins.str]:
        '''One or more AWS Regions where the provisioned product will be available.

        Applicable only to a ``CFN_STACKSET`` provisioned product type.

        The specified Regions should be within the list of Regions from the ``STACKSET`` constraint. To get the list of Regions in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation.

        If no values are specified, the default value is all Regions from the ``STACKSET`` constraint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-regionlist
        '''
        result = self._values.get("region_list")
        assert result is not None, "Required property 'region_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def stack_instance_control(self) -> builtins.str:
        '''Permission to create, update, and delete stack instances.

        Choose from ALLOWED and NOT_ALLOWED.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-stackinstancecontrol
        '''
        result = self._values.get("stack_instance_control")
        assert result is not None, "Required property 'stack_instance_control' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackSetConstraintProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTagOption(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnTagOption",
):
    '''A CloudFormation ``AWS::ServiceCatalog::TagOption``.

    Specifies a TagOption. A TagOption is a key-value pair managed by AWS Service Catalog that serves as a template for creating an AWS tag.

    :cloudformationResource: AWS::ServiceCatalog::TagOption
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_tag_option = servicecatalog.CfnTagOption(self, "MyCfnTagOption",
            key="key",
            value="value",
        
            # the properties below are optional
            active=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        key: builtins.str,
        value: builtins.str,
        active: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::TagOption``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key: The TagOption key.
        :param value: The TagOption value.
        :param active: The TagOption active state.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34347da5e8fb762c964a65f85fc79ebec7c594c1bd559349e70f2272ea2ec583)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTagOptionProps(key=key, value=value, active=active)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fb2e19d3b508b1ca1c2cae8864a42e810a534fdc6f474114a0f67587fff983)
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
            type_hints = typing.get_type_hints(_typecheckingstub__826caecc284ecc3944249f4d71f324eaf08c5adaa8912e18bcb43ecba824135b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        '''The TagOption key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-key
        '''
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff3f1576e3a9db63c91cf0e1aba117e952b52d9a32410e4df4f23ea1d6c1c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''The TagOption value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-value
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3feb59c6da58663d22531426b965db3bfee687a22aadd1f42a4e78562da40bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''The TagOption active state.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-active
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "active"))

    @active.setter
    def active(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1eddfb5a3d5cb539f5cd71506f914481eafea8eb7b12de0d1c020cdf321f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "active", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnTagOptionAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CfnTagOptionAssociation",
):
    '''A CloudFormation ``AWS::ServiceCatalog::TagOptionAssociation``.

    Associate the specified TagOption with the specified portfolio or product.

    :cloudformationResource: AWS::ServiceCatalog::TagOptionAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        cfn_tag_option_association = servicecatalog.CfnTagOptionAssociation(self, "MyCfnTagOptionAssociation",
            resource_id="resourceId",
            tag_option_id="tagOptionId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        resource_id: builtins.str,
        tag_option_id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::ServiceCatalog::TagOptionAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_id: The resource identifier.
        :param tag_option_id: The TagOption identifier.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7dd8b3f1b0d8dbd58f22bd6f147896961866bdf19f858efff69fe2a09e4557)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTagOptionAssociationProps(
            resource_id=resource_id, tag_option_id=tag_option_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c9da6f5ba3fe54b13666fac168d90a342b9fba614e0385e25ef9312b239c12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdce26e573e18c16d7e182e789259d62e6af1b274de8b11987b3f47ddf8d5577)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        '''The resource identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html#cfn-servicecatalog-tagoptionassociation-resourceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea948c812f5c73898f84aa5e9b1a01c606ac1826b13f398568c4c85b441f072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value)

    @builtins.property
    @jsii.member(jsii_name="tagOptionId")
    def tag_option_id(self) -> builtins.str:
        '''The TagOption identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html#cfn-servicecatalog-tagoptionassociation-tagoptionid
        '''
        return typing.cast(builtins.str, jsii.get(self, "tagOptionId"))

    @tag_option_id.setter
    def tag_option_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7fbf902d8389e12e5b76c8d19f4c1d70428822a021b4193cf96510aeb6f52b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagOptionId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnTagOptionAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"resource_id": "resourceId", "tag_option_id": "tagOptionId"},
)
class CfnTagOptionAssociationProps:
    def __init__(
        self,
        *,
        resource_id: builtins.str,
        tag_option_id: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnTagOptionAssociation``.

        :param resource_id: The resource identifier.
        :param tag_option_id: The TagOption identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_tag_option_association_props = servicecatalog.CfnTagOptionAssociationProps(
                resource_id="resourceId",
                tag_option_id="tagOptionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c091bb87ff87594a9a60fe7ba5975c367e4a3d034456b260b01f2bce7242bc3e)
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument tag_option_id", value=tag_option_id, expected_type=type_hints["tag_option_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_id": resource_id,
            "tag_option_id": tag_option_id,
        }

    @builtins.property
    def resource_id(self) -> builtins.str:
        '''The resource identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html#cfn-servicecatalog-tagoptionassociation-resourceid
        '''
        result = self._values.get("resource_id")
        assert result is not None, "Required property 'resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_option_id(self) -> builtins.str:
        '''The TagOption identifier.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html#cfn-servicecatalog-tagoptionassociation-tagoptionid
        '''
        result = self._values.get("tag_option_id")
        assert result is not None, "Required property 'tag_option_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTagOptionAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CfnTagOptionProps",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value", "active": "active"},
)
class CfnTagOptionProps:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: builtins.str,
        active: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTagOption``.

        :param key: The TagOption key.
        :param value: The TagOption value.
        :param active: The TagOption active state.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cfn_tag_option_props = servicecatalog.CfnTagOptionProps(
                key="key",
                value="value",
            
                # the properties below are optional
                active=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376093287aea62e59fefc23e1f17314a241a57118ca5e0b9f10b98818700fb4f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }
        if active is not None:
            self._values["active"] = active

    @builtins.property
    def key(self) -> builtins.str:
        '''The TagOption key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The TagOption value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-value
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''The TagOption active state.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-active
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTagOptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CloudFormationProductProps",
    jsii_struct_bases=[],
    name_mapping={
        "owner": "owner",
        "product_name": "productName",
        "product_versions": "productVersions",
        "description": "description",
        "distributor": "distributor",
        "message_language": "messageLanguage",
        "replace_product_version_ids": "replaceProductVersionIds",
        "support_description": "supportDescription",
        "support_email": "supportEmail",
        "support_url": "supportUrl",
        "tag_options": "tagOptions",
    },
)
class CloudFormationProductProps:
    def __init__(
        self,
        *,
        owner: builtins.str,
        product_name: builtins.str,
        product_versions: typing.Sequence[typing.Union["CloudFormationProductVersion", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        distributor: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
        replace_product_version_ids: typing.Optional[builtins.bool] = None,
        support_description: typing.Optional[builtins.str] = None,
        support_email: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
        tag_options: typing.Optional["TagOptions"] = None,
    ) -> None:
        '''(experimental) Properties for a Cloudformation Product.

        :param owner: (experimental) The owner of the product.
        :param product_name: (experimental) The name of the product.
        :param product_versions: (experimental) The configuration of the product version.
        :param description: (experimental) The description of the product. Default: - No description provided
        :param distributor: (experimental) The distributor of the product. Default: - No distributor provided
        :param message_language: (experimental) The language code. Controls language for logging and errors. Default: - English
        :param replace_product_version_ids: (experimental) Whether to give provisioning artifacts a new unique identifier when the product attributes or provisioning artifacts is updated. Default: false
        :param support_description: (experimental) The support information about the product. Default: - No support description provided
        :param support_email: (experimental) The contact email for product support. Default: - No support email provided
        :param support_url: (experimental) The contact URL for product support. Default: - No support URL provided
        :param tag_options: (experimental) TagOptions associated directly to a product. Default: - No tagOptions provided

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as s3
            import monocdk as cdk
            
            
            class S3BucketProduct(servicecatalog.ProductStack):
                def __init__(self, scope, id):
                    super().__init__(scope, id)
            
                    s3.Bucket(self, "BucketProduct")
            
            product = servicecatalog.CloudFormationProduct(self, "Product",
                product_name="My Product",
                owner="Product Owner",
                product_versions=[s3.aws_servicecatalog.CloudFormationProductVersion(
                    product_version_name="v1",
                    cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(S3BucketProduct(self, "S3BucketProduct"))
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3a7b5581814f3bdd8c23929d7ac55ae35fc55897db386cf1ad87cfb37233e0)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument product_name", value=product_name, expected_type=type_hints["product_name"])
            check_type(argname="argument product_versions", value=product_versions, expected_type=type_hints["product_versions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument distributor", value=distributor, expected_type=type_hints["distributor"])
            check_type(argname="argument message_language", value=message_language, expected_type=type_hints["message_language"])
            check_type(argname="argument replace_product_version_ids", value=replace_product_version_ids, expected_type=type_hints["replace_product_version_ids"])
            check_type(argname="argument support_description", value=support_description, expected_type=type_hints["support_description"])
            check_type(argname="argument support_email", value=support_email, expected_type=type_hints["support_email"])
            check_type(argname="argument support_url", value=support_url, expected_type=type_hints["support_url"])
            check_type(argname="argument tag_options", value=tag_options, expected_type=type_hints["tag_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "owner": owner,
            "product_name": product_name,
            "product_versions": product_versions,
        }
        if description is not None:
            self._values["description"] = description
        if distributor is not None:
            self._values["distributor"] = distributor
        if message_language is not None:
            self._values["message_language"] = message_language
        if replace_product_version_ids is not None:
            self._values["replace_product_version_ids"] = replace_product_version_ids
        if support_description is not None:
            self._values["support_description"] = support_description
        if support_email is not None:
            self._values["support_email"] = support_email
        if support_url is not None:
            self._values["support_url"] = support_url
        if tag_options is not None:
            self._values["tag_options"] = tag_options

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The owner of the product.

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_name(self) -> builtins.str:
        '''(experimental) The name of the product.

        :stability: experimental
        '''
        result = self._values.get("product_name")
        assert result is not None, "Required property 'product_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_versions(self) -> typing.List["CloudFormationProductVersion"]:
        '''(experimental) The configuration of the product version.

        :stability: experimental
        '''
        result = self._values.get("product_versions")
        assert result is not None, "Required property 'product_versions' is missing"
        return typing.cast(typing.List["CloudFormationProductVersion"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the product.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distributor(self) -> typing.Optional[builtins.str]:
        '''(experimental) The distributor of the product.

        :default: - No distributor provided

        :stability: experimental
        '''
        result = self._values.get("distributor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_language(self) -> typing.Optional["MessageLanguage"]:
        '''(experimental) The language code.

        Controls language for logging and errors.

        :default: - English

        :stability: experimental
        '''
        result = self._values.get("message_language")
        return typing.cast(typing.Optional["MessageLanguage"], result)

    @builtins.property
    def replace_product_version_ids(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to give provisioning artifacts a new unique identifier when the product attributes or provisioning artifacts is updated.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("replace_product_version_ids")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def support_description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The support information about the product.

        :default: - No support description provided

        :stability: experimental
        '''
        result = self._values.get("support_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) The contact email for product support.

        :default: - No support email provided

        :stability: experimental
        '''
        result = self._values.get("support_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The contact URL for product support.

        :default: - No support URL provided

        :stability: experimental
        '''
        result = self._values.get("support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_options(self) -> typing.Optional["TagOptions"]:
        '''(experimental) TagOptions associated directly to a product.

        :default: - No tagOptions provided

        :stability: experimental
        '''
        result = self._values.get("tag_options")
        return typing.cast(typing.Optional["TagOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationProductProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CloudFormationProductVersion",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_formation_template": "cloudFormationTemplate",
        "description": "description",
        "product_version_name": "productVersionName",
        "validate_template": "validateTemplate",
    },
)
class CloudFormationProductVersion:
    def __init__(
        self,
        *,
        cloud_formation_template: "CloudFormationTemplate",
        description: typing.Optional[builtins.str] = None,
        product_version_name: typing.Optional[builtins.str] = None,
        validate_template: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties of product version (also known as a provisioning artifact).

        :param cloud_formation_template: (experimental) The S3 template that points to the provisioning version template.
        :param description: (experimental) The description of the product version. Default: - No description provided
        :param product_version_name: (experimental) The name of the product version. Default: - No product version name provided
        :param validate_template: (experimental) Whether the specified product template will be validated by CloudFormation. If turned off, an invalid template configuration can be stored. Default: true

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            # cloud_formation_template: servicecatalog.CloudFormationTemplate
            
            cloud_formation_product_version = servicecatalog.CloudFormationProductVersion(
                cloud_formation_template=cloud_formation_template,
            
                # the properties below are optional
                description="description",
                product_version_name="productVersionName",
                validate_template=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa78ba884403832f78e38403ae3b3b6ddfc5c072cf5a0637f8332c3e2cacf26)
            check_type(argname="argument cloud_formation_template", value=cloud_formation_template, expected_type=type_hints["cloud_formation_template"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument product_version_name", value=product_version_name, expected_type=type_hints["product_version_name"])
            check_type(argname="argument validate_template", value=validate_template, expected_type=type_hints["validate_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_formation_template": cloud_formation_template,
        }
        if description is not None:
            self._values["description"] = description
        if product_version_name is not None:
            self._values["product_version_name"] = product_version_name
        if validate_template is not None:
            self._values["validate_template"] = validate_template

    @builtins.property
    def cloud_formation_template(self) -> "CloudFormationTemplate":
        '''(experimental) The S3 template that points to the provisioning version template.

        :stability: experimental
        '''
        result = self._values.get("cloud_formation_template")
        assert result is not None, "Required property 'cloud_formation_template' is missing"
        return typing.cast("CloudFormationTemplate", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the product version.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_version_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the product version.

        :default: - No product version name provided

        :stability: experimental
        '''
        result = self._values.get("product_version_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate_template(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the specified product template will be validated by CloudFormation.

        If turned off, an invalid template configuration can be stored.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("validate_template")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationProductVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudFormationTemplate(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_servicecatalog.CloudFormationTemplate",
):
    '''(experimental) Represents the Product Provisioning Artifact Template.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import path as path
        
        
        product = servicecatalog.CloudFormationProduct(self, "Product",
            product_name="My Product",
            owner="Product Owner",
            product_versions=[servicecatalog.aws_servicecatalog.CloudFormationProductVersion(
                product_version_name="v1",
                cloud_formation_template=servicecatalog.CloudFormationTemplate.from_url("https://raw.githubusercontent.com/awslabs/aws-cloudformation-templates/master/aws/services/ServiceCatalog/Product.yaml")
            ), servicecatalog.aws_servicecatalog.CloudFormationProductVersion(
                product_version_name="v2",
                cloud_formation_template=servicecatalog.CloudFormationTemplate.from_asset(path.join(__dirname, "development-environment.template.json"))
            )
            ]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        path: builtins.str,
        *,
        readers: typing.Optional[typing.Sequence[_IGrantable_4c5a91d1]] = None,
        source_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow: typing.Optional[_FollowMode_98b05cc5] = None,
        ignore_mode: typing.Optional[_IgnoreMode_31d8bf46] = None,
        follow_symlinks: typing.Optional[_SymlinkFollowMode_abf4527a] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_AssetHashType_49193809] = None,
        bundling: typing.Optional[typing.Union[_BundlingOptions_ab115a99, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "CloudFormationTemplate":
        '''(experimental) Loads the provisioning artifacts template from a local disk path.

        :param path: A file containing the provisioning artifacts.
        :param readers: (experimental) A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: (deprecated) Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param follow_symlinks: (experimental) A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param asset_hash: (experimental) Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: (experimental) Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: (experimental) Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f539e17f72a82fdf3d03b6fc29db72e44f780ff08b0e5fe7c2e8cdcd3266798f)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        options = _AssetOptions_bd2996da(
            readers=readers,
            source_hash=source_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
            follow_symlinks=follow_symlinks,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
        )

        return typing.cast("CloudFormationTemplate", jsii.sinvoke(cls, "fromAsset", [path, options]))

    @jsii.member(jsii_name="fromProductStack")
    @builtins.classmethod
    def from_product_stack(
        cls,
        product_stack: "ProductStack",
    ) -> "CloudFormationTemplate":
        '''(experimental) Creates a product with the resources defined in the given product stack.

        :param product_stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49eb94cce84255dfc5315c17696cadbe42f69096c1d51e13cf00f4202e9629a)
            check_type(argname="argument product_stack", value=product_stack, expected_type=type_hints["product_stack"])
        return typing.cast("CloudFormationTemplate", jsii.sinvoke(cls, "fromProductStack", [product_stack]))

    @jsii.member(jsii_name="fromUrl")
    @builtins.classmethod
    def from_url(cls, url: builtins.str) -> "CloudFormationTemplate":
        '''(experimental) Template from URL.

        :param url: The url that points to the provisioning artifacts template.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68da87dc01cbce0176b4e23e75fe5cdbbfe4673711535f10edbb14c8e51e068e)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        return typing.cast("CloudFormationTemplate", jsii.sinvoke(cls, "fromUrl", [url]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _Construct_e78e779f) -> "CloudFormationTemplateConfig":
        '''(experimental) Called when the product is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.

        :stability: experimental
        '''
        ...


class _CloudFormationTemplateProxy(CloudFormationTemplate):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_e78e779f) -> "CloudFormationTemplateConfig":
        '''(experimental) Called when the product is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19cc553f69512f45e46be4de2aa4442a6306d7b5be707b36418d612dbe6f53b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("CloudFormationTemplateConfig", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, CloudFormationTemplate).__jsii_proxy_class__ = lambda : _CloudFormationTemplateProxy


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CloudFormationTemplateConfig",
    jsii_struct_bases=[],
    name_mapping={"http_url": "httpUrl"},
)
class CloudFormationTemplateConfig:
    def __init__(self, *, http_url: builtins.str) -> None:
        '''(experimental) Result of binding ``Template`` into a ``Product``.

        :param http_url: (experimental) The http url of the template in S3.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            cloud_formation_template_config = servicecatalog.CloudFormationTemplateConfig(
                http_url="httpUrl"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad64e8ca1965ae00682380e0dbba2880163056e106052507446757ba3d5a3d7b)
            check_type(argname="argument http_url", value=http_url, expected_type=type_hints["http_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "http_url": http_url,
        }

    @builtins.property
    def http_url(self) -> builtins.str:
        '''(experimental) The http url of the template in S3.

        :stability: experimental
        '''
        result = self._values.get("http_url")
        assert result is not None, "Required property 'http_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CommonConstraintOptions",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "message_language": "messageLanguage"},
)
class CommonConstraintOptions:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Properties for governance mechanisms and constraints.

        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as sns
            
            # portfolio: servicecatalog.Portfolio
            # product: servicecatalog.CloudFormationProduct
            
            
            topic1 = sns.Topic(self, "Topic1")
            portfolio.notify_on_stack_events(product, topic1)
            
            topic2 = sns.Topic(self, "Topic2")
            portfolio.notify_on_stack_events(product, topic2,
                description="description for topic2"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cfbb1df9c85153dbfd1bc947c516215d0e1a55867b07b31d35f4a8da89c191a)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument message_language", value=message_language, expected_type=type_hints["message_language"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if message_language is not None:
            self._values["message_language"] = message_language

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the constraint.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_language(self) -> typing.Optional["MessageLanguage"]:
        '''(experimental) The language code.

        Configures the language for error messages from service catalog.

        :default: - English

        :stability: experimental
        '''
        result = self._values.get("message_language")
        return typing.cast(typing.Optional["MessageLanguage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonConstraintOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_servicecatalog.IPortfolio")
class IPortfolio(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A Service Catalog portfolio.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="portfolioArn")
    def portfolio_arn(self) -> builtins.str:
        '''(experimental) The ARN of the portfolio.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''(experimental) The ID of the portfolio.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addProduct")
    def add_product(self, product: "IProduct") -> None:
        '''(experimental) Associate portfolio with the given product.

        :param product: A service catalog produt.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="associateTagOptions")
    def associate_tag_options(self, tag_options: "TagOptions") -> None:
        '''(experimental) Associate Tag Options.

        A TagOption is a key-value pair managed in AWS Service Catalog.
        It is not an AWS tag, but serves as a template for creating an AWS tag based on the TagOption.

        :param tag_options: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="constrainCloudFormationParameters")
    def constrain_cloud_formation_parameters(
        self,
        product: "IProduct",
        *,
        rule: typing.Union["TemplateRule", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Set provisioning rules for the product.

        :param product: A service catalog product.
        :param rule: (experimental) The rule with condition and assertions to apply to template.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="constrainTagUpdates")
    def constrain_tag_updates(
        self,
        product: "IProduct",
        *,
        allow: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Add a Resource Update Constraint.

        :param product: -
        :param allow: (experimental) Toggle for if users should be allowed to change/update tags on provisioned products. Default: true
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="deployWithStackSets")
    def deploy_with_stack_sets(
        self,
        product: "IProduct",
        *,
        accounts: typing.Sequence[builtins.str],
        admin_role: _IRole_59af6f50,
        execution_role_name: builtins.str,
        regions: typing.Sequence[builtins.str],
        allow_stack_set_instance_operations: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Configure deployment options using AWS Cloudformation StackSets.

        :param product: A service catalog product.
        :param accounts: (experimental) List of accounts to deploy stacks to.
        :param admin_role: (experimental) IAM role used to administer the StackSets configuration.
        :param execution_role_name: (experimental) IAM role used to provision the products in the Stacks.
        :param regions: (experimental) List of regions to deploy stacks to.
        :param allow_stack_set_instance_operations: (experimental) Wether to allow end users to create, update, and delete stacks. Default: false
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="giveAccessToGroup")
    def give_access_to_group(self, group: _IGroup_8a32caf8) -> None:
        '''(experimental) Associate portfolio with an IAM Group.

        :param group: an IAM Group.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="giveAccessToRole")
    def give_access_to_role(self, role: _IRole_59af6f50) -> None:
        '''(experimental) Associate portfolio with an IAM Role.

        :param role: an IAM role.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="giveAccessToUser")
    def give_access_to_user(self, user: _IUser_9d11d57d) -> None:
        '''(experimental) Associate portfolio with an IAM User.

        :param user: an IAM user.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="notifyOnStackEvents")
    def notify_on_stack_events(
        self,
        product: "IProduct",
        topic: _ITopic_465e36b9,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Add notifications for supplied topics on the provisioned product.

        :param product: A service catalog product.
        :param topic: A SNS Topic to receive notifications on events related to the provisioned product.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="setLaunchRole")
    def set_launch_role(
        self,
        product: "IProduct",
        launch_role: _IRole_59af6f50,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Force users to assume a certain role when launching a product.

        This sets the launch role using the role arn which is tied to the account this role exists in.
        This is useful if you will be provisioning products from the account where this role exists.
        If you intend to share the portfolio across accounts, use a local launch role.

        :param product: A service catalog product.
        :param launch_role: The IAM role a user must assume when provisioning the product.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="setLocalLaunchRole")
    def set_local_launch_role(
        self,
        product: "IProduct",
        launch_role: _IRole_59af6f50,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Force users to assume a certain role when launching a product.

        The role name will be referenced by in the local account and must be set explicitly.
        This is useful when sharing the portfolio with multiple accounts.

        :param product: A service catalog product.
        :param launch_role: The IAM role a user must assume when provisioning the product. A role with this name must exist in the account where the portolio is created and the accounts it is shared with. The role name must be set explicitly.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="setLocalLaunchRoleName")
    def set_local_launch_role_name(
        self,
        product: "IProduct",
        launch_role_name: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> _IRole_59af6f50:
        '''(experimental) Force users to assume a certain role when launching a product.

        The role will be referenced by name in the local account instead of a static role arn.
        A role with this name will automatically be created and assumable by Service Catalog in this account.
        This is useful when sharing the portfolio with multiple accounts.

        :param product: A service catalog product.
        :param launch_role_name: The name of the IAM role a user must assume when provisioning the product. A role with this name must exist in the account where the portolio is created and the accounts it is shared with.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="shareWithAccount")
    def share_with_account(
        self,
        account_id: builtins.str,
        *,
        message_language: typing.Optional["MessageLanguage"] = None,
        share_tag_options: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Initiate a portfolio share with another account.

        :param account_id: AWS account to share portfolio with.
        :param message_language: (experimental) The message language of the share. Controls status and error message language for share. Default: - English
        :param share_tag_options: (experimental) Whether to share tagOptions as a part of the portfolio share. Default: - share not specified

        :stability: experimental
        '''
        ...


class _IPortfolioProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A Service Catalog portfolio.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_servicecatalog.IPortfolio"

    @builtins.property
    @jsii.member(jsii_name="portfolioArn")
    def portfolio_arn(self) -> builtins.str:
        '''(experimental) The ARN of the portfolio.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioArn"))

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''(experimental) The ID of the portfolio.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))

    @jsii.member(jsii_name="addProduct")
    def add_product(self, product: "IProduct") -> None:
        '''(experimental) Associate portfolio with the given product.

        :param product: A service catalog produt.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a5bbe75222fe426891b9f894414bc0309914052b1b647b9a43c16d5ecac203)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
        return typing.cast(None, jsii.invoke(self, "addProduct", [product]))

    @jsii.member(jsii_name="associateTagOptions")
    def associate_tag_options(self, tag_options: "TagOptions") -> None:
        '''(experimental) Associate Tag Options.

        A TagOption is a key-value pair managed in AWS Service Catalog.
        It is not an AWS tag, but serves as a template for creating an AWS tag based on the TagOption.

        :param tag_options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0649d5f680adf7747fbf3087ce1af0e23cff64246efdca5bd8764dfb1dc9ca19)
            check_type(argname="argument tag_options", value=tag_options, expected_type=type_hints["tag_options"])
        return typing.cast(None, jsii.invoke(self, "associateTagOptions", [tag_options]))

    @jsii.member(jsii_name="constrainCloudFormationParameters")
    def constrain_cloud_formation_parameters(
        self,
        product: "IProduct",
        *,
        rule: typing.Union["TemplateRule", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Set provisioning rules for the product.

        :param product: A service catalog product.
        :param rule: (experimental) The rule with condition and assertions to apply to template.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db604a98d4d01f13120134594168901610b62e6c383e61fa8f6017d81f8ceadf)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
        options = CloudFormationRuleConstraintOptions(
            rule=rule, description=description, message_language=message_language
        )

        return typing.cast(None, jsii.invoke(self, "constrainCloudFormationParameters", [product, options]))

    @jsii.member(jsii_name="constrainTagUpdates")
    def constrain_tag_updates(
        self,
        product: "IProduct",
        *,
        allow: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Add a Resource Update Constraint.

        :param product: -
        :param allow: (experimental) Toggle for if users should be allowed to change/update tags on provisioned products. Default: true
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14afa5a4e81bc92f5941d75963f729709d6a2a6ec5160029f443e4044aa2034)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
        options = TagUpdateConstraintOptions(
            allow=allow, description=description, message_language=message_language
        )

        return typing.cast(None, jsii.invoke(self, "constrainTagUpdates", [product, options]))

    @jsii.member(jsii_name="deployWithStackSets")
    def deploy_with_stack_sets(
        self,
        product: "IProduct",
        *,
        accounts: typing.Sequence[builtins.str],
        admin_role: _IRole_59af6f50,
        execution_role_name: builtins.str,
        regions: typing.Sequence[builtins.str],
        allow_stack_set_instance_operations: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Configure deployment options using AWS Cloudformation StackSets.

        :param product: A service catalog product.
        :param accounts: (experimental) List of accounts to deploy stacks to.
        :param admin_role: (experimental) IAM role used to administer the StackSets configuration.
        :param execution_role_name: (experimental) IAM role used to provision the products in the Stacks.
        :param regions: (experimental) List of regions to deploy stacks to.
        :param allow_stack_set_instance_operations: (experimental) Wether to allow end users to create, update, and delete stacks. Default: false
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66f58911bb56bdc65912805c6e8852f3b6e672eb0a61a2b08d2330e76407dce)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
        options = StackSetsConstraintOptions(
            accounts=accounts,
            admin_role=admin_role,
            execution_role_name=execution_role_name,
            regions=regions,
            allow_stack_set_instance_operations=allow_stack_set_instance_operations,
            description=description,
            message_language=message_language,
        )

        return typing.cast(None, jsii.invoke(self, "deployWithStackSets", [product, options]))

    @jsii.member(jsii_name="giveAccessToGroup")
    def give_access_to_group(self, group: _IGroup_8a32caf8) -> None:
        '''(experimental) Associate portfolio with an IAM Group.

        :param group: an IAM Group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f44be325389fc8b7e1607a28f84613ca7416cb5082a9ff4af0e3b4463699bd)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        return typing.cast(None, jsii.invoke(self, "giveAccessToGroup", [group]))

    @jsii.member(jsii_name="giveAccessToRole")
    def give_access_to_role(self, role: _IRole_59af6f50) -> None:
        '''(experimental) Associate portfolio with an IAM Role.

        :param role: an IAM role.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66f2970b3850cf0cfbaffec75bcd58a9fde27ae85b56c2d4feb9a7e772100c61)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "giveAccessToRole", [role]))

    @jsii.member(jsii_name="giveAccessToUser")
    def give_access_to_user(self, user: _IUser_9d11d57d) -> None:
        '''(experimental) Associate portfolio with an IAM User.

        :param user: an IAM user.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2a29b72dceb0d42cae20bd71904dc20e639543e8ba19e4010a72cabdc754e8)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        return typing.cast(None, jsii.invoke(self, "giveAccessToUser", [user]))

    @jsii.member(jsii_name="notifyOnStackEvents")
    def notify_on_stack_events(
        self,
        product: "IProduct",
        topic: _ITopic_465e36b9,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Add notifications for supplied topics on the provisioned product.

        :param product: A service catalog product.
        :param topic: A SNS Topic to receive notifications on events related to the provisioned product.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57c6fc6988172115b736725b1f78a7f3ba0b52ae72500d8d67baaefe8b6ec62)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        options = CommonConstraintOptions(
            description=description, message_language=message_language
        )

        return typing.cast(None, jsii.invoke(self, "notifyOnStackEvents", [product, topic, options]))

    @jsii.member(jsii_name="setLaunchRole")
    def set_launch_role(
        self,
        product: "IProduct",
        launch_role: _IRole_59af6f50,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Force users to assume a certain role when launching a product.

        This sets the launch role using the role arn which is tied to the account this role exists in.
        This is useful if you will be provisioning products from the account where this role exists.
        If you intend to share the portfolio across accounts, use a local launch role.

        :param product: A service catalog product.
        :param launch_role: The IAM role a user must assume when provisioning the product.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed16cf3e9cce8c001252c373a9c23391303ba256a5f50a2903891806a2a39a75)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument launch_role", value=launch_role, expected_type=type_hints["launch_role"])
        options = CommonConstraintOptions(
            description=description, message_language=message_language
        )

        return typing.cast(None, jsii.invoke(self, "setLaunchRole", [product, launch_role, options]))

    @jsii.member(jsii_name="setLocalLaunchRole")
    def set_local_launch_role(
        self,
        product: "IProduct",
        launch_role: _IRole_59af6f50,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> None:
        '''(experimental) Force users to assume a certain role when launching a product.

        The role name will be referenced by in the local account and must be set explicitly.
        This is useful when sharing the portfolio with multiple accounts.

        :param product: A service catalog product.
        :param launch_role: The IAM role a user must assume when provisioning the product. A role with this name must exist in the account where the portolio is created and the accounts it is shared with. The role name must be set explicitly.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755aa308d6b8389b689e2707bbab28a2e1d83e2389b4af22aaa6ffae785c78d8)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument launch_role", value=launch_role, expected_type=type_hints["launch_role"])
        options = CommonConstraintOptions(
            description=description, message_language=message_language
        )

        return typing.cast(None, jsii.invoke(self, "setLocalLaunchRole", [product, launch_role, options]))

    @jsii.member(jsii_name="setLocalLaunchRoleName")
    def set_local_launch_role_name(
        self,
        product: "IProduct",
        launch_role_name: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional["MessageLanguage"] = None,
    ) -> _IRole_59af6f50:
        '''(experimental) Force users to assume a certain role when launching a product.

        The role will be referenced by name in the local account instead of a static role arn.
        A role with this name will automatically be created and assumable by Service Catalog in this account.
        This is useful when sharing the portfolio with multiple accounts.

        :param product: A service catalog product.
        :param launch_role_name: The name of the IAM role a user must assume when provisioning the product. A role with this name must exist in the account where the portolio is created and the accounts it is shared with.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db0efb957d700097cd758541fa75f5eebca92127c1815137852a11e6f8db956)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument launch_role_name", value=launch_role_name, expected_type=type_hints["launch_role_name"])
        options = CommonConstraintOptions(
            description=description, message_language=message_language
        )

        return typing.cast(_IRole_59af6f50, jsii.invoke(self, "setLocalLaunchRoleName", [product, launch_role_name, options]))

    @jsii.member(jsii_name="shareWithAccount")
    def share_with_account(
        self,
        account_id: builtins.str,
        *,
        message_language: typing.Optional["MessageLanguage"] = None,
        share_tag_options: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Initiate a portfolio share with another account.

        :param account_id: AWS account to share portfolio with.
        :param message_language: (experimental) The message language of the share. Controls status and error message language for share. Default: - English
        :param share_tag_options: (experimental) Whether to share tagOptions as a part of the portfolio share. Default: - share not specified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ae069777f6b4e74743ef0b2cdc100c541b83b82b6bb3d15977c4d81d6d3624)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        options = PortfolioShareOptions(
            message_language=message_language, share_tag_options=share_tag_options
        )

        return typing.cast(None, jsii.invoke(self, "shareWithAccount", [account_id, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPortfolio).__jsii_proxy_class__ = lambda : _IPortfolioProxy


@jsii.interface(jsii_type="monocdk.aws_servicecatalog.IProduct")
class IProduct(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A Service Catalog product, currently only supports type CloudFormationProduct.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="productArn")
    def product_arn(self) -> builtins.str:
        '''(experimental) The ARN of the product.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''(experimental) The id of the product.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="associateTagOptions")
    def associate_tag_options(self, tag_options: "TagOptions") -> None:
        '''(experimental) Associate Tag Options.

        A TagOption is a key-value pair managed in AWS Service Catalog.
        It is not an AWS tag, but serves as a template for creating an AWS tag based on the TagOption.

        :param tag_options: -

        :stability: experimental
        '''
        ...


class _IProductProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A Service Catalog product, currently only supports type CloudFormationProduct.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_servicecatalog.IProduct"

    @builtins.property
    @jsii.member(jsii_name="productArn")
    def product_arn(self) -> builtins.str:
        '''(experimental) The ARN of the product.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "productArn"))

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''(experimental) The id of the product.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @jsii.member(jsii_name="associateTagOptions")
    def associate_tag_options(self, tag_options: "TagOptions") -> None:
        '''(experimental) Associate Tag Options.

        A TagOption is a key-value pair managed in AWS Service Catalog.
        It is not an AWS tag, but serves as a template for creating an AWS tag based on the TagOption.

        :param tag_options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9b6e3a91c83b6c37a67749ba97a222f5708966a96832673772c2d72b91d049)
            check_type(argname="argument tag_options", value=tag_options, expected_type=type_hints["tag_options"])
        return typing.cast(None, jsii.invoke(self, "associateTagOptions", [tag_options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IProduct).__jsii_proxy_class__ = lambda : _IProductProxy


@jsii.enum(jsii_type="monocdk.aws_servicecatalog.MessageLanguage")
class MessageLanguage(enum.Enum):
    '''(experimental) The language code.

    Used for error and logging messages for end users.
    The default behavior if not specified is English.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        servicecatalog.Portfolio(self, "Portfolio",
            display_name="MyFirstPortfolio",
            provider_name="SCAdmin",
            description="Portfolio for a project",
            message_language=servicecatalog.MessageLanguage.EN
        )
    '''

    EN = "EN"
    '''(experimental) English.

    :stability: experimental
    '''
    JP = "JP"
    '''(experimental) Japanese.

    :stability: experimental
    '''
    ZH = "ZH"
    '''(experimental) Chinese.

    :stability: experimental
    '''


@jsii.implements(IPortfolio)
class Portfolio(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.Portfolio",
):
    '''(experimental) A Service Catalog portfolio.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        servicecatalog.Portfolio(self, "Portfolio",
            display_name="MyPortfolio",
            provider_name="MyTeam"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        display_name: builtins.str,
        provider_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
        tag_options: typing.Optional["TagOptions"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param display_name: (experimental) The name of the portfolio.
        :param provider_name: (experimental) The provider name.
        :param description: (experimental) Description for portfolio. Default: - No description provided
        :param message_language: (experimental) The message language. Controls language for status logging and errors. Default: - English
        :param tag_options: (experimental) TagOptions associated directly to a portfolio. Default: - No tagOptions provided

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f80ec5f5bee355821a01e3fc22f91f55a7e68e00d2e684321f981760d57ad73)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PortfolioProps(
            display_name=display_name,
            provider_name=provider_name,
            description=description,
            message_language=message_language,
            tag_options=tag_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPortfolioArn")
    @builtins.classmethod
    def from_portfolio_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        portfolio_arn: builtins.str,
    ) -> IPortfolio:
        '''(experimental) Creates a Portfolio construct that represents an external portfolio.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param portfolio_arn: the Amazon Resource Name of the existing portfolio.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9c2e611d344a07c80f17c63274cf0d0940305eabdbd3c8e6e91dfedd032a47)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument portfolio_arn", value=portfolio_arn, expected_type=type_hints["portfolio_arn"])
        return typing.cast(IPortfolio, jsii.sinvoke(cls, "fromPortfolioArn", [scope, id, portfolio_arn]))

    @jsii.member(jsii_name="addProduct")
    def add_product(self, product: IProduct) -> None:
        '''(experimental) Associate portfolio with the given product.

        :param product: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4002350e77eff6e60769777d2b2649b5d61203437119ac9d20c9d3a250e84358)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
        return typing.cast(None, jsii.invoke(self, "addProduct", [product]))

    @jsii.member(jsii_name="associateTagOptions")
    def associate_tag_options(self, tag_options: "TagOptions") -> None:
        '''(experimental) Associate Tag Options.

        A TagOption is a key-value pair managed in AWS Service Catalog.
        It is not an AWS tag, but serves as a template for creating an AWS tag based on the TagOption.

        :param tag_options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788adf2a1761a91664610e791a6ae14c8827a0745c9062b359e72b99d3b48ff9)
            check_type(argname="argument tag_options", value=tag_options, expected_type=type_hints["tag_options"])
        return typing.cast(None, jsii.invoke(self, "associateTagOptions", [tag_options]))

    @jsii.member(jsii_name="constrainCloudFormationParameters")
    def constrain_cloud_formation_parameters(
        self,
        product: IProduct,
        *,
        rule: typing.Union["TemplateRule", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
    ) -> None:
        '''(experimental) Set provisioning rules for the product.

        :param product: -
        :param rule: (experimental) The rule with condition and assertions to apply to template.
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75eb81f90d7a08826e381548469c7f35fda88750fb983a1b1769d1db7710fa5)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
        options = CloudFormationRuleConstraintOptions(
            rule=rule, description=description, message_language=message_language
        )

        return typing.cast(None, jsii.invoke(self, "constrainCloudFormationParameters", [product, options]))

    @jsii.member(jsii_name="constrainTagUpdates")
    def constrain_tag_updates(
        self,
        product: IProduct,
        *,
        allow: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
    ) -> None:
        '''(experimental) Add a Resource Update Constraint.

        :param product: -
        :param allow: (experimental) Toggle for if users should be allowed to change/update tags on provisioned products. Default: true
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378804b86f7ea4c3b1e87c6890200d19c33d2f80034ccb3e90496150884f3e1d)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
        options = TagUpdateConstraintOptions(
            allow=allow, description=description, message_language=message_language
        )

        return typing.cast(None, jsii.invoke(self, "constrainTagUpdates", [product, options]))

    @jsii.member(jsii_name="deployWithStackSets")
    def deploy_with_stack_sets(
        self,
        product: IProduct,
        *,
        accounts: typing.Sequence[builtins.str],
        admin_role: _IRole_59af6f50,
        execution_role_name: builtins.str,
        regions: typing.Sequence[builtins.str],
        allow_stack_set_instance_operations: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
    ) -> None:
        '''(experimental) Configure deployment options using AWS Cloudformation StackSets.

        :param product: -
        :param accounts: (experimental) List of accounts to deploy stacks to.
        :param admin_role: (experimental) IAM role used to administer the StackSets configuration.
        :param execution_role_name: (experimental) IAM role used to provision the products in the Stacks.
        :param regions: (experimental) List of regions to deploy stacks to.
        :param allow_stack_set_instance_operations: (experimental) Wether to allow end users to create, update, and delete stacks. Default: false
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9974b51adafdd70190a96c8809cc9980c1c27643dfaf2000ef62723311607eb5)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
        options = StackSetsConstraintOptions(
            accounts=accounts,
            admin_role=admin_role,
            execution_role_name=execution_role_name,
            regions=regions,
            allow_stack_set_instance_operations=allow_stack_set_instance_operations,
            description=description,
            message_language=message_language,
        )

        return typing.cast(None, jsii.invoke(self, "deployWithStackSets", [product, options]))

    @jsii.member(jsii_name="generateUniqueHash")
    def _generate_unique_hash(self, value: builtins.str) -> builtins.str:
        '''(experimental) Create a unique id based off the L1 CfnPortfolio or the arn of an imported portfolio.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc1c77700b287580ca8e7e6e4ccf315aa80b8e2dc5c12af09006a4fa6319de7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.invoke(self, "generateUniqueHash", [value]))

    @jsii.member(jsii_name="giveAccessToGroup")
    def give_access_to_group(self, group: _IGroup_8a32caf8) -> None:
        '''(experimental) Associate portfolio with an IAM Group.

        :param group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e10d32a074e71199c93a8657add795167385f197c981f67508bd4ae9e63d209)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        return typing.cast(None, jsii.invoke(self, "giveAccessToGroup", [group]))

    @jsii.member(jsii_name="giveAccessToRole")
    def give_access_to_role(self, role: _IRole_59af6f50) -> None:
        '''(experimental) Associate portfolio with an IAM Role.

        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb787ddf8061fe500811a434aceba580bc1599195a70f58f3c632bd6e3bedf1c)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "giveAccessToRole", [role]))

    @jsii.member(jsii_name="giveAccessToUser")
    def give_access_to_user(self, user: _IUser_9d11d57d) -> None:
        '''(experimental) Associate portfolio with an IAM User.

        :param user: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afae341b5d27b8f67156e7372246a7bb9a28445a005122b210b64c7d476a113)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        return typing.cast(None, jsii.invoke(self, "giveAccessToUser", [user]))

    @jsii.member(jsii_name="notifyOnStackEvents")
    def notify_on_stack_events(
        self,
        product: IProduct,
        topic: _ITopic_465e36b9,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
    ) -> None:
        '''(experimental) Add notifications for supplied topics on the provisioned product.

        :param product: -
        :param topic: -
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a98d2096d213234b2f1bce083ca4524b700690c60b9c16034c1d0ebac1ed5c)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        options = CommonConstraintOptions(
            description=description, message_language=message_language
        )

        return typing.cast(None, jsii.invoke(self, "notifyOnStackEvents", [product, topic, options]))

    @jsii.member(jsii_name="setLaunchRole")
    def set_launch_role(
        self,
        product: IProduct,
        launch_role: _IRole_59af6f50,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
    ) -> None:
        '''(experimental) Force users to assume a certain role when launching a product.

        This sets the launch role using the role arn which is tied to the account this role exists in.
        This is useful if you will be provisioning products from the account where this role exists.
        If you intend to share the portfolio across accounts, use a local launch role.

        :param product: -
        :param launch_role: -
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1dc86d8b868bbcc44b77dbfb2adc61c7fc1b92482c17b6bf813763a81ce929)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument launch_role", value=launch_role, expected_type=type_hints["launch_role"])
        options = CommonConstraintOptions(
            description=description, message_language=message_language
        )

        return typing.cast(None, jsii.invoke(self, "setLaunchRole", [product, launch_role, options]))

    @jsii.member(jsii_name="setLocalLaunchRole")
    def set_local_launch_role(
        self,
        product: IProduct,
        launch_role: _IRole_59af6f50,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
    ) -> None:
        '''(experimental) Force users to assume a certain role when launching a product.

        The role name will be referenced by in the local account and must be set explicitly.
        This is useful when sharing the portfolio with multiple accounts.

        :param product: -
        :param launch_role: -
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c28e8e7d3f93c913fb8bf530058251f9b95ecde75ee1ea614705fbd982bf4c28)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument launch_role", value=launch_role, expected_type=type_hints["launch_role"])
        options = CommonConstraintOptions(
            description=description, message_language=message_language
        )

        return typing.cast(None, jsii.invoke(self, "setLocalLaunchRole", [product, launch_role, options]))

    @jsii.member(jsii_name="setLocalLaunchRoleName")
    def set_local_launch_role_name(
        self,
        product: IProduct,
        launch_role_name: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
    ) -> _IRole_59af6f50:
        '''(experimental) Force users to assume a certain role when launching a product.

        The role will be referenced by name in the local account instead of a static role arn.
        A role with this name will automatically be created and assumable by Service Catalog in this account.
        This is useful when sharing the portfolio with multiple accounts.

        :param product: -
        :param launch_role_name: -
        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a35466b19934456d99e3583327707187af7ad7807017ecfe8ffa9adac713ec3)
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument launch_role_name", value=launch_role_name, expected_type=type_hints["launch_role_name"])
        options = CommonConstraintOptions(
            description=description, message_language=message_language
        )

        return typing.cast(_IRole_59af6f50, jsii.invoke(self, "setLocalLaunchRoleName", [product, launch_role_name, options]))

    @jsii.member(jsii_name="shareWithAccount")
    def share_with_account(
        self,
        account_id: builtins.str,
        *,
        message_language: typing.Optional[MessageLanguage] = None,
        share_tag_options: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Initiate a portfolio share with another account.

        :param account_id: -
        :param message_language: (experimental) The message language of the share. Controls status and error message language for share. Default: - English
        :param share_tag_options: (experimental) Whether to share tagOptions as a part of the portfolio share. Default: - share not specified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17783777a200571366dee401b5a56eaa973f17f9b13d33c7e856129de68304bd)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        options = PortfolioShareOptions(
            message_language=message_language, share_tag_options=share_tag_options
        )

        return typing.cast(None, jsii.invoke(self, "shareWithAccount", [account_id, options]))

    @builtins.property
    @jsii.member(jsii_name="portfolioArn")
    def portfolio_arn(self) -> builtins.str:
        '''(experimental) The ARN of the portfolio.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioArn"))

    @builtins.property
    @jsii.member(jsii_name="portfolioId")
    def portfolio_id(self) -> builtins.str:
        '''(experimental) The ID of the portfolio.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "portfolioId"))


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.PortfolioProps",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "provider_name": "providerName",
        "description": "description",
        "message_language": "messageLanguage",
        "tag_options": "tagOptions",
    },
)
class PortfolioProps:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        provider_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
        tag_options: typing.Optional["TagOptions"] = None,
    ) -> None:
        '''(experimental) Properties for a Portfolio.

        :param display_name: (experimental) The name of the portfolio.
        :param provider_name: (experimental) The provider name.
        :param description: (experimental) Description for portfolio. Default: - No description provided
        :param message_language: (experimental) The message language. Controls language for status logging and errors. Default: - English
        :param tag_options: (experimental) TagOptions associated directly to a portfolio. Default: - No tagOptions provided

        :stability: experimental
        :exampleMetadata: infused

        Example::

            servicecatalog.Portfolio(self, "Portfolio",
                display_name="MyPortfolio",
                provider_name="MyTeam"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab658f8e281e8ab8e5e39bfc08f9f06d912f00a6713a3575a77bc225a08b1dda)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument message_language", value=message_language, expected_type=type_hints["message_language"])
            check_type(argname="argument tag_options", value=tag_options, expected_type=type_hints["tag_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "provider_name": provider_name,
        }
        if description is not None:
            self._values["description"] = description
        if message_language is not None:
            self._values["message_language"] = message_language
        if tag_options is not None:
            self._values["tag_options"] = tag_options

    @builtins.property
    def display_name(self) -> builtins.str:
        '''(experimental) The name of the portfolio.

        :stability: experimental
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_name(self) -> builtins.str:
        '''(experimental) The provider name.

        :stability: experimental
        '''
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for portfolio.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_language(self) -> typing.Optional[MessageLanguage]:
        '''(experimental) The message language.

        Controls language for
        status logging and errors.

        :default: - English

        :stability: experimental
        '''
        result = self._values.get("message_language")
        return typing.cast(typing.Optional[MessageLanguage], result)

    @builtins.property
    def tag_options(self) -> typing.Optional["TagOptions"]:
        '''(experimental) TagOptions associated directly to a portfolio.

        :default: - No tagOptions provided

        :stability: experimental
        '''
        result = self._values.get("tag_options")
        return typing.cast(typing.Optional["TagOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PortfolioProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.PortfolioShareOptions",
    jsii_struct_bases=[],
    name_mapping={
        "message_language": "messageLanguage",
        "share_tag_options": "shareTagOptions",
    },
)
class PortfolioShareOptions:
    def __init__(
        self,
        *,
        message_language: typing.Optional[MessageLanguage] = None,
        share_tag_options: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for portfolio share.

        :param message_language: (experimental) The message language of the share. Controls status and error message language for share. Default: - English
        :param share_tag_options: (experimental) Whether to share tagOptions as a part of the portfolio share. Default: - share not specified

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_servicecatalog as servicecatalog
            
            portfolio_share_options = servicecatalog.PortfolioShareOptions(
                message_language=servicecatalog.MessageLanguage.EN,
                share_tag_options=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f99f25c56b82c0a8bb46800c7beb2bbaf3b7de07dd26b49e2f8d7dec0cb82f)
            check_type(argname="argument message_language", value=message_language, expected_type=type_hints["message_language"])
            check_type(argname="argument share_tag_options", value=share_tag_options, expected_type=type_hints["share_tag_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message_language is not None:
            self._values["message_language"] = message_language
        if share_tag_options is not None:
            self._values["share_tag_options"] = share_tag_options

    @builtins.property
    def message_language(self) -> typing.Optional[MessageLanguage]:
        '''(experimental) The message language of the share.

        Controls status and error message language for share.

        :default: - English

        :stability: experimental
        '''
        result = self._values.get("message_language")
        return typing.cast(typing.Optional[MessageLanguage], result)

    @builtins.property
    def share_tag_options(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to share tagOptions as a part of the portfolio share.

        :default: - share not specified

        :stability: experimental
        '''
        result = self._values.get("share_tag_options")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PortfolioShareOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IProduct)
class Product(
    _Resource_abff4495,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_servicecatalog.Product",
):
    '''(experimental) Abstract class for Service Catalog Product.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_servicecatalog as servicecatalog
        
        product = servicecatalog.Product.from_product_arn(self, "MyProduct", "productArn")
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: (experimental) The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: (experimental) ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: (experimental) The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: (experimental) The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa330b300f438c46390a33585104e3eb6468252365b1babad66505622f8ea9cb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _ResourceProps_9b554c0f(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromProductArn")
    @builtins.classmethod
    def from_product_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        product_arn: builtins.str,
    ) -> IProduct:
        '''(experimental) Creates a Product construct that represents an external product.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param product_arn: Product Arn.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7166e186ba980c79cc7b60768e42147e814bc9c5ad5e35d60ef4515f25e68f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument product_arn", value=product_arn, expected_type=type_hints["product_arn"])
        return typing.cast(IProduct, jsii.sinvoke(cls, "fromProductArn", [scope, id, product_arn]))

    @jsii.member(jsii_name="associateTagOptions")
    def associate_tag_options(self, tag_options: "TagOptions") -> None:
        '''(experimental) Associate Tag Options.

        A TagOption is a key-value pair managed in AWS Service Catalog.
        It is not an AWS tag, but serves as a template for creating an AWS tag based on the TagOption.

        :param tag_options: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61863236bab2ac90a54c9c2f900bef6b895ec83a99a17ad5412a8490b405fb4b)
            check_type(argname="argument tag_options", value=tag_options, expected_type=type_hints["tag_options"])
        return typing.cast(None, jsii.invoke(self, "associateTagOptions", [tag_options]))

    @builtins.property
    @jsii.member(jsii_name="productArn")
    @abc.abstractmethod
    def product_arn(self) -> builtins.str:
        '''(experimental) The ARN of the product.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="productId")
    @abc.abstractmethod
    def product_id(self) -> builtins.str:
        '''(experimental) The id of the product.

        :stability: experimental
        '''
        ...


class _ProductProxy(
    Product,
    jsii.proxy_for(_Resource_abff4495), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="productArn")
    def product_arn(self) -> builtins.str:
        '''(experimental) The ARN of the product.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "productArn"))

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''(experimental) The id of the product.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "productId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Product).__jsii_proxy_class__ = lambda : _ProductProxy


class ProductStack(
    _Stack_9f43e4a3,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.ProductStack",
):
    '''(experimental) A Service Catalog product stack, which is similar in form to a Cloudformation nested stack.

    You can add the resources to this stack that you want to define for your service catalog product.

    This stack will not be treated as an independent deployment
    artifact (won't be listed in "cdk list" or deployable through "cdk deploy"),
    but rather only synthesized as a template and uploaded as an asset to S3.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as s3
        import monocdk as cdk
        
        
        class S3BucketProduct(servicecatalog.ProductStack):
            def __init__(self, scope, id):
                super().__init__(scope, id)
        
                s3.Bucket(self, "BucketProduct")
        
        product = servicecatalog.CloudFormationProduct(self, "Product",
            product_name="My Product",
            owner="Product Owner",
            product_versions=[s3.aws_servicecatalog.CloudFormationProductVersion(
                product_version_name="v1",
                cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(S3BucketProduct(self, "S3BucketProduct"))
            )
            ]
        )
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb990be77c79429898bf492f8045ab6e82e07bda61299c0db3bf88f361c243a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="templateFile")
    def template_file(self) -> builtins.str:
        '''(experimental) The name of the CloudFormation template file emitted to the output directory during synthesis.

        Example value: ``MyStack.template.json``

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateFile"))


class ProductStackHistory(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.ProductStackHistory",
):
    '''(experimental) A Construct that contains a Service Catalog product stack with its previous deployments maintained.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as s3
        import monocdk as cdk
        
        
        class S3BucketProduct(servicecatalog.ProductStack):
            def __init__(self, scope, id):
                super().__init__(scope, id)
        
                s3.Bucket(self, "BucketProductV2")
        
        product_stack_history = servicecatalog.ProductStackHistory(self, "ProductStackHistory",
            product_stack=S3BucketProduct(self, "S3BucketProduct"),
            current_version_name="v2",
            current_version_locked=True
        )
        
        product = servicecatalog.CloudFormationProduct(self, "MyFirstProduct",
            product_name="My Product",
            owner="Product Owner",
            product_versions=[
                product_stack_history.current_version()
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        current_version_locked: builtins.bool,
        current_version_name: builtins.str,
        product_stack: ProductStack,
        description: typing.Optional[builtins.str] = None,
        directory: typing.Optional[builtins.str] = None,
        validate_template: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param current_version_locked: (experimental) If this is set to true, the ProductStack will not be overwritten if a snapshot is found for the currentVersionName.
        :param current_version_name: (experimental) The current version name of the ProductStack.
        :param product_stack: (experimental) The ProductStack whose history will be retained as a snapshot.
        :param description: (experimental) The description of the product version. Default: - No description provided
        :param directory: (experimental) The directory where template snapshots will be stored. Default: 'product-stack-snapshots'
        :param validate_template: (experimental) Whether the specified product template will be validated by CloudFormation. If turned off, an invalid template configuration can be stored. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f987935770e71a41b2388a3d716ea51987c9f5dd16a1c6669f521222a1ed315d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ProductStackHistoryProps(
            current_version_locked=current_version_locked,
            current_version_name=current_version_name,
            product_stack=product_stack,
            description=description,
            directory=directory,
            validate_template=validate_template,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="currentVersion")
    def current_version(self) -> CloudFormationProductVersion:
        '''(experimental) Retains product stack template as a snapshot when deployed and retrieves a CloudFormationProductVersion for the current product version.

        :stability: experimental
        '''
        return typing.cast(CloudFormationProductVersion, jsii.invoke(self, "currentVersion", []))

    @jsii.member(jsii_name="versionFromSnapshot")
    def version_from_snapshot(
        self,
        product_version_name: builtins.str,
    ) -> CloudFormationProductVersion:
        '''(experimental) Retrieves a CloudFormationProductVersion from a previously deployed productVersionName.

        :param product_version_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f05e4148190a5ffca2b254291025a7033e0c878cac04b28caf403b22cd1d9c)
            check_type(argname="argument product_version_name", value=product_version_name, expected_type=type_hints["product_version_name"])
        return typing.cast(CloudFormationProductVersion, jsii.invoke(self, "versionFromSnapshot", [product_version_name]))


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.ProductStackHistoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "current_version_locked": "currentVersionLocked",
        "current_version_name": "currentVersionName",
        "product_stack": "productStack",
        "description": "description",
        "directory": "directory",
        "validate_template": "validateTemplate",
    },
)
class ProductStackHistoryProps:
    def __init__(
        self,
        *,
        current_version_locked: builtins.bool,
        current_version_name: builtins.str,
        product_stack: ProductStack,
        description: typing.Optional[builtins.str] = None,
        directory: typing.Optional[builtins.str] = None,
        validate_template: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for a ProductStackHistory.

        :param current_version_locked: (experimental) If this is set to true, the ProductStack will not be overwritten if a snapshot is found for the currentVersionName.
        :param current_version_name: (experimental) The current version name of the ProductStack.
        :param product_stack: (experimental) The ProductStack whose history will be retained as a snapshot.
        :param description: (experimental) The description of the product version. Default: - No description provided
        :param directory: (experimental) The directory where template snapshots will be stored. Default: 'product-stack-snapshots'
        :param validate_template: (experimental) Whether the specified product template will be validated by CloudFormation. If turned off, an invalid template configuration can be stored. Default: true

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as s3
            import monocdk as cdk
            
            
            class S3BucketProduct(servicecatalog.ProductStack):
                def __init__(self, scope, id):
                    super().__init__(scope, id)
            
                    s3.Bucket(self, "BucketProductV2")
            
            product_stack_history = servicecatalog.ProductStackHistory(self, "ProductStackHistory",
                product_stack=S3BucketProduct(self, "S3BucketProduct"),
                current_version_name="v2",
                current_version_locked=True
            )
            
            product = servicecatalog.CloudFormationProduct(self, "MyFirstProduct",
                product_name="My Product",
                owner="Product Owner",
                product_versions=[
                    product_stack_history.current_version()
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13790d59f1daf3d5ef2810019cad1b4f1e0d7620175cd02c0b2e2a053470b00d)
            check_type(argname="argument current_version_locked", value=current_version_locked, expected_type=type_hints["current_version_locked"])
            check_type(argname="argument current_version_name", value=current_version_name, expected_type=type_hints["current_version_name"])
            check_type(argname="argument product_stack", value=product_stack, expected_type=type_hints["product_stack"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
            check_type(argname="argument validate_template", value=validate_template, expected_type=type_hints["validate_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "current_version_locked": current_version_locked,
            "current_version_name": current_version_name,
            "product_stack": product_stack,
        }
        if description is not None:
            self._values["description"] = description
        if directory is not None:
            self._values["directory"] = directory
        if validate_template is not None:
            self._values["validate_template"] = validate_template

    @builtins.property
    def current_version_locked(self) -> builtins.bool:
        '''(experimental) If this is set to true, the ProductStack will not be overwritten if a snapshot is found for the currentVersionName.

        :stability: experimental
        '''
        result = self._values.get("current_version_locked")
        assert result is not None, "Required property 'current_version_locked' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def current_version_name(self) -> builtins.str:
        '''(experimental) The current version name of the ProductStack.

        :stability: experimental
        '''
        result = self._values.get("current_version_name")
        assert result is not None, "Required property 'current_version_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_stack(self) -> ProductStack:
        '''(experimental) The ProductStack whose history will be retained as a snapshot.

        :stability: experimental
        '''
        result = self._values.get("product_stack")
        assert result is not None, "Required property 'product_stack' is missing"
        return typing.cast(ProductStack, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the product version.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) The directory where template snapshots will be stored.

        :default: 'product-stack-snapshots'

        :stability: experimental
        '''
        result = self._values.get("directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate_template(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the specified product template will be validated by CloudFormation.

        If turned off, an invalid template configuration can be stored.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("validate_template")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProductStackHistoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.StackSetsConstraintOptions",
    jsii_struct_bases=[CommonConstraintOptions],
    name_mapping={
        "description": "description",
        "message_language": "messageLanguage",
        "accounts": "accounts",
        "admin_role": "adminRole",
        "execution_role_name": "executionRoleName",
        "regions": "regions",
        "allow_stack_set_instance_operations": "allowStackSetInstanceOperations",
    },
)
class StackSetsConstraintOptions(CommonConstraintOptions):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
        accounts: typing.Sequence[builtins.str],
        admin_role: _IRole_59af6f50,
        execution_role_name: builtins.str,
        regions: typing.Sequence[builtins.str],
        allow_stack_set_instance_operations: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for deploying with Stackset, which creates a StackSet constraint.

        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English
        :param accounts: (experimental) List of accounts to deploy stacks to.
        :param admin_role: (experimental) IAM role used to administer the StackSets configuration.
        :param execution_role_name: (experimental) IAM role used to provision the products in the Stacks.
        :param regions: (experimental) List of regions to deploy stacks to.
        :param allow_stack_set_instance_operations: (experimental) Wether to allow end users to create, update, and delete stacks. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as iam
            
            # portfolio: servicecatalog.Portfolio
            # product: servicecatalog.CloudFormationProduct
            
            
            admin_role = iam.Role(self, "AdminRole",
                assumed_by=iam.AccountRootPrincipal()
            )
            
            portfolio.deploy_with_stack_sets(product,
                accounts=["012345678901", "012345678902", "012345678903"],
                regions=["us-west-1", "us-east-1", "us-west-2", "us-east-1"],
                admin_role=admin_role,
                execution_role_name="SCStackSetExecutionRole",  # Name of role deployed in end users accounts.
                allow_stack_set_instance_operations=True
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1afdd778c43fc28aa0c6aaecaa71e4259080199ec8d1b4241fc7e5e4a97c01b0)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument message_language", value=message_language, expected_type=type_hints["message_language"])
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
            check_type(argname="argument admin_role", value=admin_role, expected_type=type_hints["admin_role"])
            check_type(argname="argument execution_role_name", value=execution_role_name, expected_type=type_hints["execution_role_name"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument allow_stack_set_instance_operations", value=allow_stack_set_instance_operations, expected_type=type_hints["allow_stack_set_instance_operations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accounts": accounts,
            "admin_role": admin_role,
            "execution_role_name": execution_role_name,
            "regions": regions,
        }
        if description is not None:
            self._values["description"] = description
        if message_language is not None:
            self._values["message_language"] = message_language
        if allow_stack_set_instance_operations is not None:
            self._values["allow_stack_set_instance_operations"] = allow_stack_set_instance_operations

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the constraint.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_language(self) -> typing.Optional[MessageLanguage]:
        '''(experimental) The language code.

        Configures the language for error messages from service catalog.

        :default: - English

        :stability: experimental
        '''
        result = self._values.get("message_language")
        return typing.cast(typing.Optional[MessageLanguage], result)

    @builtins.property
    def accounts(self) -> typing.List[builtins.str]:
        '''(experimental) List of accounts to deploy stacks to.

        :stability: experimental
        '''
        result = self._values.get("accounts")
        assert result is not None, "Required property 'accounts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def admin_role(self) -> _IRole_59af6f50:
        '''(experimental) IAM role used to administer the StackSets configuration.

        :stability: experimental
        '''
        result = self._values.get("admin_role")
        assert result is not None, "Required property 'admin_role' is missing"
        return typing.cast(_IRole_59af6f50, result)

    @builtins.property
    def execution_role_name(self) -> builtins.str:
        '''(experimental) IAM role used to provision the products in the Stacks.

        :stability: experimental
        '''
        result = self._values.get("execution_role_name")
        assert result is not None, "Required property 'execution_role_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regions(self) -> typing.List[builtins.str]:
        '''(experimental) List of regions to deploy stacks to.

        :stability: experimental
        '''
        result = self._values.get("regions")
        assert result is not None, "Required property 'regions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allow_stack_set_instance_operations(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Wether to allow end users to create, update, and delete stacks.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("allow_stack_set_instance_operations")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackSetsConstraintOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TagOptions(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.TagOptions",
):
    '''(experimental) Defines a set of TagOptions, which are a list of key-value pairs managed in AWS Service Catalog.

    It is not an AWS tag, but serves as a template for creating an AWS tag based on the TagOption.
    See https://docs.aws.amazon.com/servicecatalog/latest/adminguide/tagoptions.html

    :stability: experimental
    :resource: AWS::ServiceCatalog::TagOption
    :exampleMetadata: infused

    Example::

        # portfolio: servicecatalog.Portfolio
        # product: servicecatalog.CloudFormationProduct
        
        
        tag_options_for_portfolio = servicecatalog.TagOptions(self, "OrgTagOptions",
            allowed_values_for_tags={
                "Group": ["finance", "engineering", "marketing", "research"],
                "CostCenter": ["01", "02", "03"]
            }
        )
        portfolio.associate_tag_options(tag_options_for_portfolio)
        
        tag_options_for_product = servicecatalog.TagOptions(self, "ProductTagOptions",
            allowed_values_for_tags={
                "Environment": ["dev", "alpha", "prod"]
            }
        )
        product.associate_tag_options(tag_options_for_product)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allowed_values_for_tags: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allowed_values_for_tags: (experimental) The values that are allowed to be set for specific tags. The keys of the map represent the tag keys, and the values of the map are a list of allowed values for that particular tag key.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7567d6a3a803f28a0d0e7eb84ce369487acfb437b6d71889291c92f56e00e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TagOptionsProps(allowed_values_for_tags=allowed_values_for_tags)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.TagOptionsProps",
    jsii_struct_bases=[],
    name_mapping={"allowed_values_for_tags": "allowedValuesForTags"},
)
class TagOptionsProps:
    def __init__(
        self,
        *,
        allowed_values_for_tags: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
    ) -> None:
        '''(experimental) Properties for TagOptions.

        :param allowed_values_for_tags: (experimental) The values that are allowed to be set for specific tags. The keys of the map represent the tag keys, and the values of the map are a list of allowed values for that particular tag key.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # portfolio: servicecatalog.Portfolio
            # product: servicecatalog.CloudFormationProduct
            
            
            tag_options_for_portfolio = servicecatalog.TagOptions(self, "OrgTagOptions",
                allowed_values_for_tags={
                    "Group": ["finance", "engineering", "marketing", "research"],
                    "CostCenter": ["01", "02", "03"]
                }
            )
            portfolio.associate_tag_options(tag_options_for_portfolio)
            
            tag_options_for_product = servicecatalog.TagOptions(self, "ProductTagOptions",
                allowed_values_for_tags={
                    "Environment": ["dev", "alpha", "prod"]
                }
            )
            product.associate_tag_options(tag_options_for_product)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f11317240f375930315d794ff7864118108486cbfe378a0eaae373e7fd99dc6)
            check_type(argname="argument allowed_values_for_tags", value=allowed_values_for_tags, expected_type=type_hints["allowed_values_for_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_values_for_tags": allowed_values_for_tags,
        }

    @builtins.property
    def allowed_values_for_tags(
        self,
    ) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''(experimental) The values that are allowed to be set for specific tags.

        The keys of the map represent the tag keys,
        and the values of the map are a list of allowed values for that particular tag key.

        :stability: experimental
        '''
        result = self._values.get("allowed_values_for_tags")
        assert result is not None, "Required property 'allowed_values_for_tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagOptionsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.TagUpdateConstraintOptions",
    jsii_struct_bases=[CommonConstraintOptions],
    name_mapping={
        "description": "description",
        "message_language": "messageLanguage",
        "allow": "allow",
    },
)
class TagUpdateConstraintOptions(CommonConstraintOptions):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
        allow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for ResourceUpdateConstraint.

        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English
        :param allow: (experimental) Toggle for if users should be allowed to change/update tags on provisioned products. Default: true

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # portfolio: servicecatalog.Portfolio
            # product: servicecatalog.CloudFormationProduct
            
            
            # to disable tag updates:
            portfolio.constrain_tag_updates(product,
                allow=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8449641a3ab9e932e14f03a58ac3c7bd157bdb6fa5ea8f2467dac63f49acd2)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument message_language", value=message_language, expected_type=type_hints["message_language"])
            check_type(argname="argument allow", value=allow, expected_type=type_hints["allow"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if message_language is not None:
            self._values["message_language"] = message_language
        if allow is not None:
            self._values["allow"] = allow

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the constraint.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_language(self) -> typing.Optional[MessageLanguage]:
        '''(experimental) The language code.

        Configures the language for error messages from service catalog.

        :default: - English

        :stability: experimental
        '''
        result = self._values.get("message_language")
        return typing.cast(typing.Optional[MessageLanguage], result)

    @builtins.property
    def allow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Toggle for if users should be allowed to change/update tags on provisioned products.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("allow")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagUpdateConstraintOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.TemplateRule",
    jsii_struct_bases=[],
    name_mapping={
        "assertions": "assertions",
        "rule_name": "ruleName",
        "condition": "condition",
    },
)
class TemplateRule:
    def __init__(
        self,
        *,
        assertions: typing.Sequence[typing.Union["TemplateRuleAssertion", typing.Dict[builtins.str, typing.Any]]],
        rule_name: builtins.str,
        condition: typing.Optional[_ICfnRuleConditionExpression_5f18240f] = None,
    ) -> None:
        '''(experimental) Defines the provisioning template constraints.

        :param assertions: (experimental) A list of assertions that make up the rule.
        :param rule_name: (experimental) Name of the rule.
        :param condition: (experimental) Specify when to apply rule with a rule-specific intrinsic function. Default: - no rule condition provided

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as cdk
            
            # portfolio: servicecatalog.Portfolio
            # product: servicecatalog.CloudFormationProduct
            
            
            portfolio.constrain_cloud_formation_parameters(product,
                rule=cdk.aws_servicecatalog.TemplateRule(
                    rule_name="testInstanceType",
                    condition=cdk.Fn.condition_equals(cdk.Fn.ref("Environment"), "test"),
                    assertions=[cdk.aws_servicecatalog.TemplateRuleAssertion(
                        assert=cdk.Fn.condition_contains(["t2.micro", "t2.small"], cdk.Fn.ref("InstanceType")),
                        description="For test environment, the instance type should be small"
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e464274c3532cf833ab69aec7ffa6b1dbb213466f91170c4b10a2ce79ffb79c)
            check_type(argname="argument assertions", value=assertions, expected_type=type_hints["assertions"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assertions": assertions,
            "rule_name": rule_name,
        }
        if condition is not None:
            self._values["condition"] = condition

    @builtins.property
    def assertions(self) -> typing.List["TemplateRuleAssertion"]:
        '''(experimental) A list of assertions that make up the rule.

        :stability: experimental
        '''
        result = self._values.get("assertions")
        assert result is not None, "Required property 'assertions' is missing"
        return typing.cast(typing.List["TemplateRuleAssertion"], result)

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''(experimental) Name of the rule.

        :stability: experimental
        '''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional[_ICfnRuleConditionExpression_5f18240f]:
        '''(experimental) Specify when to apply rule with a rule-specific intrinsic function.

        :default: - no rule condition provided

        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[_ICfnRuleConditionExpression_5f18240f], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TemplateRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.TemplateRuleAssertion",
    jsii_struct_bases=[],
    name_mapping={"assert_": "assert", "description": "description"},
)
class TemplateRuleAssertion:
    def __init__(
        self,
        *,
        assert_: _ICfnRuleConditionExpression_5f18240f,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) An assertion within a template rule, defined by intrinsic functions.

        :param assert_: (experimental) The assertion condition.
        :param description: (experimental) The description for the asssertion. Default: - no description provided for the assertion.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_servicecatalog as servicecatalog
            
            # cfn_rule_condition_expression: monocdk.ICfnRuleConditionExpression
            
            template_rule_assertion = servicecatalog.TemplateRuleAssertion(
                assert=cfn_rule_condition_expression,
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101fcfa003a72e800257dbcb55ab9b9b4bd530ef944612818a8de8037d58d292)
            check_type(argname="argument assert_", value=assert_, expected_type=type_hints["assert_"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assert_": assert_,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def assert_(self) -> _ICfnRuleConditionExpression_5f18240f:
        '''(experimental) The assertion condition.

        :stability: experimental
        '''
        result = self._values.get("assert_")
        assert result is not None, "Required property 'assert_' is missing"
        return typing.cast(_ICfnRuleConditionExpression_5f18240f, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description for the asssertion.

        :default: - no description provided for the assertion.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TemplateRuleAssertion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudFormationProduct(
    Product,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalog.CloudFormationProduct",
):
    '''(experimental) A Service Catalog Cloudformation Product.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as s3
        import monocdk as cdk
        
        
        class S3BucketProduct(servicecatalog.ProductStack):
            def __init__(self, scope, id):
                super().__init__(scope, id)
        
                s3.Bucket(self, "BucketProduct")
        
        product = servicecatalog.CloudFormationProduct(self, "Product",
            product_name="My Product",
            owner="Product Owner",
            product_versions=[s3.aws_servicecatalog.CloudFormationProductVersion(
                product_version_name="v1",
                cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(S3BucketProduct(self, "S3BucketProduct"))
            )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        owner: builtins.str,
        product_name: builtins.str,
        product_versions: typing.Sequence[typing.Union[CloudFormationProductVersion, typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        distributor: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
        replace_product_version_ids: typing.Optional[builtins.bool] = None,
        support_description: typing.Optional[builtins.str] = None,
        support_email: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
        tag_options: typing.Optional[TagOptions] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param owner: (experimental) The owner of the product.
        :param product_name: (experimental) The name of the product.
        :param product_versions: (experimental) The configuration of the product version.
        :param description: (experimental) The description of the product. Default: - No description provided
        :param distributor: (experimental) The distributor of the product. Default: - No distributor provided
        :param message_language: (experimental) The language code. Controls language for logging and errors. Default: - English
        :param replace_product_version_ids: (experimental) Whether to give provisioning artifacts a new unique identifier when the product attributes or provisioning artifacts is updated. Default: false
        :param support_description: (experimental) The support information about the product. Default: - No support description provided
        :param support_email: (experimental) The contact email for product support. Default: - No support email provided
        :param support_url: (experimental) The contact URL for product support. Default: - No support URL provided
        :param tag_options: (experimental) TagOptions associated directly to a product. Default: - No tagOptions provided

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e38f8dd9679cf2b1355e43e418efc2c485c8339e0cca90b5c72f0a6361759bc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudFormationProductProps(
            owner=owner,
            product_name=product_name,
            product_versions=product_versions,
            description=description,
            distributor=distributor,
            message_language=message_language,
            replace_product_version_ids=replace_product_version_ids,
            support_description=support_description,
            support_email=support_email,
            support_url=support_url,
            tag_options=tag_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="productArn")
    def product_arn(self) -> builtins.str:
        '''(experimental) The ARN of the product.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "productArn"))

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        '''(experimental) The id of the product.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "productId"))


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalog.CloudFormationRuleConstraintOptions",
    jsii_struct_bases=[CommonConstraintOptions],
    name_mapping={
        "description": "description",
        "message_language": "messageLanguage",
        "rule": "rule",
    },
)
class CloudFormationRuleConstraintOptions(CommonConstraintOptions):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        message_language: typing.Optional[MessageLanguage] = None,
        rule: typing.Union[TemplateRule, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Properties for provisoning rule constraint.

        :param description: (experimental) The description of the constraint. Default: - No description provided
        :param message_language: (experimental) The language code. Configures the language for error messages from service catalog. Default: - English
        :param rule: (experimental) The rule with condition and assertions to apply to template.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as cdk
            
            # portfolio: servicecatalog.Portfolio
            # product: servicecatalog.CloudFormationProduct
            
            
            portfolio.constrain_cloud_formation_parameters(product,
                rule=cdk.aws_servicecatalog.TemplateRule(
                    rule_name="testInstanceType",
                    condition=cdk.Fn.condition_equals(cdk.Fn.ref("Environment"), "test"),
                    assertions=[cdk.aws_servicecatalog.TemplateRuleAssertion(
                        assert=cdk.Fn.condition_contains(["t2.micro", "t2.small"], cdk.Fn.ref("InstanceType")),
                        description="For test environment, the instance type should be small"
                    )]
                )
            )
        '''
        if isinstance(rule, dict):
            rule = TemplateRule(**rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__343d88b9ba0b997d099e92e0129d5f0df694b0e992ab3e5ac51fa18c5a022ae3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument message_language", value=message_language, expected_type=type_hints["message_language"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
        }
        if description is not None:
            self._values["description"] = description
        if message_language is not None:
            self._values["message_language"] = message_language

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the constraint.

        :default: - No description provided

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_language(self) -> typing.Optional[MessageLanguage]:
        '''(experimental) The language code.

        Configures the language for error messages from service catalog.

        :default: - English

        :stability: experimental
        '''
        result = self._values.get("message_language")
        return typing.cast(typing.Optional[MessageLanguage], result)

    @builtins.property
    def rule(self) -> TemplateRule:
        '''(experimental) The rule with condition and assertions to apply to template.

        :stability: experimental
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(TemplateRule, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationRuleConstraintOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAcceptedPortfolioShare",
    "CfnAcceptedPortfolioShareProps",
    "CfnCloudFormationProduct",
    "CfnCloudFormationProductProps",
    "CfnCloudFormationProvisionedProduct",
    "CfnCloudFormationProvisionedProductProps",
    "CfnLaunchNotificationConstraint",
    "CfnLaunchNotificationConstraintProps",
    "CfnLaunchRoleConstraint",
    "CfnLaunchRoleConstraintProps",
    "CfnLaunchTemplateConstraint",
    "CfnLaunchTemplateConstraintProps",
    "CfnPortfolio",
    "CfnPortfolioPrincipalAssociation",
    "CfnPortfolioPrincipalAssociationProps",
    "CfnPortfolioProductAssociation",
    "CfnPortfolioProductAssociationProps",
    "CfnPortfolioProps",
    "CfnPortfolioShare",
    "CfnPortfolioShareProps",
    "CfnResourceUpdateConstraint",
    "CfnResourceUpdateConstraintProps",
    "CfnServiceAction",
    "CfnServiceActionAssociation",
    "CfnServiceActionAssociationProps",
    "CfnServiceActionProps",
    "CfnStackSetConstraint",
    "CfnStackSetConstraintProps",
    "CfnTagOption",
    "CfnTagOptionAssociation",
    "CfnTagOptionAssociationProps",
    "CfnTagOptionProps",
    "CloudFormationProduct",
    "CloudFormationProductProps",
    "CloudFormationProductVersion",
    "CloudFormationRuleConstraintOptions",
    "CloudFormationTemplate",
    "CloudFormationTemplateConfig",
    "CommonConstraintOptions",
    "IPortfolio",
    "IProduct",
    "MessageLanguage",
    "Portfolio",
    "PortfolioProps",
    "PortfolioShareOptions",
    "Product",
    "ProductStack",
    "ProductStackHistory",
    "ProductStackHistoryProps",
    "StackSetsConstraintOptions",
    "TagOptions",
    "TagOptionsProps",
    "TagUpdateConstraintOptions",
    "TemplateRule",
    "TemplateRuleAssertion",
]

publication.publish()

def _typecheckingstub__9fb685df489c56024f8584f078468fe872941fb5734b5485ed201af4e721ed19(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    portfolio_id: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a594d112c33c8a7678141e5512d38e6f1738953f348d84b057f4c7f9aa369cb0(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f063f1cc3014b1e4639b28b313fb1c35feb9697f829e6dc0f778b4724d87a49(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd011ab55e173816627584592626db7d1d9bf2e4ddfe30b86058c9bbe6581ec2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4cf33d08399271a317321a1c29080e72fefb142166f8119dc2e8bd73602381(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc161e45ef01366620d0107e45cb474853606638759a39226147b5128acab75(
    *,
    portfolio_id: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cad7358dc48114856f78b9238c514f92f486640d9319eeb7127576712e01f8(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    owner: builtins.str,
    provisioning_artifact_parameters: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    distributor: typing.Optional[builtins.str] = None,
    replace_provisioning_artifacts: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    support_description: typing.Optional[builtins.str] = None,
    support_email: typing.Optional[builtins.str] = None,
    support_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4709033ec20ff41693d6395749a0f777254b68e8600cda3f186f665288584416(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd43bdde6c7f8345cdb7ef2aed7dd78a02e1a29fad2298531ba12239c9501ea6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94bac71d02c79d66842f08d94855cd9e2fd2d92f22bd1d1f12f99ee88b5518e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42cb8cc3df90c31867c0600eefb74a22f4fda9a2135df6f6453d9e3062bfe2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac2d5706abd7a999aff9b2574cf3355c851c2952cafd12cefa8dd4451618e66(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f6f0ce7af309724786f8527e605d07933f179d669d6e1122b589589020e6f6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1735f7671b290d9fa5b672bee0f1ce22d8ac2db43d4514bf66b793293362834c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0df9c79c44d4293504a7e33afbb958ab5638c675d3d06867bafbd290091d8d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f109e8f99080405dc4ad742d34af2790365f6d4487757cf510c81934d6902a65(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd335ddbf12141b271489844380936290547469f639a8b67bd0f6328aac0b23c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1caa6ae9c26a7fa52ba2c3dad08028190f96747b02e6f48fdbcde66cda81df(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0422bc0b2864b71a4cdfbd8b9e223a6a1cf9f5d6aa441682224609ac5e15a93f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1dcf62559e2918572877ef85a560c4c0674eaabd8857c89ef9a439f3033027(
    *,
    info: typing.Any,
    description: typing.Optional[builtins.str] = None,
    disable_template_validation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fa67596851c515b37a8c4ff84fb8c54e715b89840507c8bf46ced4e237f364(
    *,
    name: builtins.str,
    owner: builtins.str,
    provisioning_artifact_parameters: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    distributor: typing.Optional[builtins.str] = None,
    replace_provisioning_artifacts: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    support_description: typing.Optional[builtins.str] = None,
    support_email: typing.Optional[builtins.str] = None,
    support_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cdf2f6d31986e586e0370596d1bf4e2f8f63a7a22782662dc406b1c2821803(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    accept_language: typing.Optional[builtins.str] = None,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path_id: typing.Optional[builtins.str] = None,
    path_name: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    product_name: typing.Optional[builtins.str] = None,
    provisioned_product_name: typing.Optional[builtins.str] = None,
    provisioning_artifact_id: typing.Optional[builtins.str] = None,
    provisioning_artifact_name: typing.Optional[builtins.str] = None,
    provisioning_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    provisioning_preferences: typing.Optional[typing.Union[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd772f3aec3eecff526c370e71882091d82549c0538a95bf3a6a00c793cff81(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa15c208374c1d975fee78bbcbaf43155172e03a50d6be47f9de98a9cf2df40(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f9a53b9c44c1bac61c4a56a8f4de52b50c3091239021bce241e8fc6d9f4062(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233482fcfa1eefbbaa22fd2475d6b587133bea32dc599f2ccad985cbb87da925(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b389399c02209eb56af05384e6e61138cb7d4765374ce1284a02e850502e2f01(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6cbc15f02e92b6dfcc798a060ec258fc1b231e6a4b8493f5c03de4cb8dc4187(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcda3750f994a44ece3b4e21ab06359e5aab38630826c4eea0ad0689470a81f0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aef01a453134a34ec9c688286808598351db7e27ec9c657d2ebcb5a7da44d99(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515f7712d787f2e88c49a8cd030474ad8faee4aba2bf48f779eb9c2d0282af62(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a082e13f4b9b5df4d1826bdab2c82de578905a4e81c37753809c128a43ec1d10(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133037dce530aba0bd62160004f3f6320364d6c3c3840d76e7eb814b94baf03b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa95e9be68bac7b93538bf80ceca916aa3d01b03c95739ac4137c769eba050d(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a76e672cafd782295227b9e6afd1d950fc994b4d3b80e5ea7e338d24b14980(
    value: typing.Optional[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96057e2186b4eff04d05e767a288e525283e66d8c6693ecc3be1c9131b51920a(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f993219da7057d53fa76a310e0ba2a8a553f28e500c74566d14adf1b7f7dce6(
    *,
    stack_set_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_set_failure_tolerance_count: typing.Optional[jsii.Number] = None,
    stack_set_failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
    stack_set_max_concurrency_count: typing.Optional[jsii.Number] = None,
    stack_set_max_concurrency_percentage: typing.Optional[jsii.Number] = None,
    stack_set_operation_type: typing.Optional[builtins.str] = None,
    stack_set_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d74d7302604d6f1567269adcc84c2c44abe22094fcc16d4b6930fdf9868dbe5(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path_id: typing.Optional[builtins.str] = None,
    path_name: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    product_name: typing.Optional[builtins.str] = None,
    provisioned_product_name: typing.Optional[builtins.str] = None,
    provisioning_artifact_id: typing.Optional[builtins.str] = None,
    provisioning_artifact_name: typing.Optional[builtins.str] = None,
    provisioning_parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    provisioning_preferences: typing.Optional[typing.Union[typing.Union[CfnCloudFormationProvisionedProduct.ProvisioningPreferencesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536950d77e09c8d6b305a53d8cbfea275535b25572087dca563e95d37b9310dc(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    notification_arns: typing.Sequence[builtins.str],
    portfolio_id: builtins.str,
    product_id: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7fb9aa8135ecbe5a18780164e4c20f57928b860b2ff5837978995b63187471(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b926cb591c6ea74154daadf733e5f61a552829ba7a6d0740f8abd0a835adf73f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82aa67d98dabc54f3e69e96d580aa1e07ea11764169e1ac1af9b8063ce40d92f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087b604954b3203787d894de82c10ee243af370e7491788ac12913c9db57ae5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01292e2dd81e21d9c04fef071430746156ec4169f4c6f78725df409a9489e416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe0941a42f3afdee20524cecf1f3be46c4eb5ca2a5c63705faab1325f7b554e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753b38e923b3c20baf477587a5b38887ecfef4daa75a78badecf051d96c8c4a4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944a6e12125ce8626b0c3ad98aba051689e1c03e22b22e48719e6dfc31f414c6(
    *,
    notification_arns: typing.Sequence[builtins.str],
    portfolio_id: builtins.str,
    product_id: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05474fb990f6c00862dbea2a1bc3f7641413d61ce3b1b0bafcd78717df1a0866(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    portfolio_id: builtins.str,
    product_id: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    local_role_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cf4878028c39be0daca339199b9eda3392900fca6861245efdcf4c8d721e85(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67fe07ce0cae03c8be07819826ee43978161b0fad0405580385e3eb1aff449a1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fde64297da69793d9f3012c057879745f5fdf36645939644f496b23aa12d9e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf1a778ddc0356546011a8781117a0c2fad00467445f8d262ba7a0f16853d97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b831588e1ef45448e176e4f54386fd80016739da617bc77ce177b18a2c3dd75(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724fab7f84c64c90ed0ced8bff0755619f3c7ba2d812d403377cb3348d17e0d7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be6ebc03ea1089221c54d9e3cd24e8271b4d641e75e07ae7dd902f4d3ba0209(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fefa847437c7d256b8544ccb7bff368bc24fcfae7553d4353fa9417bb0bd6f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c8372b1b8f9f069fa8ddf6cc2e753a8d4de263c1e160495123c44d364a3cd1(
    *,
    portfolio_id: builtins.str,
    product_id: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    local_role_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c000292e2b24b6a46f364a1914cc442c300264ea81691c2b2019e4dc000a11aa(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    portfolio_id: builtins.str,
    product_id: builtins.str,
    rules: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6b6d9a86db133245acfab3bd54867c70ae6896664bda05c66b97b54779b149(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa443fd16f071f5c43562d815f0808a0078ae98db79ce13aa81074c95b91df51(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547fd0d7074d8a3a4cf84b071d2532b6abd79faba6bacfb5d78c3aaafb452bb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fdeeced9857ebc0143d5ebb501ceddd6891df4f21de4b8ffea9e94c3c34d3be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c0067043fe338491f6c0a55df24a5671321eb9e0eace62dc8c94f4425320e49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5912cbcc72d1e588166d7d20b6b646174a26b888dde629a62d6634d368cc28(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35fc69cd0430b3984b7a86136781941489a5745760cf50ab9276207893f3c50(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ab40a16c7614d726a380d127488d83123103eb5866c9f819c0891692a4a427(
    *,
    portfolio_id: builtins.str,
    product_id: builtins.str,
    rules: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d37a11b9127d74d008e969f20eea44cec91241a8c8e801e91effd5264b9dc1c(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    display_name: builtins.str,
    provider_name: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d42533342281f403893516e3e4684d779fdb1c62dc9018b859a2526f35a61c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c365ad6284f59bb8cf4af323651fe7aa19340d3fb94fedc488895fff21255f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a2e2a6cb2a627428107a332cce31845354dff45dfa49504fe030553fc714f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefb58d20a1045a2fdafdee143c51a6d60b1d9860c25d9dfc2c229a2716e5e76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e34fab4ec83942117254e7b2dbb6c6a3a18e90c4eb8cf5e37b33d6d5e1e8ab5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2256828f6c1b69e94fa0c961db073c0ecae0b7140f4ff6c2011f77b1da676d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1badb8b93aebd4e7bd7c4ec52efd4a76e94eb4bbf9f1a1e06464cd0164385a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    portfolio_id: builtins.str,
    principal_arn: builtins.str,
    principal_type: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9a65d802deb12803710648a5c02c798b42b9fc9a05cc48c3929e286eca45d9(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715dd6496700390bd3a26156b82fd2ec669ef7fe550a5cf87d0737e9c30fceb7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb14c43a4f6e5a507eaf39642305c31306b1008cea413e92a47a937b4c4594a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74be550dd3f924e09496a876da171df1056d214f55356d34df43bf40a2a4e095(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec49b4e446dcf7bd2ed7caeb4b80984501357025ca4d4e43fba8ebce3055c4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02df720192a545192ae25318764c92213dd491a228e08ac7fd0a68a0819354c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b746d64f4b431c05582088f413f1fe0214bc5d94d42cd25b180beb911c8b01dd(
    *,
    portfolio_id: builtins.str,
    principal_arn: builtins.str,
    principal_type: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa08d7fc1d2dcbb13e794462f72361998bde7254193599c9cfcf138ab56197dc(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    portfolio_id: builtins.str,
    product_id: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    source_portfolio_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4e566706318c289f939fa97d0a5642393bb12a0349e51b3d45592022cbaa09(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29420bfb225760a406de0eb2840a36ac5df116fa371f460637bf0193f25bc7b4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d058c54f8f9f665f65d2bd5b011578cc3548bf36f9d6c08aec04f33b052f629(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16e6d44f7b7d755f53fb09d665ed549dd3b92036bb438e636dab31136bf18b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61db5eeb19c2ada6dd48081c34e81cf1127bc7079e4ade7b74999f18dbd8bead(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398214301ea0f6e5131e1d62c63a28d6a052a448cb1ada36486413678fe04139(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06fa922bb2fafdf69c6cc3c50ef7e2f1c6f72e5ec950bb7b0c5b79b93477235b(
    *,
    portfolio_id: builtins.str,
    product_id: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    source_portfolio_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f21ac5a461a8f8745b78871c28703eab5a1f377797b2b9e07901b97eecf944(
    *,
    display_name: builtins.str,
    provider_name: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0037fe68380000e31dd0e10d0d0a03c7157f49c7758bfd556a2d921739783ee5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    account_id: builtins.str,
    portfolio_id: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    share_tag_options: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217e2be7179854152fc979402390a792ec64635700831fbd73c47cbff68056ad(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f11922ffa82c9a056bbe13f3100ff9ad654982867f72d675ddd9b88862f1847(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8c7413cfb24a2e5ca0d96930f48974ef9aabfbd93907bce9b85f29db0ead4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0daa77a66cbe5ba7ddedc04ac46f2660cefaaf04366c9fe2e8d79a38527893(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20ea98fc22fee61257435182ab11e6e24ebbef57fc91b69dbad873d54a78b9b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c93238824888a8a207df23d909c6619e27c543b02375de19aae5521d2b5c55f(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a2e151cd846989e98a12c172a20f55522edb38e50dbeb4fd9ef8ffa5c8bcd7(
    *,
    account_id: builtins.str,
    portfolio_id: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    share_tag_options: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e6158705a78f206429684c920f37b0dbf6052c1f9718d0eb64b9805f36590a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    portfolio_id: builtins.str,
    product_id: builtins.str,
    tag_update_on_provisioned_product: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0f56c32700892ddafb4ee8a148540f156341594d7aab50e99646e179dd34fa(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa5fc9999ca2e23b38cfbd12cb69d8871659fef8119452ddf32c11433cca7df(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db1d6ee955c9f11c9320451431e45e2514a3a55c901dfe4769139a99b7e28ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e20a17ece5fe0bf2be1d46c102f023c8a459cd13aad9c24e5148cc601346948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ac28643a3e86add7678f137c5035ffc535b6d59f0cdcb976824ba76fa51646(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16150eb7325e26ebbe9edc0272ef11ae36d30132fcb8b7c408573cd13abc744(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1542e426cf2609bfbbda2c53a397fd7b952616b2d10feea1f77a238967f6ded4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af61d79ae3ba512a69bd69176ec8fc3b61af69ee93fe2b05bfca75bdb1b73ee2(
    *,
    portfolio_id: builtins.str,
    product_id: builtins.str,
    tag_update_on_provisioned_product: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf8be5b8ba333f2436f119d0f45c48ba97103f215d2ea4a68dbc32bd9e11cbb(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    definition: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnServiceAction.DefinitionParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    definition_type: builtins.str,
    name: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80abf54b60353986671baa97c7fd85893e88c0f2f1f9dee5d48d50c9f5c8f95e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2a8976aef07498ac0135f199a9c4bd3870aedc8bc7b6a3ca13c4634366157c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b3fcea1911c803c6266707e4e2b01fd6ef977ec5153518ed46e2d93c0e8ced(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnServiceAction.DefinitionParameterProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5f81e9c5829266b0517e5715fa9c224a84df07e53e95df2b5fcb6ee85a3573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a57005347b85d83abd6ee49918068bbbc0099724de48bb013c724a51f2bf79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d25096bae88fa61ff09ade07169f322e20d6e560fb41a599d72c1bd136ed8e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f35cf81f8b0205bfa795f16bd4c5d272496f43b05bc0b6e78d0c003ada1b829(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92929363008293a458cfbdca39df3247b6894a8c7f81f4295fe98333efa8fe97(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2760f77e70f16e0a62b11aca2382a45f0e2ea6bb9204d1e0a791890cc976fb(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    product_id: builtins.str,
    provisioning_artifact_id: builtins.str,
    service_action_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfc3ddab4eda9045a7c80cf641629541ec3c74d3fa1f989dbaf60f231d47aee(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4e15ad3233bf31d9dad33f8a1e746d572cb67a7f5f00edb8df546d8cae8acd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2edaa252dc1e1983d48219b0493d2255176c17b02eee8738f26e0284518e09b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfcead32cf03c02dfe6bdadc9e4cf5e771aa6873592569583050faa84fe240fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6780b9ef94f370a00cf41190bedc1cd2c1f8a40359531d6e3f938373d24df7b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac0b8f611f8b9d4177f96dfffd7b911307e7001fff77e808b56c9864209b4f4(
    *,
    product_id: builtins.str,
    provisioning_artifact_id: builtins.str,
    service_action_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e66e58ae63bf70496e65aa8d5c06769c460f04a4568ac60085dd7965d029854(
    *,
    definition: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnServiceAction.DefinitionParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    definition_type: builtins.str,
    name: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdf8c8d0fce64cad689104d45f34c83e06b8f7c4f098b6f5634c85151e46262(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    account_list: typing.Sequence[builtins.str],
    admin_role: builtins.str,
    description: builtins.str,
    execution_role: builtins.str,
    portfolio_id: builtins.str,
    product_id: builtins.str,
    region_list: typing.Sequence[builtins.str],
    stack_instance_control: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ebf471413b4dda09e27e8789910307f6b3f3e02711e2f06acc50ac325b93c8(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5b6faad3c18cf05fe43a223fe30b010a7142330f7a3b22cce61698dd5d1ca5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde8f51f324956b66ffc8f1d082306fa75417eaca857f1c958ff87fd3648052d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3998db215eb7bf13492e6a7ef460b2f6ad6685b1f56ae31fad5c673acaee37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b242f34e080958c6ce538a7db003756d3ee4016b7e712bc2b0d0e85014ca0c03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16bd4423c71bef04f5b7f0646fcb205d43b3140d474581a0dcf5438e061830c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab832a39b7da19ff791f11d7963db7c12a78a1a2c2bd74747c6f8ec634012ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547b1e4945be35c7161a3528def29c53de8a6c7c51f8ad0aafa96c35186b4de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9f66bdb6a7444ac1d6fe3e72d4dd7900b30252fa16642733af135ad5d214dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4f8ebc972013becd0cf5d5fecfec4bb7c92ce2fcd246daa44abc2fe2b140aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88e3bc2ff5d3ebab865fca73b4f81fe1b2bba690fe88ef9ae93dd00120b1a28(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6705a483626b5c7fd621c817cee336faf357b47264cc41cc519eb87ce948ad98(
    *,
    account_list: typing.Sequence[builtins.str],
    admin_role: builtins.str,
    description: builtins.str,
    execution_role: builtins.str,
    portfolio_id: builtins.str,
    product_id: builtins.str,
    region_list: typing.Sequence[builtins.str],
    stack_instance_control: builtins.str,
    accept_language: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34347da5e8fb762c964a65f85fc79ebec7c594c1bd559349e70f2272ea2ec583(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    key: builtins.str,
    value: builtins.str,
    active: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fb2e19d3b508b1ca1c2cae8864a42e810a534fdc6f474114a0f67587fff983(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826caecc284ecc3944249f4d71f324eaf08c5adaa8912e18bcb43ecba824135b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff3f1576e3a9db63c91cf0e1aba117e952b52d9a32410e4df4f23ea1d6c1c05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3feb59c6da58663d22531426b965db3bfee687a22aadd1f42a4e78562da40bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1eddfb5a3d5cb539f5cd71506f914481eafea8eb7b12de0d1c020cdf321f94(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7dd8b3f1b0d8dbd58f22bd6f147896961866bdf19f858efff69fe2a09e4557(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    resource_id: builtins.str,
    tag_option_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c9da6f5ba3fe54b13666fac168d90a342b9fba614e0385e25ef9312b239c12(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdce26e573e18c16d7e182e789259d62e6af1b274de8b11987b3f47ddf8d5577(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea948c812f5c73898f84aa5e9b1a01c606ac1826b13f398568c4c85b441f072(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fbf902d8389e12e5b76c8d19f4c1d70428822a021b4193cf96510aeb6f52b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c091bb87ff87594a9a60fe7ba5975c367e4a3d034456b260b01f2bce7242bc3e(
    *,
    resource_id: builtins.str,
    tag_option_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376093287aea62e59fefc23e1f17314a241a57118ca5e0b9f10b98818700fb4f(
    *,
    key: builtins.str,
    value: builtins.str,
    active: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3a7b5581814f3bdd8c23929d7ac55ae35fc55897db386cf1ad87cfb37233e0(
    *,
    owner: builtins.str,
    product_name: builtins.str,
    product_versions: typing.Sequence[typing.Union[CloudFormationProductVersion, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    distributor: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
    replace_product_version_ids: typing.Optional[builtins.bool] = None,
    support_description: typing.Optional[builtins.str] = None,
    support_email: typing.Optional[builtins.str] = None,
    support_url: typing.Optional[builtins.str] = None,
    tag_options: typing.Optional[TagOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa78ba884403832f78e38403ae3b3b6ddfc5c072cf5a0637f8332c3e2cacf26(
    *,
    cloud_formation_template: CloudFormationTemplate,
    description: typing.Optional[builtins.str] = None,
    product_version_name: typing.Optional[builtins.str] = None,
    validate_template: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f539e17f72a82fdf3d03b6fc29db72e44f780ff08b0e5fe7c2e8cdcd3266798f(
    path: builtins.str,
    *,
    readers: typing.Optional[typing.Sequence[_IGrantable_4c5a91d1]] = None,
    source_hash: typing.Optional[builtins.str] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow: typing.Optional[_FollowMode_98b05cc5] = None,
    ignore_mode: typing.Optional[_IgnoreMode_31d8bf46] = None,
    follow_symlinks: typing.Optional[_SymlinkFollowMode_abf4527a] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_AssetHashType_49193809] = None,
    bundling: typing.Optional[typing.Union[_BundlingOptions_ab115a99, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49eb94cce84255dfc5315c17696cadbe42f69096c1d51e13cf00f4202e9629a(
    product_stack: ProductStack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68da87dc01cbce0176b4e23e75fe5cdbbfe4673711535f10edbb14c8e51e068e(
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cc553f69512f45e46be4de2aa4442a6306d7b5be707b36418d612dbe6f53b7(
    scope: _Construct_e78e779f,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad64e8ca1965ae00682380e0dbba2880163056e106052507446757ba3d5a3d7b(
    *,
    http_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cfbb1df9c85153dbfd1bc947c516215d0e1a55867b07b31d35f4a8da89c191a(
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a5bbe75222fe426891b9f894414bc0309914052b1b647b9a43c16d5ecac203(
    product: IProduct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0649d5f680adf7747fbf3087ce1af0e23cff64246efdca5bd8764dfb1dc9ca19(
    tag_options: TagOptions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db604a98d4d01f13120134594168901610b62e6c383e61fa8f6017d81f8ceadf(
    product: IProduct,
    *,
    rule: typing.Union[TemplateRule, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14afa5a4e81bc92f5941d75963f729709d6a2a6ec5160029f443e4044aa2034(
    product: IProduct,
    *,
    allow: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66f58911bb56bdc65912805c6e8852f3b6e672eb0a61a2b08d2330e76407dce(
    product: IProduct,
    *,
    accounts: typing.Sequence[builtins.str],
    admin_role: _IRole_59af6f50,
    execution_role_name: builtins.str,
    regions: typing.Sequence[builtins.str],
    allow_stack_set_instance_operations: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f44be325389fc8b7e1607a28f84613ca7416cb5082a9ff4af0e3b4463699bd(
    group: _IGroup_8a32caf8,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f2970b3850cf0cfbaffec75bcd58a9fde27ae85b56c2d4feb9a7e772100c61(
    role: _IRole_59af6f50,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2a29b72dceb0d42cae20bd71904dc20e639543e8ba19e4010a72cabdc754e8(
    user: _IUser_9d11d57d,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57c6fc6988172115b736725b1f78a7f3ba0b52ae72500d8d67baaefe8b6ec62(
    product: IProduct,
    topic: _ITopic_465e36b9,
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed16cf3e9cce8c001252c373a9c23391303ba256a5f50a2903891806a2a39a75(
    product: IProduct,
    launch_role: _IRole_59af6f50,
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755aa308d6b8389b689e2707bbab28a2e1d83e2389b4af22aaa6ffae785c78d8(
    product: IProduct,
    launch_role: _IRole_59af6f50,
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db0efb957d700097cd758541fa75f5eebca92127c1815137852a11e6f8db956(
    product: IProduct,
    launch_role_name: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ae069777f6b4e74743ef0b2cdc100c541b83b82b6bb3d15977c4d81d6d3624(
    account_id: builtins.str,
    *,
    message_language: typing.Optional[MessageLanguage] = None,
    share_tag_options: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9b6e3a91c83b6c37a67749ba97a222f5708966a96832673772c2d72b91d049(
    tag_options: TagOptions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f80ec5f5bee355821a01e3fc22f91f55a7e68e00d2e684321f981760d57ad73(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    display_name: builtins.str,
    provider_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
    tag_options: typing.Optional[TagOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9c2e611d344a07c80f17c63274cf0d0940305eabdbd3c8e6e91dfedd032a47(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    portfolio_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4002350e77eff6e60769777d2b2649b5d61203437119ac9d20c9d3a250e84358(
    product: IProduct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788adf2a1761a91664610e791a6ae14c8827a0745c9062b359e72b99d3b48ff9(
    tag_options: TagOptions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75eb81f90d7a08826e381548469c7f35fda88750fb983a1b1769d1db7710fa5(
    product: IProduct,
    *,
    rule: typing.Union[TemplateRule, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378804b86f7ea4c3b1e87c6890200d19c33d2f80034ccb3e90496150884f3e1d(
    product: IProduct,
    *,
    allow: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9974b51adafdd70190a96c8809cc9980c1c27643dfaf2000ef62723311607eb5(
    product: IProduct,
    *,
    accounts: typing.Sequence[builtins.str],
    admin_role: _IRole_59af6f50,
    execution_role_name: builtins.str,
    regions: typing.Sequence[builtins.str],
    allow_stack_set_instance_operations: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc1c77700b287580ca8e7e6e4ccf315aa80b8e2dc5c12af09006a4fa6319de7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e10d32a074e71199c93a8657add795167385f197c981f67508bd4ae9e63d209(
    group: _IGroup_8a32caf8,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb787ddf8061fe500811a434aceba580bc1599195a70f58f3c632bd6e3bedf1c(
    role: _IRole_59af6f50,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afae341b5d27b8f67156e7372246a7bb9a28445a005122b210b64c7d476a113(
    user: _IUser_9d11d57d,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a98d2096d213234b2f1bce083ca4524b700690c60b9c16034c1d0ebac1ed5c(
    product: IProduct,
    topic: _ITopic_465e36b9,
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1dc86d8b868bbcc44b77dbfb2adc61c7fc1b92482c17b6bf813763a81ce929(
    product: IProduct,
    launch_role: _IRole_59af6f50,
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28e8e7d3f93c913fb8bf530058251f9b95ecde75ee1ea614705fbd982bf4c28(
    product: IProduct,
    launch_role: _IRole_59af6f50,
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a35466b19934456d99e3583327707187af7ad7807017ecfe8ffa9adac713ec3(
    product: IProduct,
    launch_role_name: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17783777a200571366dee401b5a56eaa973f17f9b13d33c7e856129de68304bd(
    account_id: builtins.str,
    *,
    message_language: typing.Optional[MessageLanguage] = None,
    share_tag_options: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab658f8e281e8ab8e5e39bfc08f9f06d912f00a6713a3575a77bc225a08b1dda(
    *,
    display_name: builtins.str,
    provider_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
    tag_options: typing.Optional[TagOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f99f25c56b82c0a8bb46800c7beb2bbaf3b7de07dd26b49e2f8d7dec0cb82f(
    *,
    message_language: typing.Optional[MessageLanguage] = None,
    share_tag_options: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa330b300f438c46390a33585104e3eb6468252365b1babad66505622f8ea9cb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7166e186ba980c79cc7b60768e42147e814bc9c5ad5e35d60ef4515f25e68f3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    product_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61863236bab2ac90a54c9c2f900bef6b895ec83a99a17ad5412a8490b405fb4b(
    tag_options: TagOptions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb990be77c79429898bf492f8045ab6e82e07bda61299c0db3bf88f361c243a5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f987935770e71a41b2388a3d716ea51987c9f5dd16a1c6669f521222a1ed315d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    current_version_locked: builtins.bool,
    current_version_name: builtins.str,
    product_stack: ProductStack,
    description: typing.Optional[builtins.str] = None,
    directory: typing.Optional[builtins.str] = None,
    validate_template: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f05e4148190a5ffca2b254291025a7033e0c878cac04b28caf403b22cd1d9c(
    product_version_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13790d59f1daf3d5ef2810019cad1b4f1e0d7620175cd02c0b2e2a053470b00d(
    *,
    current_version_locked: builtins.bool,
    current_version_name: builtins.str,
    product_stack: ProductStack,
    description: typing.Optional[builtins.str] = None,
    directory: typing.Optional[builtins.str] = None,
    validate_template: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afdd778c43fc28aa0c6aaecaa71e4259080199ec8d1b4241fc7e5e4a97c01b0(
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
    accounts: typing.Sequence[builtins.str],
    admin_role: _IRole_59af6f50,
    execution_role_name: builtins.str,
    regions: typing.Sequence[builtins.str],
    allow_stack_set_instance_operations: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7567d6a3a803f28a0d0e7eb84ce369487acfb437b6d71889291c92f56e00e4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allowed_values_for_tags: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f11317240f375930315d794ff7864118108486cbfe378a0eaae373e7fd99dc6(
    *,
    allowed_values_for_tags: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8449641a3ab9e932e14f03a58ac3c7bd157bdb6fa5ea8f2467dac63f49acd2(
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
    allow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e464274c3532cf833ab69aec7ffa6b1dbb213466f91170c4b10a2ce79ffb79c(
    *,
    assertions: typing.Sequence[typing.Union[TemplateRuleAssertion, typing.Dict[builtins.str, typing.Any]]],
    rule_name: builtins.str,
    condition: typing.Optional[_ICfnRuleConditionExpression_5f18240f] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101fcfa003a72e800257dbcb55ab9b9b4bd530ef944612818a8de8037d58d292(
    *,
    assert_: _ICfnRuleConditionExpression_5f18240f,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e38f8dd9679cf2b1355e43e418efc2c485c8339e0cca90b5c72f0a6361759bc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    owner: builtins.str,
    product_name: builtins.str,
    product_versions: typing.Sequence[typing.Union[CloudFormationProductVersion, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    distributor: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
    replace_product_version_ids: typing.Optional[builtins.bool] = None,
    support_description: typing.Optional[builtins.str] = None,
    support_email: typing.Optional[builtins.str] = None,
    support_url: typing.Optional[builtins.str] = None,
    tag_options: typing.Optional[TagOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343d88b9ba0b997d099e92e0129d5f0df694b0e992ab3e5ac51fa18c5a022ae3(
    *,
    description: typing.Optional[builtins.str] = None,
    message_language: typing.Optional[MessageLanguage] = None,
    rule: typing.Union[TemplateRule, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass
