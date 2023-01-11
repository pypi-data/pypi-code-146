'''
# AWS::Lex Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_lex as lex
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Lex construct libraries](https://constructs.dev/search?q=lex)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Lex resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Lex.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Lex](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Lex.html).

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
class CfnBot(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lex.CfnBot",
):
    '''A CloudFormation ``AWS::Lex::Bot``.

    .. epigraph::

       Amazon Lex V2 is the only supported version in AWS CloudFormation .

    Specifies an Amazon Lex conversational bot.

    You must configure an intent based on the AMAZON.FallbackIntent built-in intent. If you don't add one, creating the bot will fail.

    :cloudformationResource: AWS::Lex::Bot
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_lex as lex
        
        # data_privacy: Any
        # sentiment_analysis_settings: Any
        
        cfn_bot = lex.CfnBot(self, "MyCfnBot",
            data_privacy=data_privacy,
            idle_session_ttl_in_seconds=123,
            name="name",
            role_arn="roleArn",
        
            # the properties below are optional
            auto_build_bot_locales=False,
            bot_file_s3_location=lex.CfnBot.S3LocationProperty(
                s3_bucket="s3Bucket",
                s3_object_key="s3ObjectKey",
        
                # the properties below are optional
                s3_object_version="s3ObjectVersion"
            ),
            bot_locales=[lex.CfnBot.BotLocaleProperty(
                locale_id="localeId",
                nlu_confidence_threshold=123,
        
                # the properties below are optional
                custom_vocabulary=lex.CfnBot.CustomVocabularyProperty(
                    custom_vocabulary_items=[lex.CfnBot.CustomVocabularyItemProperty(
                        phrase="phrase",
        
                        # the properties below are optional
                        weight=123
                    )]
                ),
                description="description",
                intents=[lex.CfnBot.IntentProperty(
                    name="name",
        
                    # the properties below are optional
                    description="description",
                    dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                        enabled=False
                    ),
                    fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                        enabled=False,
        
                        # the properties below are optional
                        fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                            active=False,
        
                            # the properties below are optional
                            start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                                delay_in_seconds=123,
                                message_groups=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            timeout_in_seconds=123,
                            update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                                frequency_in_seconds=123,
                                message_groups=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            )
                        ),
                        post_fulfillment_status_specification=lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                            failure_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            success_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False
                            )
                        )
                    ),
                    input_contexts=[lex.CfnBot.InputContextProperty(
                        name="name"
                    )],
                    intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                        closing_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
        
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
        
                            # the properties below are optional
                            allow_interrupt=False
                        ),
        
                        # the properties below are optional
                        is_active=False
                    ),
                    intent_confirmation_setting=lex.CfnBot.IntentConfirmationSettingProperty(
                        declination_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
        
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
        
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            max_retries=123,
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
        
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
        
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
        
                            # the properties below are optional
                            allow_interrupt=False,
                            message_selection_strategy="messageSelectionStrategy",
                            prompt_attempts_specification={
                                "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                    allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                        allow_audio_input=False,
                                        allow_dtmf_input=False
                                    ),
        
                                    # the properties below are optional
                                    allow_interrupt=False,
                                    audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                        start_timeout_ms=123,
        
                                        # the properties below are optional
                                        audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                            end_timeout_ms=123,
                                            max_length_ms=123
                                        ),
                                        dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                            deletion_character="deletionCharacter",
                                            end_character="endCharacter",
                                            end_timeout_ms=123,
                                            max_length=123
                                        )
                                    ),
                                    text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                        start_timeout_ms=123
                                    )
                                )
                            }
                        ),
        
                        # the properties below are optional
                        is_active=False
                    ),
                    kendra_configuration=lex.CfnBot.KendraConfigurationProperty(
                        kendra_index="kendraIndex",
        
                        # the properties below are optional
                        query_filter_string="queryFilterString",
                        query_filter_string_enabled=False
                    ),
                    output_contexts=[lex.CfnBot.OutputContextProperty(
                        name="name",
                        time_to_live_in_seconds=123,
                        turns_to_live=123
                    )],
                    parent_intent_signature="parentIntentSignature",
                    sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                        utterance="utterance"
                    )],
                    slot_priorities=[lex.CfnBot.SlotPriorityProperty(
                        priority=123,
                        slot_name="slotName"
                    )],
                    slots=[lex.CfnBot.SlotProperty(
                        name="name",
                        slot_type_name="slotTypeName",
                        value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                            slot_constraint="slotConstraint",
        
                            # the properties below are optional
                            default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                                default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                                    default_value="defaultValue"
                                )]
                            ),
                            prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                max_retries=123,
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
        
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
        
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
        
                                # the properties below are optional
                                allow_interrupt=False,
                                message_selection_strategy="messageSelectionStrategy",
                                prompt_attempts_specification={
                                    "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                        allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                            allow_audio_input=False,
                                            allow_dtmf_input=False
                                        ),
        
                                        # the properties below are optional
                                        allow_interrupt=False,
                                        audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                            start_timeout_ms=123,
        
                                            # the properties below are optional
                                            audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                                end_timeout_ms=123,
                                                max_length_ms=123
                                            ),
                                            dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                                deletion_character="deletionCharacter",
                                                end_character="endCharacter",
                                                end_timeout_ms=123,
                                                max_length=123
                                            )
                                        ),
                                        text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                            start_timeout_ms=123
                                        )
                                    )
                                }
                            ),
                            sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                                utterance="utterance"
                            )],
                            wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                                continue_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
        
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
        
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
        
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
        
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
        
                                # the properties below are optional
                                is_active=False,
                                still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                                    frequency_in_seconds=123,
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
        
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
        
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                                    timeout_in_seconds=123,
        
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            )
                        ),
        
                        # the properties below are optional
                        description="description",
                        multiple_values_setting=lex.CfnBot.MultipleValuesSettingProperty(
                            allow_multiple_values=False
                        ),
                        obfuscation_setting=lex.CfnBot.ObfuscationSettingProperty(
                            obfuscation_setting_type="obfuscationSettingType"
                        )
                    )]
                )],
                slot_types=[lex.CfnBot.SlotTypeProperty(
                    name="name",
        
                    # the properties below are optional
                    description="description",
                    external_source_setting=lex.CfnBot.ExternalSourceSettingProperty(
                        grammar_slot_type_setting=lex.CfnBot.GrammarSlotTypeSettingProperty(
                            source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                                s3_bucket_name="s3BucketName",
                                s3_object_key="s3ObjectKey",
        
                                # the properties below are optional
                                kms_key_arn="kmsKeyArn"
                            )
                        )
                    ),
                    parent_slot_type_signature="parentSlotTypeSignature",
                    slot_type_values=[lex.CfnBot.SlotTypeValueProperty(
                        sample_value=lex.CfnBot.SampleValueProperty(
                            value="value"
                        ),
        
                        # the properties below are optional
                        synonyms=[lex.CfnBot.SampleValueProperty(
                            value="value"
                        )]
                    )],
                    value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                        resolution_strategy="resolutionStrategy",
        
                        # the properties below are optional
                        advanced_recognition_setting=lex.CfnBot.AdvancedRecognitionSettingProperty(
                            audio_recognition_strategy="audioRecognitionStrategy"
                        ),
                        regex_filter=lex.CfnBot.SlotValueRegexFilterProperty(
                            pattern="pattern"
                        )
                    )
                )],
                voice_settings=lex.CfnBot.VoiceSettingsProperty(
                    voice_id="voiceId",
        
                    # the properties below are optional
                    engine="engine"
                )
            )],
            bot_tags=[CfnTag(
                key="key",
                value="value"
            )],
            description="description",
            test_bot_alias_settings=lex.CfnBot.TestBotAliasSettingsProperty(
                bot_alias_locale_settings=[lex.CfnBot.BotAliasLocaleSettingsItemProperty(
                    bot_alias_locale_setting=lex.CfnBot.BotAliasLocaleSettingsProperty(
                        enabled=False,
        
                        # the properties below are optional
                        code_hook_specification=lex.CfnBot.CodeHookSpecificationProperty(
                            lambda_code_hook=lex.CfnBot.LambdaCodeHookProperty(
                                code_hook_interface_version="codeHookInterfaceVersion",
                                lambda_arn="lambdaArn"
                            )
                        )
                    ),
                    locale_id="localeId"
                )],
                conversation_log_settings=lex.CfnBot.ConversationLogSettingsProperty(
                    audio_log_settings=[lex.CfnBot.AudioLogSettingProperty(
                        destination=lex.CfnBot.AudioLogDestinationProperty(
                            s3_bucket=lex.CfnBot.S3BucketLogDestinationProperty(
                                log_prefix="logPrefix",
                                s3_bucket_arn="s3BucketArn",
        
                                # the properties below are optional
                                kms_key_arn="kmsKeyArn"
                            )
                        ),
                        enabled=False
                    )],
                    text_log_settings=[lex.CfnBot.TextLogSettingProperty(
                        destination=lex.CfnBot.TextLogDestinationProperty(
                            cloud_watch=lex.CfnBot.CloudWatchLogGroupLogDestinationProperty(
                                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                                log_prefix="logPrefix"
                            )
                        ),
                        enabled=False
                    )]
                ),
                description="description",
                sentiment_analysis_settings=sentiment_analysis_settings
            ),
            test_bot_alias_tags=[CfnTag(
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
        data_privacy: typing.Any,
        idle_session_ttl_in_seconds: jsii.Number,
        name: builtins.str,
        role_arn: builtins.str,
        auto_build_bot_locales: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        bot_file_s3_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        bot_locales: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.BotLocaleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        bot_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        test_bot_alias_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.TestBotAliasSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        test_bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Lex::Bot``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_privacy: Provides information on additional privacy protections Amazon Lex should use with the bot's data.
        :param idle_session_ttl_in_seconds: The time, in seconds, that Amazon Lex should keep information about a user's conversation with the bot. A user interaction remains active for the amount of time specified. If no conversation occurs during this time, the session expires and Amazon Lex deletes any data provided before the timeout. You can specify between 60 (1 minute) and 86,400 (24 hours) seconds.
        :param name: The name of the field to filter the list of bots.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role used to build and run the bot.
        :param auto_build_bot_locales: Indicates whether Amazon Lex V2 should automatically build the locales for the bot after a change.
        :param bot_file_s3_location: The Amazon S3 location of files used to import a bot. The files must be in the import format specified in `JSON format for importing and exporting <https://docs.aws.amazon.com/lexv2/latest/dg/import-export-format.html>`_ in the *Amazon Lex developer guide.*
        :param bot_locales: A list of locales for the bot.
        :param bot_tags: A list of tags to add to the bot. You can only add tags when you import a bot. You can't use the ``UpdateBot`` operation to update tags. To update tags, use the ``TagResource`` operation.
        :param description: The description of the version.
        :param test_bot_alias_settings: Specifies configuration settings for the alias used to test the bot. If the ``TestBotAliasSettings`` property is not specified, the settings are configured with default values.
        :param test_bot_alias_tags: A list of tags to add to the test alias for a bot. You can only add tags when you import a bot. You can't use the ``UpdateAlias`` operation to update tags. To update tags on the test alias, use the ``TagResource`` operation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32b6ba3ac1a11f523aed5f511585db6c68f66ab488d13ff9f3b1bc0343ece29)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBotProps(
            data_privacy=data_privacy,
            idle_session_ttl_in_seconds=idle_session_ttl_in_seconds,
            name=name,
            role_arn=role_arn,
            auto_build_bot_locales=auto_build_bot_locales,
            bot_file_s3_location=bot_file_s3_location,
            bot_locales=bot_locales,
            bot_tags=bot_tags,
            description=description,
            test_bot_alias_settings=test_bot_alias_settings,
            test_bot_alias_tags=test_bot_alias_tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b44e6f55c1aaee99c24639c213099abed1c7b704a641a541f2389206b4d3d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7489eac65be2b6a4f6b60cc2d23e4020bb81c653e4e58dba47143f64169d4d42)
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
        '''The Amazon Resource Name (ARN) of the bot.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The unique identifier of the bot.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="dataPrivacy")
    def data_privacy(self) -> typing.Any:
        '''Provides information on additional privacy protections Amazon Lex should use with the bot's data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-dataprivacy
        '''
        return typing.cast(typing.Any, jsii.get(self, "dataPrivacy"))

    @data_privacy.setter
    def data_privacy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291daf3180cba7471a77ba47ca5526f76d5a822c77c6bae56a81cb20f791cca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataPrivacy", value)

    @builtins.property
    @jsii.member(jsii_name="idleSessionTtlInSeconds")
    def idle_session_ttl_in_seconds(self) -> jsii.Number:
        '''The time, in seconds, that Amazon Lex should keep information about a user's conversation with the bot.

        A user interaction remains active for the amount of time specified. If no conversation occurs during this time, the session expires and Amazon Lex deletes any data provided before the timeout.

        You can specify between 60 (1 minute) and 86,400 (24 hours) seconds.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-idlesessionttlinseconds
        '''
        return typing.cast(jsii.Number, jsii.get(self, "idleSessionTtlInSeconds"))

    @idle_session_ttl_in_seconds.setter
    def idle_session_ttl_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19fcce7464c109d027ceae526882382993870083562b90a6141a2ae436a3342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleSessionTtlInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the field to filter the list of bots.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6ae8fbab2b0706d58b4bf9de2e780913a84dd1b83350ca240fa0ac6b1fed03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role used to build and run the bot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa106447fbd5f28c2a8191871ce76e3723a1f4afe8173e6c9cb4650cb18554e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="autoBuildBotLocales")
    def auto_build_bot_locales(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether Amazon Lex V2 should automatically build the locales for the bot after a change.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-autobuildbotlocales
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "autoBuildBotLocales"))

    @auto_build_bot_locales.setter
    def auto_build_bot_locales(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f293142c9e68ba1b9f6235a9eef8f0ee35368682cc04e5b506d970d4370b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoBuildBotLocales", value)

    @builtins.property
    @jsii.member(jsii_name="botFileS3Location")
    def bot_file_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.S3LocationProperty"]]:
        '''The Amazon S3 location of files used to import a bot.

        The files must be in the import format specified in `JSON format for importing and exporting <https://docs.aws.amazon.com/lexv2/latest/dg/import-export-format.html>`_ in the *Amazon Lex developer guide.*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-botfiles3location
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.S3LocationProperty"]], jsii.get(self, "botFileS3Location"))

    @bot_file_s3_location.setter
    def bot_file_s3_location(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.S3LocationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362bfaf577ca696673ce60d5989301ba1e228a4483e8ef08bb5b78da418898f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botFileS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="botLocales")
    def bot_locales(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.BotLocaleProperty"]]]]:
        '''A list of locales for the bot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-botlocales
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.BotLocaleProperty"]]]], jsii.get(self, "botLocales"))

    @bot_locales.setter
    def bot_locales(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.BotLocaleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b917a2f613fe9b4a599279d725f726837b1659e25847d4170d03f9b499976d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botLocales", value)

    @builtins.property
    @jsii.member(jsii_name="botTags")
    def bot_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]]:
        '''A list of tags to add to the bot.

        You can only add tags when you import a bot. You can't use the ``UpdateBot`` operation to update tags. To update tags, use the ``TagResource`` operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-bottags
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]], jsii.get(self, "botTags"))

    @bot_tags.setter
    def bot_tags(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8732ebd90cc3092165edf7b3b336ce71cd94af1dac75b9d3c49317796e8c35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botTags", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36dd3001a021a12cb0baf96ff20897eff6402523f5390ef16db0498805a78917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="testBotAliasSettings")
    def test_bot_alias_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.TestBotAliasSettingsProperty"]]:
        '''Specifies configuration settings for the alias used to test the bot.

        If the ``TestBotAliasSettings`` property is not specified, the settings are configured with default values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-testbotaliassettings
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.TestBotAliasSettingsProperty"]], jsii.get(self, "testBotAliasSettings"))

    @test_bot_alias_settings.setter
    def test_bot_alias_settings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.TestBotAliasSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0486714edae70bd4cf7e2f138408212a8a7a3ed8c7703d5dbb06e7495c3254a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testBotAliasSettings", value)

    @builtins.property
    @jsii.member(jsii_name="testBotAliasTags")
    def test_bot_alias_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]]:
        '''A list of tags to add to the test alias for a bot.

        You can only add tags when you import a bot. You can't use the ``UpdateAlias`` operation to update tags. To update tags on the test alias, use the ``TagResource`` operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-testbotaliastags
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]], jsii.get(self, "testBotAliasTags"))

    @test_bot_alias_tags.setter
    def test_bot_alias_tags(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a878428d06d0371f39dac4b3340f1aba7fb3e1f726d4e7b74fc9ba5cff5093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testBotAliasTags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.AdvancedRecognitionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"audio_recognition_strategy": "audioRecognitionStrategy"},
    )
    class AdvancedRecognitionSettingProperty:
        def __init__(
            self,
            *,
            audio_recognition_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies settings that enable advanced audio recognition for slot values.

            :param audio_recognition_strategy: Specifies that Amazon Lex should use slot values as a custom vocabulary when recognizing user utterances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-advancedrecognitionsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                advanced_recognition_setting_property = lex.CfnBot.AdvancedRecognitionSettingProperty(
                    audio_recognition_strategy="audioRecognitionStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f18434d84262bd1b58a1e22a7ee7af3f5bde045708f19369d9cb2d77a669f4ca)
                check_type(argname="argument audio_recognition_strategy", value=audio_recognition_strategy, expected_type=type_hints["audio_recognition_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audio_recognition_strategy is not None:
                self._values["audio_recognition_strategy"] = audio_recognition_strategy

        @builtins.property
        def audio_recognition_strategy(self) -> typing.Optional[builtins.str]:
            '''Specifies that Amazon Lex should use slot values as a custom vocabulary when recognizing user utterances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-advancedrecognitionsetting.html#cfn-lex-bot-advancedrecognitionsetting-audiorecognitionstrategy
            '''
            result = self._values.get("audio_recognition_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedRecognitionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.AllowedInputTypesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_audio_input": "allowAudioInput",
            "allow_dtmf_input": "allowDtmfInput",
        },
    )
    class AllowedInputTypesProperty:
        def __init__(
            self,
            *,
            allow_audio_input: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            allow_dtmf_input: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''
            :param allow_audio_input: ``CfnBot.AllowedInputTypesProperty.AllowAudioInput``.
            :param allow_dtmf_input: ``CfnBot.AllowedInputTypesProperty.AllowDTMFInput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-allowedinputtypes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                allowed_input_types_property = lex.CfnBot.AllowedInputTypesProperty(
                    allow_audio_input=False,
                    allow_dtmf_input=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__81adb7683e742175fc26c6909829061374e32cd0ffca6a1498fdf1ec2679d53b)
                check_type(argname="argument allow_audio_input", value=allow_audio_input, expected_type=type_hints["allow_audio_input"])
                check_type(argname="argument allow_dtmf_input", value=allow_dtmf_input, expected_type=type_hints["allow_dtmf_input"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "allow_audio_input": allow_audio_input,
                "allow_dtmf_input": allow_dtmf_input,
            }

        @builtins.property
        def allow_audio_input(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''``CfnBot.AllowedInputTypesProperty.AllowAudioInput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-allowedinputtypes.html#cfn-lex-bot-allowedinputtypes-allowaudioinput
            '''
            result = self._values.get("allow_audio_input")
            assert result is not None, "Required property 'allow_audio_input' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def allow_dtmf_input(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''``CfnBot.AllowedInputTypesProperty.AllowDTMFInput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-allowedinputtypes.html#cfn-lex-bot-allowedinputtypes-allowdtmfinput
            '''
            result = self._values.get("allow_dtmf_input")
            assert result is not None, "Required property 'allow_dtmf_input' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AllowedInputTypesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.AudioAndDTMFInputSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "start_timeout_ms": "startTimeoutMs",
            "audio_specification": "audioSpecification",
            "dtmf_specification": "dtmfSpecification",
        },
    )
    class AudioAndDTMFInputSpecificationProperty:
        def __init__(
            self,
            *,
            start_timeout_ms: jsii.Number,
            audio_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.AudioSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dtmf_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.DTMFSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param start_timeout_ms: ``CfnBot.AudioAndDTMFInputSpecificationProperty.StartTimeoutMs``.
            :param audio_specification: ``CfnBot.AudioAndDTMFInputSpecificationProperty.AudioSpecification``.
            :param dtmf_specification: ``CfnBot.AudioAndDTMFInputSpecificationProperty.DTMFSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audioanddtmfinputspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                audio_and_dTMFInput_specification_property = lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                    start_timeout_ms=123,
                
                    # the properties below are optional
                    audio_specification=lex.CfnBot.AudioSpecificationProperty(
                        end_timeout_ms=123,
                        max_length_ms=123
                    ),
                    dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                        deletion_character="deletionCharacter",
                        end_character="endCharacter",
                        end_timeout_ms=123,
                        max_length=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__172847647b14e44f8713aab62364b1fb02bf11ca42de2d2202906964a14389f3)
                check_type(argname="argument start_timeout_ms", value=start_timeout_ms, expected_type=type_hints["start_timeout_ms"])
                check_type(argname="argument audio_specification", value=audio_specification, expected_type=type_hints["audio_specification"])
                check_type(argname="argument dtmf_specification", value=dtmf_specification, expected_type=type_hints["dtmf_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "start_timeout_ms": start_timeout_ms,
            }
            if audio_specification is not None:
                self._values["audio_specification"] = audio_specification
            if dtmf_specification is not None:
                self._values["dtmf_specification"] = dtmf_specification

        @builtins.property
        def start_timeout_ms(self) -> jsii.Number:
            '''``CfnBot.AudioAndDTMFInputSpecificationProperty.StartTimeoutMs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audioanddtmfinputspecification.html#cfn-lex-bot-audioanddtmfinputspecification-starttimeoutms
            '''
            result = self._values.get("start_timeout_ms")
            assert result is not None, "Required property 'start_timeout_ms' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def audio_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AudioSpecificationProperty"]]:
            '''``CfnBot.AudioAndDTMFInputSpecificationProperty.AudioSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audioanddtmfinputspecification.html#cfn-lex-bot-audioanddtmfinputspecification-audiospecification
            '''
            result = self._values.get("audio_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AudioSpecificationProperty"]], result)

        @builtins.property
        def dtmf_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.DTMFSpecificationProperty"]]:
            '''``CfnBot.AudioAndDTMFInputSpecificationProperty.DTMFSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audioanddtmfinputspecification.html#cfn-lex-bot-audioanddtmfinputspecification-dtmfspecification
            '''
            result = self._values.get("dtmf_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.DTMFSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioAndDTMFInputSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.AudioLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket"},
    )
    class AudioLogDestinationProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.S3BucketLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Specifies the location of audio log files collected when conversation logging is enabled for a bot.

            :param s3_bucket: Specifies the Amazon S3 bucket where the audio files are stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiologdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                audio_log_destination_property = lex.CfnBot.AudioLogDestinationProperty(
                    s3_bucket=lex.CfnBot.S3BucketLogDestinationProperty(
                        log_prefix="logPrefix",
                        s3_bucket_arn="s3BucketArn",
                
                        # the properties below are optional
                        kms_key_arn="kmsKeyArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd16255160f7020b858d622bde765d4d99dbbef63f0e46d978da9697782fde15)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket": s3_bucket,
            }

        @builtins.property
        def s3_bucket(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.S3BucketLogDestinationProperty"]:
            '''Specifies the Amazon S3 bucket where the audio files are stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiologdestination.html#cfn-lex-bot-audiologdestination-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.S3BucketLogDestinationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.AudioLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "enabled": "enabled"},
    )
    class AudioLogSettingProperty:
        def __init__(
            self,
            *,
            destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.AudioLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]],
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''Specifies settings for logging the audio of conversations between Amazon Lex and a user.

            You specify whether to log audio and the Amazon S3 bucket where the audio file is stored.

            :param destination: Specifies the location of the audio log files collected when conversation logging is enabled for a bot.
            :param enabled: Specifies whether audio logging is enabled for the bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiologsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                audio_log_setting_property = lex.CfnBot.AudioLogSettingProperty(
                    destination=lex.CfnBot.AudioLogDestinationProperty(
                        s3_bucket=lex.CfnBot.S3BucketLogDestinationProperty(
                            log_prefix="logPrefix",
                            s3_bucket_arn="s3BucketArn",
                
                            # the properties below are optional
                            kms_key_arn="kmsKeyArn"
                        )
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__012e5b81ba543678c2746364b2307194ee37ec7d0469da50bef4f95cfc3a087e)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination": destination,
                "enabled": enabled,
            }

        @builtins.property
        def destination(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AudioLogDestinationProperty"]:
            '''Specifies the location of the audio log files collected when conversation logging is enabled for a bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiologsetting.html#cfn-lex-bot-audiologsetting-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AudioLogDestinationProperty"], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Specifies whether audio logging is enabled for the bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiologsetting.html#cfn-lex-bot-audiologsetting-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.AudioSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_timeout_ms": "endTimeoutMs",
            "max_length_ms": "maxLengthMs",
        },
    )
    class AudioSpecificationProperty:
        def __init__(
            self,
            *,
            end_timeout_ms: jsii.Number,
            max_length_ms: jsii.Number,
        ) -> None:
            '''
            :param end_timeout_ms: ``CfnBot.AudioSpecificationProperty.EndTimeoutMs``.
            :param max_length_ms: ``CfnBot.AudioSpecificationProperty.MaxLengthMs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiospecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                audio_specification_property = lex.CfnBot.AudioSpecificationProperty(
                    end_timeout_ms=123,
                    max_length_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5dd5779b162d84386570c114b99f0561c027760c1f39856a6e320bfcbe356569)
                check_type(argname="argument end_timeout_ms", value=end_timeout_ms, expected_type=type_hints["end_timeout_ms"])
                check_type(argname="argument max_length_ms", value=max_length_ms, expected_type=type_hints["max_length_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "end_timeout_ms": end_timeout_ms,
                "max_length_ms": max_length_ms,
            }

        @builtins.property
        def end_timeout_ms(self) -> jsii.Number:
            '''``CfnBot.AudioSpecificationProperty.EndTimeoutMs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiospecification.html#cfn-lex-bot-audiospecification-endtimeoutms
            '''
            result = self._values.get("end_timeout_ms")
            assert result is not None, "Required property 'end_timeout_ms' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def max_length_ms(self) -> jsii.Number:
            '''``CfnBot.AudioSpecificationProperty.MaxLengthMs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-audiospecification.html#cfn-lex-bot-audiospecification-maxlengthms
            '''
            result = self._values.get("max_length_ms")
            assert result is not None, "Required property 'max_length_ms' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.BotAliasLocaleSettingsItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bot_alias_locale_setting": "botAliasLocaleSetting",
            "locale_id": "localeId",
        },
    )
    class BotAliasLocaleSettingsItemProperty:
        def __init__(
            self,
            *,
            bot_alias_locale_setting: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.BotAliasLocaleSettingsProperty", typing.Dict[builtins.str, typing.Any]]],
            locale_id: builtins.str,
        ) -> None:
            '''Specifies locale settings for a single locale.

            :param bot_alias_locale_setting: Specifies locale settings for a locale.
            :param locale_id: Specifies the locale that the settings apply to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettingsitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                bot_alias_locale_settings_item_property = lex.CfnBot.BotAliasLocaleSettingsItemProperty(
                    bot_alias_locale_setting=lex.CfnBot.BotAliasLocaleSettingsProperty(
                        enabled=False,
                
                        # the properties below are optional
                        code_hook_specification=lex.CfnBot.CodeHookSpecificationProperty(
                            lambda_code_hook=lex.CfnBot.LambdaCodeHookProperty(
                                code_hook_interface_version="codeHookInterfaceVersion",
                                lambda_arn="lambdaArn"
                            )
                        )
                    ),
                    locale_id="localeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__adf654f112e0ec8396c9ff8eb83dc7e4bde049f41919e0f85aed475d81029485)
                check_type(argname="argument bot_alias_locale_setting", value=bot_alias_locale_setting, expected_type=type_hints["bot_alias_locale_setting"])
                check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bot_alias_locale_setting": bot_alias_locale_setting,
                "locale_id": locale_id,
            }

        @builtins.property
        def bot_alias_locale_setting(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.BotAliasLocaleSettingsProperty"]:
            '''Specifies locale settings for a locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettingsitem.html#cfn-lex-bot-botaliaslocalesettingsitem-botaliaslocalesetting
            '''
            result = self._values.get("bot_alias_locale_setting")
            assert result is not None, "Required property 'bot_alias_locale_setting' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.BotAliasLocaleSettingsProperty"], result)

        @builtins.property
        def locale_id(self) -> builtins.str:
            '''Specifies the locale that the settings apply to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettingsitem.html#cfn-lex-bot-botaliaslocalesettingsitem-localeid
            '''
            result = self._values.get("locale_id")
            assert result is not None, "Required property 'locale_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotAliasLocaleSettingsItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.BotAliasLocaleSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "code_hook_specification": "codeHookSpecification",
        },
    )
    class BotAliasLocaleSettingsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            code_hook_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.CodeHookSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies settings that are unique to a locale.

            For example, you can use a different Lambda function for each locale.

            :param enabled: Specifies whether the locale is enabled for the bot. If the value is false, the locale isn't available for use.
            :param code_hook_specification: Specifies the Lambda function to use in this locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                bot_alias_locale_settings_property = lex.CfnBot.BotAliasLocaleSettingsProperty(
                    enabled=False,
                
                    # the properties below are optional
                    code_hook_specification=lex.CfnBot.CodeHookSpecificationProperty(
                        lambda_code_hook=lex.CfnBot.LambdaCodeHookProperty(
                            code_hook_interface_version="codeHookInterfaceVersion",
                            lambda_arn="lambdaArn"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf9aba6c3be74203c6592e57e7ea556c6428e5be7b09bd85b32211ec142bbb2e)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument code_hook_specification", value=code_hook_specification, expected_type=type_hints["code_hook_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }
            if code_hook_specification is not None:
                self._values["code_hook_specification"] = code_hook_specification

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Specifies whether the locale is enabled for the bot.

            If the value is false, the locale isn't available for use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettings.html#cfn-lex-bot-botaliaslocalesettings-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def code_hook_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.CodeHookSpecificationProperty"]]:
            '''Specifies the Lambda function to use in this locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botaliaslocalesettings.html#cfn-lex-bot-botaliaslocalesettings-codehookspecification
            '''
            result = self._values.get("code_hook_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.CodeHookSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotAliasLocaleSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.BotLocaleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "locale_id": "localeId",
            "nlu_confidence_threshold": "nluConfidenceThreshold",
            "custom_vocabulary": "customVocabulary",
            "description": "description",
            "intents": "intents",
            "slot_types": "slotTypes",
            "voice_settings": "voiceSettings",
        },
    )
    class BotLocaleProperty:
        def __init__(
            self,
            *,
            locale_id: builtins.str,
            nlu_confidence_threshold: jsii.Number,
            custom_vocabulary: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.CustomVocabularyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            intents: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.IntentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            slot_types: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SlotTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            voice_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.VoiceSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides configuration information for a locale.

            :param locale_id: The identifier of the language and locale that the bot will be used in. The string must match one of the supported locales.
            :param nlu_confidence_threshold: Determines the threshold where Amazon Lex will insert the AMAZON.FallbackIntent, AMAZON.KendraSearchIntent, or both when returning alternative intents. You must configure an AMAZON.FallbackIntent. AMAZON.KendraSearchIntent is only inserted if it is configured for the bot.
            :param custom_vocabulary: Specifies a custom vocabulary to use with a specific locale.
            :param description: A description of the bot locale. Use this to help identify the bot locale in lists.
            :param intents: One or more intents defined for the locale.
            :param slot_types: One or more slot types defined for the locale.
            :param voice_settings: Identifies the Amazon Polly voice used for audio interaction with the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                bot_locale_property = lex.CfnBot.BotLocaleProperty(
                    locale_id="localeId",
                    nlu_confidence_threshold=123,
                
                    # the properties below are optional
                    custom_vocabulary=lex.CfnBot.CustomVocabularyProperty(
                        custom_vocabulary_items=[lex.CfnBot.CustomVocabularyItemProperty(
                            phrase="phrase",
                
                            # the properties below are optional
                            weight=123
                        )]
                    ),
                    description="description",
                    intents=[lex.CfnBot.IntentProperty(
                        name="name",
                
                        # the properties below are optional
                        description="description",
                        dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                            enabled=False
                        ),
                        fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                            enabled=False,
                
                            # the properties below are optional
                            fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                                active=False,
                
                                # the properties below are optional
                                start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                                    delay_in_seconds=123,
                                    message_groups=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                timeout_in_seconds=123,
                                update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                                    frequency_in_seconds=123,
                                    message_groups=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            ),
                            post_fulfillment_status_specification=lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                                failure_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                success_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            )
                        ),
                        input_contexts=[lex.CfnBot.InputContextProperty(
                            name="name"
                        )],
                        intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                            closing_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                
                            # the properties below are optional
                            is_active=False
                        ),
                        intent_confirmation_setting=lex.CfnBot.IntentConfirmationSettingProperty(
                            declination_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                max_retries=123,
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False,
                                message_selection_strategy="messageSelectionStrategy",
                                prompt_attempts_specification={
                                    "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                        allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                            allow_audio_input=False,
                                            allow_dtmf_input=False
                                        ),
                
                                        # the properties below are optional
                                        allow_interrupt=False,
                                        audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                            start_timeout_ms=123,
                
                                            # the properties below are optional
                                            audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                                end_timeout_ms=123,
                                                max_length_ms=123
                                            ),
                                            dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                                deletion_character="deletionCharacter",
                                                end_character="endCharacter",
                                                end_timeout_ms=123,
                                                max_length=123
                                            )
                                        ),
                                        text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                            start_timeout_ms=123
                                        )
                                    )
                                }
                            ),
                
                            # the properties below are optional
                            is_active=False
                        ),
                        kendra_configuration=lex.CfnBot.KendraConfigurationProperty(
                            kendra_index="kendraIndex",
                
                            # the properties below are optional
                            query_filter_string="queryFilterString",
                            query_filter_string_enabled=False
                        ),
                        output_contexts=[lex.CfnBot.OutputContextProperty(
                            name="name",
                            time_to_live_in_seconds=123,
                            turns_to_live=123
                        )],
                        parent_intent_signature="parentIntentSignature",
                        sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                            utterance="utterance"
                        )],
                        slot_priorities=[lex.CfnBot.SlotPriorityProperty(
                            priority=123,
                            slot_name="slotName"
                        )],
                        slots=[lex.CfnBot.SlotProperty(
                            name="name",
                            slot_type_name="slotTypeName",
                            value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                                slot_constraint="slotConstraint",
                
                                # the properties below are optional
                                default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                                    default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                                        default_value="defaultValue"
                                    )]
                                ),
                                prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                    max_retries=123,
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False,
                                    message_selection_strategy="messageSelectionStrategy",
                                    prompt_attempts_specification={
                                        "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                            allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                                allow_audio_input=False,
                                                allow_dtmf_input=False
                                            ),
                
                                            # the properties below are optional
                                            allow_interrupt=False,
                                            audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                                start_timeout_ms=123,
                
                                                # the properties below are optional
                                                audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                                    end_timeout_ms=123,
                                                    max_length_ms=123
                                                ),
                                                dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                                    deletion_character="deletionCharacter",
                                                    end_character="endCharacter",
                                                    end_timeout_ms=123,
                                                    max_length=123
                                                )
                                            ),
                                            text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                                start_timeout_ms=123
                                            )
                                        )
                                    }
                                ),
                                sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                                    utterance="utterance"
                                )],
                                wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                                    continue_response=lex.CfnBot.ResponseSpecificationProperty(
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
                
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
                
                                        # the properties below are optional
                                        allow_interrupt=False
                                    ),
                                    waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
                
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
                
                                        # the properties below are optional
                                        allow_interrupt=False
                                    ),
                
                                    # the properties below are optional
                                    is_active=False,
                                    still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                                        frequency_in_seconds=123,
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
                
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
                
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
                                        timeout_in_seconds=123,
                
                                        # the properties below are optional
                                        allow_interrupt=False
                                    )
                                )
                            ),
                
                            # the properties below are optional
                            description="description",
                            multiple_values_setting=lex.CfnBot.MultipleValuesSettingProperty(
                                allow_multiple_values=False
                            ),
                            obfuscation_setting=lex.CfnBot.ObfuscationSettingProperty(
                                obfuscation_setting_type="obfuscationSettingType"
                            )
                        )]
                    )],
                    slot_types=[lex.CfnBot.SlotTypeProperty(
                        name="name",
                
                        # the properties below are optional
                        description="description",
                        external_source_setting=lex.CfnBot.ExternalSourceSettingProperty(
                            grammar_slot_type_setting=lex.CfnBot.GrammarSlotTypeSettingProperty(
                                source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                                    s3_bucket_name="s3BucketName",
                                    s3_object_key="s3ObjectKey",
                
                                    # the properties below are optional
                                    kms_key_arn="kmsKeyArn"
                                )
                            )
                        ),
                        parent_slot_type_signature="parentSlotTypeSignature",
                        slot_type_values=[lex.CfnBot.SlotTypeValueProperty(
                            sample_value=lex.CfnBot.SampleValueProperty(
                                value="value"
                            ),
                
                            # the properties below are optional
                            synonyms=[lex.CfnBot.SampleValueProperty(
                                value="value"
                            )]
                        )],
                        value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                            resolution_strategy="resolutionStrategy",
                
                            # the properties below are optional
                            advanced_recognition_setting=lex.CfnBot.AdvancedRecognitionSettingProperty(
                                audio_recognition_strategy="audioRecognitionStrategy"
                            ),
                            regex_filter=lex.CfnBot.SlotValueRegexFilterProperty(
                                pattern="pattern"
                            )
                        )
                    )],
                    voice_settings=lex.CfnBot.VoiceSettingsProperty(
                        voice_id="voiceId",
                
                        # the properties below are optional
                        engine="engine"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14a82cce828e0d9278905a24c9a75cf3e90c46735547a8a8dd170d77fb8b24dc)
                check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
                check_type(argname="argument nlu_confidence_threshold", value=nlu_confidence_threshold, expected_type=type_hints["nlu_confidence_threshold"])
                check_type(argname="argument custom_vocabulary", value=custom_vocabulary, expected_type=type_hints["custom_vocabulary"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument intents", value=intents, expected_type=type_hints["intents"])
                check_type(argname="argument slot_types", value=slot_types, expected_type=type_hints["slot_types"])
                check_type(argname="argument voice_settings", value=voice_settings, expected_type=type_hints["voice_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "locale_id": locale_id,
                "nlu_confidence_threshold": nlu_confidence_threshold,
            }
            if custom_vocabulary is not None:
                self._values["custom_vocabulary"] = custom_vocabulary
            if description is not None:
                self._values["description"] = description
            if intents is not None:
                self._values["intents"] = intents
            if slot_types is not None:
                self._values["slot_types"] = slot_types
            if voice_settings is not None:
                self._values["voice_settings"] = voice_settings

        @builtins.property
        def locale_id(self) -> builtins.str:
            '''The identifier of the language and locale that the bot will be used in.

            The string must match one of the supported locales.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-localeid
            '''
            result = self._values.get("locale_id")
            assert result is not None, "Required property 'locale_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def nlu_confidence_threshold(self) -> jsii.Number:
            '''Determines the threshold where Amazon Lex will insert the AMAZON.FallbackIntent, AMAZON.KendraSearchIntent, or both when returning alternative intents. You must configure an AMAZON.FallbackIntent. AMAZON.KendraSearchIntent is only inserted if it is configured for the bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-nluconfidencethreshold
            '''
            result = self._values.get("nlu_confidence_threshold")
            assert result is not None, "Required property 'nlu_confidence_threshold' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def custom_vocabulary(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.CustomVocabularyProperty"]]:
            '''Specifies a custom vocabulary to use with a specific locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-customvocabulary
            '''
            result = self._values.get("custom_vocabulary")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.CustomVocabularyProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the bot locale.

            Use this to help identify the bot locale in lists.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def intents(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.IntentProperty"]]]]:
            '''One or more intents defined for the locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-intents
            '''
            result = self._values.get("intents")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.IntentProperty"]]]], result)

        @builtins.property
        def slot_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotTypeProperty"]]]]:
            '''One or more slot types defined for the locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-slottypes
            '''
            result = self._values.get("slot_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotTypeProperty"]]]], result)

        @builtins.property
        def voice_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.VoiceSettingsProperty"]]:
            '''Identifies the Amazon Polly voice used for audio interaction with the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-botlocale.html#cfn-lex-bot-botlocale-voicesettings
            '''
            result = self._values.get("voice_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.VoiceSettingsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotLocaleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.ButtonProperty",
        jsii_struct_bases=[],
        name_mapping={"text": "text", "value": "value"},
    )
    class ButtonProperty:
        def __init__(self, *, text: builtins.str, value: builtins.str) -> None:
            '''Describes a button to use on a response card used to gather slot values from a user.

            :param text: The text that appears on the button. Use this to tell the user the value that is returned when they choose this button.
            :param value: The value returned to Amazon Lex when the user chooses this button. This must be one of the slot values configured for the slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-button.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                button_property = lex.CfnBot.ButtonProperty(
                    text="text",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e07b0e828670df93418cdfd89bf0925e98396b9ebab2dc888ab2f620545f6269)
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "text": text,
                "value": value,
            }

        @builtins.property
        def text(self) -> builtins.str:
            '''The text that appears on the button.

            Use this to tell the user the value that is returned when they choose this button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-button.html#cfn-lex-bot-button-text
            '''
            result = self._values.get("text")
            assert result is not None, "Required property 'text' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value returned to Amazon Lex when the user chooses this button.

            This must be one of the slot values configured for the slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-button.html#cfn-lex-bot-button-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ButtonProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.CloudWatchLogGroupLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
            "log_prefix": "logPrefix",
        },
    )
    class CloudWatchLogGroupLogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_log_group_arn: builtins.str,
            log_prefix: builtins.str,
        ) -> None:
            '''Specifies the Amazon CloudWatch Logs log group where text and metadata logs are delivered.

            The log group must exist before you enable logging.

            :param cloud_watch_log_group_arn: Specifies the Amazon Resource Name (ARN) of the log group where text and metadata logs are delivered.
            :param log_prefix: Specifies the prefix of the log stream name within the log group that you specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-cloudwatchloggrouplogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                cloud_watch_log_group_log_destination_property = lex.CfnBot.CloudWatchLogGroupLogDestinationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    log_prefix="logPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__806f4b049b50e6479a3b78ea5e58b022bc96989949b937c40e2470f9da95fff4)
                check_type(argname="argument cloud_watch_log_group_arn", value=cloud_watch_log_group_arn, expected_type=type_hints["cloud_watch_log_group_arn"])
                check_type(argname="argument log_prefix", value=log_prefix, expected_type=type_hints["log_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cloud_watch_log_group_arn": cloud_watch_log_group_arn,
                "log_prefix": log_prefix,
            }

        @builtins.property
        def cloud_watch_log_group_arn(self) -> builtins.str:
            '''Specifies the Amazon Resource Name (ARN) of the log group where text and metadata logs are delivered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-cloudwatchloggrouplogdestination.html#cfn-lex-bot-cloudwatchloggrouplogdestination-cloudwatchloggrouparn
            '''
            result = self._values.get("cloud_watch_log_group_arn")
            assert result is not None, "Required property 'cloud_watch_log_group_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_prefix(self) -> builtins.str:
            '''Specifies the prefix of the log stream name within the log group that you specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-cloudwatchloggrouplogdestination.html#cfn-lex-bot-cloudwatchloggrouplogdestination-logprefix
            '''
            result = self._values.get("log_prefix")
            assert result is not None, "Required property 'log_prefix' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogGroupLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.CodeHookSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_code_hook": "lambdaCodeHook"},
    )
    class CodeHookSpecificationProperty:
        def __init__(
            self,
            *,
            lambda_code_hook: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.LambdaCodeHookProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Specifies information about code hooks that Amazon Lex calls during a conversation.

            :param lambda_code_hook: Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-codehookspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                code_hook_specification_property = lex.CfnBot.CodeHookSpecificationProperty(
                    lambda_code_hook=lex.CfnBot.LambdaCodeHookProperty(
                        code_hook_interface_version="codeHookInterfaceVersion",
                        lambda_arn="lambdaArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c6f628e13f551982d33a31b7c68467c2e75d803b98bb7bbe438f0d221d19feb)
                check_type(argname="argument lambda_code_hook", value=lambda_code_hook, expected_type=type_hints["lambda_code_hook"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "lambda_code_hook": lambda_code_hook,
            }

        @builtins.property
        def lambda_code_hook(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.LambdaCodeHookProperty"]:
            '''Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-codehookspecification.html#cfn-lex-bot-codehookspecification-lambdacodehook
            '''
            result = self._values.get("lambda_code_hook")
            assert result is not None, "Required property 'lambda_code_hook' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.LambdaCodeHookProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeHookSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.ConversationLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audio_log_settings": "audioLogSettings",
            "text_log_settings": "textLogSettings",
        },
    )
    class ConversationLogSettingsProperty:
        def __init__(
            self,
            *,
            audio_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.AudioLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            text_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.TextLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies settings that manage logging that saves audio, text, and metadata for the conversations with your users.

            :param audio_log_settings: Specifies the Amazon S3 settings for logging audio to an S3 bucket.
            :param text_log_settings: Specifies settings to enable text conversation logs. You specify the Amazon CloudWatch Logs log group and whether logs should be stored for an alias.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conversationlogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                conversation_log_settings_property = lex.CfnBot.ConversationLogSettingsProperty(
                    audio_log_settings=[lex.CfnBot.AudioLogSettingProperty(
                        destination=lex.CfnBot.AudioLogDestinationProperty(
                            s3_bucket=lex.CfnBot.S3BucketLogDestinationProperty(
                                log_prefix="logPrefix",
                                s3_bucket_arn="s3BucketArn",
                
                                # the properties below are optional
                                kms_key_arn="kmsKeyArn"
                            )
                        ),
                        enabled=False
                    )],
                    text_log_settings=[lex.CfnBot.TextLogSettingProperty(
                        destination=lex.CfnBot.TextLogDestinationProperty(
                            cloud_watch=lex.CfnBot.CloudWatchLogGroupLogDestinationProperty(
                                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                                log_prefix="logPrefix"
                            )
                        ),
                        enabled=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__32014d318a463d84d2ee90b10658989e7745be06c4a07c49052abde4628a8ade)
                check_type(argname="argument audio_log_settings", value=audio_log_settings, expected_type=type_hints["audio_log_settings"])
                check_type(argname="argument text_log_settings", value=text_log_settings, expected_type=type_hints["text_log_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audio_log_settings is not None:
                self._values["audio_log_settings"] = audio_log_settings
            if text_log_settings is not None:
                self._values["text_log_settings"] = text_log_settings

        @builtins.property
        def audio_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AudioLogSettingProperty"]]]]:
            '''Specifies the Amazon S3 settings for logging audio to an S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conversationlogsettings.html#cfn-lex-bot-conversationlogsettings-audiologsettings
            '''
            result = self._values.get("audio_log_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AudioLogSettingProperty"]]]], result)

        @builtins.property
        def text_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.TextLogSettingProperty"]]]]:
            '''Specifies settings to enable text conversation logs.

            You specify the Amazon CloudWatch Logs log group and whether logs should be stored for an alias.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-conversationlogsettings.html#cfn-lex-bot-conversationlogsettings-textlogsettings
            '''
            result = self._values.get("text_log_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.TextLogSettingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConversationLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.CustomPayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class CustomPayloadProperty:
        def __init__(self, *, value: builtins.str) -> None:
            '''A custom response string that Amazon Lex sends to your application.

            You define the content and structure of the string.

            :param value: The string that is sent to your application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-custompayload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                custom_payload_property = lex.CfnBot.CustomPayloadProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c211a101090e012075cd5d7de400caf8737378224339c466fc9c98f1c66d972)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''The string that is sent to your application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-custompayload.html#cfn-lex-bot-custompayload-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.CustomVocabularyItemProperty",
        jsii_struct_bases=[],
        name_mapping={"phrase": "phrase", "weight": "weight"},
    )
    class CustomVocabularyItemProperty:
        def __init__(
            self,
            *,
            phrase: builtins.str,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies an entry in a custom vocabulary.

            :param phrase: Specifies 1 - 4 words that should be recognized.
            :param weight: Specifies the degree to which the phrase recognition is boosted. The default value is 1.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabularyitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                custom_vocabulary_item_property = lex.CfnBot.CustomVocabularyItemProperty(
                    phrase="phrase",
                
                    # the properties below are optional
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b46661b9ee8bacad87c11f515448797784114d8fdfb04e124aa3c7a0cfe232a3)
                check_type(argname="argument phrase", value=phrase, expected_type=type_hints["phrase"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "phrase": phrase,
            }
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def phrase(self) -> builtins.str:
            '''Specifies 1 - 4 words that should be recognized.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabularyitem.html#cfn-lex-bot-customvocabularyitem-phrase
            '''
            result = self._values.get("phrase")
            assert result is not None, "Required property 'phrase' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''Specifies the degree to which the phrase recognition is boosted.

            The default value is 1.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabularyitem.html#cfn-lex-bot-customvocabularyitem-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomVocabularyItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.CustomVocabularyProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_vocabulary_items": "customVocabularyItems"},
    )
    class CustomVocabularyProperty:
        def __init__(
            self,
            *,
            custom_vocabulary_items: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.CustomVocabularyItemProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''Specifies a custom vocabulary.

            A custom vocabulary is a list of words that you expect to be used during a conversation with your bot.

            :param custom_vocabulary_items: Specifies a list of words that you expect to be used during a conversation with your bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabulary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                custom_vocabulary_property = lex.CfnBot.CustomVocabularyProperty(
                    custom_vocabulary_items=[lex.CfnBot.CustomVocabularyItemProperty(
                        phrase="phrase",
                
                        # the properties below are optional
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71081a5a4f02cf15b2b9585786d6b5e59f91107b18d6dc2d0f807a12251a9a35)
                check_type(argname="argument custom_vocabulary_items", value=custom_vocabulary_items, expected_type=type_hints["custom_vocabulary_items"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "custom_vocabulary_items": custom_vocabulary_items,
            }

        @builtins.property
        def custom_vocabulary_items(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.CustomVocabularyItemProperty"]]]:
            '''Specifies a list of words that you expect to be used during a conversation with your bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-customvocabulary.html#cfn-lex-bot-customvocabulary-customvocabularyitems
            '''
            result = self._values.get("custom_vocabulary_items")
            assert result is not None, "Required property 'custom_vocabulary_items' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.CustomVocabularyItemProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomVocabularyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.DTMFSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deletion_character": "deletionCharacter",
            "end_character": "endCharacter",
            "end_timeout_ms": "endTimeoutMs",
            "max_length": "maxLength",
        },
    )
    class DTMFSpecificationProperty:
        def __init__(
            self,
            *,
            deletion_character: builtins.str,
            end_character: builtins.str,
            end_timeout_ms: jsii.Number,
            max_length: jsii.Number,
        ) -> None:
            '''
            :param deletion_character: ``CfnBot.DTMFSpecificationProperty.DeletionCharacter``.
            :param end_character: ``CfnBot.DTMFSpecificationProperty.EndCharacter``.
            :param end_timeout_ms: ``CfnBot.DTMFSpecificationProperty.EndTimeoutMs``.
            :param max_length: ``CfnBot.DTMFSpecificationProperty.MaxLength``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dtmfspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                d_tMFSpecification_property = lex.CfnBot.DTMFSpecificationProperty(
                    deletion_character="deletionCharacter",
                    end_character="endCharacter",
                    end_timeout_ms=123,
                    max_length=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bfb971d2a02e83430a9bfb5997fb6398deb433696e160a3d596545bf7b2f93ed)
                check_type(argname="argument deletion_character", value=deletion_character, expected_type=type_hints["deletion_character"])
                check_type(argname="argument end_character", value=end_character, expected_type=type_hints["end_character"])
                check_type(argname="argument end_timeout_ms", value=end_timeout_ms, expected_type=type_hints["end_timeout_ms"])
                check_type(argname="argument max_length", value=max_length, expected_type=type_hints["max_length"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "deletion_character": deletion_character,
                "end_character": end_character,
                "end_timeout_ms": end_timeout_ms,
                "max_length": max_length,
            }

        @builtins.property
        def deletion_character(self) -> builtins.str:
            '''``CfnBot.DTMFSpecificationProperty.DeletionCharacter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dtmfspecification.html#cfn-lex-bot-dtmfspecification-deletioncharacter
            '''
            result = self._values.get("deletion_character")
            assert result is not None, "Required property 'deletion_character' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def end_character(self) -> builtins.str:
            '''``CfnBot.DTMFSpecificationProperty.EndCharacter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dtmfspecification.html#cfn-lex-bot-dtmfspecification-endcharacter
            '''
            result = self._values.get("end_character")
            assert result is not None, "Required property 'end_character' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def end_timeout_ms(self) -> jsii.Number:
            '''``CfnBot.DTMFSpecificationProperty.EndTimeoutMs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dtmfspecification.html#cfn-lex-bot-dtmfspecification-endtimeoutms
            '''
            result = self._values.get("end_timeout_ms")
            assert result is not None, "Required property 'end_timeout_ms' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def max_length(self) -> jsii.Number:
            '''``CfnBot.DTMFSpecificationProperty.MaxLength``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dtmfspecification.html#cfn-lex-bot-dtmfspecification-maxlength
            '''
            result = self._values.get("max_length")
            assert result is not None, "Required property 'max_length' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DTMFSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.DataPrivacyProperty",
        jsii_struct_bases=[],
        name_mapping={"child_directed": "childDirected"},
    )
    class DataPrivacyProperty:
        def __init__(
            self,
            *,
            child_directed: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''
            :param child_directed: ``CfnBot.DataPrivacyProperty.ChildDirected``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dataprivacy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                data_privacy_property = lex.CfnBot.DataPrivacyProperty(
                    child_directed=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e2d76be0ab1d7bef5b2db6f6b7068e3739548eec497c49a26dd5bd2f3955b25)
                check_type(argname="argument child_directed", value=child_directed, expected_type=type_hints["child_directed"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "child_directed": child_directed,
            }

        @builtins.property
        def child_directed(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''``CfnBot.DataPrivacyProperty.ChildDirected``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dataprivacy.html#cfn-lex-bot-dataprivacy-childdirected
            '''
            result = self._values.get("child_directed")
            assert result is not None, "Required property 'child_directed' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataPrivacyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.DialogCodeHookSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class DialogCodeHookSettingProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''Specifies whether an intent uses the dialog code hook during conversations with a user.

            :param enabled: Indicates whether an intent uses the dialog code hook during a conversation with a user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehooksetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                dialog_code_hook_setting_property = lex.CfnBot.DialogCodeHookSettingProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6db6c1b57aa2e6666240e75ea9ff22c796a6d1dcd210a5da32a2412b0d9c6d6b)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Indicates whether an intent uses the dialog code hook during a conversation with a user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-dialogcodehooksetting.html#cfn-lex-bot-dialogcodehooksetting-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DialogCodeHookSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.ExternalSourceSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"grammar_slot_type_setting": "grammarSlotTypeSetting"},
    )
    class ExternalSourceSettingProperty:
        def __init__(
            self,
            *,
            grammar_slot_type_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.GrammarSlotTypeSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information about the external source of the slot type's definition.

            :param grammar_slot_type_setting: Settings required for a slot type based on a grammar that you provide.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-externalsourcesetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                external_source_setting_property = lex.CfnBot.ExternalSourceSettingProperty(
                    grammar_slot_type_setting=lex.CfnBot.GrammarSlotTypeSettingProperty(
                        source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                            s3_bucket_name="s3BucketName",
                            s3_object_key="s3ObjectKey",
                
                            # the properties below are optional
                            kms_key_arn="kmsKeyArn"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__048a8708754b33da941ab48ab56d391c82ce3900f3f968f262b5d4674d4ac1df)
                check_type(argname="argument grammar_slot_type_setting", value=grammar_slot_type_setting, expected_type=type_hints["grammar_slot_type_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if grammar_slot_type_setting is not None:
                self._values["grammar_slot_type_setting"] = grammar_slot_type_setting

        @builtins.property
        def grammar_slot_type_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.GrammarSlotTypeSettingProperty"]]:
            '''Settings required for a slot type based on a grammar that you provide.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-externalsourcesetting.html#cfn-lex-bot-externalsourcesetting-grammarslottypesetting
            '''
            result = self._values.get("grammar_slot_type_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.GrammarSlotTypeSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExternalSourceSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.FulfillmentCodeHookSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "fulfillment_updates_specification": "fulfillmentUpdatesSpecification",
            "post_fulfillment_status_specification": "postFulfillmentStatusSpecification",
        },
    )
    class FulfillmentCodeHookSettingProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            fulfillment_updates_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.FulfillmentUpdatesSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            post_fulfillment_status_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.PostFulfillmentStatusSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Determines if a Lambda function should be invoked for a specific intent.

            :param enabled: Indicates whether a Lambda function should be invoked for fulfill a specific intent.
            :param fulfillment_updates_specification: Provides settings for update messages sent to the user for long-running Lambda fulfillment functions. Fulfillment updates can be used only with streaming conversations.
            :param post_fulfillment_status_specification: Provides settings for messages sent to the user for after the Lambda fulfillment function completes. Post-fulfillment messages can be sent for both streaming and non-streaming conversations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                fulfillment_code_hook_setting_property = lex.CfnBot.FulfillmentCodeHookSettingProperty(
                    enabled=False,
                
                    # the properties below are optional
                    fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                        active=False,
                
                        # the properties below are optional
                        start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                            delay_in_seconds=123,
                            message_groups=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        timeout_in_seconds=123,
                        update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                            frequency_in_seconds=123,
                            message_groups=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        )
                    ),
                    post_fulfillment_status_specification=lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                        failure_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        success_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1af8baef81c0c61a62456ee7bf924fafe3aea02e2719fdda3fdc4618d4336ab)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument fulfillment_updates_specification", value=fulfillment_updates_specification, expected_type=type_hints["fulfillment_updates_specification"])
                check_type(argname="argument post_fulfillment_status_specification", value=post_fulfillment_status_specification, expected_type=type_hints["post_fulfillment_status_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }
            if fulfillment_updates_specification is not None:
                self._values["fulfillment_updates_specification"] = fulfillment_updates_specification
            if post_fulfillment_status_specification is not None:
                self._values["post_fulfillment_status_specification"] = post_fulfillment_status_specification

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Indicates whether a Lambda function should be invoked for fulfill a specific intent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html#cfn-lex-bot-fulfillmentcodehooksetting-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def fulfillment_updates_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.FulfillmentUpdatesSpecificationProperty"]]:
            '''Provides settings for update messages sent to the user for long-running Lambda fulfillment functions.

            Fulfillment updates can be used only with streaming conversations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html#cfn-lex-bot-fulfillmentcodehooksetting-fulfillmentupdatesspecification
            '''
            result = self._values.get("fulfillment_updates_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.FulfillmentUpdatesSpecificationProperty"]], result)

        @builtins.property
        def post_fulfillment_status_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.PostFulfillmentStatusSpecificationProperty"]]:
            '''Provides settings for messages sent to the user for after the Lambda fulfillment function completes.

            Post-fulfillment messages can be sent for both streaming and non-streaming conversations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentcodehooksetting.html#cfn-lex-bot-fulfillmentcodehooksetting-postfulfillmentstatusspecification
            '''
            result = self._values.get("post_fulfillment_status_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.PostFulfillmentStatusSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentCodeHookSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.FulfillmentStartResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delay_in_seconds": "delayInSeconds",
            "message_groups": "messageGroups",
            "allow_interrupt": "allowInterrupt",
        },
    )
    class FulfillmentStartResponseSpecificationProperty:
        def __init__(
            self,
            *,
            delay_in_seconds: jsii.Number,
            message_groups: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.MessageGroupProperty", typing.Dict[builtins.str, typing.Any]]]]],
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Provides settings for a message that is sent to the user when a fulfillment Lambda function starts running.

            :param delay_in_seconds: The delay between when the Lambda fulfillment function starts running and the start message is played. If the Lambda function returns before the delay is over, the start message isn't played.
            :param message_groups: One to 5 message groups that contain start messages. Amazon Lex chooses one of the messages to play to the user.
            :param allow_interrupt: Determines whether the user can interrupt the start message while it is playing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                fulfillment_start_response_specification_property = lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                    delay_in_seconds=123,
                    message_groups=[lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                
                        # the properties below are optional
                        variations=[lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                
                    # the properties below are optional
                    allow_interrupt=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5c837c09978e60daf7cbb23a64f674b8400d6cf47a63a3f86f5e0505b25e1d7)
                check_type(argname="argument delay_in_seconds", value=delay_in_seconds, expected_type=type_hints["delay_in_seconds"])
                check_type(argname="argument message_groups", value=message_groups, expected_type=type_hints["message_groups"])
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "delay_in_seconds": delay_in_seconds,
                "message_groups": message_groups,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt

        @builtins.property
        def delay_in_seconds(self) -> jsii.Number:
            '''The delay between when the Lambda fulfillment function starts running and the start message is played.

            If the Lambda function returns before the delay is over, the start message isn't played.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html#cfn-lex-bot-fulfillmentstartresponsespecification-delayinseconds
            '''
            result = self._values.get("delay_in_seconds")
            assert result is not None, "Required property 'delay_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def message_groups(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageGroupProperty"]]]:
            '''One to 5 message groups that contain start messages.

            Amazon Lex chooses one of the messages to play to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html#cfn-lex-bot-fulfillmentstartresponsespecification-messagegroups
            '''
            result = self._values.get("message_groups")
            assert result is not None, "Required property 'message_groups' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageGroupProperty"]]], result)

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Determines whether the user can interrupt the start message while it is playing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentstartresponsespecification.html#cfn-lex-bot-fulfillmentstartresponsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentStartResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "frequency_in_seconds": "frequencyInSeconds",
            "message_groups": "messageGroups",
            "allow_interrupt": "allowInterrupt",
        },
    )
    class FulfillmentUpdateResponseSpecificationProperty:
        def __init__(
            self,
            *,
            frequency_in_seconds: jsii.Number,
            message_groups: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.MessageGroupProperty", typing.Dict[builtins.str, typing.Any]]]]],
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Provides information for updating the user on the progress of fulfilling an intent.

            :param frequency_in_seconds: The frequency that a message is sent to the user. When the period ends, Amazon Lex chooses a message from the message groups and plays it to the user. If the fulfillment Lambda function returns before the first period ends, an update message is not played to the user.
            :param message_groups: One to 5 message groups that contain update messages. Amazon Lex chooses one of the messages to play to the user.
            :param allow_interrupt: Determines whether the user can interrupt an update message while it is playing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                fulfillment_update_response_specification_property = lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                    frequency_in_seconds=123,
                    message_groups=[lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                
                        # the properties below are optional
                        variations=[lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                
                    # the properties below are optional
                    allow_interrupt=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e487335482a27d40419de8fafb4e65ca6ec2162d42335b306f9bc03a11781d9b)
                check_type(argname="argument frequency_in_seconds", value=frequency_in_seconds, expected_type=type_hints["frequency_in_seconds"])
                check_type(argname="argument message_groups", value=message_groups, expected_type=type_hints["message_groups"])
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "frequency_in_seconds": frequency_in_seconds,
                "message_groups": message_groups,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt

        @builtins.property
        def frequency_in_seconds(self) -> jsii.Number:
            '''The frequency that a message is sent to the user.

            When the period ends, Amazon Lex chooses a message from the message groups and plays it to the user. If the fulfillment Lambda function returns before the first period ends, an update message is not played to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html#cfn-lex-bot-fulfillmentupdateresponsespecification-frequencyinseconds
            '''
            result = self._values.get("frequency_in_seconds")
            assert result is not None, "Required property 'frequency_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def message_groups(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageGroupProperty"]]]:
            '''One to 5 message groups that contain update messages.

            Amazon Lex chooses one of the messages to play to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html#cfn-lex-bot-fulfillmentupdateresponsespecification-messagegroups
            '''
            result = self._values.get("message_groups")
            assert result is not None, "Required property 'message_groups' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageGroupProperty"]]], result)

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Determines whether the user can interrupt an update message while it is playing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdateresponsespecification.html#cfn-lex-bot-fulfillmentupdateresponsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentUpdateResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.FulfillmentUpdatesSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active": "active",
            "start_response": "startResponse",
            "timeout_in_seconds": "timeoutInSeconds",
            "update_response": "updateResponse",
        },
    )
    class FulfillmentUpdatesSpecificationProperty:
        def __init__(
            self,
            *,
            active: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            start_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.FulfillmentStartResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
            update_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.FulfillmentUpdateResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information for updating the user on the progress of fulfilling an intent.

            :param active: Determines whether fulfillment updates are sent to the user. When this field is true, updates are sent. If the active field is set to true, the ``startResponse`` , ``updateResponse`` , and ``timeoutInSeconds`` fields are required.
            :param start_response: Provides configuration information for the message sent to users when the fulfillment Lambda functions starts running.
            :param timeout_in_seconds: The length of time that the fulfillment Lambda function should run before it times out.
            :param update_response: Provides configuration information for messages sent periodically to the user while the fulfillment Lambda function is running.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                fulfillment_updates_specification_property = lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                    active=False,
                
                    # the properties below are optional
                    start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                        delay_in_seconds=123,
                        message_groups=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    timeout_in_seconds=123,
                    update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                        frequency_in_seconds=123,
                        message_groups=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39910e837bc526af16f790a41689555e6b51358c1ab7bcce794884105453298f)
                check_type(argname="argument active", value=active, expected_type=type_hints["active"])
                check_type(argname="argument start_response", value=start_response, expected_type=type_hints["start_response"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
                check_type(argname="argument update_response", value=update_response, expected_type=type_hints["update_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "active": active,
            }
            if start_response is not None:
                self._values["start_response"] = start_response
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds
            if update_response is not None:
                self._values["update_response"] = update_response

        @builtins.property
        def active(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Determines whether fulfillment updates are sent to the user. When this field is true, updates are sent.

            If the active field is set to true, the ``startResponse`` , ``updateResponse`` , and ``timeoutInSeconds`` fields are required.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-active
            '''
            result = self._values.get("active")
            assert result is not None, "Required property 'active' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def start_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.FulfillmentStartResponseSpecificationProperty"]]:
            '''Provides configuration information for the message sent to users when the fulfillment Lambda functions starts running.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-startresponse
            '''
            result = self._values.get("start_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.FulfillmentStartResponseSpecificationProperty"]], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The length of time that the fulfillment Lambda function should run before it times out.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def update_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.FulfillmentUpdateResponseSpecificationProperty"]]:
            '''Provides configuration information for messages sent periodically to the user while the fulfillment Lambda function is running.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-fulfillmentupdatesspecification.html#cfn-lex-bot-fulfillmentupdatesspecification-updateresponse
            '''
            result = self._values.get("update_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.FulfillmentUpdateResponseSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FulfillmentUpdatesSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.GrammarSlotTypeSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class GrammarSlotTypeSettingProperty:
        def __init__(
            self,
            *,
            source: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.GrammarSlotTypeSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings required for a slot type based on a grammar that you provide.

            :param source: The source of the grammar used to create the slot type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                grammar_slot_type_setting_property = lex.CfnBot.GrammarSlotTypeSettingProperty(
                    source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                        s3_bucket_name="s3BucketName",
                        s3_object_key="s3ObjectKey",
                
                        # the properties below are optional
                        kms_key_arn="kmsKeyArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__210e6a6be1d893b8ccec42063ee2fe87b51c9b808e6cb0989d0d1f35d11766a3)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.GrammarSlotTypeSourceProperty"]]:
            '''The source of the grammar used to create the slot type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesetting.html#cfn-lex-bot-grammarslottypesetting-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.GrammarSlotTypeSourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrammarSlotTypeSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.GrammarSlotTypeSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket_name": "s3BucketName",
            "s3_object_key": "s3ObjectKey",
            "kms_key_arn": "kmsKeyArn",
        },
    )
    class GrammarSlotTypeSourceProperty:
        def __init__(
            self,
            *,
            s3_bucket_name: builtins.str,
            s3_object_key: builtins.str,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the Amazon S3 bucket name and location for the grammar that is the source of the slot type.

            :param s3_bucket_name: The name of the S3 bucket that contains the grammar source.
            :param s3_object_key: The path to the grammar in the S3 bucket.
            :param kms_key_arn: The AWS Key Management Service key required to decrypt the contents of the grammar, if any.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                grammar_slot_type_source_property = lex.CfnBot.GrammarSlotTypeSourceProperty(
                    s3_bucket_name="s3BucketName",
                    s3_object_key="s3ObjectKey",
                
                    # the properties below are optional
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a20ef2820e59b1dd5b1476f1bd0d744e9a1d190fa43c225298a906e7b8a9a959)
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument s3_object_key", value=s3_object_key, expected_type=type_hints["s3_object_key"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket_name": s3_bucket_name,
                "s3_object_key": s3_object_key,
            }
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def s3_bucket_name(self) -> builtins.str:
            '''The name of the S3 bucket that contains the grammar source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html#cfn-lex-bot-grammarslottypesource-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            assert result is not None, "Required property 's3_bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_object_key(self) -> builtins.str:
            '''The path to the grammar in the S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html#cfn-lex-bot-grammarslottypesource-s3objectkey
            '''
            result = self._values.get("s3_object_key")
            assert result is not None, "Required property 's3_object_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The AWS Key Management Service key required to decrypt the contents of the grammar, if any.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-grammarslottypesource.html#cfn-lex-bot-grammarslottypesource-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrammarSlotTypeSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.ImageResponseCardProperty",
        jsii_struct_bases=[],
        name_mapping={
            "title": "title",
            "buttons": "buttons",
            "image_url": "imageUrl",
            "subtitle": "subtitle",
        },
    )
    class ImageResponseCardProperty:
        def __init__(
            self,
            *,
            title: builtins.str,
            buttons: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ButtonProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            image_url: typing.Optional[builtins.str] = None,
            subtitle: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A card that is shown to the user by a messaging platform.

            You define the contents of the card, the card is displayed by the platform.

            When you use a response card, the response from the user is constrained to the text associated with a button on the card.

            :param title: The title to display on the response card. The format of the title is determined by the platform displaying the response card.
            :param buttons: A list of buttons that should be displayed on the response card. The arrangement of the buttons is determined by the platform that displays the buttons.
            :param image_url: The URL of an image to display on the response card. The image URL must be publicly available so that the platform displaying the response card has access to the image.
            :param subtitle: The subtitle to display on the response card. The format of the subtitle is determined by the platform displaying the response card.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                image_response_card_property = lex.CfnBot.ImageResponseCardProperty(
                    title="title",
                
                    # the properties below are optional
                    buttons=[lex.CfnBot.ButtonProperty(
                        text="text",
                        value="value"
                    )],
                    image_url="imageUrl",
                    subtitle="subtitle"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a7ecf08a64930d06e6b17db57f7c8a056f6d3c9cb420c75ed1e4332b229e6a0)
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument buttons", value=buttons, expected_type=type_hints["buttons"])
                check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
                check_type(argname="argument subtitle", value=subtitle, expected_type=type_hints["subtitle"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "title": title,
            }
            if buttons is not None:
                self._values["buttons"] = buttons
            if image_url is not None:
                self._values["image_url"] = image_url
            if subtitle is not None:
                self._values["subtitle"] = subtitle

        @builtins.property
        def title(self) -> builtins.str:
            '''The title to display on the response card.

            The format of the title is determined by the platform displaying the response card.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-title
            '''
            result = self._values.get("title")
            assert result is not None, "Required property 'title' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def buttons(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ButtonProperty"]]]]:
            '''A list of buttons that should be displayed on the response card.

            The arrangement of the buttons is determined by the platform that displays the buttons.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-buttons
            '''
            result = self._values.get("buttons")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ButtonProperty"]]]], result)

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            '''The URL of an image to display on the response card.

            The image URL must be publicly available so that the platform displaying the response card has access to the image.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-imageurl
            '''
            result = self._values.get("image_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subtitle(self) -> typing.Optional[builtins.str]:
            '''The subtitle to display on the response card.

            The format of the subtitle is determined by the platform displaying the response card.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-imageresponsecard.html#cfn-lex-bot-imageresponsecard-subtitle
            '''
            result = self._values.get("subtitle")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageResponseCardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.InputContextProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class InputContextProperty:
        def __init__(self, *, name: builtins.str) -> None:
            '''The name of a context that must be active for an intent to be selected by Amazon Lex .

            :param name: The name of the context.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-inputcontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                input_context_property = lex.CfnBot.InputContextProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__463a1f987a2cb01a67601736d8400c21d1b87c7cf7b0b1ad813834354595ef1c)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the context.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-inputcontext.html#cfn-lex-bot-inputcontext-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.IntentClosingSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"closing_response": "closingResponse", "is_active": "isActive"},
    )
    class IntentClosingSettingProperty:
        def __init__(
            self,
            *,
            closing_response: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]],
            is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Provides a statement the Amazon Lex conveys to the user when the intent is successfully fulfilled.

            :param closing_response: The response that Amazon Lex sends to the user when the intent is complete.
            :param is_active: Specifies whether an intent's closing response is used. When this field is false, the closing response isn't sent to the user and no closing input from the user is used. If the IsActive field isn't specified, the default is true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                intent_closing_setting_property = lex.CfnBot.IntentClosingSettingProperty(
                    closing_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                
                    # the properties below are optional
                    is_active=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84a50abb93edc02417385fd143fcebc88e655c5bc38c884a5f11a6f611eed6c6)
                check_type(argname="argument closing_response", value=closing_response, expected_type=type_hints["closing_response"])
                check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "closing_response": closing_response,
            }
            if is_active is not None:
                self._values["is_active"] = is_active

        @builtins.property
        def closing_response(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"]:
            '''The response that Amazon Lex sends to the user when the intent is complete.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html#cfn-lex-bot-intentclosingsetting-closingresponse
            '''
            result = self._values.get("closing_response")
            assert result is not None, "Required property 'closing_response' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies whether an intent's closing response is used.

            When this field is false, the closing response isn't sent to the user and no closing input from the user is used. If the IsActive field isn't specified, the default is true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentclosingsetting.html#cfn-lex-bot-intentclosingsetting-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntentClosingSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.IntentConfirmationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "declination_response": "declinationResponse",
            "prompt_specification": "promptSpecification",
            "is_active": "isActive",
        },
    )
    class IntentConfirmationSettingProperty:
        def __init__(
            self,
            *,
            declination_response: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]],
            prompt_specification: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.PromptSpecificationProperty", typing.Dict[builtins.str, typing.Any]]],
            is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Provides a prompt for making sure that the user is ready for the intent to be fulfilled.

            :param declination_response: When the user answers "no" to the question defined in PromptSpecification, Amazon Lex responds with this response to acknowledge that the intent was canceled.
            :param prompt_specification: Prompts the user to confirm the intent. This question should have a yes or no answer.
            :param is_active: Specifies whether the intent's confirmation is sent to the user. When this field is false, confirmation and declination responses aren't sent and processing continues as if the responses aren't present. If the active field isn't specified, the default is true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                intent_confirmation_setting_property = lex.CfnBot.IntentConfirmationSettingProperty(
                    declination_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        max_retries=123,
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False,
                        message_selection_strategy="messageSelectionStrategy",
                        prompt_attempts_specification={
                            "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                    allow_audio_input=False,
                                    allow_dtmf_input=False
                                ),
                
                                # the properties below are optional
                                allow_interrupt=False,
                                audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                    start_timeout_ms=123,
                
                                    # the properties below are optional
                                    audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                        end_timeout_ms=123,
                                        max_length_ms=123
                                    ),
                                    dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                        deletion_character="deletionCharacter",
                                        end_character="endCharacter",
                                        end_timeout_ms=123,
                                        max_length=123
                                    )
                                ),
                                text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                    start_timeout_ms=123
                                )
                            )
                        }
                    ),
                
                    # the properties below are optional
                    is_active=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6755d2bd884e0fe8ebf89d12d66f855302dbed5688f50bf3fb7cdd04643880d8)
                check_type(argname="argument declination_response", value=declination_response, expected_type=type_hints["declination_response"])
                check_type(argname="argument prompt_specification", value=prompt_specification, expected_type=type_hints["prompt_specification"])
                check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "declination_response": declination_response,
                "prompt_specification": prompt_specification,
            }
            if is_active is not None:
                self._values["is_active"] = is_active

        @builtins.property
        def declination_response(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"]:
            '''When the user answers "no" to the question defined in PromptSpecification, Amazon Lex responds with this response to acknowledge that the intent was canceled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-declinationresponse
            '''
            result = self._values.get("declination_response")
            assert result is not None, "Required property 'declination_response' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"], result)

        @builtins.property
        def prompt_specification(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.PromptSpecificationProperty"]:
            '''Prompts the user to confirm the intent.

            This question should have a yes or no answer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-promptspecification
            '''
            result = self._values.get("prompt_specification")
            assert result is not None, "Required property 'prompt_specification' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.PromptSpecificationProperty"], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies whether the intent's confirmation is sent to the user.

            When this field is false, confirmation and declination responses aren't sent and processing continues as if the responses aren't present. If the active field isn't specified, the default is true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intentconfirmationsetting.html#cfn-lex-bot-intentconfirmationsetting-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntentConfirmationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.IntentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "description": "description",
            "dialog_code_hook": "dialogCodeHook",
            "fulfillment_code_hook": "fulfillmentCodeHook",
            "input_contexts": "inputContexts",
            "intent_closing_setting": "intentClosingSetting",
            "intent_confirmation_setting": "intentConfirmationSetting",
            "kendra_configuration": "kendraConfiguration",
            "output_contexts": "outputContexts",
            "parent_intent_signature": "parentIntentSignature",
            "sample_utterances": "sampleUtterances",
            "slot_priorities": "slotPriorities",
            "slots": "slots",
        },
    )
    class IntentProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            description: typing.Optional[builtins.str] = None,
            dialog_code_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.DialogCodeHookSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            fulfillment_code_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.FulfillmentCodeHookSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            input_contexts: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.InputContextProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            intent_closing_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.IntentClosingSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            intent_confirmation_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.IntentConfirmationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kendra_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.KendraConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            output_contexts: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.OutputContextProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            parent_intent_signature: typing.Optional[builtins.str] = None,
            sample_utterances: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SampleUtteranceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            slot_priorities: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SlotPriorityProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            slots: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SlotProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Represents an action that the user wants to perform.

            :param name: The name of the intent. Intent names must be unique within the locale that contains the intent and can't match the name of any built-in intent.
            :param description: A description of the intent. Use the description to help identify the intent in lists.
            :param dialog_code_hook: Specifies that Amazon Lex invokes the alias Lambda function for each user input. You can invoke this Lambda function to personalize user interaction.
            :param fulfillment_code_hook: Specifies that Amazon Lex invokes the alias Lambda function when the intent is ready for fulfillment. You can invoke this function to complete the bot's transaction with the user.
            :param input_contexts: A list of contexts that must be active for this intent to be considered by Amazon Lex .
            :param intent_closing_setting: Sets the response that Amazon Lex sends to the user when the intent is closed.
            :param intent_confirmation_setting: Provides prompts that Amazon Lex sends to the user to confirm the completion of an intent. If the user answers "no," the settings contain a statement that is sent to the user to end the intent.
            :param kendra_configuration: Configuration information required to use the AMAZON.KendraSearchIntent intent to connect to an Amazon Kendra index. The AMAZON.KendraSearchIntent intent is called when Amazon Lex can't determine another intent to invoke.
            :param output_contexts: A list of contexts that the intent activates when it is fulfilled.
            :param parent_intent_signature: A unique identifier for the built-in intent to base this intent on.
            :param sample_utterances: A list of utterances that a user might say to signal the intent.
            :param slot_priorities: Indicates the priority for slots. Amazon Lex prompts the user for slot values in priority order.
            :param slots: A list of slots that the intent requires for fulfillment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                intent_property = lex.CfnBot.IntentProperty(
                    name="name",
                
                    # the properties below are optional
                    description="description",
                    dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                        enabled=False
                    ),
                    fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                        enabled=False,
                
                        # the properties below are optional
                        fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                            active=False,
                
                            # the properties below are optional
                            start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                                delay_in_seconds=123,
                                message_groups=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            timeout_in_seconds=123,
                            update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                                frequency_in_seconds=123,
                                message_groups=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            )
                        ),
                        post_fulfillment_status_specification=lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                            failure_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            success_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            )
                        )
                    ),
                    input_contexts=[lex.CfnBot.InputContextProperty(
                        name="name"
                    )],
                    intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                        closing_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                
                        # the properties below are optional
                        is_active=False
                    ),
                    intent_confirmation_setting=lex.CfnBot.IntentConfirmationSettingProperty(
                        declination_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            max_retries=123,
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False,
                            message_selection_strategy="messageSelectionStrategy",
                            prompt_attempts_specification={
                                "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                    allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                        allow_audio_input=False,
                                        allow_dtmf_input=False
                                    ),
                
                                    # the properties below are optional
                                    allow_interrupt=False,
                                    audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                        start_timeout_ms=123,
                
                                        # the properties below are optional
                                        audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                            end_timeout_ms=123,
                                            max_length_ms=123
                                        ),
                                        dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                            deletion_character="deletionCharacter",
                                            end_character="endCharacter",
                                            end_timeout_ms=123,
                                            max_length=123
                                        )
                                    ),
                                    text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                        start_timeout_ms=123
                                    )
                                )
                            }
                        ),
                
                        # the properties below are optional
                        is_active=False
                    ),
                    kendra_configuration=lex.CfnBot.KendraConfigurationProperty(
                        kendra_index="kendraIndex",
                
                        # the properties below are optional
                        query_filter_string="queryFilterString",
                        query_filter_string_enabled=False
                    ),
                    output_contexts=[lex.CfnBot.OutputContextProperty(
                        name="name",
                        time_to_live_in_seconds=123,
                        turns_to_live=123
                    )],
                    parent_intent_signature="parentIntentSignature",
                    sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                        utterance="utterance"
                    )],
                    slot_priorities=[lex.CfnBot.SlotPriorityProperty(
                        priority=123,
                        slot_name="slotName"
                    )],
                    slots=[lex.CfnBot.SlotProperty(
                        name="name",
                        slot_type_name="slotTypeName",
                        value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                            slot_constraint="slotConstraint",
                
                            # the properties below are optional
                            default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                                default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                                    default_value="defaultValue"
                                )]
                            ),
                            prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                max_retries=123,
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False,
                                message_selection_strategy="messageSelectionStrategy",
                                prompt_attempts_specification={
                                    "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                        allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                            allow_audio_input=False,
                                            allow_dtmf_input=False
                                        ),
                
                                        # the properties below are optional
                                        allow_interrupt=False,
                                        audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                            start_timeout_ms=123,
                
                                            # the properties below are optional
                                            audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                                end_timeout_ms=123,
                                                max_length_ms=123
                                            ),
                                            dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                                deletion_character="deletionCharacter",
                                                end_character="endCharacter",
                                                end_timeout_ms=123,
                                                max_length=123
                                            )
                                        ),
                                        text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                            start_timeout_ms=123
                                        )
                                    )
                                }
                            ),
                            sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                                utterance="utterance"
                            )],
                            wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                                continue_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                
                                # the properties below are optional
                                is_active=False,
                                still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                                    frequency_in_seconds=123,
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
                
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
                
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
                                    timeout_in_seconds=123,
                
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            )
                        ),
                
                        # the properties below are optional
                        description="description",
                        multiple_values_setting=lex.CfnBot.MultipleValuesSettingProperty(
                            allow_multiple_values=False
                        ),
                        obfuscation_setting=lex.CfnBot.ObfuscationSettingProperty(
                            obfuscation_setting_type="obfuscationSettingType"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__323e343dae13e36ad470edd5cb08b6c34db83ca1b509e8d1f5ae76058728fbeb)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument dialog_code_hook", value=dialog_code_hook, expected_type=type_hints["dialog_code_hook"])
                check_type(argname="argument fulfillment_code_hook", value=fulfillment_code_hook, expected_type=type_hints["fulfillment_code_hook"])
                check_type(argname="argument input_contexts", value=input_contexts, expected_type=type_hints["input_contexts"])
                check_type(argname="argument intent_closing_setting", value=intent_closing_setting, expected_type=type_hints["intent_closing_setting"])
                check_type(argname="argument intent_confirmation_setting", value=intent_confirmation_setting, expected_type=type_hints["intent_confirmation_setting"])
                check_type(argname="argument kendra_configuration", value=kendra_configuration, expected_type=type_hints["kendra_configuration"])
                check_type(argname="argument output_contexts", value=output_contexts, expected_type=type_hints["output_contexts"])
                check_type(argname="argument parent_intent_signature", value=parent_intent_signature, expected_type=type_hints["parent_intent_signature"])
                check_type(argname="argument sample_utterances", value=sample_utterances, expected_type=type_hints["sample_utterances"])
                check_type(argname="argument slot_priorities", value=slot_priorities, expected_type=type_hints["slot_priorities"])
                check_type(argname="argument slots", value=slots, expected_type=type_hints["slots"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if description is not None:
                self._values["description"] = description
            if dialog_code_hook is not None:
                self._values["dialog_code_hook"] = dialog_code_hook
            if fulfillment_code_hook is not None:
                self._values["fulfillment_code_hook"] = fulfillment_code_hook
            if input_contexts is not None:
                self._values["input_contexts"] = input_contexts
            if intent_closing_setting is not None:
                self._values["intent_closing_setting"] = intent_closing_setting
            if intent_confirmation_setting is not None:
                self._values["intent_confirmation_setting"] = intent_confirmation_setting
            if kendra_configuration is not None:
                self._values["kendra_configuration"] = kendra_configuration
            if output_contexts is not None:
                self._values["output_contexts"] = output_contexts
            if parent_intent_signature is not None:
                self._values["parent_intent_signature"] = parent_intent_signature
            if sample_utterances is not None:
                self._values["sample_utterances"] = sample_utterances
            if slot_priorities is not None:
                self._values["slot_priorities"] = slot_priorities
            if slots is not None:
                self._values["slots"] = slots

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the intent.

            Intent names must be unique within the locale that contains the intent and can't match the name of any built-in intent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the intent.

            Use the description to help identify the intent in lists.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dialog_code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.DialogCodeHookSettingProperty"]]:
            '''Specifies that Amazon Lex invokes the alias Lambda function for each user input.

            You can invoke this Lambda function to personalize user interaction.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-dialogcodehook
            '''
            result = self._values.get("dialog_code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.DialogCodeHookSettingProperty"]], result)

        @builtins.property
        def fulfillment_code_hook(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.FulfillmentCodeHookSettingProperty"]]:
            '''Specifies that Amazon Lex invokes the alias Lambda function when the intent is ready for fulfillment.

            You can invoke this function to complete the bot's transaction with the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-fulfillmentcodehook
            '''
            result = self._values.get("fulfillment_code_hook")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.FulfillmentCodeHookSettingProperty"]], result)

        @builtins.property
        def input_contexts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.InputContextProperty"]]]]:
            '''A list of contexts that must be active for this intent to be considered by Amazon Lex .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-inputcontexts
            '''
            result = self._values.get("input_contexts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.InputContextProperty"]]]], result)

        @builtins.property
        def intent_closing_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.IntentClosingSettingProperty"]]:
            '''Sets the response that Amazon Lex sends to the user when the intent is closed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-intentclosingsetting
            '''
            result = self._values.get("intent_closing_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.IntentClosingSettingProperty"]], result)

        @builtins.property
        def intent_confirmation_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.IntentConfirmationSettingProperty"]]:
            '''Provides prompts that Amazon Lex sends to the user to confirm the completion of an intent.

            If the user answers "no," the settings contain a statement that is sent to the user to end the intent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-intentconfirmationsetting
            '''
            result = self._values.get("intent_confirmation_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.IntentConfirmationSettingProperty"]], result)

        @builtins.property
        def kendra_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.KendraConfigurationProperty"]]:
            '''Configuration information required to use the AMAZON.KendraSearchIntent intent to connect to an Amazon Kendra index. The AMAZON.KendraSearchIntent intent is called when Amazon Lex can't determine another intent to invoke.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-kendraconfiguration
            '''
            result = self._values.get("kendra_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.KendraConfigurationProperty"]], result)

        @builtins.property
        def output_contexts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.OutputContextProperty"]]]]:
            '''A list of contexts that the intent activates when it is fulfilled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-outputcontexts
            '''
            result = self._values.get("output_contexts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.OutputContextProperty"]]]], result)

        @builtins.property
        def parent_intent_signature(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for the built-in intent to base this intent on.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-parentintentsignature
            '''
            result = self._values.get("parent_intent_signature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sample_utterances(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SampleUtteranceProperty"]]]]:
            '''A list of utterances that a user might say to signal the intent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-sampleutterances
            '''
            result = self._values.get("sample_utterances")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SampleUtteranceProperty"]]]], result)

        @builtins.property
        def slot_priorities(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotPriorityProperty"]]]]:
            '''Indicates the priority for slots.

            Amazon Lex prompts the user for slot values in priority order.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-slotpriorities
            '''
            result = self._values.get("slot_priorities")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotPriorityProperty"]]]], result)

        @builtins.property
        def slots(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotProperty"]]]]:
            '''A list of slots that the intent requires for fulfillment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-intent.html#cfn-lex-bot-intent-slots
            '''
            result = self._values.get("slots")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.KendraConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kendra_index": "kendraIndex",
            "query_filter_string": "queryFilterString",
            "query_filter_string_enabled": "queryFilterStringEnabled",
        },
    )
    class KendraConfigurationProperty:
        def __init__(
            self,
            *,
            kendra_index: builtins.str,
            query_filter_string: typing.Optional[builtins.str] = None,
            query_filter_string_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Provides configuration information for the AMAZON.KendraSearchIntent intent. When you use this intent, Amazon Lex searches the specified Amazon Kendra index and returns documents from the index that match the user's utterance.

            :param kendra_index: The Amazon Resource Name (ARN) of the Amazon Kendra index that you want the AMAZON.KendraSearchIntent intent to search. The index must be in the same account and Region as the Amazon Lex bot.
            :param query_filter_string: A query filter that Amazon Lex sends to Amazon Kendra to filter the response from a query. The filter is in the format defined by Amazon Kendra.
            :param query_filter_string_enabled: Determines whether the AMAZON.KendraSearchIntent intent uses a custom query string to query the Amazon Kendra index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                kendra_configuration_property = lex.CfnBot.KendraConfigurationProperty(
                    kendra_index="kendraIndex",
                
                    # the properties below are optional
                    query_filter_string="queryFilterString",
                    query_filter_string_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0bb9f546d3f89e926d37429c339515442456de4678657645fd465fdc193aae3)
                check_type(argname="argument kendra_index", value=kendra_index, expected_type=type_hints["kendra_index"])
                check_type(argname="argument query_filter_string", value=query_filter_string, expected_type=type_hints["query_filter_string"])
                check_type(argname="argument query_filter_string_enabled", value=query_filter_string_enabled, expected_type=type_hints["query_filter_string_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "kendra_index": kendra_index,
            }
            if query_filter_string is not None:
                self._values["query_filter_string"] = query_filter_string
            if query_filter_string_enabled is not None:
                self._values["query_filter_string_enabled"] = query_filter_string_enabled

        @builtins.property
        def kendra_index(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the Amazon Kendra index that you want the AMAZON.KendraSearchIntent intent to search. The index must be in the same account and Region as the Amazon Lex bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html#cfn-lex-bot-kendraconfiguration-kendraindex
            '''
            result = self._values.get("kendra_index")
            assert result is not None, "Required property 'kendra_index' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def query_filter_string(self) -> typing.Optional[builtins.str]:
            '''A query filter that Amazon Lex sends to Amazon Kendra to filter the response from a query.

            The filter is in the format defined by Amazon Kendra.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html#cfn-lex-bot-kendraconfiguration-queryfilterstring
            '''
            result = self._values.get("query_filter_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query_filter_string_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Determines whether the AMAZON.KendraSearchIntent intent uses a custom query string to query the Amazon Kendra index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-kendraconfiguration.html#cfn-lex-bot-kendraconfiguration-queryfilterstringenabled
            '''
            result = self._values.get("query_filter_string_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KendraConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.LambdaCodeHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_hook_interface_version": "codeHookInterfaceVersion",
            "lambda_arn": "lambdaArn",
        },
    )
    class LambdaCodeHookProperty:
        def __init__(
            self,
            *,
            code_hook_interface_version: builtins.str,
            lambda_arn: builtins.str,
        ) -> None:
            '''Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :param code_hook_interface_version: Specifies the version of the request-response that you want Amazon Lex to use to invoke your Lambda function.
            :param lambda_arn: Specifies the Amazon Resource Name (ARN) of the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-lambdacodehook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                lambda_code_hook_property = lex.CfnBot.LambdaCodeHookProperty(
                    code_hook_interface_version="codeHookInterfaceVersion",
                    lambda_arn="lambdaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__000a905b020cf2b73e24d3ce2f15b78ddf65fc4c3f883e0fd9ba73fe153f36a9)
                check_type(argname="argument code_hook_interface_version", value=code_hook_interface_version, expected_type=type_hints["code_hook_interface_version"])
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "code_hook_interface_version": code_hook_interface_version,
                "lambda_arn": lambda_arn,
            }

        @builtins.property
        def code_hook_interface_version(self) -> builtins.str:
            '''Specifies the version of the request-response that you want Amazon Lex to use to invoke your Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-lambdacodehook.html#cfn-lex-bot-lambdacodehook-codehookinterfaceversion
            '''
            result = self._values.get("code_hook_interface_version")
            assert result is not None, "Required property 'code_hook_interface_version' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def lambda_arn(self) -> builtins.str:
            '''Specifies the Amazon Resource Name (ARN) of the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-lambdacodehook.html#cfn-lex-bot-lambdacodehook-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            assert result is not None, "Required property 'lambda_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaCodeHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.MessageGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"message": "message", "variations": "variations"},
    )
    class MessageGroupProperty:
        def __init__(
            self,
            *,
            message: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.MessageProperty", typing.Dict[builtins.str, typing.Any]]],
            variations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.MessageProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides one or more messages that Amazon Lex should send to the user.

            :param message: The primary message that Amazon Lex should send to the user.
            :param variations: Message variations to send to the user. When variations are defined, Amazon Lex chooses the primary message or one of the variations to send to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-messagegroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                message_group_property = lex.CfnBot.MessageGroupProperty(
                    message=lex.CfnBot.MessageProperty(
                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                            value="value"
                        ),
                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                            title="title",
                
                            # the properties below are optional
                            buttons=[lex.CfnBot.ButtonProperty(
                                text="text",
                                value="value"
                            )],
                            image_url="imageUrl",
                            subtitle="subtitle"
                        ),
                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                            value="value"
                        ),
                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                            value="value"
                        )
                    ),
                
                    # the properties below are optional
                    variations=[lex.CfnBot.MessageProperty(
                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                            value="value"
                        ),
                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                            title="title",
                
                            # the properties below are optional
                            buttons=[lex.CfnBot.ButtonProperty(
                                text="text",
                                value="value"
                            )],
                            image_url="imageUrl",
                            subtitle="subtitle"
                        ),
                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                            value="value"
                        ),
                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                            value="value"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f95db70ba8a36be1eec43206a32e3ea68be1689c4756d582cf22679de6ff863)
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                check_type(argname="argument variations", value=variations, expected_type=type_hints["variations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "message": message,
            }
            if variations is not None:
                self._values["variations"] = variations

        @builtins.property
        def message(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageProperty"]:
            '''The primary message that Amazon Lex should send to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-messagegroup.html#cfn-lex-bot-messagegroup-message
            '''
            result = self._values.get("message")
            assert result is not None, "Required property 'message' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageProperty"], result)

        @builtins.property
        def variations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageProperty"]]]]:
            '''Message variations to send to the user.

            When variations are defined, Amazon Lex chooses the primary message or one of the variations to send to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-messagegroup.html#cfn-lex-bot-messagegroup-variations
            '''
            result = self._values.get("variations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.MessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_payload": "customPayload",
            "image_response_card": "imageResponseCard",
            "plain_text_message": "plainTextMessage",
            "ssml_message": "ssmlMessage",
        },
    )
    class MessageProperty:
        def __init__(
            self,
            *,
            custom_payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.CustomPayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_response_card: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ImageResponseCardProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            plain_text_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.PlainTextMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ssml_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SSMLMessageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The object that provides message text and it's type.

            :param custom_payload: A message in a custom format defined by the client application.
            :param image_response_card: A message that defines a response card that the client application can show to the user.
            :param plain_text_message: A message in plain text format.
            :param ssml_message: A message in Speech Synthesis Markup Language (SSML) format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                message_property = lex.CfnBot.MessageProperty(
                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                        value="value"
                    ),
                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                        title="title",
                
                        # the properties below are optional
                        buttons=[lex.CfnBot.ButtonProperty(
                            text="text",
                            value="value"
                        )],
                        image_url="imageUrl",
                        subtitle="subtitle"
                    ),
                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                        value="value"
                    ),
                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb7ab5ddf974fb59d9017c31c8f2018dd1e12468a8b5ee92f260d8ec1621851f)
                check_type(argname="argument custom_payload", value=custom_payload, expected_type=type_hints["custom_payload"])
                check_type(argname="argument image_response_card", value=image_response_card, expected_type=type_hints["image_response_card"])
                check_type(argname="argument plain_text_message", value=plain_text_message, expected_type=type_hints["plain_text_message"])
                check_type(argname="argument ssml_message", value=ssml_message, expected_type=type_hints["ssml_message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_payload is not None:
                self._values["custom_payload"] = custom_payload
            if image_response_card is not None:
                self._values["image_response_card"] = image_response_card
            if plain_text_message is not None:
                self._values["plain_text_message"] = plain_text_message
            if ssml_message is not None:
                self._values["ssml_message"] = ssml_message

        @builtins.property
        def custom_payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.CustomPayloadProperty"]]:
            '''A message in a custom format defined by the client application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-custompayload
            '''
            result = self._values.get("custom_payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.CustomPayloadProperty"]], result)

        @builtins.property
        def image_response_card(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ImageResponseCardProperty"]]:
            '''A message that defines a response card that the client application can show to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-imageresponsecard
            '''
            result = self._values.get("image_response_card")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ImageResponseCardProperty"]], result)

        @builtins.property
        def plain_text_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.PlainTextMessageProperty"]]:
            '''A message in plain text format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-plaintextmessage
            '''
            result = self._values.get("plain_text_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.PlainTextMessageProperty"]], result)

        @builtins.property
        def ssml_message(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SSMLMessageProperty"]]:
            '''A message in Speech Synthesis Markup Language (SSML) format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-message.html#cfn-lex-bot-message-ssmlmessage
            '''
            result = self._values.get("ssml_message")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SSMLMessageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.MultipleValuesSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"allow_multiple_values": "allowMultipleValues"},
    )
    class MultipleValuesSettingProperty:
        def __init__(
            self,
            *,
            allow_multiple_values: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Indicates whether a slot can return multiple values.

            :param allow_multiple_values: Indicates whether a slot can return multiple values. When true, the slot may return more than one value in a response. When false, the slot returns only a single value. If AllowMultipleValues is not set, the default value is false. Multi-value slots are only available in the en-US locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-multiplevaluessetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                multiple_values_setting_property = lex.CfnBot.MultipleValuesSettingProperty(
                    allow_multiple_values=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c771393a27a87b6bd46f3d359d46aa9447806395f53579df43f80026572a31e1)
                check_type(argname="argument allow_multiple_values", value=allow_multiple_values, expected_type=type_hints["allow_multiple_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_multiple_values is not None:
                self._values["allow_multiple_values"] = allow_multiple_values

        @builtins.property
        def allow_multiple_values(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether a slot can return multiple values.

            When true, the slot may return more than one value in a response. When false, the slot returns only a single value. If AllowMultipleValues is not set, the default value is false.

            Multi-value slots are only available in the en-US locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-multiplevaluessetting.html#cfn-lex-bot-multiplevaluessetting-allowmultiplevalues
            '''
            result = self._values.get("allow_multiple_values")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultipleValuesSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.ObfuscationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"obfuscation_setting_type": "obfuscationSettingType"},
    )
    class ObfuscationSettingProperty:
        def __init__(self, *, obfuscation_setting_type: builtins.str) -> None:
            '''Determines whether Amazon Lex obscures slot values in conversation logs.

            :param obfuscation_setting_type: Value that determines whether Amazon Lex obscures slot values in conversation logs. The default is to obscure the values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-obfuscationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                obfuscation_setting_property = lex.CfnBot.ObfuscationSettingProperty(
                    obfuscation_setting_type="obfuscationSettingType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b60cac8372bdfa58ca9cee001e189769e2a8a9a8c9da8835a54a74b3b46bc5ec)
                check_type(argname="argument obfuscation_setting_type", value=obfuscation_setting_type, expected_type=type_hints["obfuscation_setting_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "obfuscation_setting_type": obfuscation_setting_type,
            }

        @builtins.property
        def obfuscation_setting_type(self) -> builtins.str:
            '''Value that determines whether Amazon Lex obscures slot values in conversation logs.

            The default is to obscure the values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-obfuscationsetting.html#cfn-lex-bot-obfuscationsetting-obfuscationsettingtype
            '''
            result = self._values.get("obfuscation_setting_type")
            assert result is not None, "Required property 'obfuscation_setting_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObfuscationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.OutputContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "time_to_live_in_seconds": "timeToLiveInSeconds",
            "turns_to_live": "turnsToLive",
        },
    )
    class OutputContextProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            time_to_live_in_seconds: jsii.Number,
            turns_to_live: jsii.Number,
        ) -> None:
            '''Describes a session context that is activated when an intent is fulfilled.

            :param name: The name of the output context.
            :param time_to_live_in_seconds: The amount of time, in seconds, that the output context should remain active. The time is figured from the first time the context is sent to the user.
            :param turns_to_live: The number of conversation turns that the output context should remain active. The number of turns is counted from the first time that the context is sent to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                output_context_property = lex.CfnBot.OutputContextProperty(
                    name="name",
                    time_to_live_in_seconds=123,
                    turns_to_live=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51b5b676c6dabe13350db59e9f7e51478941f30d05041fd99417e62906752cd7)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument time_to_live_in_seconds", value=time_to_live_in_seconds, expected_type=type_hints["time_to_live_in_seconds"])
                check_type(argname="argument turns_to_live", value=turns_to_live, expected_type=type_hints["turns_to_live"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "time_to_live_in_seconds": time_to_live_in_seconds,
                "turns_to_live": turns_to_live,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the output context.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html#cfn-lex-bot-outputcontext-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def time_to_live_in_seconds(self) -> jsii.Number:
            '''The amount of time, in seconds, that the output context should remain active.

            The time is figured from the first time the context is sent to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html#cfn-lex-bot-outputcontext-timetoliveinseconds
            '''
            result = self._values.get("time_to_live_in_seconds")
            assert result is not None, "Required property 'time_to_live_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def turns_to_live(self) -> jsii.Number:
            '''The number of conversation turns that the output context should remain active.

            The number of turns is counted from the first time that the context is sent to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-outputcontext.html#cfn-lex-bot-outputcontext-turnstolive
            '''
            result = self._values.get("turns_to_live")
            assert result is not None, "Required property 'turns_to_live' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.PlainTextMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class PlainTextMessageProperty:
        def __init__(self, *, value: builtins.str) -> None:
            '''Defines an ASCII text message to send to the user.

            :param value: The message to send to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-plaintextmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                plain_text_message_property = lex.CfnBot.PlainTextMessageProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0e680d14ee0a7e5202804ede7b01950de731f2c5c28cc2632097099da0bc1c3)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''The message to send to the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-plaintextmessage.html#cfn-lex-bot-plaintextmessage-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlainTextMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.PostFulfillmentStatusSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failure_response": "failureResponse",
            "success_response": "successResponse",
            "timeout_response": "timeoutResponse",
        },
    )
    class PostFulfillmentStatusSpecificationProperty:
        def __init__(
            self,
            *,
            failure_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            success_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            timeout_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides a setting that determines whether the post-fulfillment response is sent to the user.

            For more information, see `Post-fulfillment response <https://docs.aws.amazon.com/lex/latest/dg/streaming-progress.html#progress-complete>`_ in the *Amazon Lex developer guide* .

            :param failure_response: Specifies a list of message groups that Amazon Lex uses to respond when fulfillment isn't successful.
            :param success_response: Specifies a list of message groups that Amazon Lex uses to respond when the fulfillment is successful.
            :param timeout_response: Specifies a list of message groups that Amazon Lex uses to respond when fulfillment isn't completed within the timeout period.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                post_fulfillment_status_specification_property = lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                    failure_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    success_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a1659ee605a6824ee30f43883012b75bb7ae3c3de400a9eafdd793212d1af1d)
                check_type(argname="argument failure_response", value=failure_response, expected_type=type_hints["failure_response"])
                check_type(argname="argument success_response", value=success_response, expected_type=type_hints["success_response"])
                check_type(argname="argument timeout_response", value=timeout_response, expected_type=type_hints["timeout_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failure_response is not None:
                self._values["failure_response"] = failure_response
            if success_response is not None:
                self._values["success_response"] = success_response
            if timeout_response is not None:
                self._values["timeout_response"] = timeout_response

        @builtins.property
        def failure_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond when fulfillment isn't successful.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-failureresponse
            '''
            result = self._values.get("failure_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"]], result)

        @builtins.property
        def success_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond when the fulfillment is successful.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-successresponse
            '''
            result = self._values.get("success_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"]], result)

        @builtins.property
        def timeout_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"]]:
            '''Specifies a list of message groups that Amazon Lex uses to respond when fulfillment isn't completed within the timeout period.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-postfulfillmentstatusspecification.html#cfn-lex-bot-postfulfillmentstatusspecification-timeoutresponse
            '''
            result = self._values.get("timeout_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PostFulfillmentStatusSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.PromptAttemptSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_input_types": "allowedInputTypes",
            "allow_interrupt": "allowInterrupt",
            "audio_and_dtmf_input_specification": "audioAndDtmfInputSpecification",
            "text_input_specification": "textInputSpecification",
        },
    )
    class PromptAttemptSpecificationProperty:
        def __init__(
            self,
            *,
            allowed_input_types: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.AllowedInputTypesProperty", typing.Dict[builtins.str, typing.Any]]],
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            audio_and_dtmf_input_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.AudioAndDTMFInputSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            text_input_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.TextInputSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param allowed_input_types: ``CfnBot.PromptAttemptSpecificationProperty.AllowedInputTypes``.
            :param allow_interrupt: ``CfnBot.PromptAttemptSpecificationProperty.AllowInterrupt``.
            :param audio_and_dtmf_input_specification: ``CfnBot.PromptAttemptSpecificationProperty.AudioAndDTMFInputSpecification``.
            :param text_input_specification: ``CfnBot.PromptAttemptSpecificationProperty.TextInputSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptattemptspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                prompt_attempt_specification_property = lex.CfnBot.PromptAttemptSpecificationProperty(
                    allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                        allow_audio_input=False,
                        allow_dtmf_input=False
                    ),
                
                    # the properties below are optional
                    allow_interrupt=False,
                    audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                        start_timeout_ms=123,
                
                        # the properties below are optional
                        audio_specification=lex.CfnBot.AudioSpecificationProperty(
                            end_timeout_ms=123,
                            max_length_ms=123
                        ),
                        dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                            deletion_character="deletionCharacter",
                            end_character="endCharacter",
                            end_timeout_ms=123,
                            max_length=123
                        )
                    ),
                    text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                        start_timeout_ms=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__359a7367f79da136d347ddf064d4ebb249581165ac501e3e8d2c59a19b571fe5)
                check_type(argname="argument allowed_input_types", value=allowed_input_types, expected_type=type_hints["allowed_input_types"])
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
                check_type(argname="argument audio_and_dtmf_input_specification", value=audio_and_dtmf_input_specification, expected_type=type_hints["audio_and_dtmf_input_specification"])
                check_type(argname="argument text_input_specification", value=text_input_specification, expected_type=type_hints["text_input_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "allowed_input_types": allowed_input_types,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt
            if audio_and_dtmf_input_specification is not None:
                self._values["audio_and_dtmf_input_specification"] = audio_and_dtmf_input_specification
            if text_input_specification is not None:
                self._values["text_input_specification"] = text_input_specification

        @builtins.property
        def allowed_input_types(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AllowedInputTypesProperty"]:
            '''``CfnBot.PromptAttemptSpecificationProperty.AllowedInputTypes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptattemptspecification.html#cfn-lex-bot-promptattemptspecification-allowedinputtypes
            '''
            result = self._values.get("allowed_input_types")
            assert result is not None, "Required property 'allowed_input_types' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AllowedInputTypesProperty"], result)

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnBot.PromptAttemptSpecificationProperty.AllowInterrupt``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptattemptspecification.html#cfn-lex-bot-promptattemptspecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def audio_and_dtmf_input_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AudioAndDTMFInputSpecificationProperty"]]:
            '''``CfnBot.PromptAttemptSpecificationProperty.AudioAndDTMFInputSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptattemptspecification.html#cfn-lex-bot-promptattemptspecification-audioanddtmfinputspecification
            '''
            result = self._values.get("audio_and_dtmf_input_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AudioAndDTMFInputSpecificationProperty"]], result)

        @builtins.property
        def text_input_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.TextInputSpecificationProperty"]]:
            '''``CfnBot.PromptAttemptSpecificationProperty.TextInputSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptattemptspecification.html#cfn-lex-bot-promptattemptspecification-textinputspecification
            '''
            result = self._values.get("text_input_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.TextInputSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PromptAttemptSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.PromptSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_retries": "maxRetries",
            "message_groups_list": "messageGroupsList",
            "allow_interrupt": "allowInterrupt",
            "message_selection_strategy": "messageSelectionStrategy",
            "prompt_attempts_specification": "promptAttemptsSpecification",
        },
    )
    class PromptSpecificationProperty:
        def __init__(
            self,
            *,
            max_retries: jsii.Number,
            message_groups_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.MessageGroupProperty", typing.Dict[builtins.str, typing.Any]]]]],
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            message_selection_strategy: typing.Optional[builtins.str] = None,
            prompt_attempts_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.PromptAttemptSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies a list of message groups that Amazon Lex sends to a user to elicit a response.

            :param max_retries: The maximum number of times the bot tries to elicit a response from the user using this prompt.
            :param message_groups_list: A collection of responses that Amazon Lex can send to the user. Amazon Lex chooses the actual response to send at runtime.
            :param allow_interrupt: Indicates whether the user can interrupt a speech prompt from the bot.
            :param message_selection_strategy: ``CfnBot.PromptSpecificationProperty.MessageSelectionStrategy``.
            :param prompt_attempts_specification: ``CfnBot.PromptSpecificationProperty.PromptAttemptsSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                prompt_specification_property = lex.CfnBot.PromptSpecificationProperty(
                    max_retries=123,
                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                
                        # the properties below are optional
                        variations=[lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                
                    # the properties below are optional
                    allow_interrupt=False,
                    message_selection_strategy="messageSelectionStrategy",
                    prompt_attempts_specification={
                        "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                            allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                allow_audio_input=False,
                                allow_dtmf_input=False
                            ),
                
                            # the properties below are optional
                            allow_interrupt=False,
                            audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                start_timeout_ms=123,
                
                                # the properties below are optional
                                audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                    end_timeout_ms=123,
                                    max_length_ms=123
                                ),
                                dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                    deletion_character="deletionCharacter",
                                    end_character="endCharacter",
                                    end_timeout_ms=123,
                                    max_length=123
                                )
                            ),
                            text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                start_timeout_ms=123
                            )
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4f8efcdf1548108a5d48068e158dddccfb29c7582216e817704419e06919d36)
                check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
                check_type(argname="argument message_groups_list", value=message_groups_list, expected_type=type_hints["message_groups_list"])
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
                check_type(argname="argument message_selection_strategy", value=message_selection_strategy, expected_type=type_hints["message_selection_strategy"])
                check_type(argname="argument prompt_attempts_specification", value=prompt_attempts_specification, expected_type=type_hints["prompt_attempts_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "max_retries": max_retries,
                "message_groups_list": message_groups_list,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt
            if message_selection_strategy is not None:
                self._values["message_selection_strategy"] = message_selection_strategy
            if prompt_attempts_specification is not None:
                self._values["prompt_attempts_specification"] = prompt_attempts_specification

        @builtins.property
        def max_retries(self) -> jsii.Number:
            '''The maximum number of times the bot tries to elicit a response from the user using this prompt.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-maxretries
            '''
            result = self._values.get("max_retries")
            assert result is not None, "Required property 'max_retries' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def message_groups_list(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageGroupProperty"]]]:
            '''A collection of responses that Amazon Lex can send to the user.

            Amazon Lex chooses the actual response to send at runtime.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-messagegroupslist
            '''
            result = self._values.get("message_groups_list")
            assert result is not None, "Required property 'message_groups_list' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageGroupProperty"]]], result)

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the user can interrupt a speech prompt from the bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def message_selection_strategy(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.PromptSpecificationProperty.MessageSelectionStrategy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-messageselectionstrategy
            '''
            result = self._values.get("message_selection_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prompt_attempts_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.PromptAttemptSpecificationProperty"]]]]:
            '''``CfnBot.PromptSpecificationProperty.PromptAttemptsSpecification``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-promptspecification.html#cfn-lex-bot-promptspecification-promptattemptsspecification
            '''
            result = self._values.get("prompt_attempts_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.PromptAttemptSpecificationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PromptSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.ResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "message_groups_list": "messageGroupsList",
            "allow_interrupt": "allowInterrupt",
        },
    )
    class ResponseSpecificationProperty:
        def __init__(
            self,
            *,
            message_groups_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.MessageGroupProperty", typing.Dict[builtins.str, typing.Any]]]]],
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Specifies a list of message groups that Amazon Lex uses to respond to user input.

            :param message_groups_list: A collection of responses that Amazon Lex can send to the user. Amazon Lex chooses the actual response to send at runtime.
            :param allow_interrupt: Indicates whether the user can interrupt a speech response from Amazon Lex .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-responsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                response_specification_property = lex.CfnBot.ResponseSpecificationProperty(
                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                
                        # the properties below are optional
                        variations=[lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                
                    # the properties below are optional
                    allow_interrupt=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__699fafdacbc9aa632e7b1f4ffe86e05ca8eb3e58c9cc72dbc0705729aeda62c6)
                check_type(argname="argument message_groups_list", value=message_groups_list, expected_type=type_hints["message_groups_list"])
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "message_groups_list": message_groups_list,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt

        @builtins.property
        def message_groups_list(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageGroupProperty"]]]:
            '''A collection of responses that Amazon Lex can send to the user.

            Amazon Lex chooses the actual response to send at runtime.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-responsespecification.html#cfn-lex-bot-responsespecification-messagegroupslist
            '''
            result = self._values.get("message_groups_list")
            assert result is not None, "Required property 'message_groups_list' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageGroupProperty"]]], result)

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the user can interrupt a speech response from Amazon Lex .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-responsespecification.html#cfn-lex-bot-responsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.S3BucketLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_prefix": "logPrefix",
            "s3_bucket_arn": "s3BucketArn",
            "kms_key_arn": "kmsKeyArn",
        },
    )
    class S3BucketLogDestinationProperty:
        def __init__(
            self,
            *,
            log_prefix: builtins.str,
            s3_bucket_arn: builtins.str,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an Amazon S3 bucket for logging audio conversations.

            :param log_prefix: Specifies the Amazon S3 prefix to assign to audio log files.
            :param s3_bucket_arn: Specifies the Amazon Resource Name (ARN) of the Amazon S3 bucket where audio files are stored.
            :param kms_key_arn: Specifies the Amazon Resource Name (ARN) of an AWS Key Management Service key for encrypting audio log files stored in an Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3bucketlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                s3_bucket_log_destination_property = lex.CfnBot.S3BucketLogDestinationProperty(
                    log_prefix="logPrefix",
                    s3_bucket_arn="s3BucketArn",
                
                    # the properties below are optional
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3479e44c0bcb1c87d470fa61abd620d0e0387132f98211932223efba7b7c5ab)
                check_type(argname="argument log_prefix", value=log_prefix, expected_type=type_hints["log_prefix"])
                check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_prefix": log_prefix,
                "s3_bucket_arn": s3_bucket_arn,
            }
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def log_prefix(self) -> builtins.str:
            '''Specifies the Amazon S3 prefix to assign to audio log files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3bucketlogdestination.html#cfn-lex-bot-s3bucketlogdestination-logprefix
            '''
            result = self._values.get("log_prefix")
            assert result is not None, "Required property 'log_prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket_arn(self) -> builtins.str:
            '''Specifies the Amazon Resource Name (ARN) of the Amazon S3 bucket where audio files are stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3bucketlogdestination.html#cfn-lex-bot-s3bucketlogdestination-s3bucketarn
            '''
            result = self._values.get("s3_bucket_arn")
            assert result is not None, "Required property 's3_bucket_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the Amazon Resource Name (ARN) of an AWS Key Management Service key for encrypting audio log files stored in an Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3bucketlogdestination.html#cfn-lex-bot-s3bucketlogdestination-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket": "s3Bucket",
            "s3_object_key": "s3ObjectKey",
            "s3_object_version": "s3ObjectVersion",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            s3_bucket: builtins.str,
            s3_object_key: builtins.str,
            s3_object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an Amazon S3 bucket location.

            :param s3_bucket: The S3 bucket name.
            :param s3_object_key: The path and file name to the object in the S3 bucket.
            :param s3_object_version: The version of the object in the S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                s3_location_property = lex.CfnBot.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_object_key="s3ObjectKey",
                
                    # the properties below are optional
                    s3_object_version="s3ObjectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73e309a4fbe8ba1fe62b123c8133503d4487d6db66620a6029709ba9e917026a)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_object_key", value=s3_object_key, expected_type=type_hints["s3_object_key"])
                check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket": s3_bucket,
                "s3_object_key": s3_object_key,
            }
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''The S3 bucket name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html#cfn-lex-bot-s3location-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_object_key(self) -> builtins.str:
            '''The path and file name to the object in the S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html#cfn-lex-bot-s3location-s3objectkey
            '''
            result = self._values.get("s3_object_key")
            assert result is not None, "Required property 's3_object_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_object_version(self) -> typing.Optional[builtins.str]:
            '''The version of the object in the S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-s3location.html#cfn-lex-bot-s3location-s3objectversion
            '''
            result = self._values.get("s3_object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SSMLMessageProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class SSMLMessageProperty:
        def __init__(self, *, value: builtins.str) -> None:
            '''Defines a Speech Synthesis Markup Language (SSML) prompt.

            :param value: The SSML text that defines the prompt.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-ssmlmessage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                s_sMLMessage_property = lex.CfnBot.SSMLMessageProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0bf7c70df8ed3eb667fbef1a57a18d58f9c085fc3c771aacf224ebf55de8a0d)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''The SSML text that defines the prompt.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-ssmlmessage.html#cfn-lex-bot-ssmlmessage-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSMLMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SampleUtteranceProperty",
        jsii_struct_bases=[],
        name_mapping={"utterance": "utterance"},
    )
    class SampleUtteranceProperty:
        def __init__(self, *, utterance: builtins.str) -> None:
            '''A sample utterance that invokes and intent or responds to a slot elicitation prompt.

            :param utterance: The sample utterance that Amazon Lex uses to build its machine-learning model to recognize intents.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sampleutterance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                sample_utterance_property = lex.CfnBot.SampleUtteranceProperty(
                    utterance="utterance"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cba40fa24c702dc2756fab3dbd3ff60161663576ce120a3d60ee583755835a92)
                check_type(argname="argument utterance", value=utterance, expected_type=type_hints["utterance"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "utterance": utterance,
            }

        @builtins.property
        def utterance(self) -> builtins.str:
            '''The sample utterance that Amazon Lex uses to build its machine-learning model to recognize intents.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sampleutterance.html#cfn-lex-bot-sampleutterance-utterance
            '''
            result = self._values.get("utterance")
            assert result is not None, "Required property 'utterance' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SampleUtteranceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SampleValueProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class SampleValueProperty:
        def __init__(self, *, value: builtins.str) -> None:
            '''Defines one of the values for a slot type.

            :param value: The value that can be used for a slot type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-samplevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                sample_value_property = lex.CfnBot.SampleValueProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c29ca9634d0fba49b3d706d05f7f5dc1da6a6cd71b41f9bebb3d17d49ebd3936)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''The value that can be used for a slot type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-samplevalue.html#cfn-lex-bot-samplevalue-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SampleValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SentimentAnalysisSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"detect_sentiment": "detectSentiment"},
    )
    class SentimentAnalysisSettingsProperty:
        def __init__(
            self,
            *,
            detect_sentiment: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''
            :param detect_sentiment: ``CfnBot.SentimentAnalysisSettingsProperty.DetectSentiment``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sentimentanalysissettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                sentiment_analysis_settings_property = lex.CfnBot.SentimentAnalysisSettingsProperty(
                    detect_sentiment=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df5fd083508d7a130d114e33b83c17957de66b4dfe31a69065e9d758e238386a)
                check_type(argname="argument detect_sentiment", value=detect_sentiment, expected_type=type_hints["detect_sentiment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "detect_sentiment": detect_sentiment,
            }

        @builtins.property
        def detect_sentiment(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''``CfnBot.SentimentAnalysisSettingsProperty.DetectSentiment``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-sentimentanalysissettings.html#cfn-lex-bot-sentimentanalysissettings-detectsentiment
            '''
            result = self._values.get("detect_sentiment")
            assert result is not None, "Required property 'detect_sentiment' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SentimentAnalysisSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SlotDefaultValueProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue"},
    )
    class SlotDefaultValueProperty:
        def __init__(self, *, default_value: builtins.str) -> None:
            '''Specifies the default value to use when a user doesn't provide a value for a slot.

            :param default_value: The default value to use when a user doesn't provide a value for a slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                slot_default_value_property = lex.CfnBot.SlotDefaultValueProperty(
                    default_value="defaultValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa56f0d00799161e87d8aec1213e5553a2f40edf609f138a8b864cd28c43426b)
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "default_value": default_value,
            }

        @builtins.property
        def default_value(self) -> builtins.str:
            '''The default value to use when a user doesn't provide a value for a slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvalue.html#cfn-lex-bot-slotdefaultvalue-defaultvalue
            '''
            result = self._values.get("default_value")
            assert result is not None, "Required property 'default_value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotDefaultValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SlotDefaultValueSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value_list": "defaultValueList"},
    )
    class SlotDefaultValueSpecificationProperty:
        def __init__(
            self,
            *,
            default_value_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SlotDefaultValueProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''Defines a list of values that Amazon Lex should use as the default value for a slot.

            :param default_value_list: A list of default values. Amazon Lex chooses the default value to use in the order that they are presented in the list.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvaluespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                slot_default_value_specification_property = lex.CfnBot.SlotDefaultValueSpecificationProperty(
                    default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                        default_value="defaultValue"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e189c45ab6d5b9447ee84586c81875fecad4babd9223fae30e1abb06bff1b598)
                check_type(argname="argument default_value_list", value=default_value_list, expected_type=type_hints["default_value_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "default_value_list": default_value_list,
            }

        @builtins.property
        def default_value_list(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotDefaultValueProperty"]]]:
            '''A list of default values.

            Amazon Lex chooses the default value to use in the order that they are presented in the list.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotdefaultvaluespecification.html#cfn-lex-bot-slotdefaultvaluespecification-defaultvaluelist
            '''
            result = self._values.get("default_value_list")
            assert result is not None, "Required property 'default_value_list' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotDefaultValueProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotDefaultValueSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SlotPriorityProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "slot_name": "slotName"},
    )
    class SlotPriorityProperty:
        def __init__(self, *, priority: jsii.Number, slot_name: builtins.str) -> None:
            '''Sets the priority that Amazon Lex should use when eliciting slots values from a user.

            :param priority: The priority that Amazon Lex should apply to the slot.
            :param slot_name: The name of the slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotpriority.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                slot_priority_property = lex.CfnBot.SlotPriorityProperty(
                    priority=123,
                    slot_name="slotName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__707e6cbad7e1fbee236c253f4f778fef89535083113e5959410e50559cd1bbc1)
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument slot_name", value=slot_name, expected_type=type_hints["slot_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "priority": priority,
                "slot_name": slot_name,
            }

        @builtins.property
        def priority(self) -> jsii.Number:
            '''The priority that Amazon Lex should apply to the slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotpriority.html#cfn-lex-bot-slotpriority-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def slot_name(self) -> builtins.str:
            '''The name of the slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotpriority.html#cfn-lex-bot-slotpriority-slotname
            '''
            result = self._values.get("slot_name")
            assert result is not None, "Required property 'slot_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotPriorityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SlotProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "slot_type_name": "slotTypeName",
            "value_elicitation_setting": "valueElicitationSetting",
            "description": "description",
            "multiple_values_setting": "multipleValuesSetting",
            "obfuscation_setting": "obfuscationSetting",
        },
    )
    class SlotProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            slot_type_name: builtins.str,
            value_elicitation_setting: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SlotValueElicitationSettingProperty", typing.Dict[builtins.str, typing.Any]]],
            description: typing.Optional[builtins.str] = None,
            multiple_values_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.MultipleValuesSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            obfuscation_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ObfuscationSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the definition of a slot.

            Amazon Lex elicits slot values from uses to fulfill the user's intent.

            :param name: The name of the slot.
            :param slot_type_name: The name of the slot type that this slot is based on. The slot type defines the acceptable values for the slot.
            :param value_elicitation_setting: Determines the slot resolution strategy that Amazon Lex uses to return slot type values. The field can be set to one of the following values: - OriginalValue - Returns the value entered by the user, if the user value is similar to a slot value. - TopResolution - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned. If you don't specify the valueSelectionStrategy, the default is OriginalValue.
            :param description: A description of the slot type.
            :param multiple_values_setting: Determines whether the slot can return multiple values to the application.
            :param obfuscation_setting: Determines whether the contents of the slot are obfuscated in Amazon CloudWatch Logs logs. Use obfuscated slots to protect information such as personally identifiable information (PII) in logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                slot_property = lex.CfnBot.SlotProperty(
                    name="name",
                    slot_type_name="slotTypeName",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="slotConstraint",
                
                        # the properties below are optional
                        default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                            default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                                default_value="defaultValue"
                            )]
                        ),
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            max_retries=123,
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False,
                            message_selection_strategy="messageSelectionStrategy",
                            prompt_attempts_specification={
                                "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                    allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                        allow_audio_input=False,
                                        allow_dtmf_input=False
                                    ),
                
                                    # the properties below are optional
                                    allow_interrupt=False,
                                    audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                        start_timeout_ms=123,
                
                                        # the properties below are optional
                                        audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                            end_timeout_ms=123,
                                            max_length_ms=123
                                        ),
                                        dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                            deletion_character="deletionCharacter",
                                            end_character="endCharacter",
                                            end_timeout_ms=123,
                                            max_length=123
                                        )
                                    ),
                                    text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                        start_timeout_ms=123
                                    )
                                )
                            }
                        ),
                        sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                            utterance="utterance"
                        )],
                        wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                            continue_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                
                            # the properties below are optional
                            is_active=False,
                            still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                                frequency_in_seconds=123,
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
                
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
                
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
                                timeout_in_seconds=123,
                
                                # the properties below are optional
                                allow_interrupt=False
                            )
                        )
                    ),
                
                    # the properties below are optional
                    description="description",
                    multiple_values_setting=lex.CfnBot.MultipleValuesSettingProperty(
                        allow_multiple_values=False
                    ),
                    obfuscation_setting=lex.CfnBot.ObfuscationSettingProperty(
                        obfuscation_setting_type="obfuscationSettingType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7ac62926bbc5f616f5f16264c0595ef4e53f02fb6d3b319b0a18e74276e1bb0)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument slot_type_name", value=slot_type_name, expected_type=type_hints["slot_type_name"])
                check_type(argname="argument value_elicitation_setting", value=value_elicitation_setting, expected_type=type_hints["value_elicitation_setting"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument multiple_values_setting", value=multiple_values_setting, expected_type=type_hints["multiple_values_setting"])
                check_type(argname="argument obfuscation_setting", value=obfuscation_setting, expected_type=type_hints["obfuscation_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "slot_type_name": slot_type_name,
                "value_elicitation_setting": value_elicitation_setting,
            }
            if description is not None:
                self._values["description"] = description
            if multiple_values_setting is not None:
                self._values["multiple_values_setting"] = multiple_values_setting
            if obfuscation_setting is not None:
                self._values["obfuscation_setting"] = obfuscation_setting

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def slot_type_name(self) -> builtins.str:
            '''The name of the slot type that this slot is based on.

            The slot type defines the acceptable values for the slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-slottypename
            '''
            result = self._values.get("slot_type_name")
            assert result is not None, "Required property 'slot_type_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value_elicitation_setting(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotValueElicitationSettingProperty"]:
            '''Determines the slot resolution strategy that Amazon Lex uses to return slot type values.

            The field can be set to one of the following values:

            - OriginalValue - Returns the value entered by the user, if the user value is similar to a slot value.
            - TopResolution - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned.

            If you don't specify the valueSelectionStrategy, the default is OriginalValue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-valueelicitationsetting
            '''
            result = self._values.get("value_elicitation_setting")
            assert result is not None, "Required property 'value_elicitation_setting' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotValueElicitationSettingProperty"], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the slot type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multiple_values_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MultipleValuesSettingProperty"]]:
            '''Determines whether the slot can return multiple values to the application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-multiplevaluessetting
            '''
            result = self._values.get("multiple_values_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MultipleValuesSettingProperty"]], result)

        @builtins.property
        def obfuscation_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ObfuscationSettingProperty"]]:
            '''Determines whether the contents of the slot are obfuscated in Amazon CloudWatch Logs logs.

            Use obfuscated slots to protect information such as personally identifiable information (PII) in logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slot.html#cfn-lex-bot-slot-obfuscationsetting
            '''
            result = self._values.get("obfuscation_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ObfuscationSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SlotTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "description": "description",
            "external_source_setting": "externalSourceSetting",
            "parent_slot_type_signature": "parentSlotTypeSignature",
            "slot_type_values": "slotTypeValues",
            "value_selection_setting": "valueSelectionSetting",
        },
    )
    class SlotTypeProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            description: typing.Optional[builtins.str] = None,
            external_source_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ExternalSourceSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parent_slot_type_signature: typing.Optional[builtins.str] = None,
            slot_type_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SlotTypeValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            value_selection_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SlotValueSelectionSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a slot type.

            :param name: The name of the slot type. A slot type name must be unique withing the account.
            :param description: A description of the slot type. Use the description to help identify the slot type in lists.
            :param external_source_setting: Sets the type of external information used to create the slot type.
            :param parent_slot_type_signature: The built-in slot type used as a parent of this slot type. When you define a parent slot type, the new slot type has the configuration of the parent lot type. Only AMAZON.AlphaNumeric is supported.
            :param slot_type_values: A list of SlotTypeValue objects that defines the values that the slot type can take. Each value can have a list of synonyms, additional values that help train the machine learning model about the values that it resolves for the slot.
            :param value_selection_setting: Determines the slot resolution strategy that Amazon Lex uses to return slot type values. The field can be set to one of the following values: - OriginalValue - Returns the value entered by the user, if the user value is similar to a slot value. - TopResolution - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned. If you don't specify the valueSelectionStrategy, the default is OriginalValue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                slot_type_property = lex.CfnBot.SlotTypeProperty(
                    name="name",
                
                    # the properties below are optional
                    description="description",
                    external_source_setting=lex.CfnBot.ExternalSourceSettingProperty(
                        grammar_slot_type_setting=lex.CfnBot.GrammarSlotTypeSettingProperty(
                            source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                                s3_bucket_name="s3BucketName",
                                s3_object_key="s3ObjectKey",
                
                                # the properties below are optional
                                kms_key_arn="kmsKeyArn"
                            )
                        )
                    ),
                    parent_slot_type_signature="parentSlotTypeSignature",
                    slot_type_values=[lex.CfnBot.SlotTypeValueProperty(
                        sample_value=lex.CfnBot.SampleValueProperty(
                            value="value"
                        ),
                
                        # the properties below are optional
                        synonyms=[lex.CfnBot.SampleValueProperty(
                            value="value"
                        )]
                    )],
                    value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                        resolution_strategy="resolutionStrategy",
                
                        # the properties below are optional
                        advanced_recognition_setting=lex.CfnBot.AdvancedRecognitionSettingProperty(
                            audio_recognition_strategy="audioRecognitionStrategy"
                        ),
                        regex_filter=lex.CfnBot.SlotValueRegexFilterProperty(
                            pattern="pattern"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff6e0399df24b43356318fd6410381e90f6a85d1abcd14000e703c32666ce438)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument external_source_setting", value=external_source_setting, expected_type=type_hints["external_source_setting"])
                check_type(argname="argument parent_slot_type_signature", value=parent_slot_type_signature, expected_type=type_hints["parent_slot_type_signature"])
                check_type(argname="argument slot_type_values", value=slot_type_values, expected_type=type_hints["slot_type_values"])
                check_type(argname="argument value_selection_setting", value=value_selection_setting, expected_type=type_hints["value_selection_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if description is not None:
                self._values["description"] = description
            if external_source_setting is not None:
                self._values["external_source_setting"] = external_source_setting
            if parent_slot_type_signature is not None:
                self._values["parent_slot_type_signature"] = parent_slot_type_signature
            if slot_type_values is not None:
                self._values["slot_type_values"] = slot_type_values
            if value_selection_setting is not None:
                self._values["value_selection_setting"] = value_selection_setting

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the slot type.

            A slot type name must be unique withing the account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the slot type.

            Use the description to help identify the slot type in lists.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_source_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ExternalSourceSettingProperty"]]:
            '''Sets the type of external information used to create the slot type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-externalsourcesetting
            '''
            result = self._values.get("external_source_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ExternalSourceSettingProperty"]], result)

        @builtins.property
        def parent_slot_type_signature(self) -> typing.Optional[builtins.str]:
            '''The built-in slot type used as a parent of this slot type.

            When you define a parent slot type, the new slot type has the configuration of the parent lot type.

            Only AMAZON.AlphaNumeric is supported.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-parentslottypesignature
            '''
            result = self._values.get("parent_slot_type_signature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slot_type_values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotTypeValueProperty"]]]]:
            '''A list of SlotTypeValue objects that defines the values that the slot type can take.

            Each value can have a list of synonyms, additional values that help train the machine learning model about the values that it resolves for the slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-slottypevalues
            '''
            result = self._values.get("slot_type_values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotTypeValueProperty"]]]], result)

        @builtins.property
        def value_selection_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotValueSelectionSettingProperty"]]:
            '''Determines the slot resolution strategy that Amazon Lex uses to return slot type values.

            The field can be set to one of the following values:

            - OriginalValue - Returns the value entered by the user, if the user value is similar to a slot value.
            - TopResolution - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned.

            If you don't specify the valueSelectionStrategy, the default is OriginalValue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottype.html#cfn-lex-bot-slottype-valueselectionsetting
            '''
            result = self._values.get("value_selection_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotValueSelectionSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SlotTypeValueProperty",
        jsii_struct_bases=[],
        name_mapping={"sample_value": "sampleValue", "synonyms": "synonyms"},
    )
    class SlotTypeValueProperty:
        def __init__(
            self,
            *,
            sample_value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SampleValueProperty", typing.Dict[builtins.str, typing.Any]]],
            synonyms: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SampleValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Each slot type can have a set of values.

            The ``SlotTypeValue`` represents a value that the slot type can take.

            :param sample_value: The value of the slot type entry.
            :param synonyms: Additional values related to the slot type entry.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottypevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                slot_type_value_property = lex.CfnBot.SlotTypeValueProperty(
                    sample_value=lex.CfnBot.SampleValueProperty(
                        value="value"
                    ),
                
                    # the properties below are optional
                    synonyms=[lex.CfnBot.SampleValueProperty(
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4dc872c6cba621347da84b298c11fd0884a45256e4915a27358d6664ff8d133)
                check_type(argname="argument sample_value", value=sample_value, expected_type=type_hints["sample_value"])
                check_type(argname="argument synonyms", value=synonyms, expected_type=type_hints["synonyms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "sample_value": sample_value,
            }
            if synonyms is not None:
                self._values["synonyms"] = synonyms

        @builtins.property
        def sample_value(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SampleValueProperty"]:
            '''The value of the slot type entry.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottypevalue.html#cfn-lex-bot-slottypevalue-samplevalue
            '''
            result = self._values.get("sample_value")
            assert result is not None, "Required property 'sample_value' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SampleValueProperty"], result)

        @builtins.property
        def synonyms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SampleValueProperty"]]]]:
            '''Additional values related to the slot type entry.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slottypevalue.html#cfn-lex-bot-slottypevalue-synonyms
            '''
            result = self._values.get("synonyms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SampleValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotTypeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SlotValueElicitationSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "slot_constraint": "slotConstraint",
            "default_value_specification": "defaultValueSpecification",
            "prompt_specification": "promptSpecification",
            "sample_utterances": "sampleUtterances",
            "wait_and_continue_specification": "waitAndContinueSpecification",
        },
    )
    class SlotValueElicitationSettingProperty:
        def __init__(
            self,
            *,
            slot_constraint: builtins.str,
            default_value_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SlotDefaultValueSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            prompt_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.PromptSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sample_utterances: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SampleUtteranceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            wait_and_continue_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.WaitAndContinueSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings that you can use for eliciting a slot value.

            :param slot_constraint: Specifies whether the slot is required or optional.
            :param default_value_specification: A list of default values for a slot. Default values are used when Amazon Lex hasn't determined a value for a slot. You can specify default values from context variables, session attributes, and defined values.
            :param prompt_specification: The prompt that Amazon Lex uses to elicit the slot value from the user.
            :param sample_utterances: If you know a specific pattern that users might respond to an Amazon Lex request for a slot value, you can provide those utterances to improve accuracy. This is optional. In most cases Amazon Lex is capable of understanding user utterances.
            :param wait_and_continue_specification: Specifies the prompts that Amazon Lex uses while a bot is waiting for customer input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                slot_value_elicitation_setting_property = lex.CfnBot.SlotValueElicitationSettingProperty(
                    slot_constraint="slotConstraint",
                
                    # the properties below are optional
                    default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                        default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                            default_value="defaultValue"
                        )]
                    ),
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        max_retries=123,
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False,
                        message_selection_strategy="messageSelectionStrategy",
                        prompt_attempts_specification={
                            "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                    allow_audio_input=False,
                                    allow_dtmf_input=False
                                ),
                
                                # the properties below are optional
                                allow_interrupt=False,
                                audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                    start_timeout_ms=123,
                
                                    # the properties below are optional
                                    audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                        end_timeout_ms=123,
                                        max_length_ms=123
                                    ),
                                    dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                        deletion_character="deletionCharacter",
                                        end_character="endCharacter",
                                        end_timeout_ms=123,
                                        max_length=123
                                    )
                                ),
                                text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                    start_timeout_ms=123
                                )
                            )
                        }
                    ),
                    sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                        utterance="utterance"
                    )],
                    wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                        continue_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                        waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                
                            # the properties below are optional
                            allow_interrupt=False
                        ),
                
                        # the properties below are optional
                        is_active=False,
                        still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                            frequency_in_seconds=123,
                            message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                ),
                
                                # the properties below are optional
                                variations=[lex.CfnBot.MessageProperty(
                                    custom_payload=lex.CfnBot.CustomPayloadProperty(
                                        value="value"
                                    ),
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="title",
                
                                        # the properties below are optional
                                        buttons=[lex.CfnBot.ButtonProperty(
                                            text="text",
                                            value="value"
                                        )],
                                        image_url="imageUrl",
                                        subtitle="subtitle"
                                    ),
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="value"
                                    ),
                                    ssml_message=lex.CfnBot.SSMLMessageProperty(
                                        value="value"
                                    )
                                )]
                            )],
                            timeout_in_seconds=123,
                
                            # the properties below are optional
                            allow_interrupt=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c40ccae0d979b7a128738e3d610d639edab8f4be1e943016dba9869717c7d4b)
                check_type(argname="argument slot_constraint", value=slot_constraint, expected_type=type_hints["slot_constraint"])
                check_type(argname="argument default_value_specification", value=default_value_specification, expected_type=type_hints["default_value_specification"])
                check_type(argname="argument prompt_specification", value=prompt_specification, expected_type=type_hints["prompt_specification"])
                check_type(argname="argument sample_utterances", value=sample_utterances, expected_type=type_hints["sample_utterances"])
                check_type(argname="argument wait_and_continue_specification", value=wait_and_continue_specification, expected_type=type_hints["wait_and_continue_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "slot_constraint": slot_constraint,
            }
            if default_value_specification is not None:
                self._values["default_value_specification"] = default_value_specification
            if prompt_specification is not None:
                self._values["prompt_specification"] = prompt_specification
            if sample_utterances is not None:
                self._values["sample_utterances"] = sample_utterances
            if wait_and_continue_specification is not None:
                self._values["wait_and_continue_specification"] = wait_and_continue_specification

        @builtins.property
        def slot_constraint(self) -> builtins.str:
            '''Specifies whether the slot is required or optional.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-slotconstraint
            '''
            result = self._values.get("slot_constraint")
            assert result is not None, "Required property 'slot_constraint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def default_value_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotDefaultValueSpecificationProperty"]]:
            '''A list of default values for a slot.

            Default values are used when Amazon Lex hasn't determined a value for a slot. You can specify default values from context variables, session attributes, and defined values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-defaultvaluespecification
            '''
            result = self._values.get("default_value_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotDefaultValueSpecificationProperty"]], result)

        @builtins.property
        def prompt_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.PromptSpecificationProperty"]]:
            '''The prompt that Amazon Lex uses to elicit the slot value from the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-promptspecification
            '''
            result = self._values.get("prompt_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.PromptSpecificationProperty"]], result)

        @builtins.property
        def sample_utterances(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SampleUtteranceProperty"]]]]:
            '''If you know a specific pattern that users might respond to an Amazon Lex request for a slot value, you can provide those utterances to improve accuracy.

            This is optional. In most cases Amazon Lex is capable of understanding user utterances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-sampleutterances
            '''
            result = self._values.get("sample_utterances")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SampleUtteranceProperty"]]]], result)

        @builtins.property
        def wait_and_continue_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.WaitAndContinueSpecificationProperty"]]:
            '''Specifies the prompts that Amazon Lex uses while a bot is waiting for customer input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueelicitationsetting.html#cfn-lex-bot-slotvalueelicitationsetting-waitandcontinuespecification
            '''
            result = self._values.get("wait_and_continue_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.WaitAndContinueSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueElicitationSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SlotValueRegexFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"pattern": "pattern"},
    )
    class SlotValueRegexFilterProperty:
        def __init__(self, *, pattern: builtins.str) -> None:
            '''Provides a regular expression used to validate the value of a slot.

            :param pattern: A regular expression used to validate the value of a slot. Use a standard regular expression. Amazon Lex supports the following characters in the regular expression: - A-Z, a-z - 0-9 - Unicode characters ("\\ u") Represent Unicode characters with four digits, for example "]u0041" or "\\ u005A". The following regular expression operators are not supported: - Infinite repeaters: *, +, or {x,} with no upper bound - Wild card (.)

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueregexfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                slot_value_regex_filter_property = lex.CfnBot.SlotValueRegexFilterProperty(
                    pattern="pattern"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__67fab4304a23c2bbd1994182d3cf16d0945b18df30ed134f65d24bea681af81f)
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "pattern": pattern,
            }

        @builtins.property
        def pattern(self) -> builtins.str:
            '''A regular expression used to validate the value of a slot.

            Use a standard regular expression. Amazon Lex supports the following characters in the regular expression:

            - A-Z, a-z
            - 0-9
            - Unicode characters ("\\ u")

            Represent Unicode characters with four digits, for example "]u0041" or "\\ u005A".

            The following regular expression operators are not supported:

            - Infinite repeaters: *, +, or {x,} with no upper bound
            - Wild card (.)

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueregexfilter.html#cfn-lex-bot-slotvalueregexfilter-pattern
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueRegexFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.SlotValueSelectionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resolution_strategy": "resolutionStrategy",
            "advanced_recognition_setting": "advancedRecognitionSetting",
            "regex_filter": "regexFilter",
        },
    )
    class SlotValueSelectionSettingProperty:
        def __init__(
            self,
            *,
            resolution_strategy: builtins.str,
            advanced_recognition_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.AdvancedRecognitionSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            regex_filter: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.SlotValueRegexFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains settings used by Amazon Lex to select a slot value.

            :param resolution_strategy: Determines the slot resolution strategy that Amazon Lex uses to return slot type values. The field can be set to one of the following values: - OriginalValue - Returns the value entered by the user, if the user value is similar to a slot value. - TopResolution - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned. If you don't specify the valueSelectionStrategy, the default is OriginalValue.
            :param advanced_recognition_setting: Specifies settings that enable advanced recognition settings for slot values. You can use this to enable using slot values as a custom vocabulary for recognizing user utterances.
            :param regex_filter: A regular expression used to validate the value of a slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                slot_value_selection_setting_property = lex.CfnBot.SlotValueSelectionSettingProperty(
                    resolution_strategy="resolutionStrategy",
                
                    # the properties below are optional
                    advanced_recognition_setting=lex.CfnBot.AdvancedRecognitionSettingProperty(
                        audio_recognition_strategy="audioRecognitionStrategy"
                    ),
                    regex_filter=lex.CfnBot.SlotValueRegexFilterProperty(
                        pattern="pattern"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4eee2760a0801a269c2ec5536aecd31c74000f7bf9e7473cfde846a6d984288d)
                check_type(argname="argument resolution_strategy", value=resolution_strategy, expected_type=type_hints["resolution_strategy"])
                check_type(argname="argument advanced_recognition_setting", value=advanced_recognition_setting, expected_type=type_hints["advanced_recognition_setting"])
                check_type(argname="argument regex_filter", value=regex_filter, expected_type=type_hints["regex_filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "resolution_strategy": resolution_strategy,
            }
            if advanced_recognition_setting is not None:
                self._values["advanced_recognition_setting"] = advanced_recognition_setting
            if regex_filter is not None:
                self._values["regex_filter"] = regex_filter

        @builtins.property
        def resolution_strategy(self) -> builtins.str:
            '''Determines the slot resolution strategy that Amazon Lex uses to return slot type values.

            The field can be set to one of the following values:

            - OriginalValue - Returns the value entered by the user, if the user value is similar to a slot value.
            - TopResolution - If there is a resolution list for the slot, return the first value in the resolution list as the slot type value. If there is no resolution list, null is returned.

            If you don't specify the valueSelectionStrategy, the default is OriginalValue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html#cfn-lex-bot-slotvalueselectionsetting-resolutionstrategy
            '''
            result = self._values.get("resolution_strategy")
            assert result is not None, "Required property 'resolution_strategy' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def advanced_recognition_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AdvancedRecognitionSettingProperty"]]:
            '''Specifies settings that enable advanced recognition settings for slot values.

            You can use this to enable using slot values as a custom vocabulary for recognizing user utterances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html#cfn-lex-bot-slotvalueselectionsetting-advancedrecognitionsetting
            '''
            result = self._values.get("advanced_recognition_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.AdvancedRecognitionSettingProperty"]], result)

        @builtins.property
        def regex_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotValueRegexFilterProperty"]]:
            '''A regular expression used to validate the value of a slot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-slotvalueselectionsetting.html#cfn-lex-bot-slotvalueselectionsetting-regexfilter
            '''
            result = self._values.get("regex_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.SlotValueRegexFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlotValueSelectionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.StillWaitingResponseSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "frequency_in_seconds": "frequencyInSeconds",
            "message_groups_list": "messageGroupsList",
            "timeout_in_seconds": "timeoutInSeconds",
            "allow_interrupt": "allowInterrupt",
        },
    )
    class StillWaitingResponseSpecificationProperty:
        def __init__(
            self,
            *,
            frequency_in_seconds: jsii.Number,
            message_groups_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.MessageGroupProperty", typing.Dict[builtins.str, typing.Any]]]]],
            timeout_in_seconds: jsii.Number,
            allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Defines the messages that Amazon Lex sends to a user to remind them that the bot is waiting for a response.

            :param frequency_in_seconds: How often a message should be sent to the user. Minimum of 1 second, maximum of 5 minutes.
            :param message_groups_list: A collection of responses that Amazon Lex can send to the user. Amazon Lex chooses the actual response to send at runtime.
            :param timeout_in_seconds: If Amazon Lex waits longer than this length of time for a response, it will stop sending messages.
            :param allow_interrupt: Indicates that the user can interrupt the response by speaking while the message is being played.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                still_waiting_response_specification_property = lex.CfnBot.StillWaitingResponseSpecificationProperty(
                    frequency_in_seconds=123,
                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        ),
                
                        # the properties below are optional
                        variations=[lex.CfnBot.MessageProperty(
                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                value="value"
                            ),
                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                title="title",
                
                                # the properties below are optional
                                buttons=[lex.CfnBot.ButtonProperty(
                                    text="text",
                                    value="value"
                                )],
                                image_url="imageUrl",
                                subtitle="subtitle"
                            ),
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value="value"
                            ),
                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                value="value"
                            )
                        )]
                    )],
                    timeout_in_seconds=123,
                
                    # the properties below are optional
                    allow_interrupt=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__567e84456959430c5fe2d7e19b42583201d32d57dbb79a2795c9a32184653266)
                check_type(argname="argument frequency_in_seconds", value=frequency_in_seconds, expected_type=type_hints["frequency_in_seconds"])
                check_type(argname="argument message_groups_list", value=message_groups_list, expected_type=type_hints["message_groups_list"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
                check_type(argname="argument allow_interrupt", value=allow_interrupt, expected_type=type_hints["allow_interrupt"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "frequency_in_seconds": frequency_in_seconds,
                "message_groups_list": message_groups_list,
                "timeout_in_seconds": timeout_in_seconds,
            }
            if allow_interrupt is not None:
                self._values["allow_interrupt"] = allow_interrupt

        @builtins.property
        def frequency_in_seconds(self) -> jsii.Number:
            '''How often a message should be sent to the user.

            Minimum of 1 second, maximum of 5 minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-frequencyinseconds
            '''
            result = self._values.get("frequency_in_seconds")
            assert result is not None, "Required property 'frequency_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def message_groups_list(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageGroupProperty"]]]:
            '''A collection of responses that Amazon Lex can send to the user.

            Amazon Lex chooses the actual response to send at runtime.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-messagegroupslist
            '''
            result = self._values.get("message_groups_list")
            assert result is not None, "Required property 'message_groups_list' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.MessageGroupProperty"]]], result)

        @builtins.property
        def timeout_in_seconds(self) -> jsii.Number:
            '''If Amazon Lex waits longer than this length of time for a response, it will stop sending messages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            assert result is not None, "Required property 'timeout_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def allow_interrupt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates that the user can interrupt the response by speaking while the message is being played.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-stillwaitingresponsespecification.html#cfn-lex-bot-stillwaitingresponsespecification-allowinterrupt
            '''
            result = self._values.get("allow_interrupt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StillWaitingResponseSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.TestBotAliasSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bot_alias_locale_settings": "botAliasLocaleSettings",
            "conversation_log_settings": "conversationLogSettings",
            "description": "description",
            "sentiment_analysis_settings": "sentimentAnalysisSettings",
        },
    )
    class TestBotAliasSettingsProperty:
        def __init__(
            self,
            *,
            bot_alias_locale_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.BotAliasLocaleSettingsItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            conversation_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ConversationLogSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            sentiment_analysis_settings: typing.Any = None,
        ) -> None:
            '''Specifies configuration settings for the alias used to test the bot.

            If the ``TestBotAliasSettings`` property is not specified, the settings are configured with default values.

            :param bot_alias_locale_settings: Specifies settings that are unique to a locale. For example, you can use a different Lambda function depending on the bot's locale.
            :param conversation_log_settings: Specifies settings for conversation logs that save audio, text, and metadata information for conversations with your users.
            :param description: Specifies a description for the test bot alias.
            :param sentiment_analysis_settings: Specifies whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-testbotaliassettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                # sentiment_analysis_settings: Any
                
                test_bot_alias_settings_property = lex.CfnBot.TestBotAliasSettingsProperty(
                    bot_alias_locale_settings=[lex.CfnBot.BotAliasLocaleSettingsItemProperty(
                        bot_alias_locale_setting=lex.CfnBot.BotAliasLocaleSettingsProperty(
                            enabled=False,
                
                            # the properties below are optional
                            code_hook_specification=lex.CfnBot.CodeHookSpecificationProperty(
                                lambda_code_hook=lex.CfnBot.LambdaCodeHookProperty(
                                    code_hook_interface_version="codeHookInterfaceVersion",
                                    lambda_arn="lambdaArn"
                                )
                            )
                        ),
                        locale_id="localeId"
                    )],
                    conversation_log_settings=lex.CfnBot.ConversationLogSettingsProperty(
                        audio_log_settings=[lex.CfnBot.AudioLogSettingProperty(
                            destination=lex.CfnBot.AudioLogDestinationProperty(
                                s3_bucket=lex.CfnBot.S3BucketLogDestinationProperty(
                                    log_prefix="logPrefix",
                                    s3_bucket_arn="s3BucketArn",
                
                                    # the properties below are optional
                                    kms_key_arn="kmsKeyArn"
                                )
                            ),
                            enabled=False
                        )],
                        text_log_settings=[lex.CfnBot.TextLogSettingProperty(
                            destination=lex.CfnBot.TextLogDestinationProperty(
                                cloud_watch=lex.CfnBot.CloudWatchLogGroupLogDestinationProperty(
                                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                                    log_prefix="logPrefix"
                                )
                            ),
                            enabled=False
                        )]
                    ),
                    description="description",
                    sentiment_analysis_settings=sentiment_analysis_settings
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04a60c523d94c3dca9c2df881d69c88595b8a14785ac5338fa1041ebe1533a13)
                check_type(argname="argument bot_alias_locale_settings", value=bot_alias_locale_settings, expected_type=type_hints["bot_alias_locale_settings"])
                check_type(argname="argument conversation_log_settings", value=conversation_log_settings, expected_type=type_hints["conversation_log_settings"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument sentiment_analysis_settings", value=sentiment_analysis_settings, expected_type=type_hints["sentiment_analysis_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bot_alias_locale_settings is not None:
                self._values["bot_alias_locale_settings"] = bot_alias_locale_settings
            if conversation_log_settings is not None:
                self._values["conversation_log_settings"] = conversation_log_settings
            if description is not None:
                self._values["description"] = description
            if sentiment_analysis_settings is not None:
                self._values["sentiment_analysis_settings"] = sentiment_analysis_settings

        @builtins.property
        def bot_alias_locale_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.BotAliasLocaleSettingsItemProperty"]]]]:
            '''Specifies settings that are unique to a locale.

            For example, you can use a different Lambda function depending on the bot's locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-testbotaliassettings.html#cfn-lex-bot-testbotaliassettings-botaliaslocalesettings
            '''
            result = self._values.get("bot_alias_locale_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.BotAliasLocaleSettingsItemProperty"]]]], result)

        @builtins.property
        def conversation_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ConversationLogSettingsProperty"]]:
            '''Specifies settings for conversation logs that save audio, text, and metadata information for conversations with your users.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-testbotaliassettings.html#cfn-lex-bot-testbotaliassettings-conversationlogsettings
            '''
            result = self._values.get("conversation_log_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ConversationLogSettingsProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''Specifies a description for the test bot alias.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-testbotaliassettings.html#cfn-lex-bot-testbotaliassettings-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sentiment_analysis_settings(self) -> typing.Any:
            '''Specifies whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-testbotaliassettings.html#cfn-lex-bot-testbotaliassettings-sentimentanalysissettings
            '''
            result = self._values.get("sentiment_analysis_settings")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TestBotAliasSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.TextInputSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"start_timeout_ms": "startTimeoutMs"},
    )
    class TextInputSpecificationProperty:
        def __init__(self, *, start_timeout_ms: jsii.Number) -> None:
            '''
            :param start_timeout_ms: ``CfnBot.TextInputSpecificationProperty.StartTimeoutMs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textinputspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                text_input_specification_property = lex.CfnBot.TextInputSpecificationProperty(
                    start_timeout_ms=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71608311423e59136a3e245126810e3b1a13181612dcd7e05e02d448e3bb5e0f)
                check_type(argname="argument start_timeout_ms", value=start_timeout_ms, expected_type=type_hints["start_timeout_ms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "start_timeout_ms": start_timeout_ms,
            }

        @builtins.property
        def start_timeout_ms(self) -> jsii.Number:
            '''``CfnBot.TextInputSpecificationProperty.StartTimeoutMs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textinputspecification.html#cfn-lex-bot-textinputspecification-starttimeoutms
            '''
            result = self._values.get("start_timeout_ms")
            assert result is not None, "Required property 'start_timeout_ms' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextInputSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.TextLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch": "cloudWatch"},
    )
    class TextLogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.CloudWatchLogGroupLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Specifies the Amazon CloudWatch Logs destination log group for conversation text logs.

            :param cloud_watch: Specifies the Amazon CloudWatch Logs log group where text and metadata logs are delivered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                text_log_destination_property = lex.CfnBot.TextLogDestinationProperty(
                    cloud_watch=lex.CfnBot.CloudWatchLogGroupLogDestinationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        log_prefix="logPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51a379ed9320c9fe288b5093153410193c754ff48b97cb1a09b61be67689ad7a)
                check_type(argname="argument cloud_watch", value=cloud_watch, expected_type=type_hints["cloud_watch"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cloud_watch": cloud_watch,
            }

        @builtins.property
        def cloud_watch(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.CloudWatchLogGroupLogDestinationProperty"]:
            '''Specifies the Amazon CloudWatch Logs log group where text and metadata logs are delivered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textlogdestination.html#cfn-lex-bot-textlogdestination-cloudwatch
            '''
            result = self._values.get("cloud_watch")
            assert result is not None, "Required property 'cloud_watch' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.CloudWatchLogGroupLogDestinationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.TextLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "enabled": "enabled"},
    )
    class TextLogSettingProperty:
        def __init__(
            self,
            *,
            destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.TextLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]],
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''Specifies settings to enable conversation logs.

            :param destination: Specifies the Amazon CloudWatch Logs destination log group for conversation text logs.
            :param enabled: Specifies whether conversation logs should be stored for an alias.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textlogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                text_log_setting_property = lex.CfnBot.TextLogSettingProperty(
                    destination=lex.CfnBot.TextLogDestinationProperty(
                        cloud_watch=lex.CfnBot.CloudWatchLogGroupLogDestinationProperty(
                            cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                            log_prefix="logPrefix"
                        )
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86bcd1e1abfed5de661ebe45b8f53167deb593668eab80d13e2dbbf0155ea8fe)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination": destination,
                "enabled": enabled,
            }

        @builtins.property
        def destination(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.TextLogDestinationProperty"]:
            '''Specifies the Amazon CloudWatch Logs destination log group for conversation text logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textlogsetting.html#cfn-lex-bot-textlogsetting-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.TextLogDestinationProperty"], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Specifies whether conversation logs should be stored for an alias.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-textlogsetting.html#cfn-lex-bot-textlogsetting-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.VoiceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"voice_id": "voiceId", "engine": "engine"},
    )
    class VoiceSettingsProperty:
        def __init__(
            self,
            *,
            voice_id: builtins.str,
            engine: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifies the Amazon Polly voice used for audio interaction with the user.

            :param voice_id: The Amazon Polly voice used for voice interaction with the user.
            :param engine: ``CfnBot.VoiceSettingsProperty.Engine``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-voicesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                voice_settings_property = lex.CfnBot.VoiceSettingsProperty(
                    voice_id="voiceId",
                
                    # the properties below are optional
                    engine="engine"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c549feb2fc08a186faf4edc6a402f03bc1c59e9aec68cb8520c1afd620e1a7d0)
                check_type(argname="argument voice_id", value=voice_id, expected_type=type_hints["voice_id"])
                check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "voice_id": voice_id,
            }
            if engine is not None:
                self._values["engine"] = engine

        @builtins.property
        def voice_id(self) -> builtins.str:
            '''The Amazon Polly voice used for voice interaction with the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-voicesettings.html#cfn-lex-bot-voicesettings-voiceid
            '''
            result = self._values.get("voice_id")
            assert result is not None, "Required property 'voice_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def engine(self) -> typing.Optional[builtins.str]:
            '''``CfnBot.VoiceSettingsProperty.Engine``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-voicesettings.html#cfn-lex-bot-voicesettings-engine
            '''
            result = self._values.get("engine")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VoiceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBot.WaitAndContinueSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "continue_response": "continueResponse",
            "waiting_response": "waitingResponse",
            "is_active": "isActive",
            "still_waiting_response": "stillWaitingResponse",
        },
    )
    class WaitAndContinueSpecificationProperty:
        def __init__(
            self,
            *,
            continue_response: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]],
            waiting_response: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.ResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]],
            is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            still_waiting_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBot.StillWaitingResponseSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the prompts that Amazon Lex uses while a bot is waiting for customer input.

            :param continue_response: The response that Amazon Lex sends to indicate that the bot is ready to continue the conversation.
            :param waiting_response: The response that Amazon Lex sends to indicate that the bot is waiting for the conversation to continue.
            :param is_active: Specifies whether the bot will wait for a user to respond. When this field is false, wait and continue responses for a slot aren't used and the bot expects an appropriate response within the configured timeout. If the IsActive field isn't specified, the default is true.
            :param still_waiting_response: A response that Amazon Lex sends periodically to the user to indicate that the bot is still waiting for input from the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                wait_and_continue_specification_property = lex.CfnBot.WaitAndContinueSpecificationProperty(
                    continue_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                    waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                
                        # the properties below are optional
                        allow_interrupt=False
                    ),
                
                    # the properties below are optional
                    is_active=False,
                    still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                        frequency_in_seconds=123,
                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            ),
                
                            # the properties below are optional
                            variations=[lex.CfnBot.MessageProperty(
                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                    value="value"
                                ),
                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                    title="title",
                
                                    # the properties below are optional
                                    buttons=[lex.CfnBot.ButtonProperty(
                                        text="text",
                                        value="value"
                                    )],
                                    image_url="imageUrl",
                                    subtitle="subtitle"
                                ),
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="value"
                                ),
                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                    value="value"
                                )
                            )]
                        )],
                        timeout_in_seconds=123,
                
                        # the properties below are optional
                        allow_interrupt=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db7ec7b22e666eb8c70be5be80fa6076961a5f2ed9849d555a9d1a08259844e4)
                check_type(argname="argument continue_response", value=continue_response, expected_type=type_hints["continue_response"])
                check_type(argname="argument waiting_response", value=waiting_response, expected_type=type_hints["waiting_response"])
                check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
                check_type(argname="argument still_waiting_response", value=still_waiting_response, expected_type=type_hints["still_waiting_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "continue_response": continue_response,
                "waiting_response": waiting_response,
            }
            if is_active is not None:
                self._values["is_active"] = is_active
            if still_waiting_response is not None:
                self._values["still_waiting_response"] = still_waiting_response

        @builtins.property
        def continue_response(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"]:
            '''The response that Amazon Lex sends to indicate that the bot is ready to continue the conversation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-continueresponse
            '''
            result = self._values.get("continue_response")
            assert result is not None, "Required property 'continue_response' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"], result)

        @builtins.property
        def waiting_response(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"]:
            '''The response that Amazon Lex sends to indicate that the bot is waiting for the conversation to continue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-waitingresponse
            '''
            result = self._values.get("waiting_response")
            assert result is not None, "Required property 'waiting_response' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.ResponseSpecificationProperty"], result)

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies whether the bot will wait for a user to respond.

            When this field is false, wait and continue responses for a slot aren't used and the bot expects an appropriate response within the configured timeout. If the IsActive field isn't specified, the default is true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def still_waiting_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.StillWaitingResponseSpecificationProperty"]]:
            '''A response that Amazon Lex sends periodically to the user to indicate that the bot is still waiting for input from the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-bot-waitandcontinuespecification.html#cfn-lex-bot-waitandcontinuespecification-stillwaitingresponse
            '''
            result = self._values.get("still_waiting_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBot.StillWaitingResponseSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WaitAndContinueSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnBotAlias(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lex.CfnBotAlias",
):
    '''A CloudFormation ``AWS::Lex::BotAlias``.

    .. epigraph::

       Amazon Lex V2 is the only supported version in AWS CloudFormation .

    Specifies an alias for the specified version of a bot. Use an alias to enable you to change the version of a bot without updating applications that use the bot.

    For example, you can specify an alias called "PROD" that your applications use to call the Amazon Lex bot.

    :cloudformationResource: AWS::Lex::BotAlias
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_lex as lex
        
        # sentiment_analysis_settings: Any
        
        cfn_bot_alias = lex.CfnBotAlias(self, "MyCfnBotAlias",
            bot_alias_name="botAliasName",
            bot_id="botId",
        
            # the properties below are optional
            bot_alias_locale_settings=[lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty(
                bot_alias_locale_setting=lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
                    enabled=False,
        
                    # the properties below are optional
                    code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
                        lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                            code_hook_interface_version="codeHookInterfaceVersion",
                            lambda_arn="lambdaArn"
                        )
                    )
                ),
                locale_id="localeId"
            )],
            bot_alias_tags=[CfnTag(
                key="key",
                value="value"
            )],
            bot_version="botVersion",
            conversation_log_settings=lex.CfnBotAlias.ConversationLogSettingsProperty(
                audio_log_settings=[lex.CfnBotAlias.AudioLogSettingProperty(
                    destination=lex.CfnBotAlias.AudioLogDestinationProperty(
                        s3_bucket=lex.CfnBotAlias.S3BucketLogDestinationProperty(
                            log_prefix="logPrefix",
                            s3_bucket_arn="s3BucketArn",
        
                            # the properties below are optional
                            kms_key_arn="kmsKeyArn"
                        )
                    ),
                    enabled=False
                )],
                text_log_settings=[lex.CfnBotAlias.TextLogSettingProperty(
                    destination=lex.CfnBotAlias.TextLogDestinationProperty(
                        cloud_watch=lex.CfnBotAlias.CloudWatchLogGroupLogDestinationProperty(
                            cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                            log_prefix="logPrefix"
                        )
                    ),
                    enabled=False
                )]
            ),
            description="description",
            sentiment_analysis_settings=sentiment_analysis_settings
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        bot_alias_name: builtins.str,
        bot_id: builtins.str,
        bot_alias_locale_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.BotAliasLocaleSettingsItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        bot_version: typing.Optional[builtins.str] = None,
        conversation_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.ConversationLogSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        sentiment_analysis_settings: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Lex::BotAlias``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bot_alias_name: The name of the bot alias.
        :param bot_id: The unique identifier of the bot.
        :param bot_alias_locale_settings: Maps configuration information to a specific locale. You can use this parameter to specify a specific Lambda function to run different functions in different locales.
        :param bot_alias_tags: An array of key-value pairs to apply to this resource. You can only add tags when you specify an alias. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param bot_version: The version of the bot that the bot alias references.
        :param conversation_log_settings: Specifies whether Amazon Lex logs text and audio for conversations with the bot. When you enable conversation logs, text logs store text input, transcripts of audio input, and associated metadata in Amazon CloudWatch logs. Audio logs store input in Amazon S3 .
        :param description: The description of the bot alias.
        :param sentiment_analysis_settings: Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0033e2634011545e69f53ada3f71b58664bbeb1b40a6cca16ce404405bcc3ff1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBotAliasProps(
            bot_alias_name=bot_alias_name,
            bot_id=bot_id,
            bot_alias_locale_settings=bot_alias_locale_settings,
            bot_alias_tags=bot_alias_tags,
            bot_version=bot_version,
            conversation_log_settings=conversation_log_settings,
            description=description,
            sentiment_analysis_settings=sentiment_analysis_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc1eaed3ce5db99103e345e12d309a2a02059bb60b71355abf6f697e4553d51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e48d939273237c40735642989bc712dd0b539da4023ab572aba709f4a771a0e0)
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
        '''The Amazon Resource Name (ARN) of the bot alias.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrBotAliasId")
    def attr_bot_alias_id(self) -> builtins.str:
        '''The unique identifier of the bot alias.

        :cloudformationAttribute: BotAliasId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBotAliasId"))

    @builtins.property
    @jsii.member(jsii_name="attrBotAliasStatus")
    def attr_bot_alias_status(self) -> builtins.str:
        '''The current status of the bot alias.

        When the status is Available the alias is ready for use with your bot.

        :cloudformationAttribute: BotAliasStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBotAliasStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="botAliasName")
    def bot_alias_name(self) -> builtins.str:
        '''The name of the bot alias.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliasname
        '''
        return typing.cast(builtins.str, jsii.get(self, "botAliasName"))

    @bot_alias_name.setter
    def bot_alias_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8dde915fc75ffc7d4697b07dffcb4b239dc4531f2fccd15afe26b2158e2afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botAliasName", value)

    @builtins.property
    @jsii.member(jsii_name="botId")
    def bot_id(self) -> builtins.str:
        '''The unique identifier of the bot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botid
        '''
        return typing.cast(builtins.str, jsii.get(self, "botId"))

    @bot_id.setter
    def bot_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3e24b6650d6fcb50149c6f6df36bfb474f1a6c2980fcc21166ddbe0073de9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botId", value)

    @builtins.property
    @jsii.member(jsii_name="sentimentAnalysisSettings")
    def sentiment_analysis_settings(self) -> typing.Any:
        '''Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-sentimentanalysissettings
        '''
        return typing.cast(typing.Any, jsii.get(self, "sentimentAnalysisSettings"))

    @sentiment_analysis_settings.setter
    def sentiment_analysis_settings(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61fd1202f74cf30d72b3387352924f892e9bf5d3464afdcb8e0d444b26295d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sentimentAnalysisSettings", value)

    @builtins.property
    @jsii.member(jsii_name="botAliasLocaleSettings")
    def bot_alias_locale_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.BotAliasLocaleSettingsItemProperty"]]]]:
        '''Maps configuration information to a specific locale.

        You can use this parameter to specify a specific Lambda function to run different functions in different locales.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliaslocalesettings
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.BotAliasLocaleSettingsItemProperty"]]]], jsii.get(self, "botAliasLocaleSettings"))

    @bot_alias_locale_settings.setter
    def bot_alias_locale_settings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.BotAliasLocaleSettingsItemProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27474b9d6c34036b5571fb162fc3a8c6d9426d1a9ff61cc2d5c7e8b7e913011d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botAliasLocaleSettings", value)

    @builtins.property
    @jsii.member(jsii_name="botAliasTags")
    def bot_alias_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]]:
        '''An array of key-value pairs to apply to this resource.

        You can only add tags when you specify an alias.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliastags
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]], jsii.get(self, "botAliasTags"))

    @bot_alias_tags.setter
    def bot_alias_tags(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c164f243d308ca08ecde6e510310a184a9be9d3c1f2f0088a7e999366196c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botAliasTags", value)

    @builtins.property
    @jsii.member(jsii_name="botVersion")
    def bot_version(self) -> typing.Optional[builtins.str]:
        '''The version of the bot that the bot alias references.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "botVersion"))

    @bot_version.setter
    def bot_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7febd15589f42cb13b75018bcee8db1da5abfd57bef44a72d7712bcb1da67e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botVersion", value)

    @builtins.property
    @jsii.member(jsii_name="conversationLogSettings")
    def conversation_log_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.ConversationLogSettingsProperty"]]:
        '''Specifies whether Amazon Lex logs text and audio for conversations with the bot.

        When you enable conversation logs, text logs store text input, transcripts of audio input, and associated metadata in Amazon CloudWatch logs. Audio logs store input in Amazon S3 .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-conversationlogsettings
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.ConversationLogSettingsProperty"]], jsii.get(self, "conversationLogSettings"))

    @conversation_log_settings.setter
    def conversation_log_settings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.ConversationLogSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1a02483838d91292dd9d3f0fda2045c37d1de6220332da8d7419713ab43fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conversationLogSettings", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the bot alias.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72bfc0faebc08882643ccece7eacf0512c38e153592ddd2392078878667b0873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.AudioLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket"},
    )
    class AudioLogDestinationProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.S3BucketLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Specifies the S3 bucket location where audio logs are stored.

            :param s3_bucket: The S3 bucket location where audio logs are stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                audio_log_destination_property = lex.CfnBotAlias.AudioLogDestinationProperty(
                    s3_bucket=lex.CfnBotAlias.S3BucketLogDestinationProperty(
                        log_prefix="logPrefix",
                        s3_bucket_arn="s3BucketArn",
                
                        # the properties below are optional
                        kms_key_arn="kmsKeyArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__568fc581a6e0457256b8069638a785fd15d4d221d0746265a7100adedd103cf4)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket": s3_bucket,
            }

        @builtins.property
        def s3_bucket(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.S3BucketLogDestinationProperty"]:
            '''The S3 bucket location where audio logs are stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologdestination.html#cfn-lex-botalias-audiologdestination-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.S3BucketLogDestinationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.AudioLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "enabled": "enabled"},
    )
    class AudioLogSettingProperty:
        def __init__(
            self,
            *,
            destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.AudioLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]],
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''Settings for logging audio of conversations between Amazon Lex and a user.

            You specify whether to log audio and the Amazon S3 bucket where the audio file is stored.

            :param destination: The location of audio log files collected when conversation logging is enabled for a bot.
            :param enabled: Determines whether audio logging in enabled for the bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                audio_log_setting_property = lex.CfnBotAlias.AudioLogSettingProperty(
                    destination=lex.CfnBotAlias.AudioLogDestinationProperty(
                        s3_bucket=lex.CfnBotAlias.S3BucketLogDestinationProperty(
                            log_prefix="logPrefix",
                            s3_bucket_arn="s3BucketArn",
                
                            # the properties below are optional
                            kms_key_arn="kmsKeyArn"
                        )
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__783da7d4119a2964ce0db3f3a3099ed7f2fd088e1ff8dff309da69d1c6fc6b3a)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination": destination,
                "enabled": enabled,
            }

        @builtins.property
        def destination(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.AudioLogDestinationProperty"]:
            '''The location of audio log files collected when conversation logging is enabled for a bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologsetting.html#cfn-lex-botalias-audiologsetting-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.AudioLogDestinationProperty"], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Determines whether audio logging in enabled for the bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-audiologsetting.html#cfn-lex-botalias-audiologsetting-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AudioLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bot_alias_locale_setting": "botAliasLocaleSetting",
            "locale_id": "localeId",
        },
    )
    class BotAliasLocaleSettingsItemProperty:
        def __init__(
            self,
            *,
            bot_alias_locale_setting: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.BotAliasLocaleSettingsProperty", typing.Dict[builtins.str, typing.Any]]],
            locale_id: builtins.str,
        ) -> None:
            '''Specifies settings that are unique to a locale.

            For example, you can use different Lambda function depending on the bot's locale.

            :param bot_alias_locale_setting: Specifies settings that are unique to a locale.
            :param locale_id: The unique identifier of the locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettingsitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                bot_alias_locale_settings_item_property = lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty(
                    bot_alias_locale_setting=lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
                        enabled=False,
                
                        # the properties below are optional
                        code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
                            lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                                code_hook_interface_version="codeHookInterfaceVersion",
                                lambda_arn="lambdaArn"
                            )
                        )
                    ),
                    locale_id="localeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__01c5abc23eca6282da359d7d4be5f597be13310d0b8c57d6566820705406f05f)
                check_type(argname="argument bot_alias_locale_setting", value=bot_alias_locale_setting, expected_type=type_hints["bot_alias_locale_setting"])
                check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bot_alias_locale_setting": bot_alias_locale_setting,
                "locale_id": locale_id,
            }

        @builtins.property
        def bot_alias_locale_setting(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.BotAliasLocaleSettingsProperty"]:
            '''Specifies settings that are unique to a locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettingsitem.html#cfn-lex-botalias-botaliaslocalesettingsitem-botaliaslocalesetting
            '''
            result = self._values.get("bot_alias_locale_setting")
            assert result is not None, "Required property 'bot_alias_locale_setting' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.BotAliasLocaleSettingsProperty"], result)

        @builtins.property
        def locale_id(self) -> builtins.str:
            '''The unique identifier of the locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettingsitem.html#cfn-lex-botalias-botaliaslocalesettingsitem-localeid
            '''
            result = self._values.get("locale_id")
            assert result is not None, "Required property 'locale_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotAliasLocaleSettingsItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.BotAliasLocaleSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "code_hook_specification": "codeHookSpecification",
        },
    )
    class BotAliasLocaleSettingsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            code_hook_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.CodeHookSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies settings that are unique to a locale.

            For example, you can use different Lambda function depending on the bot's locale.

            :param enabled: Determines whether the locale is enabled for the bot. If the value is false, the locale isn't available for use.
            :param code_hook_specification: Specifies the Lambda function that should be used in the locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                bot_alias_locale_settings_property = lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
                    enabled=False,
                
                    # the properties below are optional
                    code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
                        lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                            code_hook_interface_version="codeHookInterfaceVersion",
                            lambda_arn="lambdaArn"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40085ffc9108ae82c7ae5e17c5d82b02fc11cd773d07e89dff0d2aa75dfd317e)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument code_hook_specification", value=code_hook_specification, expected_type=type_hints["code_hook_specification"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }
            if code_hook_specification is not None:
                self._values["code_hook_specification"] = code_hook_specification

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Determines whether the locale is enabled for the bot.

            If the value is false, the locale isn't available for use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettings.html#cfn-lex-botalias-botaliaslocalesettings-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def code_hook_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.CodeHookSpecificationProperty"]]:
            '''Specifies the Lambda function that should be used in the locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-botaliaslocalesettings.html#cfn-lex-botalias-botaliaslocalesettings-codehookspecification
            '''
            result = self._values.get("code_hook_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.CodeHookSpecificationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotAliasLocaleSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.CloudWatchLogGroupLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
            "log_prefix": "logPrefix",
        },
    )
    class CloudWatchLogGroupLogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_log_group_arn: builtins.str,
            log_prefix: builtins.str,
        ) -> None:
            '''The Amazon CloudWatch Logs log group where the text and metadata logs are delivered.

            The log group must exist before you enable logging.

            :param cloud_watch_log_group_arn: The Amazon Resource Name (ARN) of the log group where text and metadata logs are delivered.
            :param log_prefix: The prefix of the log stream name within the log group that you specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-cloudwatchloggrouplogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                cloud_watch_log_group_log_destination_property = lex.CfnBotAlias.CloudWatchLogGroupLogDestinationProperty(
                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                    log_prefix="logPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__754f0770ab676e34d247fa73b12a17b618cf7573974b82d351acad9de2365aa2)
                check_type(argname="argument cloud_watch_log_group_arn", value=cloud_watch_log_group_arn, expected_type=type_hints["cloud_watch_log_group_arn"])
                check_type(argname="argument log_prefix", value=log_prefix, expected_type=type_hints["log_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cloud_watch_log_group_arn": cloud_watch_log_group_arn,
                "log_prefix": log_prefix,
            }

        @builtins.property
        def cloud_watch_log_group_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the log group where text and metadata logs are delivered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-cloudwatchloggrouplogdestination.html#cfn-lex-botalias-cloudwatchloggrouplogdestination-cloudwatchloggrouparn
            '''
            result = self._values.get("cloud_watch_log_group_arn")
            assert result is not None, "Required property 'cloud_watch_log_group_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_prefix(self) -> builtins.str:
            '''The prefix of the log stream name within the log group that you specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-cloudwatchloggrouplogdestination.html#cfn-lex-botalias-cloudwatchloggrouplogdestination-logprefix
            '''
            result = self._values.get("log_prefix")
            assert result is not None, "Required property 'log_prefix' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogGroupLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.CodeHookSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_code_hook": "lambdaCodeHook"},
    )
    class CodeHookSpecificationProperty:
        def __init__(
            self,
            *,
            lambda_code_hook: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.LambdaCodeHookProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Contains information about code hooks that Amazon Lex calls during a conversation.

            :param lambda_code_hook: Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-codehookspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                code_hook_specification_property = lex.CfnBotAlias.CodeHookSpecificationProperty(
                    lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                        code_hook_interface_version="codeHookInterfaceVersion",
                        lambda_arn="lambdaArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a6d59dfed10bb26471bb81404e9d5e62c76f020be70677485324be1fe8e9b47)
                check_type(argname="argument lambda_code_hook", value=lambda_code_hook, expected_type=type_hints["lambda_code_hook"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "lambda_code_hook": lambda_code_hook,
            }

        @builtins.property
        def lambda_code_hook(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.LambdaCodeHookProperty"]:
            '''Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-codehookspecification.html#cfn-lex-botalias-codehookspecification-lambdacodehook
            '''
            result = self._values.get("lambda_code_hook")
            assert result is not None, "Required property 'lambda_code_hook' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.LambdaCodeHookProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeHookSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.ConversationLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audio_log_settings": "audioLogSettings",
            "text_log_settings": "textLogSettings",
        },
    )
    class ConversationLogSettingsProperty:
        def __init__(
            self,
            *,
            audio_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.AudioLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            text_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.TextLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configures conversation logging that saves audio, text, and metadata for the conversations with your users.

            :param audio_log_settings: The Amazon S3 settings for logging audio to an S3 bucket.
            :param text_log_settings: The Amazon CloudWatch Logs settings for logging text and metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-conversationlogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                conversation_log_settings_property = lex.CfnBotAlias.ConversationLogSettingsProperty(
                    audio_log_settings=[lex.CfnBotAlias.AudioLogSettingProperty(
                        destination=lex.CfnBotAlias.AudioLogDestinationProperty(
                            s3_bucket=lex.CfnBotAlias.S3BucketLogDestinationProperty(
                                log_prefix="logPrefix",
                                s3_bucket_arn="s3BucketArn",
                
                                # the properties below are optional
                                kms_key_arn="kmsKeyArn"
                            )
                        ),
                        enabled=False
                    )],
                    text_log_settings=[lex.CfnBotAlias.TextLogSettingProperty(
                        destination=lex.CfnBotAlias.TextLogDestinationProperty(
                            cloud_watch=lex.CfnBotAlias.CloudWatchLogGroupLogDestinationProperty(
                                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                                log_prefix="logPrefix"
                            )
                        ),
                        enabled=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9008770d1e2263d944a42ccbf2c31e579fca9d57771ff50ed942ce39c838ffa)
                check_type(argname="argument audio_log_settings", value=audio_log_settings, expected_type=type_hints["audio_log_settings"])
                check_type(argname="argument text_log_settings", value=text_log_settings, expected_type=type_hints["text_log_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audio_log_settings is not None:
                self._values["audio_log_settings"] = audio_log_settings
            if text_log_settings is not None:
                self._values["text_log_settings"] = text_log_settings

        @builtins.property
        def audio_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.AudioLogSettingProperty"]]]]:
            '''The Amazon S3 settings for logging audio to an S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-conversationlogsettings.html#cfn-lex-botalias-conversationlogsettings-audiologsettings
            '''
            result = self._values.get("audio_log_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.AudioLogSettingProperty"]]]], result)

        @builtins.property
        def text_log_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.TextLogSettingProperty"]]]]:
            '''The Amazon CloudWatch Logs settings for logging text and metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-conversationlogsettings.html#cfn-lex-botalias-conversationlogsettings-textlogsettings
            '''
            result = self._values.get("text_log_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.TextLogSettingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConversationLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.LambdaCodeHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_hook_interface_version": "codeHookInterfaceVersion",
            "lambda_arn": "lambdaArn",
        },
    )
    class LambdaCodeHookProperty:
        def __init__(
            self,
            *,
            code_hook_interface_version: builtins.str,
            lambda_arn: builtins.str,
        ) -> None:
            '''Specifies a Lambda function that verifies requests to a bot or fulfills the user's request to a bot.

            :param code_hook_interface_version: The version of the request-response that you want Amazon Lex to use to invoke your Lambda function.
            :param lambda_arn: The Amazon Resource Name (ARN) of the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-lambdacodehook.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                lambda_code_hook_property = lex.CfnBotAlias.LambdaCodeHookProperty(
                    code_hook_interface_version="codeHookInterfaceVersion",
                    lambda_arn="lambdaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__342e895735070ce357a0a7bc974669e8506976ff219537978aa4b8dd9b9371da)
                check_type(argname="argument code_hook_interface_version", value=code_hook_interface_version, expected_type=type_hints["code_hook_interface_version"])
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "code_hook_interface_version": code_hook_interface_version,
                "lambda_arn": lambda_arn,
            }

        @builtins.property
        def code_hook_interface_version(self) -> builtins.str:
            '''The version of the request-response that you want Amazon Lex to use to invoke your Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-lambdacodehook.html#cfn-lex-botalias-lambdacodehook-codehookinterfaceversion
            '''
            result = self._values.get("code_hook_interface_version")
            assert result is not None, "Required property 'code_hook_interface_version' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def lambda_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-lambdacodehook.html#cfn-lex-botalias-lambdacodehook-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            assert result is not None, "Required property 'lambda_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaCodeHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.S3BucketLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_prefix": "logPrefix",
            "s3_bucket_arn": "s3BucketArn",
            "kms_key_arn": "kmsKeyArn",
        },
    )
    class S3BucketLogDestinationProperty:
        def __init__(
            self,
            *,
            log_prefix: builtins.str,
            s3_bucket_arn: builtins.str,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an Amazon S3 bucket for logging audio conversations.

            :param log_prefix: The S3 prefix to assign to audio log files.
            :param s3_bucket_arn: The Amazon Resource Name (ARN) of an Amazon S3 bucket where audio log files are stored.
            :param kms_key_arn: The Amazon Resource Name (ARN) of an AWS Key Management Service key for encrypting audio log files stored in an S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                s3_bucket_log_destination_property = lex.CfnBotAlias.S3BucketLogDestinationProperty(
                    log_prefix="logPrefix",
                    s3_bucket_arn="s3BucketArn",
                
                    # the properties below are optional
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__21ca74f2a19b0f31eb902f1c7c6a16b3907fef563719315b9e6dd564ce7963ee)
                check_type(argname="argument log_prefix", value=log_prefix, expected_type=type_hints["log_prefix"])
                check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_prefix": log_prefix,
                "s3_bucket_arn": s3_bucket_arn,
            }
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def log_prefix(self) -> builtins.str:
            '''The S3 prefix to assign to audio log files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html#cfn-lex-botalias-s3bucketlogdestination-logprefix
            '''
            result = self._values.get("log_prefix")
            assert result is not None, "Required property 'log_prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of an Amazon S3 bucket where audio log files are stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html#cfn-lex-botalias-s3bucketlogdestination-s3bucketarn
            '''
            result = self._values.get("s3_bucket_arn")
            assert result is not None, "Required property 's3_bucket_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Key Management Service key for encrypting audio log files stored in an S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-s3bucketlogdestination.html#cfn-lex-botalias-s3bucketlogdestination-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.SentimentAnalysisSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"detect_sentiment": "detectSentiment"},
    )
    class SentimentAnalysisSettingsProperty:
        def __init__(
            self,
            *,
            detect_sentiment: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''
            :param detect_sentiment: ``CfnBotAlias.SentimentAnalysisSettingsProperty.DetectSentiment``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-sentimentanalysissettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                sentiment_analysis_settings_property = lex.CfnBotAlias.SentimentAnalysisSettingsProperty(
                    detect_sentiment=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db1736ef08399f48feb86180360bfffdad3ba7b4cacf8e7f550fe8524849e1eb)
                check_type(argname="argument detect_sentiment", value=detect_sentiment, expected_type=type_hints["detect_sentiment"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "detect_sentiment": detect_sentiment,
            }

        @builtins.property
        def detect_sentiment(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''``CfnBotAlias.SentimentAnalysisSettingsProperty.DetectSentiment``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-sentimentanalysissettings.html#cfn-lex-botalias-sentimentanalysissettings-detectsentiment
            '''
            result = self._values.get("detect_sentiment")
            assert result is not None, "Required property 'detect_sentiment' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SentimentAnalysisSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.TextLogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch": "cloudWatch"},
    )
    class TextLogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.CloudWatchLogGroupLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Defines the Amazon CloudWatch Logs destination log group for conversation text logs.

            :param cloud_watch: Defines the Amazon CloudWatch Logs log group where text and metadata logs are delivered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                text_log_destination_property = lex.CfnBotAlias.TextLogDestinationProperty(
                    cloud_watch=lex.CfnBotAlias.CloudWatchLogGroupLogDestinationProperty(
                        cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                        log_prefix="logPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8cc7b91ff6f3795fc4fccedb4e3f614d0977c93983fea7e2f6ac0c42cb17529)
                check_type(argname="argument cloud_watch", value=cloud_watch, expected_type=type_hints["cloud_watch"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cloud_watch": cloud_watch,
            }

        @builtins.property
        def cloud_watch(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.CloudWatchLogGroupLogDestinationProperty"]:
            '''Defines the Amazon CloudWatch Logs log group where text and metadata logs are delivered.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogdestination.html#cfn-lex-botalias-textlogdestination-cloudwatch
            '''
            result = self._values.get("cloud_watch")
            assert result is not None, "Required property 'cloud_watch' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.CloudWatchLogGroupLogDestinationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextLogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotAlias.TextLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "enabled": "enabled"},
    )
    class TextLogSettingProperty:
        def __init__(
            self,
            *,
            destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotAlias.TextLogDestinationProperty", typing.Dict[builtins.str, typing.Any]]],
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        ) -> None:
            '''Defines settings to enable conversation logs.

            :param destination: Defines the Amazon CloudWatch Logs destination log group for conversation text logs.
            :param enabled: Determines whether conversation logs should be stored for an alias.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                text_log_setting_property = lex.CfnBotAlias.TextLogSettingProperty(
                    destination=lex.CfnBotAlias.TextLogDestinationProperty(
                        cloud_watch=lex.CfnBotAlias.CloudWatchLogGroupLogDestinationProperty(
                            cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                            log_prefix="logPrefix"
                        )
                    ),
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__20bd24ed340a979f0f5f7ce981be7b6841fce6c3c333e8ce6d112a3af8aeec5d)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination": destination,
                "enabled": enabled,
            }

        @builtins.property
        def destination(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.TextLogDestinationProperty"]:
            '''Defines the Amazon CloudWatch Logs destination log group for conversation text logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogsetting.html#cfn-lex-botalias-textlogsetting-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotAlias.TextLogDestinationProperty"], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Determines whether conversation logs should be stored for an alias.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botalias-textlogsetting.html#cfn-lex-botalias-textlogsetting-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lex.CfnBotAliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "bot_alias_name": "botAliasName",
        "bot_id": "botId",
        "bot_alias_locale_settings": "botAliasLocaleSettings",
        "bot_alias_tags": "botAliasTags",
        "bot_version": "botVersion",
        "conversation_log_settings": "conversationLogSettings",
        "description": "description",
        "sentiment_analysis_settings": "sentimentAnalysisSettings",
    },
)
class CfnBotAliasProps:
    def __init__(
        self,
        *,
        bot_alias_name: builtins.str,
        bot_id: builtins.str,
        bot_alias_locale_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.BotAliasLocaleSettingsItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        bot_version: typing.Optional[builtins.str] = None,
        conversation_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.ConversationLogSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        sentiment_analysis_settings: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnBotAlias``.

        :param bot_alias_name: The name of the bot alias.
        :param bot_id: The unique identifier of the bot.
        :param bot_alias_locale_settings: Maps configuration information to a specific locale. You can use this parameter to specify a specific Lambda function to run different functions in different locales.
        :param bot_alias_tags: An array of key-value pairs to apply to this resource. You can only add tags when you specify an alias. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param bot_version: The version of the bot that the bot alias references.
        :param conversation_log_settings: Specifies whether Amazon Lex logs text and audio for conversations with the bot. When you enable conversation logs, text logs store text input, transcripts of audio input, and associated metadata in Amazon CloudWatch logs. Audio logs store input in Amazon S3 .
        :param description: The description of the bot alias.
        :param sentiment_analysis_settings: Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_lex as lex
            
            # sentiment_analysis_settings: Any
            
            cfn_bot_alias_props = lex.CfnBotAliasProps(
                bot_alias_name="botAliasName",
                bot_id="botId",
            
                # the properties below are optional
                bot_alias_locale_settings=[lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty(
                    bot_alias_locale_setting=lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
                        enabled=False,
            
                        # the properties below are optional
                        code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
                            lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                                code_hook_interface_version="codeHookInterfaceVersion",
                                lambda_arn="lambdaArn"
                            )
                        )
                    ),
                    locale_id="localeId"
                )],
                bot_alias_tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                bot_version="botVersion",
                conversation_log_settings=lex.CfnBotAlias.ConversationLogSettingsProperty(
                    audio_log_settings=[lex.CfnBotAlias.AudioLogSettingProperty(
                        destination=lex.CfnBotAlias.AudioLogDestinationProperty(
                            s3_bucket=lex.CfnBotAlias.S3BucketLogDestinationProperty(
                                log_prefix="logPrefix",
                                s3_bucket_arn="s3BucketArn",
            
                                # the properties below are optional
                                kms_key_arn="kmsKeyArn"
                            )
                        ),
                        enabled=False
                    )],
                    text_log_settings=[lex.CfnBotAlias.TextLogSettingProperty(
                        destination=lex.CfnBotAlias.TextLogDestinationProperty(
                            cloud_watch=lex.CfnBotAlias.CloudWatchLogGroupLogDestinationProperty(
                                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                                log_prefix="logPrefix"
                            )
                        ),
                        enabled=False
                    )]
                ),
                description="description",
                sentiment_analysis_settings=sentiment_analysis_settings
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fcb128b628f95e893ab0bc6c0d720a0e70d788682e6a9f9e6c8ed6b019135a7)
            check_type(argname="argument bot_alias_name", value=bot_alias_name, expected_type=type_hints["bot_alias_name"])
            check_type(argname="argument bot_id", value=bot_id, expected_type=type_hints["bot_id"])
            check_type(argname="argument bot_alias_locale_settings", value=bot_alias_locale_settings, expected_type=type_hints["bot_alias_locale_settings"])
            check_type(argname="argument bot_alias_tags", value=bot_alias_tags, expected_type=type_hints["bot_alias_tags"])
            check_type(argname="argument bot_version", value=bot_version, expected_type=type_hints["bot_version"])
            check_type(argname="argument conversation_log_settings", value=conversation_log_settings, expected_type=type_hints["conversation_log_settings"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument sentiment_analysis_settings", value=sentiment_analysis_settings, expected_type=type_hints["sentiment_analysis_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bot_alias_name": bot_alias_name,
            "bot_id": bot_id,
        }
        if bot_alias_locale_settings is not None:
            self._values["bot_alias_locale_settings"] = bot_alias_locale_settings
        if bot_alias_tags is not None:
            self._values["bot_alias_tags"] = bot_alias_tags
        if bot_version is not None:
            self._values["bot_version"] = bot_version
        if conversation_log_settings is not None:
            self._values["conversation_log_settings"] = conversation_log_settings
        if description is not None:
            self._values["description"] = description
        if sentiment_analysis_settings is not None:
            self._values["sentiment_analysis_settings"] = sentiment_analysis_settings

    @builtins.property
    def bot_alias_name(self) -> builtins.str:
        '''The name of the bot alias.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliasname
        '''
        result = self._values.get("bot_alias_name")
        assert result is not None, "Required property 'bot_alias_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bot_id(self) -> builtins.str:
        '''The unique identifier of the bot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botid
        '''
        result = self._values.get("bot_id")
        assert result is not None, "Required property 'bot_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bot_alias_locale_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBotAlias.BotAliasLocaleSettingsItemProperty]]]]:
        '''Maps configuration information to a specific locale.

        You can use this parameter to specify a specific Lambda function to run different functions in different locales.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliaslocalesettings
        '''
        result = self._values.get("bot_alias_locale_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBotAlias.BotAliasLocaleSettingsItemProperty]]]], result)

    @builtins.property
    def bot_alias_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]]:
        '''An array of key-value pairs to apply to this resource.

        You can only add tags when you specify an alias.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botaliastags
        '''
        result = self._values.get("bot_alias_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]], result)

    @builtins.property
    def bot_version(self) -> typing.Optional[builtins.str]:
        '''The version of the bot that the bot alias references.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-botversion
        '''
        result = self._values.get("bot_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conversation_log_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBotAlias.ConversationLogSettingsProperty]]:
        '''Specifies whether Amazon Lex logs text and audio for conversations with the bot.

        When you enable conversation logs, text logs store text input, transcripts of audio input, and associated metadata in Amazon CloudWatch logs. Audio logs store input in Amazon S3 .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-conversationlogsettings
        '''
        result = self._values.get("conversation_log_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBotAlias.ConversationLogSettingsProperty]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the bot alias.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sentiment_analysis_settings(self) -> typing.Any:
        '''Determines whether Amazon Lex will use Amazon Comprehend to detect the sentiment of user utterances.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botalias.html#cfn-lex-botalias-sentimentanalysissettings
        '''
        result = self._values.get("sentiment_analysis_settings")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBotAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lex.CfnBotProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_privacy": "dataPrivacy",
        "idle_session_ttl_in_seconds": "idleSessionTtlInSeconds",
        "name": "name",
        "role_arn": "roleArn",
        "auto_build_bot_locales": "autoBuildBotLocales",
        "bot_file_s3_location": "botFileS3Location",
        "bot_locales": "botLocales",
        "bot_tags": "botTags",
        "description": "description",
        "test_bot_alias_settings": "testBotAliasSettings",
        "test_bot_alias_tags": "testBotAliasTags",
    },
)
class CfnBotProps:
    def __init__(
        self,
        *,
        data_privacy: typing.Any,
        idle_session_ttl_in_seconds: jsii.Number,
        name: builtins.str,
        role_arn: builtins.str,
        auto_build_bot_locales: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        bot_file_s3_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        bot_locales: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.BotLocaleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        bot_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        test_bot_alias_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.TestBotAliasSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        test_bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnBot``.

        :param data_privacy: Provides information on additional privacy protections Amazon Lex should use with the bot's data.
        :param idle_session_ttl_in_seconds: The time, in seconds, that Amazon Lex should keep information about a user's conversation with the bot. A user interaction remains active for the amount of time specified. If no conversation occurs during this time, the session expires and Amazon Lex deletes any data provided before the timeout. You can specify between 60 (1 minute) and 86,400 (24 hours) seconds.
        :param name: The name of the field to filter the list of bots.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role used to build and run the bot.
        :param auto_build_bot_locales: Indicates whether Amazon Lex V2 should automatically build the locales for the bot after a change.
        :param bot_file_s3_location: The Amazon S3 location of files used to import a bot. The files must be in the import format specified in `JSON format for importing and exporting <https://docs.aws.amazon.com/lexv2/latest/dg/import-export-format.html>`_ in the *Amazon Lex developer guide.*
        :param bot_locales: A list of locales for the bot.
        :param bot_tags: A list of tags to add to the bot. You can only add tags when you import a bot. You can't use the ``UpdateBot`` operation to update tags. To update tags, use the ``TagResource`` operation.
        :param description: The description of the version.
        :param test_bot_alias_settings: Specifies configuration settings for the alias used to test the bot. If the ``TestBotAliasSettings`` property is not specified, the settings are configured with default values.
        :param test_bot_alias_tags: A list of tags to add to the test alias for a bot. You can only add tags when you import a bot. You can't use the ``UpdateAlias`` operation to update tags. To update tags on the test alias, use the ``TagResource`` operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_lex as lex
            
            # data_privacy: Any
            # sentiment_analysis_settings: Any
            
            cfn_bot_props = lex.CfnBotProps(
                data_privacy=data_privacy,
                idle_session_ttl_in_seconds=123,
                name="name",
                role_arn="roleArn",
            
                # the properties below are optional
                auto_build_bot_locales=False,
                bot_file_s3_location=lex.CfnBot.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_object_key="s3ObjectKey",
            
                    # the properties below are optional
                    s3_object_version="s3ObjectVersion"
                ),
                bot_locales=[lex.CfnBot.BotLocaleProperty(
                    locale_id="localeId",
                    nlu_confidence_threshold=123,
            
                    # the properties below are optional
                    custom_vocabulary=lex.CfnBot.CustomVocabularyProperty(
                        custom_vocabulary_items=[lex.CfnBot.CustomVocabularyItemProperty(
                            phrase="phrase",
            
                            # the properties below are optional
                            weight=123
                        )]
                    ),
                    description="description",
                    intents=[lex.CfnBot.IntentProperty(
                        name="name",
            
                        # the properties below are optional
                        description="description",
                        dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                            enabled=False
                        ),
                        fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                            enabled=False,
            
                            # the properties below are optional
                            fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(
                                active=False,
            
                                # the properties below are optional
                                start_response=lex.CfnBot.FulfillmentStartResponseSpecificationProperty(
                                    delay_in_seconds=123,
                                    message_groups=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                timeout_in_seconds=123,
                                update_response=lex.CfnBot.FulfillmentUpdateResponseSpecificationProperty(
                                    frequency_in_seconds=123,
                                    message_groups=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            ),
                            post_fulfillment_status_specification=lex.CfnBot.PostFulfillmentStatusSpecificationProperty(
                                failure_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                success_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                ),
                                timeout_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False
                                )
                            )
                        ),
                        input_contexts=[lex.CfnBot.InputContextProperty(
                            name="name"
                        )],
                        intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                            closing_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
            
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
            
                                # the properties below are optional
                                allow_interrupt=False
                            ),
            
                            # the properties below are optional
                            is_active=False
                        ),
                        intent_confirmation_setting=lex.CfnBot.IntentConfirmationSettingProperty(
                            declination_response=lex.CfnBot.ResponseSpecificationProperty(
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
            
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
            
                                # the properties below are optional
                                allow_interrupt=False
                            ),
                            prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                max_retries=123,
                                message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    ),
            
                                    # the properties below are optional
                                    variations=[lex.CfnBot.MessageProperty(
                                        custom_payload=lex.CfnBot.CustomPayloadProperty(
                                            value="value"
                                        ),
                                        image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                            title="title",
            
                                            # the properties below are optional
                                            buttons=[lex.CfnBot.ButtonProperty(
                                                text="text",
                                                value="value"
                                            )],
                                            image_url="imageUrl",
                                            subtitle="subtitle"
                                        ),
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="value"
                                        ),
                                        ssml_message=lex.CfnBot.SSMLMessageProperty(
                                            value="value"
                                        )
                                    )]
                                )],
            
                                # the properties below are optional
                                allow_interrupt=False,
                                message_selection_strategy="messageSelectionStrategy",
                                prompt_attempts_specification={
                                    "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                        allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                            allow_audio_input=False,
                                            allow_dtmf_input=False
                                        ),
            
                                        # the properties below are optional
                                        allow_interrupt=False,
                                        audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                            start_timeout_ms=123,
            
                                            # the properties below are optional
                                            audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                                end_timeout_ms=123,
                                                max_length_ms=123
                                            ),
                                            dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                                deletion_character="deletionCharacter",
                                                end_character="endCharacter",
                                                end_timeout_ms=123,
                                                max_length=123
                                            )
                                        ),
                                        text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                            start_timeout_ms=123
                                        )
                                    )
                                }
                            ),
            
                            # the properties below are optional
                            is_active=False
                        ),
                        kendra_configuration=lex.CfnBot.KendraConfigurationProperty(
                            kendra_index="kendraIndex",
            
                            # the properties below are optional
                            query_filter_string="queryFilterString",
                            query_filter_string_enabled=False
                        ),
                        output_contexts=[lex.CfnBot.OutputContextProperty(
                            name="name",
                            time_to_live_in_seconds=123,
                            turns_to_live=123
                        )],
                        parent_intent_signature="parentIntentSignature",
                        sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                            utterance="utterance"
                        )],
                        slot_priorities=[lex.CfnBot.SlotPriorityProperty(
                            priority=123,
                            slot_name="slotName"
                        )],
                        slots=[lex.CfnBot.SlotProperty(
                            name="name",
                            slot_type_name="slotTypeName",
                            value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                                slot_constraint="slotConstraint",
            
                                # the properties below are optional
                                default_value_specification=lex.CfnBot.SlotDefaultValueSpecificationProperty(
                                    default_value_list=[lex.CfnBot.SlotDefaultValueProperty(
                                        default_value="defaultValue"
                                    )]
                                ),
                                prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                    max_retries=123,
                                    message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                        message=lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        ),
            
                                        # the properties below are optional
                                        variations=[lex.CfnBot.MessageProperty(
                                            custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                value="value"
                                            ),
                                            image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                title="title",
            
                                                # the properties below are optional
                                                buttons=[lex.CfnBot.ButtonProperty(
                                                    text="text",
                                                    value="value"
                                                )],
                                                image_url="imageUrl",
                                                subtitle="subtitle"
                                            ),
                                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                value="value"
                                            ),
                                            ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                value="value"
                                            )
                                        )]
                                    )],
            
                                    # the properties below are optional
                                    allow_interrupt=False,
                                    message_selection_strategy="messageSelectionStrategy",
                                    prompt_attempts_specification={
                                        "prompt_attempts_specification_key": lex.CfnBot.PromptAttemptSpecificationProperty(
                                            allowed_input_types=lex.CfnBot.AllowedInputTypesProperty(
                                                allow_audio_input=False,
                                                allow_dtmf_input=False
                                            ),
            
                                            # the properties below are optional
                                            allow_interrupt=False,
                                            audio_and_dtmf_input_specification=lex.CfnBot.AudioAndDTMFInputSpecificationProperty(
                                                start_timeout_ms=123,
            
                                                # the properties below are optional
                                                audio_specification=lex.CfnBot.AudioSpecificationProperty(
                                                    end_timeout_ms=123,
                                                    max_length_ms=123
                                                ),
                                                dtmf_specification=lex.CfnBot.DTMFSpecificationProperty(
                                                    deletion_character="deletionCharacter",
                                                    end_character="endCharacter",
                                                    end_timeout_ms=123,
                                                    max_length=123
                                                )
                                            ),
                                            text_input_specification=lex.CfnBot.TextInputSpecificationProperty(
                                                start_timeout_ms=123
                                            )
                                        )
                                    }
                                ),
                                sample_utterances=[lex.CfnBot.SampleUtteranceProperty(
                                    utterance="utterance"
                                )],
                                wait_and_continue_specification=lex.CfnBot.WaitAndContinueSpecificationProperty(
                                    continue_response=lex.CfnBot.ResponseSpecificationProperty(
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
            
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
            
                                        # the properties below are optional
                                        allow_interrupt=False
                                    ),
                                    waiting_response=lex.CfnBot.ResponseSpecificationProperty(
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
            
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
            
                                        # the properties below are optional
                                        allow_interrupt=False
                                    ),
            
                                    # the properties below are optional
                                    is_active=False,
                                    still_waiting_response=lex.CfnBot.StillWaitingResponseSpecificationProperty(
                                        frequency_in_seconds=123,
                                        message_groups_list=[lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            ),
            
                                            # the properties below are optional
                                            variations=[lex.CfnBot.MessageProperty(
                                                custom_payload=lex.CfnBot.CustomPayloadProperty(
                                                    value="value"
                                                ),
                                                image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                                    title="title",
            
                                                    # the properties below are optional
                                                    buttons=[lex.CfnBot.ButtonProperty(
                                                        text="text",
                                                        value="value"
                                                    )],
                                                    image_url="imageUrl",
                                                    subtitle="subtitle"
                                                ),
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="value"
                                                ),
                                                ssml_message=lex.CfnBot.SSMLMessageProperty(
                                                    value="value"
                                                )
                                            )]
                                        )],
                                        timeout_in_seconds=123,
            
                                        # the properties below are optional
                                        allow_interrupt=False
                                    )
                                )
                            ),
            
                            # the properties below are optional
                            description="description",
                            multiple_values_setting=lex.CfnBot.MultipleValuesSettingProperty(
                                allow_multiple_values=False
                            ),
                            obfuscation_setting=lex.CfnBot.ObfuscationSettingProperty(
                                obfuscation_setting_type="obfuscationSettingType"
                            )
                        )]
                    )],
                    slot_types=[lex.CfnBot.SlotTypeProperty(
                        name="name",
            
                        # the properties below are optional
                        description="description",
                        external_source_setting=lex.CfnBot.ExternalSourceSettingProperty(
                            grammar_slot_type_setting=lex.CfnBot.GrammarSlotTypeSettingProperty(
                                source=lex.CfnBot.GrammarSlotTypeSourceProperty(
                                    s3_bucket_name="s3BucketName",
                                    s3_object_key="s3ObjectKey",
            
                                    # the properties below are optional
                                    kms_key_arn="kmsKeyArn"
                                )
                            )
                        ),
                        parent_slot_type_signature="parentSlotTypeSignature",
                        slot_type_values=[lex.CfnBot.SlotTypeValueProperty(
                            sample_value=lex.CfnBot.SampleValueProperty(
                                value="value"
                            ),
            
                            # the properties below are optional
                            synonyms=[lex.CfnBot.SampleValueProperty(
                                value="value"
                            )]
                        )],
                        value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                            resolution_strategy="resolutionStrategy",
            
                            # the properties below are optional
                            advanced_recognition_setting=lex.CfnBot.AdvancedRecognitionSettingProperty(
                                audio_recognition_strategy="audioRecognitionStrategy"
                            ),
                            regex_filter=lex.CfnBot.SlotValueRegexFilterProperty(
                                pattern="pattern"
                            )
                        )
                    )],
                    voice_settings=lex.CfnBot.VoiceSettingsProperty(
                        voice_id="voiceId",
            
                        # the properties below are optional
                        engine="engine"
                    )
                )],
                bot_tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                description="description",
                test_bot_alias_settings=lex.CfnBot.TestBotAliasSettingsProperty(
                    bot_alias_locale_settings=[lex.CfnBot.BotAliasLocaleSettingsItemProperty(
                        bot_alias_locale_setting=lex.CfnBot.BotAliasLocaleSettingsProperty(
                            enabled=False,
            
                            # the properties below are optional
                            code_hook_specification=lex.CfnBot.CodeHookSpecificationProperty(
                                lambda_code_hook=lex.CfnBot.LambdaCodeHookProperty(
                                    code_hook_interface_version="codeHookInterfaceVersion",
                                    lambda_arn="lambdaArn"
                                )
                            )
                        ),
                        locale_id="localeId"
                    )],
                    conversation_log_settings=lex.CfnBot.ConversationLogSettingsProperty(
                        audio_log_settings=[lex.CfnBot.AudioLogSettingProperty(
                            destination=lex.CfnBot.AudioLogDestinationProperty(
                                s3_bucket=lex.CfnBot.S3BucketLogDestinationProperty(
                                    log_prefix="logPrefix",
                                    s3_bucket_arn="s3BucketArn",
            
                                    # the properties below are optional
                                    kms_key_arn="kmsKeyArn"
                                )
                            ),
                            enabled=False
                        )],
                        text_log_settings=[lex.CfnBot.TextLogSettingProperty(
                            destination=lex.CfnBot.TextLogDestinationProperty(
                                cloud_watch=lex.CfnBot.CloudWatchLogGroupLogDestinationProperty(
                                    cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                                    log_prefix="logPrefix"
                                )
                            ),
                            enabled=False
                        )]
                    ),
                    description="description",
                    sentiment_analysis_settings=sentiment_analysis_settings
                ),
                test_bot_alias_tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be4e658521508c907a690800c0a3f0a926558d7dd2ee7093d2fe01938f7b0ed)
            check_type(argname="argument data_privacy", value=data_privacy, expected_type=type_hints["data_privacy"])
            check_type(argname="argument idle_session_ttl_in_seconds", value=idle_session_ttl_in_seconds, expected_type=type_hints["idle_session_ttl_in_seconds"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument auto_build_bot_locales", value=auto_build_bot_locales, expected_type=type_hints["auto_build_bot_locales"])
            check_type(argname="argument bot_file_s3_location", value=bot_file_s3_location, expected_type=type_hints["bot_file_s3_location"])
            check_type(argname="argument bot_locales", value=bot_locales, expected_type=type_hints["bot_locales"])
            check_type(argname="argument bot_tags", value=bot_tags, expected_type=type_hints["bot_tags"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument test_bot_alias_settings", value=test_bot_alias_settings, expected_type=type_hints["test_bot_alias_settings"])
            check_type(argname="argument test_bot_alias_tags", value=test_bot_alias_tags, expected_type=type_hints["test_bot_alias_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_privacy": data_privacy,
            "idle_session_ttl_in_seconds": idle_session_ttl_in_seconds,
            "name": name,
            "role_arn": role_arn,
        }
        if auto_build_bot_locales is not None:
            self._values["auto_build_bot_locales"] = auto_build_bot_locales
        if bot_file_s3_location is not None:
            self._values["bot_file_s3_location"] = bot_file_s3_location
        if bot_locales is not None:
            self._values["bot_locales"] = bot_locales
        if bot_tags is not None:
            self._values["bot_tags"] = bot_tags
        if description is not None:
            self._values["description"] = description
        if test_bot_alias_settings is not None:
            self._values["test_bot_alias_settings"] = test_bot_alias_settings
        if test_bot_alias_tags is not None:
            self._values["test_bot_alias_tags"] = test_bot_alias_tags

    @builtins.property
    def data_privacy(self) -> typing.Any:
        '''Provides information on additional privacy protections Amazon Lex should use with the bot's data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-dataprivacy
        '''
        result = self._values.get("data_privacy")
        assert result is not None, "Required property 'data_privacy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def idle_session_ttl_in_seconds(self) -> jsii.Number:
        '''The time, in seconds, that Amazon Lex should keep information about a user's conversation with the bot.

        A user interaction remains active for the amount of time specified. If no conversation occurs during this time, the session expires and Amazon Lex deletes any data provided before the timeout.

        You can specify between 60 (1 minute) and 86,400 (24 hours) seconds.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-idlesessionttlinseconds
        '''
        result = self._values.get("idle_session_ttl_in_seconds")
        assert result is not None, "Required property 'idle_session_ttl_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the field to filter the list of bots.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role used to build and run the bot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_build_bot_locales(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether Amazon Lex V2 should automatically build the locales for the bot after a change.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-autobuildbotlocales
        '''
        result = self._values.get("auto_build_bot_locales")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def bot_file_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBot.S3LocationProperty]]:
        '''The Amazon S3 location of files used to import a bot.

        The files must be in the import format specified in `JSON format for importing and exporting <https://docs.aws.amazon.com/lexv2/latest/dg/import-export-format.html>`_ in the *Amazon Lex developer guide.*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-botfiles3location
        '''
        result = self._values.get("bot_file_s3_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBot.S3LocationProperty]], result)

    @builtins.property
    def bot_locales(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBot.BotLocaleProperty]]]]:
        '''A list of locales for the bot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-botlocales
        '''
        result = self._values.get("bot_locales")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBot.BotLocaleProperty]]]], result)

    @builtins.property
    def bot_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]]:
        '''A list of tags to add to the bot.

        You can only add tags when you import a bot. You can't use the ``UpdateBot`` operation to update tags. To update tags, use the ``TagResource`` operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-bottags
        '''
        result = self._values.get("bot_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_bot_alias_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBot.TestBotAliasSettingsProperty]]:
        '''Specifies configuration settings for the alias used to test the bot.

        If the ``TestBotAliasSettings`` property is not specified, the settings are configured with default values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-testbotaliassettings
        '''
        result = self._values.get("test_bot_alias_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBot.TestBotAliasSettingsProperty]], result)

    @builtins.property
    def test_bot_alias_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]]:
        '''A list of tags to add to the test alias for a bot.

        You can only add tags when you import a bot. You can't use the ``UpdateAlias`` operation to update tags. To update tags on the test alias, use the ``TagResource`` operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-bot.html#cfn-lex-bot-testbotaliastags
        '''
        result = self._values.get("test_bot_alias_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBotProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnBotVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lex.CfnBotVersion",
):
    '''A CloudFormation ``AWS::Lex::BotVersion``.

    .. epigraph::

       Amazon Lex V2 is the only supported version in AWS CloudFormation .

    Specifies a new version of the bot based on the ``DRAFT`` version. If the ``DRAFT`` version of this resource hasn't changed since you created the last version, Amazon Lex doesn't create a new version, it returns the last created version.

    When you specify the first version of a bot, Amazon Lex sets the version to 1. Subsequent versions increment by 1.

    :cloudformationResource: AWS::Lex::BotVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_lex as lex
        
        cfn_bot_version = lex.CfnBotVersion(self, "MyCfnBotVersion",
            bot_id="botId",
            bot_version_locale_specification=[lex.CfnBotVersion.BotVersionLocaleSpecificationProperty(
                bot_version_locale_details=lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
                    source_bot_version="sourceBotVersion"
                ),
                locale_id="localeId"
            )],
        
            # the properties below are optional
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        bot_id: builtins.str,
        bot_version_locale_specification: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotVersion.BotVersionLocaleSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Lex::BotVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bot_id: The unique identifier of the bot.
        :param bot_version_locale_specification: Specifies the locales that Amazon Lex adds to this version. You can choose the Draft version or any other previously published version for each locale. When you specify a source version, the locale data is copied from the source version to the new version.
        :param description: The description of the version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1934dc39f98d55c070d52078083145d29a33bb2fe35b0f4acde668a01f2c33b2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBotVersionProps(
            bot_id=bot_id,
            bot_version_locale_specification=bot_version_locale_specification,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6625f4fcb54267efbeb6c4db940a3f001ad4b1f0bae2aeac4a501095f706c38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__798d43461bb19174849f5fba35f737b5b792ddb51727ee6cc3a992d6d3822f12)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrBotVersion")
    def attr_bot_version(self) -> builtins.str:
        '''The version of the bot.

        :cloudformationAttribute: BotVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBotVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="botId")
    def bot_id(self) -> builtins.str:
        '''The unique identifier of the bot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-botid
        '''
        return typing.cast(builtins.str, jsii.get(self, "botId"))

    @bot_id.setter
    def bot_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02571acc0fb69d81968876064577b6db79c1133f325d528d26171d2e66f7d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botId", value)

    @builtins.property
    @jsii.member(jsii_name="botVersionLocaleSpecification")
    def bot_version_locale_specification(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotVersion.BotVersionLocaleSpecificationProperty"]]]:
        '''Specifies the locales that Amazon Lex adds to this version.

        You can choose the Draft version or any other previously published version for each locale. When you specify a source version, the locale data is copied from the source version to the new version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-botversionlocalespecification
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotVersion.BotVersionLocaleSpecificationProperty"]]], jsii.get(self, "botVersionLocaleSpecification"))

    @bot_version_locale_specification.setter
    def bot_version_locale_specification(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotVersion.BotVersionLocaleSpecificationProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99646775afda16766820f18de65ac94bd38dd1a4e93ba05d173b84d5180762e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botVersionLocaleSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf35d04dc8ee6312e2cb00d3b2f180d838e5cc8e39a1387fdc8a1f0ae1ac53c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotVersion.BotVersionLocaleDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"source_bot_version": "sourceBotVersion"},
    )
    class BotVersionLocaleDetailsProperty:
        def __init__(self, *, source_bot_version: builtins.str) -> None:
            '''The version of a bot used for a bot locale.

            :param source_bot_version: The version of a bot used for a bot locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocaledetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                bot_version_locale_details_property = lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
                    source_bot_version="sourceBotVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8d372396ab35154b85f98ee9b374cd281ae55e673243467be1d555a4ccef696)
                check_type(argname="argument source_bot_version", value=source_bot_version, expected_type=type_hints["source_bot_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "source_bot_version": source_bot_version,
            }

        @builtins.property
        def source_bot_version(self) -> builtins.str:
            '''The version of a bot used for a bot locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocaledetails.html#cfn-lex-botversion-botversionlocaledetails-sourcebotversion
            '''
            result = self._values.get("source_bot_version")
            assert result is not None, "Required property 'source_bot_version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotVersionLocaleDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-lex.CfnBotVersion.BotVersionLocaleSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bot_version_locale_details": "botVersionLocaleDetails",
            "locale_id": "localeId",
        },
    )
    class BotVersionLocaleSpecificationProperty:
        def __init__(
            self,
            *,
            bot_version_locale_details: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBotVersion.BotVersionLocaleDetailsProperty", typing.Dict[builtins.str, typing.Any]]],
            locale_id: builtins.str,
        ) -> None:
            '''Specifies the locale that Amazon Lex adds to this version.

            You can choose the Draft version or any other previously published version for each locale. When you specify a source version, the locale data is copied from the source version to the new version.

            :param bot_version_locale_details: The version of a bot used for a bot locale.
            :param locale_id: The identifier of the locale to add to the version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocalespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_lex as lex
                
                bot_version_locale_specification_property = lex.CfnBotVersion.BotVersionLocaleSpecificationProperty(
                    bot_version_locale_details=lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
                        source_bot_version="sourceBotVersion"
                    ),
                    locale_id="localeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09b2123fe95f8731f187cf2a68d53d5ce8e5865d0cc09b9b5e24613227546c54)
                check_type(argname="argument bot_version_locale_details", value=bot_version_locale_details, expected_type=type_hints["bot_version_locale_details"])
                check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bot_version_locale_details": bot_version_locale_details,
                "locale_id": locale_id,
            }

        @builtins.property
        def bot_version_locale_details(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotVersion.BotVersionLocaleDetailsProperty"]:
            '''The version of a bot used for a bot locale.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocalespecification.html#cfn-lex-botversion-botversionlocalespecification-botversionlocaledetails
            '''
            result = self._values.get("bot_version_locale_details")
            assert result is not None, "Required property 'bot_version_locale_details' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBotVersion.BotVersionLocaleDetailsProperty"], result)

        @builtins.property
        def locale_id(self) -> builtins.str:
            '''The identifier of the locale to add to the version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lex-botversion-botversionlocalespecification.html#cfn-lex-botversion-botversionlocalespecification-localeid
            '''
            result = self._values.get("locale_id")
            assert result is not None, "Required property 'locale_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BotVersionLocaleSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lex.CfnBotVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "bot_id": "botId",
        "bot_version_locale_specification": "botVersionLocaleSpecification",
        "description": "description",
    },
)
class CfnBotVersionProps:
    def __init__(
        self,
        *,
        bot_id: builtins.str,
        bot_version_locale_specification: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotVersion.BotVersionLocaleSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnBotVersion``.

        :param bot_id: The unique identifier of the bot.
        :param bot_version_locale_specification: Specifies the locales that Amazon Lex adds to this version. You can choose the Draft version or any other previously published version for each locale. When you specify a source version, the locale data is copied from the source version to the new version.
        :param description: The description of the version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_lex as lex
            
            cfn_bot_version_props = lex.CfnBotVersionProps(
                bot_id="botId",
                bot_version_locale_specification=[lex.CfnBotVersion.BotVersionLocaleSpecificationProperty(
                    bot_version_locale_details=lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
                        source_bot_version="sourceBotVersion"
                    ),
                    locale_id="localeId"
                )],
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c62e6b0e0243b1657500c6a68326c9f12a23962f7160ae47c6704be19aa731)
            check_type(argname="argument bot_id", value=bot_id, expected_type=type_hints["bot_id"])
            check_type(argname="argument bot_version_locale_specification", value=bot_version_locale_specification, expected_type=type_hints["bot_version_locale_specification"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bot_id": bot_id,
            "bot_version_locale_specification": bot_version_locale_specification,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def bot_id(self) -> builtins.str:
        '''The unique identifier of the bot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-botid
        '''
        result = self._values.get("bot_id")
        assert result is not None, "Required property 'bot_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bot_version_locale_specification(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBotVersion.BotVersionLocaleSpecificationProperty]]]:
        '''Specifies the locales that Amazon Lex adds to this version.

        You can choose the Draft version or any other previously published version for each locale. When you specify a source version, the locale data is copied from the source version to the new version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-botversionlocalespecification
        '''
        result = self._values.get("bot_version_locale_specification")
        assert result is not None, "Required property 'bot_version_locale_specification' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBotVersion.BotVersionLocaleSpecificationProperty]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-botversion.html#cfn-lex-botversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBotVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourcePolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-lex.CfnResourcePolicy",
):
    '''A CloudFormation ``AWS::Lex::ResourcePolicy``.

    .. epigraph::

       Amazon Lex V2 is the only supported version in AWS CloudFormation .

    Specifies a new resource policy with the specified policy statements.

    :cloudformationResource: AWS::Lex::ResourcePolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_lex as lex
        
        # policy: Any
        
        cfn_resource_policy = lex.CfnResourcePolicy(self, "MyCfnResourcePolicy",
            policy=policy,
            resource_arn="resourceArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        policy: typing.Any,
        resource_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Lex::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy: A resource policy to add to the resource. The policy is a JSON structure that contains one or more statements that define the policy. The policy must follow IAM syntax. If the policy isn't valid, Amazon Lex returns a validation exception.
        :param resource_arn: The Amazon Resource Name (ARN) of the bot or bot alias that the resource policy is attached to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee8e53e9980a7dc58a05c9d575bb6401fae4933c9ef930b1d62f1a6f6742bea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourcePolicyProps(policy=policy, resource_arn=resource_arn)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a283e8f845a7d80fc1d20252d58a6629c190830b7f02dbf2dd018fa5adbe72d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__adf92552aea03e9e5d8f4fc142e3f01fd3eb271ca5c4d08419e01653ba59e8ec)
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
        '''The identifier of the resource policy.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrRevisionId")
    def attr_revision_id(self) -> builtins.str:
        '''Specifies the current revision of a resource policy.

        :cloudformationAttribute: RevisionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRevisionId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        '''A resource policy to add to the resource.

        The policy is a JSON structure that contains one or more statements that define the policy. The policy must follow IAM syntax. If the policy isn't valid, Amazon Lex returns a validation exception.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html#cfn-lex-resourcepolicy-policy
        '''
        return typing.cast(typing.Any, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a1ad83f768ec4d11f3afa7fc52df277d9da788dedfb49223b0aa666d15d0cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the bot or bot alias that the resource policy is attached to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html#cfn-lex-resourcepolicy-resourcearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554386f2df50d52cde268d85cc95d769936c7b50a4fe5d43bf99b3122ff3b31a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-lex.CfnResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "resource_arn": "resourceArn"},
)
class CfnResourcePolicyProps:
    def __init__(self, *, policy: typing.Any, resource_arn: builtins.str) -> None:
        '''Properties for defining a ``CfnResourcePolicy``.

        :param policy: A resource policy to add to the resource. The policy is a JSON structure that contains one or more statements that define the policy. The policy must follow IAM syntax. If the policy isn't valid, Amazon Lex returns a validation exception.
        :param resource_arn: The Amazon Resource Name (ARN) of the bot or bot alias that the resource policy is attached to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_lex as lex
            
            # policy: Any
            
            cfn_resource_policy_props = lex.CfnResourcePolicyProps(
                policy=policy,
                resource_arn="resourceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc40aa0e9518ee80daac92fb58a14d51cec94485aa9db694c0ff404251ee9c1)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
            "resource_arn": resource_arn,
        }

    @builtins.property
    def policy(self) -> typing.Any:
        '''A resource policy to add to the resource.

        The policy is a JSON structure that contains one or more statements that define the policy. The policy must follow IAM syntax. If the policy isn't valid, Amazon Lex returns a validation exception.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html#cfn-lex-resourcepolicy-policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the bot or bot alias that the resource policy is attached to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lex-resourcepolicy.html#cfn-lex-resourcepolicy-resourcearn
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnBot",
    "CfnBotAlias",
    "CfnBotAliasProps",
    "CfnBotProps",
    "CfnBotVersion",
    "CfnBotVersionProps",
    "CfnResourcePolicy",
    "CfnResourcePolicyProps",
]

