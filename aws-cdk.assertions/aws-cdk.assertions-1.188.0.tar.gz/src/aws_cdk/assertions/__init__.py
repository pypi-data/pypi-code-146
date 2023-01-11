'''
# Assertions

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

If you're migrating from the old `assert` library, the migration guide can be found in
[our GitHub repository](https://github.com/aws/aws-cdk/blob/master/packages/@aws-cdk/assertions/MIGRATING.md).

Functions for writing test asserting against CDK applications, with focus on CloudFormation templates.

The `Template` class includes a set of methods for writing assertions against CloudFormation templates. Use one of the `Template.fromXxx()` static methods to create an instance of this class.

To create `Template` from CDK stack, start off with:

```python
from aws_cdk.core import Stack
from aws_cdk.assertions import Template

stack = Stack()
# ...
template = Template.from_stack(stack)
```

Alternatively, assertions can be run on an existing CloudFormation template -

```python
template_json = "{ \"Resources\": ... }" # The CloudFormation template as JSON serialized string.
template = Template.from_string(template_json)
```

## Full Template Match

The simplest assertion would be to assert that the template matches a given
template.

```python
template.template_matches({
    "Resources": {
        "BarLogicalId": {
            "Type": "Foo::Bar",
            "Properties": {
                "Baz": "Qux"
            }
        }
    }
})
```

By default, the `templateMatches()` API will use the an 'object-like' comparison,
which means that it will allow for the actual template to be a superset of the
given expectation. See [Special Matchers](#special-matchers) for details on how
to change this.

Snapshot testing is a common technique to store a snapshot of the output and
compare it during future changes. Since CloudFormation templates are human readable,
they are a good target for snapshot testing.

The `toJSON()` method on the `Template` can be used to produce a well formatted JSON
of the CloudFormation template that can be used as a snapshot.

See [Snapshot Testing in Jest](https://jestjs.io/docs/snapshot-testing) and [Snapshot
Testing in Java](https://json-snapshot.github.io/).

## Counting Resources

This module allows asserting the number of resources of a specific type found
in a template.

```python
template.resource_count_is("Foo::Bar", 2)
```

## Resource Matching & Retrieval

Beyond resource counting, the module also allows asserting that a resource with
specific properties are present.

The following code asserts that the `Properties` section of a resource of type
`Foo::Bar` contains the specified properties -

```python
template.has_resource_properties("Foo::Bar", {
    "Foo": "Bar",
    "Baz": 5,
    "Qux": ["Waldo", "Fred"]
})
```

Alternatively, if you would like to assert the entire resource definition, you
can use the `hasResource()` API.

```python
template.has_resource("Foo::Bar", {
    "Properties": {"Foo": "Bar"},
    "DependsOn": ["Waldo", "Fred"]
})
```

Beyond assertions, the module provides APIs to retrieve matching resources.
The `findResources()` API is complementary to the `hasResource()` API, except,
instead of asserting its presence, it returns the set of matching resources.

By default, the `hasResource()` and `hasResourceProperties()` APIs perform deep
partial object matching. This behavior can be configured using matchers.
See subsequent section on [special matchers](#special-matchers).

## Output and Mapping sections

The module allows you to assert that the CloudFormation template contains an Output
that matches specific properties. The following code asserts that a template contains
an Output with a `logicalId` of `Foo` and the specified properties -

```python
expected = {
    "Value": "Bar",
    "Export": {"Name": "ExportBaz"}
}
template.has_output("Foo", expected)
```

If you want to match against all Outputs in the template, use `*` as the `logicalId`.

```python
template.has_output("*", {
    "Value": "Bar",
    "Export": {"Name": "ExportBaz"}
})
```

`findOutputs()` will return a set of outputs that match the `logicalId` and `props`,
and you can use the `'*'` special case as well.

```python
result = template.find_outputs("*", {"Value": "Fred"})
expect(result.Foo).to_equal({"Value": "Fred", "Description": "FooFred"})
expect(result.Bar).to_equal({"Value": "Fred", "Description": "BarFred"})
```

The APIs `hasMapping()`, `findMappings()`, `hasCondition()`, and `hasCondtions()` provide similar functionalities.

## Special Matchers

The expectation provided to the `hasXxx()`, `findXxx()` and `templateMatches()`
APIs, besides carrying literal values, as seen in the above examples, also accept
special matchers.

They are available as part of the `Match` class.

### Object Matchers

The `Match.objectLike()` API can be used to assert that the target is a superset
object of the provided pattern.
This API will perform a deep partial match on the target.
Deep partial matching is where objects are matched partially recursively. At each
level, the list of keys in the target is a subset of the provided pattern.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": "Flob",
#           "Bob": "Cat"
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Wobble": "Flob"
    })
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Brew": "Coffee"
    })
})
```

The `Match.objectEquals()` API can be used to assert a target as a deep exact
match.

### Presence and Absence

The `Match.absent()` matcher can be used to specify that a specific
value should not exist on the target. This can be used within `Match.objectLike()`
or outside of any matchers.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": "Flob",
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Bob": Match.absent()
    })
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.object_like({
        "Wobble": Match.absent()
    })
})
```

The `Match.anyValue()` matcher can be used to specify that a specific value should be found
at the location. This matcher will fail if when the target location has null-ish values
(i.e., `null` or `undefined`).

This matcher can be combined with any of the other matchers.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": ["Flob", "Flib"],
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": {
        "Wobble": [Match.any_value(), Match.any_value()]
    }
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": {
        "Wimble": Match.any_value()
    }
})
```

### Array Matchers

The `Match.arrayWith()` API can be used to assert that the target is equal to or a subset
of the provided pattern array.
This API will perform subset match on the target.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"]
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.array_with(["Flob"])
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", Match.object_like({
    "Fred": Match.array_with(["Wobble"])
}))
```

*Note:* The list of items in the pattern array should be in order as they appear in the
target array. Out of order will be recorded as a match failure.

Alternatively, the `Match.arrayEquals()` API can be used to assert that the target is
exactly equal to the pattern array.

### String Matchers

The `Match.stringLikeRegexp()` API can be used to assert that the target matches the
provided regular expression.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Template": "const includeHeaders = true;"
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Template": Match.string_like_regexp("includeHeaders = (true|false)")
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Template": Match.string_like_regexp("includeHeaders = null")
})
```

### Not Matcher

The not matcher inverts the search pattern and matches all patterns in the path that does
not match the pattern specified.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"]
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Fred": Match.not(["Flob"])
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", Match.object_like({
    "Fred": Match.not(["Flob", "Cat"])
}))
```

### Serialized JSON

Often, we find that some CloudFormation Resource types declare properties as a string,
but actually expect JSON serialized as a string.
For example, the [`BuildSpec` property of `AWS::CodeBuild::Project`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codebuild-project-source.html#cfn-codebuild-project-source-buildspec),
the [`Definition` property of `AWS::StepFunctions::StateMachine`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definition),
to name a couple.

The `Match.serializedJson()` matcher allows deep matching within a stringified JSON.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Baz": "{ \"Fred\": [\"Waldo\", \"Willow\"] }"
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Baz": Match.serialized_json({
        "Fred": Match.array_with(["Waldo"])
    })
})

# The following will throw an assertion error
template.has_resource_properties("Foo::Bar", {
    "Baz": Match.serialized_json({
        "Fred": ["Waldo", "Johnny"]
    })
})
```

## Capturing Values

The matcher APIs documented above allow capturing values in the matching entry
(Resource, Output, Mapping, etc.). The following code captures a string from a
matching resource.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"],
#         "Waldo": ["Qix", "Qux"],
#       }
#     }
#   }
# }

fred_capture = Capture()
waldo_capture = Capture()
template.has_resource_properties("Foo::Bar", {
    "Fred": fred_capture,
    "Waldo": ["Qix", waldo_capture]
})

fred_capture.as_array() # returns ["Flob", "Cat"]
waldo_capture.as_string()
```

With captures, a nested pattern can also be specified, so that only targets
that match the nested pattern will be captured. This pattern can be literals or
further Matchers.

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar1": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"],
#       }
#     }
#     "MyBar2": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Qix", "Qux"],
#       }
#     }
#   }
# }

capture = Capture(Match.array_with(["Cat"]))
template.has_resource_properties("Foo::Bar", {
    "Fred": capture
})

capture.as_array()
```

When multiple resources match the given condition, each `Capture` defined in
the condition will capture all matching values. They can be paged through using
the `next()` API. The following example illustrates this -

```python
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": "Flob",
#       }
#     },
#     "MyBaz": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": "Quib",
#       }
#     }
#   }
# }

fred_capture = Capture()
template.has_resource_properties("Foo::Bar", {
    "Fred": fred_capture
})

fred_capture.as_string() # returns "Flob"
fred_capture.next() # returns true
fred_capture.as_string()
```

## Asserting Annotations

In addition to template matching, we provide an API for annotation matching.
[Annotations](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Annotations.html)
can be added via the [Aspects](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Aspects.html)
API. You can learn more about Aspects [here](https://docs.aws.amazon.com/cdk/v2/guide/aspects.html).

Say you have a `MyAspect` and a `MyStack` that uses `MyAspect`:

```python
import aws_cdk.core as cdk
from constructs import Construct, IConstruct

class MyAspect(cdk.IAspect):
    def visit(self, node):
        if node instanceof cdk.CfnResource && node.cfn_resource_type == "Foo::Bar":
            self.error(node, "we do not want a Foo::Bar resource")

    def error(self, node, message):
        cdk.Annotations.of(node).add_error(message)

class MyStack(cdk.Stack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        stack = cdk.Stack()
        cdk.CfnResource(stack, "Foo",
            type="Foo::Bar",
            properties={
                "Fred": "Thud"
            }
        )
        cdk.Aspects.of(stack).add(MyAspect())
```

We can then assert that the stack contains the expected Error:

```python
# import { Annotations } from '@aws-cdk/assertions';

Annotations.from_stack(stack).has_error("/Default/Foo", "we do not want a Foo::Bar resource")
```

Here are the available APIs for `Annotations`:

* `hasError()`, `hasNoError()`, and `findError()`
* `hasWarning()`, `hasNoWarning()`, and `findWarning()`
* `hasInfo()`, `hasNoInfo()`, and `findInfo()`

The corresponding `findXxx()` API is complementary to the `hasXxx()` API, except instead
of asserting its presence, it returns the set of matching messages.

In addition, this suite of APIs is compatable with `Matchers` for more fine-grained control.
For example, the following assertion works as well:

```python
Annotations.from_stack(stack).has_error("/Default/Foo",
    Match.string_like_regexp(".*Foo::Bar.*"))
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

import aws_cdk.core as _aws_cdk_core_f4b25747
import aws_cdk.cx_api as _aws_cdk_cx_api_9a62db47


class Annotations(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assertions.Annotations"):
    '''Suite of assertions that can be run on a CDK Stack.

    Focused on asserting annotations.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.assertions as assertions
        import aws_cdk.core as cdk
        
        # stack: cdk.Stack
        
        annotations = assertions.Annotations.from_stack(stack)
    '''

    @jsii.member(jsii_name="fromStack")
    @builtins.classmethod
    def from_stack(cls, stack: _aws_cdk_core_f4b25747.Stack) -> "Annotations":
        '''Base your assertions on the messages returned by a synthesized CDK ``Stack``.

        :param stack: the CDK Stack to run assertions on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4776f3330e9f7c7c149d8e58636faf4bb7b7af2d47493c52f41a29501e257162)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast("Annotations", jsii.sinvoke(cls, "fromStack", [stack]))

    @jsii.member(jsii_name="findError")
    def find_error(
        self,
        construct_path: builtins.str,
        message: typing.Any,
    ) -> typing.List[_aws_cdk_cx_api_9a62db47.SynthesisMessage]:
        '''Get the set of matching errors of a given construct path and message.

        :param construct_path: the construct path to the error. Provide ``'*'`` to match all errors in the template.
        :param message: the error message as should be expected. This should be a string or Matcher object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__926cdc57b33370dbaae7f42c0146d498880442679248560af04f5d0138450a13)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(typing.List[_aws_cdk_cx_api_9a62db47.SynthesisMessage], jsii.invoke(self, "findError", [construct_path, message]))

    @jsii.member(jsii_name="findInfo")
    def find_info(
        self,
        construct_path: builtins.str,
        message: typing.Any,
    ) -> typing.List[_aws_cdk_cx_api_9a62db47.SynthesisMessage]:
        '''Get the set of matching infos of a given construct path and message.

        :param construct_path: the construct path to the info. Provide ``'*'`` to match all infos in the template.
        :param message: the info message as should be expected. This should be a string or Matcher object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e1d77cfc14858b867b433ed3b1e377fd3a817bea19f66c139f9ee420ee9f48)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(typing.List[_aws_cdk_cx_api_9a62db47.SynthesisMessage], jsii.invoke(self, "findInfo", [construct_path, message]))

    @jsii.member(jsii_name="findWarning")
    def find_warning(
        self,
        construct_path: builtins.str,
        message: typing.Any,
    ) -> typing.List[_aws_cdk_cx_api_9a62db47.SynthesisMessage]:
        '''Get the set of matching warning of a given construct path and message.

        :param construct_path: the construct path to the warning. Provide ``'*'`` to match all warnings in the template.
        :param message: the warning message as should be expected. This should be a string or Matcher object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fac69bd448b958d44579d4c494bd116210d0a48591a10c5c14fd082735db502)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(typing.List[_aws_cdk_cx_api_9a62db47.SynthesisMessage], jsii.invoke(self, "findWarning", [construct_path, message]))

    @jsii.member(jsii_name="hasError")
    def has_error(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''Assert that an error with the given message exists in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the error. Provide ``'*'`` to match all errors in the template.
        :param message: the error message as should be expected. This should be a string or Matcher object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a869ba274728ae9608a5b315ed01d41a7ea9eb5bfac2dfd3d5afc2c3a8f30b)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasError", [construct_path, message]))

    @jsii.member(jsii_name="hasInfo")
    def has_info(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''Assert that an info with the given message exists in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the info. Provide ``'*'`` to match all info in the template.
        :param message: the info message as should be expected. This should be a string or Matcher object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a8b81413e5985c79dfe32bdc54d4780a8d6240fc4887e05764b93551f5be98)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasInfo", [construct_path, message]))

    @jsii.member(jsii_name="hasNoError")
    def has_no_error(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''Assert that an error with the given message does not exist in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the error. Provide ``'*'`` to match all errors in the template.
        :param message: the error message as should be expected. This should be a string or Matcher object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449dd2e59a7da77170ba8cb2523f7e7a97bf0ed723456540c32e716200eaf2ef)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasNoError", [construct_path, message]))

    @jsii.member(jsii_name="hasNoInfo")
    def has_no_info(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''Assert that an info with the given message does not exist in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the info. Provide ``'*'`` to match all info in the template.
        :param message: the info message as should be expected. This should be a string or Matcher object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d576bffef3dc6d940c0f3e1a894e54722abf373ad83a17cbc8324eb339d11a9c)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasNoInfo", [construct_path, message]))

    @jsii.member(jsii_name="hasNoWarning")
    def has_no_warning(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''Assert that an warning with the given message does not exist in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the warning. Provide ``'*'`` to match all warnings in the template.
        :param message: the warning message as should be expected. This should be a string or Matcher object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7475b4f161319d93d660ae5a788269cd0f6a73b1ac7e6d1ad072a4068d6faac5)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasNoWarning", [construct_path, message]))

    @jsii.member(jsii_name="hasWarning")
    def has_warning(self, construct_path: builtins.str, message: typing.Any) -> None:
        '''Assert that an warning with the given message exists in the synthesized CDK ``Stack``.

        :param construct_path: the construct path to the warning. Provide ``'*'`` to match all warnings in the template.
        :param message: the warning message as should be expected. This should be a string or Matcher object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d514b512db676ee5a943271fb9b9a057893b1b3d93ddb13be9e0441fb3f2f3)
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast(None, jsii.invoke(self, "hasWarning", [construct_path, message]))


