'''
# AWS::Personalize Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_personalize as personalize
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Personalize construct libraries](https://constructs.dev/search?q=personalize)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Personalize resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Personalize.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Personalize](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Personalize.html).

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
class CfnDataset(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-personalize.CfnDataset",
):
    '''A CloudFormation ``AWS::Personalize::Dataset``.

    Creates an empty dataset and adds it to the specified dataset group. Use `CreateDatasetImportJob <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDatasetImportJob.html>`_ to import your training data to a dataset.

    There are three types of datasets:

    - Interactions
    - Items
    - Users

    Each dataset type has an associated schema with required field types. Only the ``Interactions`` dataset is required in order to train a model (also referred to as creating a solution).

    A dataset can be in one of the following states:

    - CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED
    - DELETE PENDING > DELETE IN_PROGRESS

    To get the status of the dataset, call `DescribeDataset <https://docs.aws.amazon.com/personalize/latest/dg/API_DescribeDataset.html>`_ .

    **Related APIs** - `CreateDatasetGroup <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDatasetGroup.html>`_

    - `ListDatasets <https://docs.aws.amazon.com/personalize/latest/dg/API_ListDatasets.html>`_
    - `DescribeDataset <https://docs.aws.amazon.com/personalize/latest/dg/API_DescribeDataset.html>`_
    - `DeleteDataset <https://docs.aws.amazon.com/personalize/latest/dg/API_DeleteDataset.html>`_

    :cloudformationResource: AWS::Personalize::Dataset
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_personalize as personalize
        
        # data_source: Any
        
        cfn_dataset = personalize.CfnDataset(self, "MyCfnDataset",
            dataset_group_arn="datasetGroupArn",
            dataset_type="datasetType",
            name="name",
            schema_arn="schemaArn",
        
            # the properties below are optional
            dataset_import_job=personalize.CfnDataset.DatasetImportJobProperty(
                dataset_arn="datasetArn",
                dataset_import_job_arn="datasetImportJobArn",
                data_source=data_source,
                job_name="jobName",
                role_arn="roleArn"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        dataset_group_arn: builtins.str,
        dataset_type: builtins.str,
        name: builtins.str,
        schema_arn: builtins.str,
        dataset_import_job: typing.Optional[typing.Union[typing.Union["CfnDataset.DatasetImportJobProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::Personalize::Dataset``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dataset_group_arn: The Amazon Resource Name (ARN) of the dataset group.
        :param dataset_type: One of the following values:. - Interactions - Items - Users
        :param name: The name of the dataset.
        :param schema_arn: The ARN of the associated schema.
        :param dataset_import_job: Describes a job that imports training data from a data source (Amazon S3 bucket) to an Amazon Personalize dataset.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf8a77fa1b7db6041ca39dead952a3e5ec0ec6fc35eb62d778644fab1b7055b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDatasetProps(
            dataset_group_arn=dataset_group_arn,
            dataset_type=dataset_type,
            name=name,
            schema_arn=schema_arn,
            dataset_import_job=dataset_import_job,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af0e90f73eaf1361e0d2ebcbf41fbe9db7bab230bde5fce1111d306b228cbc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2713723c8ab7065fd2b992587a76c65203bc626ee3529dc5a10e21a586f0c352)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDatasetArn")
    def attr_dataset_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the dataset.

        :cloudformationAttribute: DatasetArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDatasetArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="datasetGroupArn")
    def dataset_group_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-datasetgrouparn
        '''
        return typing.cast(builtins.str, jsii.get(self, "datasetGroupArn"))

    @dataset_group_arn.setter
    def dataset_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97904bb0fb2491f211dcfb8e236c6e809a82631eaaf8debd2af366362a01c21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="datasetType")
    def dataset_type(self) -> builtins.str:
        '''One of the following values:.

        - Interactions
        - Items
        - Users

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-datasettype
        '''
        return typing.cast(builtins.str, jsii.get(self, "datasetType"))

    @dataset_type.setter
    def dataset_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7fc14414585bc0a054dc333f4606a903d6f5fbecb2c7e3481ea72585caba5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the dataset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0a67ecfdfb636659d74ce66f322419f0f7c0315d282cb3182336071b1d4134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="schemaArn")
    def schema_arn(self) -> builtins.str:
        '''The ARN of the associated schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-schemaarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "schemaArn"))

    @schema_arn.setter
    def schema_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b186e2244b8f85f981897989d8b81c4ff3d7f54c74051522c43816c8b197b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaArn", value)

    @builtins.property
    @jsii.member(jsii_name="datasetImportJob")
    def dataset_import_job(
        self,
    ) -> typing.Optional[typing.Union["CfnDataset.DatasetImportJobProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''Describes a job that imports training data from a data source (Amazon S3 bucket) to an Amazon Personalize dataset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-datasetimportjob
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDataset.DatasetImportJobProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "datasetImportJob"))

    @dataset_import_job.setter
    def dataset_import_job(
        self,
        value: typing.Optional[typing.Union["CfnDataset.DatasetImportJobProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c7a168946676fa588824e81f36f5953a9ed70bf8b30c03553a45d35bb2c807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetImportJob", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnDataset.DataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"data_location": "dataLocation"},
    )
    class DataSourceProperty:
        def __init__(
            self,
            *,
            data_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the data source that contains the data to upload to a dataset.

            :param data_location: The path to the Amazon S3 bucket where the data that you want to upload to your dataset is stored. For example: ``s3://bucket-name/folder-name/``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                data_source_property = personalize.CfnDataset.DataSourceProperty(
                    data_location="dataLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd0278f363afc7be1112c8c382047c98436642405aaccd13ebe291d00bb649fe)
                check_type(argname="argument data_location", value=data_location, expected_type=type_hints["data_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_location is not None:
                self._values["data_location"] = data_location

        @builtins.property
        def data_location(self) -> typing.Optional[builtins.str]:
            '''The path to the Amazon S3 bucket where the data that you want to upload to your dataset is stored.

            For example:

            ``s3://bucket-name/folder-name/``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasource.html#cfn-personalize-dataset-datasource-datalocation
            '''
            result = self._values.get("data_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnDataset.DatasetImportJobProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dataset_arn": "datasetArn",
            "dataset_import_job_arn": "datasetImportJobArn",
            "data_source": "dataSource",
            "job_name": "jobName",
            "role_arn": "roleArn",
        },
    )
    class DatasetImportJobProperty:
        def __init__(
            self,
            *,
            dataset_arn: typing.Optional[builtins.str] = None,
            dataset_import_job_arn: typing.Optional[builtins.str] = None,
            data_source: typing.Any = None,
            job_name: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a job that imports training data from a data source (Amazon S3 bucket) to an Amazon Personalize dataset.

            For more information, see `CreateDatasetImportJob <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDatasetImportJob.html>`_ .

            A dataset import job can be in one of the following states:

            - CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED

            :param dataset_arn: The Amazon Resource Name (ARN) of the dataset that receives the imported data.
            :param dataset_import_job_arn: The ARN of the dataset import job.
            :param data_source: The Amazon S3 bucket that contains the training data to import.
            :param job_name: The name of the import job.
            :param role_arn: The ARN of the IAM role that has permissions to read from the Amazon S3 data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                # data_source: Any
                
                dataset_import_job_property = personalize.CfnDataset.DatasetImportJobProperty(
                    dataset_arn="datasetArn",
                    dataset_import_job_arn="datasetImportJobArn",
                    data_source=data_source,
                    job_name="jobName",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84e07de0dac3bcb21f154d56a6a433353f817f690b98f4f45184c9d1a6aa4b4d)
                check_type(argname="argument dataset_arn", value=dataset_arn, expected_type=type_hints["dataset_arn"])
                check_type(argname="argument dataset_import_job_arn", value=dataset_import_job_arn, expected_type=type_hints["dataset_import_job_arn"])
                check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
                check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dataset_arn is not None:
                self._values["dataset_arn"] = dataset_arn
            if dataset_import_job_arn is not None:
                self._values["dataset_import_job_arn"] = dataset_import_job_arn
            if data_source is not None:
                self._values["data_source"] = data_source
            if job_name is not None:
                self._values["job_name"] = job_name
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def dataset_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the dataset that receives the imported data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html#cfn-personalize-dataset-datasetimportjob-datasetarn
            '''
            result = self._values.get("dataset_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dataset_import_job_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the dataset import job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html#cfn-personalize-dataset-datasetimportjob-datasetimportjobarn
            '''
            result = self._values.get("dataset_import_job_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_source(self) -> typing.Any:
            '''The Amazon S3 bucket that contains the training data to import.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html#cfn-personalize-dataset-datasetimportjob-datasource
            '''
            result = self._values.get("data_source")
            return typing.cast(typing.Any, result)

        @builtins.property
        def job_name(self) -> typing.Optional[builtins.str]:
            '''The name of the import job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html#cfn-personalize-dataset-datasetimportjob-jobname
            '''
            result = self._values.get("job_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role that has permissions to read from the Amazon S3 data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html#cfn-personalize-dataset-datasetimportjob-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetImportJobProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDatasetGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-personalize.CfnDatasetGroup",
):
    '''A CloudFormation ``AWS::Personalize::DatasetGroup``.

    A dataset group is a collection of related datasets (Interactions, User, and Item). You create a dataset group by calling `CreateDatasetGroup <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDatasetGroup.html>`_ . You then create a dataset and add it to a dataset group by calling `CreateDataset <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDataset.html>`_ . The dataset group is used to create and train a solution by calling `CreateSolution <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateSolution.html>`_ . A dataset group can contain only one of each type of dataset.

    You can specify an AWS Key Management Service (KMS) key to encrypt the datasets in the group.

    :cloudformationResource: AWS::Personalize::DatasetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_personalize as personalize
        
        cfn_dataset_group = personalize.CfnDatasetGroup(self, "MyCfnDatasetGroup",
            name="name",
        
            # the properties below are optional
            domain="domain",
            kms_key_arn="kmsKeyArn",
            role_arn="roleArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Personalize::DatasetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the dataset group.
        :param domain: The domain of a Domain dataset group.
        :param kms_key_arn: The Amazon Resource Name (ARN) of the AWS Key Management Service (KMS) key used to encrypt the datasets.
        :param role_arn: The ARN of the IAM role that has permissions to create the dataset group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3570de5b03a449c0fe5332ece68bcd4620b6005e3bd51336cbc0fa9d9878120b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDatasetGroupProps(
            name=name, domain=domain, kms_key_arn=kms_key_arn, role_arn=role_arn
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f78a2507f6e1b5217b383a7e13c885e6925ed21645961415ec2b3f32017c11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__233244d6671c11b7b169853dfde07077d704f69cf2663ccf0405f04fd8a31994)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fed7ca2ec87d06e0938a3a2524b77d7950b64593718aef55c4d9e3dda189773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain of a Domain dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-domain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86162b7b06bae8240d77ef03b5be62f4bbf6b8d65c73a4456959c88bbd20d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Key Management Service (KMS) key used to encrypt the datasets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-kmskeyarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9482a37792b59b25afa0e3476a273f2ab8a403925f240e59c305faed0b9e3059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that has permissions to create the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76dc70f48959b8901aa004ad7e2ee8fd46d0afe0fec8835639dc332f82699cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-personalize.CfnDatasetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "domain": "domain",
        "kms_key_arn": "kmsKeyArn",
        "role_arn": "roleArn",
    },
)
class CfnDatasetGroupProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDatasetGroup``.

        :param name: The name of the dataset group.
        :param domain: The domain of a Domain dataset group.
        :param kms_key_arn: The Amazon Resource Name (ARN) of the AWS Key Management Service (KMS) key used to encrypt the datasets.
        :param role_arn: The ARN of the IAM role that has permissions to create the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_personalize as personalize
            
            cfn_dataset_group_props = personalize.CfnDatasetGroupProps(
                name="name",
            
                # the properties below are optional
                domain="domain",
                kms_key_arn="kmsKeyArn",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b648503a401f01beb6222bd0af27c00da9fd299ee3ccb0a80daebda23992e79e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if domain is not None:
            self._values["domain"] = domain
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain of a Domain dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Key Management Service (KMS) key used to encrypt the datasets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that has permissions to create the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-personalize.CfnDatasetProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_group_arn": "datasetGroupArn",
        "dataset_type": "datasetType",
        "name": "name",
        "schema_arn": "schemaArn",
        "dataset_import_job": "datasetImportJob",
    },
)
class CfnDatasetProps:
    def __init__(
        self,
        *,
        dataset_group_arn: builtins.str,
        dataset_type: builtins.str,
        name: builtins.str,
        schema_arn: builtins.str,
        dataset_import_job: typing.Optional[typing.Union[typing.Union[CfnDataset.DatasetImportJobProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDataset``.

        :param dataset_group_arn: The Amazon Resource Name (ARN) of the dataset group.
        :param dataset_type: One of the following values:. - Interactions - Items - Users
        :param name: The name of the dataset.
        :param schema_arn: The ARN of the associated schema.
        :param dataset_import_job: Describes a job that imports training data from a data source (Amazon S3 bucket) to an Amazon Personalize dataset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_personalize as personalize
            
            # data_source: Any
            
            cfn_dataset_props = personalize.CfnDatasetProps(
                dataset_group_arn="datasetGroupArn",
                dataset_type="datasetType",
                name="name",
                schema_arn="schemaArn",
            
                # the properties below are optional
                dataset_import_job=personalize.CfnDataset.DatasetImportJobProperty(
                    dataset_arn="datasetArn",
                    dataset_import_job_arn="datasetImportJobArn",
                    data_source=data_source,
                    job_name="jobName",
                    role_arn="roleArn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170e5421c2620440ae17a8534108beb32b93cdce31b718c033d4cb7edcbbad21)
            check_type(argname="argument dataset_group_arn", value=dataset_group_arn, expected_type=type_hints["dataset_group_arn"])
            check_type(argname="argument dataset_type", value=dataset_type, expected_type=type_hints["dataset_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema_arn", value=schema_arn, expected_type=type_hints["schema_arn"])
            check_type(argname="argument dataset_import_job", value=dataset_import_job, expected_type=type_hints["dataset_import_job"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_group_arn": dataset_group_arn,
            "dataset_type": dataset_type,
            "name": name,
            "schema_arn": schema_arn,
        }
        if dataset_import_job is not None:
            self._values["dataset_import_job"] = dataset_import_job

    @builtins.property
    def dataset_group_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-datasetgrouparn
        '''
        result = self._values.get("dataset_group_arn")
        assert result is not None, "Required property 'dataset_group_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_type(self) -> builtins.str:
        '''One of the following values:.

        - Interactions
        - Items
        - Users

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-datasettype
        '''
        result = self._values.get("dataset_type")
        assert result is not None, "Required property 'dataset_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the dataset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema_arn(self) -> builtins.str:
        '''The ARN of the associated schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-schemaarn
        '''
        result = self._values.get("schema_arn")
        assert result is not None, "Required property 'schema_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_import_job(
        self,
    ) -> typing.Optional[typing.Union[CfnDataset.DatasetImportJobProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Describes a job that imports training data from a data source (Amazon S3 bucket) to an Amazon Personalize dataset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-datasetimportjob
        '''
        result = self._values.get("dataset_import_job")
        return typing.cast(typing.Optional[typing.Union[CfnDataset.DatasetImportJobProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSchema(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-personalize.CfnSchema",
):
    '''A CloudFormation ``AWS::Personalize::Schema``.

    Creates an Amazon Personalize schema from the specified schema string. The schema you create must be in Avro JSON format.

    Amazon Personalize recognizes three schema variants. Each schema is associated with a dataset type and has a set of required field and keywords. If you are creating a schema for a dataset in a Domain dataset group, you provide the domain of the Domain dataset group. You specify a schema when you call `CreateDataset <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDataset.html>`_ .

    For more information on schemas, see `Datasets and schemas <https://docs.aws.amazon.com/personalize/latest/dg/how-it-works-dataset-schema.html>`_ .

    **Related APIs** - `ListSchemas <https://docs.aws.amazon.com/personalize/latest/dg/API_ListSchemas.html>`_

    - `DescribeSchema <https://docs.aws.amazon.com/personalize/latest/dg/API_DescribeSchema.html>`_
    - `DeleteSchema <https://docs.aws.amazon.com/personalize/latest/dg/API_DeleteSchema.html>`_

    :cloudformationResource: AWS::Personalize::Schema
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_personalize as personalize
        
        cfn_schema = personalize.CfnSchema(self, "MyCfnSchema",
            name="name",
            schema="schema",
        
            # the properties below are optional
            domain="domain"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        schema: builtins.str,
        domain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Personalize::Schema``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the schema.
        :param schema: The schema.
        :param domain: The domain of a schema that you created for a dataset in a Domain dataset group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d802b29f1eccb88439ff9a65f27618ed36c1cbc2b0460bb3029e2667a372d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSchemaProps(name=name, schema=schema, domain=domain)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0b17267f31a927139c3c3c9762139e8cbf023dfad58d2dc3b73e1ff473536e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e9a8b2451663454255f294f6e043d87ee3e6af2d3c0fe69cc13433f7d669d88)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSchemaArn")
    def attr_schema_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the schema.

        :cloudformationAttribute: SchemaArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSchemaArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html#cfn-personalize-schema-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17aa1472f054b84e09afdc3e92157aa9e4a4ccaf7850a26679daf7e149b3a8e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        '''The schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html#cfn-personalize-schema-schema
        '''
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef3c8f772c75e7741afb9ccef31f1531dcaea2a0f5b8a8ddf5a3e7c8f2f6a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain of a schema that you created for a dataset in a Domain dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html#cfn-personalize-schema-domain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98eed33aae5f80e7898feea11c83f68515f563b6b7b317622b3e5815433a4864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-personalize.CfnSchemaProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "schema": "schema", "domain": "domain"},
)
class CfnSchemaProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        schema: builtins.str,
        domain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSchema``.

        :param name: The name of the schema.
        :param schema: The schema.
        :param domain: The domain of a schema that you created for a dataset in a Domain dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_personalize as personalize
            
            cfn_schema_props = personalize.CfnSchemaProps(
                name="name",
                schema="schema",
            
                # the properties below are optional
                domain="domain"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638695462e4fea7e98eadcd53399f6eac00fef9aafa80dbc7fdd2c19dd0f9ef9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "schema": schema,
        }
        if domain is not None:
            self._values["domain"] = domain

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html#cfn-personalize-schema-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html#cfn-personalize-schema-schema
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain of a schema that you created for a dataset in a Domain dataset group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html#cfn-personalize-schema-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSchemaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSolution(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-personalize.CfnSolution",
):
    '''A CloudFormation ``AWS::Personalize::Solution``.

    An object that provides information about a solution. A solution is a trained model that can be deployed as a campaign.

    :cloudformationResource: AWS::Personalize::Solution
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_personalize as personalize
        
        # auto_ml_config: Any
        # hpo_config: Any
        
        cfn_solution = personalize.CfnSolution(self, "MyCfnSolution",
            dataset_group_arn="datasetGroupArn",
            name="name",
        
            # the properties below are optional
            event_type="eventType",
            perform_auto_ml=False,
            perform_hpo=False,
            recipe_arn="recipeArn",
            solution_config=personalize.CfnSolution.SolutionConfigProperty(
                algorithm_hyper_parameters={
                    "algorithm_hyper_parameters_key": "algorithmHyperParameters"
                },
                auto_ml_config=auto_ml_config,
                event_value_threshold="eventValueThreshold",
                feature_transformation_parameters={
                    "feature_transformation_parameters_key": "featureTransformationParameters"
                },
                hpo_config=hpo_config
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        dataset_group_arn: builtins.str,
        name: builtins.str,
        event_type: typing.Optional[builtins.str] = None,
        perform_auto_ml: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        perform_hpo: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        recipe_arn: typing.Optional[builtins.str] = None,
        solution_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSolution.SolutionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Personalize::Solution``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dataset_group_arn: The Amazon Resource Name (ARN) of the dataset group that provides the training data.
        :param name: The name of the solution.
        :param event_type: The event type (for example, 'click' or 'like') that is used for training the model. If no ``eventType`` is provided, Amazon Personalize uses all interactions for training with equal weight regardless of type.
        :param perform_auto_ml: .. epigraph:: We don't recommend enabling automated machine learning. Instead, match your use case to the available Amazon Personalize recipes. For more information, see `Determining your use case. <https://docs.aws.amazon.com/personalize/latest/dg/determining-use-case.html>`_ When true, Amazon Personalize performs a search for the best USER_PERSONALIZATION recipe from the list specified in the solution configuration ( ``recipeArn`` must not be specified). When false (the default), Amazon Personalize uses ``recipeArn`` for training.
        :param perform_hpo: Whether to perform hyperparameter optimization (HPO) on the chosen recipe. The default is ``false`` .
        :param recipe_arn: The ARN of the recipe used to create the solution.
        :param solution_config: Describes the configuration properties for the solution.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc347588a2a8e0ad6e70dcbe0c4e0d2c19221c579d86f463e795c5d497072b3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSolutionProps(
            dataset_group_arn=dataset_group_arn,
            name=name,
            event_type=event_type,
            perform_auto_ml=perform_auto_ml,
            perform_hpo=perform_hpo,
            recipe_arn=recipe_arn,
            solution_config=solution_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d7c7501db412a48d5ced091a1edf2ddac962d488281b796bc2af839347640d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee39e6d7cb53570c24fc29413a2e45eafae85804521b6239244557343837b97e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSolutionArn")
    def attr_solution_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the solution.

        :cloudformationAttribute: SolutionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSolutionArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="datasetGroupArn")
    def dataset_group_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the dataset group that provides the training data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-datasetgrouparn
        '''
        return typing.cast(builtins.str, jsii.get(self, "datasetGroupArn"))

    @dataset_group_arn.setter
    def dataset_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a025e7521524110cbe3dae051fdcdd12c614408d7ba516f5beeb5a91ce97098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the solution.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbd3962d59115ec758487e726cedaee192da1ed1a703c4c5b9ff896bf2630fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> typing.Optional[builtins.str]:
        '''The event type (for example, 'click' or 'like') that is used for training the model.

        If no ``eventType`` is provided, Amazon Personalize uses all interactions for training with equal weight regardless of type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-eventtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c6b75aa2ea86be2592ef9a07f55af9feb33092345831fff4738214cbdce72c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value)

    @builtins.property
    @jsii.member(jsii_name="performAutoMl")
    def perform_auto_ml(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''.. epigraph::

   We don't recommend enabling automated machine learning.

        Instead, match your use case to the available Amazon Personalize recipes. For more information, see `Determining your use case. <https://docs.aws.amazon.com/personalize/latest/dg/determining-use-case.html>`_

        When true, Amazon Personalize performs a search for the best USER_PERSONALIZATION recipe from the list specified in the solution configuration ( ``recipeArn`` must not be specified). When false (the default), Amazon Personalize uses ``recipeArn`` for training.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-performautoml
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "performAutoMl"))

    @perform_auto_ml.setter
    def perform_auto_ml(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63af310ef2a950c148ffc1654d2d382bec929942560b47d339475ec0124e9507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performAutoMl", value)

    @builtins.property
    @jsii.member(jsii_name="performHpo")
    def perform_hpo(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Whether to perform hyperparameter optimization (HPO) on the chosen recipe.

        The default is ``false`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-performhpo
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "performHpo"))

    @perform_hpo.setter
    def perform_hpo(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ab3b11cdef1d6b1ec9d39fa9ddcdacf2630404f1c1e4fb72d1bfa3d40c4cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performHpo", value)

    @builtins.property
    @jsii.member(jsii_name="recipeArn")
    def recipe_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the recipe used to create the solution.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-recipearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recipeArn"))

    @recipe_arn.setter
    def recipe_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be20be8f1b831141405634c45196b6662e45fc5101c70e5d49e3f3e107155236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipeArn", value)

    @builtins.property
    @jsii.member(jsii_name="solutionConfig")
    def solution_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.SolutionConfigProperty"]]:
        '''Describes the configuration properties for the solution.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-solutionconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.SolutionConfigProperty"]], jsii.get(self, "solutionConfig"))

    @solution_config.setter
    def solution_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.SolutionConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f61df265d3ee9ece087763f8c166789fd17565a6e580515d1410d70c235655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "solutionConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnSolution.AlgorithmHyperParameterRangesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "categorical_hyper_parameter_ranges": "categoricalHyperParameterRanges",
            "continuous_hyper_parameter_ranges": "continuousHyperParameterRanges",
            "integer_hyper_parameter_ranges": "integerHyperParameterRanges",
        },
    )
    class AlgorithmHyperParameterRangesProperty:
        def __init__(
            self,
            *,
            categorical_hyper_parameter_ranges: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSolution.CategoricalHyperParameterRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            continuous_hyper_parameter_ranges: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSolution.ContinuousHyperParameterRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            integer_hyper_parameter_ranges: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSolution.IntegerHyperParameterRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''
            :param categorical_hyper_parameter_ranges: ``CfnSolution.AlgorithmHyperParameterRangesProperty.CategoricalHyperParameterRanges``.
            :param continuous_hyper_parameter_ranges: ``CfnSolution.AlgorithmHyperParameterRangesProperty.ContinuousHyperParameterRanges``.
            :param integer_hyper_parameter_ranges: ``CfnSolution.AlgorithmHyperParameterRangesProperty.IntegerHyperParameterRanges``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-algorithmhyperparameterranges.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                algorithm_hyper_parameter_ranges_property = personalize.CfnSolution.AlgorithmHyperParameterRangesProperty(
                    categorical_hyper_parameter_ranges=[personalize.CfnSolution.CategoricalHyperParameterRangeProperty(
                        name="name",
                        values=["values"]
                    )],
                    continuous_hyper_parameter_ranges=[personalize.CfnSolution.ContinuousHyperParameterRangeProperty(
                        max_value=123,
                        min_value=123,
                        name="name"
                    )],
                    integer_hyper_parameter_ranges=[personalize.CfnSolution.IntegerHyperParameterRangeProperty(
                        max_value=123,
                        min_value=123,
                        name="name"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27409c42888b8dd7b13ce15077a2531ed1b0f73b29148d0d779dab6d6adfba6f)
                check_type(argname="argument categorical_hyper_parameter_ranges", value=categorical_hyper_parameter_ranges, expected_type=type_hints["categorical_hyper_parameter_ranges"])
                check_type(argname="argument continuous_hyper_parameter_ranges", value=continuous_hyper_parameter_ranges, expected_type=type_hints["continuous_hyper_parameter_ranges"])
                check_type(argname="argument integer_hyper_parameter_ranges", value=integer_hyper_parameter_ranges, expected_type=type_hints["integer_hyper_parameter_ranges"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if categorical_hyper_parameter_ranges is not None:
                self._values["categorical_hyper_parameter_ranges"] = categorical_hyper_parameter_ranges
            if continuous_hyper_parameter_ranges is not None:
                self._values["continuous_hyper_parameter_ranges"] = continuous_hyper_parameter_ranges
            if integer_hyper_parameter_ranges is not None:
                self._values["integer_hyper_parameter_ranges"] = integer_hyper_parameter_ranges

        @builtins.property
        def categorical_hyper_parameter_ranges(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.CategoricalHyperParameterRangeProperty"]]]]:
            '''``CfnSolution.AlgorithmHyperParameterRangesProperty.CategoricalHyperParameterRanges``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-algorithmhyperparameterranges.html#cfn-personalize-solution-algorithmhyperparameterranges-categoricalhyperparameterranges
            '''
            result = self._values.get("categorical_hyper_parameter_ranges")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.CategoricalHyperParameterRangeProperty"]]]], result)

        @builtins.property
        def continuous_hyper_parameter_ranges(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.ContinuousHyperParameterRangeProperty"]]]]:
            '''``CfnSolution.AlgorithmHyperParameterRangesProperty.ContinuousHyperParameterRanges``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-algorithmhyperparameterranges.html#cfn-personalize-solution-algorithmhyperparameterranges-continuoushyperparameterranges
            '''
            result = self._values.get("continuous_hyper_parameter_ranges")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.ContinuousHyperParameterRangeProperty"]]]], result)

        @builtins.property
        def integer_hyper_parameter_ranges(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.IntegerHyperParameterRangeProperty"]]]]:
            '''``CfnSolution.AlgorithmHyperParameterRangesProperty.IntegerHyperParameterRanges``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-algorithmhyperparameterranges.html#cfn-personalize-solution-algorithmhyperparameterranges-integerhyperparameterranges
            '''
            result = self._values.get("integer_hyper_parameter_ranges")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.IntegerHyperParameterRangeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlgorithmHyperParameterRangesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnSolution.AutoMLConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"metric_name": "metricName", "recipe_list": "recipeList"},
    )
    class AutoMLConfigProperty:
        def __init__(
            self,
            *,
            metric_name: typing.Optional[builtins.str] = None,
            recipe_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''When the solution performs AutoML ( ``performAutoML`` is true in `CreateSolution <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateSolution.html>`_ ), Amazon Personalize determines which recipe, from the specified list, optimizes the given metric. Amazon Personalize then uses that recipe for the solution.

            :param metric_name: The metric to optimize.
            :param recipe_list: The list of candidate recipes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-automlconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                auto_mLConfig_property = personalize.CfnSolution.AutoMLConfigProperty(
                    metric_name="metricName",
                    recipe_list=["recipeList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90186f72416b9ffe73e6213229b57867a4cb3761d563ab39d66fc049664aea0c)
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument recipe_list", value=recipe_list, expected_type=type_hints["recipe_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if recipe_list is not None:
                self._values["recipe_list"] = recipe_list

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The metric to optimize.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-automlconfig.html#cfn-personalize-solution-automlconfig-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recipe_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of candidate recipes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-automlconfig.html#cfn-personalize-solution-automlconfig-recipelist
            '''
            result = self._values.get("recipe_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoMLConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnSolution.CategoricalHyperParameterRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "values": "values"},
    )
    class CategoricalHyperParameterRangeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the name and range of a categorical hyperparameter.

            :param name: The name of the hyperparameter.
            :param values: A list of the categories for the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-categoricalhyperparameterrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                categorical_hyper_parameter_range_property = personalize.CfnSolution.CategoricalHyperParameterRangeProperty(
                    name="name",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__500fec2aacb17db446ba751a423003b910f521d801f76733b2d366d973402b4e)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-categoricalhyperparameterrange.html#cfn-personalize-solution-categoricalhyperparameterrange-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of the categories for the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-categoricalhyperparameterrange.html#cfn-personalize-solution-categoricalhyperparameterrange-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CategoricalHyperParameterRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnSolution.ContinuousHyperParameterRangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_value": "maxValue",
            "min_value": "minValue",
            "name": "name",
        },
    )
    class ContinuousHyperParameterRangeProperty:
        def __init__(
            self,
            *,
            max_value: typing.Optional[jsii.Number] = None,
            min_value: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the name and range of a continuous hyperparameter.

            :param max_value: The maximum allowable value for the hyperparameter.
            :param min_value: The minimum allowable value for the hyperparameter.
            :param name: The name of the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-continuoushyperparameterrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                continuous_hyper_parameter_range_property = personalize.CfnSolution.ContinuousHyperParameterRangeProperty(
                    max_value=123,
                    min_value=123,
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee27a55fba38740547f4fc1b0c86893e1c6602463255b3003ccd65d30ef52d57)
                check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
                check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_value is not None:
                self._values["max_value"] = max_value
            if min_value is not None:
                self._values["min_value"] = min_value
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def max_value(self) -> typing.Optional[jsii.Number]:
            '''The maximum allowable value for the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-continuoushyperparameterrange.html#cfn-personalize-solution-continuoushyperparameterrange-maxvalue
            '''
            result = self._values.get("max_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_value(self) -> typing.Optional[jsii.Number]:
            '''The minimum allowable value for the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-continuoushyperparameterrange.html#cfn-personalize-solution-continuoushyperparameterrange-minvalue
            '''
            result = self._values.get("min_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-continuoushyperparameterrange.html#cfn-personalize-solution-continuoushyperparameterrange-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContinuousHyperParameterRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnSolution.HpoConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm_hyper_parameter_ranges": "algorithmHyperParameterRanges",
            "hpo_objective": "hpoObjective",
            "hpo_resource_config": "hpoResourceConfig",
        },
    )
    class HpoConfigProperty:
        def __init__(
            self,
            *,
            algorithm_hyper_parameter_ranges: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSolution.AlgorithmHyperParameterRangesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hpo_objective: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSolution.HpoObjectiveProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hpo_resource_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSolution.HpoResourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the properties for hyperparameter optimization (HPO).

            :param algorithm_hyper_parameter_ranges: The hyperparameters and their allowable ranges.
            :param hpo_objective: The metric to optimize during HPO. .. epigraph:: Amazon Personalize doesn't support configuring the ``hpoObjective`` at this time.
            :param hpo_resource_config: Describes the resource configuration for HPO.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hpoconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                hpo_config_property = personalize.CfnSolution.HpoConfigProperty(
                    algorithm_hyper_parameter_ranges=personalize.CfnSolution.AlgorithmHyperParameterRangesProperty(
                        categorical_hyper_parameter_ranges=[personalize.CfnSolution.CategoricalHyperParameterRangeProperty(
                            name="name",
                            values=["values"]
                        )],
                        continuous_hyper_parameter_ranges=[personalize.CfnSolution.ContinuousHyperParameterRangeProperty(
                            max_value=123,
                            min_value=123,
                            name="name"
                        )],
                        integer_hyper_parameter_ranges=[personalize.CfnSolution.IntegerHyperParameterRangeProperty(
                            max_value=123,
                            min_value=123,
                            name="name"
                        )]
                    ),
                    hpo_objective=personalize.CfnSolution.HpoObjectiveProperty(
                        metric_name="metricName",
                        metric_regex="metricRegex",
                        type="type"
                    ),
                    hpo_resource_config=personalize.CfnSolution.HpoResourceConfigProperty(
                        max_number_of_training_jobs="maxNumberOfTrainingJobs",
                        max_parallel_training_jobs="maxParallelTrainingJobs"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6513c6ebefc651aa6b073c740e3d4a16cf85e8f4d6f7ed82f486144c315ae88d)
                check_type(argname="argument algorithm_hyper_parameter_ranges", value=algorithm_hyper_parameter_ranges, expected_type=type_hints["algorithm_hyper_parameter_ranges"])
                check_type(argname="argument hpo_objective", value=hpo_objective, expected_type=type_hints["hpo_objective"])
                check_type(argname="argument hpo_resource_config", value=hpo_resource_config, expected_type=type_hints["hpo_resource_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if algorithm_hyper_parameter_ranges is not None:
                self._values["algorithm_hyper_parameter_ranges"] = algorithm_hyper_parameter_ranges
            if hpo_objective is not None:
                self._values["hpo_objective"] = hpo_objective
            if hpo_resource_config is not None:
                self._values["hpo_resource_config"] = hpo_resource_config

        @builtins.property
        def algorithm_hyper_parameter_ranges(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.AlgorithmHyperParameterRangesProperty"]]:
            '''The hyperparameters and their allowable ranges.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hpoconfig.html#cfn-personalize-solution-hpoconfig-algorithmhyperparameterranges
            '''
            result = self._values.get("algorithm_hyper_parameter_ranges")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.AlgorithmHyperParameterRangesProperty"]], result)

        @builtins.property
        def hpo_objective(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.HpoObjectiveProperty"]]:
            '''The metric to optimize during HPO.

            .. epigraph::

               Amazon Personalize doesn't support configuring the ``hpoObjective`` at this time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hpoconfig.html#cfn-personalize-solution-hpoconfig-hpoobjective
            '''
            result = self._values.get("hpo_objective")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.HpoObjectiveProperty"]], result)

        @builtins.property
        def hpo_resource_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.HpoResourceConfigProperty"]]:
            '''Describes the resource configuration for HPO.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hpoconfig.html#cfn-personalize-solution-hpoconfig-hporesourceconfig
            '''
            result = self._values.get("hpo_resource_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSolution.HpoResourceConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HpoConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnSolution.HpoObjectiveProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric_name": "metricName",
            "metric_regex": "metricRegex",
            "type": "type",
        },
    )
    class HpoObjectiveProperty:
        def __init__(
            self,
            *,
            metric_name: typing.Optional[builtins.str] = None,
            metric_regex: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The metric to optimize during hyperparameter optimization (HPO).

            .. epigraph::

               Amazon Personalize doesn't support configuring the ``hpoObjective`` at this time.

            :param metric_name: The name of the metric.
            :param metric_regex: A regular expression for finding the metric in the training job logs.
            :param type: The type of the metric. Valid values are ``Maximize`` and ``Minimize`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hpoobjective.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                hpo_objective_property = personalize.CfnSolution.HpoObjectiveProperty(
                    metric_name="metricName",
                    metric_regex="metricRegex",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf5739e4547deb30036092613e73431ae25b9bcd3ad8ba62b7e2a461d8b06c3c)
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument metric_regex", value=metric_regex, expected_type=type_hints["metric_regex"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if metric_regex is not None:
                self._values["metric_regex"] = metric_regex
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hpoobjective.html#cfn-personalize-solution-hpoobjective-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_regex(self) -> typing.Optional[builtins.str]:
            '''A regular expression for finding the metric in the training job logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hpoobjective.html#cfn-personalize-solution-hpoobjective-metricregex
            '''
            result = self._values.get("metric_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the metric.

            Valid values are ``Maximize`` and ``Minimize`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hpoobjective.html#cfn-personalize-solution-hpoobjective-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HpoObjectiveProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnSolution.HpoResourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_number_of_training_jobs": "maxNumberOfTrainingJobs",
            "max_parallel_training_jobs": "maxParallelTrainingJobs",
        },
    )
    class HpoResourceConfigProperty:
        def __init__(
            self,
            *,
            max_number_of_training_jobs: typing.Optional[builtins.str] = None,
            max_parallel_training_jobs: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the resource configuration for hyperparameter optimization (HPO).

            :param max_number_of_training_jobs: The maximum number of training jobs when you create a solution version. The maximum value for ``maxNumberOfTrainingJobs`` is ``40`` .
            :param max_parallel_training_jobs: The maximum number of parallel training jobs when you create a solution version. The maximum value for ``maxParallelTrainingJobs`` is ``10`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hporesourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                hpo_resource_config_property = personalize.CfnSolution.HpoResourceConfigProperty(
                    max_number_of_training_jobs="maxNumberOfTrainingJobs",
                    max_parallel_training_jobs="maxParallelTrainingJobs"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afc5d4d65fe3756bc98b0b1d0e2e81ecb199ef550dfc585b38e3462859bcf704)
                check_type(argname="argument max_number_of_training_jobs", value=max_number_of_training_jobs, expected_type=type_hints["max_number_of_training_jobs"])
                check_type(argname="argument max_parallel_training_jobs", value=max_parallel_training_jobs, expected_type=type_hints["max_parallel_training_jobs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_number_of_training_jobs is not None:
                self._values["max_number_of_training_jobs"] = max_number_of_training_jobs
            if max_parallel_training_jobs is not None:
                self._values["max_parallel_training_jobs"] = max_parallel_training_jobs

        @builtins.property
        def max_number_of_training_jobs(self) -> typing.Optional[builtins.str]:
            '''The maximum number of training jobs when you create a solution version.

            The maximum value for ``maxNumberOfTrainingJobs`` is ``40`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hporesourceconfig.html#cfn-personalize-solution-hporesourceconfig-maxnumberoftrainingjobs
            '''
            result = self._values.get("max_number_of_training_jobs")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_parallel_training_jobs(self) -> typing.Optional[builtins.str]:
            '''The maximum number of parallel training jobs when you create a solution version.

            The maximum value for ``maxParallelTrainingJobs`` is ``10`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-hporesourceconfig.html#cfn-personalize-solution-hporesourceconfig-maxparalleltrainingjobs
            '''
            result = self._values.get("max_parallel_training_jobs")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HpoResourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnSolution.IntegerHyperParameterRangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_value": "maxValue",
            "min_value": "minValue",
            "name": "name",
        },
    )
    class IntegerHyperParameterRangeProperty:
        def __init__(
            self,
            *,
            max_value: typing.Optional[jsii.Number] = None,
            min_value: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the name and range of an integer-valued hyperparameter.

            :param max_value: The maximum allowable value for the hyperparameter.
            :param min_value: The minimum allowable value for the hyperparameter.
            :param name: The name of the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-integerhyperparameterrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                integer_hyper_parameter_range_property = personalize.CfnSolution.IntegerHyperParameterRangeProperty(
                    max_value=123,
                    min_value=123,
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__55f0636c98a472f966b1d55aa073079aadae425f38abee9aa42254929614261b)
                check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
                check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_value is not None:
                self._values["max_value"] = max_value
            if min_value is not None:
                self._values["min_value"] = min_value
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def max_value(self) -> typing.Optional[jsii.Number]:
            '''The maximum allowable value for the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-integerhyperparameterrange.html#cfn-personalize-solution-integerhyperparameterrange-maxvalue
            '''
            result = self._values.get("max_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_value(self) -> typing.Optional[jsii.Number]:
            '''The minimum allowable value for the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-integerhyperparameterrange.html#cfn-personalize-solution-integerhyperparameterrange-minvalue
            '''
            result = self._values.get("min_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the hyperparameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-integerhyperparameterrange.html#cfn-personalize-solution-integerhyperparameterrange-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntegerHyperParameterRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-personalize.CfnSolution.SolutionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm_hyper_parameters": "algorithmHyperParameters",
            "auto_ml_config": "autoMlConfig",
            "event_value_threshold": "eventValueThreshold",
            "feature_transformation_parameters": "featureTransformationParameters",
            "hpo_config": "hpoConfig",
        },
    )
    class SolutionConfigProperty:
        def __init__(
            self,
            *,
            algorithm_hyper_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            auto_ml_config: typing.Any = None,
            event_value_threshold: typing.Optional[builtins.str] = None,
            feature_transformation_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            hpo_config: typing.Any = None,
        ) -> None:
            '''Describes the configuration properties for the solution.

            :param algorithm_hyper_parameters: Lists the hyperparameter names and ranges.
            :param auto_ml_config: The `AutoMLConfig <https://docs.aws.amazon.com/personalize/latest/dg/API_AutoMLConfig.html>`_ object containing a list of recipes to search when AutoML is performed.
            :param event_value_threshold: Only events with a value greater than or equal to this threshold are used for training a model.
            :param feature_transformation_parameters: Lists the feature transformation parameters.
            :param hpo_config: Describes the properties for hyperparameter optimization (HPO).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_personalize as personalize
                
                # auto_ml_config: Any
                # hpo_config: Any
                
                solution_config_property = personalize.CfnSolution.SolutionConfigProperty(
                    algorithm_hyper_parameters={
                        "algorithm_hyper_parameters_key": "algorithmHyperParameters"
                    },
                    auto_ml_config=auto_ml_config,
                    event_value_threshold="eventValueThreshold",
                    feature_transformation_parameters={
                        "feature_transformation_parameters_key": "featureTransformationParameters"
                    },
                    hpo_config=hpo_config
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eef584a0e3f5641014c597b963aa241739f1f6e903d9ab5b22b34d949c41f129)
                check_type(argname="argument algorithm_hyper_parameters", value=algorithm_hyper_parameters, expected_type=type_hints["algorithm_hyper_parameters"])
                check_type(argname="argument auto_ml_config", value=auto_ml_config, expected_type=type_hints["auto_ml_config"])
                check_type(argname="argument event_value_threshold", value=event_value_threshold, expected_type=type_hints["event_value_threshold"])
                check_type(argname="argument feature_transformation_parameters", value=feature_transformation_parameters, expected_type=type_hints["feature_transformation_parameters"])
                check_type(argname="argument hpo_config", value=hpo_config, expected_type=type_hints["hpo_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if algorithm_hyper_parameters is not None:
                self._values["algorithm_hyper_parameters"] = algorithm_hyper_parameters
            if auto_ml_config is not None:
                self._values["auto_ml_config"] = auto_ml_config
            if event_value_threshold is not None:
                self._values["event_value_threshold"] = event_value_threshold
            if feature_transformation_parameters is not None:
                self._values["feature_transformation_parameters"] = feature_transformation_parameters
            if hpo_config is not None:
                self._values["hpo_config"] = hpo_config

        @builtins.property
        def algorithm_hyper_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''Lists the hyperparameter names and ranges.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html#cfn-personalize-solution-solutionconfig-algorithmhyperparameters
            '''
            result = self._values.get("algorithm_hyper_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def auto_ml_config(self) -> typing.Any:
            '''The `AutoMLConfig <https://docs.aws.amazon.com/personalize/latest/dg/API_AutoMLConfig.html>`_ object containing a list of recipes to search when AutoML is performed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html#cfn-personalize-solution-solutionconfig-automlconfig
            '''
            result = self._values.get("auto_ml_config")
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_value_threshold(self) -> typing.Optional[builtins.str]:
            '''Only events with a value greater than or equal to this threshold are used for training a model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html#cfn-personalize-solution-solutionconfig-eventvaluethreshold
            '''
            result = self._values.get("event_value_threshold")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def feature_transformation_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''Lists the feature transformation parameters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html#cfn-personalize-solution-solutionconfig-featuretransformationparameters
            '''
            result = self._values.get("feature_transformation_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def hpo_config(self) -> typing.Any:
            '''Describes the properties for hyperparameter optimization (HPO).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html#cfn-personalize-solution-solutionconfig-hpoconfig
            '''
            result = self._values.get("hpo_config")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SolutionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-personalize.CfnSolutionProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_group_arn": "datasetGroupArn",
        "name": "name",
        "event_type": "eventType",
        "perform_auto_ml": "performAutoMl",
        "perform_hpo": "performHpo",
        "recipe_arn": "recipeArn",
        "solution_config": "solutionConfig",
    },
)
class CfnSolutionProps:
    def __init__(
        self,
        *,
        dataset_group_arn: builtins.str,
        name: builtins.str,
        event_type: typing.Optional[builtins.str] = None,
        perform_auto_ml: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        perform_hpo: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        recipe_arn: typing.Optional[builtins.str] = None,
        solution_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSolution.SolutionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSolution``.

        :param dataset_group_arn: The Amazon Resource Name (ARN) of the dataset group that provides the training data.
        :param name: The name of the solution.
        :param event_type: The event type (for example, 'click' or 'like') that is used for training the model. If no ``eventType`` is provided, Amazon Personalize uses all interactions for training with equal weight regardless of type.
        :param perform_auto_ml: .. epigraph:: We don't recommend enabling automated machine learning. Instead, match your use case to the available Amazon Personalize recipes. For more information, see `Determining your use case. <https://docs.aws.amazon.com/personalize/latest/dg/determining-use-case.html>`_ When true, Amazon Personalize performs a search for the best USER_PERSONALIZATION recipe from the list specified in the solution configuration ( ``recipeArn`` must not be specified). When false (the default), Amazon Personalize uses ``recipeArn`` for training.
        :param perform_hpo: Whether to perform hyperparameter optimization (HPO) on the chosen recipe. The default is ``false`` .
        :param recipe_arn: The ARN of the recipe used to create the solution.
        :param solution_config: Describes the configuration properties for the solution.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_personalize as personalize
            
            # auto_ml_config: Any
            # hpo_config: Any
            
            cfn_solution_props = personalize.CfnSolutionProps(
                dataset_group_arn="datasetGroupArn",
                name="name",
            
                # the properties below are optional
                event_type="eventType",
                perform_auto_ml=False,
                perform_hpo=False,
                recipe_arn="recipeArn",
                solution_config=personalize.CfnSolution.SolutionConfigProperty(
                    algorithm_hyper_parameters={
                        "algorithm_hyper_parameters_key": "algorithmHyperParameters"
                    },
                    auto_ml_config=auto_ml_config,
                    event_value_threshold="eventValueThreshold",
                    feature_transformation_parameters={
                        "feature_transformation_parameters_key": "featureTransformationParameters"
                    },
                    hpo_config=hpo_config
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c7b58f5d5153ecda3b74c657e3eebe16f61dfb4e52836e5cb63dde5cb511a8)
            check_type(argname="argument dataset_group_arn", value=dataset_group_arn, expected_type=type_hints["dataset_group_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument perform_auto_ml", value=perform_auto_ml, expected_type=type_hints["perform_auto_ml"])
            check_type(argname="argument perform_hpo", value=perform_hpo, expected_type=type_hints["perform_hpo"])
            check_type(argname="argument recipe_arn", value=recipe_arn, expected_type=type_hints["recipe_arn"])
            check_type(argname="argument solution_config", value=solution_config, expected_type=type_hints["solution_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_group_arn": dataset_group_arn,
            "name": name,
        }
        if event_type is not None:
            self._values["event_type"] = event_type
        if perform_auto_ml is not None:
            self._values["perform_auto_ml"] = perform_auto_ml
        if perform_hpo is not None:
            self._values["perform_hpo"] = perform_hpo
        if recipe_arn is not None:
            self._values["recipe_arn"] = recipe_arn
        if solution_config is not None:
            self._values["solution_config"] = solution_config

    @builtins.property
    def dataset_group_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the dataset group that provides the training data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-datasetgrouparn
        '''
        result = self._values.get("dataset_group_arn")
        assert result is not None, "Required property 'dataset_group_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the solution.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_type(self) -> typing.Optional[builtins.str]:
        '''The event type (for example, 'click' or 'like') that is used for training the model.

        If no ``eventType`` is provided, Amazon Personalize uses all interactions for training with equal weight regardless of type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-eventtype
        '''
        result = self._values.get("event_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def perform_auto_ml(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''.. epigraph::

   We don't recommend enabling automated machine learning.

        Instead, match your use case to the available Amazon Personalize recipes. For more information, see `Determining your use case. <https://docs.aws.amazon.com/personalize/latest/dg/determining-use-case.html>`_

        When true, Amazon Personalize performs a search for the best USER_PERSONALIZATION recipe from the list specified in the solution configuration ( ``recipeArn`` must not be specified). When false (the default), Amazon Personalize uses ``recipeArn`` for training.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-performautoml
        '''
        result = self._values.get("perform_auto_ml")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def perform_hpo(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Whether to perform hyperparameter optimization (HPO) on the chosen recipe.

        The default is ``false`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-performhpo
        '''
        result = self._values.get("perform_hpo")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def recipe_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the recipe used to create the solution.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-recipearn
        '''
        result = self._values.get("recipe_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def solution_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSolution.SolutionConfigProperty]]:
        '''Describes the configuration properties for the solution.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-solutionconfig
        '''
        result = self._values.get("solution_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSolution.SolutionConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSolutionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDataset",
    "CfnDatasetGroup",
    "CfnDatasetGroupProps",
    "CfnDatasetProps",
    "CfnSchema",
    "CfnSchemaProps",
    "CfnSolution",
    "CfnSolutionProps",
]

publication.publish()

def _typecheckingstub__3cf8a77fa1b7db6041ca39dead952a3e5ec0ec6fc35eb62d778644fab1b7055b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    dataset_group_arn: builtins.str,
    dataset_type: builtins.str,
    name: builtins.str,
    schema_arn: builtins.str,
    dataset_import_job: typing.Optional[typing.Union[typing.Union[CfnDataset.DatasetImportJobProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af0e90f73eaf1361e0d2ebcbf41fbe9db7bab230bde5fce1111d306b228cbc1(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2713723c8ab7065fd2b992587a76c65203bc626ee3529dc5a10e21a586f0c352(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97904bb0fb2491f211dcfb8e236c6e809a82631eaaf8debd2af366362a01c21f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7fc14414585bc0a054dc333f4606a903d6f5fbecb2c7e3481ea72585caba5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0a67ecfdfb636659d74ce66f322419f0f7c0315d282cb3182336071b1d4134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b186e2244b8f85f981897989d8b81c4ff3d7f54c74051522c43816c8b197b1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c7a168946676fa588824e81f36f5953a9ed70bf8b30c03553a45d35bb2c807(
    value: typing.Optional[typing.Union[CfnDataset.DatasetImportJobProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0278f363afc7be1112c8c382047c98436642405aaccd13ebe291d00bb649fe(
    *,
    data_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e07de0dac3bcb21f154d56a6a433353f817f690b98f4f45184c9d1a6aa4b4d(
    *,
    dataset_arn: typing.Optional[builtins.str] = None,
    dataset_import_job_arn: typing.Optional[builtins.str] = None,
    data_source: typing.Any = None,
    job_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3570de5b03a449c0fe5332ece68bcd4620b6005e3bd51336cbc0fa9d9878120b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f78a2507f6e1b5217b383a7e13c885e6925ed21645961415ec2b3f32017c11(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233244d6671c11b7b169853dfde07077d704f69cf2663ccf0405f04fd8a31994(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fed7ca2ec87d06e0938a3a2524b77d7950b64593718aef55c4d9e3dda189773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86162b7b06bae8240d77ef03b5be62f4bbf6b8d65c73a4456959c88bbd20d5f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9482a37792b59b25afa0e3476a273f2ab8a403925f240e59c305faed0b9e3059(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76dc70f48959b8901aa004ad7e2ee8fd46d0afe0fec8835639dc332f82699cf7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b648503a401f01beb6222bd0af27c00da9fd299ee3ccb0a80daebda23992e79e(
    *,
    name: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170e5421c2620440ae17a8534108beb32b93cdce31b718c033d4cb7edcbbad21(
    *,
    dataset_group_arn: builtins.str,
    dataset_type: builtins.str,
    name: builtins.str,
    schema_arn: builtins.str,
    dataset_import_job: typing.Optional[typing.Union[typing.Union[CfnDataset.DatasetImportJobProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d802b29f1eccb88439ff9a65f27618ed36c1cbc2b0460bb3029e2667a372d0(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    schema: builtins.str,
    domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0b17267f31a927139c3c3c9762139e8cbf023dfad58d2dc3b73e1ff473536e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9a8b2451663454255f294f6e043d87ee3e6af2d3c0fe69cc13433f7d669d88(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17aa1472f054b84e09afdc3e92157aa9e4a4ccaf7850a26679daf7e149b3a8e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef3c8f772c75e7741afb9ccef31f1531dcaea2a0f5b8a8ddf5a3e7c8f2f6a36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98eed33aae5f80e7898feea11c83f68515f563b6b7b317622b3e5815433a4864(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638695462e4fea7e98eadcd53399f6eac00fef9aafa80dbc7fdd2c19dd0f9ef9(
    *,
    name: builtins.str,
    schema: builtins.str,
    domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc347588a2a8e0ad6e70dcbe0c4e0d2c19221c579d86f463e795c5d497072b3(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    dataset_group_arn: builtins.str,
    name: builtins.str,
    event_type: typing.Optional[builtins.str] = None,
    perform_auto_ml: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    perform_hpo: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    recipe_arn: typing.Optional[builtins.str] = None,
    solution_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSolution.SolutionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d7c7501db412a48d5ced091a1edf2ddac962d488281b796bc2af839347640d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee39e6d7cb53570c24fc29413a2e45eafae85804521b6239244557343837b97e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a025e7521524110cbe3dae051fdcdd12c614408d7ba516f5beeb5a91ce97098(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbd3962d59115ec758487e726cedaee192da1ed1a703c4c5b9ff896bf2630fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c6b75aa2ea86be2592ef9a07f55af9feb33092345831fff4738214cbdce72c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63af310ef2a950c148ffc1654d2d382bec929942560b47d339475ec0124e9507(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ab3b11cdef1d6b1ec9d39fa9ddcdacf2630404f1c1e4fb72d1bfa3d40c4cbb(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be20be8f1b831141405634c45196b6662e45fc5101c70e5d49e3f3e107155236(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f61df265d3ee9ece087763f8c166789fd17565a6e580515d1410d70c235655(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSolution.SolutionConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27409c42888b8dd7b13ce15077a2531ed1b0f73b29148d0d779dab6d6adfba6f(
    *,
    categorical_hyper_parameter_ranges: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSolution.CategoricalHyperParameterRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    continuous_hyper_parameter_ranges: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSolution.ContinuousHyperParameterRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    integer_hyper_parameter_ranges: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSolution.IntegerHyperParameterRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90186f72416b9ffe73e6213229b57867a4cb3761d563ab39d66fc049664aea0c(
    *,
    metric_name: typing.Optional[builtins.str] = None,
    recipe_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500fec2aacb17db446ba751a423003b910f521d801f76733b2d366d973402b4e(
    *,
    name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee27a55fba38740547f4fc1b0c86893e1c6602463255b3003ccd65d30ef52d57(
    *,
    max_value: typing.Optional[jsii.Number] = None,
    min_value: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6513c6ebefc651aa6b073c740e3d4a16cf85e8f4d6f7ed82f486144c315ae88d(
    *,
    algorithm_hyper_parameter_ranges: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSolution.AlgorithmHyperParameterRangesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hpo_objective: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSolution.HpoObjectiveProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hpo_resource_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSolution.HpoResourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5739e4547deb30036092613e73431ae25b9bcd3ad8ba62b7e2a461d8b06c3c(
    *,
    metric_name: typing.Optional[builtins.str] = None,
    metric_regex: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc5d4d65fe3756bc98b0b1d0e2e81ecb199ef550dfc585b38e3462859bcf704(
    *,
    max_number_of_training_jobs: typing.Optional[builtins.str] = None,
    max_parallel_training_jobs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f0636c98a472f966b1d55aa073079aadae425f38abee9aa42254929614261b(
    *,
    max_value: typing.Optional[jsii.Number] = None,
    min_value: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef584a0e3f5641014c597b963aa241739f1f6e903d9ab5b22b34d949c41f129(
    *,
    algorithm_hyper_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    auto_ml_config: typing.Any = None,
    event_value_threshold: typing.Optional[builtins.str] = None,
    feature_transformation_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    hpo_config: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c7b58f5d5153ecda3b74c657e3eebe16f61dfb4e52836e5cb63dde5cb511a8(
    *,
    dataset_group_arn: builtins.str,
    name: builtins.str,
    event_type: typing.Optional[builtins.str] = None,
    perform_auto_ml: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    perform_hpo: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    recipe_arn: typing.Optional[builtins.str] = None,
    solution_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSolution.SolutionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
