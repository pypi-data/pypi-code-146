'''
# AWS Data Pipeline Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_datapipeline as datapipeline
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for DataPipeline construct libraries](https://constructs.dev/search?q=datapipeline)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::DataPipeline resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataPipeline.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::DataPipeline](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataPipeline.html).

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
class CfnPipeline(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline",
):
    '''A CloudFormation ``AWS::DataPipeline::Pipeline``.

    The AWS::DataPipeline::Pipeline resource specifies a data pipeline that you can use to automate the movement and transformation of data. In each pipeline, you define pipeline objects, such as activities, schedules, data nodes, and resources. For information about pipeline objects and components that you can use, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* .

    The ``AWS::DataPipeline::Pipeline`` resource adds tasks, schedules, and preconditions to the specified pipeline. You can use ``PutPipelineDefinition`` to populate a new pipeline.

    ``PutPipelineDefinition`` also validates the configuration as it adds it to the pipeline. Changes to the pipeline are saved unless one of the following validation errors exist in the pipeline.

    - An object is missing a name or identifier field.
    - A string or reference field is empty.
    - The number of objects in the pipeline exceeds the allowed maximum number of objects.
    - The pipeline is in a FINISHED state.

    Pipeline object definitions are passed to the `PutPipelineDefinition <https://docs.aws.amazon.com/datapipeline/latest/APIReference/API_PutPipelineDefinition.html>`_ action and returned by the `GetPipelineDefinition <https://docs.aws.amazon.com/datapipeline/latest/APIReference/API_GetPipelineDefinition.html>`_ action.

    :cloudformationResource: AWS::DataPipeline::Pipeline
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datapipeline as datapipeline
        
        cfn_pipeline = datapipeline.CfnPipeline(self, "MyCfnPipeline",
            name="name",
        
            # the properties below are optional
            activate=False,
            description="description",
            parameter_objects=[datapipeline.CfnPipeline.ParameterObjectProperty(
                attributes=[datapipeline.CfnPipeline.ParameterAttributeProperty(
                    key="key",
                    string_value="stringValue"
                )],
                id="id"
            )],
            parameter_values=[datapipeline.CfnPipeline.ParameterValueProperty(
                id="id",
                string_value="stringValue"
            )],
            pipeline_objects=[datapipeline.CfnPipeline.PipelineObjectProperty(
                fields=[datapipeline.CfnPipeline.FieldProperty(
                    key="key",
        
                    # the properties below are optional
                    ref_value="refValue",
                    string_value="stringValue"
                )],
                id="id",
                name="name"
            )],
            pipeline_tags=[datapipeline.CfnPipeline.PipelineTagProperty(
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
        name: builtins.str,
        activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_objects: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPipeline.ParameterObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        parameter_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPipeline.ParameterValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        pipeline_objects: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPipeline.PipelineObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        pipeline_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPipeline.PipelineTagProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataPipeline::Pipeline``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the pipeline.
        :param activate: Indicates whether to validate and start the pipeline or stop an active pipeline. By default, the value is set to ``true`` .
        :param description: A description of the pipeline.
        :param parameter_objects: The parameter objects used with the pipeline.
        :param parameter_values: The parameter values used with the pipeline.
        :param pipeline_objects: The objects that define the pipeline. These objects overwrite the existing pipeline definition. Not all objects, fields, and values can be updated. For information about restrictions, see `Editing Your Pipeline <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-manage-pipeline-modify-console.html>`_ in the *AWS Data Pipeline Developer Guide* .
        :param pipeline_tags: A list of arbitrary tags (key-value pairs) to associate with the pipeline, which you can use to control permissions. For more information, see `Controlling Access to Pipelines and Resources <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-control-access.html>`_ in the *AWS Data Pipeline Developer Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a259d35408fa1ef72af1c8b5e4ffdb2ed913379c7f39465eaa3a5a33c213f3b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPipelineProps(
            name=name,
            activate=activate,
            description=description,
            parameter_objects=parameter_objects,
            parameter_values=parameter_values,
            pipeline_objects=pipeline_objects,
            pipeline_tags=pipeline_tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402e2e3e29a1850e62e49c2816567049c4775858393ebf60b9f433f80c9ff6f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84e2d8a2f1638a4983e0fb83bb3f24da3a550d2a3a79f41449797ecb46b1e95e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrPipelineId")
    def attr_pipeline_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: PipelineId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPipelineId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the pipeline.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a46f70a9174c4fdca6b612cf3a4d77ecfdf17670d4450724c22b315a2fa612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="activate")
    def activate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether to validate and start the pipeline or stop an active pipeline.

        By default, the value is set to ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-activate
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "activate"))

    @activate.setter
    def activate(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bceea8c6f61bdc5056addd76b5b58c81a90de623381163c3be2565ff702afc1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activate", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the pipeline.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b10c7ddd3be0326cea9aa091123a30602516fc94a0a23c687b5803f07ffae00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="parameterObjects")
    def parameter_objects(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.ParameterObjectProperty"]]]]:
        '''The parameter objects used with the pipeline.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parameterobjects
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.ParameterObjectProperty"]]]], jsii.get(self, "parameterObjects"))

    @parameter_objects.setter
    def parameter_objects(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.ParameterObjectProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297709dcf01039ea59b47821d8538e7f180a654b8bace2424de2523db1ad2eb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterObjects", value)

    @builtins.property
    @jsii.member(jsii_name="parameterValues")
    def parameter_values(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.ParameterValueProperty"]]]]:
        '''The parameter values used with the pipeline.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parametervalues
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.ParameterValueProperty"]]]], jsii.get(self, "parameterValues"))

    @parameter_values.setter
    def parameter_values(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.ParameterValueProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5a19b6d13fb1b12d1a9fcb5a22b7343809dfe62ea31cdb223817d29a2df235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterValues", value)

    @builtins.property
    @jsii.member(jsii_name="pipelineObjects")
    def pipeline_objects(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.PipelineObjectProperty"]]]]:
        '''The objects that define the pipeline.

        These objects overwrite the existing pipeline definition. Not all objects, fields, and values can be updated. For information about restrictions, see `Editing Your Pipeline <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-manage-pipeline-modify-console.html>`_ in the *AWS Data Pipeline Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelineobjects
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.PipelineObjectProperty"]]]], jsii.get(self, "pipelineObjects"))

    @pipeline_objects.setter
    def pipeline_objects(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.PipelineObjectProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65a887274196f67182384490490bf9bc45bcecfcf4eece856427005b058f230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineObjects", value)

    @builtins.property
    @jsii.member(jsii_name="pipelineTags")
    def pipeline_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.PipelineTagProperty"]]]]:
        '''A list of arbitrary tags (key-value pairs) to associate with the pipeline, which you can use to control permissions.

        For more information, see `Controlling Access to Pipelines and Resources <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-control-access.html>`_ in the *AWS Data Pipeline Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelinetags
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.PipelineTagProperty"]]]], jsii.get(self, "pipelineTags"))

    @pipeline_tags.setter
    def pipeline_tags(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.PipelineTagProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4ac4602c2cbed6d09d5ec7388cf4b49c76fcecf379ae549bf78933f6d2fd7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineTags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.FieldProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "ref_value": "refValue",
            "string_value": "stringValue",
        },
    )
    class FieldProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            ref_value: typing.Optional[builtins.str] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A key-value pair that describes a property of a ``PipelineObject`` .

            The value is specified as either a string value ( ``StringValue`` ) or a reference to another object ( ``RefValue`` ) but not as both. To view fields for a data pipeline object, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* .

            :param key: Specifies the name of a field for a particular object. To view valid values for a particular field, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* .
            :param ref_value: A field value that you specify as an identifier of another object in the same pipeline definition. .. epigraph:: You can specify the field value as either a string value ( ``StringValue`` ) or a reference to another object ( ``RefValue`` ), but not both. Required if the key that you are using requires it.
            :param string_value: A field value that you specify as a string. To view valid values for a particular field, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* . .. epigraph:: You can specify the field value as either a string value ( ``StringValue`` ) or a reference to another object ( ``RefValue`` ), but not both. Required if the key that you are using requires it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-field.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datapipeline as datapipeline
                
                field_property = datapipeline.CfnPipeline.FieldProperty(
                    key="key",
                
                    # the properties below are optional
                    ref_value="refValue",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__81419d6ba902e15556c4eff1db6801701ed0bc6389394a578d614cd7528ddc36)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument ref_value", value=ref_value, expected_type=type_hints["ref_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
            }
            if ref_value is not None:
                self._values["ref_value"] = ref_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def key(self) -> builtins.str:
            '''Specifies the name of a field for a particular object.

            To view valid values for a particular field, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-field.html#cfn-datapipeline-pipeline-field-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def ref_value(self) -> typing.Optional[builtins.str]:
            '''A field value that you specify as an identifier of another object in the same pipeline definition.

            .. epigraph::

               You can specify the field value as either a string value ( ``StringValue`` ) or a reference to another object ( ``RefValue`` ), but not both.

            Required if the key that you are using requires it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-field.html#cfn-datapipeline-pipeline-field-refvalue
            '''
            result = self._values.get("ref_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A field value that you specify as a string.

            To view valid values for a particular field, see `Pipeline Object Reference <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-pipeline-objects.html>`_ in the *AWS Data Pipeline Developer Guide* .
            .. epigraph::

               You can specify the field value as either a string value ( ``StringValue`` ) or a reference to another object ( ``RefValue`` ), but not both.

            Required if the key that you are using requires it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-field.html#cfn-datapipeline-pipeline-field-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.ParameterAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "string_value": "stringValue"},
    )
    class ParameterAttributeProperty:
        def __init__(self, *, key: builtins.str, string_value: builtins.str) -> None:
            '''``Attribute`` is a property of ``ParameterObject`` that defines the attributes of a parameter object as key-value pairs.

            :param key: The field identifier.
            :param string_value: The field value, expressed as a String.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datapipeline as datapipeline
                
                parameter_attribute_property = datapipeline.CfnPipeline.ParameterAttributeProperty(
                    key="key",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18166f4891901bb3befe7811bf3ccf42446aedd01287394261368496247acc5d)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "string_value": string_value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The field identifier.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterattribute.html#cfn-datapipeline-pipeline-parameterattribute-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def string_value(self) -> builtins.str:
            '''The field value, expressed as a String.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterattribute.html#cfn-datapipeline-pipeline-parameterattribute-stringvalue
            '''
            result = self._values.get("string_value")
            assert result is not None, "Required property 'string_value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.ParameterObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "id": "id"},
    )
    class ParameterObjectProperty:
        def __init__(
            self,
            *,
            attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPipeline.ParameterAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]],
            id: builtins.str,
        ) -> None:
            '''Contains information about a parameter object.

            :param attributes: The attributes of the parameter object.
            :param id: The ID of the parameter object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datapipeline as datapipeline
                
                parameter_object_property = datapipeline.CfnPipeline.ParameterObjectProperty(
                    attributes=[datapipeline.CfnPipeline.ParameterAttributeProperty(
                        key="key",
                        string_value="stringValue"
                    )],
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a19dbbf590422eab0eb80b72712c4c55d48789d8588bc65dc8e029e47d05237)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "attributes": attributes,
                "id": id,
            }

        @builtins.property
        def attributes(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.ParameterAttributeProperty"]]]:
            '''The attributes of the parameter object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobject.html#cfn-datapipeline-pipeline-parameterobject-attributes
            '''
            result = self._values.get("attributes")
            assert result is not None, "Required property 'attributes' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.ParameterAttributeProperty"]]], result)

        @builtins.property
        def id(self) -> builtins.str:
            '''The ID of the parameter object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parameterobject.html#cfn-datapipeline-pipeline-parameterobject-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.ParameterValueProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "string_value": "stringValue"},
    )
    class ParameterValueProperty:
        def __init__(self, *, id: builtins.str, string_value: builtins.str) -> None:
            '''A value or list of parameter values.

            :param id: The ID of the parameter value.
            :param string_value: The field value, expressed as a String.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datapipeline as datapipeline
                
                parameter_value_property = datapipeline.CfnPipeline.ParameterValueProperty(
                    id="id",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c50c169957f80f6242ed12feb7348ced9130e0179fcebba1e3be7c9ddddfcd88)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "string_value": string_value,
            }

        @builtins.property
        def id(self) -> builtins.str:
            '''The ID of the parameter value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalue.html#cfn-datapipeline-pipeline-parametervalue-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def string_value(self) -> builtins.str:
            '''The field value, expressed as a String.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-parametervalue.html#cfn-datapipeline-pipeline-parametervalue-stringvalue
            '''
            result = self._values.get("string_value")
            assert result is not None, "Required property 'string_value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.PipelineObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"fields": "fields", "id": "id", "name": "name"},
    )
    class PipelineObjectProperty:
        def __init__(
            self,
            *,
            fields: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPipeline.FieldProperty", typing.Dict[builtins.str, typing.Any]]]]],
            id: builtins.str,
            name: builtins.str,
        ) -> None:
            '''PipelineObject is property of the AWS::DataPipeline::Pipeline resource that contains information about a pipeline object.

            This can be a logical, physical, or physical attempt pipeline object. The complete set of components of a pipeline defines the pipeline.

            :param fields: Key-value pairs that define the properties of the object.
            :param id: The ID of the object.
            :param name: The name of the object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datapipeline as datapipeline
                
                pipeline_object_property = datapipeline.CfnPipeline.PipelineObjectProperty(
                    fields=[datapipeline.CfnPipeline.FieldProperty(
                        key="key",
                
                        # the properties below are optional
                        ref_value="refValue",
                        string_value="stringValue"
                    )],
                    id="id",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83b227f2f033c7f2dcd2cf08b42858b67f1566f3d549e39a149bc2a190ef88ad)
                check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "fields": fields,
                "id": id,
                "name": name,
            }

        @builtins.property
        def fields(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.FieldProperty"]]]:
            '''Key-value pairs that define the properties of the object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobject.html#cfn-datapipeline-pipeline-pipelineobject-fields
            '''
            result = self._values.get("fields")
            assert result is not None, "Required property 'fields' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPipeline.FieldProperty"]]], result)

        @builtins.property
        def id(self) -> builtins.str:
            '''The ID of the object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobject.html#cfn-datapipeline-pipeline-pipelineobject-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelineobject.html#cfn-datapipeline-pipeline-pipelineobject-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipelineObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datapipeline.CfnPipeline.PipelineTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class PipelineTagProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''A list of arbitrary tags (key-value pairs) to associate with the pipeline, which you can use to control permissions.

            For more information, see `Controlling Access to Pipelines and Resources <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-control-access.html>`_ in the *AWS Data Pipeline Developer Guide* .

            :param key: The key name of a tag.
            :param value: The value to associate with the key name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datapipeline as datapipeline
                
                pipeline_tag_property = datapipeline.CfnPipeline.PipelineTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3f61225f0839c3b4d3777bf71e2b8b911152c5699298d97c42668f6f6467967)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The key name of a tag.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetag.html#cfn-datapipeline-pipeline-pipelinetag-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The value to associate with the key name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datapipeline-pipeline-pipelinetag.html#cfn-datapipeline-pipeline-pipelinetag-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipelineTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datapipeline.CfnPipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "activate": "activate",
        "description": "description",
        "parameter_objects": "parameterObjects",
        "parameter_values": "parameterValues",
        "pipeline_objects": "pipelineObjects",
        "pipeline_tags": "pipelineTags",
    },
)
class CfnPipelineProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_objects: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.ParameterObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        parameter_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.ParameterValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        pipeline_objects: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.PipelineObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        pipeline_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.PipelineTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPipeline``.

        :param name: The name of the pipeline.
        :param activate: Indicates whether to validate and start the pipeline or stop an active pipeline. By default, the value is set to ``true`` .
        :param description: A description of the pipeline.
        :param parameter_objects: The parameter objects used with the pipeline.
        :param parameter_values: The parameter values used with the pipeline.
        :param pipeline_objects: The objects that define the pipeline. These objects overwrite the existing pipeline definition. Not all objects, fields, and values can be updated. For information about restrictions, see `Editing Your Pipeline <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-manage-pipeline-modify-console.html>`_ in the *AWS Data Pipeline Developer Guide* .
        :param pipeline_tags: A list of arbitrary tags (key-value pairs) to associate with the pipeline, which you can use to control permissions. For more information, see `Controlling Access to Pipelines and Resources <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-control-access.html>`_ in the *AWS Data Pipeline Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datapipeline as datapipeline
            
            cfn_pipeline_props = datapipeline.CfnPipelineProps(
                name="name",
            
                # the properties below are optional
                activate=False,
                description="description",
                parameter_objects=[datapipeline.CfnPipeline.ParameterObjectProperty(
                    attributes=[datapipeline.CfnPipeline.ParameterAttributeProperty(
                        key="key",
                        string_value="stringValue"
                    )],
                    id="id"
                )],
                parameter_values=[datapipeline.CfnPipeline.ParameterValueProperty(
                    id="id",
                    string_value="stringValue"
                )],
                pipeline_objects=[datapipeline.CfnPipeline.PipelineObjectProperty(
                    fields=[datapipeline.CfnPipeline.FieldProperty(
                        key="key",
            
                        # the properties below are optional
                        ref_value="refValue",
                        string_value="stringValue"
                    )],
                    id="id",
                    name="name"
                )],
                pipeline_tags=[datapipeline.CfnPipeline.PipelineTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640b8a6d6bd2d8badf454d3e170ecaedc30a638ebdc5df14138d4721bdf1604b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument activate", value=activate, expected_type=type_hints["activate"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameter_objects", value=parameter_objects, expected_type=type_hints["parameter_objects"])
            check_type(argname="argument parameter_values", value=parameter_values, expected_type=type_hints["parameter_values"])
            check_type(argname="argument pipeline_objects", value=pipeline_objects, expected_type=type_hints["pipeline_objects"])
            check_type(argname="argument pipeline_tags", value=pipeline_tags, expected_type=type_hints["pipeline_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if activate is not None:
            self._values["activate"] = activate
        if description is not None:
            self._values["description"] = description
        if parameter_objects is not None:
            self._values["parameter_objects"] = parameter_objects
        if parameter_values is not None:
            self._values["parameter_values"] = parameter_values
        if pipeline_objects is not None:
            self._values["pipeline_objects"] = pipeline_objects
        if pipeline_tags is not None:
            self._values["pipeline_tags"] = pipeline_tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the pipeline.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether to validate and start the pipeline or stop an active pipeline.

        By default, the value is set to ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-activate
        '''
        result = self._values.get("activate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the pipeline.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_objects(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.ParameterObjectProperty]]]]:
        '''The parameter objects used with the pipeline.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parameterobjects
        '''
        result = self._values.get("parameter_objects")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.ParameterObjectProperty]]]], result)

    @builtins.property
    def parameter_values(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.ParameterValueProperty]]]]:
        '''The parameter values used with the pipeline.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-parametervalues
        '''
        result = self._values.get("parameter_values")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.ParameterValueProperty]]]], result)

    @builtins.property
    def pipeline_objects(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.PipelineObjectProperty]]]]:
        '''The objects that define the pipeline.

        These objects overwrite the existing pipeline definition. Not all objects, fields, and values can be updated. For information about restrictions, see `Editing Your Pipeline <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-manage-pipeline-modify-console.html>`_ in the *AWS Data Pipeline Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelineobjects
        '''
        result = self._values.get("pipeline_objects")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.PipelineObjectProperty]]]], result)

    @builtins.property
    def pipeline_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.PipelineTagProperty]]]]:
        '''A list of arbitrary tags (key-value pairs) to associate with the pipeline, which you can use to control permissions.

        For more information, see `Controlling Access to Pipelines and Resources <https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-control-access.html>`_ in the *AWS Data Pipeline Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datapipeline-pipeline.html#cfn-datapipeline-pipeline-pipelinetags
        '''
        result = self._values.get("pipeline_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.PipelineTagProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnPipeline",
    "CfnPipelineProps",
]

publication.publish()

def _typecheckingstub__a259d35408fa1ef72af1c8b5e4ffdb2ed913379c7f39465eaa3a5a33c213f3b1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    parameter_objects: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.ParameterObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    parameter_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.ParameterValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    pipeline_objects: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.PipelineObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    pipeline_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.PipelineTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402e2e3e29a1850e62e49c2816567049c4775858393ebf60b9f433f80c9ff6f9(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e2d8a2f1638a4983e0fb83bb3f24da3a550d2a3a79f41449797ecb46b1e95e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a46f70a9174c4fdca6b612cf3a4d77ecfdf17670d4450724c22b315a2fa612(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bceea8c6f61bdc5056addd76b5b58c81a90de623381163c3be2565ff702afc1a(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b10c7ddd3be0326cea9aa091123a30602516fc94a0a23c687b5803f07ffae00(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297709dcf01039ea59b47821d8538e7f180a654b8bace2424de2523db1ad2eb0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.ParameterObjectProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5a19b6d13fb1b12d1a9fcb5a22b7343809dfe62ea31cdb223817d29a2df235(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.ParameterValueProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65a887274196f67182384490490bf9bc45bcecfcf4eece856427005b058f230(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.PipelineObjectProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4ac4602c2cbed6d09d5ec7388cf4b49c76fcecf379ae549bf78933f6d2fd7a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPipeline.PipelineTagProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81419d6ba902e15556c4eff1db6801701ed0bc6389394a578d614cd7528ddc36(
    *,
    key: builtins.str,
    ref_value: typing.Optional[builtins.str] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18166f4891901bb3befe7811bf3ccf42446aedd01287394261368496247acc5d(
    *,
    key: builtins.str,
    string_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a19dbbf590422eab0eb80b72712c4c55d48789d8588bc65dc8e029e47d05237(
    *,
    attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.ParameterAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]],
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50c169957f80f6242ed12feb7348ced9130e0179fcebba1e3be7c9ddddfcd88(
    *,
    id: builtins.str,
    string_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b227f2f033c7f2dcd2cf08b42858b67f1566f3d549e39a149bc2a190ef88ad(
    *,
    fields: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.FieldProperty, typing.Dict[builtins.str, typing.Any]]]]],
    id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f61225f0839c3b4d3777bf71e2b8b911152c5699298d97c42668f6f6467967(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640b8a6d6bd2d8badf454d3e170ecaedc30a638ebdc5df14138d4721bdf1604b(
    *,
    name: builtins.str,
    activate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    parameter_objects: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.ParameterObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    parameter_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.ParameterValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    pipeline_objects: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.PipelineObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    pipeline_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPipeline.PipelineTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
