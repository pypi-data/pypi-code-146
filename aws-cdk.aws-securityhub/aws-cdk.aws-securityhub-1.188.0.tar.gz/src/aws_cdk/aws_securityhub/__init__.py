'''
# AWS Security Hub Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_securityhub as securityhub
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for SecurityHub construct libraries](https://constructs.dev/search?q=securityhub)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::SecurityHub resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SecurityHub.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::SecurityHub](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SecurityHub.html).

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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnHub(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-securityhub.CfnHub",
):
    '''A CloudFormation ``AWS::SecurityHub::Hub``.

    The ``AWS::SecurityHub::Hub`` resource represents the implementation of the AWS Security Hub service in your account. One hub resource is created for each Region in which you enable Security Hub .

    The CIS AWS Foundations Benchmark standard and the Foundational Security Best Practices standard are also enabled in each Region where you enable Security Hub .

    :cloudformationResource: AWS::SecurityHub::Hub
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_securityhub as securityhub
        
        # tags: Any
        
        cfn_hub = securityhub.CfnHub(self, "MyCfnHub",
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::SecurityHub::Hub``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param tags: The tags to add to the hub resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3563ef17bf8074b42c52e43b2585ba5c613b9ece089f510bbb78c9fe62296041)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHubProps(tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ce0bd179e10dc2b1c444decf6304c1ee01a8028b6974e0ea95df11e3465941)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb929b1ca9535fbe9ab05042fdbad8e3193a991581aae8997fd92dda664a94e8)
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags to add to the hub resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html#cfn-securityhub-hub-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-securityhub.CfnHubProps",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags"},
)
class CfnHubProps:
    def __init__(self, *, tags: typing.Any = None) -> None:
        '''Properties for defining a ``CfnHub``.

        :param tags: The tags to add to the hub resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_securityhub as securityhub
            
            # tags: Any
            
            cfn_hub_props = securityhub.CfnHubProps(
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11bd20a2f282fdf105f84e18e75e21561b1948691fb7c9b7d73b92ce9447df76)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def tags(self) -> typing.Any:
        '''The tags to add to the hub resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-securityhub-hub.html#cfn-securityhub-hub-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHubProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnHub",
    "CfnHubProps",
]

publication.publish()

def _typecheckingstub__3563ef17bf8074b42c52e43b2585ba5c613b9ece089f510bbb78c9fe62296041(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ce0bd179e10dc2b1c444decf6304c1ee01a8028b6974e0ea95df11e3465941(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb929b1ca9535fbe9ab05042fdbad8e3193a991581aae8997fd92dda664a94e8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11bd20a2f282fdf105f84e18e75e21561b1948691fb7c9b7d73b92ce9447df76(
    *,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