publication.publish()

def _typecheckingstub__c32b6ba3ac1a11f523aed5f511585db6c68f66ab488d13ff9f3b1bc0343ece29(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    data_privacy: typing.Any,
    idle_session_ttl_in_seconds: jsii.Number,
    name: builtins.str,
    role_arn: builtins.str,
    auto_build_bot_locales: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    bot_file_s3_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bot_locales: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.BotLocaleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    bot_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    test_bot_alias_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.TestBotAliasSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    test_bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b44e6f55c1aaee99c24639c213099abed1c7b704a641a541f2389206b4d3d3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7489eac65be2b6a4f6b60cc2d23e4020bb81c653e4e58dba47143f64169d4d42(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291daf3180cba7471a77ba47ca5526f76d5a822c77c6bae56a81cb20f791cca5(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19fcce7464c109d027ceae526882382993870083562b90a6141a2ae436a3342(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6ae8fbab2b0706d58b4bf9de2e780913a84dd1b83350ca240fa0ac6b1fed03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa106447fbd5f28c2a8191871ce76e3723a1f4afe8173e6c9cb4650cb18554e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f293142c9e68ba1b9f6235a9eef8f0ee35368682cc04e5b506d970d4370b90(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362bfaf577ca696673ce60d5989301ba1e228a4483e8ef08bb5b78da418898f5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBot.S3LocationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b917a2f613fe9b4a599279d725f726837b1659e25847d4170d03f9b499976d(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBot.BotLocaleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8732ebd90cc3092165edf7b3b336ce71cd94af1dac75b9d3c49317796e8c35(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36dd3001a021a12cb0baf96ff20897eff6402523f5390ef16db0498805a78917(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0486714edae70bd4cf7e2f138408212a8a7a3ed8c7703d5dbb06e7495c3254a5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBot.TestBotAliasSettingsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a878428d06d0371f39dac4b3340f1aba7fb3e1f726d4e7b74fc9ba5cff5093(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18434d84262bd1b58a1e22a7ee7af3f5bde045708f19369d9cb2d77a669f4ca(
    *,
    audio_recognition_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81adb7683e742175fc26c6909829061374e32cd0ffca6a1498fdf1ec2679d53b(
    *,
    allow_audio_input: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    allow_dtmf_input: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172847647b14e44f8713aab62364b1fb02bf11ca42de2d2202906964a14389f3(
    *,
    start_timeout_ms: jsii.Number,
    audio_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.AudioSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dtmf_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.DTMFSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd16255160f7020b858d622bde765d4d99dbbef63f0e46d978da9697782fde15(
    *,
    s3_bucket: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.S3BucketLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012e5b81ba543678c2746364b2307194ee37ec7d0469da50bef4f95cfc3a087e(
    *,
    destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.AudioLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd5779b162d84386570c114b99f0561c027760c1f39856a6e320bfcbe356569(
    *,
    end_timeout_ms: jsii.Number,
    max_length_ms: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf654f112e0ec8396c9ff8eb83dc7e4bde049f41919e0f85aed475d81029485(
    *,
    bot_alias_locale_setting: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.BotAliasLocaleSettingsProperty, typing.Dict[builtins.str, typing.Any]]],
    locale_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9aba6c3be74203c6592e57e7ea556c6428e5be7b09bd85b32211ec142bbb2e(
    *,
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    code_hook_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.CodeHookSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a82cce828e0d9278905a24c9a75cf3e90c46735547a8a8dd170d77fb8b24dc(
    *,
    locale_id: builtins.str,
    nlu_confidence_threshold: jsii.Number,
    custom_vocabulary: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.CustomVocabularyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    intents: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.IntentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    slot_types: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SlotTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    voice_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.VoiceSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07b0e828670df93418cdfd89bf0925e98396b9ebab2dc888ab2f620545f6269(
    *,
    text: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806f4b049b50e6479a3b78ea5e58b022bc96989949b937c40e2470f9da95fff4(
    *,
    cloud_watch_log_group_arn: builtins.str,
    log_prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6f628e13f551982d33a31b7c68467c2e75d803b98bb7bbe438f0d221d19feb(
    *,
    lambda_code_hook: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.LambdaCodeHookProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32014d318a463d84d2ee90b10658989e7745be06c4a07c49052abde4628a8ade(
    *,
    audio_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.AudioLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    text_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.TextLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c211a101090e012075cd5d7de400caf8737378224339c466fc9c98f1c66d972(
    *,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46661b9ee8bacad87c11f515448797784114d8fdfb04e124aa3c7a0cfe232a3(
    *,
    phrase: builtins.str,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71081a5a4f02cf15b2b9585786d6b5e59f91107b18d6dc2d0f807a12251a9a35(
    *,
    custom_vocabulary_items: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.CustomVocabularyItemProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb971d2a02e83430a9bfb5997fb6398deb433696e160a3d596545bf7b2f93ed(
    *,
    deletion_character: builtins.str,
    end_character: builtins.str,
    end_timeout_ms: jsii.Number,
    max_length: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2d76be0ab1d7bef5b2db6f6b7068e3739548eec497c49a26dd5bd2f3955b25(
    *,
    child_directed: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db6c1b57aa2e6666240e75ea9ff22c796a6d1dcd210a5da32a2412b0d9c6d6b(
    *,
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048a8708754b33da941ab48ab56d391c82ce3900f3f968f262b5d4674d4ac1df(
    *,
    grammar_slot_type_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.GrammarSlotTypeSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1af8baef81c0c61a62456ee7bf924fafe3aea02e2719fdda3fdc4618d4336ab(
    *,
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    fulfillment_updates_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.FulfillmentUpdatesSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    post_fulfillment_status_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.PostFulfillmentStatusSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c837c09978e60daf7cbb23a64f674b8400d6cf47a63a3f86f5e0505b25e1d7(
    *,
    delay_in_seconds: jsii.Number,
    message_groups: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.MessageGroupProperty, typing.Dict[builtins.str, typing.Any]]]]],
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e487335482a27d40419de8fafb4e65ca6ec2162d42335b306f9bc03a11781d9b(
    *,
    frequency_in_seconds: jsii.Number,
    message_groups: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.MessageGroupProperty, typing.Dict[builtins.str, typing.Any]]]]],
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39910e837bc526af16f790a41689555e6b51358c1ab7bcce794884105453298f(
    *,
    active: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    start_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.FulfillmentStartResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
    update_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.FulfillmentUpdateResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210e6a6be1d893b8ccec42063ee2fe87b51c9b808e6cb0989d0d1f35d11766a3(
    *,
    source: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.GrammarSlotTypeSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20ef2820e59b1dd5b1476f1bd0d744e9a1d190fa43c225298a906e7b8a9a959(
    *,
    s3_bucket_name: builtins.str,
    s3_object_key: builtins.str,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7ecf08a64930d06e6b17db57f7c8a056f6d3c9cb420c75ed1e4332b229e6a0(
    *,
    title: builtins.str,
    buttons: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ButtonProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    image_url: typing.Optional[builtins.str] = None,
    subtitle: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463a1f987a2cb01a67601736d8400c21d1b87c7cf7b0b1ad813834354595ef1c(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a50abb93edc02417385fd143fcebc88e655c5bc38c884a5f11a6f611eed6c6(
    *,
    closing_response: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]],
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6755d2bd884e0fe8ebf89d12d66f855302dbed5688f50bf3fb7cdd04643880d8(
    *,
    declination_response: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]],
    prompt_specification: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.PromptSpecificationProperty, typing.Dict[builtins.str, typing.Any]]],
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323e343dae13e36ad470edd5cb08b6c34db83ca1b509e8d1f5ae76058728fbeb(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dialog_code_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.DialogCodeHookSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fulfillment_code_hook: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.FulfillmentCodeHookSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_contexts: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.InputContextProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    intent_closing_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.IntentClosingSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    intent_confirmation_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.IntentConfirmationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kendra_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.KendraConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    output_contexts: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.OutputContextProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    parent_intent_signature: typing.Optional[builtins.str] = None,
    sample_utterances: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SampleUtteranceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    slot_priorities: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SlotPriorityProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    slots: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SlotProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bb9f546d3f89e926d37429c339515442456de4678657645fd465fdc193aae3(
    *,
    kendra_index: builtins.str,
    query_filter_string: typing.Optional[builtins.str] = None,
    query_filter_string_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000a905b020cf2b73e24d3ce2f15b78ddf65fc4c3f883e0fd9ba73fe153f36a9(
    *,
    code_hook_interface_version: builtins.str,
    lambda_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f95db70ba8a36be1eec43206a32e3ea68be1689c4756d582cf22679de6ff863(
    *,
    message: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.MessageProperty, typing.Dict[builtins.str, typing.Any]]],
    variations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.MessageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7ab5ddf974fb59d9017c31c8f2018dd1e12468a8b5ee92f260d8ec1621851f(
    *,
    custom_payload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.CustomPayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_response_card: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ImageResponseCardProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    plain_text_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.PlainTextMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ssml_message: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SSMLMessageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c771393a27a87b6bd46f3d359d46aa9447806395f53579df43f80026572a31e1(
    *,
    allow_multiple_values: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60cac8372bdfa58ca9cee001e189769e2a8a9a8c9da8835a54a74b3b46bc5ec(
    *,
    obfuscation_setting_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b5b676c6dabe13350db59e9f7e51478941f30d05041fd99417e62906752cd7(
    *,
    name: builtins.str,
    time_to_live_in_seconds: jsii.Number,
    turns_to_live: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e680d14ee0a7e5202804ede7b01950de731f2c5c28cc2632097099da0bc1c3(
    *,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1659ee605a6824ee30f43883012b75bb7ae3c3de400a9eafdd793212d1af1d(
    *,
    failure_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    success_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359a7367f79da136d347ddf064d4ebb249581165ac501e3e8d2c59a19b571fe5(
    *,
    allowed_input_types: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.AllowedInputTypesProperty, typing.Dict[builtins.str, typing.Any]]],
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    audio_and_dtmf_input_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.AudioAndDTMFInputSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    text_input_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.TextInputSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f8efcdf1548108a5d48068e158dddccfb29c7582216e817704419e06919d36(
    *,
    max_retries: jsii.Number,
    message_groups_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.MessageGroupProperty, typing.Dict[builtins.str, typing.Any]]]]],
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    message_selection_strategy: typing.Optional[builtins.str] = None,
    prompt_attempts_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.PromptAttemptSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699fafdacbc9aa632e7b1f4ffe86e05ca8eb3e58c9cc72dbc0705729aeda62c6(
    *,
    message_groups_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.MessageGroupProperty, typing.Dict[builtins.str, typing.Any]]]]],
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3479e44c0bcb1c87d470fa61abd620d0e0387132f98211932223efba7b7c5ab(
    *,
    log_prefix: builtins.str,
    s3_bucket_arn: builtins.str,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e309a4fbe8ba1fe62b123c8133503d4487d6db66620a6029709ba9e917026a(
    *,
    s3_bucket: builtins.str,
    s3_object_key: builtins.str,
    s3_object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0bf7c70df8ed3eb667fbef1a57a18d58f9c085fc3c771aacf224ebf55de8a0d(
    *,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba40fa24c702dc2756fab3dbd3ff60161663576ce120a3d60ee583755835a92(
    *,
    utterance: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29ca9634d0fba49b3d706d05f7f5dc1da6a6cd71b41f9bebb3d17d49ebd3936(
    *,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5fd083508d7a130d114e33b83c17957de66b4dfe31a69065e9d758e238386a(
    *,
    detect_sentiment: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa56f0d00799161e87d8aec1213e5553a2f40edf609f138a8b864cd28c43426b(
    *,
    default_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e189c45ab6d5b9447ee84586c81875fecad4babd9223fae30e1abb06bff1b598(
    *,
    default_value_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SlotDefaultValueProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707e6cbad7e1fbee236c253f4f778fef89535083113e5959410e50559cd1bbc1(
    *,
    priority: jsii.Number,
    slot_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ac62926bbc5f616f5f16264c0595ef4e53f02fb6d3b319b0a18e74276e1bb0(
    *,
    name: builtins.str,
    slot_type_name: builtins.str,
    value_elicitation_setting: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SlotValueElicitationSettingProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    multiple_values_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.MultipleValuesSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    obfuscation_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ObfuscationSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6e0399df24b43356318fd6410381e90f6a85d1abcd14000e703c32666ce438(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    external_source_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ExternalSourceSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parent_slot_type_signature: typing.Optional[builtins.str] = None,
    slot_type_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SlotTypeValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    value_selection_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SlotValueSelectionSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4dc872c6cba621347da84b298c11fd0884a45256e4915a27358d6664ff8d133(
    *,
    sample_value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SampleValueProperty, typing.Dict[builtins.str, typing.Any]]],
    synonyms: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SampleValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c40ccae0d979b7a128738e3d610d639edab8f4be1e943016dba9869717c7d4b(
    *,
    slot_constraint: builtins.str,
    default_value_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SlotDefaultValueSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    prompt_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.PromptSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sample_utterances: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SampleUtteranceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    wait_and_continue_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.WaitAndContinueSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67fab4304a23c2bbd1994182d3cf16d0945b18df30ed134f65d24bea681af81f(
    *,
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eee2760a0801a269c2ec5536aecd31c74000f7bf9e7473cfde846a6d984288d(
    *,
    resolution_strategy: builtins.str,
    advanced_recognition_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.AdvancedRecognitionSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex_filter: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.SlotValueRegexFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567e84456959430c5fe2d7e19b42583201d32d57dbb79a2795c9a32184653266(
    *,
    frequency_in_seconds: jsii.Number,
    message_groups_list: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.MessageGroupProperty, typing.Dict[builtins.str, typing.Any]]]]],
    timeout_in_seconds: jsii.Number,
    allow_interrupt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a60c523d94c3dca9c2df881d69c88595b8a14785ac5338fa1041ebe1533a13(
    *,
    bot_alias_locale_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.BotAliasLocaleSettingsItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    conversation_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ConversationLogSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    sentiment_analysis_settings: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71608311423e59136a3e245126810e3b1a13181612dcd7e05e02d448e3bb5e0f(
    *,
    start_timeout_ms: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a379ed9320c9fe288b5093153410193c754ff48b97cb1a09b61be67689ad7a(
    *,
    cloud_watch: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.CloudWatchLogGroupLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bcd1e1abfed5de661ebe45b8f53167deb593668eab80d13e2dbbf0155ea8fe(
    *,
    destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.TextLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c549feb2fc08a186faf4edc6a402f03bc1c59e9aec68cb8520c1afd620e1a7d0(
    *,
    voice_id: builtins.str,
    engine: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7ec7b22e666eb8c70be5be80fa6076961a5f2ed9849d555a9d1a08259844e4(
    *,
    continue_response: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]],
    waiting_response: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.ResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]],
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    still_waiting_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.StillWaitingResponseSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0033e2634011545e69f53ada3f71b58664bbeb1b40a6cca16ce404405bcc3ff1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    bot_alias_name: builtins.str,
    bot_id: builtins.str,
    bot_alias_locale_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.BotAliasLocaleSettingsItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    bot_version: typing.Optional[builtins.str] = None,
    conversation_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.ConversationLogSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    sentiment_analysis_settings: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc1eaed3ce5db99103e345e12d309a2a02059bb60b71355abf6f697e4553d51(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48d939273237c40735642989bc712dd0b539da4023ab572aba709f4a771a0e0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8dde915fc75ffc7d4697b07dffcb4b239dc4531f2fccd15afe26b2158e2afa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3e24b6650d6fcb50149c6f6df36bfb474f1a6c2980fcc21166ddbe0073de9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61fd1202f74cf30d72b3387352924f892e9bf5d3464afdcb8e0d444b26295d8(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27474b9d6c34036b5571fb162fc3a8c6d9426d1a9ff61cc2d5c7e8b7e913011d(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBotAlias.BotAliasLocaleSettingsItemProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c164f243d308ca08ecde6e510310a184a9be9d3c1f2f0088a7e999366196c4(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, _aws_cdk_core_f4b25747.CfnTag]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7febd15589f42cb13b75018bcee8db1da5abfd57bef44a72d7712bcb1da67e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1a02483838d91292dd9d3f0fda2045c37d1de6220332da8d7419713ab43fc2(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBotAlias.ConversationLogSettingsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bfc0faebc08882643ccece7eacf0512c38e153592ddd2392078878667b0873(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568fc581a6e0457256b8069638a785fd15d4d221d0746265a7100adedd103cf4(
    *,
    s3_bucket: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.S3BucketLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783da7d4119a2964ce0db3f3a3099ed7f2fd088e1ff8dff309da69d1c6fc6b3a(
    *,
    destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.AudioLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c5abc23eca6282da359d7d4be5f597be13310d0b8c57d6566820705406f05f(
    *,
    bot_alias_locale_setting: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.BotAliasLocaleSettingsProperty, typing.Dict[builtins.str, typing.Any]]],
    locale_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40085ffc9108ae82c7ae5e17c5d82b02fc11cd773d07e89dff0d2aa75dfd317e(
    *,
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    code_hook_specification: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.CodeHookSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754f0770ab676e34d247fa73b12a17b618cf7573974b82d351acad9de2365aa2(
    *,
    cloud_watch_log_group_arn: builtins.str,
    log_prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6d59dfed10bb26471bb81404e9d5e62c76f020be70677485324be1fe8e9b47(
    *,
    lambda_code_hook: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.LambdaCodeHookProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9008770d1e2263d944a42ccbf2c31e579fca9d57771ff50ed942ce39c838ffa(
    *,
    audio_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.AudioLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    text_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.TextLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342e895735070ce357a0a7bc974669e8506976ff219537978aa4b8dd9b9371da(
    *,
    code_hook_interface_version: builtins.str,
    lambda_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ca74f2a19b0f31eb902f1c7c6a16b3907fef563719315b9e6dd564ce7963ee(
    *,
    log_prefix: builtins.str,
    s3_bucket_arn: builtins.str,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1736ef08399f48feb86180360bfffdad3ba7b4cacf8e7f550fe8524849e1eb(
    *,
    detect_sentiment: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8cc7b91ff6f3795fc4fccedb4e3f614d0977c93983fea7e2f6ac0c42cb17529(
    *,
    cloud_watch: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.CloudWatchLogGroupLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bd24ed340a979f0f5f7ce981be7b6841fce6c3c333e8ce6d112a3af8aeec5d(
    *,
    destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.TextLogDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fcb128b628f95e893ab0bc6c0d720a0e70d788682e6a9f9e6c8ed6b019135a7(
    *,
    bot_alias_name: builtins.str,
    bot_id: builtins.str,
    bot_alias_locale_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.BotAliasLocaleSettingsItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    bot_version: typing.Optional[builtins.str] = None,
    conversation_log_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotAlias.ConversationLogSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    sentiment_analysis_settings: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be4e658521508c907a690800c0a3f0a926558d7dd2ee7093d2fe01938f7b0ed(
    *,
    data_privacy: typing.Any,
    idle_session_ttl_in_seconds: jsii.Number,
    name: builtins.str,
    role_arn: builtins.str,
    auto_build_bot_locales: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    bot_file_s3_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bot_locales: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.BotLocaleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    bot_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    test_bot_alias_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBot.TestBotAliasSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    test_bot_alias_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1934dc39f98d55c070d52078083145d29a33bb2fe35b0f4acde668a01f2c33b2(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    bot_id: builtins.str,
    bot_version_locale_specification: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotVersion.BotVersionLocaleSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6625f4fcb54267efbeb6c4db940a3f001ad4b1f0bae2aeac4a501095f706c38(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798d43461bb19174849f5fba35f737b5b792ddb51727ee6cc3a992d6d3822f12(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02571acc0fb69d81968876064577b6db79c1133f325d528d26171d2e66f7d5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99646775afda16766820f18de65ac94bd38dd1a4e93ba05d173b84d5180762e9(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBotVersion.BotVersionLocaleSpecificationProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf35d04dc8ee6312e2cb00d3b2f180d838e5cc8e39a1387fdc8a1f0ae1ac53c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d372396ab35154b85f98ee9b374cd281ae55e673243467be1d555a4ccef696(
    *,
    source_bot_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b2123fe95f8731f187cf2a68d53d5ce8e5865d0cc09b9b5e24613227546c54(
    *,
    bot_version_locale_details: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotVersion.BotVersionLocaleDetailsProperty, typing.Dict[builtins.str, typing.Any]]],
    locale_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c62e6b0e0243b1657500c6a68326c9f12a23962f7160ae47c6704be19aa731(
    *,
    bot_id: builtins.str,
    bot_version_locale_specification: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBotVersion.BotVersionLocaleSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee8e53e9980a7dc58a05c9d575bb6401fae4933c9ef930b1d62f1a6f6742bea(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    policy: typing.Any,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a283e8f845a7d80fc1d20252d58a6629c190830b7f02dbf2dd018fa5adbe72d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf92552aea03e9e5d8f4fc142e3f01fd3eb271ca5c4d08419e01653ba59e8ec(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a1ad83f768ec4d11f3afa7fc52df277d9da788dedfb49223b0aa666d15d0cf(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554386f2df50d52cde268d85cc95d769936c7b50a4fe5d43bf99b3122ff3b31a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc40aa0e9518ee80daac92fb58a14d51cec94485aa9db694c0ff404251ee9c1(
    *,
    policy: typing.Any,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