class Match(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/assertions.Match"):
    '''Partial and special matching during template assertions.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="absent")
    @builtins.classmethod
    def absent(cls) -> "Matcher":
        '''Use this matcher in the place of a field's value, if the field must not be present.'''
        return typing.cast("Matcher", jsii.sinvoke(cls, "absent", []))

    @jsii.member(jsii_name="anyValue")
    @builtins.classmethod
    def any_value(cls) -> "Matcher":
        '''Matches any non-null value at the target.'''
        return typing.cast("Matcher", jsii.sinvoke(cls, "anyValue", []))

    @jsii.member(jsii_name="arrayEquals")
    @builtins.classmethod
    def array_equals(cls, pattern: typing.Sequence[typing.Any]) -> "Matcher":
        '''Matches the specified pattern with the array found in the same relative path of the target.

        The set of elements (or matchers) must match exactly and in order.

        :param pattern: the pattern to match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ebfea2b7fe77abd2d67255287185c7ca09d748790bb537192cd7cdcdc768fcd)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "arrayEquals", [pattern]))

    @jsii.member(jsii_name="arrayWith")
    @builtins.classmethod
    def array_with(cls, pattern: typing.Sequence[typing.Any]) -> "Matcher":
        '''Matches the specified pattern with the array found in the same relative path of the target.

        The set of elements (or matchers) must be in the same order as would be found.

        :param pattern: the pattern to match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46c96a58e6ed805ee3728f4912911fe4de977713cb40c1517a47ebc01b2240d)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "arrayWith", [pattern]))

    @jsii.member(jsii_name="exact")
    @builtins.classmethod
    def exact(cls, pattern: typing.Any) -> "Matcher":
        '''Deep exact matching of the specified pattern to the target.

        :param pattern: the pattern to match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f7b8a3bcd5101cbcfed6bd62706be40c8c5a33f0a41d1047d11aa608b0d4b0)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "exact", [pattern]))

    @jsii.member(jsii_name="not")
    @builtins.classmethod
    def not_(cls, pattern: typing.Any) -> "Matcher":
        '''Matches any target which does NOT follow the specified pattern.

        :param pattern: the pattern to NOT match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca9e0aeebfbe461e09b97dbd3b420b4c64e8a3683b345580a0081a9c9a22f5e)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "not", [pattern]))

    @jsii.member(jsii_name="objectEquals")
    @builtins.classmethod
    def object_equals(
        cls,
        pattern: typing.Mapping[builtins.str, typing.Any],
    ) -> "Matcher":
        '''Matches the specified pattern to an object found in the same relative path of the target.

        The keys and their values (or matchers) must match exactly with the target.

        :param pattern: the pattern to match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6ad13d0cdc150262ff11a0028408e347591b4b6e5fcc57b564b665e7f53c32)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "objectEquals", [pattern]))

    @jsii.member(jsii_name="objectLike")
    @builtins.classmethod
    def object_like(
        cls,
        pattern: typing.Mapping[builtins.str, typing.Any],
    ) -> "Matcher":
        '''Matches the specified pattern to an object found in the same relative path of the target.

        The keys and their values (or matchers) must be present in the target but the target can be a superset.

        :param pattern: the pattern to match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d99129cd34c2ee16315b19771583a262754032dcfc992e1f2ca8a137e78eeee)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "objectLike", [pattern]))

    @jsii.member(jsii_name="serializedJson")
    @builtins.classmethod
    def serialized_json(cls, pattern: typing.Any) -> "Matcher":
        '''Matches any string-encoded JSON and applies the specified pattern after parsing it.

        :param pattern: the pattern to match after parsing the encoded JSON.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e49b581a299c812014dbbea0c6e55a4317ee355d1584ab11c7420735591134f)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "serializedJson", [pattern]))

    @jsii.member(jsii_name="stringLikeRegexp")
    @builtins.classmethod
    def string_like_regexp(cls, pattern: builtins.str) -> "Matcher":
        '''Matches targets according to a regular expression.

        :param pattern: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e20e44f3feeb105b943805f455a7729b93d9586037c13056e0f7487f5bf5ade0)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("Matcher", jsii.sinvoke(cls, "stringLikeRegexp", [pattern]))


