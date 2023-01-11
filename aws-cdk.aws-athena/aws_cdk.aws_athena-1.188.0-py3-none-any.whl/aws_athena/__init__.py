'''
# Amazon Athena Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_athena as athena
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Athena construct libraries](https://constructs.dev/search?q=athena)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Athena resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Athena.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Athena](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Athena.html).

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
class CfnDataCatalog(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-athena.CfnDataCatalog",
):
    '''A CloudFormation ``AWS::Athena::DataCatalog``.

    The AWS::Athena::DataCatalog resource specifies an Amazon Athena data catalog, which contains a name, description, type, parameters, and tags. For more information, see `DataCatalog <https://docs.aws.amazon.com/athena/latest/APIReference/API_DataCatalog.html>`_ in the *Amazon Athena API Reference* .

    :cloudformationResource: AWS::Athena::DataCatalog
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_athena as athena
        
        cfn_data_catalog = athena.CfnDataCatalog(self, "MyCfnDataCatalog",
            name="name",
            type="type",
        
            # the properties below are optional
            description="description",
            parameters={
                "parameters_key": "parameters"
            },
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
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_core_f4b25747.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Athena::DataCatalog``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the data catalog. The catalog name must be unique for the AWS account and can use a maximum of 128 alphanumeric, underscore, at sign, or hyphen characters.
        :param type: The type of data catalog: ``LAMBDA`` for a federated catalog, ``GLUE`` for AWS Glue Catalog, or ``HIVE`` for an external hive metastore.
        :param description: A description of the data catalog.
        :param parameters: Specifies the Lambda function or functions to use for the data catalog. The mapping used depends on the catalog type. - The ``HIVE`` data catalog type uses the following syntax. The ``metadata-function`` parameter is required. ``The sdk-version`` parameter is optional and defaults to the currently supported version. ``metadata-function= *lambda_arn* , sdk-version= *version_number*`` - The ``LAMBDA`` data catalog type uses one of the following sets of required parameters, but not both. - When one Lambda function processes metadata and another Lambda function reads data, the following syntax is used. Both parameters are required. ``metadata-function= *lambda_arn* , record-function= *lambda_arn*`` - A composite Lambda function that processes both metadata and data uses the following syntax. ``function= *lambda_arn*`` - The ``GLUE`` type takes a catalog ID parameter and is required. The ``*catalog_id*`` is the account ID of the AWS account to which the Glue catalog belongs. ``catalog-id= *catalog_id*`` - The ``GLUE`` data catalog type also applies to the default ``AwsDataCatalog`` that already exists in your account, of which you can have only one and cannot modify. - Queries that specify a GLUE data catalog other than the default ``AwsDataCatalog`` must be run on Athena engine version 2. - In Regions where Athena engine version 2 is not available, creating new GLUE data catalogs results in an ``INVALID_INPUT`` error.
        :param tags: The tags (key-value pairs) to associate with this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9629b1ed5ce76b06d349b123752ad27b08002cb6151e19d9187f037c00ea8a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDataCatalogProps(
            name=name,
            type=type,
            description=description,
            parameters=parameters,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a554efb0ccf8a0963ad36bdf03a8d2d339b0be943494a3db10099a102fa14e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6613f67534203de197328f4b67a6e2843a445115c9902df21a653923f380bef1)
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags (key-value pairs) to associate with this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the data catalog.

        The catalog name must be unique for the AWS account and can use a maximum of 128 alphanumeric, underscore, at sign, or hyphen characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0bee152e2ac4b06ade7320a7278ad89af4718974314d02952490645ee5f6e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of data catalog: ``LAMBDA`` for a federated catalog, ``GLUE`` for AWS Glue Catalog, or ``HIVE`` for an external hive metastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc92272d8e384d77b7cb27dc83f7c5699e6505abd596f413695824a5f63efee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the data catalog.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a51219f15807edf23e3c21823b9293350c05b0d4ee0d7f5a0cfa527a829ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        '''Specifies the Lambda function or functions to use for the data catalog.

        The mapping used depends on the catalog type.

        - The ``HIVE`` data catalog type uses the following syntax. The ``metadata-function`` parameter is required. ``The sdk-version`` parameter is optional and defaults to the currently supported version.

        ``metadata-function= *lambda_arn* , sdk-version= *version_number*``

        - The ``LAMBDA`` data catalog type uses one of the following sets of required parameters, but not both.
        - When one Lambda function processes metadata and another Lambda function reads data, the following syntax is used. Both parameters are required.

        ``metadata-function= *lambda_arn* , record-function= *lambda_arn*``

        - A composite Lambda function that processes both metadata and data uses the following syntax.

        ``function= *lambda_arn*``

        - The ``GLUE`` type takes a catalog ID parameter and is required. The ``*catalog_id*`` is the account ID of the AWS account to which the Glue catalog belongs.

        ``catalog-id= *catalog_id*``

        - The ``GLUE`` data catalog type also applies to the default ``AwsDataCatalog`` that already exists in your account, of which you can have only one and cannot modify.
        - Queries that specify a GLUE data catalog other than the default ``AwsDataCatalog`` must be run on Athena engine version 2.
        - In Regions where Athena engine version 2 is not available, creating new GLUE data catalogs results in an ``INVALID_INPUT`` error.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-parameters
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__322b30a0d7ffe4f32f913c3a7494cd77c556303de3d80b1ca2648b97e774c092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-athena.CfnDataCatalogProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "description": "description",
        "parameters": "parameters",
        "tags": "tags",
    },
)
class CfnDataCatalogProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_core_f4b25747.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDataCatalog``.

        :param name: The name of the data catalog. The catalog name must be unique for the AWS account and can use a maximum of 128 alphanumeric, underscore, at sign, or hyphen characters.
        :param type: The type of data catalog: ``LAMBDA`` for a federated catalog, ``GLUE`` for AWS Glue Catalog, or ``HIVE`` for an external hive metastore.
        :param description: A description of the data catalog.
        :param parameters: Specifies the Lambda function or functions to use for the data catalog. The mapping used depends on the catalog type. - The ``HIVE`` data catalog type uses the following syntax. The ``metadata-function`` parameter is required. ``The sdk-version`` parameter is optional and defaults to the currently supported version. ``metadata-function= *lambda_arn* , sdk-version= *version_number*`` - The ``LAMBDA`` data catalog type uses one of the following sets of required parameters, but not both. - When one Lambda function processes metadata and another Lambda function reads data, the following syntax is used. Both parameters are required. ``metadata-function= *lambda_arn* , record-function= *lambda_arn*`` - A composite Lambda function that processes both metadata and data uses the following syntax. ``function= *lambda_arn*`` - The ``GLUE`` type takes a catalog ID parameter and is required. The ``*catalog_id*`` is the account ID of the AWS account to which the Glue catalog belongs. ``catalog-id= *catalog_id*`` - The ``GLUE`` data catalog type also applies to the default ``AwsDataCatalog`` that already exists in your account, of which you can have only one and cannot modify. - Queries that specify a GLUE data catalog other than the default ``AwsDataCatalog`` must be run on Athena engine version 2. - In Regions where Athena engine version 2 is not available, creating new GLUE data catalogs results in an ``INVALID_INPUT`` error.
        :param tags: The tags (key-value pairs) to associate with this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_athena as athena
            
            cfn_data_catalog_props = athena.CfnDataCatalogProps(
                name="name",
                type="type",
            
                # the properties below are optional
                description="description",
                parameters={
                    "parameters_key": "parameters"
                },
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5391b8af13484e587649f404116f3a7c538b02685af2429dd4b8dd3f78480410)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the data catalog.

        The catalog name must be unique for the AWS account and can use a maximum of 128 alphanumeric, underscore, at sign, or hyphen characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of data catalog: ``LAMBDA`` for a federated catalog, ``GLUE`` for AWS Glue Catalog, or ``HIVE`` for an external hive metastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the data catalog.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies the Lambda function or functions to use for the data catalog.

        The mapping used depends on the catalog type.

        - The ``HIVE`` data catalog type uses the following syntax. The ``metadata-function`` parameter is required. ``The sdk-version`` parameter is optional and defaults to the currently supported version.

        ``metadata-function= *lambda_arn* , sdk-version= *version_number*``

        - The ``LAMBDA`` data catalog type uses one of the following sets of required parameters, but not both.
        - When one Lambda function processes metadata and another Lambda function reads data, the following syntax is used. Both parameters are required.

        ``metadata-function= *lambda_arn* , record-function= *lambda_arn*``

        - A composite Lambda function that processes both metadata and data uses the following syntax.

        ``function= *lambda_arn*``

        - The ``GLUE`` type takes a catalog ID parameter and is required. The ``*catalog_id*`` is the account ID of the AWS account to which the Glue catalog belongs.

        ``catalog-id= *catalog_id*``

        - The ``GLUE`` data catalog type also applies to the default ``AwsDataCatalog`` that already exists in your account, of which you can have only one and cannot modify.
        - Queries that specify a GLUE data catalog other than the default ``AwsDataCatalog`` must be run on Athena engine version 2.
        - In Regions where Athena engine version 2 is not available, creating new GLUE data catalogs results in an ``INVALID_INPUT`` error.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags (key-value pairs) to associate with this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataCatalogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnNamedQuery(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-athena.CfnNamedQuery",
):
    '''A CloudFormation ``AWS::Athena::NamedQuery``.

    The ``AWS::Athena::NamedQuery`` resource specifies an Amazon Athena saved query, where ``QueryString`` contains the SQL query statements that make up the query.

    :cloudformationResource: AWS::Athena::NamedQuery
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_athena as athena
        
        cfn_named_query = athena.CfnNamedQuery(self, "MyCfnNamedQuery",
            database="database",
            query_string="queryString",
        
            # the properties below are optional
            description="description",
            name="name",
            work_group="workGroup"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        database: builtins.str,
        query_string: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        work_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Athena::NamedQuery``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database: The database to which the query belongs.
        :param query_string: The SQL statements that make up the query.
        :param description: The query description.
        :param name: The query name.
        :param work_group: The name of the workgroup that contains the named query.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6a5f41e435a68d330dc6cf34c81270ad09a1a9d22534ea1b3cad9c3a61cb41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNamedQueryProps(
            database=database,
            query_string=query_string,
            description=description,
            name=name,
            work_group=work_group,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7672eb6497741aae3b4096950b68071b33b130339fc49d88820506ab54fc001a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bee7d973558cc017b0c603e43fa26c9ba9db5737693abf9cb4a2d176c36637b9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrNamedQueryId")
    def attr_named_query_id(self) -> builtins.str:
        '''The unique ID of the query.

        :cloudformationAttribute: NamedQueryId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNamedQueryId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        '''The database to which the query belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database
        '''
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187d1fb5c54449ed3a2cba78ae0c54efb1038fa3fa111443d9bff771171d575d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value)

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        '''The SQL statements that make up the query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-querystring
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c17eb421cceeea7b8a9c209ad6aeacf56044d8a14fbf59f3c6a76205956f246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The query description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88f0455144a827615f100e95765f452bb42003be6c2c5d151c1a54ed09f7e36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The query name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa850e292bd7d014d0c1750a1e5c2212ff03fd5736a77c3cd8c0a3b57935b58e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="workGroup")
    def work_group(self) -> typing.Optional[builtins.str]:
        '''The name of the workgroup that contains the named query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-workgroup
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workGroup"))

    @work_group.setter
    def work_group(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c32c33126b3d16c5840a31c4f3da1d954964f761596d9e4338ad1c8fb9cc4d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workGroup", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-athena.CfnNamedQueryProps",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "query_string": "queryString",
        "description": "description",
        "name": "name",
        "work_group": "workGroup",
    },
)
class CfnNamedQueryProps:
    def __init__(
        self,
        *,
        database: builtins.str,
        query_string: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        work_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnNamedQuery``.

        :param database: The database to which the query belongs.
        :param query_string: The SQL statements that make up the query.
        :param description: The query description.
        :param name: The query name.
        :param work_group: The name of the workgroup that contains the named query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_athena as athena
            
            cfn_named_query_props = athena.CfnNamedQueryProps(
                database="database",
                query_string="queryString",
            
                # the properties below are optional
                description="description",
                name="name",
                work_group="workGroup"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492a98f9db0ea11674733422b52ce91e2d538e18ece4ba6371c38e65d65c111a)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument work_group", value=work_group, expected_type=type_hints["work_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "query_string": query_string,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if work_group is not None:
            self._values["work_group"] = work_group

    @builtins.property
    def database(self) -> builtins.str:
        '''The database to which the query belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query_string(self) -> builtins.str:
        '''The SQL statements that make up the query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-querystring
        '''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The query description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The query name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def work_group(self) -> typing.Optional[builtins.str]:
        '''The name of the workgroup that contains the named query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-workgroup
        '''
        result = self._values.get("work_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNamedQueryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPreparedStatement(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-athena.CfnPreparedStatement",
):
    '''A CloudFormation ``AWS::Athena::PreparedStatement``.

    Specifies a prepared statement for use with SQL queries in Athena.

    :cloudformationResource: AWS::Athena::PreparedStatement
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_athena as athena
        
        cfn_prepared_statement = athena.CfnPreparedStatement(self, "MyCfnPreparedStatement",
            query_statement="queryStatement",
            statement_name="statementName",
            work_group="workGroup",
        
            # the properties below are optional
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        query_statement: builtins.str,
        statement_name: builtins.str,
        work_group: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Athena::PreparedStatement``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param query_statement: The query string for the prepared statement.
        :param statement_name: The name of the prepared statement.
        :param work_group: The workgroup to which the prepared statement belongs.
        :param description: The description of the prepared statement.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f9a0d60d83b896925ae654eb4518b0874a376768ee3776c178e986b37e510b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPreparedStatementProps(
            query_statement=query_statement,
            statement_name=statement_name,
            work_group=work_group,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785da83b2107db4b2862d207c17d7be80ed1c1fe2bd50adafa664102b04d1bff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d29c1af4bac7f3b867dcbc14b7d1e352d3ce8b043e5d603e5d92eb1b6ce11a9)
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
    @jsii.member(jsii_name="queryStatement")
    def query_statement(self) -> builtins.str:
        '''The query string for the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-querystatement
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryStatement"))

    @query_statement.setter
    def query_statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e269d49f2c1dc4547bebe2243513595e06861dd66b90d8aec0249c7a28633b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStatement", value)

    @builtins.property
    @jsii.member(jsii_name="statementName")
    def statement_name(self) -> builtins.str:
        '''The name of the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-statementname
        '''
        return typing.cast(builtins.str, jsii.get(self, "statementName"))

    @statement_name.setter
    def statement_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5442af524459c8fd63faa36684112531ef970551c03fa7d3ad89f763ecf1cf14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementName", value)

    @builtins.property
    @jsii.member(jsii_name="workGroup")
    def work_group(self) -> builtins.str:
        '''The workgroup to which the prepared statement belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-workgroup
        '''
        return typing.cast(builtins.str, jsii.get(self, "workGroup"))

    @work_group.setter
    def work_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913887e9083182548145f510d6af94881fcffab5403a5071c376f058f1761861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workGroup", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35810fe787f3db92b09553a4196cd55f13992bcffb5f3897e26351a853015535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-athena.CfnPreparedStatementProps",
    jsii_struct_bases=[],
    name_mapping={
        "query_statement": "queryStatement",
        "statement_name": "statementName",
        "work_group": "workGroup",
        "description": "description",
    },
)
class CfnPreparedStatementProps:
    def __init__(
        self,
        *,
        query_statement: builtins.str,
        statement_name: builtins.str,
        work_group: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnPreparedStatement``.

        :param query_statement: The query string for the prepared statement.
        :param statement_name: The name of the prepared statement.
        :param work_group: The workgroup to which the prepared statement belongs.
        :param description: The description of the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_athena as athena
            
            cfn_prepared_statement_props = athena.CfnPreparedStatementProps(
                query_statement="queryStatement",
                statement_name="statementName",
                work_group="workGroup",
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811bcd8d104b96bfede7d655a3ca274743deac91573e318135d9d202500e0a0d)
            check_type(argname="argument query_statement", value=query_statement, expected_type=type_hints["query_statement"])
            check_type(argname="argument statement_name", value=statement_name, expected_type=type_hints["statement_name"])
            check_type(argname="argument work_group", value=work_group, expected_type=type_hints["work_group"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query_statement": query_statement,
            "statement_name": statement_name,
            "work_group": work_group,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def query_statement(self) -> builtins.str:
        '''The query string for the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-querystatement
        '''
        result = self._values.get("query_statement")
        assert result is not None, "Required property 'query_statement' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def statement_name(self) -> builtins.str:
        '''The name of the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-statementname
        '''
        result = self._values.get("statement_name")
        assert result is not None, "Required property 'statement_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def work_group(self) -> builtins.str:
        '''The workgroup to which the prepared statement belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-workgroup
        '''
        result = self._values.get("work_group")
        assert result is not None, "Required property 'work_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the prepared statement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPreparedStatementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnWorkGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-athena.CfnWorkGroup",
):
    '''A CloudFormation ``AWS::Athena::WorkGroup``.

    The AWS::Athena::WorkGroup resource specifies an Amazon Athena workgroup, which contains a name, description, creation time, state, and other configuration, listed under ``WorkGroupConfiguration`` . Each workgroup enables you to isolate queries for you or your group from other queries in the same account. For more information, see `CreateWorkGroup <https://docs.aws.amazon.com/athena/latest/APIReference/API_CreateWorkGroup.html>`_ in the *Amazon Athena API Reference* .

    :cloudformationResource: AWS::Athena::WorkGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_athena as athena
        
        cfn_work_group = athena.CfnWorkGroup(self, "MyCfnWorkGroup",
            name="name",
        
            # the properties below are optional
            description="description",
            recursive_delete_option=False,
            state="state",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                bytes_scanned_cutoff_per_query=123,
                enforce_work_group_configuration=False,
                engine_version=athena.CfnWorkGroup.EngineVersionProperty(
                    effective_engine_version="effectiveEngineVersion",
                    selected_engine_version="selectedEngineVersion"
                ),
                publish_cloud_watch_metrics_enabled=False,
                requester_pays_enabled=False,
                result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                    encryption_configuration=athena.CfnWorkGroup.EncryptionConfigurationProperty(
                        encryption_option="encryptionOption",
        
                        # the properties below are optional
                        kms_key="kmsKey"
                    ),
                    output_location="outputLocation"
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        recursive_delete_option: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        work_group_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWorkGroup.WorkGroupConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Athena::WorkGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The workgroup name.
        :param description: The workgroup description.
        :param recursive_delete_option: The option to delete a workgroup and its contents even if the workgroup contains any named queries. The default is false.
        :param state: The state of the workgroup: ENABLED or DISABLED.
        :param tags: The tags (key-value pairs) to associate with this resource.
        :param work_group_configuration: The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified. The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082a138a2a88094b56dfc838124211e9e6c51500a48fd8f40a625c49bee1d90a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkGroupProps(
            name=name,
            description=description,
            recursive_delete_option=recursive_delete_option,
            state=state,
            tags=tags,
            work_group_configuration=work_group_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1c8f74df3016fe98461a50ec2cec21af139158fd00d7793b30bf852483179c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__602ca4d0b3ac911028658f8b4d2a0ca637503c02ca350531b16124c7d083704a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time the workgroup was created, as a UNIX timestamp in seconds.

        For example: ``1582761016`` .

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrWorkGroupConfigurationEngineVersionEffectiveEngineVersion")
    def attr_work_group_configuration_engine_version_effective_engine_version(
        self,
    ) -> builtins.str:
        '''
        :cloudformationAttribute: WorkGroupConfiguration.EngineVersion.EffectiveEngineVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrWorkGroupConfigurationEngineVersionEffectiveEngineVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags (key-value pairs) to associate with this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The workgroup name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e6730bd6d041a7524a4e1f9ee3fec88e904adfe7e76920e28adfccde08654f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The workgroup description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e09d39190ce21646e6d7bae543b5b1a41bfefea08a66f93c7da4338776061620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="recursiveDeleteOption")
    def recursive_delete_option(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The option to delete a workgroup and its contents even if the workgroup contains any named queries.

        The default is false.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-recursivedeleteoption
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "recursiveDeleteOption"))

    @recursive_delete_option.setter
    def recursive_delete_option(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d961b1373b5bfb7c97c45308ed56a50c36d8077cd44f29f197b26cfb9e3fcdd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recursiveDeleteOption", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the workgroup: ENABLED or DISABLED.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11f3f8e81143487ca3d3ce026a9657d351a8b601d3973644af1b7b35bd5a928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @builtins.property
    @jsii.member(jsii_name="workGroupConfiguration")
    def work_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkGroup.WorkGroupConfigurationProperty"]]:
        '''The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified.

        The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-workgroupconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkGroup.WorkGroupConfigurationProperty"]], jsii.get(self, "workGroupConfiguration"))

    @work_group_configuration.setter
    def work_group_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkGroup.WorkGroupConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77fd64433b9ba526acbae6c557a40626ca0d5302c2afce6013287e04c0ae226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workGroupConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-athena.CfnWorkGroup.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_option": "encryptionOption", "kms_key": "kmsKey"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_option: builtins.str,
            kms_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE_KMS`` or ``CSE_KMS`` ) and key information.

            :param encryption_option: Indicates whether Amazon S3 server-side encryption with Amazon S3-managed keys ( ``SSE_S3`` ), server-side encryption with KMS-managed keys ( ``SSE_KMS`` ), or client-side encryption with KMS-managed keys ( ``CSE_KMS`` ) is used. If a query runs in a workgroup and the workgroup overrides client-side settings, then the workgroup's setting for encryption is used. It specifies whether query results must be encrypted, for all queries that run in this workgroup.
            :param kms_key: For ``SSE_KMS`` and ``CSE_KMS`` , this is the KMS key ARN or ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_athena as athena
                
                encryption_configuration_property = athena.CfnWorkGroup.EncryptionConfigurationProperty(
                    encryption_option="encryptionOption",
                
                    # the properties below are optional
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a29b981aa183612144f567fb1b856c62071fd055d40ae1d2e2b840efe43adac)
                check_type(argname="argument encryption_option", value=encryption_option, expected_type=type_hints["encryption_option"])
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "encryption_option": encryption_option,
            }
            if kms_key is not None:
                self._values["kms_key"] = kms_key

        @builtins.property
        def encryption_option(self) -> builtins.str:
            '''Indicates whether Amazon S3 server-side encryption with Amazon S3-managed keys ( ``SSE_S3`` ), server-side encryption with KMS-managed keys ( ``SSE_KMS`` ), or client-side encryption with KMS-managed keys ( ``CSE_KMS`` ) is used.

            If a query runs in a workgroup and the workgroup overrides client-side settings, then the workgroup's setting for encryption is used. It specifies whether query results must be encrypted, for all queries that run in this workgroup.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html#cfn-athena-workgroup-encryptionconfiguration-encryptionoption
            '''
            result = self._values.get("encryption_option")
            assert result is not None, "Required property 'encryption_option' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''For ``SSE_KMS`` and ``CSE_KMS`` , this is the KMS key ARN or ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html#cfn-athena-workgroup-encryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-athena.CfnWorkGroup.EngineVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "effective_engine_version": "effectiveEngineVersion",
            "selected_engine_version": "selectedEngineVersion",
        },
    )
    class EngineVersionProperty:
        def __init__(
            self,
            *,
            effective_engine_version: typing.Optional[builtins.str] = None,
            selected_engine_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Athena engine version for running queries, or the PySpark engine version for running sessions.

            :param effective_engine_version: Read only. The engine version on which the query runs. If the user requests a valid engine version other than Auto, the effective engine version is the same as the engine version that the user requested. If the user requests Auto, the effective engine version is chosen by Athena. When a request to update the engine version is made by a ``CreateWorkGroup`` or ``UpdateWorkGroup`` operation, the ``EffectiveEngineVersion`` field is ignored.
            :param selected_engine_version: The engine version requested by the user. Possible values are determined by the output of ``ListEngineVersions`` , including AUTO. The default is AUTO.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_athena as athena
                
                engine_version_property = athena.CfnWorkGroup.EngineVersionProperty(
                    effective_engine_version="effectiveEngineVersion",
                    selected_engine_version="selectedEngineVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__68b53c3b99e62289ff4e9f63e2d6f216bd7606542e2ac2ad53030956fc155ed7)
                check_type(argname="argument effective_engine_version", value=effective_engine_version, expected_type=type_hints["effective_engine_version"])
                check_type(argname="argument selected_engine_version", value=selected_engine_version, expected_type=type_hints["selected_engine_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if effective_engine_version is not None:
                self._values["effective_engine_version"] = effective_engine_version
            if selected_engine_version is not None:
                self._values["selected_engine_version"] = selected_engine_version

        @builtins.property
        def effective_engine_version(self) -> typing.Optional[builtins.str]:
            '''Read only.

            The engine version on which the query runs. If the user requests a valid engine version other than Auto, the effective engine version is the same as the engine version that the user requested. If the user requests Auto, the effective engine version is chosen by Athena. When a request to update the engine version is made by a ``CreateWorkGroup`` or ``UpdateWorkGroup`` operation, the ``EffectiveEngineVersion`` field is ignored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineversion.html#cfn-athena-workgroup-engineversion-effectiveengineversion
            '''
            result = self._values.get("effective_engine_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def selected_engine_version(self) -> typing.Optional[builtins.str]:
            '''The engine version requested by the user.

            Possible values are determined by the output of ``ListEngineVersions`` , including AUTO. The default is AUTO.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineversion.html#cfn-athena-workgroup-engineversion-selectedengineversion
            '''
            result = self._values.get("selected_engine_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EngineVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-athena.CfnWorkGroup.ResultConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_configuration": "encryptionConfiguration",
            "output_location": "outputLocation",
        },
    )
    class ResultConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWorkGroup.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            output_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The location in Amazon S3 where query results are stored and the encryption option, if any, used for query results.

            These are known as "client-side settings". If workgroup settings override client-side settings, then the query uses the workgroup settings.

            :param encryption_configuration: If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE_KMS`` or ``CSE_KMS`` ) and key information. This is a client-side setting. If workgroup settings override client-side settings, then the query uses the encryption configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` and `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .
            :param output_location: The location in Amazon S3 where your query results are stored, such as ``s3://path/to/query/bucket/`` . To run a query, you must specify the query results location using either a client-side setting for individual queries or a location specified by the workgroup. If workgroup settings override client-side settings, then the query uses the location specified for the workgroup. If no query location is set, Athena issues an error. For more information, see `Working with Query Results, Output Files, and Query History <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ and ``EnforceWorkGroupConfiguration`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_athena as athena
                
                result_configuration_property = athena.CfnWorkGroup.ResultConfigurationProperty(
                    encryption_configuration=athena.CfnWorkGroup.EncryptionConfigurationProperty(
                        encryption_option="encryptionOption",
                
                        # the properties below are optional
                        kms_key="kmsKey"
                    ),
                    output_location="outputLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2990999a03f1997dd4ce098ec12e9e5f054cff5bc648be68784dcb98d379c2e)
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if output_location is not None:
                self._values["output_location"] = output_location

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkGroup.EncryptionConfigurationProperty"]]:
            '''If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE_KMS`` or ``CSE_KMS`` ) and key information.

            This is a client-side setting. If workgroup settings override client-side settings, then the query uses the encryption configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` and `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkGroup.EncryptionConfigurationProperty"]], result)

        @builtins.property
        def output_location(self) -> typing.Optional[builtins.str]:
            '''The location in Amazon S3 where your query results are stored, such as ``s3://path/to/query/bucket/`` .

            To run a query, you must specify the query results location using either a client-side setting for individual queries or a location specified by the workgroup. If workgroup settings override client-side settings, then the query uses the location specified for the workgroup. If no query location is set, Athena issues an error. For more information, see `Working with Query Results, Output Files, and Query History <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ and ``EnforceWorkGroupConfiguration`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-outputlocation
            '''
            result = self._values.get("output_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResultConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-athena.CfnWorkGroup.WorkGroupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bytes_scanned_cutoff_per_query": "bytesScannedCutoffPerQuery",
            "enforce_work_group_configuration": "enforceWorkGroupConfiguration",
            "engine_version": "engineVersion",
            "publish_cloud_watch_metrics_enabled": "publishCloudWatchMetricsEnabled",
            "requester_pays_enabled": "requesterPaysEnabled",
            "result_configuration": "resultConfiguration",
        },
    )
    class WorkGroupConfigurationProperty:
        def __init__(
            self,
            *,
            bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
            enforce_work_group_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            engine_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWorkGroup.EngineVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            publish_cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            result_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWorkGroup.ResultConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified.

            The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.

            :param bytes_scanned_cutoff_per_query: The upper limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan. No default is defined. .. epigraph:: This property currently supports integer types. Support for long values is planned.
            :param enforce_work_group_configuration: If set to "true", the settings for the workgroup override client-side settings. If set to "false", client-side settings are used. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .
            :param engine_version: The engine version that all queries running on the workgroup use. Queries on the ``AmazonAthenaPreviewFunctionality`` workgroup run on the preview engine regardless of this setting.
            :param publish_cloud_watch_metrics_enabled: Indicates that the Amazon CloudWatch metrics are enabled for the workgroup.
            :param requester_pays_enabled: If set to ``true`` , allows members assigned to a workgroup to reference Amazon S3 Requester Pays buckets in queries. If set to ``false`` , workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error. The default is ``false`` . For more information about Requester Pays buckets, see `Requester Pays Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html>`_ in the *Amazon Simple Storage Service Developer Guide* .
            :param result_configuration: Specifies the location in Amazon S3 where query results are stored and the encryption option, if any, used for query results. For more information, see `Working with Query Results, Output Files, and Query History <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_athena as athena
                
                work_group_configuration_property = athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                    bytes_scanned_cutoff_per_query=123,
                    enforce_work_group_configuration=False,
                    engine_version=athena.CfnWorkGroup.EngineVersionProperty(
                        effective_engine_version="effectiveEngineVersion",
                        selected_engine_version="selectedEngineVersion"
                    ),
                    publish_cloud_watch_metrics_enabled=False,
                    requester_pays_enabled=False,
                    result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                        encryption_configuration=athena.CfnWorkGroup.EncryptionConfigurationProperty(
                            encryption_option="encryptionOption",
                
                            # the properties below are optional
                            kms_key="kmsKey"
                        ),
                        output_location="outputLocation"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9a8c9b5dc0d543787f2596c22ec02a788e419ba270c18374b84c81fe12b1b8d)
                check_type(argname="argument bytes_scanned_cutoff_per_query", value=bytes_scanned_cutoff_per_query, expected_type=type_hints["bytes_scanned_cutoff_per_query"])
                check_type(argname="argument enforce_work_group_configuration", value=enforce_work_group_configuration, expected_type=type_hints["enforce_work_group_configuration"])
                check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
                check_type(argname="argument publish_cloud_watch_metrics_enabled", value=publish_cloud_watch_metrics_enabled, expected_type=type_hints["publish_cloud_watch_metrics_enabled"])
                check_type(argname="argument requester_pays_enabled", value=requester_pays_enabled, expected_type=type_hints["requester_pays_enabled"])
                check_type(argname="argument result_configuration", value=result_configuration, expected_type=type_hints["result_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bytes_scanned_cutoff_per_query is not None:
                self._values["bytes_scanned_cutoff_per_query"] = bytes_scanned_cutoff_per_query
            if enforce_work_group_configuration is not None:
                self._values["enforce_work_group_configuration"] = enforce_work_group_configuration
            if engine_version is not None:
                self._values["engine_version"] = engine_version
            if publish_cloud_watch_metrics_enabled is not None:
                self._values["publish_cloud_watch_metrics_enabled"] = publish_cloud_watch_metrics_enabled
            if requester_pays_enabled is not None:
                self._values["requester_pays_enabled"] = requester_pays_enabled
            if result_configuration is not None:
                self._values["result_configuration"] = result_configuration

        @builtins.property
        def bytes_scanned_cutoff_per_query(self) -> typing.Optional[jsii.Number]:
            '''The upper limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan.

            No default is defined.
            .. epigraph::

               This property currently supports integer types. Support for long values is planned.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-bytesscannedcutoffperquery
            '''
            result = self._values.get("bytes_scanned_cutoff_per_query")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enforce_work_group_configuration(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If set to "true", the settings for the workgroup override client-side settings.

            If set to "false", client-side settings are used. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-enforceworkgroupconfiguration
            '''
            result = self._values.get("enforce_work_group_configuration")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def engine_version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkGroup.EngineVersionProperty"]]:
            '''The engine version that all queries running on the workgroup use.

            Queries on the ``AmazonAthenaPreviewFunctionality`` workgroup run on the preview engine regardless of this setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-engineversion
            '''
            result = self._values.get("engine_version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkGroup.EngineVersionProperty"]], result)

        @builtins.property
        def publish_cloud_watch_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates that the Amazon CloudWatch metrics are enabled for the workgroup.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-publishcloudwatchmetricsenabled
            '''
            result = self._values.get("publish_cloud_watch_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def requester_pays_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If set to ``true`` , allows members assigned to a workgroup to reference Amazon S3 Requester Pays buckets in queries.

            If set to ``false`` , workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error. The default is ``false`` . For more information about Requester Pays buckets, see `Requester Pays Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html>`_ in the *Amazon Simple Storage Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-requesterpaysenabled
            '''
            result = self._values.get("requester_pays_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def result_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkGroup.ResultConfigurationProperty"]]:
            '''Specifies the location in Amazon S3 where query results are stored and the encryption option, if any, used for query results.

            For more information, see `Working with Query Results, Output Files, and Query History <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-resultconfiguration
            '''
            result = self._values.get("result_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkGroup.ResultConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkGroupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-athena.CfnWorkGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "recursive_delete_option": "recursiveDeleteOption",
        "state": "state",
        "tags": "tags",
        "work_group_configuration": "workGroupConfiguration",
    },
)
class CfnWorkGroupProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        recursive_delete_option: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        work_group_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWorkGroup.WorkGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkGroup``.

        :param name: The workgroup name.
        :param description: The workgroup description.
        :param recursive_delete_option: The option to delete a workgroup and its contents even if the workgroup contains any named queries. The default is false.
        :param state: The state of the workgroup: ENABLED or DISABLED.
        :param tags: The tags (key-value pairs) to associate with this resource.
        :param work_group_configuration: The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified. The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_athena as athena
            
            cfn_work_group_props = athena.CfnWorkGroupProps(
                name="name",
            
                # the properties below are optional
                description="description",
                recursive_delete_option=False,
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                    bytes_scanned_cutoff_per_query=123,
                    enforce_work_group_configuration=False,
                    engine_version=athena.CfnWorkGroup.EngineVersionProperty(
                        effective_engine_version="effectiveEngineVersion",
                        selected_engine_version="selectedEngineVersion"
                    ),
                    publish_cloud_watch_metrics_enabled=False,
                    requester_pays_enabled=False,
                    result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                        encryption_configuration=athena.CfnWorkGroup.EncryptionConfigurationProperty(
                            encryption_option="encryptionOption",
            
                            # the properties below are optional
                            kms_key="kmsKey"
                        ),
                        output_location="outputLocation"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7439c04cb8e804e3d065957ea9686adff86ec714a22ab95d5d8e054185906df6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument recursive_delete_option", value=recursive_delete_option, expected_type=type_hints["recursive_delete_option"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument work_group_configuration", value=work_group_configuration, expected_type=type_hints["work_group_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if recursive_delete_option is not None:
            self._values["recursive_delete_option"] = recursive_delete_option
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags
        if work_group_configuration is not None:
            self._values["work_group_configuration"] = work_group_configuration

    @builtins.property
    def name(self) -> builtins.str:
        '''The workgroup name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The workgroup description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recursive_delete_option(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The option to delete a workgroup and its contents even if the workgroup contains any named queries.

        The default is false.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-recursivedeleteoption
        '''
        result = self._values.get("recursive_delete_option")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the workgroup: ENABLED or DISABLED.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags (key-value pairs) to associate with this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def work_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWorkGroup.WorkGroupConfigurationProperty]]:
        '''The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified.

        The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-workgroupconfiguration
        '''
        result = self._values.get("work_group_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWorkGroup.WorkGroupConfigurationProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDataCatalog",
    "CfnDataCatalogProps",
    "CfnNamedQuery",
    "CfnNamedQueryProps",
    "CfnPreparedStatement",
    "CfnPreparedStatementProps",
    "CfnWorkGroup",
    "CfnWorkGroupProps",
]

publication.publish()

def _typecheckingstub__ed9629b1ed5ce76b06d349b123752ad27b08002cb6151e19d9187f037c00ea8a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_core_f4b25747.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a554efb0ccf8a0963ad36bdf03a8d2d339b0be943494a3db10099a102fa14e3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6613f67534203de197328f4b67a6e2843a445115c9902df21a653923f380bef1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bee152e2ac4b06ade7320a7278ad89af4718974314d02952490645ee5f6e99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc92272d8e384d77b7cb27dc83f7c5699e6505abd596f413695824a5f63efee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a51219f15807edf23e3c21823b9293350c05b0d4ee0d7f5a0cfa527a829ff3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322b30a0d7ffe4f32f913c3a7494cd77c556303de3d80b1ca2648b97e774c092(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5391b8af13484e587649f404116f3a7c538b02685af2429dd4b8dd3f78480410(
    *,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_core_f4b25747.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6a5f41e435a68d330dc6cf34c81270ad09a1a9d22534ea1b3cad9c3a61cb41(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    database: builtins.str,
    query_string: builtins.str,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    work_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7672eb6497741aae3b4096950b68071b33b130339fc49d88820506ab54fc001a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee7d973558cc017b0c603e43fa26c9ba9db5737693abf9cb4a2d176c36637b9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187d1fb5c54449ed3a2cba78ae0c54efb1038fa3fa111443d9bff771171d575d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c17eb421cceeea7b8a9c209ad6aeacf56044d8a14fbf59f3c6a76205956f246(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f0455144a827615f100e95765f452bb42003be6c2c5d151c1a54ed09f7e36c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa850e292bd7d014d0c1750a1e5c2212ff03fd5736a77c3cd8c0a3b57935b58e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c32c33126b3d16c5840a31c4f3da1d954964f761596d9e4338ad1c8fb9cc4d7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492a98f9db0ea11674733422b52ce91e2d538e18ece4ba6371c38e65d65c111a(
    *,
    database: builtins.str,
    query_string: builtins.str,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    work_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f9a0d60d83b896925ae654eb4518b0874a376768ee3776c178e986b37e510b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    query_statement: builtins.str,
    statement_name: builtins.str,
    work_group: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785da83b2107db4b2862d207c17d7be80ed1c1fe2bd50adafa664102b04d1bff(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d29c1af4bac7f3b867dcbc14b7d1e352d3ce8b043e5d603e5d92eb1b6ce11a9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e269d49f2c1dc4547bebe2243513595e06861dd66b90d8aec0249c7a28633b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5442af524459c8fd63faa36684112531ef970551c03fa7d3ad89f763ecf1cf14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913887e9083182548145f510d6af94881fcffab5403a5071c376f058f1761861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35810fe787f3db92b09553a4196cd55f13992bcffb5f3897e26351a853015535(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811bcd8d104b96bfede7d655a3ca274743deac91573e318135d9d202500e0a0d(
    *,
    query_statement: builtins.str,
    statement_name: builtins.str,
    work_group: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082a138a2a88094b56dfc838124211e9e6c51500a48fd8f40a625c49bee1d90a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    recursive_delete_option: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    work_group_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWorkGroup.WorkGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1c8f74df3016fe98461a50ec2cec21af139158fd00d7793b30bf852483179c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602ca4d0b3ac911028658f8b4d2a0ca637503c02ca350531b16124c7d083704a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e6730bd6d041a7524a4e1f9ee3fec88e904adfe7e76920e28adfccde08654f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09d39190ce21646e6d7bae543b5b1a41bfefea08a66f93c7da4338776061620(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d961b1373b5bfb7c97c45308ed56a50c36d8077cd44f29f197b26cfb9e3fcdd3(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11f3f8e81143487ca3d3ce026a9657d351a8b601d3973644af1b7b35bd5a928(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77fd64433b9ba526acbae6c557a40626ca0d5302c2afce6013287e04c0ae226(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWorkGroup.WorkGroupConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a29b981aa183612144f567fb1b856c62071fd055d40ae1d2e2b840efe43adac(
    *,
    encryption_option: builtins.str,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b53c3b99e62289ff4e9f63e2d6f216bd7606542e2ac2ad53030956fc155ed7(
    *,
    effective_engine_version: typing.Optional[builtins.str] = None,
    selected_engine_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2990999a03f1997dd4ce098ec12e9e5f054cff5bc648be68784dcb98d379c2e(
    *,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWorkGroup.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    output_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a8c9b5dc0d543787f2596c22ec02a788e419ba270c18374b84c81fe12b1b8d(
    *,
    bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
    enforce_work_group_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    engine_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWorkGroup.EngineVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    result_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWorkGroup.ResultConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7439c04cb8e804e3d065957ea9686adff86ec714a22ab95d5d8e054185906df6(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    recursive_delete_option: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    work_group_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWorkGroup.WorkGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
