'''
# AWS Web Application Firewall Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_waf as waf
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for WAF construct libraries](https://constructs.dev/search?q=waf)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::WAF resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WAF.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::WAF](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_WAF.html).

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
    jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet",
):
    '''A CloudFormation ``AWS::WAF::ByteMatchSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    The ``AWS::WAF::ByteMatchSet`` resource creates an AWS WAF ``ByteMatchSet`` that identifies a part of a web request that you want to inspect.

    :cloudformationResource: AWS::WAF::ByteMatchSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_waf as waf
        
        cfn_byte_match_set = waf.CfnByteMatchSet(self, "MyCfnByteMatchSet",
            name="name",
        
            # the properties below are optional
            byte_match_tuples=[waf.CfnByteMatchSet.ByteMatchTupleProperty(
                field_to_match=waf.CfnByteMatchSet.FieldToMatchProperty(
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
        '''Create a new ``AWS::WAF::ByteMatchSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the ``ByteMatchSet`` . You can't change ``Name`` after you create a ``ByteMatchSet`` .
        :param byte_match_tuples: Specifies the bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff9b621c9d700b26114e8c55d0581f1cd76eacc1249303b31e31dd17db2539f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72bb9f6e07c45ae311ef3b6b169fd3b107c61898ac1d850ab84732260cbbc34a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e66199391c07d8f80703f2a29874c52c3853b1bfaadca0889b574a3a50491b3)
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
        '''The name of the ``ByteMatchSet`` .

        You can't change ``Name`` after you create a ``ByteMatchSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html#cfn-waf-bytematchset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af8e56453fe3265390c7d6b6602958908f01dfa188d8ade928fe233ab5a67d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="byteMatchTuples")
    def byte_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnByteMatchSet.ByteMatchTupleProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''Specifies the bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html#cfn-waf-bytematchset-bytematchtuples
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnByteMatchSet.ByteMatchTupleProperty", _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "byteMatchTuples"))

    @byte_match_tuples.setter
    def byte_match_tuples(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnByteMatchSet.ByteMatchTupleProperty", _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348cffb9e6f600bfa21c699986a7d73c8b8d99db580b50c0c2b59818a19c646a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "byteMatchTuples", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet.ByteMatchTupleProperty",
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

            :param field_to_match: The part of a web request that you want to inspect, such as a specified header or a query string.
            :param positional_constraint: Within the portion of a web request that you want to search (for example, in the query string, if any), specify where you want AWS WAF to search. Valid values include the following: *CONTAINS* The specified part of the web request must include the value of ``TargetString`` , but the location doesn't matter. *CONTAINS_WORD* The specified part of the web request must include the value of ``TargetString`` , and ``TargetString`` must contain only alphanumeric characters or underscore (A-Z, a-z, 0-9, or _). In addition, ``TargetString`` must be a word, which means one of the following: - ``TargetString`` exactly matches the value of the specified part of the web request, such as the value of a header. - ``TargetString`` is at the beginning of the specified part of the web request and is followed by a character other than an alphanumeric character or underscore (_), for example, ``BadBot;`` . - ``TargetString`` is at the end of the specified part of the web request and is preceded by a character other than an alphanumeric character or underscore (_), for example, ``;BadBot`` . - ``TargetString`` is in the middle of the specified part of the web request and is preceded and followed by characters other than alphanumeric characters or underscore (_), for example, ``-BadBot;`` . *EXACTLY* The value of the specified part of the web request must exactly match the value of ``TargetString`` . *STARTS_WITH* The value of ``TargetString`` must appear at the beginning of the specified part of the web request. *ENDS_WITH* The value of ``TargetString`` must appear at the end of the specified part of the web request.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match. You can only specify a single type of TextTransformation. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value. *NONE* Specify ``NONE`` if you don't want to perform any text transformations.
            :param target_string: The value that you want AWS WAF to search for. AWS WAF searches for the specified string in the part of web requests that you specified in ``FieldToMatch`` . The maximum length of the value is 50 bytes. You must specify this property or the ``TargetStringBase64`` property. Valid values depend on the values that you specified for ``FieldToMatch`` : - ``HEADER`` : The value that you want AWS WAF to search for in the request header that you specified in ``FieldToMatch`` , for example, the value of the ``User-Agent`` or ``Referer`` header. - ``METHOD`` : The HTTP method, which indicates the type of operation specified in the request. Amazon CloudFront supports the following methods: ``DELETE`` , ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PATCH`` , ``POST`` , and ``PUT`` . - ``QUERY_STRING`` : The value that you want AWS WAF to search for in the query string, which is the part of a URL that appears after a ``?`` character. - ``URI`` : The value that you want AWS WAF to search for in the part of a URL that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but instead of inspecting a single parameter, AWS WAF inspects all parameters within the query string for the value or regex pattern that you specify in ``TargetString`` . If ``TargetString`` includes alphabetic characters A-Z and a-z, note that the value is case sensitive.
            :param target_string_base64: The base64-encoded value that AWS WAF searches for. AWS CloudFormation sends this value to AWS WAF without encoding it. You must specify this property or the ``TargetString`` property. AWS WAF searches for this value in a specific part of web requests, which you define in the ``FieldToMatch`` property. Valid values depend on the Type value in the ``FieldToMatch`` property. For example, for a ``METHOD`` type, you must specify HTTP methods such as ``DELETE, GET, HEAD, OPTIONS, PATCH, POST`` , and ``PUT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                byte_match_tuple_property = waf.CfnByteMatchSet.ByteMatchTupleProperty(
                    field_to_match=waf.CfnByteMatchSet.FieldToMatchProperty(
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
                type_hints = typing.get_type_hints(_typecheckingstub__f615c50ac397240ef456ec57d22a117fb5dd4ce9f467f2fbb4c7505da21ad231)
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
            '''The part of a web request that you want to inspect, such as a specified header or a query string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-fieldtomatch
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-positionalconstraint
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-texttransformation
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
            - ``METHOD`` : The HTTP method, which indicates the type of operation specified in the request. Amazon CloudFront supports the following methods: ``DELETE`` , ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PATCH`` , ``POST`` , and ``PUT`` .
            - ``QUERY_STRING`` : The value that you want AWS WAF to search for in the query string, which is the part of a URL that appears after a ``?`` character.
            - ``URI`` : The value that you want AWS WAF to search for in the part of a URL that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but instead of inspecting a single parameter, AWS WAF inspects all parameters within the query string for the value or regex pattern that you specify in ``TargetString`` .

            If ``TargetString`` includes alphabetic characters A-Z and a-z, note that the value is case sensitive.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-targetstring
            '''
            result = self._values.get("target_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_string_base64(self) -> typing.Optional[builtins.str]:
            '''The base64-encoded value that AWS WAF searches for. AWS CloudFormation sends this value to AWS WAF without encoding it.

            You must specify this property or the ``TargetString`` property.

            AWS WAF searches for this value in a specific part of web requests, which you define in the ``FieldToMatch`` property.

            Valid values depend on the Type value in the ``FieldToMatch`` property. For example, for a ``METHOD`` type, you must specify HTTP methods such as ``DELETE, GET, HEAD, OPTIONS, PATCH, POST`` , and ``PUT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples.html#cfn-waf-bytematchset-bytematchtuples-targetstringbase64
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
        jsii_type="@aws-cdk/aws-waf.CfnByteMatchSet.FieldToMatchProperty",
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

            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform. Amazon CloudFront supports the following methods: ``DELETE`` , ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PATCH`` , ``POST`` , and ``PUT`` . - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .
            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                field_to_match_property = waf.CfnByteMatchSet.FieldToMatchProperty(
                    type="type",
                
                    # the properties below are optional
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7154ed71c4602041a72374ffe2cdddaeb12fdee7198ece0e9a31f9e6b81364b6)
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
            - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform. Amazon CloudFront supports the following methods: ``DELETE`` , ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PATCH`` , ``POST`` , and ``PUT`` .
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-bytematchset-bytematchtuples-fieldtomatch-type
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-bytematchset-bytematchtuples-fieldtomatch-data
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
    jsii_type="@aws-cdk/aws-waf.CfnByteMatchSetProps",
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

        :param name: The name of the ``ByteMatchSet`` . You can't change ``Name`` after you create a ``ByteMatchSet`` .
        :param byte_match_tuples: Specifies the bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_waf as waf
            
            cfn_byte_match_set_props = waf.CfnByteMatchSetProps(
                name="name",
            
                # the properties below are optional
                byte_match_tuples=[waf.CfnByteMatchSet.ByteMatchTupleProperty(
                    field_to_match=waf.CfnByteMatchSet.FieldToMatchProperty(
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
            type_hints = typing.get_type_hints(_typecheckingstub__161a568cd4770d077eec7193fc874c37b11e9b443a016bc48adb91e333c0dfd8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument byte_match_tuples", value=byte_match_tuples, expected_type=type_hints["byte_match_tuples"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if byte_match_tuples is not None:
            self._values["byte_match_tuples"] = byte_match_tuples

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the ``ByteMatchSet`` .

        You can't change ``Name`` after you create a ``ByteMatchSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html#cfn-waf-bytematchset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def byte_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnByteMatchSet.ByteMatchTupleProperty, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''Specifies the bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-bytematchset.html#cfn-waf-bytematchset-bytematchtuples
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
class CfnIPSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-waf.CfnIPSet",
):
    '''A CloudFormation ``AWS::WAF::IPSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    Contains one or more IP addresses or blocks of IP addresses specified in Classless Inter-Domain Routing (CIDR) notation. AWS WAF supports IPv4 address ranges: /8 and any range between /16 through /32. AWS WAF supports IPv6 address ranges: /24, /32, /48, /56, /64, and /128.

    To specify an individual IP address, you specify the four-part IP address followed by a ``/32`` , for example, 192.0.2.0/32. To block a range of IP addresses, you can specify /8 or any range between /16 through /32 (for IPv4) or /24, /32, /48, /56, /64, or /128 (for IPv6). For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

    :cloudformationResource: AWS::WAF::IPSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_waf as waf
        
        cfn_iPSet = waf.CfnIPSet(self, "MyCfnIPSet",
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
        '''Create a new ``AWS::WAF::IPSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the ``IPSet`` . You can't change the name of an ``IPSet`` after you create it.
        :param ip_set_descriptors: The IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR notation) that web requests originate from. If the ``WebACL`` is associated with an Amazon CloudFront distribution and the viewer did not use an HTTP proxy or a load balancer to send the request, this is the value of the c-ip field in the CloudFront access logs.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32a18f7210ce113d1a9998808c0f823422883df8bb594280868228baaf96a79b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0baa80babbfc753aaf0aa673d59d0f192e26ac2f3f9d732d700e1fbc611990c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af8517257e3821d6c22634b1d2be1de36d3498e904ec723c2fcff6e34a2fbcda)
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
        '''The name of the ``IPSet`` .

        You can't change the name of an ``IPSet`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html#cfn-waf-ipset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d9a43b65a96f08b3dd2f8a42a8df8570b842dd64dd5de746eb9e1c0efa6f6bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ipSetDescriptors")
    def ip_set_descriptors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnIPSet.IPSetDescriptorProperty"]]]]:
        '''The IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR notation) that web requests originate from.

        If the ``WebACL`` is associated with an Amazon CloudFront distribution and the viewer did not use an HTTP proxy or a load balancer to send the request, this is the value of the c-ip field in the CloudFront access logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html#cfn-waf-ipset-ipsetdescriptors
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnIPSet.IPSetDescriptorProperty"]]]], jsii.get(self, "ipSetDescriptors"))

    @ip_set_descriptors.setter
    def ip_set_descriptors(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnIPSet.IPSetDescriptorProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e6fd9a88419dcbc3facedb7b94efc69bb5da47f9baa0d81f5894707823c6e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipSetDescriptors", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-waf.CfnIPSet.IPSetDescriptorProperty",
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                i_pSet_descriptor_property = {
                    "type": "type",
                    "value": "value"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ba6ca3f8f4aa5131b6c0790ac408d836c80789c4f394c5e81460cf6c0b7d993)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''Specify ``IPV4`` or ``IPV6`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html#cfn-waf-ipset-ipsetdescriptors-type
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-ipset-ipsetdescriptors.html#cfn-waf-ipset-ipsetdescriptors-value
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
    jsii_type="@aws-cdk/aws-waf.CfnIPSetProps",
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

        :param name: The name of the ``IPSet`` . You can't change the name of an ``IPSet`` after you create it.
        :param ip_set_descriptors: The IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR notation) that web requests originate from. If the ``WebACL`` is associated with an Amazon CloudFront distribution and the viewer did not use an HTTP proxy or a load balancer to send the request, this is the value of the c-ip field in the CloudFront access logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_waf as waf
            
            cfn_iPSet_props = waf.CfnIPSetProps(
                name="name",
            
                # the properties below are optional
                ip_set_descriptors=[{
                    "type": "type",
                    "value": "value"
                }]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e065c4f1d20f561df3d5b0a1f965eb1f514b36b90716f3552ccdb678c5c47633)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ip_set_descriptors", value=ip_set_descriptors, expected_type=type_hints["ip_set_descriptors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if ip_set_descriptors is not None:
            self._values["ip_set_descriptors"] = ip_set_descriptors

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the ``IPSet`` .

        You can't change the name of an ``IPSet`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html#cfn-waf-ipset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_set_descriptors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnIPSet.IPSetDescriptorProperty]]]]:
        '''The IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR notation) that web requests originate from.

        If the ``WebACL`` is associated with an Amazon CloudFront distribution and the viewer did not use an HTTP proxy or a load balancer to send the request, this is the value of the c-ip field in the CloudFront access logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-ipset.html#cfn-waf-ipset-ipsetdescriptors
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
class CfnRule(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-waf.CfnRule",
):
    '''A CloudFormation ``AWS::WAF::Rule``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A combination of ``ByteMatchSet`` , ``IPSet`` , and/or ``SqlInjectionMatchSet`` objects that identify the web requests that you want to allow, block, or count. For example, you might create a ``Rule`` that includes the following predicates:

    - An ``IPSet`` that causes AWS WAF to search for web requests that originate from the IP address ``192.0.2.44``
    - A ``ByteMatchSet`` that causes AWS WAF to search for web requests for which the value of the ``User-Agent`` header is ``BadBot`` .

    To match the settings in this ``Rule`` , a request must originate from ``192.0.2.44`` AND include a ``User-Agent`` header for which the value is ``BadBot`` .

    :cloudformationResource: AWS::WAF::Rule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_waf as waf
        
        cfn_rule = waf.CfnRule(self, "MyCfnRule",
            metric_name="metricName",
            name="name",
        
            # the properties below are optional
            predicates=[waf.CfnRule.PredicateProperty(
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
        '''Create a new ``AWS::WAF::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param metric_name: The name of the metrics for this ``Rule`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``Rule`` .
        :param name: The friendly name or description for the ``Rule`` . You can't change the name of a ``Rule`` after you create it.
        :param predicates: The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet`` object that you want to include in a ``Rule`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc688a3bad3463713a45885f1ba83433a2095417b718020cd1ff230ec90d8a93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__951d7a0c98eeeacd730f20f48b5fe9075aebc2ed59c702337c2ed750338305d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a10a59480b8152726ced54dc9994021cf03808e7227a2e3155a974440ec09026)
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
        '''The name of the metrics for this ``Rule`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-metricname
        '''
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a2ea8b9bf30c2fafbc436d932d38f548323961d7600f1442dee7cc7f4313f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The friendly name or description for the ``Rule`` .

        You can't change the name of a ``Rule`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cbc0b30c2bf6d75b6e6c94961415b195f6c9f06811433b6d54af58e745273fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="predicates")
    def predicates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.PredicateProperty"]]]]:
        '''The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet`` object that you want to include in a ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-predicates
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.PredicateProperty"]]]], jsii.get(self, "predicates"))

    @predicates.setter
    def predicates(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.PredicateProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba9da071001acadeba37fb8db736489bf6c9b8b0fcb2c2ad52f8f08cfef8979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predicates", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-waf.CfnRule.PredicateProperty",
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                predicate_property = waf.CfnRule.PredicateProperty(
                    data_id="dataId",
                    negated=False,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc224fa84c648f83adf2fb1ea06c7c955934d2638323d4d6385d9ba62dc7ae68)
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html#cfn-waf-rule-predicates-dataid
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html#cfn-waf-rule-predicates-negated
            '''
            result = self._values.get("negated")
            assert result is not None, "Required property 'negated' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of predicate in a ``Rule`` , such as ``ByteMatch`` or ``IPSet`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-rule-predicates.html#cfn-waf-rule-predicates-type
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
    jsii_type="@aws-cdk/aws-waf.CfnRuleProps",
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

        :param metric_name: The name of the metrics for this ``Rule`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``Rule`` .
        :param name: The friendly name or description for the ``Rule`` . You can't change the name of a ``Rule`` after you create it.
        :param predicates: The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet`` object that you want to include in a ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_waf as waf
            
            cfn_rule_props = waf.CfnRuleProps(
                metric_name="metricName",
                name="name",
            
                # the properties below are optional
                predicates=[waf.CfnRule.PredicateProperty(
                    data_id="dataId",
                    negated=False,
                    type="type"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3711652825bb89ed61fd78f18c78cc978a8c9d8075ed61feb475ca12519842)
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
        '''The name of the metrics for this ``Rule`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-metricname
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The friendly name or description for the ``Rule`` .

        You can't change the name of a ``Rule`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def predicates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.PredicateProperty]]]]:
        '''The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet`` object that you want to include in a ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-rule.html#cfn-waf-rule-predicates
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
    jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet",
):
    '''A CloudFormation ``AWS::WAF::SizeConstraintSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A complex type that contains ``SizeConstraint`` objects, which specify the parts of web requests that you want AWS WAF to inspect the size of. If a ``SizeConstraintSet`` contains more than one ``SizeConstraint`` object, a request only needs to match one constraint to be considered a match.

    :cloudformationResource: AWS::WAF::SizeConstraintSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_waf as waf
        
        cfn_size_constraint_set = waf.CfnSizeConstraintSet(self, "MyCfnSizeConstraintSet",
            name="name",
            size_constraints=[waf.CfnSizeConstraintSet.SizeConstraintProperty(
                comparison_operator="comparisonOperator",
                field_to_match=waf.CfnSizeConstraintSet.FieldToMatchProperty(
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
        size_constraints: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSizeConstraintSet.SizeConstraintProperty", typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Create a new ``AWS::WAF::SizeConstraintSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name, if any, of the ``SizeConstraintSet`` .
        :param size_constraints: The size constraint and the part of the web request to check.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147d3705a211b6b10a58a7a1b89d34ed53ce861eda8a8425dc2bd22b97061932)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2a714d14c4aadbcb49972a390608326ed98a93093d8b4ac3029f0384351a613)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36c9988a44611d657ab5323faed14a7877dba68a8baefc628eef0b9c7e172eda)
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

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html#cfn-waf-sizeconstraintset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282b71a0f00220a6f77f2fbc2f53f90cd77a9fa4c4af564eba7f551687d4d2ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sizeConstraints")
    def size_constraints(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSizeConstraintSet.SizeConstraintProperty"]]]:
        '''The size constraint and the part of the web request to check.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html#cfn-waf-sizeconstraintset-sizeconstraints
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSizeConstraintSet.SizeConstraintProperty"]]], jsii.get(self, "sizeConstraints"))

    @size_constraints.setter
    def size_constraints(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSizeConstraintSet.SizeConstraintProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa60c509300e19ecd8eb54f2662174c439aa4f6cd07b5281b5096c75776d35f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeConstraints", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet.FieldToMatchProperty",
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
            '''The part of a web request that you want to inspect, such as a specified header or a query string.

            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform. Amazon CloudFront supports the following methods: ``DELETE`` , ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PATCH`` , ``POST`` , and ``PUT`` . - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .
            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                field_to_match_property = waf.CfnSizeConstraintSet.FieldToMatchProperty(
                    type="type",
                
                    # the properties below are optional
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9153fd31e6d2796edbd4743b9b4ae9cbc04dafc48c0fa47d0af6544f953d484)
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
            - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform. Amazon CloudFront supports the following methods: ``DELETE`` , ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PATCH`` , ``POST`` , and ``PUT`` .
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-type
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-data
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
        jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSet.SizeConstraintProperty",
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
            :param field_to_match: The part of a web request that you want to inspect, such as a specified header or a query string.
            :param size: The size in bytes that you want AWS WAF to compare against the size of the specified ``FieldToMatch`` . AWS WAF uses this in combination with ``ComparisonOperator`` and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match. Valid values for size are 0 - 21474836480 bytes (0 - 20 GB). If you specify ``URI`` for the value of ``Type`` , the / in the URI path that you specify counts as one character. For example, the URI ``/logo.jpg`` is nine characters long.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match. You can only specify a single type of TextTransformation. Note that if you choose ``BODY`` for the value of ``Type`` , you must choose ``NONE`` for ``TextTransformation`` because Amazon CloudFront forwards only the first 8192 bytes for inspection. *NONE* Specify ``NONE`` if you don't want to perform any text transformations. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                size_constraint_property = waf.CfnSizeConstraintSet.SizeConstraintProperty(
                    comparison_operator="comparisonOperator",
                    field_to_match=waf.CfnSizeConstraintSet.FieldToMatchProperty(
                        type="type",
                
                        # the properties below are optional
                        data="data"
                    ),
                    size=123,
                    text_transformation="textTransformation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c8aa0453e40c4a2f8494780ccd11394ae6676d00872132827d27aa4921e9687)
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            assert result is not None, "Required property 'comparison_operator' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSizeConstraintSet.FieldToMatchProperty"]:
            '''The part of a web request that you want to inspect, such as a specified header or a query string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-size
            '''
            result = self._values.get("size")
            assert result is not None, "Required property 'size' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def text_transformation(self) -> builtins.str:
            '''Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF .

            If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match.

            You can only specify a single type of TextTransformation.

            Note that if you choose ``BODY`` for the value of ``Type`` , you must choose ``NONE`` for ``TextTransformation`` because Amazon CloudFront forwards only the first 8192 bytes for inspection.

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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sizeconstraintset-sizeconstraint.html#cfn-waf-sizeconstraintset-sizeconstraint-texttransformation
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
    jsii_type="@aws-cdk/aws-waf.CfnSizeConstraintSetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "size_constraints": "sizeConstraints"},
)
class CfnSizeConstraintSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        size_constraints: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSizeConstraintSet.SizeConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Properties for defining a ``CfnSizeConstraintSet``.

        :param name: The name, if any, of the ``SizeConstraintSet`` .
        :param size_constraints: The size constraint and the part of the web request to check.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_waf as waf
            
            cfn_size_constraint_set_props = waf.CfnSizeConstraintSetProps(
                name="name",
                size_constraints=[waf.CfnSizeConstraintSet.SizeConstraintProperty(
                    comparison_operator="comparisonOperator",
                    field_to_match=waf.CfnSizeConstraintSet.FieldToMatchProperty(
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac0e72b54c644faf83882e65ec8e01e31e580d58b7f772b63ba0e47a99429630)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument size_constraints", value=size_constraints, expected_type=type_hints["size_constraints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "size_constraints": size_constraints,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name, if any, of the ``SizeConstraintSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html#cfn-waf-sizeconstraintset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size_constraints(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSizeConstraintSet.SizeConstraintProperty]]]:
        '''The size constraint and the part of the web request to check.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sizeconstraintset.html#cfn-waf-sizeconstraintset-sizeconstraints
        '''
        result = self._values.get("size_constraints")
        assert result is not None, "Required property 'size_constraints' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSizeConstraintSet.SizeConstraintProperty]]], result)

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
    jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet",
):
    '''A CloudFormation ``AWS::WAF::SqlInjectionMatchSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A complex type that contains ``SqlInjectionMatchTuple`` objects, which specify the parts of web requests that you want AWS WAF to inspect for snippets of malicious SQL code and, if you want AWS WAF to inspect a header, the name of the header. If a ``SqlInjectionMatchSet`` contains more than one ``SqlInjectionMatchTuple`` object, a request needs to include snippets of SQL code in only one of the specified parts of the request to be considered a match.

    :cloudformationResource: AWS::WAF::SqlInjectionMatchSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_waf as waf
        
        cfn_sql_injection_match_set = waf.CfnSqlInjectionMatchSet(self, "MyCfnSqlInjectionMatchSet",
            name="name",
        
            # the properties below are optional
            sql_injection_match_tuples=[waf.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty(
                field_to_match=waf.CfnSqlInjectionMatchSet.FieldToMatchProperty(
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
        '''Create a new ``AWS::WAF::SqlInjectionMatchSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name, if any, of the ``SqlInjectionMatchSet`` .
        :param sql_injection_match_tuples: Specifies the parts of web requests that you want to inspect for snippets of malicious SQL code.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff44c952e7db72eaf06c9e5ec46952ab683f2be4abc814aeeedd95e33922b14b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53d871d36825088c53dc1ef3afa231d08f4152b61e12748f244ef24bd030d63a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fd807aeb78554149de4035f0a12c2bde135af5ad900856a24a5680c71b132cd)
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

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html#cfn-waf-sqlinjectionmatchset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db603e1fbe8b5ec5543794c9447e31c8614aeb5c2f546939f521a60d8887f92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sqlInjectionMatchTuples")
    def sql_injection_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]]:
        '''Specifies the parts of web requests that you want to inspect for snippets of malicious SQL code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]], jsii.get(self, "sqlInjectionMatchTuples"))

    @sql_injection_match_tuples.setter
    def sql_injection_match_tuples(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65306ec7d8fa3321a8663826a238c3106ca8b7a1522d548a2aba4c961777c0b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlInjectionMatchTuples", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet.FieldToMatchProperty",
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
            '''The part of a web request that you want to inspect, such as a specified header or a query string.

            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform. Amazon CloudFront supports the following methods: ``DELETE`` , ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PATCH`` , ``POST`` , and ``PUT`` . - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .
            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                field_to_match_property = waf.CfnSqlInjectionMatchSet.FieldToMatchProperty(
                    type="type",
                
                    # the properties below are optional
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17e09a3e5fe1cd009d383fe804ca2f4dc8e8598c07bfdd28edcb4c583739d9ba)
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
            - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform. Amazon CloudFront supports the following methods: ``DELETE`` , ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PATCH`` , ``POST`` , and ``PUT`` .
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-type
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-bytematchset-bytematchtuples-fieldtomatch.html#cfn-waf-sizeconstraintset-sizeconstraint-fieldtomatch-data
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
        jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty",
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

            :param field_to_match: The part of a web request that you want to inspect, such as a specified header or a query string.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match. You can only specify a single type of TextTransformation. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value. *NONE* Specify ``NONE`` if you don't want to perform any text transformations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sqlinjectionmatchset-sqlinjectionmatchtuples.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                sql_injection_match_tuple_property = waf.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty(
                    field_to_match=waf.CfnSqlInjectionMatchSet.FieldToMatchProperty(
                        type="type",
                
                        # the properties below are optional
                        data="data"
                    ),
                    text_transformation="textTransformation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ede7a1b9d6a241c6026ea6d1c9e14ad1074dadde534dd2eeeb47e7eedb12ba90)
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
            '''The part of a web request that you want to inspect, such as a specified header or a query string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sqlinjectionmatchset-sqlinjectionmatchtuples.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples-fieldtomatch
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-sqlinjectionmatchset-sqlinjectionmatchtuples.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples-texttransformation
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
    jsii_type="@aws-cdk/aws-waf.CfnSqlInjectionMatchSetProps",
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

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_waf as waf
            
            cfn_sql_injection_match_set_props = waf.CfnSqlInjectionMatchSetProps(
                name="name",
            
                # the properties below are optional
                sql_injection_match_tuples=[waf.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty(
                    field_to_match=waf.CfnSqlInjectionMatchSet.FieldToMatchProperty(
                        type="type",
            
                        # the properties below are optional
                        data="data"
                    ),
                    text_transformation="textTransformation"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03916999b5f3289953855256277e15731012fbcbed4090b1618a43f468a05ec)
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

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html#cfn-waf-sqlinjectionmatchset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_injection_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty]]]]:
        '''Specifies the parts of web requests that you want to inspect for snippets of malicious SQL code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-sqlinjectionmatchset.html#cfn-waf-sqlinjectionmatchset-sqlinjectionmatchtuples
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
    jsii_type="@aws-cdk/aws-waf.CfnWebACL",
):
    '''A CloudFormation ``AWS::WAF::WebACL``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    Contains the ``Rules`` that identify the requests that you want to allow, block, or count. In a ``WebACL`` , you also specify a default action ( ``ALLOW`` or ``BLOCK`` ), and the action for each ``Rule`` that you add to a ``WebACL`` , for example, block requests from specified IP addresses or block requests from specified referrers. You also associate the ``WebACL`` with a Amazon CloudFront distribution to identify the requests that you want AWS WAF to filter. If you add more than one ``Rule`` to a ``WebACL`` , a request needs to match only one of the specifications to be allowed, blocked, or counted.

    :cloudformationResource: AWS::WAF::WebACL
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_waf as waf
        
        cfn_web_aCL = waf.CfnWebACL(self, "MyCfnWebACL",
            default_action=waf.CfnWebACL.WafActionProperty(
                type="type"
            ),
            metric_name="metricName",
            name="name",
        
            # the properties below are optional
            rules=[waf.CfnWebACL.ActivatedRuleProperty(
                priority=123,
                rule_id="ruleId",
        
                # the properties below are optional
                action=waf.CfnWebACL.WafActionProperty(
                    type="type"
                )
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWebACL.WafActionProperty", typing.Dict[builtins.str, typing.Any]]],
        metric_name: builtins.str,
        name: builtins.str,
        rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWebACL.ActivatedRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::WAF::WebACL``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_action: The action to perform if none of the ``Rules`` contained in the ``WebACL`` match. The action is specified by the ``WafAction`` object.
        :param metric_name: The name of the metrics for this ``WebACL`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``WebACL`` .
        :param name: A friendly name or description of the ``WebACL`` . You can't change the name of a ``WebACL`` after you create it.
        :param rules: An array that contains the action for each ``Rule`` in a ``WebACL`` , the priority of the ``Rule`` , and the ID of the ``Rule`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007bd193a928f8ca5e5b10ca3d2cab27775877b83a51baf94418b3b84c3f8214)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e1063519e0aa7b02fcb7eca91584b0cb77b98d96a981148f84d98e4febaa993)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad6f8d5058d16e261b175279938408bc225c0970bda76423bf223153d82b3341)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.WafActionProperty"]:
        '''The action to perform if none of the ``Rules`` contained in the ``WebACL`` match.

        The action is specified by the ``WafAction`` object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-defaultaction
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.WafActionProperty"], jsii.get(self, "defaultAction"))

    @default_action.setter
    def default_action(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.WafActionProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41fc9e82491d8fd84cb36f1adc61ab0c4ea85383a020a92f1f911f57b217fe53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAction", value)

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        '''The name of the metrics for this ``WebACL`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``WebACL`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-metricname
        '''
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2f08ffa3ce4ac24b6bb903bcedebc4726aa85be46d27a92f39b5cb08beeac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``WebACL`` .

        You can't change the name of a ``WebACL`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d434aafb282be37b0873334db37de7409ae644943da46274072748ecbdaa2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.ActivatedRuleProperty"]]]]:
        '''An array that contains the action for each ``Rule`` in a ``WebACL`` , the priority of the ``Rule`` , and the ID of the ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-rules
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.ActivatedRuleProperty"]]]], jsii.get(self, "rules"))

    @rules.setter
    def rules(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.ActivatedRuleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce4ef78bcb17f4cffada04f8c08a3c5e4c97f3febd70c2f46c98e5bb6280ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rules", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-waf.CfnWebACL.ActivatedRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "rule_id": "ruleId", "action": "action"},
    )
    class ActivatedRuleProperty:
        def __init__(
            self,
            *,
            priority: jsii.Number,
            rule_id: builtins.str,
            action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWebACL.WafActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``ActivatedRule`` object in an ``UpdateWebACL`` request specifies a ``Rule`` that you want to insert or delete, the priority of the ``Rule`` in the ``WebACL`` , and the action that you want AWS WAF to take when a web request matches the ``Rule`` ( ``ALLOW`` , ``BLOCK`` , or ``COUNT`` ).

            To specify whether to insert or delete a ``Rule`` , use the ``Action`` parameter in the ``WebACLUpdate`` data type.

            :param priority: Specifies the order in which the ``Rules`` in a ``WebACL`` are evaluated. Rules with a lower value for ``Priority`` are evaluated before ``Rules`` with a higher value. The value must be a unique integer. If you add multiple ``Rules`` to a ``WebACL`` , the values don't need to be consecutive.
            :param rule_id: The ``RuleId`` for a ``Rule`` . You use ``RuleId`` to get more information about a ``Rule`` , update a ``Rule`` , insert a ``Rule`` into a ``WebACL`` or delete a one from a ``WebACL`` , or delete a ``Rule`` from AWS WAF . ``RuleId`` is returned by ``CreateRule`` and by ``ListRules`` .
            :param action: Specifies the action that Amazon CloudFront or AWS WAF takes when a web request matches the conditions in the ``Rule`` . Valid values for ``Action`` include the following: - ``ALLOW`` : CloudFront responds with the requested object. - ``BLOCK`` : CloudFront responds with an HTTP 403 (Forbidden) status code. - ``COUNT`` : AWS WAF increments a counter of requests that match the conditions in the rule and then continues to inspect the web request based on the remaining rules in the web ACL. ``ActivatedRule|OverrideAction`` applies only when updating or adding a ``RuleGroup`` to a ``WebACL`` . In this case, you do not use ``ActivatedRule|Action`` . For all other update requests, ``ActivatedRule|Action`` is used instead of ``ActivatedRule|OverrideAction`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                activated_rule_property = waf.CfnWebACL.ActivatedRuleProperty(
                    priority=123,
                    rule_id="ruleId",
                
                    # the properties below are optional
                    action=waf.CfnWebACL.WafActionProperty(
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9e3a6c8af62f886785a4e04344f282b7cba72d41e5a33022f236c6f6b41789d)
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "priority": priority,
                "rule_id": rule_id,
            }
            if action is not None:
                self._values["action"] = action

        @builtins.property
        def priority(self) -> jsii.Number:
            '''Specifies the order in which the ``Rules`` in a ``WebACL`` are evaluated.

            Rules with a lower value for ``Priority`` are evaluated before ``Rules`` with a higher value. The value must be a unique integer. If you add multiple ``Rules`` to a ``WebACL`` , the values don't need to be consecutive.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html#cfn-waf-webacl-rules-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def rule_id(self) -> builtins.str:
            '''The ``RuleId`` for a ``Rule`` .

            You use ``RuleId`` to get more information about a ``Rule`` , update a ``Rule`` , insert a ``Rule`` into a ``WebACL`` or delete a one from a ``WebACL`` , or delete a ``Rule`` from AWS WAF .

            ``RuleId`` is returned by ``CreateRule`` and by ``ListRules`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html#cfn-waf-webacl-rules-ruleid
            '''
            result = self._values.get("rule_id")
            assert result is not None, "Required property 'rule_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.WafActionProperty"]]:
            '''Specifies the action that Amazon CloudFront or AWS WAF takes when a web request matches the conditions in the ``Rule`` .

            Valid values for ``Action`` include the following:

            - ``ALLOW`` : CloudFront responds with the requested object.
            - ``BLOCK`` : CloudFront responds with an HTTP 403 (Forbidden) status code.
            - ``COUNT`` : AWS WAF increments a counter of requests that match the conditions in the rule and then continues to inspect the web request based on the remaining rules in the web ACL.

            ``ActivatedRule|OverrideAction`` applies only when updating or adding a ``RuleGroup`` to a ``WebACL`` . In this case, you do not use ``ActivatedRule|Action`` . For all other update requests, ``ActivatedRule|Action`` is used instead of ``ActivatedRule|OverrideAction`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-rules.html#cfn-waf-webacl-rules-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWebACL.WafActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActivatedRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-waf.CfnWebACL.WafActionProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class WafActionProperty:
        def __init__(self, *, type: builtins.str) -> None:
            '''.. epigraph::

   This is *AWS WAF Classic* documentation.

            For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
            .. epigraph::

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            For the action that is associated with a rule in a ``WebACL`` , specifies the action that you want AWS WAF to perform when a web request matches all of the conditions in a rule. For the default action in a ``WebACL`` , specifies the action that you want AWS WAF to take when a web request doesn't match all of the conditions in any of the rules in a ``WebACL`` .

            :param type: Specifies how you want AWS WAF to respond to requests that match the settings in a ``Rule`` . Valid settings include the following: - ``ALLOW`` : AWS WAF allows requests - ``BLOCK`` : AWS WAF blocks requests - ``COUNT`` : AWS WAF increments a counter of the requests that match all of the conditions in the rule. AWS WAF then continues to inspect the web request based on the remaining rules in the web ACL. You can't specify ``COUNT`` for the default action for a ``WebACL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                waf_action_property = waf.CfnWebACL.WafActionProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cdae02a6013f36edef311b7c4f34580b82045f7dbcc6a0f224141956bb54c687)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''Specifies how you want AWS WAF to respond to requests that match the settings in a ``Rule`` .

            Valid settings include the following:

            - ``ALLOW`` : AWS WAF allows requests
            - ``BLOCK`` : AWS WAF blocks requests
            - ``COUNT`` : AWS WAF increments a counter of the requests that match all of the conditions in the rule. AWS WAF then continues to inspect the web request based on the remaining rules in the web ACL. You can't specify ``COUNT`` for the default action for a ``WebACL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-webacl-action.html#cfn-waf-webacl-action-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WafActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-waf.CfnWebACLProps",
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
        default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.WafActionProperty, typing.Dict[builtins.str, typing.Any]]],
        metric_name: builtins.str,
        name: builtins.str,
        rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.ActivatedRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWebACL``.

        :param default_action: The action to perform if none of the ``Rules`` contained in the ``WebACL`` match. The action is specified by the ``WafAction`` object.
        :param metric_name: The name of the metrics for this ``WebACL`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``WebACL`` .
        :param name: A friendly name or description of the ``WebACL`` . You can't change the name of a ``WebACL`` after you create it.
        :param rules: An array that contains the action for each ``Rule`` in a ``WebACL`` , the priority of the ``Rule`` , and the ID of the ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_waf as waf
            
            cfn_web_aCLProps = waf.CfnWebACLProps(
                default_action=waf.CfnWebACL.WafActionProperty(
                    type="type"
                ),
                metric_name="metricName",
                name="name",
            
                # the properties below are optional
                rules=[waf.CfnWebACL.ActivatedRuleProperty(
                    priority=123,
                    rule_id="ruleId",
            
                    # the properties below are optional
                    action=waf.CfnWebACL.WafActionProperty(
                        type="type"
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a88e6925951af40d970244cf347ed426b9d5f2edc814562672a3a4f2ab39f78)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.WafActionProperty]:
        '''The action to perform if none of the ``Rules`` contained in the ``WebACL`` match.

        The action is specified by the ``WafAction`` object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-defaultaction
        '''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.WafActionProperty], result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''The name of the metrics for this ``WebACL`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``WebACL`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-metricname
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A friendly name or description of the ``WebACL`` .

        You can't change the name of a ``WebACL`` after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.ActivatedRuleProperty]]]]:
        '''An array that contains the action for each ``Rule`` in a ``WebACL`` , the priority of the ``Rule`` , and the ID of the ``Rule`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-webacl.html#cfn-waf-webacl-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.ActivatedRuleProperty]]]], result)

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
    jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet",
):
    '''A CloudFormation ``AWS::WAF::XssMatchSet``.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A complex type that contains ``XssMatchTuple`` objects, which specify the parts of web requests that you want AWS WAF to inspect for cross-site scripting attacks and, if you want AWS WAF to inspect a header, the name of the header. If a ``XssMatchSet`` contains more than one ``XssMatchTuple`` object, a request needs to include cross-site scripting attacks in only one of the specified parts of the request to be considered a match.

    :cloudformationResource: AWS::WAF::XssMatchSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_waf as waf
        
        cfn_xss_match_set = waf.CfnXssMatchSet(self, "MyCfnXssMatchSet",
            name="name",
            xss_match_tuples=[waf.CfnXssMatchSet.XssMatchTupleProperty(
                field_to_match=waf.CfnXssMatchSet.FieldToMatchProperty(
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
        xss_match_tuples: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnXssMatchSet.XssMatchTupleProperty", typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Create a new ``AWS::WAF::XssMatchSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name, if any, of the ``XssMatchSet`` .
        :param xss_match_tuples: Specifies the parts of web requests that you want to inspect for cross-site scripting attacks.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405cf02adcd18e57dfc6d756cb487f5d3cde2d2b16485441e7c54bde1ca35bb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__418a0a63da39224cac63c85ebd1ad34197091f9481966b4b12ae672a9ff22bca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__042cfd7f312e5fbee0433f0e57406e97a157d1a9ea22b6c33daf2faec2c7ae0b)
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

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html#cfn-waf-xssmatchset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4d32e4755a442edb1eef590cc8a9e7b7da040f9a3492d2fed9c67ae793e275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="xssMatchTuples")
    def xss_match_tuples(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnXssMatchSet.XssMatchTupleProperty"]]]:
        '''Specifies the parts of web requests that you want to inspect for cross-site scripting attacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html#cfn-waf-xssmatchset-xssmatchtuples
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnXssMatchSet.XssMatchTupleProperty"]]], jsii.get(self, "xssMatchTuples"))

    @xss_match_tuples.setter
    def xss_match_tuples(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnXssMatchSet.XssMatchTupleProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77c47a01f0eee1b50d8962b9cfde5dc1bba7587d7cc18ec566a52d513cc0095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xssMatchTuples", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet.FieldToMatchProperty",
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
            '''The part of a web request that you want to inspect, such as a specified header or a query string.

            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform. Amazon CloudFront supports the following methods: ``DELETE`` , ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PATCH`` , ``POST`` , and ``PUT`` . - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .
            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                field_to_match_property = waf.CfnXssMatchSet.FieldToMatchProperty(
                    type="type",
                
                    # the properties below are optional
                    data="data"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80c573338e7b3ec912d262565cc48a0380876d5575f25a7bc3cc5ecf4c643fa1)
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
            - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform. Amazon CloudFront supports the following methods: ``DELETE`` , ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PATCH`` , ``POST`` , and ``PUT`` .
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple-fieldtomatch.html#cfn-waf-xssmatchset-xssmatchtuple-fieldtomatch-type
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple-fieldtomatch.html#cfn-waf-xssmatchset-xssmatchtuple-fieldtomatch-data
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
        jsii_type="@aws-cdk/aws-waf.CfnXssMatchSet.XssMatchTupleProperty",
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

            :param field_to_match: The part of a web request that you want to inspect, such as a specified header or a query string.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match. You can only specify a single type of TextTransformation. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value. *NONE* Specify ``NONE`` if you don't want to perform any text transformations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_waf as waf
                
                xss_match_tuple_property = waf.CfnXssMatchSet.XssMatchTupleProperty(
                    field_to_match=waf.CfnXssMatchSet.FieldToMatchProperty(
                        type="type",
                
                        # the properties below are optional
                        data="data"
                    ),
                    text_transformation="textTransformation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0539908fb56e88e12933a17bc0d9625231444753c001e297ac7bfe75f8c7b323)
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
            '''The part of a web request that you want to inspect, such as a specified header or a query string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple.html#cfn-waf-xssmatchset-xssmatchtuple-fieldtomatch
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

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-waf-xssmatchset-xssmatchtuple.html#cfn-waf-xssmatchset-xssmatchtuple-texttransformation
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
    jsii_type="@aws-cdk/aws-waf.CfnXssMatchSetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "xss_match_tuples": "xssMatchTuples"},
)
class CfnXssMatchSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        xss_match_tuples: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnXssMatchSet.XssMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Properties for defining a ``CfnXssMatchSet``.

        :param name: The name, if any, of the ``XssMatchSet`` .
        :param xss_match_tuples: Specifies the parts of web requests that you want to inspect for cross-site scripting attacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_waf as waf
            
            cfn_xss_match_set_props = waf.CfnXssMatchSetProps(
                name="name",
                xss_match_tuples=[waf.CfnXssMatchSet.XssMatchTupleProperty(
                    field_to_match=waf.CfnXssMatchSet.FieldToMatchProperty(
                        type="type",
            
                        # the properties below are optional
                        data="data"
                    ),
                    text_transformation="textTransformation"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed42a7dec474a3a64815e3da384e51793fc8a87ecd3bc3b34bbcaf0475f8462)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument xss_match_tuples", value=xss_match_tuples, expected_type=type_hints["xss_match_tuples"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "xss_match_tuples": xss_match_tuples,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name, if any, of the ``XssMatchSet`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html#cfn-waf-xssmatchset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def xss_match_tuples(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnXssMatchSet.XssMatchTupleProperty]]]:
        '''Specifies the parts of web requests that you want to inspect for cross-site scripting attacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-waf-xssmatchset.html#cfn-waf-xssmatchset-xssmatchtuples
        '''
        result = self._values.get("xss_match_tuples")
        assert result is not None, "Required property 'xss_match_tuples' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnXssMatchSet.XssMatchTupleProperty]]], result)

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
    "CfnIPSet",
    "CfnIPSetProps",
    "CfnRule",
    "CfnRuleProps",
    "CfnSizeConstraintSet",
    "CfnSizeConstraintSetProps",
    "CfnSqlInjectionMatchSet",
    "CfnSqlInjectionMatchSetProps",
    "CfnWebACL",
    "CfnWebACLProps",
    "CfnXssMatchSet",
    "CfnXssMatchSetProps",
]

publication.publish()

def _typecheckingstub__5ff9b621c9d700b26114e8c55d0581f1cd76eacc1249303b31e31dd17db2539f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    byte_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnByteMatchSet.ByteMatchTupleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bb9f6e07c45ae311ef3b6b169fd3b107c61898ac1d850ab84732260cbbc34a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e66199391c07d8f80703f2a29874c52c3853b1bfaadca0889b574a3a50491b3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8e56453fe3265390c7d6b6602958908f01dfa188d8ade928fe233ab5a67d02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348cffb9e6f600bfa21c699986a7d73c8b8d99db580b50c0c2b59818a19c646a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnByteMatchSet.ByteMatchTupleProperty, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f615c50ac397240ef456ec57d22a117fb5dd4ce9f467f2fbb4c7505da21ad231(
    *,
    field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnByteMatchSet.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]],
    positional_constraint: builtins.str,
    text_transformation: builtins.str,
    target_string: typing.Optional[builtins.str] = None,
    target_string_base64: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7154ed71c4602041a72374ffe2cdddaeb12fdee7198ece0e9a31f9e6b81364b6(
    *,
    type: builtins.str,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161a568cd4770d077eec7193fc874c37b11e9b443a016bc48adb91e333c0dfd8(
    *,
    name: builtins.str,
    byte_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnByteMatchSet.ByteMatchTupleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a18f7210ce113d1a9998808c0f823422883df8bb594280868228baaf96a79b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    ip_set_descriptors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnIPSet.IPSetDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baa80babbfc753aaf0aa673d59d0f192e26ac2f3f9d732d700e1fbc611990c6(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8517257e3821d6c22634b1d2be1de36d3498e904ec723c2fcff6e34a2fbcda(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9a43b65a96f08b3dd2f8a42a8df8570b842dd64dd5de746eb9e1c0efa6f6bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e6fd9a88419dcbc3facedb7b94efc69bb5da47f9baa0d81f5894707823c6e0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnIPSet.IPSetDescriptorProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba6ca3f8f4aa5131b6c0790ac408d836c80789c4f394c5e81460cf6c0b7d993(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e065c4f1d20f561df3d5b0a1f965eb1f514b36b90716f3552ccdb678c5c47633(
    *,
    name: builtins.str,
    ip_set_descriptors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnIPSet.IPSetDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc688a3bad3463713a45885f1ba83433a2095417b718020cd1ff230ec90d8a93(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    metric_name: builtins.str,
    name: builtins.str,
    predicates: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951d7a0c98eeeacd730f20f48b5fe9075aebc2ed59c702337c2ed750338305d0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10a59480b8152726ced54dc9994021cf03808e7227a2e3155a974440ec09026(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a2ea8b9bf30c2fafbc436d932d38f548323961d7600f1442dee7cc7f4313f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbc0b30c2bf6d75b6e6c94961415b195f6c9f06811433b6d54af58e745273fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba9da071001acadeba37fb8db736489bf6c9b8b0fcb2c2ad52f8f08cfef8979(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.PredicateProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc224fa84c648f83adf2fb1ea06c7c955934d2638323d4d6385d9ba62dc7ae68(
    *,
    data_id: builtins.str,
    negated: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3711652825bb89ed61fd78f18c78cc978a8c9d8075ed61feb475ca12519842(
    *,
    metric_name: builtins.str,
    name: builtins.str,
    predicates: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147d3705a211b6b10a58a7a1b89d34ed53ce861eda8a8425dc2bd22b97061932(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    size_constraints: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSizeConstraintSet.SizeConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a714d14c4aadbcb49972a390608326ed98a93093d8b4ac3029f0384351a613(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c9988a44611d657ab5323faed14a7877dba68a8baefc628eef0b9c7e172eda(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282b71a0f00220a6f77f2fbc2f53f90cd77a9fa4c4af564eba7f551687d4d2ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa60c509300e19ecd8eb54f2662174c439aa4f6cd07b5281b5096c75776d35f(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSizeConstraintSet.SizeConstraintProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9153fd31e6d2796edbd4743b9b4ae9cbc04dafc48c0fa47d0af6544f953d484(
    *,
    type: builtins.str,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8aa0453e40c4a2f8494780ccd11394ae6676d00872132827d27aa4921e9687(
    *,
    comparison_operator: builtins.str,
    field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSizeConstraintSet.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]],
    size: jsii.Number,
    text_transformation: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0e72b54c644faf83882e65ec8e01e31e580d58b7f772b63ba0e47a99429630(
    *,
    name: builtins.str,
    size_constraints: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSizeConstraintSet.SizeConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff44c952e7db72eaf06c9e5ec46952ab683f2be4abc814aeeedd95e33922b14b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    sql_injection_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d871d36825088c53dc1ef3afa231d08f4152b61e12748f244ef24bd030d63a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd807aeb78554149de4035f0a12c2bde135af5ad900856a24a5680c71b132cd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db603e1fbe8b5ec5543794c9447e31c8614aeb5c2f546939f521a60d8887f92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65306ec7d8fa3321a8663826a238c3106ca8b7a1522d548a2aba4c961777c0b6(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e09a3e5fe1cd009d383fe804ca2f4dc8e8598c07bfdd28edcb4c583739d9ba(
    *,
    type: builtins.str,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede7a1b9d6a241c6026ea6d1c9e14ad1074dadde534dd2eeeb47e7eedb12ba90(
    *,
    field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSqlInjectionMatchSet.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]],
    text_transformation: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03916999b5f3289953855256277e15731012fbcbed4090b1618a43f468a05ec(
    *,
    name: builtins.str,
    sql_injection_match_tuples: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007bd193a928f8ca5e5b10ca3d2cab27775877b83a51baf94418b3b84c3f8214(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.WafActionProperty, typing.Dict[builtins.str, typing.Any]]],
    metric_name: builtins.str,
    name: builtins.str,
    rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.ActivatedRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1063519e0aa7b02fcb7eca91584b0cb77b98d96a981148f84d98e4febaa993(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6f8d5058d16e261b175279938408bc225c0970bda76423bf223153d82b3341(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41fc9e82491d8fd84cb36f1adc61ab0c4ea85383a020a92f1f911f57b217fe53(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.WafActionProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2f08ffa3ce4ac24b6bb903bcedebc4726aa85be46d27a92f39b5cb08beeac4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d434aafb282be37b0873334db37de7409ae644943da46274072748ecbdaa2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce4ef78bcb17f4cffada04f8c08a3c5e4c97f3febd70c2f46c98e5bb6280ee5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWebACL.ActivatedRuleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e3a6c8af62f886785a4e04344f282b7cba72d41e5a33022f236c6f6b41789d(
    *,
    priority: jsii.Number,
    rule_id: builtins.str,
    action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.WafActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdae02a6013f36edef311b7c4f34580b82045f7dbcc6a0f224141956bb54c687(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a88e6925951af40d970244cf347ed426b9d5f2edc814562672a3a4f2ab39f78(
    *,
    default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.WafActionProperty, typing.Dict[builtins.str, typing.Any]]],
    metric_name: builtins.str,
    name: builtins.str,
    rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWebACL.ActivatedRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405cf02adcd18e57dfc6d756cb487f5d3cde2d2b16485441e7c54bde1ca35bb1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    xss_match_tuples: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnXssMatchSet.XssMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418a0a63da39224cac63c85ebd1ad34197091f9481966b4b12ae672a9ff22bca(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042cfd7f312e5fbee0433f0e57406e97a157d1a9ea22b6c33daf2faec2c7ae0b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4d32e4755a442edb1eef590cc8a9e7b7da040f9a3492d2fed9c67ae793e275(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77c47a01f0eee1b50d8962b9cfde5dc1bba7587d7cc18ec566a52d513cc0095(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnXssMatchSet.XssMatchTupleProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c573338e7b3ec912d262565cc48a0380876d5575f25a7bc3cc5ecf4c643fa1(
    *,
    type: builtins.str,
    data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0539908fb56e88e12933a17bc0d9625231444753c001e297ac7bfe75f8c7b323(
    *,
    field_to_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnXssMatchSet.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]],
    text_transformation: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed42a7dec474a3a64815e3da384e51793fc8a87ecd3bc3b34bbcaf0475f8462(
    *,
    name: builtins.str,
    xss_match_tuples: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnXssMatchSet.XssMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass
