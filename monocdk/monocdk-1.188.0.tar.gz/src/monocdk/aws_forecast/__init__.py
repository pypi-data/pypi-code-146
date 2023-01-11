'''
# AWS::Forecast Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as forecast
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Forecast construct libraries](https://constructs.dev/search?q=forecast)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Forecast resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Forecast.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Forecast](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Forecast.html).

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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnDataset(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_forecast.CfnDataset",
):
    '''A CloudFormation ``AWS::Forecast::Dataset``.

    Creates an Amazon Forecast dataset. The information about the dataset that you provide helps Forecast understand how to consume the data for model training. This includes the following:

    - *``DataFrequency``* - How frequently your historical time-series data is collected.
    - *``Domain``* and *``DatasetType``* - Each dataset has an associated dataset domain and a type within the domain. Amazon Forecast provides a list of predefined domains and types within each domain. For each unique dataset domain and type within the domain, Amazon Forecast requires your data to include a minimum set of predefined fields.
    - *``Schema``* - A schema specifies the fields in the dataset, including the field name and data type.

    After creating a dataset, you import your training data into it and add the dataset to a dataset group. You use the dataset group to create a predictor. For more information, see `Importing datasets <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html>`_ .

    To get a list of all your datasets, use the `ListDatasets <https://docs.aws.amazon.com/forecast/latest/dg/API_ListDatasets.html>`_ operation.

    For example Forecast datasets, see the `Amazon Forecast Sample GitHub repository <https://docs.aws.amazon.com/https://github.com/aws-samples/amazon-forecast-samples>`_ .
    .. epigraph::

       The ``Status`` of a dataset must be ``ACTIVE`` before you can import training data. Use the `DescribeDataset <https://docs.aws.amazon.com/forecast/latest/dg/API_DescribeDataset.html>`_ operation to get the status.

    :cloudformationResource: AWS::Forecast::Dataset
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_forecast as forecast
        
        # encryption_config: Any
        # schema: Any
        
        cfn_dataset = forecast.CfnDataset(self, "MyCfnDataset",
            dataset_name="datasetName",
            dataset_type="datasetType",
            domain="domain",
            schema=schema,
        
            # the properties below are optional
            data_frequency="dataFrequency",
            encryption_config=encryption_config,
            tags=[forecast.CfnDataset.TagsItemsProperty(
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
        dataset_name: builtins.str,
        dataset_type: builtins.str,
        domain: builtins.str,
        schema: typing.Any,
        data_frequency: typing.Optional[builtins.str] = None,
        encryption_config: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnDataset.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Forecast::Dataset``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dataset_name: The name of the dataset.
        :param dataset_type: The dataset type.
        :param domain: The domain associated with the dataset.
        :param schema: The schema for the dataset. The schema attributes and their order must match the fields in your data. The dataset ``Domain`` and ``DatasetType`` that you choose determine the minimum required fields in your training data. For information about the required fields for a specific dataset domain and type, see `Dataset Domains and Dataset Types <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-domains-ds-types.html>`_ .
        :param data_frequency: The frequency of data collection. This parameter is required for RELATED_TIME_SERIES datasets. Valid intervals are an integer followed by Y (Year), M (Month), W (Week), D (Day), H (Hour), and min (Minute). For example, "1D" indicates every day and "15min" indicates every 15 minutes. You cannot specify a value that would overlap with the next larger frequency. That means, for example, you cannot specify a frequency of 60 minutes, because that is equivalent to 1 hour. The valid values for each frequency are the following: - Minute - 1-59 - Hour - 1-23 - Day - 1-6 - Week - 1-4 - Month - 1-11 - Year - 1 Thus, if you want every other week forecasts, specify "2W". Or, if you want quarterly forecasts, you specify "3M".
        :param encryption_config: A Key Management Service (KMS) key and the Identity and Access Management (IAM) role that Amazon Forecast can assume to access the key.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ef8e9258718bc48ac62a8b11879bf8172381e3ab4687b862a09f69b07a0201)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDatasetProps(
            dataset_name=dataset_name,
            dataset_type=dataset_type,
            domain=domain,
            schema=schema,
            data_frequency=data_frequency,
            encryption_config=encryption_config,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e28efdfc4a3cbe79ecc04f340f97c162c20b1ffd2c9f4bdbd4a8f95468d77e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44e7ba802920bdf41c195bbf296104741990c432006ccb9aac8e65cc0ee4ca5d)
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
        '''The Amazon Resource Name (ARN) of the dataset.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="datasetName")
    def dataset_name(self) -> builtins.str:
        '''The name of the dataset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-datasetname
        '''
        return typing.cast(builtins.str, jsii.get(self, "datasetName"))

    @dataset_name.setter
    def dataset_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0c55769fdcbd492655fb7147766a1f3a45135bf81c73f48c84cffc70b4ea99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetName", value)

    @builtins.property
    @jsii.member(jsii_name="datasetType")
    def dataset_type(self) -> builtins.str:
        '''The dataset type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-datasettype
        '''
        return typing.cast(builtins.str, jsii.get(self, "datasetType"))

    @dataset_type.setter
    def dataset_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e186489c52d3f1bb7e1895ea2ec0c15a1af3bff2ca6c089e07a984e2a6a7d9f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetType", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        '''The domain associated with the dataset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-domain
        '''
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b67eaae49fe11555062f0f107f9c9854b8f52f9e5de9efce788cf30ba6f139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(self) -> typing.Any:
        '''A Key Management Service (KMS) key and the Identity and Access Management (IAM) role that Amazon Forecast can assume to access the key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-encryptionconfig
        '''
        return typing.cast(typing.Any, jsii.get(self, "encryptionConfig"))

    @encryption_config.setter
    def encryption_config(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6889cbd3ff11fabce4ec3d0876b70732b863c183ed7bbba697e5b18937c69eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionConfig", value)

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> typing.Any:
        '''The schema for the dataset.

        The schema attributes and their order must match the fields in your data. The dataset ``Domain`` and ``DatasetType`` that you choose determine the minimum required fields in your training data. For information about the required fields for a specific dataset domain and type, see `Dataset Domains and Dataset Types <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-domains-ds-types.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-schema
        '''
        return typing.cast(typing.Any, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86642ba35f7d9c2b2b5fb40a85fed6c22ef0f3e00076390c5570537b2dc03bdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="dataFrequency")
    def data_frequency(self) -> typing.Optional[builtins.str]:
        '''The frequency of data collection. This parameter is required for RELATED_TIME_SERIES datasets.

        Valid intervals are an integer followed by Y (Year), M (Month), W (Week), D (Day), H (Hour), and min (Minute). For example, "1D" indicates every day and "15min" indicates every 15 minutes. You cannot specify a value that would overlap with the next larger frequency. That means, for example, you cannot specify a frequency of 60 minutes, because that is equivalent to 1 hour. The valid values for each frequency are the following:

        - Minute - 1-59
        - Hour - 1-23
        - Day - 1-6
        - Week - 1-4
        - Month - 1-11
        - Year - 1

        Thus, if you want every other week forecasts, specify "2W". Or, if you want quarterly forecasts, you specify "3M".

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-datafrequency
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFrequency"))

    @data_frequency.setter
    def data_frequency(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4ecb5f1a0be6b2049fada93fe90d41903d33dc9c48c7fd0ea63609d1ef37a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFrequency", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["CfnDataset.TagsItemsProperty"]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-tags
        '''
        return typing.cast(typing.Optional[typing.List["CfnDataset.TagsItemsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnDataset.TagsItemsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360090827520cf55640f2f42d241609c952c0018ac17266e8a0ef5c8ff34f71e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_forecast.CfnDataset.AttributesItemsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "attribute_type": "attributeType",
        },
    )
    class AttributesItemsProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            attribute_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param attribute_name: ``CfnDataset.AttributesItemsProperty.AttributeName``.
            :param attribute_type: ``CfnDataset.AttributesItemsProperty.AttributeType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-attributesitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_forecast as forecast
                
                attributes_items_property = forecast.CfnDataset.AttributesItemsProperty(
                    attribute_name="attributeName",
                    attribute_type="attributeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d49c0bc5baa9c0350aec4ea796e98f4ba9d5be5f2189867abf811954f6298cc8)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument attribute_type", value=attribute_type, expected_type=type_hints["attribute_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if attribute_type is not None:
                self._values["attribute_type"] = attribute_type

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''``CfnDataset.AttributesItemsProperty.AttributeName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-attributesitems.html#cfn-forecast-dataset-attributesitems-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def attribute_type(self) -> typing.Optional[builtins.str]:
            '''``CfnDataset.AttributesItemsProperty.AttributeType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-attributesitems.html#cfn-forecast-dataset-attributesitems-attributetype
            '''
            result = self._values.get("attribute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributesItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_forecast.CfnDataset.EncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn", "role_arn": "roleArn"},
    )
    class EncryptionConfigProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An AWS Key Management Service (KMS) key and an AWS Identity and Access Management (IAM) role that Amazon Forecast can assume to access the key.

            You can specify this optional object in the ``CreateDataset`` and ``CreatePredictor`` requests.

            :param kms_key_arn: The Amazon Resource Name (ARN) of the KMS key.
            :param role_arn: The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key. Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your account, you get an ``InvalidInputException`` error.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-encryptionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_forecast as forecast
                
                encryption_config_property = forecast.CfnDataset.EncryptionConfigProperty(
                    kms_key_arn="kmsKeyArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5c5e7a06dbf31b4e9b1df15271369026161c3afe9afe71312956e4f26b1c7051)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the KMS key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-encryptionconfig.html#cfn-forecast-dataset-encryptionconfig-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role that Amazon Forecast can assume to access the AWS KMS key.

            Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your account, you get an ``InvalidInputException`` error.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-encryptionconfig.html#cfn-forecast-dataset-encryptionconfig-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_forecast.CfnDataset.SchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes"},
    )
    class SchemaProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDataset.AttributesItemsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Defines the fields of a dataset.

            :param attributes: An array of attributes specifying the name and type of each field in a dataset.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-schema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_forecast as forecast
                
                schema_property = forecast.CfnDataset.SchemaProperty(
                    attributes=[forecast.CfnDataset.AttributesItemsProperty(
                        attribute_name="attributeName",
                        attribute_type="attributeType"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfab63a9e216451d50bf34b5c61d724286f95ac61afb9a60b6255b1964a9cd03)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDataset.AttributesItemsProperty", _IResolvable_a771d0ef]]]]:
            '''An array of attributes specifying the name and type of each field in a dataset.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-schema.html#cfn-forecast-dataset-schema-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDataset.AttributesItemsProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_forecast.CfnDataset.TagsItemsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsItemsProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnDataset.TagsItemsProperty.Key``.
            :param value: ``CfnDataset.TagsItemsProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-tagsitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_forecast as forecast
                
                tags_items_property = forecast.CfnDataset.TagsItemsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12c06c470e1947c467aceef706fedf49299744f010b70fa268ef5e8b45de4dea)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnDataset.TagsItemsProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-tagsitems.html#cfn-forecast-dataset-tagsitems-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnDataset.TagsItemsProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-tagsitems.html#cfn-forecast-dataset-tagsitems-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnDatasetGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_forecast.CfnDatasetGroup",
):
    '''A CloudFormation ``AWS::Forecast::DatasetGroup``.

    Creates a dataset group, which holds a collection of related datasets. You can add datasets to the dataset group when you create the dataset group, or later by using the `UpdateDatasetGroup <https://docs.aws.amazon.com/forecast/latest/dg/API_UpdateDatasetGroup.html>`_ operation.

    After creating a dataset group and adding datasets, you use the dataset group when you create a predictor. For more information, see `Dataset groups <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html>`_ .

    To get a list of all your datasets groups, use the `ListDatasetGroups <https://docs.aws.amazon.com/forecast/latest/dg/API_ListDatasetGroups.html>`_ operation.
    .. epigraph::

       The ``Status`` of a dataset group must be ``ACTIVE`` before you can use the dataset group to create a predictor. To get the status, use the `DescribeDatasetGroup <https://docs.aws.amazon.com/forecast/latest/dg/API_DescribeDatasetGroup.html>`_ operation.

    :cloudformationResource: AWS::Forecast::DatasetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_forecast as forecast
        
        cfn_dataset_group = forecast.CfnDatasetGroup(self, "MyCfnDatasetGroup",
            dataset_group_name="datasetGroupName",
            domain="domain",
        
            # the properties below are optional
            dataset_arns=["datasetArns"],
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
        dataset_group_name: builtins.str,
        domain: builtins.str,
        dataset_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Forecast::DatasetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dataset_group_name: The name of the dataset group.
        :param domain: The domain associated with the dataset group. When you add a dataset to a dataset group, this value and the value specified for the ``Domain`` parameter of the `CreateDataset <https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html>`_ operation must match. The ``Domain`` and ``DatasetType`` that you choose determine the fields that must be present in training data that you import to a dataset. For example, if you choose the ``RETAIL`` domain and ``TARGET_TIME_SERIES`` as the ``DatasetType`` , Amazon Forecast requires that ``item_id`` , ``timestamp`` , and ``demand`` fields are present in your data. For more information, see `Dataset groups <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html>`_ .
        :param dataset_arns: An array of Amazon Resource Names (ARNs) of the datasets that you want to include in the dataset group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee115794123e55021c9e8671d790198a7cf6dafa1f84af1c0d4f11fbfa41dd9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDatasetGroupProps(
            dataset_group_name=dataset_group_name,
            domain=domain,
            dataset_arns=dataset_arns,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b2feb013dcd05afb8daad3920e682926aaff6108b92f9ae8733a08bfce9feb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c64c1e182d6c072a1e250be6d2672eceba54d32c5786a40cd740071068980857)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDatasetGroupArn")
    def attr_dataset_group_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the dataset group.

        :cloudformationAttribute: DatasetGroupArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDatasetGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="datasetGroupName")
    def dataset_group_name(self) -> builtins.str:
        '''The name of the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-datasetgroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "datasetGroupName"))

    @dataset_group_name.setter
    def dataset_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd1ee2177dd70f5ec3fecaedd0709182f8e7f124d1299de6f466282c9195ae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        '''The domain associated with the dataset group.

        When you add a dataset to a dataset group, this value and the value specified for the ``Domain`` parameter of the `CreateDataset <https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html>`_ operation must match.

        The ``Domain`` and ``DatasetType`` that you choose determine the fields that must be present in training data that you import to a dataset. For example, if you choose the ``RETAIL`` domain and ``TARGET_TIME_SERIES`` as the ``DatasetType`` , Amazon Forecast requires that ``item_id`` , ``timestamp`` , and ``demand`` fields are present in your data. For more information, see `Dataset groups <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-domain
        '''
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f07c2326bd4a7877e8e617a14c78cfaa37473b3e38ebc550a22f7709536c55a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="datasetArns")
    def dataset_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of Amazon Resource Names (ARNs) of the datasets that you want to include in the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-datasetarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "datasetArns"))

    @dataset_arns.setter
    def dataset_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32232021fb0dfb5f8960b7b705608e4e82c46ddc5693a9de4a49b97738d25293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetArns", value)


@jsii.data_type(
    jsii_type="monocdk.aws_forecast.CfnDatasetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_group_name": "datasetGroupName",
        "domain": "domain",
        "dataset_arns": "datasetArns",
        "tags": "tags",
    },
)
class CfnDatasetGroupProps:
    def __init__(
        self,
        *,
        dataset_group_name: builtins.str,
        domain: builtins.str,
        dataset_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDatasetGroup``.

        :param dataset_group_name: The name of the dataset group.
        :param domain: The domain associated with the dataset group. When you add a dataset to a dataset group, this value and the value specified for the ``Domain`` parameter of the `CreateDataset <https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html>`_ operation must match. The ``Domain`` and ``DatasetType`` that you choose determine the fields that must be present in training data that you import to a dataset. For example, if you choose the ``RETAIL`` domain and ``TARGET_TIME_SERIES`` as the ``DatasetType`` , Amazon Forecast requires that ``item_id`` , ``timestamp`` , and ``demand`` fields are present in your data. For more information, see `Dataset groups <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html>`_ .
        :param dataset_arns: An array of Amazon Resource Names (ARNs) of the datasets that you want to include in the dataset group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_forecast as forecast
            
            cfn_dataset_group_props = forecast.CfnDatasetGroupProps(
                dataset_group_name="datasetGroupName",
                domain="domain",
            
                # the properties below are optional
                dataset_arns=["datasetArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ed7a931788bb0fa9715fe939a23d2641d6eccd082050ca3229698ca2719d93)
            check_type(argname="argument dataset_group_name", value=dataset_group_name, expected_type=type_hints["dataset_group_name"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument dataset_arns", value=dataset_arns, expected_type=type_hints["dataset_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_group_name": dataset_group_name,
            "domain": domain,
        }
        if dataset_arns is not None:
            self._values["dataset_arns"] = dataset_arns
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dataset_group_name(self) -> builtins.str:
        '''The name of the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-datasetgroupname
        '''
        result = self._values.get("dataset_group_name")
        assert result is not None, "Required property 'dataset_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> builtins.str:
        '''The domain associated with the dataset group.

        When you add a dataset to a dataset group, this value and the value specified for the ``Domain`` parameter of the `CreateDataset <https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html>`_ operation must match.

        The ``Domain`` and ``DatasetType`` that you choose determine the fields that must be present in training data that you import to a dataset. For example, if you choose the ``RETAIL`` domain and ``TARGET_TIME_SERIES`` as the ``DatasetType`` , Amazon Forecast requires that ``item_id`` , ``timestamp`` , and ``demand`` fields are present in your data. For more information, see `Dataset groups <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-domain
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of Amazon Resource Names (ARNs) of the datasets that you want to include in the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-datasetarns
        '''
        result = self._values.get("dataset_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_forecast.CfnDatasetProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_name": "datasetName",
        "dataset_type": "datasetType",
        "domain": "domain",
        "schema": "schema",
        "data_frequency": "dataFrequency",
        "encryption_config": "encryptionConfig",
        "tags": "tags",
    },
)
class CfnDatasetProps:
    def __init__(
        self,
        *,
        dataset_name: builtins.str,
        dataset_type: builtins.str,
        domain: builtins.str,
        schema: typing.Any,
        data_frequency: typing.Optional[builtins.str] = None,
        encryption_config: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnDataset.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDataset``.

        :param dataset_name: The name of the dataset.
        :param dataset_type: The dataset type.
        :param domain: The domain associated with the dataset.
        :param schema: The schema for the dataset. The schema attributes and their order must match the fields in your data. The dataset ``Domain`` and ``DatasetType`` that you choose determine the minimum required fields in your training data. For information about the required fields for a specific dataset domain and type, see `Dataset Domains and Dataset Types <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-domains-ds-types.html>`_ .
        :param data_frequency: The frequency of data collection. This parameter is required for RELATED_TIME_SERIES datasets. Valid intervals are an integer followed by Y (Year), M (Month), W (Week), D (Day), H (Hour), and min (Minute). For example, "1D" indicates every day and "15min" indicates every 15 minutes. You cannot specify a value that would overlap with the next larger frequency. That means, for example, you cannot specify a frequency of 60 minutes, because that is equivalent to 1 hour. The valid values for each frequency are the following: - Minute - 1-59 - Hour - 1-23 - Day - 1-6 - Week - 1-4 - Month - 1-11 - Year - 1 Thus, if you want every other week forecasts, specify "2W". Or, if you want quarterly forecasts, you specify "3M".
        :param encryption_config: A Key Management Service (KMS) key and the Identity and Access Management (IAM) role that Amazon Forecast can assume to access the key.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_forecast as forecast
            
            # encryption_config: Any
            # schema: Any
            
            cfn_dataset_props = forecast.CfnDatasetProps(
                dataset_name="datasetName",
                dataset_type="datasetType",
                domain="domain",
                schema=schema,
            
                # the properties below are optional
                data_frequency="dataFrequency",
                encryption_config=encryption_config,
                tags=[forecast.CfnDataset.TagsItemsProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d943b95b4e9d3a29de8aef44030eb54e90e9d20cb52d4d0c0729ecc6c597a87c)
            check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
            check_type(argname="argument dataset_type", value=dataset_type, expected_type=type_hints["dataset_type"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument data_frequency", value=data_frequency, expected_type=type_hints["data_frequency"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_name": dataset_name,
            "dataset_type": dataset_type,
            "domain": domain,
            "schema": schema,
        }
        if data_frequency is not None:
            self._values["data_frequency"] = data_frequency
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dataset_name(self) -> builtins.str:
        '''The name of the dataset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-datasetname
        '''
        result = self._values.get("dataset_name")
        assert result is not None, "Required property 'dataset_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_type(self) -> builtins.str:
        '''The dataset type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-datasettype
        '''
        result = self._values.get("dataset_type")
        assert result is not None, "Required property 'dataset_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> builtins.str:
        '''The domain associated with the dataset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-domain
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> typing.Any:
        '''The schema for the dataset.

        The schema attributes and their order must match the fields in your data. The dataset ``Domain`` and ``DatasetType`` that you choose determine the minimum required fields in your training data. For information about the required fields for a specific dataset domain and type, see `Dataset Domains and Dataset Types <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-domains-ds-types.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-schema
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def data_frequency(self) -> typing.Optional[builtins.str]:
        '''The frequency of data collection. This parameter is required for RELATED_TIME_SERIES datasets.

        Valid intervals are an integer followed by Y (Year), M (Month), W (Week), D (Day), H (Hour), and min (Minute). For example, "1D" indicates every day and "15min" indicates every 15 minutes. You cannot specify a value that would overlap with the next larger frequency. That means, for example, you cannot specify a frequency of 60 minutes, because that is equivalent to 1 hour. The valid values for each frequency are the following:

        - Minute - 1-59
        - Hour - 1-23
        - Day - 1-6
        - Week - 1-4
        - Month - 1-11
        - Year - 1

        Thus, if you want every other week forecasts, specify "2W". Or, if you want quarterly forecasts, you specify "3M".

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-datafrequency
        '''
        result = self._values.get("data_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_config(self) -> typing.Any:
        '''A Key Management Service (KMS) key and the Identity and Access Management (IAM) role that Amazon Forecast can assume to access the key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-encryptionconfig
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnDataset.TagsItemsProperty]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnDataset.TagsItemsProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDataset",
    "CfnDatasetGroup",
    "CfnDatasetGroupProps",
    "CfnDatasetProps",
]

publication.publish()

def _typecheckingstub__29ef8e9258718bc48ac62a8b11879bf8172381e3ab4687b862a09f69b07a0201(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    dataset_name: builtins.str,
    dataset_type: builtins.str,
    domain: builtins.str,
    schema: typing.Any,
    data_frequency: typing.Optional[builtins.str] = None,
    encryption_config: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDataset.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e28efdfc4a3cbe79ecc04f340f97c162c20b1ffd2c9f4bdbd4a8f95468d77e1(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e7ba802920bdf41c195bbf296104741990c432006ccb9aac8e65cc0ee4ca5d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0c55769fdcbd492655fb7147766a1f3a45135bf81c73f48c84cffc70b4ea99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e186489c52d3f1bb7e1895ea2ec0c15a1af3bff2ca6c089e07a984e2a6a7d9f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b67eaae49fe11555062f0f107f9c9854b8f52f9e5de9efce788cf30ba6f139(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6889cbd3ff11fabce4ec3d0876b70732b863c183ed7bbba697e5b18937c69eed(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86642ba35f7d9c2b2b5fb40a85fed6c22ef0f3e00076390c5570537b2dc03bdb(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4ecb5f1a0be6b2049fada93fe90d41903d33dc9c48c7fd0ea63609d1ef37a0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360090827520cf55640f2f42d241609c952c0018ac17266e8a0ef5c8ff34f71e(
    value: typing.Optional[typing.List[CfnDataset.TagsItemsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49c0bc5baa9c0350aec4ea796e98f4ba9d5be5f2189867abf811954f6298cc8(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    attribute_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5e7a06dbf31b4e9b1df15271369026161c3afe9afe71312956e4f26b1c7051(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfab63a9e216451d50bf34b5c61d724286f95ac61afb9a60b6255b1964a9cd03(
    *,
    attributes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDataset.AttributesItemsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c06c470e1947c467aceef706fedf49299744f010b70fa268ef5e8b45de4dea(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee115794123e55021c9e8671d790198a7cf6dafa1f84af1c0d4f11fbfa41dd9(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    dataset_group_name: builtins.str,
    domain: builtins.str,
    dataset_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b2feb013dcd05afb8daad3920e682926aaff6108b92f9ae8733a08bfce9feb(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64c1e182d6c072a1e250be6d2672eceba54d32c5786a40cd740071068980857(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd1ee2177dd70f5ec3fecaedd0709182f8e7f124d1299de6f466282c9195ae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f07c2326bd4a7877e8e617a14c78cfaa37473b3e38ebc550a22f7709536c55a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32232021fb0dfb5f8960b7b705608e4e82c46ddc5693a9de4a49b97738d25293(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ed7a931788bb0fa9715fe939a23d2641d6eccd082050ca3229698ca2719d93(
    *,
    dataset_group_name: builtins.str,
    domain: builtins.str,
    dataset_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d943b95b4e9d3a29de8aef44030eb54e90e9d20cb52d4d0c0729ecc6c597a87c(
    *,
    dataset_name: builtins.str,
    dataset_type: builtins.str,
    domain: builtins.str,
    schema: typing.Any,
    data_frequency: typing.Optional[builtins.str] = None,
    encryption_config: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDataset.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