class _MatchProxy(Match):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Match).__jsii_proxy_class__ = lambda : _MatchProxy


@jsii.data_type(
    jsii_type="@aws-cdk/assertions.MatchCapture",
    jsii_struct_bases=[],
    name_mapping={"capture": "capture", "value": "value"},
)
class MatchCapture:
    def __init__(self, *, capture: "Capture", value: typing.Any) -> None:
        '''Information about a value captured during match.

        :param capture: The instance of Capture class to which this capture is associated with.
        :param value: The value that was captured.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.assertions as assertions
            
            # capture: assertions.Capture
            # value: Any
            
            match_capture = assertions.MatchCapture(
                capture=capture,
                value=value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85aa91a87986009f605a2ae1a32b7350ef70dfbbe6e3bf99f6bc4f5673798736)
            check_type(argname="argument capture", value=capture, expected_type=type_hints["capture"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capture": capture,
            "value": value,
        }

    @builtins.property
    def capture(self) -> "Capture":
        '''The instance of Capture class to which this capture is associated with.'''
        result = self._values.get("capture")
        assert result is not None, "Required property 'capture' is missing"
        return typing.cast("Capture", result)

    @builtins.property
    def value(self) -> typing.Any:
        '''The value that was captured.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MatchCapture(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/assertions.MatchFailure",
    jsii_struct_bases=[],
    name_mapping={"matcher": "matcher", "message": "message", "path": "path"},
)
class MatchFailure:
    def __init__(
        self,
        *,
        matcher: "Matcher",
        message: builtins.str,
        path: typing.Sequence[builtins.str],
    ) -> None:
        '''Match failure details.

        :param matcher: The matcher that had the failure.
        :param message: Failure message.
        :param path: The relative path in the target where the failure occurred. If the failure occurred at root of the match tree, set the path to an empty list. If it occurs in the 5th index of an array nested within the 'foo' key of an object, set the path as ``['/foo', '[5]']``.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.assertions as assertions
            
            # matcher: assertions.Matcher
            
            match_failure = assertions.MatchFailure(
                matcher=matcher,
                message="message",
                path=["path"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35cef13b82962737b757f37428b05befa6096945b04b75e1af6a45fca17fdbe)
            check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "matcher": matcher,
            "message": message,
            "path": path,
        }

    @builtins.property
    def matcher(self) -> "Matcher":
        '''The matcher that had the failure.'''
        result = self._values.get("matcher")
        assert result is not None, "Required property 'matcher' is missing"
        return typing.cast("Matcher", result)

    @builtins.property
    def message(self) -> builtins.str:
        '''Failure message.'''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.List[builtins.str]:
        '''The relative path in the target where the failure occurred.

        If the failure occurred at root of the match tree, set the path to an empty list.
        If it occurs in the 5th index of an array nested within the 'foo' key of an object,
        set the path as ``['/foo', '[5]']``.
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MatchFailure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MatchResult(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assertions.MatchResult"):
    '''The result of ``Match.test()``.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.assertions as assertions
        
        # target: Any
        
        match_result = assertions.MatchResult(target)
    '''

    def __init__(self, target: typing.Any) -> None:
        '''
        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584cd61323669b435ec39752ea455b7b3b552ecc0fb627b85bd1135417e22ed8)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        jsii.create(self.__class__, self, [target])

    @jsii.member(jsii_name="compose")
    def compose(self, id: builtins.str, inner: "MatchResult") -> "MatchResult":
        '''Compose the results of a previous match as a subtree.

        :param id: the id of the parent tree.
        :param inner: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1654ecc612a339620fef05a2b1f41f153491cb2154773d8e9d66d6a57998a6a7)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inner", value=inner, expected_type=type_hints["inner"])
        return typing.cast("MatchResult", jsii.invoke(self, "compose", [id, inner]))

    @jsii.member(jsii_name="finished")
    def finished(self) -> "MatchResult":
        '''Prepare the result to be analyzed.

        This API *must* be called prior to analyzing these results.
        '''
        return typing.cast("MatchResult", jsii.invoke(self, "finished", []))

    @jsii.member(jsii_name="hasFailed")
    def has_failed(self) -> builtins.bool:
        '''Does the result contain any failures.

        If not, the result is a success
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "hasFailed", []))

    @jsii.member(jsii_name="push")
    def push(
        self,
        matcher: "Matcher",
        path: typing.Sequence[builtins.str],
        message: builtins.str,
    ) -> "MatchResult":
        '''(deprecated) DEPRECATED.

        :param matcher: -
        :param path: -
        :param message: -

        :deprecated: use recordFailure()

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9694d7304cba82ed278f97224420a71cefaef5968f9ca63c99385456328a15d4)
            check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        return typing.cast("MatchResult", jsii.invoke(self, "push", [matcher, path, message]))

    @jsii.member(jsii_name="recordCapture")
    def record_capture(self, *, capture: "Capture", value: typing.Any) -> None:
        '''Record a capture against in this match result.

        :param capture: The instance of Capture class to which this capture is associated with.
        :param value: The value that was captured.
        '''
        options = MatchCapture(capture=capture, value=value)

        return typing.cast(None, jsii.invoke(self, "recordCapture", [options]))

    @jsii.member(jsii_name="recordFailure")
    def record_failure(
        self,
        *,
        matcher: "Matcher",
        message: builtins.str,
        path: typing.Sequence[builtins.str],
    ) -> "MatchResult":
        '''Record a new failure into this result at a specific path.

        :param matcher: The matcher that had the failure.
        :param message: Failure message.
        :param path: The relative path in the target where the failure occurred. If the failure occurred at root of the match tree, set the path to an empty list. If it occurs in the 5th index of an array nested within the 'foo' key of an object, set the path as ``['/foo', '[5]']``.
        '''
        failure = MatchFailure(matcher=matcher, message=message, path=path)

        return typing.cast("MatchResult", jsii.invoke(self, "recordFailure", [failure]))

    @jsii.member(jsii_name="toHumanStrings")
    def to_human_strings(self) -> typing.List[builtins.str]:
        '''Get the list of failures as human readable strings.'''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "toHumanStrings", []))

    @builtins.property
    @jsii.member(jsii_name="failCount")
    def fail_count(self) -> jsii.Number:
        '''The number of failures.'''
        return typing.cast(jsii.Number, jsii.get(self, "failCount"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> typing.Any:
        '''The target for which this result was generated.'''
        return typing.cast(typing.Any, jsii.get(self, "target"))


class Matcher(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/assertions.Matcher",
):
    '''Represents a matcher that can perform special data matching capabilities between a given pattern and a target.

    :exampleMetadata: infused

    Example::

        # Given a template -
        # {
        #   "Resources": {
        #     "MyBar": {
        #       "Type": "Foo::Bar",
        #       "Properties": {
        #         "Fred": ["Flob", "Cat"]
        #       }
        #     }
        #   }
        # }
        
        # The following will NOT throw an assertion error
        template.has_resource_properties("Foo::Bar", {
            "Fred": Match.array_with(["Flob"])
        })
        
        # The following will throw an assertion error
        template.has_resource_properties("Foo::Bar", Match.object_like({
            "Fred": Match.array_with(["Wobble"])
        }))
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="isMatcher")
    @builtins.classmethod
    def is_matcher(cls, x: typing.Any) -> builtins.bool:
        '''Check whether the provided object is a subtype of the ``IMatcher``.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b766e18352f2b7f0dc4b9783948a2df4eb151d5b1ac4ec12cf834d4a4c4e5b)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isMatcher", [x]))

    @jsii.member(jsii_name="test")
    @abc.abstractmethod
    def test(self, actual: typing.Any) -> MatchResult:
        '''Test whether a target matches the provided pattern.

        Every Matcher must implement this method.
        This method will be invoked by the assertions framework. Do not call this method directly.

        :param actual: the target to match.

        :return: the list of match failures. An empty array denotes a successful match.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        '''A name for the matcher.

        This is collected as part of the result and may be presented to the user.
        '''
        ...


class _MatcherProxy(Matcher):
    @jsii.member(jsii_name="test")
    def test(self, actual: typing.Any) -> MatchResult:
        '''Test whether a target matches the provided pattern.

        Every Matcher must implement this method.
        This method will be invoked by the assertions framework. Do not call this method directly.

        :param actual: the target to match.

        :return: the list of match failures. An empty array denotes a successful match.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b2345ca70fbb3e7e2b835aa079f9bd835c0e14d5444be5b45b4541f0a4638dd)
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
        return typing.cast(MatchResult, jsii.invoke(self, "test", [actual]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the matcher.

        This is collected as part of the result and may be presented to the user.
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Matcher).__jsii_proxy_class__ = lambda : _MatcherProxy


class Template(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assertions.Template"):
    '''Suite of assertions that can be run on a CDK stack.

    Typically used, as part of unit tests, to validate that the rendered
    CloudFormation template has expected resources and properties.

    :exampleMetadata: nofixture infused

    Example::

        from aws_cdk.core import Stack
        from aws_cdk.assertions import Template
        
        stack = Stack()
        # ...
        template = Template.from_stack(stack)
    '''

    @jsii.member(jsii_name="fromJSON")
    @builtins.classmethod
    def from_json(
        cls,
        template: typing.Mapping[builtins.str, typing.Any],
    ) -> "Template":
        '''Base your assertions from an existing CloudFormation template formatted as an in-memory JSON object.

        :param template: the CloudFormation template formatted as a nested set of records.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96dcbc23e9b1275d1a851aa7f894d0e0e530a8ef7fdb10e4db58bb9c910ca9ec)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        return typing.cast("Template", jsii.sinvoke(cls, "fromJSON", [template]))

    @jsii.member(jsii_name="fromStack")
    @builtins.classmethod
    def from_stack(cls, stack: _aws_cdk_core_f4b25747.Stack) -> "Template":
        '''Base your assertions on the CloudFormation template synthesized by a CDK ``Stack``.

        :param stack: the CDK Stack to run assertions on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeed46da25e136d26947ea8f1705146b14d3a3fb7b6ca4be311c205738b7c6b1)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast("Template", jsii.sinvoke(cls, "fromStack", [stack]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, template: builtins.str) -> "Template":
        '''Base your assertions from an existing CloudFormation template formatted as a JSON string.

        :param template: the CloudFormation template in.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b16a8ad424155231dad2c542a177d5e242eb4c3415c35b9b741bc70d01d42c5)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        return typing.cast("Template", jsii.sinvoke(cls, "fromString", [template]))

    @jsii.member(jsii_name="findConditions")
    def find_conditions(
        self,
        logical_id: builtins.str,
        props: typing.Any = None,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''Get the set of matching Conditions that match the given properties in the CloudFormation template.

        :param logical_id: the name of the condition. Provide ``'*'`` to match all conditions in the template.
        :param props: by default, matches all Conditions in the template. When a literal object is provided, performs a partial match via ``Match.objectLike()``. Use the ``Match`` APIs to configure a different behaviour.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699f5ca6452f893ae4ef3a193d6cce1eb34c9741dbe5ee3a277847b8761b6b4c)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.invoke(self, "findConditions", [logical_id, props]))

    @jsii.member(jsii_name="findMappings")
    def find_mappings(
        self,
        logical_id: builtins.str,
        props: typing.Any = None,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''Get the set of matching Mappings that match the given properties in the CloudFormation template.

        :param logical_id: the name of the mapping. Provide ``'*'`` to match all mappings in the template.
        :param props: by default, matches all Mappings in the template. When a literal object is provided, performs a partial match via ``Match.objectLike()``. Use the ``Match`` APIs to configure a different behaviour.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63be95806acdc9131cb2d57368cebc46740f27c49e967975c62a08a78f76162a)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.invoke(self, "findMappings", [logical_id, props]))

    @jsii.member(jsii_name="findOutputs")
    def find_outputs(
        self,
        logical_id: builtins.str,
        props: typing.Any = None,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''Get the set of matching Outputs that match the given properties in the CloudFormation template.

        :param logical_id: the name of the output. Provide ``'*'`` to match all outputs in the template.
        :param props: by default, matches all Outputs in the template. When a literal object is provided, performs a partial match via ``Match.objectLike()``. Use the ``Match`` APIs to configure a different behaviour.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ad9611bd3e614a8136f850fc56196a997a10ef95b4a169ae6393aece2c6ff6)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.invoke(self, "findOutputs", [logical_id, props]))

    @jsii.member(jsii_name="findParameters")
    def find_parameters(
        self,
        logical_id: builtins.str,
        props: typing.Any = None,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''Get the set of matching Parameters that match the given properties in the CloudFormation template.

        :param logical_id: the name of the parameter. Provide ``'*'`` to match all parameters in the template.
        :param props: by default, matches all Parameters in the template. When a literal object is provided, performs a partial match via ``Match.objectLike()``. Use the ``Match`` APIs to configure a different behaviour.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0edc994a16140d14bf7832adbd878016ddd3d74a198be919a7ac48974b410876)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.invoke(self, "findParameters", [logical_id, props]))

    @jsii.member(jsii_name="findResources")
    def find_resources(
        self,
        type: builtins.str,
        props: typing.Any = None,
    ) -> typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]]:
        '''Get the set of matching resources of a given type and properties in the CloudFormation template.

        :param type: the type to match in the CloudFormation template.
        :param props: by default, matches all resources with the given type. When a literal is provided, performs a partial match via ``Match.objectLike()``. Use the ``Match`` APIs to configure a different behaviour.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1be668a5f6ff542b43cc17c68fbf616c3c99cd93123bd3f9b4ba3f152acf87)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Mapping[builtins.str, typing.Any]], jsii.invoke(self, "findResources", [type, props]))

    @jsii.member(jsii_name="hasCondition")
    def has_condition(self, logical_id: builtins.str, props: typing.Any) -> None:
        '''Assert that a Condition with the given properties exists in the CloudFormation template.

        By default, performs partial matching on the resource, via the ``Match.objectLike()``.
        To configure different behavour, use other matchers in the ``Match`` class.

        :param logical_id: the name of the mapping. Provide ``'*'`` to match all conditions in the template.
        :param props: the output as should be expected in the template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d78c06892688cd43143d5794593a28790b1db17b68a827375b3f76e4b66e37)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasCondition", [logical_id, props]))

    @jsii.member(jsii_name="hasMapping")
    def has_mapping(self, logical_id: builtins.str, props: typing.Any) -> None:
        '''Assert that a Mapping with the given properties exists in the CloudFormation template.

        By default, performs partial matching on the resource, via the ``Match.objectLike()``.
        To configure different behavour, use other matchers in the ``Match`` class.

        :param logical_id: the name of the mapping. Provide ``'*'`` to match all mappings in the template.
        :param props: the output as should be expected in the template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3ff62ce48765704006054f8fa4f7fb5823938f0706f74029257ac2e52bd4b6)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasMapping", [logical_id, props]))

    @jsii.member(jsii_name="hasOutput")
    def has_output(self, logical_id: builtins.str, props: typing.Any) -> None:
        '''Assert that an Output with the given properties exists in the CloudFormation template.

        By default, performs partial matching on the resource, via the ``Match.objectLike()``.
        To configure different behavour, use other matchers in the ``Match`` class.

        :param logical_id: the name of the output. Provide ``'*'`` to match all outputs in the template.
        :param props: the output as should be expected in the template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c955bc900b00f4049500ed9576b903a60f9f439f61016fca3448765d1e6dece)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasOutput", [logical_id, props]))

    @jsii.member(jsii_name="hasParameter")
    def has_parameter(self, logical_id: builtins.str, props: typing.Any) -> None:
        '''Assert that a Parameter with the given properties exists in the CloudFormation template.

        By default, performs partial matching on the parameter, via the ``Match.objectLike()``.
        To configure different behavior, use other matchers in the ``Match`` class.

        :param logical_id: the name of the parameter. Provide ``'*'`` to match all parameters in the template.
        :param props: the parameter as should be expected in the template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712e8be0129d45c91065aa69aec87ac51d54d80393899fb3ca7b7f158157d155)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasParameter", [logical_id, props]))

    @jsii.member(jsii_name="hasResource")
    def has_resource(self, type: builtins.str, props: typing.Any) -> None:
        '''Assert that a resource of the given type and given definition exists in the CloudFormation template.

        By default, performs partial matching on the resource, via the ``Match.objectLike()``.
        To configure different behavour, use other matchers in the ``Match`` class.

        :param type: the resource type; ex: ``AWS::S3::Bucket``
        :param props: the entire defintion of the resource as should be expected in the template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a29912f59d4a3fb117406c8776145d047f9c210e9d2d8c1f3110f622cf0d33a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasResource", [type, props]))

    @jsii.member(jsii_name="hasResourceProperties")
    def has_resource_properties(self, type: builtins.str, props: typing.Any) -> None:
        '''Assert that a resource of the given type and properties exists in the CloudFormation template.

        By default, performs partial matching on the ``Properties`` key of the resource, via the
        ``Match.objectLike()``. To configure different behavour, use other matchers in the ``Match`` class.

        :param type: the resource type; ex: ``AWS::S3::Bucket``
        :param props: the 'Properties' section of the resource as should be expected in the template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4021ae9e71e8fb6a459d37d7df6391d527b831bbe4b1faf16e7e11fdbcf55b90)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(None, jsii.invoke(self, "hasResourceProperties", [type, props]))

    @jsii.member(jsii_name="resourceCountIs")
    def resource_count_is(self, type: builtins.str, count: jsii.Number) -> None:
        '''Assert that the given number of resources of the given type exist in the template.

        :param type: the resource type; ex: ``AWS::S3::Bucket``
        :param count: number of expected instances.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc6ab862f51901a5025f2b2d7e35f60d161a5d8e4e5806e52f36ef67ca90fbe)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        return typing.cast(None, jsii.invoke(self, "resourceCountIs", [type, count]))

    @jsii.member(jsii_name="templateMatches")
    def template_matches(self, expected: typing.Any) -> None:
        '''Assert that the CloudFormation template matches the given value.

        :param expected: the expected CloudFormation template as key-value pairs.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086c4a2c4ad8ba8f82afc59a6eb7594c1904290498facbd7408dd7aab412d95b)
            check_type(argname="argument expected", value=expected, expected_type=type_hints["expected"])
        return typing.cast(None, jsii.invoke(self, "templateMatches", [expected]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''The CloudFormation template deserialized into an object.'''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "toJSON", []))


class Capture(
    Matcher,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/assertions.Capture",
):
    '''Capture values while matching templates.

    Using an instance of this class within a Matcher will capture the matching value.
    The ``as*()`` APIs on the instance can be used to get the captured value.

    :exampleMetadata: infused

    Example::

        # Given a template -
        # {
        #   "Resources": {
        #     "MyBar": {
        #       "Type": "Foo::Bar",
        #       "Properties": {
        #         "Fred": "Flob",
        #       }
        #     },
        #     "MyBaz": {
        #       "Type": "Foo::Bar",
        #       "Properties": {
        #         "Fred": "Quib",
        #       }
        #     }
        #   }
        # }
        
        fred_capture = Capture()
        template.has_resource_properties("Foo::Bar", {
            "Fred": fred_capture
        })
        
        fred_capture.as_string() # returns "Flob"
        fred_capture.next() # returns true
        fred_capture.as_string()
    '''

    def __init__(self, pattern: typing.Any = None) -> None:
        '''Initialize a new capture.

        :param pattern: a nested pattern or Matcher. If a nested pattern is provided ``objectLike()`` matching is applied.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a8ac84aea9975ddab49bc89272f9f0728502816218b8d96ff90b9255759a46a)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        jsii.create(self.__class__, self, [pattern])

    @jsii.member(jsii_name="asArray")
    def as_array(self) -> typing.List[typing.Any]:
        '''Retrieve the captured value as an array.

        An error is generated if no value is captured or if the value is not an array.
        '''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "asArray", []))

    @jsii.member(jsii_name="asBoolean")
    def as_boolean(self) -> builtins.bool:
        '''Retrieve the captured value as a boolean.

        An error is generated if no value is captured or if the value is not a boolean.
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "asBoolean", []))

    @jsii.member(jsii_name="asNumber")
    def as_number(self) -> jsii.Number:
        '''Retrieve the captured value as a number.

        An error is generated if no value is captured or if the value is not a number.
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "asNumber", []))

    @jsii.member(jsii_name="asObject")
    def as_object(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Retrieve the captured value as a JSON object.

        An error is generated if no value is captured or if the value is not an object.
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "asObject", []))

    @jsii.member(jsii_name="asString")
    def as_string(self) -> builtins.str:
        '''Retrieve the captured value as a string.

        An error is generated if no value is captured or if the value is not a string.
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "asString", []))

    @jsii.member(jsii_name="next")
    def next(self) -> builtins.bool:
        '''When multiple results are captured, move the iterator to the next result.

        :return: true if another capture is present, false otherwise
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "next", []))

    @jsii.member(jsii_name="test")
    def test(self, actual: typing.Any) -> MatchResult:
        '''Test whether a target matches the provided pattern.

        Every Matcher must implement this method.
        This method will be invoked by the assertions framework. Do not call this method directly.

        :param actual: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3dbb142bc4a308005a503eb5aa33e3bd3d79e252d05301ec962a7917e36c9a)
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
        return typing.cast(MatchResult, jsii.invoke(self, "test", [actual]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the matcher.

        This is collected as part of the result and may be presented to the user.
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


__all__ = [
    "Annotations",
    "Capture",
    "Match",
    "MatchCapture",
    "MatchFailure",
    "MatchResult",
    "Matcher",
    "Template",
]

publication.publish()

def _typecheckingstub__4776f3330e9f7c7c149d8e58636faf4bb7b7af2d47493c52f41a29501e257162(
    stack: _aws_cdk_core_f4b25747.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926cdc57b33370dbaae7f42c0146d498880442679248560af04f5d0138450a13(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e1d77cfc14858b867b433ed3b1e377fd3a817bea19f66c139f9ee420ee9f48(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fac69bd448b958d44579d4c494bd116210d0a48591a10c5c14fd082735db502(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a869ba274728ae9608a5b315ed01d41a7ea9eb5bfac2dfd3d5afc2c3a8f30b(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a8b81413e5985c79dfe32bdc54d4780a8d6240fc4887e05764b93551f5be98(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449dd2e59a7da77170ba8cb2523f7e7a97bf0ed723456540c32e716200eaf2ef(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d576bffef3dc6d940c0f3e1a894e54722abf373ad83a17cbc8324eb339d11a9c(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7475b4f161319d93d660ae5a788269cd0f6a73b1ac7e6d1ad072a4068d6faac5(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d514b512db676ee5a943271fb9b9a057893b1b3d93ddb13be9e0441fb3f2f3(
    construct_path: builtins.str,
    message: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebfea2b7fe77abd2d67255287185c7ca09d748790bb537192cd7cdcdc768fcd(
    pattern: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46c96a58e6ed805ee3728f4912911fe4de977713cb40c1517a47ebc01b2240d(
    pattern: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f7b8a3bcd5101cbcfed6bd62706be40c8c5a33f0a41d1047d11aa608b0d4b0(
    pattern: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca9e0aeebfbe461e09b97dbd3b420b4c64e8a3683b345580a0081a9c9a22f5e(
    pattern: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6ad13d0cdc150262ff11a0028408e347591b4b6e5fcc57b564b665e7f53c32(
    pattern: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d99129cd34c2ee16315b19771583a262754032dcfc992e1f2ca8a137e78eeee(
    pattern: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e49b581a299c812014dbbea0c6e55a4317ee355d1584ab11c7420735591134f(
    pattern: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20e44f3feeb105b943805f455a7729b93d9586037c13056e0f7487f5bf5ade0(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85aa91a87986009f605a2ae1a32b7350ef70dfbbe6e3bf99f6bc4f5673798736(
    *,
    capture: Capture,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35cef13b82962737b757f37428b05befa6096945b04b75e1af6a45fca17fdbe(
    *,
    matcher: Matcher,
    message: builtins.str,
    path: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584cd61323669b435ec39752ea455b7b3b552ecc0fb627b85bd1135417e22ed8(
    target: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1654ecc612a339620fef05a2b1f41f153491cb2154773d8e9d66d6a57998a6a7(
    id: builtins.str,
    inner: MatchResult,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9694d7304cba82ed278f97224420a71cefaef5968f9ca63c99385456328a15d4(
    matcher: Matcher,
    path: typing.Sequence[builtins.str],
    message: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b766e18352f2b7f0dc4b9783948a2df4eb151d5b1ac4ec12cf834d4a4c4e5b(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2345ca70fbb3e7e2b835aa079f9bd835c0e14d5444be5b45b4541f0a4638dd(
    actual: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96dcbc23e9b1275d1a851aa7f894d0e0e530a8ef7fdb10e4db58bb9c910ca9ec(
    template: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeed46da25e136d26947ea8f1705146b14d3a3fb7b6ca4be311c205738b7c6b1(
    stack: _aws_cdk_core_f4b25747.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b16a8ad424155231dad2c542a177d5e242eb4c3415c35b9b741bc70d01d42c5(
    template: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699f5ca6452f893ae4ef3a193d6cce1eb34c9741dbe5ee3a277847b8761b6b4c(
    logical_id: builtins.str,
    props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63be95806acdc9131cb2d57368cebc46740f27c49e967975c62a08a78f76162a(
    logical_id: builtins.str,
    props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ad9611bd3e614a8136f850fc56196a997a10ef95b4a169ae6393aece2c6ff6(
    logical_id: builtins.str,
    props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0edc994a16140d14bf7832adbd878016ddd3d74a198be919a7ac48974b410876(
    logical_id: builtins.str,
    props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1be668a5f6ff542b43cc17c68fbf616c3c99cd93123bd3f9b4ba3f152acf87(
    type: builtins.str,
    props: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d78c06892688cd43143d5794593a28790b1db17b68a827375b3f76e4b66e37(
    logical_id: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3ff62ce48765704006054f8fa4f7fb5823938f0706f74029257ac2e52bd4b6(
    logical_id: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c955bc900b00f4049500ed9576b903a60f9f439f61016fca3448765d1e6dece(
    logical_id: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712e8be0129d45c91065aa69aec87ac51d54d80393899fb3ca7b7f158157d155(
    logical_id: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a29912f59d4a3fb117406c8776145d047f9c210e9d2d8c1f3110f622cf0d33a(
    type: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4021ae9e71e8fb6a459d37d7df6391d527b831bbe4b1faf16e7e11fdbcf55b90(
    type: builtins.str,
    props: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc6ab862f51901a5025f2b2d7e35f60d161a5d8e4e5806e52f36ef67ca90fbe(
    type: builtins.str,
    count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086c4a2c4ad8ba8f82afc59a6eb7594c1904290498facbd7408dd7aab412d95b(
    expected: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8ac84aea9975ddab49bc89272f9f0728502816218b8d96ff90b9255759a46a(
    pattern: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3dbb142bc4a308005a503eb5aa33e3bd3d79e252d05301ec962a7917e36c9a(
    actual: typing.Any,
) -> None:
    """Type checking stubs"""
    pass
