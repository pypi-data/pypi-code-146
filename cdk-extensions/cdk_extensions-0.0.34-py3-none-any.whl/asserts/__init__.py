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

import aws_cdk.assertions


class JoinedJson(
    aws_cdk.assertions.Matcher,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.asserts.JoinedJson",
):
    def __init__(self, pattern: typing.Any) -> None:
        '''
        :param pattern: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JoinedJson.__init__)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        jsii.create(self.__class__, self, [pattern])

    @jsii.member(jsii_name="test")
    def test(self, actual: typing.Any) -> aws_cdk.assertions.MatchResult:
        '''Test whether a target matches the provided pattern.

        Every Matcher must implement this method.
        This method will be invoked by the assertions framework. Do not call this method directly.

        :param actual: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JoinedJson.test)
            check_type(argname="argument actual", value=actual, expected_type=type_hints["actual"])
        return typing.cast(aws_cdk.assertions.MatchResult, jsii.invoke(self, "test", [actual]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the matcher.

        This is collected as part of the result and may be presented to the user.
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class Match(
    aws_cdk.assertions.Match,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.asserts.Match",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="joinedJson")
    @builtins.classmethod
    def joined_json(cls, pattern: typing.Any) -> aws_cdk.assertions.Matcher:
        '''
        :param pattern: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Match.joined_json)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast(aws_cdk.assertions.Matcher, jsii.sinvoke(cls, "joinedJson", [pattern]))


__all__ = [
    "JoinedJson",
    "Match",
]

publication.publish()
