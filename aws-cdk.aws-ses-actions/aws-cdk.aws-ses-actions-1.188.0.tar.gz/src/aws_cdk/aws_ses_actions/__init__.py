'''
# Amazon Simple Email Service Actions Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module contains integration classes to add action to SES email receiving rules.
Instances of these classes should be passed to the `rule.addAction()` method.

Currently supported are:

* [Add header](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-add-header.html)
* [Bounce](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-bounce.html)
* [Lambda](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-lambda.html)
* [S3](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-s3.html)
* [SNS](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-sns.html)
* [Stop](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-stop.html)

See the README of `@aws-cdk/aws-ses` for more information.
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

import aws_cdk.aws_kms as _aws_cdk_aws_kms_e491a92b
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_5443dbc3
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_55f001a5
import aws_cdk.aws_ses as _aws_cdk_aws_ses_b8f9c394
import aws_cdk.aws_sns as _aws_cdk_aws_sns_889c7272


@jsii.implements(_aws_cdk_aws_ses_b8f9c394.IReceiptRuleAction)
class AddHeader(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses-actions.AddHeader",
):
    '''Adds a header to the received email.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_s3 as s3
        import aws_cdk.aws_ses_actions as actions
        
        
        bucket = s3.Bucket(self, "Bucket")
        topic = sns.Topic(self, "Topic")
        
        ses.ReceiptRuleSet(self, "RuleSet",
            rules=[ses.ReceiptRuleOptions(
                recipients=["hello@aws.com"],
                actions=[
                    actions.AddHeader(
                        name="X-Special-Header",
                        value="aws"
                    ),
                    actions.S3(
                        bucket=bucket,
                        object_key_prefix="emails/",
                        topic=topic
                    )
                ]
            ), ses.ReceiptRuleOptions(
                recipients=["aws.com"],
                actions=[
                    actions.Sns(
                        topic=topic
                    )
                ]
            )
            ]
        )
    '''

    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: The name of the header to add. Must be between 1 and 50 characters, inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters and dashes only.
        :param value: The value of the header to add. Must be less than 2048 characters, and must not contain newline characters ("\\r" or "\\n").
        '''
        props = AddHeaderProps(name=name, value=value)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
    ) -> _aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig:
        '''Returns the receipt rule action specification.

        :param _rule: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e62c47a3073f2fa057acf62f9842bd0161c1e30751c3579d931081d0010241)
            check_type(argname="argument _rule", value=_rule, expected_type=type_hints["_rule"])
        return typing.cast(_aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig, jsii.invoke(self, "bind", [_rule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.AddHeaderProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class AddHeaderProps:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''Construction properties for a add header action.

        :param name: The name of the header to add. Must be between 1 and 50 characters, inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters and dashes only.
        :param value: The value of the header to add. Must be less than 2048 characters, and must not contain newline characters ("\\r" or "\\n").

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_s3 as s3
            import aws_cdk.aws_ses_actions as actions
            
            
            bucket = s3.Bucket(self, "Bucket")
            topic = sns.Topic(self, "Topic")
            
            ses.ReceiptRuleSet(self, "RuleSet",
                rules=[ses.ReceiptRuleOptions(
                    recipients=["hello@aws.com"],
                    actions=[
                        actions.AddHeader(
                            name="X-Special-Header",
                            value="aws"
                        ),
                        actions.S3(
                            bucket=bucket,
                            object_key_prefix="emails/",
                            topic=topic
                        )
                    ]
                ), ses.ReceiptRuleOptions(
                    recipients=["aws.com"],
                    actions=[
                        actions.Sns(
                            topic=topic
                        )
                    ]
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7eed0eabb35a3d9510a514abe92497021b023b56ba9682b716fda62d494d90)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the header to add.

        Must be between 1 and 50 characters,
        inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters
        and dashes only.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the header to add.

        Must be less than 2048 characters,
        and must not contain newline characters ("\\r" or "\\n").
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddHeaderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ses_b8f9c394.IReceiptRuleAction)
class Bounce(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses-actions.Bounce"):
    '''Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon SNS.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses_actions as ses_actions
        import aws_cdk.aws_sns as sns
        
        # bounce_template: ses_actions.BounceTemplate
        # topic: sns.Topic
        
        bounce = ses_actions.Bounce(
            sender="sender",
            template=bounce_template,
        
            # the properties below are optional
            topic=topic
        )
    '''

    def __init__(
        self,
        *,
        sender: builtins.str,
        template: "BounceTemplate",
        topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
    ) -> None:
        '''
        :param sender: The email address of the sender of the bounced email. This is the address from which the bounce message will be sent.
        :param template: The template containing the message, reply code and status code.
        :param topic: The SNS topic to notify when the bounce action is taken. Default: no notification
        '''
        props = BounceProps(sender=sender, template=template, topic=topic)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
    ) -> _aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig:
        '''Returns the receipt rule action specification.

        :param _rule: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32785a0b7d9413fe20b4aafc8f06f718ccc235c60f88c5a82ed16f3bcddb38ca)
            check_type(argname="argument _rule", value=_rule, expected_type=type_hints["_rule"])
        return typing.cast(_aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig, jsii.invoke(self, "bind", [_rule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.BounceProps",
    jsii_struct_bases=[],
    name_mapping={"sender": "sender", "template": "template", "topic": "topic"},
)
class BounceProps:
    def __init__(
        self,
        *,
        sender: builtins.str,
        template: "BounceTemplate",
        topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
    ) -> None:
        '''Construction properties for a bounce action.

        :param sender: The email address of the sender of the bounced email. This is the address from which the bounce message will be sent.
        :param template: The template containing the message, reply code and status code.
        :param topic: The SNS topic to notify when the bounce action is taken. Default: no notification

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses_actions as ses_actions
            import aws_cdk.aws_sns as sns
            
            # bounce_template: ses_actions.BounceTemplate
            # topic: sns.Topic
            
            bounce_props = ses_actions.BounceProps(
                sender="sender",
                template=bounce_template,
            
                # the properties below are optional
                topic=topic
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9d72774b8be6e2d2b1f96682e3960356d65ab6320051251a3dfb9b874c5331)
            check_type(argname="argument sender", value=sender, expected_type=type_hints["sender"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sender": sender,
            "template": template,
        }
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def sender(self) -> builtins.str:
        '''The email address of the sender of the bounced email.

        This is the address
        from which the bounce message will be sent.
        '''
        result = self._values.get("sender")
        assert result is not None, "Required property 'sender' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> "BounceTemplate":
        '''The template containing the message, reply code and status code.'''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast("BounceTemplate", result)

    @builtins.property
    def topic(self) -> typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic]:
        '''The SNS topic to notify when the bounce action is taken.

        :default: no notification
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BounceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BounceTemplate(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses-actions.BounceTemplate",
):
    '''A bounce template.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses_actions as ses_actions
        
        bounce_template = ses_actions.BounceTemplate.MAILBOX_DOES_NOT_EXIST
    '''

    def __init__(
        self,
        *,
        message: builtins.str,
        smtp_reply_code: builtins.str,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: Human-readable text to include in the bounce message.
        :param smtp_reply_code: The SMTP reply code, as defined by RFC 5321.
        :param status_code: The SMTP enhanced status code, as defined by RFC 3463.
        '''
        props = BounceTemplateProps(
            message=message, smtp_reply_code=smtp_reply_code, status_code=status_code
        )

        jsii.create(self.__class__, self, [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAILBOX_DOES_NOT_EXIST")
    def MAILBOX_DOES_NOT_EXIST(cls) -> "BounceTemplate":
        return typing.cast("BounceTemplate", jsii.sget(cls, "MAILBOX_DOES_NOT_EXIST"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MAILBOX_FULL")
    def MAILBOX_FULL(cls) -> "BounceTemplate":
        return typing.cast("BounceTemplate", jsii.sget(cls, "MAILBOX_FULL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MESSAGE_CONTENT_REJECTED")
    def MESSAGE_CONTENT_REJECTED(cls) -> "BounceTemplate":
        return typing.cast("BounceTemplate", jsii.sget(cls, "MESSAGE_CONTENT_REJECTED"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MESSAGE_TOO_LARGE")
    def MESSAGE_TOO_LARGE(cls) -> "BounceTemplate":
        return typing.cast("BounceTemplate", jsii.sget(cls, "MESSAGE_TOO_LARGE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TEMPORARY_FAILURE")
    def TEMPORARY_FAILURE(cls) -> "BounceTemplate":
        return typing.cast("BounceTemplate", jsii.sget(cls, "TEMPORARY_FAILURE"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "BounceTemplateProps":
        return typing.cast("BounceTemplateProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.BounceTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "message": "message",
        "smtp_reply_code": "smtpReplyCode",
        "status_code": "statusCode",
    },
)
class BounceTemplateProps:
    def __init__(
        self,
        *,
        message: builtins.str,
        smtp_reply_code: builtins.str,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Construction properties for a BounceTemplate.

        :param message: Human-readable text to include in the bounce message.
        :param smtp_reply_code: The SMTP reply code, as defined by RFC 5321.
        :param status_code: The SMTP enhanced status code, as defined by RFC 3463.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses_actions as ses_actions
            
            bounce_template_props = ses_actions.BounceTemplateProps(
                message="message",
                smtp_reply_code="smtpReplyCode",
            
                # the properties below are optional
                status_code="statusCode"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de96ec77596b08d03d0643fe3d841a0a40bb3f75479fb08bc5fd12b962a04306)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument smtp_reply_code", value=smtp_reply_code, expected_type=type_hints["smtp_reply_code"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message": message,
            "smtp_reply_code": smtp_reply_code,
        }
        if status_code is not None:
            self._values["status_code"] = status_code

    @builtins.property
    def message(self) -> builtins.str:
        '''Human-readable text to include in the bounce message.'''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def smtp_reply_code(self) -> builtins.str:
        '''The SMTP reply code, as defined by RFC 5321.

        :see: https://tools.ietf.org/html/rfc5321
        '''
        result = self._values.get("smtp_reply_code")
        assert result is not None, "Required property 'smtp_reply_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status_code(self) -> typing.Optional[builtins.str]:
        '''The SMTP enhanced status code, as defined by RFC 3463.

        :see: https://tools.ietf.org/html/rfc3463
        '''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BounceTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-ses-actions.EmailEncoding")
class EmailEncoding(enum.Enum):
    '''The type of email encoding to use for a SNS action.'''

    BASE64 = "BASE64"
    '''Base 64.'''
    UTF8 = "UTF8"
    '''UTF-8.'''


@jsii.implements(_aws_cdk_aws_ses_b8f9c394.IReceiptRuleAction)
class Lambda(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses-actions.Lambda"):
    '''Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_lambda as lambda_
        import aws_cdk.aws_ses_actions as ses_actions
        import aws_cdk.aws_sns as sns
        
        # function_: lambda.Function
        # topic: sns.Topic
        
        lambda_ = ses_actions.Lambda(
            function=function_,
        
            # the properties below are optional
            invocation_type=ses_actions.LambdaInvocationType.EVENT,
            topic=topic
        )
    '''

    def __init__(
        self,
        *,
        function: _aws_cdk_aws_lambda_5443dbc3.IFunction,
        invocation_type: typing.Optional["LambdaInvocationType"] = None,
        topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
    ) -> None:
        '''
        :param function: The Lambda function to invoke.
        :param invocation_type: The invocation type of the Lambda function. Default: Event
        :param topic: The SNS topic to notify when the Lambda action is taken. Default: no notification
        '''
        props = LambdaProps(
            function=function, invocation_type=invocation_type, topic=topic
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
    ) -> _aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig:
        '''Returns the receipt rule action specification.

        :param rule: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee0690847d1cf346edface8531759c56aeeab60ceddd1bfc5742381cc50dacf)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig, jsii.invoke(self, "bind", [rule]))


@jsii.enum(jsii_type="@aws-cdk/aws-ses-actions.LambdaInvocationType")
class LambdaInvocationType(enum.Enum):
    '''The type of invocation to use for a Lambda Action.'''

    EVENT = "EVENT"
    '''The function will be invoked asynchronously.'''
    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    '''The function will be invoked sychronously.

    Use RequestResponse only when
    you want to make a mail flow decision, such as whether to stop the receipt
    rule or the receipt rule set.
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.LambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "function": "function",
        "invocation_type": "invocationType",
        "topic": "topic",
    },
)
class LambdaProps:
    def __init__(
        self,
        *,
        function: _aws_cdk_aws_lambda_5443dbc3.IFunction,
        invocation_type: typing.Optional[LambdaInvocationType] = None,
        topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
    ) -> None:
        '''Construction properties for a Lambda action.

        :param function: The Lambda function to invoke.
        :param invocation_type: The invocation type of the Lambda function. Default: Event
        :param topic: The SNS topic to notify when the Lambda action is taken. Default: no notification

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_lambda as lambda_
            import aws_cdk.aws_ses_actions as ses_actions
            import aws_cdk.aws_sns as sns
            
            # function_: lambda.Function
            # topic: sns.Topic
            
            lambda_props = ses_actions.LambdaProps(
                function=function_,
            
                # the properties below are optional
                invocation_type=ses_actions.LambdaInvocationType.EVENT,
                topic=topic
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da29c068d9e0c6064dedc8cedacf82ba8ec7da99207a04293e46bc64894b6b1f)
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function": function,
        }
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def function(self) -> _aws_cdk_aws_lambda_5443dbc3.IFunction:
        '''The Lambda function to invoke.'''
        result = self._values.get("function")
        assert result is not None, "Required property 'function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.IFunction, result)

    @builtins.property
    def invocation_type(self) -> typing.Optional[LambdaInvocationType]:
        '''The invocation type of the Lambda function.

        :default: Event
        '''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional[LambdaInvocationType], result)

    @builtins.property
    def topic(self) -> typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic]:
        '''The SNS topic to notify when the Lambda action is taken.

        :default: no notification
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ses_b8f9c394.IReceiptRuleAction)
class S3(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses-actions.S3"):
    '''Saves the received message to an Amazon S3 bucket and, optionally, publishes a notification to Amazon SNS.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_s3 as s3
        import aws_cdk.aws_ses_actions as actions
        
        
        bucket = s3.Bucket(self, "Bucket")
        topic = sns.Topic(self, "Topic")
        
        ses.ReceiptRuleSet(self, "RuleSet",
            rules=[ses.ReceiptRuleOptions(
                recipients=["hello@aws.com"],
                actions=[
                    actions.AddHeader(
                        name="X-Special-Header",
                        value="aws"
                    ),
                    actions.S3(
                        bucket=bucket,
                        object_key_prefix="emails/",
                        topic=topic
                    )
                ]
            ), ses.ReceiptRuleOptions(
                recipients=["aws.com"],
                actions=[
                    actions.Sns(
                        topic=topic
                    )
                ]
            )
            ]
        )
    '''

    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
        kms_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        object_key_prefix: typing.Optional[builtins.str] = None,
        topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
    ) -> None:
        '''
        :param bucket: The S3 bucket that incoming email will be saved to.
        :param kms_key: The master key that SES should use to encrypt your emails before saving them to the S3 bucket. Default: no encryption
        :param object_key_prefix: The key prefix of the S3 bucket. Default: no prefix
        :param topic: The SNS topic to notify when the S3 action is taken. Default: no notification
        '''
        props = S3Props(
            bucket=bucket,
            kms_key=kms_key,
            object_key_prefix=object_key_prefix,
            topic=topic,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
    ) -> _aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig:
        '''Returns the receipt rule action specification.

        :param rule: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5997337e7d9c333c826453698a6f90415823277cfd5dc3dc1c7b8dd11c69c53)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast(_aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.S3Props",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "kms_key": "kmsKey",
        "object_key_prefix": "objectKeyPrefix",
        "topic": "topic",
    },
)
class S3Props:
    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
        kms_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
        object_key_prefix: typing.Optional[builtins.str] = None,
        topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
    ) -> None:
        '''Construction properties for a S3 action.

        :param bucket: The S3 bucket that incoming email will be saved to.
        :param kms_key: The master key that SES should use to encrypt your emails before saving them to the S3 bucket. Default: no encryption
        :param object_key_prefix: The key prefix of the S3 bucket. Default: no prefix
        :param topic: The SNS topic to notify when the S3 action is taken. Default: no notification

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_s3 as s3
            import aws_cdk.aws_ses_actions as actions
            
            
            bucket = s3.Bucket(self, "Bucket")
            topic = sns.Topic(self, "Topic")
            
            ses.ReceiptRuleSet(self, "RuleSet",
                rules=[ses.ReceiptRuleOptions(
                    recipients=["hello@aws.com"],
                    actions=[
                        actions.AddHeader(
                            name="X-Special-Header",
                            value="aws"
                        ),
                        actions.S3(
                            bucket=bucket,
                            object_key_prefix="emails/",
                            topic=topic
                        )
                    ]
                ), ses.ReceiptRuleOptions(
                    recipients=["aws.com"],
                    actions=[
                        actions.Sns(
                            topic=topic
                        )
                    ]
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d01ca4c64e4cdec9c2038b9ce262c3eb9561c3600503d6a8960a4b7b7b6886)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if object_key_prefix is not None:
            self._values["object_key_prefix"] = object_key_prefix
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_55f001a5.IBucket:
        '''The S3 bucket that incoming email will be saved to.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_55f001a5.IBucket, result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey]:
        '''The master key that SES should use to encrypt your emails before saving them to the S3 bucket.

        :default: no encryption
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey], result)

    @builtins.property
    def object_key_prefix(self) -> typing.Optional[builtins.str]:
        '''The key prefix of the S3 bucket.

        :default: no prefix
        '''
        result = self._values.get("object_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic]:
        '''The SNS topic to notify when the S3 action is taken.

        :default: no notification
        '''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ses_b8f9c394.IReceiptRuleAction)
class Sns(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses-actions.Sns"):
    '''Publishes the email content within a notification to Amazon SNS.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_s3 as s3
        import aws_cdk.aws_ses_actions as actions
        
        
        bucket = s3.Bucket(self, "Bucket")
        topic = sns.Topic(self, "Topic")
        
        ses.ReceiptRuleSet(self, "RuleSet",
            rules=[ses.ReceiptRuleOptions(
                recipients=["hello@aws.com"],
                actions=[
                    actions.AddHeader(
                        name="X-Special-Header",
                        value="aws"
                    ),
                    actions.S3(
                        bucket=bucket,
                        object_key_prefix="emails/",
                        topic=topic
                    )
                ]
            ), ses.ReceiptRuleOptions(
                recipients=["aws.com"],
                actions=[
                    actions.Sns(
                        topic=topic
                    )
                ]
            )
            ]
        )
    '''

    def __init__(
        self,
        *,
        topic: _aws_cdk_aws_sns_889c7272.ITopic,
        encoding: typing.Optional[EmailEncoding] = None,
    ) -> None:
        '''
        :param topic: The SNS topic to notify.
        :param encoding: The encoding to use for the email within the Amazon SNS notification. Default: UTF-8
        '''
        props = SnsProps(topic=topic, encoding=encoding)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
    ) -> _aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig:
        '''Returns the receipt rule action specification.

        :param _rule: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594d4dbd36338a6129440938bba6a77e4813538082203c997ab5dae502e43102)
            check_type(argname="argument _rule", value=_rule, expected_type=type_hints["_rule"])
        return typing.cast(_aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig, jsii.invoke(self, "bind", [_rule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.SnsProps",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic", "encoding": "encoding"},
)
class SnsProps:
    def __init__(
        self,
        *,
        topic: _aws_cdk_aws_sns_889c7272.ITopic,
        encoding: typing.Optional[EmailEncoding] = None,
    ) -> None:
        '''Construction properties for a SNS action.

        :param topic: The SNS topic to notify.
        :param encoding: The encoding to use for the email within the Amazon SNS notification. Default: UTF-8

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_s3 as s3
            import aws_cdk.aws_ses_actions as actions
            
            
            bucket = s3.Bucket(self, "Bucket")
            topic = sns.Topic(self, "Topic")
            
            ses.ReceiptRuleSet(self, "RuleSet",
                rules=[ses.ReceiptRuleOptions(
                    recipients=["hello@aws.com"],
                    actions=[
                        actions.AddHeader(
                            name="X-Special-Header",
                            value="aws"
                        ),
                        actions.S3(
                            bucket=bucket,
                            object_key_prefix="emails/",
                            topic=topic
                        )
                    ]
                ), ses.ReceiptRuleOptions(
                    recipients=["aws.com"],
                    actions=[
                        actions.Sns(
                            topic=topic
                        )
                    ]
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2030df3cfc0117247d81de06d9c7d2a1d88d95b646559148a708a95cffa74803)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }
        if encoding is not None:
            self._values["encoding"] = encoding

    @builtins.property
    def topic(self) -> _aws_cdk_aws_sns_889c7272.ITopic:
        '''The SNS topic to notify.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(_aws_cdk_aws_sns_889c7272.ITopic, result)

    @builtins.property
    def encoding(self) -> typing.Optional[EmailEncoding]:
        '''The encoding to use for the email within the Amazon SNS notification.

        :default: UTF-8
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[EmailEncoding], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ses_b8f9c394.IReceiptRuleAction)
class Stop(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses-actions.Stop"):
    '''Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses_actions as ses_actions
        import aws_cdk.aws_sns as sns
        
        # topic: sns.Topic
        
        stop = ses_actions.Stop(
            topic=topic
        )
    '''

    def __init__(
        self,
        *,
        topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
    ) -> None:
        '''
        :param topic: The SNS topic to notify when the stop action is taken.
        '''
        props = StopProps(topic=topic)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
    ) -> _aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig:
        '''Returns the receipt rule action specification.

        :param _rule: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d704a6b39ca84228a72395f25eb274c7cfbbbf1f6be0a2d0c3a4af09da85c28)
            check_type(argname="argument _rule", value=_rule, expected_type=type_hints["_rule"])
        return typing.cast(_aws_cdk_aws_ses_b8f9c394.ReceiptRuleActionConfig, jsii.invoke(self, "bind", [_rule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses-actions.StopProps",
    jsii_struct_bases=[],
    name_mapping={"topic": "topic"},
)
class StopProps:
    def __init__(
        self,
        *,
        topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
    ) -> None:
        '''Construction properties for a stop action.

        :param topic: The SNS topic to notify when the stop action is taken.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses_actions as ses_actions
            import aws_cdk.aws_sns as sns
            
            # topic: sns.Topic
            
            stop_props = ses_actions.StopProps(
                topic=topic
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262765d74e99561035e4bf24b371987b8ecaffabee8b65ae2556a77af49e5d18)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if topic is not None:
            self._values["topic"] = topic

    @builtins.property
    def topic(self) -> typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic]:
        '''The SNS topic to notify when the stop action is taken.'''
        result = self._values.get("topic")
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StopProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddHeader",
    "AddHeaderProps",
    "Bounce",
    "BounceProps",
    "BounceTemplate",
    "BounceTemplateProps",
    "EmailEncoding",
    "Lambda",
    "LambdaInvocationType",
    "LambdaProps",
    "S3",
    "S3Props",
    "Sns",
    "SnsProps",
    "Stop",
    "StopProps",
]

publication.publish()

def _typecheckingstub__83e62c47a3073f2fa057acf62f9842bd0161c1e30751c3579d931081d0010241(
    _rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7eed0eabb35a3d9510a514abe92497021b023b56ba9682b716fda62d494d90(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32785a0b7d9413fe20b4aafc8f06f718ccc235c60f88c5a82ed16f3bcddb38ca(
    _rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9d72774b8be6e2d2b1f96682e3960356d65ab6320051251a3dfb9b874c5331(
    *,
    sender: builtins.str,
    template: BounceTemplate,
    topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de96ec77596b08d03d0643fe3d841a0a40bb3f75479fb08bc5fd12b962a04306(
    *,
    message: builtins.str,
    smtp_reply_code: builtins.str,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee0690847d1cf346edface8531759c56aeeab60ceddd1bfc5742381cc50dacf(
    rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da29c068d9e0c6064dedc8cedacf82ba8ec7da99207a04293e46bc64894b6b1f(
    *,
    function: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    invocation_type: typing.Optional[LambdaInvocationType] = None,
    topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5997337e7d9c333c826453698a6f90415823277cfd5dc3dc1c7b8dd11c69c53(
    rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d01ca4c64e4cdec9c2038b9ce262c3eb9561c3600503d6a8960a4b7b7b6886(
    *,
    bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    kms_key: typing.Optional[_aws_cdk_aws_kms_e491a92b.IKey] = None,
    object_key_prefix: typing.Optional[builtins.str] = None,
    topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594d4dbd36338a6129440938bba6a77e4813538082203c997ab5dae502e43102(
    _rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2030df3cfc0117247d81de06d9c7d2a1d88d95b646559148a708a95cffa74803(
    *,
    topic: _aws_cdk_aws_sns_889c7272.ITopic,
    encoding: typing.Optional[EmailEncoding] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d704a6b39ca84228a72395f25eb274c7cfbbbf1f6be0a2d0c3a4af09da85c28(
    _rule: _aws_cdk_aws_ses_b8f9c394.IReceiptRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262765d74e99561035e4bf24b371987b8ecaffabee8b65ae2556a77af49e5d18(
    *,
    topic: typing.Optional[_aws_cdk_aws_sns_889c7272.ITopic] = None,
) -> None:
    """Type checking stubs"""
    pass
