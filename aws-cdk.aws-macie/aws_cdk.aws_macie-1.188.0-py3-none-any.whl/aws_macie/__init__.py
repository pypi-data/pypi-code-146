'''
# AWS::Macie Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_macie as macie
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Macie construct libraries](https://constructs.dev/search?q=macie)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Macie resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Macie.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Macie](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Macie.html).

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
class CfnAllowList(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-macie.CfnAllowList",
):
    '''A CloudFormation ``AWS::Macie::AllowList``.

    The ``AWS::Macie::AllowList`` resource specifies an allow list. In Amazon Macie , an allow list defines specific text or a text pattern for Macie to ignore when it inspects data sources for sensitive data. If data matches text or a text pattern in an allow list, Macie doesn’t report the data in sensitive data findings or sensitive data discovery results, even if the data matches the criteria of a custom data identifier or a managed data identifier. You can create and use allow lists in all the AWS Regions where Macie is currently available except the Asia Pacific (Osaka) Region.

    Macie supports two types of allow lists:

    - *Predefined text* - For this type of list ( ``S3WordsList`` ), you create a line-delimited plaintext file that lists specific text to ignore, and you store the file in an Amazon Simple Storage Service ( Amazon S3 ) bucket. You then configure settings for Macie to access the list in the bucket.

    This type of list typically contains specific words, phrases, and other kinds of character sequences that aren’t sensitive, aren't likely to change, and don’t necessarily adhere to a common pattern. If you use this type of list, Macie doesn't report occurrences of text that exactly match a complete entry in the list. Macie treats each entry in the list as a string literal value. Matches aren't case sensitive.

    - *Regular expression* - For this type of list ( ``Regex`` ), you specify a regular expression that defines a text pattern to ignore. Unlike an allow list with predefined text, you store the regex and all other list settings in Macie .

    This type of list is helpful if you want to specify text that isn’t sensitive but varies or is likely to change while also adhering to a common pattern. If you use this type of list, Macie doesn't report occurrences of text that completely match the pattern defined by the list.

    For more information, see `Defining sensitive data exceptions with allow lists <https://docs.aws.amazon.com/macie/latest/user/allow-lists.html>`_ in the *Amazon Macie User Guide* .

    An ``AWS::Macie::Session`` resource must exist for an AWS account before you can create an ``AWS::Macie::AllowList`` resource for the account. Use a `DependsOn attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ to ensure that an ``AWS::Macie::Session`` resource is created before other Macie resources are created for an account. For example, ``"DependsOn": "Session"`` .

    :cloudformationResource: AWS::Macie::AllowList
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-allowlist.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_macie as macie
        
        cfn_allow_list = macie.CfnAllowList(self, "MyCfnAllowList",
            criteria=macie.CfnAllowList.CriteriaProperty(
                regex="regex",
                s3_words_list=macie.CfnAllowList.S3WordsListProperty(
                    bucket_name="bucketName",
                    object_key="objectKey"
                )
            ),
            name="name",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        criteria: typing.Union[typing.Union["CfnAllowList.CriteriaProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Macie::AllowList``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param criteria: The criteria that specify the text or text pattern to ignore. The criteria can be the location and name of an Amazon S3 object that lists specific text to ignore ( ``S3WordsList`` ), or a regular expression ( ``Regex`` ) that defines a text pattern to ignore.
        :param name: A custom name for the allow list. The name can contain 1-128 characters.
        :param description: A custom description of the allow list. The description can contain 1-512 characters.
        :param tags: An array of key-value pairs to apply to the allow list. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97dd8f9de24502693512247a15acf868ef9ef512cf75e3ccdc87bc15bb53d690)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAllowListProps(
            criteria=criteria, name=name, description=description, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4721b70f482d51384dccc06621eb481a9b32e91dd8d409192642431b9972248f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd4a448000cdacf9c97a2df5a143ba12aaae0db801a1834ed18abc2c3a910380)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the allow list.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The unique identifier for the allow list.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current status of the allow list, which indicates whether Amazon Macie can access and use the list's criteria.

        If the list's criteria specify a regular expression ( ``Regex`` ), this value is typically ``OK`` . Macie can compile the expression. If the list's criteria specify an Amazon S3 object ( ``S3WordsList`` ), possible values are:

        - ``OK`` - Macie can retrieve and parse the contents of the object.
        - ``S3_OBJECT_ACCESS_DENIED`` - Macie isn't allowed to access the object or the object is encrypted with a customer managed AWS KMS key that Macie isn't allowed to use. Check the bucket policy and other permissions settings for the bucket and the object. If the object is encrypted, also ensure that it's encrypted with a key that Macie is allowed to use.
        - ``S3_OBJECT_EMPTY`` - Macie can retrieve the object but the object doesn't contain any content. Ensure that the object contains the correct entries. Also ensure that the list's criteria specify the correct bucket and object names.
        - ``S3_OBJECT_NOT_FOUND`` - The object doesn't exist in Amazon S3 . Ensure that the list's criteria specify the correct bucket and object names.
        - ``S3_OBJECT_OVERSIZE`` - Macie can retrieve the object. However, the object contains too many entries or its storage size exceeds the quota for an allow list. Try breaking the list into multiple files and ensure that each file doesn't exceed any quotas. Then configure list settings in Macie for each file.
        - ``S3_THROTTLED`` - Amazon S3 throttled the request to retrieve the object. Wait a few minutes and then try again.
        - ``S3_USER_ACCESS_DENIED`` - Amazon S3 denied the request to retrieve the object. If the specified object exists, you're not allowed to access it or it's encrypted with an AWS KMS key that you're not allowed to use. Work with your AWS administrator to ensure that the list's criteria specify the correct bucket and object names, and you have read access to the bucket and the object. If the object is encrypted, also ensure that it's encrypted with a key that you're allowed to use.
        - ``UNKNOWN_ERROR`` - A transient or internal error occurred when Macie attempted to retrieve or parse the object. Wait a few minutes and then try again. A list can also have this status if it's encrypted with a key that Amazon S3 and Macie can't access or use.

        For more information, see `Allow list options and requirements <https://docs.aws.amazon.com/macie/latest/user/allow-lists-options.html>`_ in the *Amazon Macie User Guide* .

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to the allow list.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-allowlist.html#cfn-macie-allowlist-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(
        self,
    ) -> typing.Union["CfnAllowList.CriteriaProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The criteria that specify the text or text pattern to ignore.

        The criteria can be the location and name of an Amazon S3 object that lists specific text to ignore ( ``S3WordsList`` ), or a regular expression ( ``Regex`` ) that defines a text pattern to ignore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-allowlist.html#cfn-macie-allowlist-criteria
        '''
        return typing.cast(typing.Union["CfnAllowList.CriteriaProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(
        self,
        value: typing.Union["CfnAllowList.CriteriaProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a82cc0776cfdb1c16791a2bf50700a4ab51f191dcd52bf48483b33029c2c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A custom name for the allow list.

        The name can contain 1-128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-allowlist.html#cfn-macie-allowlist-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c736883bc58756ce664cf6ac61e82ba58514919f6bf93c21efc5230fbf6b9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the allow list.

        The description can contain 1-512 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-allowlist.html#cfn-macie-allowlist-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9362298689ec96e92f699d9949825c9b1a474c9c74bbb804ea9f6d278775753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-macie.CfnAllowList.CriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"regex": "regex", "s3_words_list": "s3WordsList"},
    )
    class CriteriaProperty:
        def __init__(
            self,
            *,
            regex: typing.Optional[builtins.str] = None,
            s3_words_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAllowList.S3WordsListProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the criteria for an allow list, which is a list that defines specific text or a text pattern to ignore when inspecting data sources for sensitive data.

            The criteria can be:

            - The location and name of an Amazon Simple Storage Service ( Amazon S3 ) object that lists specific, predefined text to ignore ( ``S3WordsList`` ), or
            - A regular expression ( ``Regex`` ) that defines a text pattern to ignore.

            The criteria must specify either an S3 object or a regular expression. It can't specify both.

            :param regex: The regular expression ( *regex* ) that defines the text pattern to ignore. The expression can contain 1-512 characters.
            :param s3_words_list: The location and name of an Amazon S3 object that lists specific text to ignore.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-allowlist-criteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_macie as macie
                
                criteria_property = macie.CfnAllowList.CriteriaProperty(
                    regex="regex",
                    s3_words_list=macie.CfnAllowList.S3WordsListProperty(
                        bucket_name="bucketName",
                        object_key="objectKey"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87a4eb646199e38fcd3a9e6a39eafb4d418c8e7b0f9cde9537efb137423be979)
                check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
                check_type(argname="argument s3_words_list", value=s3_words_list, expected_type=type_hints["s3_words_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if regex is not None:
                self._values["regex"] = regex
            if s3_words_list is not None:
                self._values["s3_words_list"] = s3_words_list

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''The regular expression ( *regex* ) that defines the text pattern to ignore.

            The expression can contain 1-512 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-allowlist-criteria.html#cfn-macie-allowlist-criteria-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_words_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAllowList.S3WordsListProperty"]]:
            '''The location and name of an Amazon S3 object that lists specific text to ignore.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-allowlist-criteria.html#cfn-macie-allowlist-criteria-s3wordslist
            '''
            result = self._values.get("s3_words_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAllowList.S3WordsListProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-macie.CfnAllowList.S3WordsListProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "object_key": "objectKey"},
    )
    class S3WordsListProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            object_key: builtins.str,
        ) -> None:
            '''Specifies the location and name of an Amazon Simple Storage Service ( Amazon S3 ) object that lists specific, predefined text to ignore when inspecting data sources for sensitive data.

            :param bucket_name: The full name of the S3 bucket that contains the object. This value correlates to the ``Name`` field of a bucket's properties in Amazon S3 . This value is case sensitive. In addition, don't use wildcard characters or specify partial values for the name.
            :param object_key: The full name of the S3 object. This value correlates to the ``Key`` field of an object's properties in Amazon S3 . If the name includes a path, include the complete path. For example, ``AllowLists/Macie/MyList.txt`` . This value is case sensitive. In addition, don't use wildcard characters or specify partial values for the name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-allowlist-s3wordslist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_macie as macie
                
                s3_words_list_property = macie.CfnAllowList.S3WordsListProperty(
                    bucket_name="bucketName",
                    object_key="objectKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e03463a9c7b7d0ae41b5429f53ac214667de8976d3f13d8f2ffafe6cc892c5d4)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument object_key", value=object_key, expected_type=type_hints["object_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
                "object_key": object_key,
            }

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The full name of the S3 bucket that contains the object.

            This value correlates to the ``Name`` field of a bucket's properties in Amazon S3 .

            This value is case sensitive. In addition, don't use wildcard characters or specify partial values for the name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-allowlist-s3wordslist.html#cfn-macie-allowlist-s3wordslist-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object_key(self) -> builtins.str:
            '''The full name of the S3 object.

            This value correlates to the ``Key`` field of an object's properties in Amazon S3 . If the name includes a path, include the complete path. For example, ``AllowLists/Macie/MyList.txt`` .

            This value is case sensitive. In addition, don't use wildcard characters or specify partial values for the name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-allowlist-s3wordslist.html#cfn-macie-allowlist-s3wordslist-objectkey
            '''
            result = self._values.get("object_key")
            assert result is not None, "Required property 'object_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3WordsListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-macie.CfnAllowListProps",
    jsii_struct_bases=[],
    name_mapping={
        "criteria": "criteria",
        "name": "name",
        "description": "description",
        "tags": "tags",
    },
)
class CfnAllowListProps:
    def __init__(
        self,
        *,
        criteria: typing.Union[typing.Union[CfnAllowList.CriteriaProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAllowList``.

        :param criteria: The criteria that specify the text or text pattern to ignore. The criteria can be the location and name of an Amazon S3 object that lists specific text to ignore ( ``S3WordsList`` ), or a regular expression ( ``Regex`` ) that defines a text pattern to ignore.
        :param name: A custom name for the allow list. The name can contain 1-128 characters.
        :param description: A custom description of the allow list. The description can contain 1-512 characters.
        :param tags: An array of key-value pairs to apply to the allow list. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-allowlist.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_macie as macie
            
            cfn_allow_list_props = macie.CfnAllowListProps(
                criteria=macie.CfnAllowList.CriteriaProperty(
                    regex="regex",
                    s3_words_list=macie.CfnAllowList.S3WordsListProperty(
                        bucket_name="bucketName",
                        object_key="objectKey"
                    )
                ),
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58d8913ba8a7509519e13822c0e8dd7db9ee38788e1ce2416018f329e4e0d0f)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def criteria(
        self,
    ) -> typing.Union[CfnAllowList.CriteriaProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The criteria that specify the text or text pattern to ignore.

        The criteria can be the location and name of an Amazon S3 object that lists specific text to ignore ( ``S3WordsList`` ), or a regular expression ( ``Regex`` ) that defines a text pattern to ignore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-allowlist.html#cfn-macie-allowlist-criteria
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(typing.Union[CfnAllowList.CriteriaProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A custom name for the allow list.

        The name can contain 1-128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-allowlist.html#cfn-macie-allowlist-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the allow list.

        The description can contain 1-512 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-allowlist.html#cfn-macie-allowlist-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to the allow list.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-allowlist.html#cfn-macie-allowlist-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAllowListProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCustomDataIdentifier(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-macie.CfnCustomDataIdentifier",
):
    '''A CloudFormation ``AWS::Macie::CustomDataIdentifier``.

    The ``AWS::Macie::CustomDataIdentifier`` resource specifies a custom data identifier. A *custom data identifier* is a set of custom criteria for Amazon Macie to use when it inspects data sources for sensitive data. The criteria consist of a regular expression ( *regex* ) that defines a text pattern to match and, optionally, character sequences and a proximity rule that refine the results. The character sequences can be:

    - *Keywords* , which are words or phrases that must be in proximity of text that matches the regex, or
    - *Ignore words* , which are words or phrases to exclude from the results.

    By using custom data identifiers, you can supplement the managed data identifiers that Macie provides and detect sensitive data that reflects your particular scenarios, intellectual property, or proprietary data. For more information, see `Building custom data identifiers <https://docs.aws.amazon.com/macie/latest/user/custom-data-identifiers.html>`_ in the *Amazon Macie User Guide* .

    An ``AWS::Macie::Session`` resource must exist for an AWS account before you can create an ``AWS::Macie::CustomDataIdentifier`` resource for the account. Use a `DependsOn attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ to ensure that an ``AWS::Macie::Session`` resource is created before other Macie resources are created for an account. For example, ``"DependsOn": "Session"`` .

    :cloudformationResource: AWS::Macie::CustomDataIdentifier
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_macie as macie
        
        cfn_custom_data_identifier = macie.CfnCustomDataIdentifier(self, "MyCfnCustomDataIdentifier",
            name="name",
            regex="regex",
        
            # the properties below are optional
            description="description",
            ignore_words=["ignoreWords"],
            keywords=["keywords"],
            maximum_match_distance=123
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        regex: builtins.str,
        description: typing.Optional[builtins.str] = None,
        ignore_words: typing.Optional[typing.Sequence[builtins.str]] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        maximum_match_distance: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::Macie::CustomDataIdentifier``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A custom name for the custom data identifier. The name can contain 1-128 characters. Avoid including sensitive data in the name of a custom data identifier. Users of the account might be able to see the name, depending on the actions that they're allowed to perform in Amazon Macie .
        :param regex: The regular expression ( *regex* ) that defines the text pattern to match. The expression can contain 1-512 characters.
        :param description: A custom description of the custom data identifier. The description can contain 1-512 characters. Avoid including sensitive data in the description. Users of the account might be able to see the description, depending on the actions that they're allowed to perform in Amazon Macie .
        :param ignore_words: An array of character sequences ( *ignore words* ) to exclude from the results. If text matches the regular expression ( ``Regex`` ) but it contains a string in this array, Amazon Macie ignores the text and doesn't include it in the results. The array can contain 1-10 ignore words. Each ignore word can contain 4-90 UTF-8 characters. Ignore words are case sensitive.
        :param keywords: An array of character sequences ( *keywords* ), one of which must precede and be in proximity ( ``MaximumMatchDistance`` ) of the regular expression ( ``Regex`` ) to match. The array can contain 1-50 keywords. Each keyword can contain 3-90 UTF-8 characters. Keywords aren't case sensitive.
        :param maximum_match_distance: The maximum number of characters that can exist between the end of at least one complete character sequence specified by the ``Keywords`` array and the end of text that matches the regular expression ( ``Regex`` ). If a complete keyword precedes all the text that matches the regular expression and the keyword is within the specified distance, Amazon Macie includes the result. The distance can be 1-300 characters. The default value is 50.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ebfbb72b7660862fea4775332c253283ef76d1fdd2bf6a52971e20536b57759)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCustomDataIdentifierProps(
            name=name,
            regex=regex,
            description=description,
            ignore_words=ignore_words,
            keywords=keywords,
            maximum_match_distance=maximum_match_distance,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da76827dd5acc2bdb4e71b27a860bb6d7620de6eb6ac42741764bc9082423e4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f271d9b4e7e46bbf5cb470f99ed8b6c256438e7557a85570873f772db183f6a4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the custom data identifier.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The unique identifier for the custom data identifier.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A custom name for the custom data identifier. The name can contain 1-128 characters.

        Avoid including sensitive data in the name of a custom data identifier. Users of the account might be able to see the name, depending on the actions that they're allowed to perform in Amazon Macie .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dde24b9bcbb30e5eecdee101e7ac3c6036633a96a2c04a65a249738e7fd4a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        '''The regular expression ( *regex* ) that defines the text pattern to match.

        The expression can contain 1-512 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-regex
        '''
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2b0d7f9daa3c5bbc27e6ac01073798a0644191bcd1b6354b58e33898c5ee91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the custom data identifier. The description can contain 1-512 characters.

        Avoid including sensitive data in the description. Users of the account might be able to see the description, depending on the actions that they're allowed to perform in Amazon Macie .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62273c6bb7975450e05119ba8677a33b9a90766a3503fd462c4dd82e2748167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreWords")
    def ignore_words(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of character sequences ( *ignore words* ) to exclude from the results.

        If text matches the regular expression ( ``Regex`` ) but it contains a string in this array, Amazon Macie ignores the text and doesn't include it in the results.

        The array can contain 1-10 ignore words. Each ignore word can contain 4-90 UTF-8 characters. Ignore words are case sensitive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-ignorewords
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ignoreWords"))

    @ignore_words.setter
    def ignore_words(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9719ff39cfadeeff7f90d458ed2e77976577c05b0c31222c41e1442ef187b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreWords", value)

    @builtins.property
    @jsii.member(jsii_name="keywords")
    def keywords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of character sequences ( *keywords* ), one of which must precede and be in proximity ( ``MaximumMatchDistance`` ) of the regular expression ( ``Regex`` ) to match.

        The array can contain 1-50 keywords. Each keyword can contain 3-90 UTF-8 characters. Keywords aren't case sensitive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-keywords
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keywords"))

    @keywords.setter
    def keywords(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3309c5a1290d62709cea89929d1175596fa3b0557c175d878012f82f8a836650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keywords", value)

    @builtins.property
    @jsii.member(jsii_name="maximumMatchDistance")
    def maximum_match_distance(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of characters that can exist between the end of at least one complete character sequence specified by the ``Keywords`` array and the end of text that matches the regular expression ( ``Regex`` ).

        If a complete keyword precedes all the text that matches the regular expression and the keyword is within the specified distance, Amazon Macie includes the result.

        The distance can be 1-300 characters. The default value is 50.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-maximummatchdistance
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumMatchDistance"))

    @maximum_match_distance.setter
    def maximum_match_distance(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4daeaa44fe130a04a736bd1bd3c848e594e29ddb2d152112c849a60a25ad31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumMatchDistance", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-macie.CfnCustomDataIdentifierProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "regex": "regex",
        "description": "description",
        "ignore_words": "ignoreWords",
        "keywords": "keywords",
        "maximum_match_distance": "maximumMatchDistance",
    },
)
class CfnCustomDataIdentifierProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        regex: builtins.str,
        description: typing.Optional[builtins.str] = None,
        ignore_words: typing.Optional[typing.Sequence[builtins.str]] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        maximum_match_distance: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``CfnCustomDataIdentifier``.

        :param name: A custom name for the custom data identifier. The name can contain 1-128 characters. Avoid including sensitive data in the name of a custom data identifier. Users of the account might be able to see the name, depending on the actions that they're allowed to perform in Amazon Macie .
        :param regex: The regular expression ( *regex* ) that defines the text pattern to match. The expression can contain 1-512 characters.
        :param description: A custom description of the custom data identifier. The description can contain 1-512 characters. Avoid including sensitive data in the description. Users of the account might be able to see the description, depending on the actions that they're allowed to perform in Amazon Macie .
        :param ignore_words: An array of character sequences ( *ignore words* ) to exclude from the results. If text matches the regular expression ( ``Regex`` ) but it contains a string in this array, Amazon Macie ignores the text and doesn't include it in the results. The array can contain 1-10 ignore words. Each ignore word can contain 4-90 UTF-8 characters. Ignore words are case sensitive.
        :param keywords: An array of character sequences ( *keywords* ), one of which must precede and be in proximity ( ``MaximumMatchDistance`` ) of the regular expression ( ``Regex`` ) to match. The array can contain 1-50 keywords. Each keyword can contain 3-90 UTF-8 characters. Keywords aren't case sensitive.
        :param maximum_match_distance: The maximum number of characters that can exist between the end of at least one complete character sequence specified by the ``Keywords`` array and the end of text that matches the regular expression ( ``Regex`` ). If a complete keyword precedes all the text that matches the regular expression and the keyword is within the specified distance, Amazon Macie includes the result. The distance can be 1-300 characters. The default value is 50.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_macie as macie
            
            cfn_custom_data_identifier_props = macie.CfnCustomDataIdentifierProps(
                name="name",
                regex="regex",
            
                # the properties below are optional
                description="description",
                ignore_words=["ignoreWords"],
                keywords=["keywords"],
                maximum_match_distance=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b6735142bcacaa789882c384e72aeae768e766c8f3f583e4c5e9099d2e4fef)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ignore_words", value=ignore_words, expected_type=type_hints["ignore_words"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument maximum_match_distance", value=maximum_match_distance, expected_type=type_hints["maximum_match_distance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "regex": regex,
        }
        if description is not None:
            self._values["description"] = description
        if ignore_words is not None:
            self._values["ignore_words"] = ignore_words
        if keywords is not None:
            self._values["keywords"] = keywords
        if maximum_match_distance is not None:
            self._values["maximum_match_distance"] = maximum_match_distance

    @builtins.property
    def name(self) -> builtins.str:
        '''A custom name for the custom data identifier. The name can contain 1-128 characters.

        Avoid including sensitive data in the name of a custom data identifier. Users of the account might be able to see the name, depending on the actions that they're allowed to perform in Amazon Macie .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex(self) -> builtins.str:
        '''The regular expression ( *regex* ) that defines the text pattern to match.

        The expression can contain 1-512 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-regex
        '''
        result = self._values.get("regex")
        assert result is not None, "Required property 'regex' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the custom data identifier. The description can contain 1-512 characters.

        Avoid including sensitive data in the description. Users of the account might be able to see the description, depending on the actions that they're allowed to perform in Amazon Macie .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_words(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of character sequences ( *ignore words* ) to exclude from the results.

        If text matches the regular expression ( ``Regex`` ) but it contains a string in this array, Amazon Macie ignores the text and doesn't include it in the results.

        The array can contain 1-10 ignore words. Each ignore word can contain 4-90 UTF-8 characters. Ignore words are case sensitive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-ignorewords
        '''
        result = self._values.get("ignore_words")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def keywords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of character sequences ( *keywords* ), one of which must precede and be in proximity ( ``MaximumMatchDistance`` ) of the regular expression ( ``Regex`` ) to match.

        The array can contain 1-50 keywords. Each keyword can contain 3-90 UTF-8 characters. Keywords aren't case sensitive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-keywords
        '''
        result = self._values.get("keywords")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def maximum_match_distance(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of characters that can exist between the end of at least one complete character sequence specified by the ``Keywords`` array and the end of text that matches the regular expression ( ``Regex`` ).

        If a complete keyword precedes all the text that matches the regular expression and the keyword is within the specified distance, Amazon Macie includes the result.

        The distance can be 1-300 characters. The default value is 50.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-maximummatchdistance
        '''
        result = self._values.get("maximum_match_distance")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomDataIdentifierProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFindingsFilter(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-macie.CfnFindingsFilter",
):
    '''A CloudFormation ``AWS::Macie::FindingsFilter``.

    The ``AWS::Macie::FindingsFilter`` resource specifies a findings filter. In Amazon Macie , a *findings filter* , also referred to as a *filter rule* , is a set of custom criteria that specifies which findings to include or exclude from the results of a query for findings. The criteria can help you identify and focus on findings that have specific characteristics, such as severity, type, or the name of an affected AWS resource. You can also configure a findings filter to suppress (automatically archive) findings that match the filter's criteria. For more information, see `Filtering findings <https://docs.aws.amazon.com/macie/latest/user/findings-filter-overview.html>`_ in the *Amazon Macie User Guide* .

    An ``AWS::Macie::Session`` resource must exist for an AWS account before you can create an ``AWS::Macie::FindingsFilter`` resource for the account. Use a `DependsOn attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ to ensure that an ``AWS::Macie::Session`` resource is created before other Macie resources are created for an account. For example, ``"DependsOn": "Session"`` .

    :cloudformationResource: AWS::Macie::FindingsFilter
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_macie as macie
        
        cfn_findings_filter = macie.CfnFindingsFilter(self, "MyCfnFindingsFilter",
            finding_criteria=macie.CfnFindingsFilter.FindingCriteriaProperty(
                criterion={
                    "criterion_key": macie.CfnFindingsFilter.CriterionAdditionalPropertiesProperty(
                        eq=["eq"],
                        gt=123,
                        gte=123,
                        lt=123,
                        lte=123,
                        neq=["neq"]
                    )
                }
            ),
            name="name",
        
            # the properties below are optional
            action="action",
            description="description",
            position=123
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        finding_criteria: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFindingsFilter.FindingCriteriaProperty", typing.Dict[builtins.str, typing.Any]]],
        name: builtins.str,
        action: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        position: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::Macie::FindingsFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param finding_criteria: The criteria to use to filter findings.
        :param name: A custom name for the findings filter. The name can contain 3-64 characters. Avoid including sensitive data in the name. Users of the account might be able to see the name, depending on the actions that they're allowed to perform in Amazon Macie .
        :param action: The action to perform on findings that match the filter criteria ( ``FindingCriteria`` ). Valid values are:. - ``ARCHIVE`` - Suppress (automatically archive) the findings. - ``NOOP`` - Don't perform any action on the findings.
        :param description: A custom description of the findings filter. The description can contain 1-512 characters. Avoid including sensitive data in the description. Users of the account might be able to see the description, depending on the actions that they're allowed to perform in Amazon Macie .
        :param position: The position of the findings filter in the list of saved filters on the Amazon Macie console. This value also determines the order in which the filter is applied to findings, relative to other filters that are also applied to findings.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abbc60bb254d59e9553dd9c8df1745b1a997f30c8166193f6f4ecbf7e032d81c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFindingsFilterProps(
            finding_criteria=finding_criteria,
            name=name,
            action=action,
            description=description,
            position=position,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c1177e3b90eeffaf77428a3df777251354dac1b35a62c7f48230365f8fb3b16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29eeb11c7c2256493b3b9aa46bf6e36a04f5c53cb4cd9be10db76c06428cae04)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the findings filter.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrFindingsFilterListItems")
    def attr_findings_filter_list_items(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''An array of ``FindingsFilterListItem`` objects, one for each findings filter that's associated with the account.

        :cloudformationAttribute: FindingsFilterListItems
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrFindingsFilterListItems"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The unique identifier for the findings filter.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="findingCriteria")
    def finding_criteria(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFindingsFilter.FindingCriteriaProperty"]:
        '''The criteria to use to filter findings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-findingcriteria
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFindingsFilter.FindingCriteriaProperty"], jsii.get(self, "findingCriteria"))

    @finding_criteria.setter
    def finding_criteria(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFindingsFilter.FindingCriteriaProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af0604d2361c3b11d37674f66d55bdba5e5b94399ffca1a8d53eb9e17f2c62f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "findingCriteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A custom name for the findings filter. The name can contain 3-64 characters.

        Avoid including sensitive data in the name. Users of the account might be able to see the name, depending on the actions that they're allowed to perform in Amazon Macie .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d766ea1f0d0a012466f1d09cdcee8c2254da13b6fef87061b0bb5d4b29381c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> typing.Optional[builtins.str]:
        '''The action to perform on findings that match the filter criteria ( ``FindingCriteria`` ). Valid values are:.

        - ``ARCHIVE`` - Suppress (automatically archive) the findings.
        - ``NOOP`` - Don't perform any action on the findings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-action
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "action"))

    @action.setter
    def action(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310d09b403bcd150057929d0470f1b45ae3a978058d70ccd073568481c10b67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the findings filter. The description can contain 1-512 characters.

        Avoid including sensitive data in the description. Users of the account might be able to see the description, depending on the actions that they're allowed to perform in Amazon Macie .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5fb1620049f3d24f8f1319ff0da489b02ab55b47b901dc445858d82d68511b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> typing.Optional[jsii.Number]:
        '''The position of the findings filter in the list of saved filters on the Amazon Macie console.

        This value also determines the order in which the filter is applied to findings, relative to other filters that are also applied to findings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-position
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "position"))

    @position.setter
    def position(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2514b379e98377b57ddb05f12c2eda062a53195cf18bb34e4509d57696ba46bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "position", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-macie.CfnFindingsFilter.CriterionAdditionalPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "eq": "eq",
            "gt": "gt",
            "gte": "gte",
            "lt": "lt",
            "lte": "lte",
            "neq": "neq",
        },
    )
    class CriterionAdditionalPropertiesProperty:
        def __init__(
            self,
            *,
            eq: typing.Optional[typing.Sequence[builtins.str]] = None,
            gt: typing.Optional[jsii.Number] = None,
            gte: typing.Optional[jsii.Number] = None,
            lt: typing.Optional[jsii.Number] = None,
            lte: typing.Optional[jsii.Number] = None,
            neq: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param eq: ``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.eq``.
            :param gt: ``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.gt``.
            :param gte: ``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.gte``.
            :param lt: ``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.lt``.
            :param lte: ``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.lte``.
            :param neq: ``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.neq``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-criterionadditionalproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_macie as macie
                
                criterion_additional_properties_property = macie.CfnFindingsFilter.CriterionAdditionalPropertiesProperty(
                    eq=["eq"],
                    gt=123,
                    gte=123,
                    lt=123,
                    lte=123,
                    neq=["neq"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b388e75d196e7858448de19437fc6f0ac1e5b84e49daafa3884f258e3391b531)
                check_type(argname="argument eq", value=eq, expected_type=type_hints["eq"])
                check_type(argname="argument gt", value=gt, expected_type=type_hints["gt"])
                check_type(argname="argument gte", value=gte, expected_type=type_hints["gte"])
                check_type(argname="argument lt", value=lt, expected_type=type_hints["lt"])
                check_type(argname="argument lte", value=lte, expected_type=type_hints["lte"])
                check_type(argname="argument neq", value=neq, expected_type=type_hints["neq"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if eq is not None:
                self._values["eq"] = eq
            if gt is not None:
                self._values["gt"] = gt
            if gte is not None:
                self._values["gte"] = gte
            if lt is not None:
                self._values["lt"] = lt
            if lte is not None:
                self._values["lte"] = lte
            if neq is not None:
                self._values["neq"] = neq

        @builtins.property
        def eq(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.eq``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-criterionadditionalproperties.html#cfn-macie-findingsfilter-criterionadditionalproperties-eq
            '''
            result = self._values.get("eq")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def gt(self) -> typing.Optional[jsii.Number]:
            '''``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.gt``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-criterionadditionalproperties.html#cfn-macie-findingsfilter-criterionadditionalproperties-gt
            '''
            result = self._values.get("gt")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gte(self) -> typing.Optional[jsii.Number]:
            '''``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.gte``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-criterionadditionalproperties.html#cfn-macie-findingsfilter-criterionadditionalproperties-gte
            '''
            result = self._values.get("gte")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lt(self) -> typing.Optional[jsii.Number]:
            '''``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.lt``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-criterionadditionalproperties.html#cfn-macie-findingsfilter-criterionadditionalproperties-lt
            '''
            result = self._values.get("lt")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def lte(self) -> typing.Optional[jsii.Number]:
            '''``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.lte``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-criterionadditionalproperties.html#cfn-macie-findingsfilter-criterionadditionalproperties-lte
            '''
            result = self._values.get("lte")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def neq(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFindingsFilter.CriterionAdditionalPropertiesProperty.neq``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-criterionadditionalproperties.html#cfn-macie-findingsfilter-criterionadditionalproperties-neq
            '''
            result = self._values.get("neq")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CriterionAdditionalPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-macie.CfnFindingsFilter.FindingCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"criterion": "criterion"},
    )
    class FindingCriteriaProperty:
        def __init__(
            self,
            *,
            criterion: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFindingsFilter.CriterionAdditionalPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies, as a map, one or more property-based conditions that filter the results of a query for findings.

            For more information, see `Filtering findings <https://docs.aws.amazon.com/macie/latest/user/findings-filter-overview.html>`_ in the *Amazon Macie User Guide* .

            :param criterion: Specifies a condition that defines the property, operator, and one or more values to use to filter the results.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-findingcriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_macie as macie
                
                finding_criteria_property = macie.CfnFindingsFilter.FindingCriteriaProperty(
                    criterion={
                        "criterion_key": macie.CfnFindingsFilter.CriterionAdditionalPropertiesProperty(
                            eq=["eq"],
                            gt=123,
                            gte=123,
                            lt=123,
                            lte=123,
                            neq=["neq"]
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5e010fa9ca03a748a20a09717aad1cc6a344cb0c65ba6fc6c59f9b46838caa0)
                check_type(argname="argument criterion", value=criterion, expected_type=type_hints["criterion"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if criterion is not None:
                self._values["criterion"] = criterion

        @builtins.property
        def criterion(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFindingsFilter.CriterionAdditionalPropertiesProperty"]]]]:
            '''Specifies a condition that defines the property, operator, and one or more values to use to filter the results.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-findingcriteria.html#cfn-macie-findingsfilter-findingcriteria-criterion
            '''
            result = self._values.get("criterion")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFindingsFilter.CriterionAdditionalPropertiesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FindingCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-macie.CfnFindingsFilter.FindingsFilterListItemProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "name": "name"},
    )
    class FindingsFilterListItemProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the unique identifier and custom name of a findings filter.

            :param id: The unique identifier for the findings filter.
            :param name: The custom name of the findings filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-findingsfilterlistitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_macie as macie
                
                findings_filter_list_item_property = macie.CfnFindingsFilter.FindingsFilterListItemProperty(
                    id="id",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__192e9204b1256ff1c14d76fc1a29478e66aa376bf6453b2e443da65d834b1aab)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the findings filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-findingsfilterlistitem.html#cfn-macie-findingsfilter-findingsfilterlistitem-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The custom name of the findings filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-findingsfilterlistitem.html#cfn-macie-findingsfilter-findingsfilterlistitem-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FindingsFilterListItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-macie.CfnFindingsFilterProps",
    jsii_struct_bases=[],
    name_mapping={
        "finding_criteria": "findingCriteria",
        "name": "name",
        "action": "action",
        "description": "description",
        "position": "position",
    },
)
class CfnFindingsFilterProps:
    def __init__(
        self,
        *,
        finding_criteria: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFindingsFilter.FindingCriteriaProperty, typing.Dict[builtins.str, typing.Any]]],
        name: builtins.str,
        action: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        position: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``CfnFindingsFilter``.

        :param finding_criteria: The criteria to use to filter findings.
        :param name: A custom name for the findings filter. The name can contain 3-64 characters. Avoid including sensitive data in the name. Users of the account might be able to see the name, depending on the actions that they're allowed to perform in Amazon Macie .
        :param action: The action to perform on findings that match the filter criteria ( ``FindingCriteria`` ). Valid values are:. - ``ARCHIVE`` - Suppress (automatically archive) the findings. - ``NOOP`` - Don't perform any action on the findings.
        :param description: A custom description of the findings filter. The description can contain 1-512 characters. Avoid including sensitive data in the description. Users of the account might be able to see the description, depending on the actions that they're allowed to perform in Amazon Macie .
        :param position: The position of the findings filter in the list of saved filters on the Amazon Macie console. This value also determines the order in which the filter is applied to findings, relative to other filters that are also applied to findings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_macie as macie
            
            cfn_findings_filter_props = macie.CfnFindingsFilterProps(
                finding_criteria=macie.CfnFindingsFilter.FindingCriteriaProperty(
                    criterion={
                        "criterion_key": macie.CfnFindingsFilter.CriterionAdditionalPropertiesProperty(
                            eq=["eq"],
                            gt=123,
                            gte=123,
                            lt=123,
                            lte=123,
                            neq=["neq"]
                        )
                    }
                ),
                name="name",
            
                # the properties below are optional
                action="action",
                description="description",
                position=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82ebd8b1d5573150770342b6dc666c3045ba280fcb9afbf16ecc0490c80038d)
            check_type(argname="argument finding_criteria", value=finding_criteria, expected_type=type_hints["finding_criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument position", value=position, expected_type=type_hints["position"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "finding_criteria": finding_criteria,
            "name": name,
        }
        if action is not None:
            self._values["action"] = action
        if description is not None:
            self._values["description"] = description
        if position is not None:
            self._values["position"] = position

    @builtins.property
    def finding_criteria(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFindingsFilter.FindingCriteriaProperty]:
        '''The criteria to use to filter findings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-findingcriteria
        '''
        result = self._values.get("finding_criteria")
        assert result is not None, "Required property 'finding_criteria' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFindingsFilter.FindingCriteriaProperty], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A custom name for the findings filter. The name can contain 3-64 characters.

        Avoid including sensitive data in the name. Users of the account might be able to see the name, depending on the actions that they're allowed to perform in Amazon Macie .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The action to perform on findings that match the filter criteria ( ``FindingCriteria`` ). Valid values are:.

        - ``ARCHIVE`` - Suppress (automatically archive) the findings.
        - ``NOOP`` - Don't perform any action on the findings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A custom description of the findings filter. The description can contain 1-512 characters.

        Avoid including sensitive data in the description. Users of the account might be able to see the description, depending on the actions that they're allowed to perform in Amazon Macie .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def position(self) -> typing.Optional[jsii.Number]:
        '''The position of the findings filter in the list of saved filters on the Amazon Macie console.

        This value also determines the order in which the filter is applied to findings, relative to other filters that are also applied to findings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-position
        '''
        result = self._values.get("position")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFindingsFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSession(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-macie.CfnSession",
):
    '''A CloudFormation ``AWS::Macie::Session``.

    The ``AWS::Macie::Session`` resource represents the Amazon Macie service and certain configuration settings for an Amazon Macie account in a specific AWS Region . It enables Macie to become operational for a specific account in a specific Region. An account can have only one session in each Region.

    You must create an ``AWS::Macie::Session`` resource for an account before you can create other types of resources for the account. Use a `DependsOn attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ to ensure that an ``AWS::Macie::Session`` resource is created before other Macie resources are created for an account. For example, ``"DependsOn": "Session"`` .

    :cloudformationResource: AWS::Macie::Session
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_macie as macie
        
        cfn_session = macie.CfnSession(self, "MyCfnSession",
            finding_publishing_frequency="findingPublishingFrequency",
            status="status"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        finding_publishing_frequency: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Macie::Session``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param finding_publishing_frequency: Specifies how often Amazon Macie publishes updates to policy findings for the account. This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly Amazon CloudWatch Events ). Valid values are: - FIFTEEN_MINUTES - ONE_HOUR - SIX_HOURS
        :param status: The status of Amazon Macie for the account. Valid values are: ``ENABLED`` , start or resume all Macie activities for the account; and, ``PAUSED`` , suspend all Macie activities for the account.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a120b555fad2d26c72c1960084943bd04669e088a9ca190978c7b7b0bc46d6e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSessionProps(
            finding_publishing_frequency=finding_publishing_frequency, status=status
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c8e2db695bd324850764ebc7b91adc396df569fce04e472baf9e98e067decb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8be6b425f1b3254e5d1e13ae4153c3683eae9ca5e828e2357ff7ec5258eeaeb3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAwsAccountId")
    def attr_aws_account_id(self) -> builtins.str:
        '''The account ID for the AWS account in which the Amazon Macie session is created.

        :cloudformationAttribute: AwsAccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAwsAccountId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceRole")
    def attr_service_role(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the service-linked role that allows Amazon Macie to monitor and analyze data in AWS resources for the account.

        :cloudformationAttribute: ServiceRole
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceRole"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="findingPublishingFrequency")
    def finding_publishing_frequency(self) -> typing.Optional[builtins.str]:
        '''Specifies how often Amazon Macie publishes updates to policy findings for the account.

        This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly Amazon CloudWatch Events ). Valid values are:

        - FIFTEEN_MINUTES
        - ONE_HOUR
        - SIX_HOURS

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html#cfn-macie-session-findingpublishingfrequency
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "findingPublishingFrequency"))

    @finding_publishing_frequency.setter
    def finding_publishing_frequency(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c89b791f03e46e5abc0fe1d048721a7df9d166cf993d3a9d4bb4ae90d9fa0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "findingPublishingFrequency", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of Amazon Macie for the account.

        Valid values are: ``ENABLED`` , start or resume all Macie activities for the account; and, ``PAUSED`` , suspend all Macie activities for the account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html#cfn-macie-session-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348fe0daf9fe9a524bc31e37850dfbee414b475472bdfd88192797f6b6971291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-macie.CfnSessionProps",
    jsii_struct_bases=[],
    name_mapping={
        "finding_publishing_frequency": "findingPublishingFrequency",
        "status": "status",
    },
)
class CfnSessionProps:
    def __init__(
        self,
        *,
        finding_publishing_frequency: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSession``.

        :param finding_publishing_frequency: Specifies how often Amazon Macie publishes updates to policy findings for the account. This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly Amazon CloudWatch Events ). Valid values are: - FIFTEEN_MINUTES - ONE_HOUR - SIX_HOURS
        :param status: The status of Amazon Macie for the account. Valid values are: ``ENABLED`` , start or resume all Macie activities for the account; and, ``PAUSED`` , suspend all Macie activities for the account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_macie as macie
            
            cfn_session_props = macie.CfnSessionProps(
                finding_publishing_frequency="findingPublishingFrequency",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060b047d37c195a710501713918993ba73f58b84132889e216919530739254e6)
            check_type(argname="argument finding_publishing_frequency", value=finding_publishing_frequency, expected_type=type_hints["finding_publishing_frequency"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if finding_publishing_frequency is not None:
            self._values["finding_publishing_frequency"] = finding_publishing_frequency
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def finding_publishing_frequency(self) -> typing.Optional[builtins.str]:
        '''Specifies how often Amazon Macie publishes updates to policy findings for the account.

        This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly Amazon CloudWatch Events ). Valid values are:

        - FIFTEEN_MINUTES
        - ONE_HOUR
        - SIX_HOURS

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html#cfn-macie-session-findingpublishingfrequency
        '''
        result = self._values.get("finding_publishing_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of Amazon Macie for the account.

        Valid values are: ``ENABLED`` , start or resume all Macie activities for the account; and, ``PAUSED`` , suspend all Macie activities for the account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html#cfn-macie-session-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSessionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAllowList",
    "CfnAllowListProps",
    "CfnCustomDataIdentifier",
    "CfnCustomDataIdentifierProps",
    "CfnFindingsFilter",
    "CfnFindingsFilterProps",
    "CfnSession",
    "CfnSessionProps",
]

publication.publish()

def _typecheckingstub__97dd8f9de24502693512247a15acf868ef9ef512cf75e3ccdc87bc15bb53d690(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    criteria: typing.Union[typing.Union[CfnAllowList.CriteriaProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4721b70f482d51384dccc06621eb481a9b32e91dd8d409192642431b9972248f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4a448000cdacf9c97a2df5a143ba12aaae0db801a1834ed18abc2c3a910380(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a82cc0776cfdb1c16791a2bf50700a4ab51f191dcd52bf48483b33029c2c58(
    value: typing.Union[CfnAllowList.CriteriaProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c736883bc58756ce664cf6ac61e82ba58514919f6bf93c21efc5230fbf6b9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9362298689ec96e92f699d9949825c9b1a474c9c74bbb804ea9f6d278775753(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a4eb646199e38fcd3a9e6a39eafb4d418c8e7b0f9cde9537efb137423be979(
    *,
    regex: typing.Optional[builtins.str] = None,
    s3_words_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAllowList.S3WordsListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03463a9c7b7d0ae41b5429f53ac214667de8976d3f13d8f2ffafe6cc892c5d4(
    *,
    bucket_name: builtins.str,
    object_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58d8913ba8a7509519e13822c0e8dd7db9ee38788e1ce2416018f329e4e0d0f(
    *,
    criteria: typing.Union[typing.Union[CfnAllowList.CriteriaProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebfbb72b7660862fea4775332c253283ef76d1fdd2bf6a52971e20536b57759(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    regex: builtins.str,
    description: typing.Optional[builtins.str] = None,
    ignore_words: typing.Optional[typing.Sequence[builtins.str]] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_match_distance: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da76827dd5acc2bdb4e71b27a860bb6d7620de6eb6ac42741764bc9082423e4c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f271d9b4e7e46bbf5cb470f99ed8b6c256438e7557a85570873f772db183f6a4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dde24b9bcbb30e5eecdee101e7ac3c6036633a96a2c04a65a249738e7fd4a87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2b0d7f9daa3c5bbc27e6ac01073798a0644191bcd1b6354b58e33898c5ee91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62273c6bb7975450e05119ba8677a33b9a90766a3503fd462c4dd82e2748167(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9719ff39cfadeeff7f90d458ed2e77976577c05b0c31222c41e1442ef187b84(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3309c5a1290d62709cea89929d1175596fa3b0557c175d878012f82f8a836650(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4daeaa44fe130a04a736bd1bd3c848e594e29ddb2d152112c849a60a25ad31(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b6735142bcacaa789882c384e72aeae768e766c8f3f583e4c5e9099d2e4fef(
    *,
    name: builtins.str,
    regex: builtins.str,
    description: typing.Optional[builtins.str] = None,
    ignore_words: typing.Optional[typing.Sequence[builtins.str]] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_match_distance: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbc60bb254d59e9553dd9c8df1745b1a997f30c8166193f6f4ecbf7e032d81c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    finding_criteria: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFindingsFilter.FindingCriteriaProperty, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    action: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    position: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1177e3b90eeffaf77428a3df777251354dac1b35a62c7f48230365f8fb3b16(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29eeb11c7c2256493b3b9aa46bf6e36a04f5c53cb4cd9be10db76c06428cae04(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af0604d2361c3b11d37674f66d55bdba5e5b94399ffca1a8d53eb9e17f2c62f(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFindingsFilter.FindingCriteriaProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d766ea1f0d0a012466f1d09cdcee8c2254da13b6fef87061b0bb5d4b29381c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310d09b403bcd150057929d0470f1b45ae3a978058d70ccd073568481c10b67e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5fb1620049f3d24f8f1319ff0da489b02ab55b47b901dc445858d82d68511b8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2514b379e98377b57ddb05f12c2eda062a53195cf18bb34e4509d57696ba46bc(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b388e75d196e7858448de19437fc6f0ac1e5b84e49daafa3884f258e3391b531(
    *,
    eq: typing.Optional[typing.Sequence[builtins.str]] = None,
    gt: typing.Optional[jsii.Number] = None,
    gte: typing.Optional[jsii.Number] = None,
    lt: typing.Optional[jsii.Number] = None,
    lte: typing.Optional[jsii.Number] = None,
    neq: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e010fa9ca03a748a20a09717aad1cc6a344cb0c65ba6fc6c59f9b46838caa0(
    *,
    criterion: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFindingsFilter.CriterionAdditionalPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192e9204b1256ff1c14d76fc1a29478e66aa376bf6453b2e443da65d834b1aab(
    *,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82ebd8b1d5573150770342b6dc666c3045ba280fcb9afbf16ecc0490c80038d(
    *,
    finding_criteria: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFindingsFilter.FindingCriteriaProperty, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    action: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    position: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a120b555fad2d26c72c1960084943bd04669e088a9ca190978c7b7b0bc46d6e7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    finding_publishing_frequency: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c8e2db695bd324850764ebc7b91adc396df569fce04e472baf9e98e067decb(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be6b425f1b3254e5d1e13ae4153c3683eae9ca5e828e2357ff7ec5258eeaeb3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c89b791f03e46e5abc0fe1d048721a7df9d166cf993d3a9d4bb4ae90d9fa0b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348fe0daf9fe9a524bc31e37850dfbee414b475472bdfd88192797f6b6971291(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060b047d37c195a710501713918993ba73f58b84132889e216919530739254e6(
    *,
    finding_publishing_frequency: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
