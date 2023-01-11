'''
# AWS WAF Regional Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_wafregional as wafregional
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for WAFRegional construct libraries](https://constructs.dev/search?q=wafregional)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::WAFRegional resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WAFRegional.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::WAFRegional](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WAFRegional.html).

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
class CfnByteMatchSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnByteMatchSet",
):
    '''A CloudFormation ``AWS::WAFRegional::ByteMatchSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    The ``AWS::WAFRegional::ByteMatchSet`` resource creates an AWS WAF ``ByteMatchSet`` that identifies a part of a web request that you want to inspect.

    :cloudformationResource: AWS::WAFRegional::ByteMatchSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_byte_match_set = wafregional.CfnByteMatchSet(self, "MyCfnByteMatchSet",
            name="name",
        
            # the properties below are optional
            byte_match_tuples=[wafregional.CfnByteMatchSet.ByteMatchTupleProperty(
                field_to_match=wafregional.CfnByteMatchSet.FieldToMatchProperty(
                    type="type",
        
                    # the properties below are optional
                    data="data"
                ),
                positional_constraint="positionalConstraint",
                text_transformation="textTransformation",
        
                # the properties below are optional
                target_string="targetString",
                target_string_base64="targetStringBase64"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        byte_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnByteMatchSet.ByteMatchTupleProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFRegional::ByteMatchSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A friendly name or description of the ``ByteMatchSet`` . You can't change ``Name`` after you create a ``ByteMatchSet`` .
        :param byte_match_tuples: Specifies the bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae63cbf467e3ff3e3c6b8d6b285887e2ae652922cc71eb7bb59b95c5a6b70e0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnByteMatchSetProps(name=name, byte_match_tuples=byte_match_tuples)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ddfa33dac211ba0ee7aac4b5f6fe5024ad7a31d28b1f8f34e4447ffbde95b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6536db848f978e45ac33a419a2125733d829f99bcf122ef89ec97e96818db20)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``ByteMatchSet`` .

        You can't change ``Name`` after you create a ``ByteMatchSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html#cfn-wafregional-bytematchset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b98ec0fc5a55e39713b858a083753ff59459356a819f2f8e539943a9de8f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="byteMatchTuples")
    def byte_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnByteMatchSet.ByteMatchTupleProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''Specifies the bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html#cfn-wafregional-bytematchset-bytematchtuples
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnByteMatchSet.ByteMatchTupleProperty", _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "byteMatchTuples"))

    @byte_match_tuples.setter
    def byte_match_tuples(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnByteMatchSet.ByteMatchTupleProperty", _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__239b1ba1fe61fa61bb32db6f9d716e237a345858d28adab98b570ca6fa5f6cd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "byteMatchTuples", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnByteMatchSet.ByteMatchTupleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "positional_constraint": "positionalConstraint",
            "text_transformation": "textTransformation",
            "target_string": "targetString",
            "target_string_base64": "targetStringBase64",
        },
    )
    class ByteMatchTupleProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnByteMatchSet.FieldToMatchProperty", typing.Dict[builtins.str, typing.Any]]],
            positional_constraint: builtins.str,
            text_transformation: builtins.str,
            target_string: typing.Optional[builtins.str] = None,
            target_string_base64: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   This is *AWS WAF Classic* documentation.

            For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
            .. epigraph::

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            The bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.

            :param field_to_match: The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.
            :param positional_constraint: Within the portion of a web request that you want to search (for example, in the query string, if any), specify where you want AWS WAF to search. Valid values include the following: *CONTAINS* The specified part of the web request must include the value of ``TargetString`` , but the location doesn't matter. *CONTAINS_WORD* The specified part of the web request must include the value of ``TargetString`` , and ``TargetString`` must contain only alphanumeric characters or underscore (A-Z, a-z, 0-9, or _). In addition, ``TargetString`` must be a word, which means one of the following: - ``TargetString`` exactly matches the value of the specified part of the web request, such as the value of a header. - ``TargetString`` is at the beginning of the specified part of the web request and is followed by a character other than an alphanumeric character or underscore (_), for example, ``BadBot;`` . - ``TargetString`` is at the end of the specified part of the web request and is preceded by a character other than an alphanumeric character or underscore (_), for example, ``;BadBot`` . - ``TargetString`` is in the middle of the specified part of the web request and is preceded and followed by characters other than alphanumeric characters or underscore (_), for example, ``-BadBot;`` . *EXACTLY* The value of the specified part of the web request must exactly match the value of ``TargetString`` . *STARTS_WITH* The value of ``TargetString`` must appear at the beginning of the specified part of the web request. *ENDS_WITH* The value of ``TargetString`` must appear at the end of the specified part of the web request.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match. You can only specify a single type of TextTransformation. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value. *NONE* Specify ``NONE`` if you don't want to perform any text transformations.
            :param target_string: The value that you want AWS WAF to search for. AWS WAF searches for the specified string in the part of web requests that you specified in ``FieldToMatch`` . The maximum length of the value is 50 bytes. You must specify this property or the ``TargetStringBase64`` property. Valid values depend on the values that you specified for ``FieldToMatch`` : - ``HEADER`` : The value that you want AWS WAF to search for in the request header that you specified in ``FieldToMatch`` , for example, the value of the ``User-Agent`` or ``Referer`` header. - ``METHOD`` : The HTTP method, which indicates the type of operation specified in the request. - ``QUERY_STRING`` : The value that you want AWS WAF to search for in the query string, which is the part of a URL that appears after a ``?`` character. - ``URI`` : The value that you want AWS WAF to search for in the part of a URL that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but instead of inspecting a single parameter, AWS WAF inspects all parameters within the query string for the value or regex pattern that you specify in ``TargetString`` . If ``TargetString`` includes alphabetic characters A-Z and a-z, note that the value is case sensitive.
            :param target_string_base64: The base64-encoded value that AWS WAF searches for. AWS CloudFormation sends this value to AWS WAF without encoding it. You must specify this property or the ``TargetString`` property. AWS WAF searches for this value in a specific part of web requests, which you define in the ``FieldToMatch`` property. Valid values depend on the Type value in the ``FieldToMatch`` property. For example, for a ``METHOD`` type, you must specify HTTP methods such as ``DELETE, GET, HEAD, OPTIONS, PATCH, POST`` , and ``PUT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                byte_match_tuple_property = wafregional.CfnByteMatchSet.ByteMatchTupleProperty(
                    field_to_match=wafregional.CfnByteMatchSet.FieldToMatchProperty(
                        type="type",
                
                        # the properties below are optional
                        data="data"
                    ),
                    positional_constraint="positionalConstraint",
                    text_transformation="textTransformation",
                
                    # the properties below are optional
                    target_string="targetString",
                    target_string_base64="targetStringBase64"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7bad6b0c549eae06757b16d2a78b0845d31d285d02641273a99b0f74275dbe8)
                check_type(argname="argument field_to_match", value=field_to_match, expected_type=type_hints["field_to_match"])
                check_type(argname="argument positional_constraint", value=positional_constraint, expected_type=type_hints["positional_constraint"])
                check_type(argname="argument text_transformation", value=text_transformation, expected_type=type_hints["text_transformation"])
                check_type(argname="argument target_string", value=target_string, expected_type=type_hints["target_string"])
                check_type(argname="argument target_string_base64", value=target_string_base64, expected_type=type_hints["target_string_base64"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "field_to_match": field_to_match,
                "positional_constraint": positional_constraint,
                "text_transformation": text_transformation,
            }
            if target_string is not None:
                self._values["target_string"] = target_string
            if target_string_base64 is not None:
                self._values["target_string_base64"] = target_string_base64

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnByteMatchSet.FieldToMatchProperty"]:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnByteMatchSet.FieldToMatchProperty"], result)

        @builtins.property
        def positional_constraint(self) -> builtins.str:
            '''Within the portion of a web request that you want to search (for example, in the query string, if any), specify where you want AWS WAF to search.

            Valid values include the following:

            *CONTAINS*

            The specified part of the web request must include the value of ``TargetString`` , but the location doesn't matter.

            *CONTAINS_WORD*

            The specified part of the web request must include the value of ``TargetString`` , and ``TargetString`` must contain only alphanumeric characters or underscore (A-Z, a-z, 0-9, or _). In addition, ``TargetString`` must be a word, which means one of the following:

            - ``TargetString`` exactly matches the value of the specified part of the web request, such as the value of a header.
            - ``TargetString`` is at the beginning of the specified part of the web request and is followed by a character other than an alphanumeric character or underscore (_), for example, ``BadBot;`` .
            - ``TargetString`` is at the end of the specified part of the web request and is preceded by a character other than an alphanumeric character or underscore (_), for example, ``;BadBot`` .
            - ``TargetString`` is in the middle of the specified part of the web request and is preceded and followed by characters other than alphanumeric characters or underscore (_), for example, ``-BadBot;`` .

            *EXACTLY*

            The value of the specified part of the web request must exactly match the value of ``TargetString`` .

            *STARTS_WITH*

            The value of ``TargetString`` must appear at the beginning of the specified part of the web request.

            *ENDS_WITH*

            The value of ``TargetString`` must appear at the end of the specified part of the web request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-positionalconstraint
            '''
            result = self._values.get("positional_constraint")
            assert result is not None, "Required property 'positional_constraint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def text_transformation(self) -> builtins.str:
            '''Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF .

            If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match.

            You can only specify a single type of TextTransformation.

            *CMD_LINE*

            When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations:

            - Delete the following characters: \\ " ' ^
            - Delete spaces before the following characters: / (
            - Replace the following characters with a space: , ;
            - Replace multiple spaces with one space
            - Convert uppercase letters (A-Z) to lowercase (a-z)

            *COMPRESS_WHITE_SPACE*

            Use this option to replace the following characters with a space character (decimal 32):

            - \\f, formfeed, decimal 12
            - \\t, tab, decimal 9
            - \\n, newline, decimal 10
            - \\r, carriage return, decimal 13
            - \\v, vertical tab, decimal 11
            - non-breaking space, decimal 160

            ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.

            *HTML_ENTITY_DECODE*

            Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations:

            - Replaces ``(ampersand)quot;`` with ``"``
            - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
            - Replaces ``(ampersand)lt;`` with a "less than" symbol
            - Replaces ``(ampersand)gt;`` with ``>``
            - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters
            - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters

            *LOWERCASE*

            Use this option to convert uppercase letters (A-Z) to lowercase (a-z).

            *URL_DECODE*

            Use this option to decode a URL-encoded value.

            *NONE*

            Specify ``NONE`` if you don't want to perform any text transformations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-texttransformation
            '''
            result = self._values.get("text_transformation")
            assert result is not None, "Required property 'text_transformation' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target_string(self) -> typing.Optional[builtins.str]:
            '''The value that you want AWS WAF to search for.

            AWS WAF searches for the specified string in the part of web requests that you specified in ``FieldToMatch`` . The maximum length of the value is 50 bytes.

            You must specify this property or the ``TargetStringBase64`` property.

            Valid values depend on the values that you specified for ``FieldToMatch`` :

            - ``HEADER`` : The value that you want AWS WAF to search for in the request header that you specified in ``FieldToMatch`` , for example, the value of the ``User-Agent`` or ``Referer`` header.
            - ``METHOD`` : The HTTP method, which indicates the type of operation specified in the request.
            - ``QUERY_STRING`` : The value that you want AWS WAF to search for in the query string, which is the part of a URL that appears after a ``?`` character.
            - ``URI`` : The value that you want AWS WAF to search for in the part of a URL that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but instead of inspecting a single parameter, AWS WAF inspects all parameters within the query string for the value or regex pattern that you specify in ``TargetString`` .

            If ``TargetString`` includes alphabetic characters A-Z and a-z, note that the value is case sensitive.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-targetstring
            '''
            result = self._values.get("target_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_string_base64(self) -> typing.Optional[builtins.str]:
            '''The base64-encoded value that AWS WAF searches for. AWS CloudFormation sends this value to AWS WAF without encoding it.

            You must specify this property or the ``TargetString`` property.

            AWS WAF searches for this value in a specific part of web requests, which you define in the ``FieldToMatch`` property.

            Valid values depend on the Type value in the ``FieldToMatch`` property. For example, for a ``METHOD`` type, you must specify HTTP methods such as ``DELETE, GET, HEAD, OPTIONS, PATCH, POST`` , and ``PUT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-targetstringbase64
            '''
            result = self._values.get("target_string_base64")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ByteMatchTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnByteMatchSet.FieldToMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "data": "data"},
    )
    class FieldToMatchProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   This is *AWS WAF Classic* documentation.

            For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
            .. epigraph::

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            Specifies where in a web request to look for ``TargetString`` .

            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform. - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .
            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                field_to_match_property = wafregional.CfnByteMatchSet.FieldToMatchProperty(
                    type="type",
                
                    # the properties below are optional
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__64319f6759e7e4aa082a4633fb674506f7ba1fbcf59a86bea959524adf45e094)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if data is not None:
                self._values["data"] = data

        @builtins.property
        def type(self) -> builtins.str:
            '''The part of the web request that you want AWS WAF to search for a specified string.

            Parts of a request that you can search include the following:

            - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` .
            - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform.
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-fieldtomatch.html#cfn-wafregional-bytematchset-fieldtomatch-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` .

            The name of the header is not case sensitive.

            When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive.

            If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-fieldtomatch.html#cfn-wafregional-bytematchset-fieldtomatch-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldToMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnByteMatchSetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "byte_match_tuples": "byteMatchTuples"},
)
class CfnByteMatchSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        byte_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnByteMatchSet.ByteMatchTupleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnByteMatchSet``.

        :param name: A friendly name or description of the ``ByteMatchSet`` . You can't change ``Name`` after you create a ``ByteMatchSet`` .
        :param byte_match_tuples: Specifies the bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_byte_match_set_props = wafregional.CfnByteMatchSetProps(
                name="name",
            
                # the properties below are optional
                byte_match_tuples=[wafregional.CfnByteMatchSet.ByteMatchTupleProperty(
                    field_to_match=wafregional.CfnByteMatchSet.FieldToMatchProperty(
                        type="type",
            
                        # the properties below are optional
                        data="data"
                    ),
                    positional_constraint="positionalConstraint",
                    text_transformation="textTransformation",
            
                    # the properties below are optional
                    target_string="targetString",
                    target_string_base64="targetStringBase64"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0265e2ffb25f4ad7e97879144a3f2b05ac3dd8a050b6f29f6438f73a25a21c75)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument byte_match_tuples", value=byte_match_tuples, expected_type=type_hints["byte_match_tuples"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if byte_match_tuples is not None:
            self._values["byte_match_tuples"] = byte_match_tuples

    @builtins.property
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``ByteMatchSet`` .

        You can't change ``Name`` after you create a ``ByteMatchSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html#cfn-wafregional-bytematchset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def byte_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnByteMatchSet.ByteMatchTupleProperty, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''Specifies the bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html#cfn-wafregional-bytematchset-bytematchtuples
        '''
        result = self._values.get("byte_match_tuples")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnByteMatchSet.ByteMatchTupleProperty, _aws_cdk_core_f4b25747.IResolvable]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnByteMatchSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnGeoMatchSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnGeoMatchSet",
):
    '''A CloudFormation ``AWS::WAFRegional::GeoMatchSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    Contains one or more countries that AWS WAF will search for.

    :cloudformationResource: AWS::WAFRegional::GeoMatchSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-geomatchset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_geo_match_set = wafregional.CfnGeoMatchSet(self, "MyCfnGeoMatchSet",
            name="name",
        
            # the properties below are optional
            geo_match_constraints=[wafregional.CfnGeoMatchSet.GeoMatchConstraintProperty(
                type="type",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        geo_match_constraints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnGeoMatchSet.GeoMatchConstraintProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFRegional::GeoMatchSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A friendly name or description of the ``GeoMatchSet`` . You can't change the name of an ``GeoMatchSet`` after you create it.
        :param geo_match_constraints: An array of ``GeoMatchConstraint`` objects, which contain the country that you want AWS WAF to search for.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a389e753656373661a818bda860db59cfc521d153e0491ad0b00254cfda620)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGeoMatchSetProps(
            name=name, geo_match_constraints=geo_match_constraints
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4242f7c2138da06e509eea43351baa3840c7e190be8fda2bc558a42215fde0a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1104a1b28dc16c72fc1b3154f9da5448083280ae7c9415516ff91a10884952d4)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``GeoMatchSet`` .

        You can't change the name of an ``GeoMatchSet`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-geomatchset.html#cfn-wafregional-geomatchset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71cad14f14431a0dacfba5259ae0250322b372acfc7da24285f123cc4825d249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="geoMatchConstraints")
    def geo_match_constraints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGeoMatchSet.GeoMatchConstraintProperty"]]]]:
        '''An array of ``GeoMatchConstraint`` objects, which contain the country that you want AWS WAF to search for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-geomatchset.html#cfn-wafregional-geomatchset-geomatchconstraints
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGeoMatchSet.GeoMatchConstraintProperty"]]]], jsii.get(self, "geoMatchConstraints"))

    @geo_match_constraints.setter
    def geo_match_constraints(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGeoMatchSet.GeoMatchConstraintProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba89c7c1672048011be38d0b8f438c767dbb3ad33d065e63e755f4de0c157342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geoMatchConstraints", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnGeoMatchSet.GeoMatchConstraintProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class GeoMatchConstraintProperty:
        def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
            '''.. epigraph::

   This is *AWS WAF Classic* documentation.

            For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
            .. epigraph::

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            The country from which web requests originate that you want AWS WAF to search for.

            :param type: The type of geographical area you want AWS WAF to search for. Currently ``Country`` is the only valid value.
            :param value: The country that you want AWS WAF to search for.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-geomatchset-geomatchconstraint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                geo_match_constraint_property = wafregional.CfnGeoMatchSet.GeoMatchConstraintProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a676c5cd078b5dfa4974f49f50b9d6aa7460b70f5e506907e8fac2e99dbddc66)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of geographical area you want AWS WAF to search for.

            Currently ``Country`` is the only valid value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-geomatchset-geomatchconstraint.html#cfn-wafregional-geomatchset-geomatchconstraint-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The country that you want AWS WAF to search for.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-geomatchset-geomatchconstraint.html#cfn-wafregional-geomatchset-geomatchconstraint-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeoMatchConstraintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnGeoMatchSetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "geo_match_constraints": "geoMatchConstraints"},
)
class CfnGeoMatchSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        geo_match_constraints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGeoMatchSet.GeoMatchConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGeoMatchSet``.

        :param name: A friendly name or description of the ``GeoMatchSet`` . You can't change the name of an ``GeoMatchSet`` after you create it.
        :param geo_match_constraints: An array of ``GeoMatchConstraint`` objects, which contain the country that you want AWS WAF to search for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-geomatchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_geo_match_set_props = wafregional.CfnGeoMatchSetProps(
                name="name",
            
                # the properties below are optional
                geo_match_constraints=[wafregional.CfnGeoMatchSet.GeoMatchConstraintProperty(
                    type="type",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2930bdae832d48c2f5c96355eed91f2f6b508acd8a4f16714a41cb83f189e8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument geo_match_constraints", value=geo_match_constraints, expected_type=type_hints["geo_match_constraints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if geo_match_constraints is not None:
            self._values["geo_match_constraints"] = geo_match_constraints

    @builtins.property
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``GeoMatchSet`` .

        You can't change the name of an ``GeoMatchSet`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-geomatchset.html#cfn-wafregional-geomatchset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def geo_match_constraints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGeoMatchSet.GeoMatchConstraintProperty]]]]:
        '''An array of ``GeoMatchConstraint`` objects, which contain the country that you want AWS WAF to search for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-geomatchset.html#cfn-wafregional-geomatchset-geomatchconstraints
        '''
        result = self._values.get("geo_match_constraints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGeoMatchSet.GeoMatchConstraintProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGeoMatchSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnIPSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnIPSet",
):
    '''A CloudFormation ``AWS::WAFRegional::IPSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    Contains one or more IP addresses or blocks of IP addresses specified in Classless Inter-Domain Routing (CIDR) notation. AWS WAF supports IPv4 address ranges: /8 and any range between /16 through /32. AWS WAF supports IPv6 address ranges: /24, /32, /48, /56, /64, and /128.

    To specify an individual IP address, you specify the four-part IP address followed by a ``/32`` , for example, 192.0.2.0/32. To block a range of IP addresses, you can specify /8 or any range between /16 through /32 (for IPv4) or /24, /32, /48, /56, /64, or /128 (for IPv6). For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

    :cloudformationResource: AWS::WAFRegional::IPSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_iPSet = wafregional.CfnIPSet(self, "MyCfnIPSet",
            name="name",
        
            # the properties below are optional
            ip_set_descriptors=[{
                "type": "type",
                "value": "value"
            }]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        ip_set_descriptors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnIPSet.IPSetDescriptorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFRegional::IPSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A friendly name or description of the ``IPSet`` . You can't change the name of an ``IPSet`` after you create it.
        :param ip_set_descriptors: The IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR notation) that web requests originate from.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d03d2f6ba139af9fb798d1bcac74821793fbe74fbd057ea76c65a322a5ccf52a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIPSetProps(name=name, ip_set_descriptors=ip_set_descriptors)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449192ced2815a9318979c40d783cf7892acc4de56579fecc114a524ca488031)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0df8077391a72e8cb2b61e5faa5bd4501177a723f1ea75cabce60035cbbf62f5)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``IPSet`` .

        You can't change the name of an ``IPSet`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html#cfn-wafregional-ipset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beced03e839e144be568a6c708627502660180f4ede2c358f30b6252ec5459c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ipSetDescriptors")
    def ip_set_descriptors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnIPSet.IPSetDescriptorProperty"]]]]:
        '''The IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR notation) that web requests originate from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html#cfn-wafregional-ipset-ipsetdescriptors
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnIPSet.IPSetDescriptorProperty"]]]], jsii.get(self, "ipSetDescriptors"))

    @ip_set_descriptors.setter
    def ip_set_descriptors(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnIPSet.IPSetDescriptorProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2b3cd8ff2fc1d0d2ed659b518af31dc403006873bd7197b3acb904d18e3ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipSetDescriptors", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnIPSet.IPSetDescriptorProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class IPSetDescriptorProperty:
        def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
            '''.. epigraph::

   This is *AWS WAF Classic* documentation.

            For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
            .. epigraph::

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            Specifies the IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR format) that web requests originate from.

            :param type: Specify ``IPV4`` or ``IPV6`` .
            :param value: Specify an IPv4 address by using CIDR notation. For example:. - To configure AWS WAF to allow, block, or count requests that originated from the IP address 192.0.2.44, specify ``192.0.2.44/32`` . - To configure AWS WAF to allow, block, or count requests that originated from IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` . For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ . Specify an IPv6 address by using CIDR notation. For example: - To configure AWS WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` . - To configure AWS WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                i_pSet_descriptor_property = {
                    "type": "type",
                    "value": "value"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef582d725da96d9f86f721068e24efdf2cc95894cc781a63c725f254d589a6a6)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''Specify ``IPV4`` or ``IPV6`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html#cfn-wafregional-ipset-ipsetdescriptor-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''Specify an IPv4 address by using CIDR notation. For example:.

            - To configure AWS WAF to allow, block, or count requests that originated from the IP address 192.0.2.44, specify ``192.0.2.44/32`` .
            - To configure AWS WAF to allow, block, or count requests that originated from IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` .

            For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            Specify an IPv6 address by using CIDR notation. For example:

            - To configure AWS WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` .
            - To configure AWS WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html#cfn-wafregional-ipset-ipsetdescriptor-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IPSetDescriptorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnIPSetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "ip_set_descriptors": "ipSetDescriptors"},
)
class CfnIPSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        ip_set_descriptors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnIPSet.IPSetDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnIPSet``.

        :param name: A friendly name or description of the ``IPSet`` . You can't change the name of an ``IPSet`` after you create it.
        :param ip_set_descriptors: The IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR notation) that web requests originate from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_iPSet_props = wafregional.CfnIPSetProps(
                name="name",
            
                # the properties below are optional
                ip_set_descriptors=[{
                    "type": "type",
                    "value": "value"
                }]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6192ad1664f8c183bbbbc2ff82845b03d100542b22297781ca130884d2493814)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ip_set_descriptors", value=ip_set_descriptors, expected_type=type_hints["ip_set_descriptors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if ip_set_descriptors is not None:
            self._values["ip_set_descriptors"] = ip_set_descriptors

    @builtins.property
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``IPSet`` .

        You can't change the name of an ``IPSet`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html#cfn-wafregional-ipset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_set_descriptors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnIPSet.IPSetDescriptorProperty]]]]:
        '''The IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR notation) that web requests originate from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html#cfn-wafregional-ipset-ipsetdescriptors
        '''
        result = self._values.get("ip_set_descriptors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnIPSet.IPSetDescriptorProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIPSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRateBasedRule(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnRateBasedRule",
):
    '''A CloudFormation ``AWS::WAFRegional::RateBasedRule``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A ``RateBasedRule`` is identical to a regular ``Rule`` , with one addition: a ``RateBasedRule`` counts the number of requests that arrive from a specified IP address every five minutes. For example, based on recent requests that you've seen from an attacker, you might create a ``RateBasedRule`` that includes the following conditions:

    - The requests come from 192.0.2.44.
    - They contain the value ``BadBot`` in the ``User-Agent`` header.

    In the rule, you also define the rate limit as 15,000.

    Requests that meet both of these conditions and exceed 15,000 requests every five minutes trigger the rule's action (block or count), which is defined in the web ACL.

    Note you can only create rate-based rules using an AWS CloudFormation template. To add the rate-based rules created through AWS CloudFormation to a web ACL, use the AWS WAF console, API, or command line interface (CLI). For more information, see `UpdateWebACL <https://docs.aws.amazon.com/waf/latest/APIReference/API_regional_UpdateWebACL.html>`_ .

    :cloudformationResource: AWS::WAFRegional::RateBasedRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_rate_based_rule = wafregional.CfnRateBasedRule(self, "MyCfnRateBasedRule",
            metric_name="metricName",
            name="name",
            rate_key="rateKey",
            rate_limit=123,
        
            # the properties below are optional
            match_predicates=[wafregional.CfnRateBasedRule.PredicateProperty(
                data_id="dataId",
                negated=False,
                type="type"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        metric_name: builtins.str,
        name: builtins.str,
        rate_key: builtins.str,
        rate_limit: jsii.Number,
        match_predicates: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRateBasedRule.PredicateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFRegional::RateBasedRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param metric_name: A name for the metrics for a ``RateBasedRule`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change the name of the metric after you create the ``RateBasedRule`` .
        :param name: A friendly name or description for a ``RateBasedRule`` . You can't change the name of a ``RateBasedRule`` after you create it.
        :param rate_key: The field that AWS WAF uses to determine if requests are likely arriving from single source and thus subject to rate monitoring. The only valid value for ``RateKey`` is ``IP`` . ``IP`` indicates that requests arriving from the same IP address are subject to the ``RateLimit`` that is specified in the ``RateBasedRule`` .
        :param rate_limit: The maximum number of requests, which have an identical value in the field specified by the ``RateKey`` , allowed in a five-minute period. If the number of requests exceeds the ``RateLimit`` and the other predicates specified in the rule are also met, AWS WAF triggers the action that is specified for this rule.
        :param match_predicates: The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet>`` object that you want to include in a ``RateBasedRule`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11e4e3c4df513e64e6b0470810c647daacab55a0a4235d06191e0ea01045ec7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRateBasedRuleProps(
            metric_name=metric_name,
            name=name,
            rate_key=rate_key,
            rate_limit=rate_limit,
            match_predicates=match_predicates,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7441cd88c81d33b763a22c49fca6fb8a91e515944ad47b4f42f528fce74299d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26550c816cbc14ef30635b49a0e4cd170521bc605407e1e28ceab29514bf9f11)
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
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        '''A name for the metrics for a ``RateBasedRule`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change the name of the metric after you create the ``RateBasedRule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-metricname
        '''
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f32089a08f2c7f22934f00b672d2a47d23dc1d2ff0d9471c20de759247ebba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A friendly name or description for a ``RateBasedRule`` .

        You can't change the name of a ``RateBasedRule`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__677f3a83909f80bd536826c039b59c77e62f57e083383b95b1452aa04dd6c6a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="rateKey")
    def rate_key(self) -> builtins.str:
        '''The field that AWS WAF uses to determine if requests are likely arriving from single source and thus subject to rate monitoring.

        The only valid value for ``RateKey`` is ``IP`` . ``IP`` indicates that requests arriving from the same IP address are subject to the ``RateLimit`` that is specified in the ``RateBasedRule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-ratekey
        '''
        return typing.cast(builtins.str, jsii.get(self, "rateKey"))

    @rate_key.setter
    def rate_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0342491e29c52e5e2ab55abf51757852a10195255412a977e8182d52515c97f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rateKey", value)

    @builtins.property
    @jsii.member(jsii_name="rateLimit")
    def rate_limit(self) -> jsii.Number:
        '''The maximum number of requests, which have an identical value in the field specified by the ``RateKey`` , allowed in a five-minute period.

        If the number of requests exceeds the ``RateLimit`` and the other predicates specified in the rule are also met, AWS WAF triggers the action that is specified for this rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-ratelimit
        '''
        return typing.cast(jsii.Number, jsii.get(self, "rateLimit"))

    @rate_limit.setter
    def rate_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d352dbaeac84df7347442f63cc118db4d38117775ec7de43faf7946078fc495)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rateLimit", value)

    @builtins.property
    @jsii.member(jsii_name="matchPredicates")
    def match_predicates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRateBasedRule.PredicateProperty"]]]]:
        '''The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet>`` object that you want to include in a ``RateBasedRule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-matchpredicates
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRateBasedRule.PredicateProperty"]]]], jsii.get(self, "matchPredicates"))

    @match_predicates.setter
    def match_predicates(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRateBasedRule.PredicateProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f632d7e53c53a966605e2643a25ecb62dbbdc68fe7096d09f9f3d67671a52f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchPredicates", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnRateBasedRule.PredicateProperty",
        jsii_struct_bases=[],
        name_mapping={"data_id": "dataId", "negated": "negated", "type": "type"},
    )
    class PredicateProperty:
        def __init__(
            self,
            *,
            data_id: builtins.str,
            negated: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            type: builtins.str,
        ) -> None:
            '''Specifies the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , and ``SizeConstraintSet`` objects that you want to add to a ``Rule`` and, for each object, indicates whether you want to negate the settings, for example, requests that do NOT originate from the IP address 192.0.2.44.

            :param data_id: A unique identifier for a predicate in a ``Rule`` , such as ``ByteMatchSetId`` or ``IPSetId`` . The ID is returned by the corresponding ``Create`` or ``List`` command.
            :param negated: Set ``Negated`` to ``False`` if you want AWS WAF to allow, block, or count requests based on the settings in the specified ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` . For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow or block requests based on that IP address. Set ``Negated`` to ``True`` if you want AWS WAF to allow or block a request based on the negation of the settings in the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` >. For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow, block, or count requests based on all IP addresses *except* ``192.0.2.44`` .
            :param type: The type of predicate in a ``Rule`` , such as ``ByteMatch`` or ``IPSet`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ratebasedrule-predicate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                predicate_property = wafregional.CfnRateBasedRule.PredicateProperty(
                    data_id="dataId",
                    negated=False,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b06f9dc648a3e80f7a760ea5188309d45a3daea111084ebc0a40ff6ffb63d1f3)
                check_type(argname="argument data_id", value=data_id, expected_type=type_hints["data_id"])
                check_type(argname="argument negated", value=negated, expected_type=type_hints["negated"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_id": data_id,
                "negated": negated,
                "type": type,
            }

        @builtins.property
        def data_id(self) -> builtins.str:
            '''A unique identifier for a predicate in a ``Rule`` , such as ``ByteMatchSetId`` or ``IPSetId`` .

            The ID is returned by the corresponding ``Create`` or ``List`` command.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ratebasedrule-predicate.html#cfn-wafregional-ratebasedrule-predicate-dataid
            '''
            result = self._values.get("data_id")
            assert result is not None, "Required property 'data_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def negated(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Set ``Negated`` to ``False`` if you want AWS WAF to allow, block, or count requests based on the settings in the specified ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` .

            For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow or block requests based on that IP address.

            Set ``Negated`` to ``True`` if you want AWS WAF to allow or block a request based on the negation of the settings in the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` >. For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow, block, or count requests based on all IP addresses *except* ``192.0.2.44`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ratebasedrule-predicate.html#cfn-wafregional-ratebasedrule-predicate-negated
            '''
            result = self._values.get("negated")
            assert result is not None, "Required property 'negated' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of predicate in a ``Rule`` , such as ``ByteMatch`` or ``IPSet`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ratebasedrule-predicate.html#cfn-wafregional-ratebasedrule-predicate-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredicateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnRateBasedRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "name": "name",
        "rate_key": "rateKey",
        "rate_limit": "rateLimit",
        "match_predicates": "matchPredicates",
    },
)
class CfnRateBasedRuleProps:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        name: builtins.str,
        rate_key: builtins.str,
        rate_limit: jsii.Number,
        match_predicates: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRateBasedRule.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRateBasedRule``.

        :param metric_name: A name for the metrics for a ``RateBasedRule`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change the name of the metric after you create the ``RateBasedRule`` .
        :param name: A friendly name or description for a ``RateBasedRule`` . You can't change the name of a ``RateBasedRule`` after you create it.
        :param rate_key: The field that AWS WAF uses to determine if requests are likely arriving from single source and thus subject to rate monitoring. The only valid value for ``RateKey`` is ``IP`` . ``IP`` indicates that requests arriving from the same IP address are subject to the ``RateLimit`` that is specified in the ``RateBasedRule`` .
        :param rate_limit: The maximum number of requests, which have an identical value in the field specified by the ``RateKey`` , allowed in a five-minute period. If the number of requests exceeds the ``RateLimit`` and the other predicates specified in the rule are also met, AWS WAF triggers the action that is specified for this rule.
        :param match_predicates: The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet>`` object that you want to include in a ``RateBasedRule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_rate_based_rule_props = wafregional.CfnRateBasedRuleProps(
                metric_name="metricName",
                name="name",
                rate_key="rateKey",
                rate_limit=123,
            
                # the properties below are optional
                match_predicates=[wafregional.CfnRateBasedRule.PredicateProperty(
                    data_id="dataId",
                    negated=False,
                    type="type"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce09e6b2e13dded59d5cefd028df78eec7a2c8bb53d8ca7d322fb00ad668668)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rate_key", value=rate_key, expected_type=type_hints["rate_key"])
            check_type(argname="argument rate_limit", value=rate_limit, expected_type=type_hints["rate_limit"])
            check_type(argname="argument match_predicates", value=match_predicates, expected_type=type_hints["match_predicates"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "name": name,
            "rate_key": rate_key,
            "rate_limit": rate_limit,
        }
        if match_predicates is not None:
            self._values["match_predicates"] = match_predicates

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''A name for the metrics for a ``RateBasedRule`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change the name of the metric after you create the ``RateBasedRule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-metricname
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A friendly name or description for a ``RateBasedRule`` .

        You can't change the name of a ``RateBasedRule`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rate_key(self) -> builtins.str:
        '''The field that AWS WAF uses to determine if requests are likely arriving from single source and thus subject to rate monitoring.

        The only valid value for ``RateKey`` is ``IP`` . ``IP`` indicates that requests arriving from the same IP address are subject to the ``RateLimit`` that is specified in the ``RateBasedRule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-ratekey
        '''
        result = self._values.get("rate_key")
        assert result is not None, "Required property 'rate_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rate_limit(self) -> jsii.Number:
        '''The maximum number of requests, which have an identical value in the field specified by the ``RateKey`` , allowed in a five-minute period.

        If the number of requests exceeds the ``RateLimit`` and the other predicates specified in the rule are also met, AWS WAF triggers the action that is specified for this rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-ratelimit
        '''
        result = self._values.get("rate_limit")
        assert result is not None, "Required property 'rate_limit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def match_predicates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRateBasedRule.PredicateProperty]]]]:
        '''The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet>`` object that you want to include in a ``RateBasedRule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-matchpredicates
        '''
        result = self._values.get("match_predicates")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRateBasedRule.PredicateProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRateBasedRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRegexPatternSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnRegexPatternSet",
):
    '''A CloudFormation ``AWS::WAFRegional::RegexPatternSet``.

    The ``RegexPatternSet`` specifies the regular expression (regex) pattern that you want AWS WAF to search for, such as ``B[a@]dB[o0]t`` . You can then configure AWS WAF to reject those requests.

    Note that you can only create regex pattern sets using a AWS CloudFormation template. To add the regex pattern sets created through AWS CloudFormation to a RegexMatchSet, use the AWS WAF console, API, or command line interface (CLI). For more information, see `UpdateRegexMatchSet <https://docs.aws.amazon.com/waf/latest/APIReference/API_regional_UpdateRegexMatchSet.html>`_ .

    :cloudformationResource: AWS::WAFRegional::RegexPatternSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-regexpatternset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_regex_pattern_set = wafregional.CfnRegexPatternSet(self, "MyCfnRegexPatternSet",
            name="name",
            regex_pattern_strings=["regexPatternStrings"]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        regex_pattern_strings: typing.Sequence[builtins.str],
    ) -> None:
        '''Create a new ``AWS::WAFRegional::RegexPatternSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A friendly name or description of the ``RegexPatternSet`` . You can't change ``Name`` after you create a ``RegexPatternSet`` .
        :param regex_pattern_strings: Specifies the regular expression (regex) patterns that you want AWS WAF to search for, such as ``B[a@]dB[o0]t`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dfc1a5b9d56b9e911641cde7754f5413b2f02e8265319e6708bcebccf19c8ca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRegexPatternSetProps(
            name=name, regex_pattern_strings=regex_pattern_strings
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1d4177e39e952d51913d358b1050567b0b3d9aa86c3973047c0751f4154a83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ea7b66c14c7e2bede1c44979ca83790f9c714272e26091346793cfb398c2f5f)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``RegexPatternSet`` .

        You can't change ``Name`` after you create a ``RegexPatternSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-regexpatternset.html#cfn-wafregional-regexpatternset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e5613fc125ec783c548f0f16ac85d2a3b1e9aa989775da1dcf10f2b82de78f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="regexPatternStrings")
    def regex_pattern_strings(self) -> typing.List[builtins.str]:
        '''Specifies the regular expression (regex) patterns that you want AWS WAF to search for, such as ``B[a@]dB[o0]t`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-regexpatternset.html#cfn-wafregional-regexpatternset-regexpatternstrings
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regexPatternStrings"))

    @regex_pattern_strings.setter
    def regex_pattern_strings(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ac9aaae7ff1be3e42ab4832923c9f2ef4845fb5238e3250ad27eabbdb949c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regexPatternStrings", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnRegexPatternSetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "regex_pattern_strings": "regexPatternStrings"},
)
class CfnRegexPatternSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        regex_pattern_strings: typing.Sequence[builtins.str],
    ) -> None:
        '''Properties for defining a ``CfnRegexPatternSet``.

        :param name: A friendly name or description of the ``RegexPatternSet`` . You can't change ``Name`` after you create a ``RegexPatternSet`` .
        :param regex_pattern_strings: Specifies the regular expression (regex) patterns that you want AWS WAF to search for, such as ``B[a@]dB[o0]t`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-regexpatternset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_regex_pattern_set_props = wafregional.CfnRegexPatternSetProps(
                name="name",
                regex_pattern_strings=["regexPatternStrings"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab30dc578c86bb3ccf7624b362571ac79ace9375851d2bca19bfce5ce48d032)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument regex_pattern_strings", value=regex_pattern_strings, expected_type=type_hints["regex_pattern_strings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "regex_pattern_strings": regex_pattern_strings,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``RegexPatternSet`` .

        You can't change ``Name`` after you create a ``RegexPatternSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-regexpatternset.html#cfn-wafregional-regexpatternset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex_pattern_strings(self) -> typing.List[builtins.str]:
        '''Specifies the regular expression (regex) patterns that you want AWS WAF to search for, such as ``B[a@]dB[o0]t`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-regexpatternset.html#cfn-wafregional-regexpatternset-regexpatternstrings
        '''
        result = self._values.get("regex_pattern_strings")
        assert result is not None, "Required property 'regex_pattern_strings' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegexPatternSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRule(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnRule",
):
    '''A CloudFormation ``AWS::WAFRegional::Rule``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A combination of ``ByteMatchSet`` , ``IPSet`` , and/or ``SqlInjectionMatchSet`` objects that identify the web requests that you want to allow, block, or count. For example, you might create a ``Rule`` that includes the following predicates:

    - An ``IPSet`` that causes AWS WAF to search for web requests that originate from the IP address ``192.0.2.44``
    - A ``ByteMatchSet`` that causes AWS WAF to search for web requests for which the value of the ``User-Agent`` header is ``BadBot`` .

    To match the settings in this ``Rule`` , a request must originate from ``192.0.2.44`` AND include a ``User-Agent`` header for which the value is ``BadBot`` .

    :cloudformationResource: AWS::WAFRegional::Rule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_rule = wafregional.CfnRule(self, "MyCfnRule",
            metric_name="metricName",
            name="name",
        
            # the properties below are optional
            predicates=[wafregional.CfnRule.PredicateProperty(
                data_id="dataId",
                negated=False,
                type="type"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        metric_name: builtins.str,
        name: builtins.str,
        predicates: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.PredicateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFRegional::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param metric_name: A name for the metrics for this ``Rule`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``Rule`` .
        :param name: The friendly name or description for the ``Rule`` . You can't change the name of a ``Rule`` after you create it.
        :param predicates: The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet`` object that you want to include in a ``Rule`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80fa91600b63012d013cf1185c8be8867ef7463e57b756b06cc44413fa7e53bf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleProps(metric_name=metric_name, name=name, predicates=predicates)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb1810e16d3cef4160360eb521f6e8576f52b9cf2c00ea2f6ba1861f4243c3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__773a8a674451a3dc5756dfbcd7dcb0f5f0a5f2c0eb78e652c4765d8d2d5fad77)
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
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        '''A name for the metrics for this ``Rule`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-metricname
        '''
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f897467efba84f84593a2a395d866a674d8ea4843e500aab6fffad3a772e54f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The friendly name or description for the ``Rule`` .

        You can't change the name of a ``Rule`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dad97555fa6e16aaf28d9dd5cc2582a5b8e0e594abe07d6481c27b8ace0084e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="predicates")
    def predicates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.PredicateProperty"]]]]:
        '''The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet`` object that you want to include in a ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-predicates
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.PredicateProperty"]]]], jsii.get(self, "predicates"))

    @predicates.setter
    def predicates(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.PredicateProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b899e13bec4e076b8a1ab16345315e7bfc40bdfe5c38d49d635cea8f00c1fbb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predicates", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnRule.PredicateProperty",
        jsii_struct_bases=[],
        name_mapping={"data_id": "dataId", "negated": "negated", "type": "type"},
    )
    class PredicateProperty:
        def __init__(
            self,
            *,
            data_id: builtins.str,
            negated: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            type: builtins.str,
        ) -> None:
            '''Specifies the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , and ``SizeConstraintSet`` objects that you want to add to a ``Rule`` and, for each object, indicates whether you want to negate the settings, for example, requests that do NOT originate from the IP address 192.0.2.44.

            :param data_id: A unique identifier for a predicate in a ``Rule`` , such as ``ByteMatchSetId`` or ``IPSetId`` . The ID is returned by the corresponding ``Create`` or ``List`` command.
            :param negated: Set ``Negated`` to ``False`` if you want AWS WAF to allow, block, or count requests based on the settings in the specified ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` . For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow or block requests based on that IP address. Set ``Negated`` to ``True`` if you want AWS WAF to allow or block a request based on the negation of the settings in the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` . For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow, block, or count requests based on all IP addresses *except* ``192.0.2.44`` .
            :param type: The type of predicate in a ``Rule`` , such as ``ByteMatch`` or ``IPSet`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                predicate_property = wafregional.CfnRule.PredicateProperty(
                    data_id="dataId",
                    negated=False,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd1f309db5d7c5126c7a8cfaece9c629cfab2061be0c3a1ee6b287e4c0afc961)
                check_type(argname="argument data_id", value=data_id, expected_type=type_hints["data_id"])
                check_type(argname="argument negated", value=negated, expected_type=type_hints["negated"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_id": data_id,
                "negated": negated,
                "type": type,
            }

        @builtins.property
        def data_id(self) -> builtins.str:
            '''A unique identifier for a predicate in a ``Rule`` , such as ``ByteMatchSetId`` or ``IPSetId`` .

            The ID is returned by the corresponding ``Create`` or ``List`` command.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html#cfn-wafregional-rule-predicate-dataid
            '''
            result = self._values.get("data_id")
            assert result is not None, "Required property 'data_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def negated(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Set ``Negated`` to ``False`` if you want AWS WAF to allow, block, or count requests based on the settings in the specified ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` .

            For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow or block requests based on that IP address.

            Set ``Negated`` to ``True`` if you want AWS WAF to allow or block a request based on the negation of the settings in the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` . For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow, block, or count requests based on all IP addresses *except* ``192.0.2.44`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html#cfn-wafregional-rule-predicate-negated
            '''
            result = self._values.get("negated")
            assert result is not None, "Required property 'negated' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of predicate in a ``Rule`` , such as ``ByteMatch`` or ``IPSet`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html#cfn-wafregional-rule-predicate-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredicateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "name": "name",
        "predicates": "predicates",
    },
)
class CfnRuleProps:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        name: builtins.str,
        predicates: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRule``.

        :param metric_name: A name for the metrics for this ``Rule`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``Rule`` .
        :param name: The friendly name or description for the ``Rule`` . You can't change the name of a ``Rule`` after you create it.
        :param predicates: The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet`` object that you want to include in a ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_rule_props = wafregional.CfnRuleProps(
                metric_name="metricName",
                name="name",
            
                # the properties below are optional
                predicates=[wafregional.CfnRule.PredicateProperty(
                    data_id="dataId",
                    negated=False,
                    type="type"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b9daa2800ba7434c2ae734fd3bdd9273603fefdd3aaa332e67d84e548c74cc)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument predicates", value=predicates, expected_type=type_hints["predicates"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "name": name,
        }
        if predicates is not None:
            self._values["predicates"] = predicates

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''A name for the metrics for this ``Rule`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-metricname
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The friendly name or description for the ``Rule`` .

        You can't change the name of a ``Rule`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def predicates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.PredicateProperty]]]]:
        '''The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet`` object that you want to include in a ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-predicates
        '''
        result = self._values.get("predicates")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.PredicateProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSizeConstraintSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnSizeConstraintSet",
):
    '''A CloudFormation ``AWS::WAFRegional::SizeConstraintSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A complex type that contains ``SizeConstraint`` objects, which specify the parts of web requests that you want AWS WAF to inspect the size of. If a ``SizeConstraintSet`` contains more than one ``SizeConstraint`` object, a request only needs to match one constraint to be considered a match.

    :cloudformationResource: AWS::WAFRegional::SizeConstraintSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_size_constraint_set = wafregional.CfnSizeConstraintSet(self, "MyCfnSizeConstraintSet",
            name="name",
        
            # the properties below are optional
            size_constraints=[wafregional.CfnSizeConstraintSet.SizeConstraintProperty(
                comparison_operator="comparisonOperator",
                field_to_match=wafregional.CfnSizeConstraintSet.FieldToMatchProperty(
                    type="type",
        
                    # the properties below are optional
                    data="data"
                ),
                size=123,
                text_transformation="textTransformation"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        size_constraints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSizeConstraintSet.SizeConstraintProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFRegional::SizeConstraintSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name, if any, of the ``SizeConstraintSet`` .
        :param size_constraints: The size constraint and the part of the web request to check.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72777156691cf4f340deeac3ce3fa2ddb4f33c5903d99ef70cf7fd5a4434a4ab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSizeConstraintSetProps(name=name, size_constraints=size_constraints)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d956df208e94a979bb0b3d40c7e5f84cadcbaa8a9f393fb24faae04c4455930)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b940af892d36ca1b4bdc79673864bb0ca423e1bd083521ee65316784e3956d19)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name, if any, of the ``SizeConstraintSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html#cfn-wafregional-sizeconstraintset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf8d8a26bdbfe0ac67855ecd3f8af80ea054c1cc018e93136a007798e5f34ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sizeConstraints")
    def size_constraints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSizeConstraintSet.SizeConstraintProperty"]]]]:
        '''The size constraint and the part of the web request to check.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html#cfn-wafregional-sizeconstraintset-sizeconstraints
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSizeConstraintSet.SizeConstraintProperty"]]]], jsii.get(self, "sizeConstraints"))

    @size_constraints.setter
    def size_constraints(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSizeConstraintSet.SizeConstraintProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7375e7cbfbe6d05fb709221650a42c3328fd8184ec831b0fd7a6be6af4e57565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeConstraints", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnSizeConstraintSet.FieldToMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "data": "data"},
    )
    class FieldToMatchProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform. - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .
            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                field_to_match_property = wafregional.CfnSizeConstraintSet.FieldToMatchProperty(
                    type="type",
                
                    # the properties below are optional
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__688c51984174abe796f4020050d3b48c5f0d682115fedb981a7036bcb26d0ccc)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if data is not None:
                self._values["data"] = data

        @builtins.property
        def type(self) -> builtins.str:
            '''The part of the web request that you want AWS WAF to search for a specified string.

            Parts of a request that you can search include the following:

            - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` .
            - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform.
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-fieldtomatch.html#cfn-wafregional-sizeconstraintset-fieldtomatch-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` .

            The name of the header is not case sensitive.

            When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive.

            If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-fieldtomatch.html#cfn-wafregional-sizeconstraintset-fieldtomatch-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldToMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnSizeConstraintSet.SizeConstraintProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "field_to_match": "fieldToMatch",
            "size": "size",
            "text_transformation": "textTransformation",
        },
    )
    class SizeConstraintProperty:
        def __init__(
            self,
            *,
            comparison_operator: builtins.str,
            field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSizeConstraintSet.FieldToMatchProperty", typing.Dict[builtins.str, typing.Any]]],
            size: jsii.Number,
            text_transformation: builtins.str,
        ) -> None:
            '''.. epigraph::

   This is *AWS WAF Classic* documentation.

            For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
            .. epigraph::

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            Specifies a constraint on the size of a part of the web request. AWS WAF uses the ``Size`` , ``ComparisonOperator`` , and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match.

            :param comparison_operator: The type of comparison you want AWS WAF to perform. AWS WAF uses this in combination with the provided ``Size`` and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match. *EQ* : Used to test if the ``Size`` is equal to the size of the ``FieldToMatch`` *NE* : Used to test if the ``Size`` is not equal to the size of the ``FieldToMatch`` *LE* : Used to test if the ``Size`` is less than or equal to the size of the ``FieldToMatch`` *LT* : Used to test if the ``Size`` is strictly less than the size of the ``FieldToMatch`` *GE* : Used to test if the ``Size`` is greater than or equal to the size of the ``FieldToMatch`` *GT* : Used to test if the ``Size`` is strictly greater than the size of the ``FieldToMatch``
            :param field_to_match: The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.
            :param size: The size in bytes that you want AWS WAF to compare against the size of the specified ``FieldToMatch`` . AWS WAF uses this in combination with ``ComparisonOperator`` and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match. Valid values for size are 0 - 21474836480 bytes (0 - 20 GB). If you specify ``URI`` for the value of ``Type`` , the / in the URI path that you specify counts as one character. For example, the URI ``/logo.jpg`` is nine characters long.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting a request for a match. You can only specify a single type of TextTransformation. Note that if you choose ``BODY`` for the value of ``Type`` , you must choose ``NONE`` for ``TextTransformation`` because the API Gateway API or Application Load Balancer forward only the first 8192 bytes for inspection. *NONE* Specify ``NONE`` if you don't want to perform any text transformations. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                size_constraint_property = wafregional.CfnSizeConstraintSet.SizeConstraintProperty(
                    comparison_operator="comparisonOperator",
                    field_to_match=wafregional.CfnSizeConstraintSet.FieldToMatchProperty(
                        type="type",
                
                        # the properties below are optional
                        data="data"
                    ),
                    size=123,
                    text_transformation="textTransformation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a23e47f0d15253341b2104c2702af713a996f3390769f48da4c833ef556fc712)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument field_to_match", value=field_to_match, expected_type=type_hints["field_to_match"])
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                check_type(argname="argument text_transformation", value=text_transformation, expected_type=type_hints["text_transformation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "comparison_operator": comparison_operator,
                "field_to_match": field_to_match,
                "size": size,
                "text_transformation": text_transformation,
            }

        @builtins.property
        def comparison_operator(self) -> builtins.str:
            '''The type of comparison you want AWS WAF to perform.

            AWS WAF uses this in combination with the provided ``Size`` and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match.

            *EQ* : Used to test if the ``Size`` is equal to the size of the ``FieldToMatch``

            *NE* : Used to test if the ``Size`` is not equal to the size of the ``FieldToMatch``

            *LE* : Used to test if the ``Size`` is less than or equal to the size of the ``FieldToMatch``

            *LT* : Used to test if the ``Size`` is strictly less than the size of the ``FieldToMatch``

            *GE* : Used to test if the ``Size`` is greater than or equal to the size of the ``FieldToMatch``

            *GT* : Used to test if the ``Size`` is strictly greater than the size of the ``FieldToMatch``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            assert result is not None, "Required property 'comparison_operator' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSizeConstraintSet.FieldToMatchProperty"]:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSizeConstraintSet.FieldToMatchProperty"], result)

        @builtins.property
        def size(self) -> jsii.Number:
            '''The size in bytes that you want AWS WAF to compare against the size of the specified ``FieldToMatch`` .

            AWS WAF uses this in combination with ``ComparisonOperator`` and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match.

            Valid values for size are 0 - 21474836480 bytes (0 - 20 GB).

            If you specify ``URI`` for the value of ``Type`` , the / in the URI path that you specify counts as one character. For example, the URI ``/logo.jpg`` is nine characters long.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-size
            '''
            result = self._values.get("size")
            assert result is not None, "Required property 'size' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def text_transformation(self) -> builtins.str:
            '''Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF .

            If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting a request for a match.

            You can only specify a single type of TextTransformation.

            Note that if you choose ``BODY`` for the value of ``Type`` , you must choose ``NONE`` for ``TextTransformation`` because the API Gateway API or Application Load Balancer forward only the first 8192 bytes for inspection.

            *NONE*

            Specify ``NONE`` if you don't want to perform any text transformations.

            *CMD_LINE*

            When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations:

            - Delete the following characters: \\ " ' ^
            - Delete spaces before the following characters: / (
            - Replace the following characters with a space: , ;
            - Replace multiple spaces with one space
            - Convert uppercase letters (A-Z) to lowercase (a-z)

            *COMPRESS_WHITE_SPACE*

            Use this option to replace the following characters with a space character (decimal 32):

            - \\f, formfeed, decimal 12
            - \\t, tab, decimal 9
            - \\n, newline, decimal 10
            - \\r, carriage return, decimal 13
            - \\v, vertical tab, decimal 11
            - non-breaking space, decimal 160

            ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.

            *HTML_ENTITY_DECODE*

            Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations:

            - Replaces ``(ampersand)quot;`` with ``"``
            - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
            - Replaces ``(ampersand)lt;`` with a "less than" symbol
            - Replaces ``(ampersand)gt;`` with ``>``
            - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters
            - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters

            *LOWERCASE*

            Use this option to convert uppercase letters (A-Z) to lowercase (a-z).

            *URL_DECODE*

            Use this option to decode a URL-encoded value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-texttransformation
            '''
            result = self._values.get("text_transformation")
            assert result is not None, "Required property 'text_transformation' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SizeConstraintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnSizeConstraintSetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "size_constraints": "sizeConstraints"},
)
class CfnSizeConstraintSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        size_constraints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSizeConstraintSet.SizeConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSizeConstraintSet``.

        :param name: The name, if any, of the ``SizeConstraintSet`` .
        :param size_constraints: The size constraint and the part of the web request to check.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_size_constraint_set_props = wafregional.CfnSizeConstraintSetProps(
                name="name",
            
                # the properties below are optional
                size_constraints=[wafregional.CfnSizeConstraintSet.SizeConstraintProperty(
                    comparison_operator="comparisonOperator",
                    field_to_match=wafregional.CfnSizeConstraintSet.FieldToMatchProperty(
                        type="type",
            
                        # the properties below are optional
                        data="data"
                    ),
                    size=123,
                    text_transformation="textTransformation"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08f3afa4a29f0c9b7f506838b52615dc29c46478bb59a201dce0b195ac5371d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument size_constraints", value=size_constraints, expected_type=type_hints["size_constraints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if size_constraints is not None:
            self._values["size_constraints"] = size_constraints

    @builtins.property
    def name(self) -> builtins.str:
        '''The name, if any, of the ``SizeConstraintSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html#cfn-wafregional-sizeconstraintset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size_constraints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSizeConstraintSet.SizeConstraintProperty]]]]:
        '''The size constraint and the part of the web request to check.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html#cfn-wafregional-sizeconstraintset-sizeconstraints
        '''
        result = self._values.get("size_constraints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSizeConstraintSet.SizeConstraintProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSizeConstraintSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSqlInjectionMatchSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnSqlInjectionMatchSet",
):
    '''A CloudFormation ``AWS::WAFRegional::SqlInjectionMatchSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A complex type that contains ``SqlInjectionMatchTuple`` objects, which specify the parts of web requests that you want AWS WAF to inspect for snippets of malicious SQL code and, if you want AWS WAF to inspect a header, the name of the header. If a ``SqlInjectionMatchSet`` contains more than one ``SqlInjectionMatchTuple`` object, a request needs to include snippets of SQL code in only one of the specified parts of the request to be considered a match.

    :cloudformationResource: AWS::WAFRegional::SqlInjectionMatchSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_sql_injection_match_set = wafregional.CfnSqlInjectionMatchSet(self, "MyCfnSqlInjectionMatchSet",
            name="name",
        
            # the properties below are optional
            sql_injection_match_tuples=[wafregional.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty(
                field_to_match=wafregional.CfnSqlInjectionMatchSet.FieldToMatchProperty(
                    type="type",
        
                    # the properties below are optional
                    data="data"
                ),
                text_transformation="textTransformation"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        sql_injection_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFRegional::SqlInjectionMatchSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name, if any, of the ``SqlInjectionMatchSet`` .
        :param sql_injection_match_tuples: Specifies the parts of web requests that you want to inspect for snippets of malicious SQL code.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfcb23690f9464dd62a02338d0a176cf18ed28c464e6aa1c9495b045d10da80)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSqlInjectionMatchSetProps(
            name=name, sql_injection_match_tuples=sql_injection_match_tuples
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d59d90288ee4ec4b3b80011a74e9065f26d739a0ece63cd2e8c7fe42106841b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fc62c4a92cb3ed26f01c8b4fb2b95b53d39bffdfe49d505eaf2cb49ac520e58)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name, if any, of the ``SqlInjectionMatchSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html#cfn-wafregional-sqlinjectionmatchset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f67200cb192695b10f2b43d51e1f17cc5b7573320e99555a3e574f5e14b93be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sqlInjectionMatchTuples")
    def sql_injection_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]]:
        '''Specifies the parts of web requests that you want to inspect for snippets of malicious SQL code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html#cfn-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuples
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]], jsii.get(self, "sqlInjectionMatchTuples"))

    @sql_injection_match_tuples.setter
    def sql_injection_match_tuples(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c152430dddcecdd29473fa78506ec32b29d63dfbe95cf0a3ef9006367c7727e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlInjectionMatchTuples", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnSqlInjectionMatchSet.FieldToMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "data": "data"},
    )
    class FieldToMatchProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform. - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .
            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                field_to_match_property = wafregional.CfnSqlInjectionMatchSet.FieldToMatchProperty(
                    type="type",
                
                    # the properties below are optional
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb01189a5dabd7a285cab5f7e392511f8595adbe8a2d2f2c613404610a0da792)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if data is not None:
                self._values["data"] = data

        @builtins.property
        def type(self) -> builtins.str:
            '''The part of the web request that you want AWS WAF to search for a specified string.

            Parts of a request that you can search include the following:

            - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` .
            - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform.
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-fieldtomatch.html#cfn-wafregional-sqlinjectionmatchset-fieldtomatch-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` .

            The name of the header is not case sensitive.

            When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive.

            If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-fieldtomatch.html#cfn-wafregional-sqlinjectionmatchset-fieldtomatch-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldToMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "text_transformation": "textTransformation",
        },
    )
    class SqlInjectionMatchTupleProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSqlInjectionMatchSet.FieldToMatchProperty", typing.Dict[builtins.str, typing.Any]]],
            text_transformation: builtins.str,
        ) -> None:
            '''.. epigraph::

   This is *AWS WAF Classic* documentation.

            For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
            .. epigraph::

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            Specifies the part of a web request that you want AWS WAF to inspect for snippets of malicious SQL code and, if you want AWS WAF to inspect a header, the name of the header.

            :param field_to_match: The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match. You can only specify a single type of TextTransformation. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value. *NONE* Specify ``NONE`` if you don't want to perform any text transformations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                sql_injection_match_tuple_property = wafregional.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty(
                    field_to_match=wafregional.CfnSqlInjectionMatchSet.FieldToMatchProperty(
                        type="type",
                
                        # the properties below are optional
                        data="data"
                    ),
                    text_transformation="textTransformation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b8ad44e2a3f3083094c88a9604c54635eec345c904ffdbafac08da0467424f2)
                check_type(argname="argument field_to_match", value=field_to_match, expected_type=type_hints["field_to_match"])
                check_type(argname="argument text_transformation", value=text_transformation, expected_type=type_hints["text_transformation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "field_to_match": field_to_match,
                "text_transformation": text_transformation,
            }

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSqlInjectionMatchSet.FieldToMatchProperty"]:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple.html#cfn-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSqlInjectionMatchSet.FieldToMatchProperty"], result)

        @builtins.property
        def text_transformation(self) -> builtins.str:
            '''Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF .

            If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match.

            You can only specify a single type of TextTransformation.

            *CMD_LINE*

            When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations:

            - Delete the following characters: \\ " ' ^
            - Delete spaces before the following characters: / (
            - Replace the following characters with a space: , ;
            - Replace multiple spaces with one space
            - Convert uppercase letters (A-Z) to lowercase (a-z)

            *COMPRESS_WHITE_SPACE*

            Use this option to replace the following characters with a space character (decimal 32):

            - \\f, formfeed, decimal 12
            - \\t, tab, decimal 9
            - \\n, newline, decimal 10
            - \\r, carriage return, decimal 13
            - \\v, vertical tab, decimal 11
            - non-breaking space, decimal 160

            ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.

            *HTML_ENTITY_DECODE*

            Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations:

            - Replaces ``(ampersand)quot;`` with ``"``
            - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
            - Replaces ``(ampersand)lt;`` with a "less than" symbol
            - Replaces ``(ampersand)gt;`` with ``>``
            - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters
            - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters

            *LOWERCASE*

            Use this option to convert uppercase letters (A-Z) to lowercase (a-z).

            *URL_DECODE*

            Use this option to decode a URL-encoded value.

            *NONE*

            Specify ``NONE`` if you don't want to perform any text transformations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple.html#cfn-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple-texttransformation
            '''
            result = self._values.get("text_transformation")
            assert result is not None, "Required property 'text_transformation' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqlInjectionMatchTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnSqlInjectionMatchSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sql_injection_match_tuples": "sqlInjectionMatchTuples",
    },
)
class CfnSqlInjectionMatchSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        sql_injection_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSqlInjectionMatchSet``.

        :param name: The name, if any, of the ``SqlInjectionMatchSet`` .
        :param sql_injection_match_tuples: Specifies the parts of web requests that you want to inspect for snippets of malicious SQL code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_sql_injection_match_set_props = wafregional.CfnSqlInjectionMatchSetProps(
                name="name",
            
                # the properties below are optional
                sql_injection_match_tuples=[wafregional.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty(
                    field_to_match=wafregional.CfnSqlInjectionMatchSet.FieldToMatchProperty(
                        type="type",
            
                        # the properties below are optional
                        data="data"
                    ),
                    text_transformation="textTransformation"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14edc69e5fdd10fdfa15ecd98953d6c0891c073a8e6e9a023182d83373b37dd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql_injection_match_tuples", value=sql_injection_match_tuples, expected_type=type_hints["sql_injection_match_tuples"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if sql_injection_match_tuples is not None:
            self._values["sql_injection_match_tuples"] = sql_injection_match_tuples

    @builtins.property
    def name(self) -> builtins.str:
        '''The name, if any, of the ``SqlInjectionMatchSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html#cfn-wafregional-sqlinjectionmatchset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_injection_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty]]]]:
        '''Specifies the parts of web requests that you want to inspect for snippets of malicious SQL code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html#cfn-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuples
        '''
        result = self._values.get("sql_injection_match_tuples")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSqlInjectionMatchSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnWebACL(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnWebACL",
):
    '''A CloudFormation ``AWS::WAFRegional::WebACL``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    Contains the ``Rules`` that identify the requests that you want to allow, block, or count. In a ``WebACL`` , you also specify a default action ( ``ALLOW`` or ``BLOCK`` ), and the action for each ``Rule`` that you add to a ``WebACL`` , for example, block requests from specified IP addresses or block requests from specified referrers. If you add more than one ``Rule`` to a ``WebACL`` , a request needs to match only one of the specifications to be allowed, blocked, or counted.

    To identify the requests that you want AWS WAF to filter, you associate the ``WebACL`` with an API Gateway API or an Application Load Balancer.

    :cloudformationResource: AWS::WAFRegional::WebACL
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_web_aCL = wafregional.CfnWebACL(self, "MyCfnWebACL",
            default_action=wafregional.CfnWebACL.ActionProperty(
                type="type"
            ),
            metric_name="metricName",
            name="name",
        
            # the properties below are optional
            rules=[wafregional.CfnWebACL.RuleProperty(
                action=wafregional.CfnWebACL.ActionProperty(
                    type="type"
                ),
                priority=123,
                rule_id="ruleId"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWebACL.ActionProperty", typing.Dict[builtins.str, typing.Any]]],
        metric_name: builtins.str,
        name: builtins.str,
        rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWebACL.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFRegional::WebACL``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_action: The action to perform if none of the ``Rules`` contained in the ``WebACL`` match. The action is specified by the ``WafAction`` object.
        :param metric_name: A name for the metrics for this ``WebACL`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``WebACL`` .
        :param name: A friendly name or description of the ``WebACL`` . You can't change the name of a ``WebACL`` after you create it.
        :param rules: An array that contains the action for each ``Rule`` in a ``WebACL`` , the priority of the ``Rule`` , and the ID of the ``Rule`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ebbb44fd103694e243ed17ee24dfd41fbe6f61eb3289d0a618d4af02f1fdc8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWebACLProps(
            default_action=default_action,
            metric_name=metric_name,
            name=name,
            rules=rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e797498b1d594d4b52f9301d6a6c4b75083e2b07442a6300ff2762df59996e90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed0948cd4630e9c7b195900979f774907535974af8c969ee68177bb8965ecb06)
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
    @jsii.member(jsii_name="defaultAction")
    def default_action(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.ActionProperty"]:
        '''The action to perform if none of the ``Rules`` contained in the ``WebACL`` match.

        The action is specified by the ``WafAction`` object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-defaultaction
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.ActionProperty"], jsii.get(self, "defaultAction"))

    @default_action.setter
    def default_action(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.ActionProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b50e87cdc75c02801bc1832711c991e655ae1977073bd5e3c09ebce62344e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAction", value)

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        '''A name for the metrics for this ``WebACL`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``WebACL`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-metricname
        '''
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053b0bb61c8edd972ab5101804261ec4d2df7af05dd95eee6ca924ff5ce15a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``WebACL`` .

        You can't change the name of a ``WebACL`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b400e18cc837ddba6f7307041520ec3c0f70bc0b1bc413ef747675f5ccca5e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.RuleProperty"]]]]:
        '''An array that contains the action for each ``Rule`` in a ``WebACL`` , the priority of the ``Rule`` , and the ID of the ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-rules
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.RuleProperty"]]]], jsii.get(self, "rules"))

    @rules.setter
    def rules(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.RuleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1453c4b4d341b1b4e6a01c5b6204c8d1da6eae00fc13c7f7cc4a945722b4043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rules", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnWebACL.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class ActionProperty:
        def __init__(self, *, type: builtins.str) -> None:
            '''Specifies the action AWS WAF takes when a web request matches or doesn't match all rule conditions.

            :param type: For actions that are associated with a rule, the action that AWS WAF takes when a web request matches all conditions in a rule. For the default action of a web access control list (ACL), the action that AWS WAF takes when a web request doesn't match all conditions in any rule. Valid settings include the following: - ``ALLOW`` : AWS WAF allows requests - ``BLOCK`` : AWS WAF blocks requests - ``COUNT`` : AWS WAF increments a counter of the requests that match all of the conditions in the rule. AWS WAF then continues to inspect the web request based on the remaining rules in the web ACL. You can't specify ``COUNT`` for the default action for a WebACL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                action_property = wafregional.CfnWebACL.ActionProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9c142f4b96f0b1d2db46ab8fbb90bef15a293b474f36ecf650af96195be672c)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''For actions that are associated with a rule, the action that AWS WAF takes when a web request matches all conditions in a rule.

            For the default action of a web access control list (ACL), the action that AWS WAF takes when a web request doesn't match all conditions in any rule.

            Valid settings include the following:

            - ``ALLOW`` : AWS WAF allows requests
            - ``BLOCK`` : AWS WAF blocks requests
            - ``COUNT`` : AWS WAF increments a counter of the requests that match all of the conditions in the rule. AWS WAF then continues to inspect the web request based on the remaining rules in the web ACL. You can't specify ``COUNT`` for the default action for a WebACL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-action.html#cfn-wafregional-webacl-action-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnWebACL.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "priority": "priority", "rule_id": "ruleId"},
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWebACL.ActionProperty", typing.Dict[builtins.str, typing.Any]]],
            priority: jsii.Number,
            rule_id: builtins.str,
        ) -> None:
            '''A combination of ``ByteMatchSet`` , ``IPSet`` , and/or ``SqlInjectionMatchSet`` objects that identify the web requests that you want to allow, block, or count.

            For example, you might create a ``Rule`` that includes the following predicates:

            - An ``IPSet`` that causes AWS WAF to search for web requests that originate from the IP address ``192.0.2.44``
            - A ``ByteMatchSet`` that causes AWS WAF to search for web requests for which the value of the ``User-Agent`` header is ``BadBot`` .

            To match the settings in this ``Rule`` , a request must originate from ``192.0.2.44`` AND include a ``User-Agent`` header for which the value is ``BadBot`` .

            :param action: The action that AWS WAF takes when a web request matches all conditions in the rule, such as allow, block, or count the request.
            :param priority: The order in which AWS WAF evaluates the rules in a web ACL. AWS WAF evaluates rules with a lower value before rules with a higher value. The value must be a unique integer. If you have multiple rules in a web ACL, the priority numbers do not need to be consecutive.
            :param rule_id: The ID of an AWS WAF Regional rule to associate with a web ACL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                rule_property = wafregional.CfnWebACL.RuleProperty(
                    action=wafregional.CfnWebACL.ActionProperty(
                        type="type"
                    ),
                    priority=123,
                    rule_id="ruleId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__847acd2ec59fb19e9a6253ba05d3113d154b887a07ad7e419996f55275f2e5ba)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action": action,
                "priority": priority,
                "rule_id": rule_id,
            }

        @builtins.property
        def action(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.ActionProperty"]:
            '''The action that AWS WAF takes when a web request matches all conditions in the rule, such as allow, block, or count the request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html#cfn-wafregional-webacl-rule-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.ActionProperty"], result)

        @builtins.property
        def priority(self) -> jsii.Number:
            '''The order in which AWS WAF evaluates the rules in a web ACL.

            AWS WAF evaluates rules with a lower value before rules with a higher value. The value must be a unique integer. If you have multiple rules in a web ACL, the priority numbers do not need to be consecutive.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html#cfn-wafregional-webacl-rule-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def rule_id(self) -> builtins.str:
            '''The ID of an AWS WAF Regional rule to associate with a web ACL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html#cfn-wafregional-webacl-rule-ruleid
            '''
            result = self._values.get("rule_id")
            assert result is not None, "Required property 'rule_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnWebACLAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnWebACLAssociation",
):
    '''A CloudFormation ``AWS::WAFRegional::WebACLAssociation``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    The AWS::WAFRegional::WebACLAssociation resource associates an AWS WAF Regional web access control group (ACL) with a resource.

    :cloudformationResource: AWS::WAFRegional::WebACLAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_web_aCLAssociation = wafregional.CfnWebACLAssociation(self, "MyCfnWebACLAssociation",
            resource_arn="resourceArn",
            web_acl_id="webAclId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        resource_arn: builtins.str,
        web_acl_id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::WAFRegional::WebACLAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_arn: The Amazon Resource Name (ARN) of the resource to protect with the web ACL.
        :param web_acl_id: A unique identifier (ID) for the web ACL.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e961102c74e9b1a4d5f873562bb09811065215110b8954b7d7a7ace1d16693f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWebACLAssociationProps(
            resource_arn=resource_arn, web_acl_id=web_acl_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551714c77391a2a75ae46d10c42f3f9608ecf5304929a3ad09cb4a04c38efebb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a89b42eae92fe75f74beb15aa8804b887bd23746fd3827da42ea0a2a46c9fe53)
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
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the resource to protect with the web ACL.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html#cfn-wafregional-webaclassociation-resourcearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6526381fb7f5e0d1ff10d553317bab69a4e8cc614c9ff84060eb1c469f325def)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="webAclId")
    def web_acl_id(self) -> builtins.str:
        '''A unique identifier (ID) for the web ACL.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html#cfn-wafregional-webaclassociation-webaclid
        '''
        return typing.cast(builtins.str, jsii.get(self, "webAclId"))

    @web_acl_id.setter
    def web_acl_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed1975b0701c0645f3abcd469b739c066ea1100e3f35aa9875e491b73bdbaa96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webAclId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnWebACLAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "web_acl_id": "webAclId"},
)
class CfnWebACLAssociationProps:
    def __init__(self, *, resource_arn: builtins.str, web_acl_id: builtins.str) -> None:
        '''Properties for defining a ``CfnWebACLAssociation``.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource to protect with the web ACL.
        :param web_acl_id: A unique identifier (ID) for the web ACL.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_web_aCLAssociation_props = wafregional.CfnWebACLAssociationProps(
                resource_arn="resourceArn",
                web_acl_id="webAclId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c9d2a46c7dc88a3ad1e1440295c6b6d59ef58157404bdef96c69763a9b5f85)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument web_acl_id", value=web_acl_id, expected_type=type_hints["web_acl_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "web_acl_id": web_acl_id,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the resource to protect with the web ACL.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html#cfn-wafregional-webaclassociation-resourcearn
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def web_acl_id(self) -> builtins.str:
        '''A unique identifier (ID) for the web ACL.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html#cfn-wafregional-webaclassociation-webaclid
        '''
        result = self._values.get("web_acl_id")
        assert result is not None, "Required property 'web_acl_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebACLAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnWebACLProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_action": "defaultAction",
        "metric_name": "metricName",
        "name": "name",
        "rules": "rules",
    },
)
class CfnWebACLProps:
    def __init__(
        self,
        *,
        default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.ActionProperty, typing.Dict[builtins.str, typing.Any]]],
        metric_name: builtins.str,
        name: builtins.str,
        rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWebACL``.

        :param default_action: The action to perform if none of the ``Rules`` contained in the ``WebACL`` match. The action is specified by the ``WafAction`` object.
        :param metric_name: A name for the metrics for this ``WebACL`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``WebACL`` .
        :param name: A friendly name or description of the ``WebACL`` . You can't change the name of a ``WebACL`` after you create it.
        :param rules: An array that contains the action for each ``Rule`` in a ``WebACL`` , the priority of the ``Rule`` , and the ID of the ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_web_aCLProps = wafregional.CfnWebACLProps(
                default_action=wafregional.CfnWebACL.ActionProperty(
                    type="type"
                ),
                metric_name="metricName",
                name="name",
            
                # the properties below are optional
                rules=[wafregional.CfnWebACL.RuleProperty(
                    action=wafregional.CfnWebACL.ActionProperty(
                        type="type"
                    ),
                    priority=123,
                    rule_id="ruleId"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e745feb18dfc89f8837bb3f048de20c6c564b7daca6d2dcec056c0b14ae0bfcf)
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_action": default_action,
            "metric_name": metric_name,
            "name": name,
        }
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def default_action(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.ActionProperty]:
        '''The action to perform if none of the ``Rules`` contained in the ``WebACL`` match.

        The action is specified by the ``WafAction`` object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-defaultaction
        '''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.ActionProperty], result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''A name for the metrics for this ``WebACL`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``WebACL`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-metricname
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``WebACL`` .

        You can't change the name of a ``WebACL`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.RuleProperty]]]]:
        '''An array that contains the action for each ``Rule`` in a ``WebACL`` , the priority of the ``Rule`` , and the ID of the ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.RuleProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebACLProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnXssMatchSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wafregional.CfnXssMatchSet",
):
    '''A CloudFormation ``AWS::WAFRegional::XssMatchSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A complex type that contains ``XssMatchTuple`` objects, which specify the parts of web requests that you want AWS WAF to inspect for cross-site scripting attacks and, if you want AWS WAF to inspect a header, the name of the header. If a ``XssMatchSet`` contains more than one ``XssMatchTuple`` object, a request needs to include cross-site scripting attacks in only one of the specified parts of the request to be considered a match.

    :cloudformationResource: AWS::WAFRegional::XssMatchSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wafregional as wafregional
        
        cfn_xss_match_set = wafregional.CfnXssMatchSet(self, "MyCfnXssMatchSet",
            name="name",
        
            # the properties below are optional
            xss_match_tuples=[wafregional.CfnXssMatchSet.XssMatchTupleProperty(
                field_to_match=wafregional.CfnXssMatchSet.FieldToMatchProperty(
                    type="type",
        
                    # the properties below are optional
                    data="data"
                ),
                text_transformation="textTransformation"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        xss_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnXssMatchSet.XssMatchTupleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFRegional::XssMatchSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name, if any, of the ``XssMatchSet`` .
        :param xss_match_tuples: Specifies the parts of web requests that you want to inspect for cross-site scripting attacks.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca96bae6fa51e14a1eea881647e8be6c0f2eb715af115cbcb71576594befcb7b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnXssMatchSetProps(name=name, xss_match_tuples=xss_match_tuples)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26316e22b9a33d4b73bb405199d8fea5955c209c275ec31976928c06db14386)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68a12f0ae012054279e1b6001af5d08562797e445ef9606a425e5737f33f548f)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name, if any, of the ``XssMatchSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html#cfn-wafregional-xssmatchset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ac7c3c407c5b1ee3167b1111aee43a9bb2d8c3adf641cd9aefc5f47a66a6e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="xssMatchTuples")
    def xss_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnXssMatchSet.XssMatchTupleProperty"]]]]:
        '''Specifies the parts of web requests that you want to inspect for cross-site scripting attacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html#cfn-wafregional-xssmatchset-xssmatchtuples
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnXssMatchSet.XssMatchTupleProperty"]]]], jsii.get(self, "xssMatchTuples"))

    @xss_match_tuples.setter
    def xss_match_tuples(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnXssMatchSet.XssMatchTupleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fae8b859b102bd4390b077a67635a79726cee5054f60a22352fcba4e5986098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xssMatchTuples", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnXssMatchSet.FieldToMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "data": "data"},
    )
    class FieldToMatchProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform. - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .
            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                field_to_match_property = wafregional.CfnXssMatchSet.FieldToMatchProperty(
                    type="type",
                
                    # the properties below are optional
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e07e6a4bf82d1cdb8dc5d3476b69e9f0c201f11912677350b0aef35676e9958)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if data is not None:
                self._values["data"] = data

        @builtins.property
        def type(self) -> builtins.str:
            '''The part of the web request that you want AWS WAF to search for a specified string.

            Parts of a request that you can search include the following:

            - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` .
            - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform.
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-fieldtomatch.html#cfn-wafregional-xssmatchset-fieldtomatch-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` .

            The name of the header is not case sensitive.

            When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive.

            If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-fieldtomatch.html#cfn-wafregional-xssmatchset-fieldtomatch-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldToMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wafregional.CfnXssMatchSet.XssMatchTupleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "text_transformation": "textTransformation",
        },
    )
    class XssMatchTupleProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnXssMatchSet.FieldToMatchProperty", typing.Dict[builtins.str, typing.Any]]],
            text_transformation: builtins.str,
        ) -> None:
            '''.. epigraph::

   This is *AWS WAF Classic* documentation.

            For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
            .. epigraph::

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            Specifies the part of a web request that you want AWS WAF to inspect for cross-site scripting attacks and, if you want AWS WAF to inspect a header, the name of the header.

            :param field_to_match: The part of a web request that you want AWS WAF to inspect, such as a specified header or a query string.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match. You can only specify a single type of TextTransformation. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value. *NONE* Specify ``NONE`` if you don't want to perform any text transformations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-xssmatchtuple.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wafregional as wafregional
                
                xss_match_tuple_property = wafregional.CfnXssMatchSet.XssMatchTupleProperty(
                    field_to_match=wafregional.CfnXssMatchSet.FieldToMatchProperty(
                        type="type",
                
                        # the properties below are optional
                        data="data"
                    ),
                    text_transformation="textTransformation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a88c7cc9bc1ac64f3db396799bf8a6df4e422c2d9419320e118f1470311bc3fc)
                check_type(argname="argument field_to_match", value=field_to_match, expected_type=type_hints["field_to_match"])
                check_type(argname="argument text_transformation", value=text_transformation, expected_type=type_hints["text_transformation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "field_to_match": field_to_match,
                "text_transformation": text_transformation,
            }

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnXssMatchSet.FieldToMatchProperty"]:
            '''The part of a web request that you want AWS WAF to inspect, such as a specified header or a query string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-xssmatchtuple.html#cfn-wafregional-xssmatchset-xssmatchtuple-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnXssMatchSet.FieldToMatchProperty"], result)

        @builtins.property
        def text_transformation(self) -> builtins.str:
            '''Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF .

            If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match.

            You can only specify a single type of TextTransformation.

            *CMD_LINE*

            When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations:

            - Delete the following characters: \\ " ' ^
            - Delete spaces before the following characters: / (
            - Replace the following characters with a space: , ;
            - Replace multiple spaces with one space
            - Convert uppercase letters (A-Z) to lowercase (a-z)

            *COMPRESS_WHITE_SPACE*

            Use this option to replace the following characters with a space character (decimal 32):

            - \\f, formfeed, decimal 12
            - \\t, tab, decimal 9
            - \\n, newline, decimal 10
            - \\r, carriage return, decimal 13
            - \\v, vertical tab, decimal 11
            - non-breaking space, decimal 160

            ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.

            *HTML_ENTITY_DECODE*

            Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations:

            - Replaces ``(ampersand)quot;`` with ``"``
            - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
            - Replaces ``(ampersand)lt;`` with a "less than" symbol
            - Replaces ``(ampersand)gt;`` with ``>``
            - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters
            - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters

            *LOWERCASE*

            Use this option to convert uppercase letters (A-Z) to lowercase (a-z).

            *URL_DECODE*

            Use this option to decode a URL-encoded value.

            *NONE*

            Specify ``NONE`` if you don't want to perform any text transformations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-xssmatchtuple.html#cfn-wafregional-xssmatchset-xssmatchtuple-texttransformation
            '''
            result = self._values.get("text_transformation")
            assert result is not None, "Required property 'text_transformation' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "XssMatchTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wafregional.CfnXssMatchSetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "xss_match_tuples": "xssMatchTuples"},
)
class CfnXssMatchSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        xss_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnXssMatchSet.XssMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnXssMatchSet``.

        :param name: The name, if any, of the ``XssMatchSet`` .
        :param xss_match_tuples: Specifies the parts of web requests that you want to inspect for cross-site scripting attacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wafregional as wafregional
            
            cfn_xss_match_set_props = wafregional.CfnXssMatchSetProps(
                name="name",
            
                # the properties below are optional
                xss_match_tuples=[wafregional.CfnXssMatchSet.XssMatchTupleProperty(
                    field_to_match=wafregional.CfnXssMatchSet.FieldToMatchProperty(
                        type="type",
            
                        # the properties below are optional
                        data="data"
                    ),
                    text_transformation="textTransformation"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35c0a5e31cd619ab40592756e324338f296c894b379858fa7a93d9baabfb55f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument xss_match_tuples", value=xss_match_tuples, expected_type=type_hints["xss_match_tuples"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if xss_match_tuples is not None:
            self._values["xss_match_tuples"] = xss_match_tuples

    @builtins.property
    def name(self) -> builtins.str:
        '''The name, if any, of the ``XssMatchSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html#cfn-wafregional-xssmatchset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def xss_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnXssMatchSet.XssMatchTupleProperty]]]]:
        '''Specifies the parts of web requests that you want to inspect for cross-site scripting attacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html#cfn-wafregional-xssmatchset-xssmatchtuples
        '''
        result = self._values.get("xss_match_tuples")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnXssMatchSet.XssMatchTupleProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnXssMatchSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnByteMatchSet",
    "CfnByteMatchSetProps",
    "CfnGeoMatchSet",
    "CfnGeoMatchSetProps",
    "CfnIPSet",
    "CfnIPSetProps",
    "CfnRateBasedRule",
    "CfnRateBasedRuleProps",
    "CfnRegexPatternSet",
    "CfnRegexPatternSetProps",
    "CfnRule",
    "CfnRuleProps",
    "CfnSizeConstraintSet",
    "CfnSizeConstraintSetProps",
    "CfnSqlInjectionMatchSet",
    "CfnSqlInjectionMatchSetProps",
    "CfnWebACL",
    "CfnWebACLAssociation",
    "CfnWebACLAssociationProps",
    "CfnWebACLProps",
    "CfnXssMatchSet",
    "CfnXssMatchSetProps",
]

publication.publish()

def _typecheckingstub__fae63cbf467e3ff3e3c6b8d6b285887e2ae652922cc71eb7bb59b95c5a6b70e0(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    byte_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnByteMatchSet.ByteMatchTupleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ddfa33dac211ba0ee7aac4b5f6fe5024ad7a31d28b1f8f34e4447ffbde95b7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6536db848f978e45ac33a419a2125733d829f99bcf122ef89ec97e96818db20(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b98ec0fc5a55e39713b858a083753ff59459356a819f2f8e539943a9de8f5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239b1ba1fe61fa61bb32db6f9d716e237a345858d28adab98b570ca6fa5f6cd6(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnByteMatchSet.ByteMatchTupleProperty, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7bad6b0c549eae06757b16d2a78b0845d31d285d02641273a99b0f74275dbe8(
    *,
    field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnByteMatchSet.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]],
    positional_constraint: builtins.str,
    text_transformation: builtins.str,
    target_string: typing.Optional[builtins.str] = None,
    target_string_base64: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64319f6759e7e4aa082a4633fb674506f7ba1fbcf59a86bea959524adf45e094(
    *,
    type: builtins.str,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0265e2ffb25f4ad7e97879144a3f2b05ac3dd8a050b6f29f6438f73a25a21c75(
    *,
    name: builtins.str,
    byte_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnByteMatchSet.ByteMatchTupleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a389e753656373661a818bda860db59cfc521d153e0491ad0b00254cfda620(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    geo_match_constraints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGeoMatchSet.GeoMatchConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4242f7c2138da06e509eea43351baa3840c7e190be8fda2bc558a42215fde0a0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1104a1b28dc16c72fc1b3154f9da5448083280ae7c9415516ff91a10884952d4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cad14f14431a0dacfba5259ae0250322b372acfc7da24285f123cc4825d249(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba89c7c1672048011be38d0b8f438c767dbb3ad33d065e63e755f4de0c157342(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGeoMatchSet.GeoMatchConstraintProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a676c5cd078b5dfa4974f49f50b9d6aa7460b70f5e506907e8fac2e99dbddc66(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2930bdae832d48c2f5c96355eed91f2f6b508acd8a4f16714a41cb83f189e8(
    *,
    name: builtins.str,
    geo_match_constraints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGeoMatchSet.GeoMatchConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03d2f6ba139af9fb798d1bcac74821793fbe74fbd057ea76c65a322a5ccf52a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    ip_set_descriptors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnIPSet.IPSetDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449192ced2815a9318979c40d783cf7892acc4de56579fecc114a524ca488031(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df8077391a72e8cb2b61e5faa5bd4501177a723f1ea75cabce60035cbbf62f5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beced03e839e144be568a6c708627502660180f4ede2c358f30b6252ec5459c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2b3cd8ff2fc1d0d2ed659b518af31dc403006873bd7197b3acb904d18e3ba5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnIPSet.IPSetDescriptorProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef582d725da96d9f86f721068e24efdf2cc95894cc781a63c725f254d589a6a6(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6192ad1664f8c183bbbbc2ff82845b03d100542b22297781ca130884d2493814(
    *,
    name: builtins.str,
    ip_set_descriptors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnIPSet.IPSetDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11e4e3c4df513e64e6b0470810c647daacab55a0a4235d06191e0ea01045ec7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    metric_name: builtins.str,
    name: builtins.str,
    rate_key: builtins.str,
    rate_limit: jsii.Number,
    match_predicates: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRateBasedRule.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7441cd88c81d33b763a22c49fca6fb8a91e515944ad47b4f42f528fce74299d4(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26550c816cbc14ef30635b49a0e4cd170521bc605407e1e28ceab29514bf9f11(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f32089a08f2c7f22934f00b672d2a47d23dc1d2ff0d9471c20de759247ebba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677f3a83909f80bd536826c039b59c77e62f57e083383b95b1452aa04dd6c6a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0342491e29c52e5e2ab55abf51757852a10195255412a977e8182d52515c97f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d352dbaeac84df7347442f63cc118db4d38117775ec7de43faf7946078fc495(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f632d7e53c53a966605e2643a25ecb62dbbdc68fe7096d09f9f3d67671a52f17(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRateBasedRule.PredicateProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06f9dc648a3e80f7a760ea5188309d45a3daea111084ebc0a40ff6ffb63d1f3(
    *,
    data_id: builtins.str,
    negated: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce09e6b2e13dded59d5cefd028df78eec7a2c8bb53d8ca7d322fb00ad668668(
    *,
    metric_name: builtins.str,
    name: builtins.str,
    rate_key: builtins.str,
    rate_limit: jsii.Number,
    match_predicates: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRateBasedRule.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dfc1a5b9d56b9e911641cde7754f5413b2f02e8265319e6708bcebccf19c8ca(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    regex_pattern_strings: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1d4177e39e952d51913d358b1050567b0b3d9aa86c3973047c0751f4154a83(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea7b66c14c7e2bede1c44979ca83790f9c714272e26091346793cfb398c2f5f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e5613fc125ec783c548f0f16ac85d2a3b1e9aa989775da1dcf10f2b82de78f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ac9aaae7ff1be3e42ab4832923c9f2ef4845fb5238e3250ad27eabbdb949c4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab30dc578c86bb3ccf7624b362571ac79ace9375851d2bca19bfce5ce48d032(
    *,
    name: builtins.str,
    regex_pattern_strings: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fa91600b63012d013cf1185c8be8867ef7463e57b756b06cc44413fa7e53bf(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    metric_name: builtins.str,
    name: builtins.str,
    predicates: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb1810e16d3cef4160360eb521f6e8576f52b9cf2c00ea2f6ba1861f4243c3d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773a8a674451a3dc5756dfbcd7dcb0f5f0a5f2c0eb78e652c4765d8d2d5fad77(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f897467efba84f84593a2a395d866a674d8ea4843e500aab6fffad3a772e54f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dad97555fa6e16aaf28d9dd5cc2582a5b8e0e594abe07d6481c27b8ace0084e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b899e13bec4e076b8a1ab16345315e7bfc40bdfe5c38d49d635cea8f00c1fbb0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.PredicateProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1f309db5d7c5126c7a8cfaece9c629cfab2061be0c3a1ee6b287e4c0afc961(
    *,
    data_id: builtins.str,
    negated: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b9daa2800ba7434c2ae734fd3bdd9273603fefdd3aaa332e67d84e548c74cc(
    *,
    metric_name: builtins.str,
    name: builtins.str,
    predicates: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72777156691cf4f340deeac3ce3fa2ddb4f33c5903d99ef70cf7fd5a4434a4ab(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    size_constraints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSizeConstraintSet.SizeConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d956df208e94a979bb0b3d40c7e5f84cadcbaa8a9f393fb24faae04c4455930(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b940af892d36ca1b4bdc79673864bb0ca423e1bd083521ee65316784e3956d19(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf8d8a26bdbfe0ac67855ecd3f8af80ea054c1cc018e93136a007798e5f34ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7375e7cbfbe6d05fb709221650a42c3328fd8184ec831b0fd7a6be6af4e57565(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSizeConstraintSet.SizeConstraintProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688c51984174abe796f4020050d3b48c5f0d682115fedb981a7036bcb26d0ccc(
    *,
    type: builtins.str,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23e47f0d15253341b2104c2702af713a996f3390769f48da4c833ef556fc712(
    *,
    comparison_operator: builtins.str,
    field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSizeConstraintSet.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]],
    size: jsii.Number,
    text_transformation: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08f3afa4a29f0c9b7f506838b52615dc29c46478bb59a201dce0b195ac5371d(
    *,
    name: builtins.str,
    size_constraints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSizeConstraintSet.SizeConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfcb23690f9464dd62a02338d0a176cf18ed28c464e6aa1c9495b045d10da80(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    sql_injection_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d59d90288ee4ec4b3b80011a74e9065f26d739a0ece63cd2e8c7fe42106841b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc62c4a92cb3ed26f01c8b4fb2b95b53d39bffdfe49d505eaf2cb49ac520e58(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f67200cb192695b10f2b43d51e1f17cc5b7573320e99555a3e574f5e14b93be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c152430dddcecdd29473fa78506ec32b29d63dfbe95cf0a3ef9006367c7727e4(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb01189a5dabd7a285cab5f7e392511f8595adbe8a2d2f2c613404610a0da792(
    *,
    type: builtins.str,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8ad44e2a3f3083094c88a9604c54635eec345c904ffdbafac08da0467424f2(
    *,
    field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSqlInjectionMatchSet.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]],
    text_transformation: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14edc69e5fdd10fdfa15ecd98953d6c0891c073a8e6e9a023182d83373b37dd(
    *,
    name: builtins.str,
    sql_injection_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ebbb44fd103694e243ed17ee24dfd41fbe6f61eb3289d0a618d4af02f1fdc8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.ActionProperty, typing.Dict[builtins.str, typing.Any]]],
    metric_name: builtins.str,
    name: builtins.str,
    rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e797498b1d594d4b52f9301d6a6c4b75083e2b07442a6300ff2762df59996e90(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0948cd4630e9c7b195900979f774907535974af8c969ee68177bb8965ecb06(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b50e87cdc75c02801bc1832711c991e655ae1977073bd5e3c09ebce62344e1(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.ActionProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053b0bb61c8edd972ab5101804261ec4d2df7af05dd95eee6ca924ff5ce15a9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b400e18cc837ddba6f7307041520ec3c0f70bc0b1bc413ef747675f5ccca5e79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1453c4b4d341b1b4e6a01c5b6204c8d1da6eae00fc13c7f7cc4a945722b4043(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.RuleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c142f4b96f0b1d2db46ab8fbb90bef15a293b474f36ecf650af96195be672c(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847acd2ec59fb19e9a6253ba05d3113d154b887a07ad7e419996f55275f2e5ba(
    *,
    action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.ActionProperty, typing.Dict[builtins.str, typing.Any]]],
    priority: jsii.Number,
    rule_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e961102c74e9b1a4d5f873562bb09811065215110b8954b7d7a7ace1d16693f6(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    resource_arn: builtins.str,
    web_acl_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551714c77391a2a75ae46d10c42f3f9608ecf5304929a3ad09cb4a04c38efebb(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89b42eae92fe75f74beb15aa8804b887bd23746fd3827da42ea0a2a46c9fe53(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6526381fb7f5e0d1ff10d553317bab69a4e8cc614c9ff84060eb1c469f325def(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1975b0701c0645f3abcd469b739c066ea1100e3f35aa9875e491b73bdbaa96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c9d2a46c7dc88a3ad1e1440295c6b6d59ef58157404bdef96c69763a9b5f85(
    *,
    resource_arn: builtins.str,
    web_acl_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e745feb18dfc89f8837bb3f048de20c6c564b7daca6d2dcec056c0b14ae0bfcf(
    *,
    default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.ActionProperty, typing.Dict[builtins.str, typing.Any]]],
    metric_name: builtins.str,
    name: builtins.str,
    rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca96bae6fa51e14a1eea881647e8be6c0f2eb715af115cbcb71576594befcb7b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    xss_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnXssMatchSet.XssMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26316e22b9a33d4b73bb405199d8fea5955c209c275ec31976928c06db14386(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a12f0ae012054279e1b6001af5d08562797e445ef9606a425e5737f33f548f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ac7c3c407c5b1ee3167b1111aee43a9bb2d8c3adf641cd9aefc5f47a66a6e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fae8b859b102bd4390b077a67635a79726cee5054f60a22352fcba4e5986098(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnXssMatchSet.XssMatchTupleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e07e6a4bf82d1cdb8dc5d3476b69e9f0c201f11912677350b0aef35676e9958(
    *,
    type: builtins.str,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88c7cc9bc1ac64f3db396799bf8a6df4e422c2d9419320e118f1470311bc3fc(
    *,
    field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnXssMatchSet.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]],
    text_transformation: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35c0a5e31cd619ab40592756e324338f296c894b379858fa7a93d9baabfb55f(
    *,
    name: builtins.str,
    xss_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnXssMatchSet.XssMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
