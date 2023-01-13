'''
# AWS Glue Library

The `@cdk-extensions/glue` module contains configurations for AWS Glue.

```python
import * as glue from 'cdk-extensions/glue';
```

## Objective

The Glue module is used to consolidate data from multiple different sources into a single location to simplify analysis and review. It provides the ability to discover and organize data from a wide variety of sources; tranform, prepare and clean that data for analysis; and the creation of data pipelines to deliver the prepared data for storage and analysis and monitor the process.

The AWS Glue Catalog is used to orchestrate the operation based on using metadata stored in its tables which define the sources and targets it should operate on. Crawlers are added to the Glue Catalog which allow access to the data sources and target, providing information on data changes which need to be acted upon. Jobs are then configured to perform the transformation of that data for delivery to its target location. Scheduling of these jobs can then be configured to either run at specific times, based off of triggering events or performed manually.

## Important Constructs

### Catalog

The Catalog construct defines the Glue Catalog that will hold metadata and act as the source for orchestrating all Glue Jobs

### Table

The Table construct holds the table definition within the Glue Catalog which contains the necessary metadata for performing Glue jobs

### Crawler

The Crawler construct contains the information defining a source of data, including the necessary information or credentials to reach and access it.

### Jobs

The Jobs construct contains the instructions to perform transformation and delivery of the crawled data.

### Trigger

The Trigger construct defines what triggers should be used to run a particular job.

### Workflow

The Workflow construct contains a collection of Triggers and Jobs to link together a set of processes into a complete data pipeline.
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

import aws_cdk
import aws_cdk.aws_ec2
import aws_cdk.aws_events
import aws_cdk.aws_glue
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_logs
import aws_cdk.aws_s3
import constructs


class BookmarkConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.BookmarkConfiguration",
):
    '''Controls the bookmark state of a Glue job.

    :see: `Using job bookmarks in AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html#monitor-continuations-implement>`_
    '''

    @jsii.member(jsii_name="disable")
    @builtins.classmethod
    def disable(cls) -> "BookmarkConfiguration":
        '''Job bookmarks are not used, and the job always processes the entire dataset.

        You are responsible for managing the output from previous job
        runs.

        :return: A configuration object that disabled job bookmarks.
        '''
        return typing.cast("BookmarkConfiguration", jsii.sinvoke(cls, "disable", []))

    @jsii.member(jsii_name="enable")
    @builtins.classmethod
    def enable(cls) -> "BookmarkConfiguration":
        '''Causes the job to update the state after a run to keep track of previously processed data.

        If your job has a source with job bookmark support, it
        will keep track of processed data, and when a job runs, it processes new
        data since the last checkpoint.

        :return: A configuration object that enables job bookmarks.
        '''
        return typing.cast("BookmarkConfiguration", jsii.sinvoke(cls, "enable", []))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        value: builtins.str,
        *,
        from_: builtins.str,
        to: builtins.str,
    ) -> "BookmarkConfiguration":
        '''An escape hatch method that allows specifying arbitrary values for the ``job-bookmark-option`` argument of a Glue job.

        :param value: The value to pass to the ``job-bookmark-option`` argument.
        :param from_: The run ID which represents all the input that was processed until the last successful run before and including the specified run ID. The corresponding input is ignored.
        :param to: The run ID which represents all the input that was processed until the last successful run before and including the specified run ID. The corresponding input excluding the input identified by the {@link BookmarkRange.from | from} is processed by the job. Any input later than this input is also excluded for processing.

        :return: A configuration object that represents the provided bookmark configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BookmarkConfiguration.of)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        range = BookmarkRange(from_=from_, to=to)

        return typing.cast("BookmarkConfiguration", jsii.sinvoke(cls, "of", [value, range]))

    @jsii.member(jsii_name="pause")
    @builtins.classmethod
    def pause(cls, *, from_: builtins.str, to: builtins.str) -> "BookmarkConfiguration":
        '''Process incremental data since the last successful run or the data in a specified range, without updating the state of last bookmark.

        You are
        responsible for managing the output from previous job runs.

        :param from_: The run ID which represents all the input that was processed until the last successful run before and including the specified run ID. The corresponding input is ignored.
        :param to: The run ID which represents all the input that was processed until the last successful run before and including the specified run ID. The corresponding input excluding the input identified by the {@link BookmarkRange.from | from} is processed by the job. Any input later than this input is also excluded for processing.

        :return: A configuration object that pauses job bookmarks.
        '''
        range = BookmarkRange(from_=from_, to=to)

        return typing.cast("BookmarkConfiguration", jsii.sinvoke(cls, "pause", [range]))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''The value to pass to the ``job-bookmark-option`` argument.'''
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> typing.Optional["BookmarkRange"]:
        '''An optional range of job ID's that will correspond to the ``job-bookmark-from`` and ``job-bookmark-to`` arguments.'''
        return typing.cast(typing.Optional["BookmarkRange"], jsii.get(self, "range"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.BookmarkRange",
    jsii_struct_bases=[],
    name_mapping={"from_": "from", "to": "to"},
)
class BookmarkRange:
    def __init__(self, *, from_: builtins.str, to: builtins.str) -> None:
        '''A range of job run ID's that specify the job bookmark state of a Glue job which has had its bookmark state set to paused.

        :param from_: The run ID which represents all the input that was processed until the last successful run before and including the specified run ID. The corresponding input is ignored.
        :param to: The run ID which represents all the input that was processed until the last successful run before and including the specified run ID. The corresponding input excluding the input identified by the {@link BookmarkRange.from | from} is processed by the job. Any input later than this input is also excluded for processing.

        :see: `Using job bookmarks in AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html#monitor-continuations-implement>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BookmarkRange.__init__)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
        self._values: typing.Dict[str, typing.Any] = {
            "from_": from_,
            "to": to,
        }

    @builtins.property
    def from_(self) -> builtins.str:
        '''The run ID which represents all the input that was processed until the last successful run before and including the specified run ID.

        The
        corresponding input is ignored.
        '''
        result = self._values.get("from_")
        assert result is not None, "Required property 'from_' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The run ID which represents all the input that was processed until the last successful run before and including the specified run ID.

        The
        corresponding input excluding the input identified by the
        {@link BookmarkRange.from | from} is processed by the job. Any input later
        than this input is also excluded for processing.
        '''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BookmarkRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClassificationString(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.ClassificationString",
):
    '''Classification string given to tables with this data format.

    :see: https://docs.aws.amazon.com/glue/latest/dg/add-classifier.html#classifier-built-in
    '''

    def __init__(self, value: builtins.str) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ClassificationString.__init__)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [value])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVRO")
    def AVRO(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-avro
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "AVRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CSV")
    def CSV(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-csv
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "CSV"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="JSON")
    def JSON(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-json
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "JSON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORC")
    def ORC(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-orc
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "ORC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARQUET")
    def PARQUET(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-parquet
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "PARQUET"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="XML")
    def XML(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-xml
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "XML"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.CloudWatchEncryption",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "kms_key": "kmsKey"},
)
class CloudWatchEncryption:
    def __init__(
        self,
        *,
        mode: "CloudWatchEncryptionMode",
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        '''CloudWatch Logs encryption configuration.

        :param mode: Encryption mode.
        :param kms_key: The KMS key to be used to encrypt the data. Default: A key will be created if one is not provided.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudWatchEncryption.__init__)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "mode": mode,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def mode(self) -> "CloudWatchEncryptionMode":
        '''Encryption mode.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast("CloudWatchEncryptionMode", result)

    @builtins.property
    def kms_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''The KMS key to be used to encrypt the data.

        :default: A key will be created if one is not provided.
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.CloudWatchEncryptionMode")
class CloudWatchEncryptionMode(enum.Enum):
    '''Encryption mode for CloudWatch Logs.

    :see: https://docs.aws.amazon.com/glue/latest/webapi/API_CloudWatchEncryption.html#Glue-Type-CloudWatchEncryption-CloudWatchEncryptionMode
    '''

    KMS = "KMS"
    '''Server-side encryption (SSE) with an AWS KMS key managed by the account owner.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html
    '''


class Code(metaclass=jsii.JSIIAbstractClass, jsii_type="cdk-extensions.glue.Code"):
    '''Represents a Glue Job's Code assets (an asset can be a scripts, a jar, a python file or any other file).'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        path: builtins.str,
        *,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[aws_cdk.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[aws_cdk.BundlingOptions, typing.Dict[str, typing.Any]]] = None,
    ) -> "AssetCode":
        '''Job code from a local disk path.

        :param path: Code file (not a directory).
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Code.from_asset)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        options = aws_cdk.AssetOptions(
            asset_hash=asset_hash, asset_hash_type=asset_hash_type, bundling=bundling
        )

        return typing.cast("AssetCode", jsii.sinvoke(cls, "fromAsset", [path, options]))

    @jsii.member(jsii_name="fromBucket")
    @builtins.classmethod
    def from_bucket(cls, bucket: aws_cdk.aws_s3.IBucket, key: builtins.str) -> "S3Code":
        '''Job code as an S3 object.

        :param bucket: The S3 bucket.
        :param key: The object key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Code.from_bucket)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("S3Code", jsii.sinvoke(cls, "fromBucket", [bucket, key]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        scope: constructs.Construct,
        grantable: aws_cdk.aws_iam.IGrantable,
    ) -> "CodeConfig":
        '''Called when the Job is initialized to allow this object to bind.

        :param scope: -
        :param grantable: -
        '''
        ...


class _CodeProxy(Code):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.Construct,
        grantable: aws_cdk.aws_iam.IGrantable,
    ) -> "CodeConfig":
        '''Called when the Job is initialized to allow this object to bind.

        :param scope: -
        :param grantable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Code.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument grantable", value=grantable, expected_type=type_hints["grantable"])
        return typing.cast("CodeConfig", jsii.invoke(self, "bind", [scope, grantable]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Code).__jsii_proxy_class__ = lambda : _CodeProxy


@jsii.data_type(
    jsii_type="cdk-extensions.glue.CodeConfig",
    jsii_struct_bases=[],
    name_mapping={"s3_location": "s3Location"},
)
class CodeConfig:
    def __init__(
        self,
        *,
        s3_location: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
    ) -> None:
        '''Result of binding ``Code`` into a ``Job``.

        :param s3_location: The location of the code in S3.
        '''
        if isinstance(s3_location, dict):
            s3_location = aws_cdk.aws_s3.Location(**s3_location)
        if __debug__:
            type_hints = typing.get_type_hints(CodeConfig.__init__)
            check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
        self._values: typing.Dict[str, typing.Any] = {
            "s3_location": s3_location,
        }

    @builtins.property
    def s3_location(self) -> aws_cdk.aws_s3.Location:
        '''The location of the code in S3.'''
        result = self._values.get("s3_location")
        assert result is not None, "Required property 's3_location' is missing"
        return typing.cast(aws_cdk.aws_s3.Location, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Column(metaclass=jsii.JSIIAbstractClass, jsii_type="cdk-extensions.glue.Column"):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comment: 
        :param name: 
        '''
        props = ColumnProps(comment=comment, name=name)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_glue.CfnTable.ColumnProperty:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Column.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_glue.CfnTable.ColumnProperty, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="typeString")
    @abc.abstractmethod
    def type_string(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> typing.Optional[builtins.str]:
        '''A free-form text comment.

        :see: `AWS::Glue::Table Column <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-column.html#cfn-glue-table-column-comment>`_
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Column.

        :see: `AWS::Glue::Table Column <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-column.html#cfn-glue-table-column-name>`_
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))


class _ColumnProxy(Column):
    @builtins.property
    @jsii.member(jsii_name="typeString")
    def type_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeString"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Column).__jsii_proxy_class__ = lambda : _ColumnProxy


@jsii.data_type(
    jsii_type="cdk-extensions.glue.ColumnProps",
    jsii_struct_bases=[],
    name_mapping={"comment": "comment", "name": "name"},
)
class ColumnProps:
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comment: 
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ColumnProps.__init__)
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColumnProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.ConfigurationVersion")
class ConfigurationVersion(enum.Enum):
    V1_0 = "V1_0"


@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class Connection(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.Connection",
):
    '''Creates a resource specifying a Glue Connection to a data source.

    :see: `AWS::Glue::Connection <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html>`_
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        connection_type: "ConnectionType",
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the Connection class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param connection_type: The type of the connection.
        :param description: A description for the Connection.
        :param name: The name of the connection. Connection will not function as expected without a name.
        :param properties: List of Key/Value pairs defining the properties of the Connection.
        :param security_groups: Existing Security Group to assign to the Connection. If none is provided a new Security Group will be created.
        :param subnets: Options for selection of subnets from the VPC to attach to the Connection.
        :param vpc: VPC to attach to the Connection.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Connection.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConnectionProps(
            connection_type=connection_type,
            description=description,
            name=name,
            properties=properties,
            security_groups=security_groups,
            subnets=subnets,
            vpc=vpc,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addMatchCriteria")
    def add_match_criteria(self, value: builtins.str) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Connection.add_match_criteria)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addMatchCriteria", [value]))

    @jsii.member(jsii_name="addProperty")
    def add_property(self, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Connection.add_property)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addProperty", [key, value]))

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        '''The network connections associated with this resource.'''
        return typing.cast(aws_cdk.aws_ec2.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> "ConnectionType":
        '''{@link ConnectionProps.connectionType:}.'''
        return typing.cast("ConnectionType", jsii.get(self, "connectionType"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_glue.CfnConnection:
        return typing.cast(aws_cdk.aws_glue.CfnConnection, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[aws_cdk.aws_ec2.ISecurityGroup]:
        '''{@link ConnectionProps.securityGroups:}.'''
        return typing.cast(typing.List[aws_cdk.aws_ec2.ISecurityGroup], jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''{@link ConnectionProps.description}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''{@link ConnectionProps.name}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.SecurityGroup]:
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SecurityGroup], jsii.get(self, "securityGroup"))

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''{@link ConnectionProps.subnets}.'''
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], jsii.get(self, "subnets"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        '''{@link ConnectionProps.vpc}.'''
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.ConnectionProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "connection_type": "connectionType",
        "description": "description",
        "name": "name",
        "properties": "properties",
        "security_groups": "securityGroups",
        "subnets": "subnets",
        "vpc": "vpc",
    },
)
class ConnectionProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        connection_type: "ConnectionType",
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''Configuration for the Glue Workflow resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param connection_type: The type of the connection.
        :param description: A description for the Connection.
        :param name: The name of the connection. Connection will not function as expected without a name.
        :param properties: List of Key/Value pairs defining the properties of the Connection.
        :param security_groups: Existing Security Group to assign to the Connection. If none is provided a new Security Group will be created.
        :param subnets: Options for selection of subnets from the VPC to attach to the Connection.
        :param vpc: VPC to attach to the Connection.
        '''
        if isinstance(subnets, dict):
            subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        if __debug__:
            type_hints = typing.get_type_hints(ConnectionProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[str, typing.Any] = {
            "connection_type": connection_type,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if properties is not None:
            self._values["properties"] = properties
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_type(self) -> "ConnectionType":
        '''The type of the connection.

        :see: `AWS::Glue::Connection ConnectionInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-connectiontype>`_
        '''
        result = self._values.get("connection_type")
        assert result is not None, "Required property 'connection_type' is missing"
        return typing.cast("ConnectionType", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the Connection.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the connection.

        Connection will not function as expected without a name.

        :see: `AWS::Glue::Connection ConnectionInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-name>`_
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''List of Key/Value pairs defining the properties of the Connection.

        :see: `AWS::Glue::Connection Properties <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html#Properties>`_
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        '''Existing Security Group to assign to the Connection.

        If none is provided a new Security Group will be created.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''Options for selection of subnets from the VPC to attach to the Connection.

        :see: `CDK SubnetSelection <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.SubnetSelection.html>`_
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        '''VPC to attach to the Connection.

        :see: `IVpc Interface <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.IVpc.html>`_
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.ConnectionType")
class ConnectionType(enum.Enum):
    JDBC = "JDBC"
    '''JDBC - Designates a connection to a database through Java Database Connectivity (JDBC).'''
    KAFKA = "KAFKA"
    '''KAFKA - Designates a connection to an Apache Kafka streaming platform.'''
    MONGODB = "MONGODB"
    '''MONGODB - Designates a connection to a MongoDB document database.'''
    NETWORK = "NETWORK"
    '''NETWORK - Designates a network connection to a data source within an Amazon Virtual Private Cloud environment (Amazon VPC).'''


@jsii.data_type(
    jsii_type="cdk-extensions.glue.ContinuousLoggingProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "conversion_pattern": "conversionPattern",
        "log_group": "logGroup",
        "log_stream_prefix": "logStreamPrefix",
        "quiet": "quiet",
    },
)
class ContinuousLoggingProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        conversion_pattern: typing.Optional[builtins.str] = None,
        log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup] = None,
        log_stream_prefix: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param enabled: Enable continouous logging.
        :param conversion_pattern: Apply the provided conversion pattern. This is a Log4j Conversion Pattern to customize driver and executor logs. Default: ``%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n``
        :param log_group: Specify a custom CloudWatch log group name. Default: - a log group is created with name ``/aws-glue/jobs/logs-v2/``.
        :param log_stream_prefix: Specify a custom CloudWatch log stream prefix. Default: - the job run ID.
        :param quiet: Filter out non-useful Apache Spark driver/executor and Apache Hadoop YARN heartbeat log messages. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ContinuousLoggingProps.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument conversion_pattern", value=conversion_pattern, expected_type=type_hints["conversion_pattern"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_stream_prefix", value=log_stream_prefix, expected_type=type_hints["log_stream_prefix"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
        self._values: typing.Dict[str, typing.Any] = {
            "enabled": enabled,
        }
        if conversion_pattern is not None:
            self._values["conversion_pattern"] = conversion_pattern
        if log_group is not None:
            self._values["log_group"] = log_group
        if log_stream_prefix is not None:
            self._values["log_stream_prefix"] = log_stream_prefix
        if quiet is not None:
            self._values["quiet"] = quiet

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Enable continouous logging.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def conversion_pattern(self) -> typing.Optional[builtins.str]:
        '''Apply the provided conversion pattern.

        This is a Log4j Conversion Pattern to customize driver and executor logs.

        :default: ``%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n``
        '''
        result = self._values.get("conversion_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        '''Specify a custom CloudWatch log group name.

        :default: - a log group is created with name ``/aws-glue/jobs/logs-v2/``.
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogGroup], result)

    @builtins.property
    def log_stream_prefix(self) -> typing.Optional[builtins.str]:
        '''Specify a custom CloudWatch log stream prefix.

        :default: - the job run ID.
        '''
        result = self._values.get("log_stream_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        '''Filter out non-useful Apache Spark driver/executor and Apache Hadoop YARN heartbeat log messages.

        :default: true
        '''
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContinuousLoggingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.glue.CrawlerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "partition_update_behavior": "partitionUpdateBehavior",
        "table_grouping_policy": "tableGroupingPolicy",
        "table_level": "tableLevel",
        "table_update_behavior": "tableUpdateBehavior",
        "version": "version",
    },
)
class CrawlerConfiguration:
    def __init__(
        self,
        *,
        partition_update_behavior: typing.Optional["PartitionUpdateBehavior"] = None,
        table_grouping_policy: typing.Optional["TableGroupingPolicy"] = None,
        table_level: typing.Optional[jsii.Number] = None,
        table_update_behavior: typing.Optional["TableUpdateBehavior"] = None,
        version: typing.Optional[ConfigurationVersion] = None,
    ) -> None:
        '''
        :param partition_update_behavior: 
        :param table_grouping_policy: 
        :param table_level: 
        :param table_update_behavior: 
        :param version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CrawlerConfiguration.__init__)
            check_type(argname="argument partition_update_behavior", value=partition_update_behavior, expected_type=type_hints["partition_update_behavior"])
            check_type(argname="argument table_grouping_policy", value=table_grouping_policy, expected_type=type_hints["table_grouping_policy"])
            check_type(argname="argument table_level", value=table_level, expected_type=type_hints["table_level"])
            check_type(argname="argument table_update_behavior", value=table_update_behavior, expected_type=type_hints["table_update_behavior"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[str, typing.Any] = {}
        if partition_update_behavior is not None:
            self._values["partition_update_behavior"] = partition_update_behavior
        if table_grouping_policy is not None:
            self._values["table_grouping_policy"] = table_grouping_policy
        if table_level is not None:
            self._values["table_level"] = table_level
        if table_update_behavior is not None:
            self._values["table_update_behavior"] = table_update_behavior
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def partition_update_behavior(self) -> typing.Optional["PartitionUpdateBehavior"]:
        result = self._values.get("partition_update_behavior")
        return typing.cast(typing.Optional["PartitionUpdateBehavior"], result)

    @builtins.property
    def table_grouping_policy(self) -> typing.Optional["TableGroupingPolicy"]:
        result = self._values.get("table_grouping_policy")
        return typing.cast(typing.Optional["TableGroupingPolicy"], result)

    @builtins.property
    def table_level(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("table_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def table_update_behavior(self) -> typing.Optional["TableUpdateBehavior"]:
        result = self._values.get("table_update_behavior")
        return typing.cast(typing.Optional["TableUpdateBehavior"], result)

    @builtins.property
    def version(self) -> typing.Optional[ConfigurationVersion]:
        result = self._values.get("version")
        return typing.cast(typing.Optional[ConfigurationVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrawlerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.glue.CrawlerProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "classifiers": "classifiers",
        "configuration": "configuration",
        "database": "database",
        "delete_behavior": "deleteBehavior",
        "description": "description",
        "name": "name",
        "recrawl_behavior": "recrawlBehavior",
        "schedule_expression": "scheduleExpression",
        "security_configuration": "securityConfiguration",
        "table_prefix": "tablePrefix",
        "targets": "targets",
        "update_behavior": "updateBehavior",
    },
)
class CrawlerProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[typing.Union[CrawlerConfiguration, typing.Dict[str, typing.Any]]] = None,
        database: typing.Optional["Database"] = None,
        delete_behavior: typing.Optional["DeleteBehavior"] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        recrawl_behavior: typing.Optional["RecrawlBehavior"] = None,
        schedule_expression: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        security_configuration: typing.Optional["SecurityConfiguration"] = None,
        table_prefix: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence["ICrawlerTarget"]] = None,
        update_behavior: typing.Optional["UpdateBehavior"] = None,
    ) -> None:
        '''Configuration for Crawler.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param classifiers: A list of UTF-8 strings that specify the names of custom classifiers that are associated with the crawler.
        :param configuration: Crawler configuration information. This versioned JSON string allows users to specify aspects of a crawler's behavior. For more information, see Configuring a Crawler.
        :param database: The {@link aws-glue.Database | Database } object in which the crawler's output is stored.
        :param delete_behavior: The deletion behavior when the crawler finds a deleted object.
        :param description: Description of the Crawler.
        :param name: Name of the Crawler.
        :param recrawl_behavior: When crawling an Amazon S3 data source after the first crawl is complete, specifies whether to crawl the entire dataset again or to crawl only folders that were added since the last crawler run.
        :param schedule_expression: For scheduled crawlers, the schedule when the crawler runs.
        :param security_configuration: A {@link aws-glue.SecurityConfiguration | SecurityConfiguration } object to apply to the Crawler.
        :param table_prefix: The prefix added to the names of tables that are created.
        :param targets: A collection of targets to crawl.
        :param update_behavior: The update behavior when the crawler finds a changed schema.
        '''
        if isinstance(configuration, dict):
            configuration = CrawlerConfiguration(**configuration)
        if __debug__:
            type_hints = typing.get_type_hints(CrawlerProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument classifiers", value=classifiers, expected_type=type_hints["classifiers"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument delete_behavior", value=delete_behavior, expected_type=type_hints["delete_behavior"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recrawl_behavior", value=recrawl_behavior, expected_type=type_hints["recrawl_behavior"])
            check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument update_behavior", value=update_behavior, expected_type=type_hints["update_behavior"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if classifiers is not None:
            self._values["classifiers"] = classifiers
        if configuration is not None:
            self._values["configuration"] = configuration
        if database is not None:
            self._values["database"] = database
        if delete_behavior is not None:
            self._values["delete_behavior"] = delete_behavior
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if recrawl_behavior is not None:
            self._values["recrawl_behavior"] = recrawl_behavior
        if schedule_expression is not None:
            self._values["schedule_expression"] = schedule_expression
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if table_prefix is not None:
            self._values["table_prefix"] = table_prefix
        if targets is not None:
            self._values["targets"] = targets
        if update_behavior is not None:
            self._values["update_behavior"] = update_behavior

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def classifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of UTF-8 strings that specify the names of custom classifiers that are associated with the crawler.

        :see: `AWS::Glue::Crawler <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-classifiers>`_
        '''
        result = self._values.get("classifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def configuration(self) -> typing.Optional[CrawlerConfiguration]:
        '''Crawler configuration information.

        This versioned JSON string allows users to specify aspects of a crawler's behavior. For more information, see Configuring a Crawler.

        :see: `AWS::Glue::Crawler <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-configuration>`_
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[CrawlerConfiguration], result)

    @builtins.property
    def database(self) -> typing.Optional["Database"]:
        '''The {@link aws-glue.Database | Database } object in which the crawler's output is stored.'''
        result = self._values.get("database")
        return typing.cast(typing.Optional["Database"], result)

    @builtins.property
    def delete_behavior(self) -> typing.Optional["DeleteBehavior"]:
        '''The deletion behavior when the crawler finds a deleted object.

        :see: `AWS::Glue::Crawler SchemaChangePolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schemachangepolicy.html#cfn-glue-crawler-schemachangepolicy-deletebehavior>`_
        '''
        result = self._values.get("delete_behavior")
        return typing.cast(typing.Optional["DeleteBehavior"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the Crawler.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the Crawler.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recrawl_behavior(self) -> typing.Optional["RecrawlBehavior"]:
        '''When crawling an Amazon S3 data source after the first crawl is complete, specifies whether to crawl the entire dataset again or to crawl only folders that were added since the last crawler run.

        :see: `AWS::Glue::Crawler RecrawlPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-recrawlpolicy.html>`_
        '''
        result = self._values.get("recrawl_behavior")
        return typing.cast(typing.Optional["RecrawlBehavior"], result)

    @builtins.property
    def schedule_expression(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        '''For scheduled crawlers, the schedule when the crawler runs.

        :see: `AWS::Glue::Crawler Schedule <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schedule.html>`_
        '''
        result = self._values.get("schedule_expression")
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional["SecurityConfiguration"]:
        '''A {@link aws-glue.SecurityConfiguration | SecurityConfiguration } object to apply to the Crawler.'''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional["SecurityConfiguration"], result)

    @builtins.property
    def table_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix added to the names of tables that are created.

        :see: `AWS::Glue::Crawler <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-tableprefix>`_
        '''
        result = self._values.get("table_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List["ICrawlerTarget"]]:
        '''A collection of targets to crawl.

        :see: `AWS::Glue::Crawler <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-targets>`_
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List["ICrawlerTarget"]], result)

    @builtins.property
    def update_behavior(self) -> typing.Optional["UpdateBehavior"]:
        '''The update behavior when the crawler finds a changed schema.

        :see: `AWS::Glue::Crawler SchemaChangePolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schemachangepolicy.html#cfn-glue-crawler-schemachangepolicy-updatebehavior>`_
        '''
        result = self._values.get("update_behavior")
        return typing.cast(typing.Optional["UpdateBehavior"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrawlerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.CrawlerState")
class CrawlerState(enum.Enum):
    '''State a Glue crawler must be in in order to satisfy a predicate condition to trigger a part of a workflow.'''

    CANCELLED = "CANCELLED"
    '''A crawler execution was cancelled before it could finish.'''
    FAILED = "FAILED"
    '''A crawler that has finished and ended in an error.'''
    SUCCEEDED = "SUCCEEDED"
    '''A crawler which has finished successfully.'''


@jsii.data_type(
    jsii_type="cdk-extensions.glue.CrawlerTargetCollection",
    jsii_struct_bases=[],
    name_mapping={
        "catalog_targets": "catalogTargets",
        "dynamo_db_targets": "dynamoDbTargets",
        "jdbc_targets": "jdbcTargets",
        "s3_targets": "s3Targets",
    },
)
class CrawlerTargetCollection:
    def __init__(
        self,
        *,
        catalog_targets: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_glue.CfnCrawler.CatalogTargetProperty, typing.Dict[str, typing.Any]]]] = None,
        dynamo_db_targets: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_glue.CfnCrawler.DynamoDBTargetProperty, typing.Dict[str, typing.Any]]]] = None,
        jdbc_targets: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_glue.CfnCrawler.JdbcTargetProperty, typing.Dict[str, typing.Any]]]] = None,
        s3_targets: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_glue.CfnCrawler.S3TargetProperty, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param catalog_targets: 
        :param dynamo_db_targets: 
        :param jdbc_targets: 
        :param s3_targets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CrawlerTargetCollection.__init__)
            check_type(argname="argument catalog_targets", value=catalog_targets, expected_type=type_hints["catalog_targets"])
            check_type(argname="argument dynamo_db_targets", value=dynamo_db_targets, expected_type=type_hints["dynamo_db_targets"])
            check_type(argname="argument jdbc_targets", value=jdbc_targets, expected_type=type_hints["jdbc_targets"])
            check_type(argname="argument s3_targets", value=s3_targets, expected_type=type_hints["s3_targets"])
        self._values: typing.Dict[str, typing.Any] = {}
        if catalog_targets is not None:
            self._values["catalog_targets"] = catalog_targets
        if dynamo_db_targets is not None:
            self._values["dynamo_db_targets"] = dynamo_db_targets
        if jdbc_targets is not None:
            self._values["jdbc_targets"] = jdbc_targets
        if s3_targets is not None:
            self._values["s3_targets"] = s3_targets

    @builtins.property
    def catalog_targets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_glue.CfnCrawler.CatalogTargetProperty]]:
        result = self._values.get("catalog_targets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_glue.CfnCrawler.CatalogTargetProperty]], result)

    @builtins.property
    def dynamo_db_targets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_glue.CfnCrawler.DynamoDBTargetProperty]]:
        result = self._values.get("dynamo_db_targets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_glue.CfnCrawler.DynamoDBTargetProperty]], result)

    @builtins.property
    def jdbc_targets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_glue.CfnCrawler.JdbcTargetProperty]]:
        result = self._values.get("jdbc_targets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_glue.CfnCrawler.JdbcTargetProperty]], result)

    @builtins.property
    def s3_targets(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_glue.CfnCrawler.S3TargetProperty]]:
        result = self._values.get("s3_targets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_glue.CfnCrawler.S3TargetProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrawlerTargetCollection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFormat(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.glue.DataFormat"):
    '''Defines the input/output formats and ser/de for a single DataFormat.'''

    def __init__(
        self,
        *,
        input_format: "InputFormat",
        output_format: "OutputFormat",
        serialization_library: "SerializationLibrary",
        classification_string: typing.Optional[ClassificationString] = None,
    ) -> None:
        '''
        :param input_format: ``InputFormat`` for this data format.
        :param output_format: ``OutputFormat`` for this data format.
        :param serialization_library: Serialization library for this data format.
        :param classification_string: Classification string given to tables with this data format. Default: - No classification is specified.
        '''
        props = DataFormatProps(
            input_format=input_format,
            output_format=output_format,
            serialization_library=serialization_library,
            classification_string=classification_string,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="APACHE_LOGS")
    def APACHE_LOGS(cls) -> "DataFormat":
        '''DataFormat for Apache Web Server Logs.

        Also works for CloudFront logs

        :see: https://docs.aws.amazon.com/athena/latest/ug/apache.html
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "APACHE_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVRO")
    def AVRO(cls) -> "DataFormat":
        '''DataFormat for Apache Avro.

        :see: https://docs.aws.amazon.com/athena/latest/ug/avro.html
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "AVRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDTRAIL_LOGS")
    def CLOUDTRAIL_LOGS(cls) -> "DataFormat":
        '''DataFormat for CloudTrail logs stored on S3.

        :see: https://docs.aws.amazon.com/athena/latest/ug/cloudtrail.html
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "CLOUDTRAIL_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CSV")
    def CSV(cls) -> "DataFormat":
        '''DataFormat for CSV Files.

        :see: https://docs.aws.amazon.com/athena/latest/ug/csv.html
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "CSV"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="JSON")
    def JSON(cls) -> "DataFormat":
        '''Stored as plain text files in JSON format.

        Uses OpenX Json SerDe for serialization and deseralization.

        :see: https://docs.aws.amazon.com/athena/latest/ug/json.html
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "JSON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOGSTASH")
    def LOGSTASH(cls) -> "DataFormat":
        '''DataFormat for Logstash Logs, using the GROK SerDe.

        :see: https://docs.aws.amazon.com/athena/latest/ug/grok.html
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "LOGSTASH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORC")
    def ORC(cls) -> "DataFormat":
        '''DataFormat for Apache ORC (Optimized Row Columnar).

        :see: https://docs.aws.amazon.com/athena/latest/ug/orc.html
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "ORC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARQUET")
    def PARQUET(cls) -> "DataFormat":
        '''DataFormat for Apache Parquet.

        :see: https://docs.aws.amazon.com/athena/latest/ug/parquet.html
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "PARQUET"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TSV")
    def TSV(cls) -> "DataFormat":
        '''DataFormat for TSV (Tab-Separated Values).

        :see: https://docs.aws.amazon.com/athena/latest/ug/lazy-simple-serde.html
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "TSV"))

    @builtins.property
    @jsii.member(jsii_name="inputFormat")
    def input_format(self) -> "InputFormat":
        '''``InputFormat`` for this data format.'''
        return typing.cast("InputFormat", jsii.get(self, "inputFormat"))

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> "OutputFormat":
        '''``OutputFormat`` for this data format.'''
        return typing.cast("OutputFormat", jsii.get(self, "outputFormat"))

    @builtins.property
    @jsii.member(jsii_name="serializationLibrary")
    def serialization_library(self) -> "SerializationLibrary":
        '''Serialization library for this data format.'''
        return typing.cast("SerializationLibrary", jsii.get(self, "serializationLibrary"))

    @builtins.property
    @jsii.member(jsii_name="classificationString")
    def classification_string(self) -> typing.Optional[ClassificationString]:
        '''Classification string given to tables with this data format.'''
        return typing.cast(typing.Optional[ClassificationString], jsii.get(self, "classificationString"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.DataFormatProps",
    jsii_struct_bases=[],
    name_mapping={
        "input_format": "inputFormat",
        "output_format": "outputFormat",
        "serialization_library": "serializationLibrary",
        "classification_string": "classificationString",
    },
)
class DataFormatProps:
    def __init__(
        self,
        *,
        input_format: "InputFormat",
        output_format: "OutputFormat",
        serialization_library: "SerializationLibrary",
        classification_string: typing.Optional[ClassificationString] = None,
    ) -> None:
        '''Properties of a DataFormat instance.

        :param input_format: ``InputFormat`` for this data format.
        :param output_format: ``OutputFormat`` for this data format.
        :param serialization_library: Serialization library for this data format.
        :param classification_string: Classification string given to tables with this data format. Default: - No classification is specified.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataFormatProps.__init__)
            check_type(argname="argument input_format", value=input_format, expected_type=type_hints["input_format"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument serialization_library", value=serialization_library, expected_type=type_hints["serialization_library"])
            check_type(argname="argument classification_string", value=classification_string, expected_type=type_hints["classification_string"])
        self._values: typing.Dict[str, typing.Any] = {
            "input_format": input_format,
            "output_format": output_format,
            "serialization_library": serialization_library,
        }
        if classification_string is not None:
            self._values["classification_string"] = classification_string

    @builtins.property
    def input_format(self) -> "InputFormat":
        '''``InputFormat`` for this data format.'''
        result = self._values.get("input_format")
        assert result is not None, "Required property 'input_format' is missing"
        return typing.cast("InputFormat", result)

    @builtins.property
    def output_format(self) -> "OutputFormat":
        '''``OutputFormat`` for this data format.'''
        result = self._values.get("output_format")
        assert result is not None, "Required property 'output_format' is missing"
        return typing.cast("OutputFormat", result)

    @builtins.property
    def serialization_library(self) -> "SerializationLibrary":
        '''Serialization library for this data format.'''
        result = self._values.get("serialization_library")
        assert result is not None, "Required property 'serialization_library' is missing"
        return typing.cast("SerializationLibrary", result)

    @builtins.property
    def classification_string(self) -> typing.Optional[ClassificationString]:
        '''Classification string given to tables with this data format.

        :default: - No classification is specified.
        '''
        result = self._values.get("classification_string")
        return typing.cast(typing.Optional[ClassificationString], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFormatProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Database(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.Database",
):
    '''Creates a Glue Database resource to contain a collection of metadata Tables.

    :see: [AWS::Glue::Database](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        location_uri: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the Database class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param description: A description of the database.
        :param location_uri: The location of the database (for example, an HDFS path).
        :param name: The name of the database. For Hive compatibility, this is folded to lowercase when it is stored.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Database.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DatabaseProps(
            description=description,
            location_uri=location_uri,
            name=name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="catalogArn")
    def catalog_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalogArn"))

    @builtins.property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalogId"))

    @builtins.property
    @jsii.member(jsii_name="databaseArn")
    def database_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseArn"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''{@link DatabaseProps.name:}.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_glue.CfnDatabase:
        return typing.cast(aws_cdk.aws_glue.CfnDatabase, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''{@link DatabaseProps.description}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="locationUri")
    def location_uri(self) -> typing.Optional[builtins.str]:
        '''{@link DatabaseProps.locationUri}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationUri"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.DatabaseProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "description": "description",
        "location_uri": "locationUri",
        "name": "name",
    },
)
class DatabaseProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        location_uri: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for Database.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param description: A description of the database.
        :param location_uri: The location of the database (for example, an HDFS path).
        :param name: The name of the database. For Hive compatibility, this is folded to lowercase when it is stored.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DatabaseProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location_uri", value=location_uri, expected_type=type_hints["location_uri"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if description is not None:
            self._values["description"] = description
        if location_uri is not None:
            self._values["location_uri"] = location_uri
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the database.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location_uri(self) -> typing.Optional[builtins.str]:
        '''The location of the database (for example, an HDFS path).

        :see: `AWS::Glue::Database DatabaseInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-locationuri>`_
        '''
        result = self._values.get("location_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the database.

        For Hive compatibility, this is folded to lowercase when it is stored.
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.DeleteBehavior")
class DeleteBehavior(enum.Enum):
    DELETE_FROM_DATABASE = "DELETE_FROM_DATABASE"
    DEPRECATE_IN_DATABASE = "DEPRECATE_IN_DATABASE"
    LOG = "LOG"


class GlueVersion(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.glue.GlueVersion"):
    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, version: builtins.str) -> "GlueVersion":
        '''Custom Glue version.

        :param version: custom version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GlueVersion.of)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("GlueVersion", jsii.sinvoke(cls, "of", [version]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V0_9")
    def V0_9(cls) -> "GlueVersion":
        '''Glue version using Spark 2.2.1 and Python 2.7.'''
        return typing.cast("GlueVersion", jsii.sget(cls, "V0_9"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_0")
    def V1_0(cls) -> "GlueVersion":
        '''Glue version using Spark 2.4.3, Python 2.7 and Python 3.6.'''
        return typing.cast("GlueVersion", jsii.sget(cls, "V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_0")
    def V2_0(cls) -> "GlueVersion":
        '''Glue version using Spark 2.4.3 and Python 3.7.'''
        return typing.cast("GlueVersion", jsii.sget(cls, "V2_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_0")
    def V3_0(cls) -> "GlueVersion":
        '''Glue version using Spark 3.1.1 and Python 3.7.'''
        return typing.cast("GlueVersion", jsii.sget(cls, "V3_0"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of this GlueVersion, as expected by Job resource.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.interface(jsii_type="cdk-extensions.glue.ICrawler")
class ICrawler(constructs.IConstruct, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="crawlerArn")
    def crawler_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the crawler.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="crawlerName")
    def crawler_name(self) -> builtins.str:
        '''The name of the crawler.'''
        ...


class _ICrawlerProxy(
    jsii.proxy_for(constructs.IConstruct), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.glue.ICrawler"

    @builtins.property
    @jsii.member(jsii_name="crawlerArn")
    def crawler_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the crawler.'''
        return typing.cast(builtins.str, jsii.get(self, "crawlerArn"))

    @builtins.property
    @jsii.member(jsii_name="crawlerName")
    def crawler_name(self) -> builtins.str:
        '''The name of the crawler.'''
        return typing.cast(builtins.str, jsii.get(self, "crawlerName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICrawler).__jsii_proxy_class__ = lambda : _ICrawlerProxy


@jsii.interface(jsii_type="cdk-extensions.glue.ICrawlerTarget")
class ICrawlerTarget(typing_extensions.Protocol):
    @jsii.member(jsii_name="bind")
    def bind(self, crawler: "Crawler") -> CrawlerTargetCollection:
        '''
        :param crawler: -
        '''
        ...


class _ICrawlerTargetProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.glue.ICrawlerTarget"

    @jsii.member(jsii_name="bind")
    def bind(self, crawler: "Crawler") -> CrawlerTargetCollection:
        '''
        :param crawler: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ICrawlerTarget.bind)
            check_type(argname="argument crawler", value=crawler, expected_type=type_hints["crawler"])
        return typing.cast(CrawlerTargetCollection, jsii.invoke(self, "bind", [crawler]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICrawlerTarget).__jsii_proxy_class__ = lambda : _ICrawlerTargetProxy


@jsii.interface(jsii_type="cdk-extensions.glue.IJob")
class IJob(constructs.IConstruct, typing_extensions.Protocol):
    '''Represnets a Glue Job in AWS.'''

    @builtins.property
    @jsii.member(jsii_name="jobArn")
    def job_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the job.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''The name of the job.'''
        ...


class _IJobProxy(
    jsii.proxy_for(constructs.IConstruct), # type: ignore[misc]
):
    '''Represnets a Glue Job in AWS.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.glue.IJob"

    @builtins.property
    @jsii.member(jsii_name="jobArn")
    def job_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobArn"))

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''The name of the job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJob).__jsii_proxy_class__ = lambda : _IJobProxy


@jsii.interface(jsii_type="cdk-extensions.glue.ITrigger")
class ITrigger(constructs.IConstruct, typing_extensions.Protocol):
    '''Represents a Glue Trigger in AWS.'''

    @builtins.property
    @jsii.member(jsii_name="triggerArn")
    def trigger_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the trigger.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="triggerName")
    def trigger_name(self) -> builtins.str:
        '''The name of the trigger.'''
        ...


class _ITriggerProxy(
    jsii.proxy_for(constructs.IConstruct), # type: ignore[misc]
):
    '''Represents a Glue Trigger in AWS.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.glue.ITrigger"

    @builtins.property
    @jsii.member(jsii_name="triggerArn")
    def trigger_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the trigger.'''
        return typing.cast(builtins.str, jsii.get(self, "triggerArn"))

    @builtins.property
    @jsii.member(jsii_name="triggerName")
    def trigger_name(self) -> builtins.str:
        '''The name of the trigger.'''
        return typing.cast(builtins.str, jsii.get(self, "triggerName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITrigger).__jsii_proxy_class__ = lambda : _ITriggerProxy


@jsii.interface(jsii_type="cdk-extensions.glue.ITriggerAction")
class ITriggerAction(typing_extensions.Protocol):
    '''Represents an action that should be taken when a trigger is executed.'''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_glue.CfnTrigger.ActionProperty:
        '''
        :param scope: -
        '''
        ...


class _ITriggerActionProxy:
    '''Represents an action that should be taken when a trigger is executed.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.glue.ITriggerAction"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_glue.CfnTrigger.ActionProperty:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ITriggerAction.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_glue.CfnTrigger.ActionProperty, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITriggerAction).__jsii_proxy_class__ = lambda : _ITriggerActionProxy


@jsii.interface(jsii_type="cdk-extensions.glue.ITriggerPredicate")
class ITriggerPredicate(typing_extensions.Protocol):
    '''Represents a precondition that must be satisfied in order for a trigger to be executed.'''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_glue.CfnTrigger.ConditionProperty:
        '''
        :param scope: -
        '''
        ...


class _ITriggerPredicateProxy:
    '''Represents a precondition that must be satisfied in order for a trigger to be executed.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.glue.ITriggerPredicate"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_glue.CfnTrigger.ConditionProperty:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ITriggerPredicate.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_glue.CfnTrigger.ConditionProperty, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITriggerPredicate).__jsii_proxy_class__ = lambda : _ITriggerPredicateProxy


class InputFormat(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.glue.InputFormat"):
    '''Absolute class name of the Hadoop ``InputFormat`` to use when reading table files.'''

    def __init__(self, class_name: builtins.str) -> None:
        '''
        :param class_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(InputFormat.__init__)
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
        jsii.create(self.__class__, self, [class_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVRO")
    def AVRO(cls) -> "InputFormat":
        '''InputFormat for Avro files.

        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/ql/io/avro/AvroContainerInputFormat.html
        '''
        return typing.cast("InputFormat", jsii.sget(cls, "AVRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDTRAIL")
    def CLOUDTRAIL(cls) -> "InputFormat":
        '''InputFormat for Cloudtrail Logs.

        :see: https://docs.aws.amazon.com/athena/latest/ug/cloudtrail.html
        '''
        return typing.cast("InputFormat", jsii.sget(cls, "CLOUDTRAIL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORC")
    def ORC(cls) -> "InputFormat":
        '''InputFormat for Orc files.

        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/ql/io/orc/OrcInputFormat.html
        '''
        return typing.cast("InputFormat", jsii.sget(cls, "ORC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARQUET")
    def PARQUET(cls) -> "InputFormat":
        '''InputFormat for Parquet files.

        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/ql/io/parquet/MapredParquetInputFormat.html
        '''
        return typing.cast("InputFormat", jsii.sget(cls, "PARQUET"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TEXT")
    def TEXT(cls) -> "InputFormat":
        '''An InputFormat for plain text files.

        Files are broken into lines. Either linefeed or
        carriage-return are used to signal end of line. Keys are the position in the file, and
        values are the line of text.
        JSON & CSV files are examples of this InputFormat

        :see: https://hadoop.apache.org/docs/stable/api/org/apache/hadoop/mapred/TextInputFormat.html
        '''
        return typing.cast("InputFormat", jsii.sget(cls, "TEXT"))

    @builtins.property
    @jsii.member(jsii_name="className")
    def class_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "className"))


class JdbcConnection(
    Connection,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.JdbcConnection",
):
    '''Creates a Connection resource to a Java Database.

    :see: `AWS::Glue::Connection <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html>`_
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        password: aws_cdk.SecretValue,
        url: builtins.str,
        username: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
        description: typing.Optional[builtins.str] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the JdbcConnection class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param password: A SecretValue providing the password for the Connection to authenticate to the source with.
        :param url: The URL to the source for the Connection.
        :param username: The username for the Connection to authenticate to the source with.
        :param vpc: VPC to attach to the Connection.
        :param description: A description of the Connection.
        :param enforce_ssl: Boolean value on whether to require encryption on the Connection.
        :param name: A name for the Connection.
        :param security_groups: A list of Security Groups to apply to the Connection.
        :param subnets: Options for selection of subnets from the VPC to attach to the Connection.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JdbcConnection.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JdbcConnectionProps(
            password=password,
            url=url,
            username=username,
            vpc=vpc,
            description=description,
            enforce_ssl=enforce_ssl,
            name=name,
            security_groups=security_groups,
            subnets=subnets,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> aws_cdk.SecretValue:
        '''{@link JdbcConnectionProps.password:}.'''
        return typing.cast(aws_cdk.SecretValue, jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''{@link JdbcConnectionProps.url:}.'''
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        '''{@link JdbcConnectionProps.username:}.'''
        return typing.cast(builtins.str, jsii.get(self, "username"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.JdbcConnectionProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "password": "password",
        "url": "url",
        "username": "username",
        "vpc": "vpc",
        "description": "description",
        "enforce_ssl": "enforceSsl",
        "name": "name",
        "security_groups": "securityGroups",
        "subnets": "subnets",
    },
)
class JdbcConnectionProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        password: aws_cdk.SecretValue,
        url: builtins.str,
        username: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
        description: typing.Optional[builtins.str] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''Configuration for the Glue Workflow resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param password: A SecretValue providing the password for the Connection to authenticate to the source with.
        :param url: The URL to the source for the Connection.
        :param username: The username for the Connection to authenticate to the source with.
        :param vpc: VPC to attach to the Connection.
        :param description: A description of the Connection.
        :param enforce_ssl: Boolean value on whether to require encryption on the Connection.
        :param name: A name for the Connection.
        :param security_groups: A list of Security Groups to apply to the Connection.
        :param subnets: Options for selection of subnets from the VPC to attach to the Connection.
        '''
        if isinstance(subnets, dict):
            subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        if __debug__:
            type_hints = typing.get_type_hints(JdbcConnectionProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enforce_ssl", value=enforce_ssl, expected_type=type_hints["enforce_ssl"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[str, typing.Any] = {
            "password": password,
            "url": url,
            "username": username,
            "vpc": vpc,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if description is not None:
            self._values["description"] = description
        if enforce_ssl is not None:
            self._values["enforce_ssl"] = enforce_ssl
        if name is not None:
            self._values["name"] = name
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> aws_cdk.SecretValue:
        '''A SecretValue providing the password for the Connection to authenticate to the source with.

        :see: `AWS::Glue::Connection ConnectionInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-connectiontype>`_
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(aws_cdk.SecretValue, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL to the source for the Connection.

        :see: `AWS::Glue::Connection ConnectionInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-connectiontype>`_
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The username for the Connection to authenticate to the source with.

        :see: `AWS::Glue::Connection ConnectionInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-connectiontype>`_
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''VPC to attach to the Connection.

        :see: `IVpc Interface <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.IVpc.html>`_
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the Connection.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_ssl(self) -> typing.Optional[builtins.bool]:
        '''Boolean value on whether to require encryption on the Connection.

        :see: `AWS::Glue::Connection ConnectionInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-connectiontype>`_
        '''
        result = self._values.get("enforce_ssl")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the Connection.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        '''A list of Security Groups to apply to the Connection.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''Options for selection of subnets from the VPC to attach to the Connection.

        :see: `CDK SubnetSelection <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.SubnetSelection.html>`_
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JdbcConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ICrawlerTarget)
class JdbcTarget(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.glue.JdbcTarget"):
    def __init__(
        self,
        connection: Connection,
        *,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Creates a new instance of the JdbcTarget class.

        :param connection: -
        :param exclusions: A list of glob patterns used to exclude from the crawl. For more information
        :param paths: The path of the JDBC target.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JdbcTarget.__init__)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
        options = JdbcTargetOptions(exclusions=exclusions, paths=paths)

        jsii.create(self.__class__, self, [connection, options])

    @jsii.member(jsii_name="addExclusion")
    def add_exclusion(self, exclusion: builtins.str) -> None:
        '''
        :param exclusion: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JdbcTarget.add_exclusion)
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
        return typing.cast(None, jsii.invoke(self, "addExclusion", [exclusion]))

    @jsii.member(jsii_name="addPath")
    def add_path(self, path: builtins.str) -> None:
        '''
        :param path: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JdbcTarget.add_path)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(None, jsii.invoke(self, "addPath", [path]))

    @jsii.member(jsii_name="bind")
    def bind(self, _crawler: "Crawler") -> CrawlerTargetCollection:
        '''
        :param _crawler: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JdbcTarget.bind)
            check_type(argname="argument _crawler", value=_crawler, expected_type=type_hints["_crawler"])
        return typing.cast(CrawlerTargetCollection, jsii.invoke(self, "bind", [_crawler]))

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(self) -> Connection:
        return typing.cast(Connection, jsii.get(self, "connection"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.JdbcTargetOptions",
    jsii_struct_bases=[],
    name_mapping={"exclusions": "exclusions", "paths": "paths"},
)
class JdbcTargetOptions:
    def __init__(
        self,
        *,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Configuration for Crawler JDBC target.

        :param exclusions: A list of glob patterns used to exclude from the crawl. For more information
        :param paths: The path of the JDBC target.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JdbcTargetOptions.__init__)
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        self._values: typing.Dict[str, typing.Any] = {}
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if paths is not None:
            self._values["paths"] = paths

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of glob patterns used to exclude from the crawl.

        For more information

        :see: `Catalog Tables with a Crawler <https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html>`_
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The path of the JDBC target.

        :see: `AWS::Glue::Crawler JdbcTarget <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-jdbctarget.html#cfn-glue-crawler-jdbctarget-path>`_
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JdbcTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IJob)
class Job(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.Job",
):
    '''Creates a Glue Job.

    :see: `AWS::Glue::Job <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html>`_
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        executable: "JobExecutable",
        allocated_capacity: typing.Optional[jsii.Number] = None,
        connections: typing.Optional[typing.Sequence[Connection]] = None,
        continuous_logging: typing.Optional[typing.Union[ContinuousLoggingProps, typing.Dict[str, typing.Any]]] = None,
        default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_profiling_metrics: typing.Optional[builtins.bool] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_configuration: typing.Optional["SecurityConfiguration"] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        worker_count: typing.Optional[jsii.Number] = None,
        worker_type: typing.Optional["WorkerType"] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the Job class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param executable: Executable properties for the Job.
        :param allocated_capacity: The number of capacity units that are allocated to this job.
        :param connections: List of Connections for use with this job.
        :param continuous_logging: Set of properties for configuration of Continuous Logging.
        :param default_arguments: The default arguments for this job, specified as name-value pairs. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.
        :param description: A description of the job.
        :param enable_profiling_metrics: Boolean value for whether to enable Profiling Metrics.
        :param max_capacity: The number of AWS Glue data processing units (DPUs) that can be allocated when this job runs. A DPU is a relative measure of processing power that consists of 4 vCPUs of compute capacity and 16 GB of memory. Do not set Max Capacity if using WorkerType and NumberOfWorkers. The value that can be allocated for MaxCapacity depends on whether you are running a Python shell job or an Apache Spark ETL job:: - When you specify a Python shell job (JobCommand.Name="pythonshell"), you can allocate either 0.0625 or 1 DPU. The default is 0.0625 DPU. - When you specify an Apache Spark ETL job (JobCommand.Name="glueetl"), you can allocate from 2 to 100 DPUs. The default is 10 DPUs. This job type cannot have a fractional DPU allocation.
        :param max_concurrent_runs: Maximum number of concurrent executions.
        :param max_retries: The maximum number of times to retry this job after a JobRun fails.
        :param name: A name for the Job.
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.
        :param role: The name or Amazon Resource Name (ARN) of the IAM role associated with this job.
        :param security_configuration: The Security Configuration object to be applied to the Job.
        :param timeout: The job timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 2,880 minutes (48 hours).
        :param worker_count: The number of worker available the Job.
        :param worker_type: The type of predefined worker that is allocated when a job runs. Accepts a value of Standard, G.1X, or G.2X.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Job.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JobProps(
            executable=executable,
            allocated_capacity=allocated_capacity,
            connections=connections,
            continuous_logging=continuous_logging,
            default_arguments=default_arguments,
            description=description,
            enable_profiling_metrics=enable_profiling_metrics,
            max_capacity=max_capacity,
            max_concurrent_runs=max_concurrent_runs,
            max_retries=max_retries,
            name=name,
            notify_delay_after=notify_delay_after,
            role=role,
            security_configuration=security_configuration,
            timeout=timeout,
            worker_count=worker_count,
            worker_type=worker_type,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromJobArn")
    @builtins.classmethod
    def from_job_arn(
        cls,
        scope: constructs.IConstruct,
        id: builtins.str,
        job_arn: builtins.str,
    ) -> IJob:
        '''Imports an existing job using its Amazon Resource Name (ARN).

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param job_arn: The ARN of the job to import.

        :return: An object representing the job that was imported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Job.from_job_arn)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_arn", value=job_arn, expected_type=type_hints["job_arn"])
        return typing.cast(IJob, jsii.sinvoke(cls, "fromJobArn", [scope, id, job_arn]))

    @jsii.member(jsii_name="fromJobName")
    @builtins.classmethod
    def from_job_name(
        cls,
        scope: constructs.IConstruct,
        id: builtins.str,
        job_name: builtins.str,
    ) -> IJob:
        '''Imports an existing job using its name.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param job_name: The name of the job to import.

        :return: An object representing the job that was imported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Job.from_job_name)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
        return typing.cast(IJob, jsii.sinvoke(cls, "fromJobName", [scope, id, job_name]))

    @jsii.member(jsii_name="addArgument")
    def add_argument(self, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Job.add_argument)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addArgument", [key, value]))

    @jsii.member(jsii_name="addConnection")
    def add_connection(self, connection: Connection) -> None:
        '''
        :param connection: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Job.add_connection)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
        return typing.cast(None, jsii.invoke(self, "addConnection", [connection]))

    @builtins.property
    @jsii.member(jsii_name="executable")
    def executable(self) -> "JobExecutable":
        '''{@link JobProps.executable:}.'''
        return typing.cast("JobExecutable", jsii.get(self, "executable"))

    @builtins.property
    @jsii.member(jsii_name="jobArn")
    def job_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobArn"))

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''The name of the job.'''
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_glue.CfnJob:
        return typing.cast(aws_cdk.aws_glue.CfnJob, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="allocatedCapacity")
    def allocated_capacity(self) -> typing.Optional[jsii.Number]:
        '''{@link JobProps.allocatedCapacity }.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "allocatedCapacity"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> typing.Optional[typing.List[Connection]]:
        '''{@link JobProps.connections}.'''
        return typing.cast(typing.Optional[typing.List[Connection]], jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="continuousLogging")
    def continuous_logging(self) -> typing.Optional[ContinuousLoggingProps]:
        '''{@link JobProps.continuousLogging}.'''
        return typing.cast(typing.Optional[ContinuousLoggingProps], jsii.get(self, "continuousLogging"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''{@link JobProps.description}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogGroup], jsii.get(self, "logGroup"))

    @builtins.property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''{@link JobProps.maxCapacity}.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxCapacity"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentRuns")
    def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
        '''{@link JobProps.maxConcurrentRuns}.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentRuns"))

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''{@link JobProps.maxRetries}.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetries"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''{@link JobProps.name}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="notifyDelayAfter")
    def notify_delay_after(self) -> typing.Optional[aws_cdk.Duration]:
        '''{@link JobProps.notifyDelayAfter}.'''
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "notifyDelayAfter"))

    @builtins.property
    @jsii.member(jsii_name="securityConfiguration")
    def security_configuration(self) -> typing.Optional["SecurityConfiguration"]:
        '''{@link JobProps.securityConfiguration}.'''
        return typing.cast(typing.Optional["SecurityConfiguration"], jsii.get(self, "securityConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[aws_cdk.Duration]:
        '''{@link JobProps.timeout}.'''
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="workerCount")
    def worker_count(self) -> typing.Optional[jsii.Number]:
        '''{@link JobProps.workerCount}.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "workerCount"))

    @builtins.property
    @jsii.member(jsii_name="workerType")
    def worker_type(self) -> typing.Optional["WorkerType"]:
        '''{@link JobProps.workerType}.'''
        return typing.cast(typing.Optional["WorkerType"], jsii.get(self, "workerType"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.JobBookmarksEncryption",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "kms_key": "kmsKey"},
)
class JobBookmarksEncryption:
    def __init__(
        self,
        *,
        mode: "JobBookmarksEncryptionMode",
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        '''Job bookmarks encryption configuration.

        :param mode: Encryption mode.
        :param kms_key: The KMS key to be used to encrypt the data. Default: A key will be created if one is not provided.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JobBookmarksEncryption.__init__)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "mode": mode,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def mode(self) -> "JobBookmarksEncryptionMode":
        '''Encryption mode.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast("JobBookmarksEncryptionMode", result)

    @builtins.property
    def kms_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''The KMS key to be used to encrypt the data.

        :default: A key will be created if one is not provided.
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobBookmarksEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.JobBookmarksEncryptionMode")
class JobBookmarksEncryptionMode(enum.Enum):
    '''Encryption mode for Job Bookmarks.

    :see: https://docs.aws.amazon.com/glue/latest/webapi/API_JobBookmarksEncryption.html#Glue-Type-JobBookmarksEncryption-JobBookmarksEncryptionMode
    '''

    CLIENT_SIDE_KMS = "CLIENT_SIDE_KMS"
    '''Client-side encryption (CSE) with an AWS KMS key managed by the account owner.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html
    '''


class JobExecutable(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.JobExecutable",
):
    '''The executable properties related to the Glue job's GlueVersion, JobType and code.'''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        *,
        glue_version: GlueVersion,
        language: "JobLanguage",
        script: Code,
        type: "JobType",
        class_name: typing.Optional[builtins.str] = None,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
        python_version: typing.Optional["PythonVersion"] = None,
    ) -> "JobExecutable":
        '''Create a custom JobExecutable.

        :param glue_version: Glue version.
        :param language: The language of the job (Scala or Python).
        :param script: The script that is executed by a job.
        :param type: Specify the type of the job whether it's an Apache Spark ETL or streaming one or if it's a Python shell job.
        :param class_name: The Scala class that serves as the entry point for the job. This applies only if your the job langauage is Scala. Default: - no scala className specified
        :param extra_files: Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Default: - no extra files specified.
        :param extra_jars: Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Default: - no extra jars specified.
        :param extra_jars_first: Setting this value to true prioritizes the customer's extra JAR files in the classpath. Default: - extra jars are not prioritized.
        :param extra_python_files: Additional Python files that AWS Glue adds to the Python path before executing your script. Default: - no extra python files specified.
        :param python_version: The Python version to use. Default: - no python version specified
        '''
        config = JobExecutableConfig(
            glue_version=glue_version,
            language=language,
            script=script,
            type=type,
            class_name=class_name,
            extra_files=extra_files,
            extra_jars=extra_jars,
            extra_jars_first=extra_jars_first,
            extra_python_files=extra_python_files,
            python_version=python_version,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "of", [config]))

    @jsii.member(jsii_name="pythonEtl")
    @builtins.classmethod
    def python_etl(
        cls,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
    ) -> "JobExecutable":
        '''Create Python executable props for Apache Spark ETL job.

        :param glue_version: Glue version.
        :param python_version: The Python version to use.
        :param script: The script that executes a job.
        :param extra_files: Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Default: [] - no extra files are copied to the working directory
        :param extra_jars: Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: Setting this value to true prioritizes the customer's extra JAR files in the classpath. Default: false - priority is not given to user-provided jars
        :param extra_python_files: Additional Python files that AWS Glue adds to the Python path before executing your script. Only individual files are supported, directories are not supported. Default: - no extra python files and argument is not set
        '''
        props = PythonSparkJobExecutableProps(
            glue_version=glue_version,
            python_version=python_version,
            script=script,
            extra_files=extra_files,
            extra_jars=extra_jars,
            extra_jars_first=extra_jars_first,
            extra_python_files=extra_python_files,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "pythonEtl", [props]))

    @jsii.member(jsii_name="pythonShell")
    @builtins.classmethod
    def python_shell(
        cls,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
    ) -> "JobExecutable":
        '''Create Python executable props for python shell jobs.

        :param glue_version: Glue version.
        :param python_version: The Python version to use.
        :param script: The script that executes a job.
        :param extra_files: Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Default: [] - no extra files are copied to the working directory
        :param extra_python_files: Additional Python files that AWS Glue adds to the Python path before executing your script. Only individual files are supported, directories are not supported. Default: - no extra python files and argument is not set
        '''
        props = PythonShellExecutableProps(
            glue_version=glue_version,
            python_version=python_version,
            script=script,
            extra_files=extra_files,
            extra_python_files=extra_python_files,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "pythonShell", [props]))

    @jsii.member(jsii_name="pythonStreaming")
    @builtins.classmethod
    def python_streaming(
        cls,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
    ) -> "JobExecutable":
        '''Create Python executable props for Apache Spark Streaming job.

        :param glue_version: Glue version.
        :param python_version: The Python version to use.
        :param script: The script that executes a job.
        :param extra_files: Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Default: [] - no extra files are copied to the working directory
        :param extra_jars: Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: Setting this value to true prioritizes the customer's extra JAR files in the classpath. Default: false - priority is not given to user-provided jars
        :param extra_python_files: Additional Python files that AWS Glue adds to the Python path before executing your script. Only individual files are supported, directories are not supported. Default: - no extra python files and argument is not set
        '''
        props = PythonSparkJobExecutableProps(
            glue_version=glue_version,
            python_version=python_version,
            script=script,
            extra_files=extra_files,
            extra_jars=extra_jars,
            extra_jars_first=extra_jars_first,
            extra_python_files=extra_python_files,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "pythonStreaming", [props]))

    @jsii.member(jsii_name="scalaEtl")
    @builtins.classmethod
    def scala_etl(
        cls,
        *,
        class_name: builtins.str,
        glue_version: GlueVersion,
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
    ) -> "JobExecutable":
        '''Create Scala executable props for Apache Spark ETL job.

        :param class_name: The fully qualified Scala class name that serves as the entry point for the job.
        :param glue_version: Glue version.
        :param script: The script that executes a job.
        :param extra_files: Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Default: [] - no extra files are copied to the working directory
        :param extra_jars: Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: Setting this value to true prioritizes the customer's extra JAR files in the classpath. Default: false - priority is not given to user-provided jars
        '''
        props = ScalaJobExecutableProps(
            class_name=class_name,
            glue_version=glue_version,
            script=script,
            extra_files=extra_files,
            extra_jars=extra_jars,
            extra_jars_first=extra_jars_first,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "scalaEtl", [props]))

    @jsii.member(jsii_name="scalaStreaming")
    @builtins.classmethod
    def scala_streaming(
        cls,
        *,
        class_name: builtins.str,
        glue_version: GlueVersion,
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
    ) -> "JobExecutable":
        '''Create Scala executable props for Apache Spark Streaming job.

        :param class_name: The fully qualified Scala class name that serves as the entry point for the job.
        :param glue_version: Glue version.
        :param script: The script that executes a job.
        :param extra_files: Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Default: [] - no extra files are copied to the working directory
        :param extra_jars: Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: Setting this value to true prioritizes the customer's extra JAR files in the classpath. Default: false - priority is not given to user-provided jars
        '''
        props = ScalaJobExecutableProps(
            class_name=class_name,
            glue_version=glue_version,
            script=script,
            extra_files=extra_files,
            extra_jars=extra_jars,
            extra_jars_first=extra_jars_first,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "scalaStreaming", [props]))

    @jsii.member(jsii_name="bind")
    def bind(self) -> "JobExecutableConfig":
        '''Called during Job initialization to get JobExecutableConfig.'''
        return typing.cast("JobExecutableConfig", jsii.invoke(self, "bind", []))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.JobExecutableConfig",
    jsii_struct_bases=[],
    name_mapping={
        "glue_version": "glueVersion",
        "language": "language",
        "script": "script",
        "type": "type",
        "class_name": "className",
        "extra_files": "extraFiles",
        "extra_jars": "extraJars",
        "extra_jars_first": "extraJarsFirst",
        "extra_python_files": "extraPythonFiles",
        "python_version": "pythonVersion",
    },
)
class JobExecutableConfig:
    def __init__(
        self,
        *,
        glue_version: GlueVersion,
        language: "JobLanguage",
        script: Code,
        type: "JobType",
        class_name: typing.Optional[builtins.str] = None,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
        python_version: typing.Optional["PythonVersion"] = None,
    ) -> None:
        '''Result of binding a ``JobExecutable`` into a ``Job``.

        :param glue_version: Glue version.
        :param language: The language of the job (Scala or Python).
        :param script: The script that is executed by a job.
        :param type: Specify the type of the job whether it's an Apache Spark ETL or streaming one or if it's a Python shell job.
        :param class_name: The Scala class that serves as the entry point for the job. This applies only if your the job langauage is Scala. Default: - no scala className specified
        :param extra_files: Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Default: - no extra files specified.
        :param extra_jars: Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Default: - no extra jars specified.
        :param extra_jars_first: Setting this value to true prioritizes the customer's extra JAR files in the classpath. Default: - extra jars are not prioritized.
        :param extra_python_files: Additional Python files that AWS Glue adds to the Python path before executing your script. Default: - no extra python files specified.
        :param python_version: The Python version to use. Default: - no python version specified
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JobExecutableConfig.__init__)
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
            check_type(argname="argument extra_files", value=extra_files, expected_type=type_hints["extra_files"])
            check_type(argname="argument extra_jars", value=extra_jars, expected_type=type_hints["extra_jars"])
            check_type(argname="argument extra_jars_first", value=extra_jars_first, expected_type=type_hints["extra_jars_first"])
            check_type(argname="argument extra_python_files", value=extra_python_files, expected_type=type_hints["extra_python_files"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
        self._values: typing.Dict[str, typing.Any] = {
            "glue_version": glue_version,
            "language": language,
            "script": script,
            "type": type,
        }
        if class_name is not None:
            self._values["class_name"] = class_name
        if extra_files is not None:
            self._values["extra_files"] = extra_files
        if extra_jars is not None:
            self._values["extra_jars"] = extra_jars
        if extra_jars_first is not None:
            self._values["extra_jars_first"] = extra_jars_first
        if extra_python_files is not None:
            self._values["extra_python_files"] = extra_python_files
        if python_version is not None:
            self._values["python_version"] = python_version

    @builtins.property
    def glue_version(self) -> GlueVersion:
        '''Glue version.

        :see: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
        '''
        result = self._values.get("glue_version")
        assert result is not None, "Required property 'glue_version' is missing"
        return typing.cast(GlueVersion, result)

    @builtins.property
    def language(self) -> "JobLanguage":
        '''The language of the job (Scala or Python).

        :see: ``--job-language`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("language")
        assert result is not None, "Required property 'language' is missing"
        return typing.cast("JobLanguage", result)

    @builtins.property
    def script(self) -> Code:
        '''The script that is executed by a job.'''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def type(self) -> "JobType":
        '''Specify the type of the job whether it's an Apache Spark ETL or streaming one or if it's a Python shell job.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("JobType", result)

    @builtins.property
    def class_name(self) -> typing.Optional[builtins.str]:
        '''The Scala class that serves as the entry point for the job.

        This applies only if your the job langauage is Scala.

        :default: - no scala className specified

        :see: ``--class`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("class_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_files(self) -> typing.Optional[typing.List[Code]]:
        '''Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it.

        :default: - no extra files specified.

        :see: ``--extra-files`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars(self) -> typing.Optional[typing.List[Code]]:
        '''Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script.

        :default: - no extra jars specified.

        :see: ``--extra-jars`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_jars")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars_first(self) -> typing.Optional[builtins.bool]:
        '''Setting this value to true prioritizes the customer's extra JAR files in the classpath.

        :default: - extra jars are not prioritized.

        :see: ``--user-jars-first`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_jars_first")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_python_files(self) -> typing.Optional[typing.List[Code]]:
        '''Additional Python files that AWS Glue adds to the Python path before executing your script.

        :default: - no extra python files specified.

        :see: ``--extra-py-files`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_python_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def python_version(self) -> typing.Optional["PythonVersion"]:
        '''The Python version to use.

        :default: - no python version specified
        '''
        result = self._values.get("python_version")
        return typing.cast(typing.Optional["PythonVersion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobExecutableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.JobLanguage")
class JobLanguage(enum.Enum):
    PYTHON = "PYTHON"
    '''Python.'''
    SCALA = "SCALA"
    '''Scala.'''


@jsii.data_type(
    jsii_type="cdk-extensions.glue.JobProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "executable": "executable",
        "allocated_capacity": "allocatedCapacity",
        "connections": "connections",
        "continuous_logging": "continuousLogging",
        "default_arguments": "defaultArguments",
        "description": "description",
        "enable_profiling_metrics": "enableProfilingMetrics",
        "max_capacity": "maxCapacity",
        "max_concurrent_runs": "maxConcurrentRuns",
        "max_retries": "maxRetries",
        "name": "name",
        "notify_delay_after": "notifyDelayAfter",
        "role": "role",
        "security_configuration": "securityConfiguration",
        "timeout": "timeout",
        "worker_count": "workerCount",
        "worker_type": "workerType",
    },
)
class JobProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        executable: JobExecutable,
        allocated_capacity: typing.Optional[jsii.Number] = None,
        connections: typing.Optional[typing.Sequence[Connection]] = None,
        continuous_logging: typing.Optional[typing.Union[ContinuousLoggingProps, typing.Dict[str, typing.Any]]] = None,
        default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_profiling_metrics: typing.Optional[builtins.bool] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_configuration: typing.Optional["SecurityConfiguration"] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        worker_count: typing.Optional[jsii.Number] = None,
        worker_type: typing.Optional["WorkerType"] = None,
    ) -> None:
        '''Configuration for the Glue Job resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param executable: Executable properties for the Job.
        :param allocated_capacity: The number of capacity units that are allocated to this job.
        :param connections: List of Connections for use with this job.
        :param continuous_logging: Set of properties for configuration of Continuous Logging.
        :param default_arguments: The default arguments for this job, specified as name-value pairs. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.
        :param description: A description of the job.
        :param enable_profiling_metrics: Boolean value for whether to enable Profiling Metrics.
        :param max_capacity: The number of AWS Glue data processing units (DPUs) that can be allocated when this job runs. A DPU is a relative measure of processing power that consists of 4 vCPUs of compute capacity and 16 GB of memory. Do not set Max Capacity if using WorkerType and NumberOfWorkers. The value that can be allocated for MaxCapacity depends on whether you are running a Python shell job or an Apache Spark ETL job:: - When you specify a Python shell job (JobCommand.Name="pythonshell"), you can allocate either 0.0625 or 1 DPU. The default is 0.0625 DPU. - When you specify an Apache Spark ETL job (JobCommand.Name="glueetl"), you can allocate from 2 to 100 DPUs. The default is 10 DPUs. This job type cannot have a fractional DPU allocation.
        :param max_concurrent_runs: Maximum number of concurrent executions.
        :param max_retries: The maximum number of times to retry this job after a JobRun fails.
        :param name: A name for the Job.
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.
        :param role: The name or Amazon Resource Name (ARN) of the IAM role associated with this job.
        :param security_configuration: The Security Configuration object to be applied to the Job.
        :param timeout: The job timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 2,880 minutes (48 hours).
        :param worker_count: The number of worker available the Job.
        :param worker_type: The type of predefined worker that is allocated when a job runs. Accepts a value of Standard, G.1X, or G.2X.
        '''
        if isinstance(continuous_logging, dict):
            continuous_logging = ContinuousLoggingProps(**continuous_logging)
        if __debug__:
            type_hints = typing.get_type_hints(JobProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument allocated_capacity", value=allocated_capacity, expected_type=type_hints["allocated_capacity"])
            check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
            check_type(argname="argument continuous_logging", value=continuous_logging, expected_type=type_hints["continuous_logging"])
            check_type(argname="argument default_arguments", value=default_arguments, expected_type=type_hints["default_arguments"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_profiling_metrics", value=enable_profiling_metrics, expected_type=type_hints["enable_profiling_metrics"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notify_delay_after", value=notify_delay_after, expected_type=type_hints["notify_delay_after"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
            check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "executable": executable,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if allocated_capacity is not None:
            self._values["allocated_capacity"] = allocated_capacity
        if connections is not None:
            self._values["connections"] = connections
        if continuous_logging is not None:
            self._values["continuous_logging"] = continuous_logging
        if default_arguments is not None:
            self._values["default_arguments"] = default_arguments
        if description is not None:
            self._values["description"] = description
        if enable_profiling_metrics is not None:
            self._values["enable_profiling_metrics"] = enable_profiling_metrics
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_concurrent_runs is not None:
            self._values["max_concurrent_runs"] = max_concurrent_runs
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if name is not None:
            self._values["name"] = name
        if notify_delay_after is not None:
            self._values["notify_delay_after"] = notify_delay_after
        if role is not None:
            self._values["role"] = role
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if timeout is not None:
            self._values["timeout"] = timeout
        if worker_count is not None:
            self._values["worker_count"] = worker_count
        if worker_type is not None:
            self._values["worker_type"] = worker_type

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executable(self) -> JobExecutable:
        '''Executable properties for the Job.'''
        result = self._values.get("executable")
        assert result is not None, "Required property 'executable' is missing"
        return typing.cast(JobExecutable, result)

    @builtins.property
    def allocated_capacity(self) -> typing.Optional[jsii.Number]:
        '''The number of capacity units that are allocated to this job.

        :see: `AWS::Glue::Job <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-allocatedcapacity>`_
        '''
        result = self._values.get("allocated_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def connections(self) -> typing.Optional[typing.List[Connection]]:
        '''List of Connections for use with this job.

        :see: `AWS::Glue::Job <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-connections>`_
        '''
        result = self._values.get("connections")
        return typing.cast(typing.Optional[typing.List[Connection]], result)

    @builtins.property
    def continuous_logging(self) -> typing.Optional[ContinuousLoggingProps]:
        '''Set of properties for configuration of Continuous Logging.'''
        result = self._values.get("continuous_logging")
        return typing.cast(typing.Optional[ContinuousLoggingProps], result)

    @builtins.property
    def default_arguments(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The default arguments for this job, specified as name-value pairs.

        You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.

        :see: `AWS::Glue::Job <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-defaultarguments>`_
        '''
        result = self._values.get("default_arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the job.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_profiling_metrics(self) -> typing.Optional[builtins.bool]:
        '''Boolean value for whether to enable Profiling Metrics.'''
        result = self._values.get("enable_profiling_metrics")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''The number of AWS Glue data processing units (DPUs) that can be allocated when this job runs.

        A DPU is a relative measure of processing power that consists of 4 vCPUs of compute capacity and 16 GB of memory.

        Do not set Max Capacity if using WorkerType and NumberOfWorkers.

        The value that can be allocated for MaxCapacity depends on whether you are running a Python shell job or an Apache Spark ETL job::

           - When you specify a Python shell job (JobCommand.Name="pythonshell"), you can allocate either 0.0625 or 1 DPU. The default is 0.0625 DPU.

           - When you specify an Apache Spark ETL job (JobCommand.Name="glueetl"), you can allocate from 2 to 100 DPUs. The default is 10 DPUs. This job type cannot have a fractional DPU allocation.
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of concurrent executions.

        :see: `AWS::Glue::Job ExecutionProperty <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-executionproperty.html>`_
        '''
        result = self._values.get("max_concurrent_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry this job after a JobRun fails.

        :see: `AWS::Glue::Job <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-maxretries>`_
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the Job.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notify_delay_after(self) -> typing.Optional[aws_cdk.Duration]:
        '''After a job run starts, the number of minutes to wait before sending a job run delay notification.

        :see: `AWS::Glue::Job NotificationProperty <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-notificationproperty.html>`_
        '''
        result = self._values.get("notify_delay_after")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''The name or Amazon Resource Name (ARN) of the IAM role associated with this job.'''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional["SecurityConfiguration"]:
        '''The Security Configuration object to be applied to the Job.'''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional["SecurityConfiguration"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.Duration]:
        '''The job timeout in minutes.

        This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 2,880 minutes (48 hours).

        :see: `AWS::Glue::Job <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-timeout>`_
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def worker_count(self) -> typing.Optional[jsii.Number]:
        '''The number of worker available the Job.'''
        result = self._values.get("worker_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def worker_type(self) -> typing.Optional["WorkerType"]:
        '''The type of predefined worker that is allocated when a job runs.

        Accepts a value of Standard, G.1X, or G.2X.

        :see: `AWS::Glue::Job <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-workertype>`_
        '''
        result = self._values.get("worker_type")
        return typing.cast(typing.Optional["WorkerType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.JobState")
class JobState(enum.Enum):
    '''State a Glue job must be in in order to satisfy a predicate condition to trigger a part of a workflow.'''

    FAILED = "FAILED"
    '''A job that has finished and ended with an error.'''
    STOPPED = "STOPPED"
    '''A job which was stopped before completion.'''
    SUCCEEDED = "SUCCEEDED"
    '''A job which has finished successfully.'''
    TIMEOUT = "TIMEOUT"
    '''A job which timed out without completing.'''


class JobType(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.glue.JobType"):
    '''The job type.

    If you need to use a JobType that doesn't exist as a static member, you
    can instantiate a ``JobType`` object, e.g: ``JobType.of('other name')``.
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "JobType":
        '''Custom type name.

        :param name: type name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JobType.of)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("JobType", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ETL")
    def ETL(cls) -> "JobType":
        '''Command for running a Glue ETL job.'''
        return typing.cast("JobType", jsii.sget(cls, "ETL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHON_SHELL")
    def PYTHON_SHELL(cls) -> "JobType":
        '''Command for running a Glue python shell job.'''
        return typing.cast("JobType", jsii.sget(cls, "PYTHON_SHELL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STREAMING")
    def STREAMING(cls) -> "JobType":
        '''Command for running a Glue streaming job.'''
        return typing.cast("JobType", jsii.sget(cls, "STREAMING"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of this JobType, as expected by Job resource.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class OutputFormat(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.OutputFormat",
):
    '''Absolute class name of the Hadoop ``OutputFormat`` to use when writing table files.'''

    def __init__(self, class_name: builtins.str) -> None:
        '''
        :param class_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OutputFormat.__init__)
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
        jsii.create(self.__class__, self, [class_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVRO")
    def AVRO(cls) -> InputFormat:
        '''OutputFormat for Avro files.

        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/ql/io/avro/AvroContainerOutputFormat.html
        '''
        return typing.cast(InputFormat, jsii.sget(cls, "AVRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIVE_IGNORE_KEY_TEXT")
    def HIVE_IGNORE_KEY_TEXT(cls) -> "OutputFormat":
        '''Writes text data with a null key (value only).

        :see: https://hive.apache.org/javadocs/r2.2.0/api/org/apache/hadoop/hive/ql/io/HiveIgnoreKeyTextOutputFormat.html
        '''
        return typing.cast("OutputFormat", jsii.sget(cls, "HIVE_IGNORE_KEY_TEXT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORC")
    def ORC(cls) -> InputFormat:
        '''OutputFormat for Orc files.

        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/ql/io/orc/OrcOutputFormat.html
        '''
        return typing.cast(InputFormat, jsii.sget(cls, "ORC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARQUET")
    def PARQUET(cls) -> "OutputFormat":
        '''OutputFormat for Parquet files.

        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/ql/io/parquet/MapredParquetOutputFormat.html
        '''
        return typing.cast("OutputFormat", jsii.sget(cls, "PARQUET"))

    @builtins.property
    @jsii.member(jsii_name="className")
    def class_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "className"))


@jsii.enum(jsii_type="cdk-extensions.glue.PartitionUpdateBehavior")
class PartitionUpdateBehavior(enum.Enum):
    INHERIT_FROM_TABLE = "INHERIT_FROM_TABLE"


@jsii.enum(jsii_type="cdk-extensions.glue.PredicateLogicalOperator")
class PredicateLogicalOperator(enum.Enum):
    '''Logical operator that specifies how the conditions of a predicate should be evaluated.'''

    EQUALS = "EQUALS"
    '''State equals specified value.'''


@jsii.enum(jsii_type="cdk-extensions.glue.PredicateOperator")
class PredicateOperator(enum.Enum):
    AND = "AND"
    OR = "OR"


@jsii.data_type(
    jsii_type="cdk-extensions.glue.PythonShellExecutableProps",
    jsii_struct_bases=[],
    name_mapping={
        "glue_version": "glueVersion",
        "python_version": "pythonVersion",
        "script": "script",
        "extra_files": "extraFiles",
        "extra_python_files": "extraPythonFiles",
    },
)
class PythonShellExecutableProps:
    def __init__(
        self,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
    ) -> None:
        '''Props for creating a Python shell job executable.

        :param glue_version: Glue version.
        :param python_version: The Python version to use.
        :param script: The script that executes a job.
        :param extra_files: Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Default: [] - no extra files are copied to the working directory
        :param extra_python_files: Additional Python files that AWS Glue adds to the Python path before executing your script. Only individual files are supported, directories are not supported. Default: - no extra python files and argument is not set
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PythonShellExecutableProps.__init__)
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument extra_files", value=extra_files, expected_type=type_hints["extra_files"])
            check_type(argname="argument extra_python_files", value=extra_python_files, expected_type=type_hints["extra_python_files"])
        self._values: typing.Dict[str, typing.Any] = {
            "glue_version": glue_version,
            "python_version": python_version,
            "script": script,
        }
        if extra_files is not None:
            self._values["extra_files"] = extra_files
        if extra_python_files is not None:
            self._values["extra_python_files"] = extra_python_files

    @builtins.property
    def glue_version(self) -> GlueVersion:
        '''Glue version.

        :see: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
        '''
        result = self._values.get("glue_version")
        assert result is not None, "Required property 'glue_version' is missing"
        return typing.cast(GlueVersion, result)

    @builtins.property
    def python_version(self) -> "PythonVersion":
        '''The Python version to use.'''
        result = self._values.get("python_version")
        assert result is not None, "Required property 'python_version' is missing"
        return typing.cast("PythonVersion", result)

    @builtins.property
    def script(self) -> Code:
        '''The script that executes a job.'''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def extra_files(self) -> typing.Optional[typing.List[Code]]:
        '''Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it.

        Only individual files are supported, directories are not supported.

        :default: [] - no extra files are copied to the working directory

        :see: ``--extra-files`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_python_files(self) -> typing.Optional[typing.List[Code]]:
        '''Additional Python files that AWS Glue adds to the Python path before executing your script.

        Only individual files are supported, directories are not supported.

        :default: - no extra python files and argument is not set

        :see: ``--extra-py-files`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_python_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonShellExecutableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.glue.PythonSparkJobExecutableProps",
    jsii_struct_bases=[],
    name_mapping={
        "glue_version": "glueVersion",
        "python_version": "pythonVersion",
        "script": "script",
        "extra_files": "extraFiles",
        "extra_jars": "extraJars",
        "extra_jars_first": "extraJarsFirst",
        "extra_python_files": "extraPythonFiles",
    },
)
class PythonSparkJobExecutableProps:
    def __init__(
        self,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
    ) -> None:
        '''Props for creating a Python Spark (ETL or Streaming) job executable.

        :param glue_version: Glue version.
        :param python_version: The Python version to use.
        :param script: The script that executes a job.
        :param extra_files: Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Default: [] - no extra files are copied to the working directory
        :param extra_jars: Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: Setting this value to true prioritizes the customer's extra JAR files in the classpath. Default: false - priority is not given to user-provided jars
        :param extra_python_files: Additional Python files that AWS Glue adds to the Python path before executing your script. Only individual files are supported, directories are not supported. Default: - no extra python files and argument is not set
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PythonSparkJobExecutableProps.__init__)
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument extra_files", value=extra_files, expected_type=type_hints["extra_files"])
            check_type(argname="argument extra_jars", value=extra_jars, expected_type=type_hints["extra_jars"])
            check_type(argname="argument extra_jars_first", value=extra_jars_first, expected_type=type_hints["extra_jars_first"])
            check_type(argname="argument extra_python_files", value=extra_python_files, expected_type=type_hints["extra_python_files"])
        self._values: typing.Dict[str, typing.Any] = {
            "glue_version": glue_version,
            "python_version": python_version,
            "script": script,
        }
        if extra_files is not None:
            self._values["extra_files"] = extra_files
        if extra_jars is not None:
            self._values["extra_jars"] = extra_jars
        if extra_jars_first is not None:
            self._values["extra_jars_first"] = extra_jars_first
        if extra_python_files is not None:
            self._values["extra_python_files"] = extra_python_files

    @builtins.property
    def glue_version(self) -> GlueVersion:
        '''Glue version.

        :see: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
        '''
        result = self._values.get("glue_version")
        assert result is not None, "Required property 'glue_version' is missing"
        return typing.cast(GlueVersion, result)

    @builtins.property
    def python_version(self) -> "PythonVersion":
        '''The Python version to use.'''
        result = self._values.get("python_version")
        assert result is not None, "Required property 'python_version' is missing"
        return typing.cast("PythonVersion", result)

    @builtins.property
    def script(self) -> Code:
        '''The script that executes a job.'''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def extra_files(self) -> typing.Optional[typing.List[Code]]:
        '''Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it.

        Only individual files are supported, directories are not supported.

        :default: [] - no extra files are copied to the working directory

        :see: ``--extra-files`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars(self) -> typing.Optional[typing.List[Code]]:
        '''Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported.

        :default: [] - no extra jars are added to the classpath

        :see: ``--extra-jars`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_jars")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars_first(self) -> typing.Optional[builtins.bool]:
        '''Setting this value to true prioritizes the customer's extra JAR files in the classpath.

        :default: false - priority is not given to user-provided jars

        :see: ``--user-jars-first`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_jars_first")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_python_files(self) -> typing.Optional[typing.List[Code]]:
        '''Additional Python files that AWS Glue adds to the Python path before executing your script.

        Only individual files are supported, directories are not supported.

        :default: - no extra python files and argument is not set

        :see: ``--extra-py-files`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_python_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonSparkJobExecutableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.PythonVersion")
class PythonVersion(enum.Enum):
    THREE = "THREE"
    '''Python 3 (the exact version depends on GlueVersion and JobCommand used).'''
    TWO = "TWO"
    '''Python 2 (the exact version depends on GlueVersion and JobCommand used).'''


@jsii.enum(jsii_type="cdk-extensions.glue.RecrawlBehavior")
class RecrawlBehavior(enum.Enum):
    EVENT_MODE = "EVENT_MODE"
    EVERYTHING = "EVERYTHING"
    NEW_FOLDERS_ONLY = "NEW_FOLDERS_ONLY"


class S3Code(Code, metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.glue.S3Code"):
    '''Glue job Code from an S3 bucket.'''

    def __init__(self, bucket: aws_cdk.aws_s3.IBucket, key: builtins.str) -> None:
        '''
        :param bucket: -
        :param key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Code.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        jsii.create(self.__class__, self, [bucket, key])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.Construct,
        grantable: aws_cdk.aws_iam.IGrantable,
    ) -> CodeConfig:
        '''Called when the Job is initialized to allow this object to bind.

        :param _scope: -
        :param grantable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Code.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument grantable", value=grantable, expected_type=type_hints["grantable"])
        return typing.cast(CodeConfig, jsii.invoke(self, "bind", [_scope, grantable]))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.S3Encryption",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "kms_key": "kmsKey"},
)
class S3Encryption:
    def __init__(
        self,
        *,
        mode: "S3EncryptionMode",
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        '''S3 encryption configuration.

        :param mode: Encryption mode.
        :param kms_key: The KMS key to be used to encrypt the data. Default: no kms key if mode = S3_MANAGED. A key will be created if one is not provided and mode = KMS.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Encryption.__init__)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "mode": mode,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def mode(self) -> "S3EncryptionMode":
        '''Encryption mode.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast("S3EncryptionMode", result)

    @builtins.property
    def kms_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''The KMS key to be used to encrypt the data.

        :default: no kms key if mode = S3_MANAGED. A key will be created if one is not provided and mode = KMS.
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Encryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.S3EncryptionMode")
class S3EncryptionMode(enum.Enum):
    '''Encryption mode for S3.

    :see: https://docs.aws.amazon.com/glue/latest/webapi/API_S3Encryption.html#Glue-Type-S3Encryption-S3EncryptionMode
    '''

    KMS = "KMS"
    '''Server-side encryption (SSE) with an AWS KMS key managed by the account owner.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html
    '''
    S3_MANAGED = "S3_MANAGED"
    '''Server side encryption (SSE) with an Amazon S3-managed key.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html
    '''


@jsii.implements(ICrawlerTarget)
class S3Target(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.glue.S3Target"):
    def __init__(
        self,
        bucket: aws_cdk.aws_s3.IBucket,
        *,
        connection: typing.Optional[Connection] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        sample_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: -
        :param connection: A {@link aws-glue.Connection | "Connection" } object to connect to the target with.
        :param exclusions: A list of glob patterns used to exclude from the crawl.
        :param key_prefix: A Prefix Key for identification and organization of objects in the bucket.
        :param sample_size: Sets the number of files in each leaf folder to be crawled when crawling sample files in a dataset. If not set, all the files are crawled. A valid value is an integer between 1 and 249.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Target.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        options = S3TargetOptions(
            connection=connection,
            exclusions=exclusions,
            key_prefix=key_prefix,
            sample_size=sample_size,
        )

        jsii.create(self.__class__, self, [bucket, options])

    @jsii.member(jsii_name="addExclusion")
    def add_exclusion(self, exclusion: builtins.str) -> None:
        '''
        :param exclusion: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Target.add_exclusion)
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
        return typing.cast(None, jsii.invoke(self, "addExclusion", [exclusion]))

    @jsii.member(jsii_name="bind")
    def bind(self, crawler: "Crawler") -> CrawlerTargetCollection:
        '''
        :param crawler: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Target.bind)
            check_type(argname="argument crawler", value=crawler, expected_type=type_hints["crawler"])
        return typing.cast(CrawlerTargetCollection, jsii.invoke(self, "bind", [crawler]))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''Bucket to use as the Target.'''
        return typing.cast(aws_cdk.aws_s3.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(self) -> typing.Optional[Connection]:
        '''{@link S3TargetOptions.connection}.'''
        return typing.cast(typing.Optional[Connection], jsii.get(self, "connection"))

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''{@link S3TargetOptions.exclusions}.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusions"))

    @builtins.property
    @jsii.member(jsii_name="keyPrefix")
    def key_prefix(self) -> typing.Optional[builtins.str]:
        '''{@link S3TargetOptions.keyPrefix}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPrefix"))

    @builtins.property
    @jsii.member(jsii_name="sampleSize")
    def sample_size(self) -> typing.Optional[builtins.str]:
        '''{@link S3TargetOptions.sampleSize}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sampleSize"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.S3TargetOptions",
    jsii_struct_bases=[],
    name_mapping={
        "connection": "connection",
        "exclusions": "exclusions",
        "key_prefix": "keyPrefix",
        "sample_size": "sampleSize",
    },
)
class S3TargetOptions:
    def __init__(
        self,
        *,
        connection: typing.Optional[Connection] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        sample_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for Crawler S3 target.

        :param connection: A {@link aws-glue.Connection | "Connection" } object to connect to the target with.
        :param exclusions: A list of glob patterns used to exclude from the crawl.
        :param key_prefix: A Prefix Key for identification and organization of objects in the bucket.
        :param sample_size: Sets the number of files in each leaf folder to be crawled when crawling sample files in a dataset. If not set, all the files are crawled. A valid value is an integer between 1 and 249.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3TargetOptions.__init__)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
            check_type(argname="argument sample_size", value=sample_size, expected_type=type_hints["sample_size"])
        self._values: typing.Dict[str, typing.Any] = {}
        if connection is not None:
            self._values["connection"] = connection
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if key_prefix is not None:
            self._values["key_prefix"] = key_prefix
        if sample_size is not None:
            self._values["sample_size"] = sample_size

    @builtins.property
    def connection(self) -> typing.Optional[Connection]:
        '''A {@link aws-glue.Connection | "Connection" } object to connect to the target with.'''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[Connection], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of glob patterns used to exclude from the crawl.

        :see: `For More Information <https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html>`_
        '''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def key_prefix(self) -> typing.Optional[builtins.str]:
        '''A Prefix Key for identification and organization of objects in the bucket.'''
        result = self._values.get("key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_size(self) -> typing.Optional[builtins.str]:
        '''Sets the number of files in each leaf folder to be crawled when crawling sample files in a dataset.

        If not set, all the files are crawled. A valid value is an integer between 1 and 249.

        :see: `AWS::Glue::Crawler S3Target <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html#cfn-glue-crawler-s3target-samplesize>`_
        '''
        result = self._values.get("sample_size")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.glue.ScalaJobExecutableProps",
    jsii_struct_bases=[],
    name_mapping={
        "class_name": "className",
        "glue_version": "glueVersion",
        "script": "script",
        "extra_files": "extraFiles",
        "extra_jars": "extraJars",
        "extra_jars_first": "extraJarsFirst",
    },
)
class ScalaJobExecutableProps:
    def __init__(
        self,
        *,
        class_name: builtins.str,
        glue_version: GlueVersion,
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Props for creating a Scala Spark (ETL or Streaming) job executable.

        :param class_name: The fully qualified Scala class name that serves as the entry point for the job.
        :param glue_version: Glue version.
        :param script: The script that executes a job.
        :param extra_files: Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Default: [] - no extra files are copied to the working directory
        :param extra_jars: Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: Setting this value to true prioritizes the customer's extra JAR files in the classpath. Default: false - priority is not given to user-provided jars
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ScalaJobExecutableProps.__init__)
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument extra_files", value=extra_files, expected_type=type_hints["extra_files"])
            check_type(argname="argument extra_jars", value=extra_jars, expected_type=type_hints["extra_jars"])
            check_type(argname="argument extra_jars_first", value=extra_jars_first, expected_type=type_hints["extra_jars_first"])
        self._values: typing.Dict[str, typing.Any] = {
            "class_name": class_name,
            "glue_version": glue_version,
            "script": script,
        }
        if extra_files is not None:
            self._values["extra_files"] = extra_files
        if extra_jars is not None:
            self._values["extra_jars"] = extra_jars
        if extra_jars_first is not None:
            self._values["extra_jars_first"] = extra_jars_first

    @builtins.property
    def class_name(self) -> builtins.str:
        '''The fully qualified Scala class name that serves as the entry point for the job.

        :see: ``--class`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("class_name")
        assert result is not None, "Required property 'class_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def glue_version(self) -> GlueVersion:
        '''Glue version.

        :see: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
        '''
        result = self._values.get("glue_version")
        assert result is not None, "Required property 'glue_version' is missing"
        return typing.cast(GlueVersion, result)

    @builtins.property
    def script(self) -> Code:
        '''The script that executes a job.'''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def extra_files(self) -> typing.Optional[typing.List[Code]]:
        '''Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it.

        Only individual files are supported, directories are not supported.

        :default: [] - no extra files are copied to the working directory

        :see: ``--extra-files`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars(self) -> typing.Optional[typing.List[Code]]:
        '''Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported.

        :default: [] - no extra jars are added to the classpath

        :see: ``--extra-jars`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_jars")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars_first(self) -> typing.Optional[builtins.bool]:
        '''Setting this value to true prioritizes the customer's extra JAR files in the classpath.

        :default: false - priority is not given to user-provided jars

        :see: ``--user-jars-first`` in https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        '''
        result = self._values.get("extra_jars_first")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScalaJobExecutableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityConfiguration(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.SecurityConfiguration",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cloud_watch_encryption: typing.Optional[typing.Union[CloudWatchEncryption, typing.Dict[str, typing.Any]]] = None,
        job_bookmarks_encryption: typing.Optional[typing.Union[JobBookmarksEncryption, typing.Dict[str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        s3_encryption: typing.Optional[typing.Union[S3Encryption, typing.Dict[str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_watch_encryption: Cloudwatch Encryption Settings.
        :param job_bookmarks_encryption: The encryption configuration for job bookmarks.
        :param name: Name for the Security Configuration.
        :param s3_encryption: The encyption configuration for Amazon Simple Storage Service (Amazon S3) data.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SecurityConfiguration.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecurityConfigurationProps(
            cloud_watch_encryption=cloud_watch_encryption,
            job_bookmarks_encryption=job_bookmarks_encryption,
            name=name,
            s3_encryption=s3_encryption,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> aws_cdk.aws_kms.Key:
        return typing.cast(aws_cdk.aws_kms.Key, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_glue.CfnSecurityConfiguration:
        return typing.cast(aws_cdk.aws_glue.CfnSecurityConfiguration, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigurationName")
    def security_configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchEncryption")
    def cloud_watch_encryption(self) -> typing.Optional[CloudWatchEncryption]:
        '''{@link SecurityConfigurationProps.cloudWatchEncryption}.'''
        return typing.cast(typing.Optional[CloudWatchEncryption], jsii.get(self, "cloudWatchEncryption"))

    @builtins.property
    @jsii.member(jsii_name="jobBookmarksEncryption")
    def job_bookmarks_encryption(self) -> typing.Optional[JobBookmarksEncryption]:
        '''{@link SecurityConfigurationProps.jobBookmarksEncryption}.'''
        return typing.cast(typing.Optional[JobBookmarksEncryption], jsii.get(self, "jobBookmarksEncryption"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''{@link SecurityConfigurationProps.name}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="s3Encryption")
    def s3_encryption(self) -> typing.Optional[S3Encryption]:
        '''{@link SecurityConfigurationProps.s3Encryption}.'''
        return typing.cast(typing.Optional[S3Encryption], jsii.get(self, "s3Encryption"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.SecurityConfigurationProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cloud_watch_encryption": "cloudWatchEncryption",
        "job_bookmarks_encryption": "jobBookmarksEncryption",
        "name": "name",
        "s3_encryption": "s3Encryption",
    },
)
class SecurityConfigurationProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cloud_watch_encryption: typing.Optional[typing.Union[CloudWatchEncryption, typing.Dict[str, typing.Any]]] = None,
        job_bookmarks_encryption: typing.Optional[typing.Union[JobBookmarksEncryption, typing.Dict[str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        s3_encryption: typing.Optional[typing.Union[S3Encryption, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''Configuration for the Glue SecurityConfiguration resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cloud_watch_encryption: Cloudwatch Encryption Settings.
        :param job_bookmarks_encryption: The encryption configuration for job bookmarks.
        :param name: Name for the Security Configuration.
        :param s3_encryption: The encyption configuration for Amazon Simple Storage Service (Amazon S3) data.
        '''
        if isinstance(cloud_watch_encryption, dict):
            cloud_watch_encryption = CloudWatchEncryption(**cloud_watch_encryption)
        if isinstance(job_bookmarks_encryption, dict):
            job_bookmarks_encryption = JobBookmarksEncryption(**job_bookmarks_encryption)
        if isinstance(s3_encryption, dict):
            s3_encryption = S3Encryption(**s3_encryption)
        if __debug__:
            type_hints = typing.get_type_hints(SecurityConfigurationProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cloud_watch_encryption", value=cloud_watch_encryption, expected_type=type_hints["cloud_watch_encryption"])
            check_type(argname="argument job_bookmarks_encryption", value=job_bookmarks_encryption, expected_type=type_hints["job_bookmarks_encryption"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3_encryption", value=s3_encryption, expected_type=type_hints["s3_encryption"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if cloud_watch_encryption is not None:
            self._values["cloud_watch_encryption"] = cloud_watch_encryption
        if job_bookmarks_encryption is not None:
            self._values["job_bookmarks_encryption"] = job_bookmarks_encryption
        if name is not None:
            self._values["name"] = name
        if s3_encryption is not None:
            self._values["s3_encryption"] = s3_encryption

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_watch_encryption(self) -> typing.Optional[CloudWatchEncryption]:
        '''Cloudwatch Encryption Settings.

        :see: `AWS::Glue::SecurityConfiguration EncryptionConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration-cloudwatchencryption>`_
        '''
        result = self._values.get("cloud_watch_encryption")
        return typing.cast(typing.Optional[CloudWatchEncryption], result)

    @builtins.property
    def job_bookmarks_encryption(self) -> typing.Optional[JobBookmarksEncryption]:
        '''The encryption configuration for job bookmarks.

        :see: `AWS::Glue::SecurityConfiguration EncryptionConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration-jobbookmarksencryption>`_
        '''
        result = self._values.get("job_bookmarks_encryption")
        return typing.cast(typing.Optional[JobBookmarksEncryption], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name for the Security Configuration.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_encryption(self) -> typing.Optional[S3Encryption]:
        '''The encyption configuration for Amazon Simple Storage Service (Amazon S3) data.

        :see: `AWS::Glue::SecurityConfiguration EncryptionConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration-s3encryptions>`_
        '''
        result = self._values.get("s3_encryption")
        return typing.cast(typing.Optional[S3Encryption], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SerializationLibrary(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.SerializationLibrary",
):
    '''Serialization library to use when serializing/deserializing (SerDe) table records.

    :see: https://cwiki.apache.org/confluence/display/Hive/SerDe
    '''

    def __init__(self, class_name: builtins.str) -> None:
        '''
        :param class_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SerializationLibrary.__init__)
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
        jsii.create(self.__class__, self, [class_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVRO")
    def AVRO(cls) -> "SerializationLibrary":
        '''
        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/serde2/avro/AvroSerDe.html
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "AVRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDTRAIL")
    def CLOUDTRAIL(cls) -> "SerializationLibrary":
        '''
        :see: https://docs.aws.amazon.com/athena/latest/ug/cloudtrail.html
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "CLOUDTRAIL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GROK")
    def GROK(cls) -> "SerializationLibrary":
        '''
        :see: https://docs.aws.amazon.com/athena/latest/ug/grok.html
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "GROK"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIVE_JSON")
    def HIVE_JSON(cls) -> "SerializationLibrary":
        '''
        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hive/hcatalog/data/JsonSerDe.html
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "HIVE_JSON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LAZY_SIMPLE")
    def LAZY_SIMPLE(cls) -> "SerializationLibrary":
        '''
        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/serde2/lazy/LazySimpleSerDe.html
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "LAZY_SIMPLE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPEN_CSV")
    def OPEN_CSV(cls) -> "SerializationLibrary":
        '''
        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/serde2/OpenCSVSerde.html
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "OPEN_CSV"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPENX_JSON")
    def OPENX_JSON(cls) -> "SerializationLibrary":
        '''
        :see: https://github.com/rcongiu/Hive-JSON-Serde
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "OPENX_JSON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORC")
    def ORC(cls) -> "SerializationLibrary":
        '''
        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/ql/io/orc/OrcSerde.html
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "ORC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARQUET")
    def PARQUET(cls) -> "SerializationLibrary":
        '''
        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/ql/io/parquet/serde/ParquetHiveSerDe.html
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "PARQUET"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REGEXP")
    def REGEXP(cls) -> "SerializationLibrary":
        '''
        :see: https://hive.apache.org/javadocs/r1.2.2/api/org/apache/hadoop/hive/serde2/RegexSerDe.html
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "REGEXP"))

    @builtins.property
    @jsii.member(jsii_name="className")
    def class_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "className"))


class StructColumn(
    Column,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.StructColumn",
):
    def __init__(
        self,
        *,
        data: typing.Optional[typing.Sequence[Column]] = None,
        comment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data: 
        :param comment: 
        :param name: 
        '''
        props = StructColumnProps(data=data, comment=comment, name=name)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addColumn")
    def add_column(self, column: Column) -> None:
        '''
        :param column: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StructColumn.add_column)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
        return typing.cast(None, jsii.invoke(self, "addColumn", [column]))

    @builtins.property
    @jsii.member(jsii_name="typeString")
    def type_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeString"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.StructColumnProps",
    jsii_struct_bases=[ColumnProps],
    name_mapping={"comment": "comment", "name": "name", "data": "data"},
)
class StructColumnProps(ColumnProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Sequence[Column]] = None,
    ) -> None:
        '''
        :param comment: 
        :param name: 
        :param data: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StructColumnProps.__init__)
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if name is not None:
            self._values["name"] = name
        if data is not None:
            self._values["data"] = data

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.List[Column]]:
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.List[Column]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StructColumnProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Table(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.Table",
):
    '''Creates a Table resource specifying tabular data in the Glue Database.

    :see: `AWS::Glue::Table <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html>`_
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        database: Database,
        columns: typing.Optional[typing.Sequence[Column]] = None,
        compressed: typing.Optional[builtins.bool] = None,
        data_format: typing.Optional[DataFormat] = None,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partition_keys: typing.Optional[typing.Sequence[Column]] = None,
        retention: typing.Optional[aws_cdk.Duration] = None,
        serde_name: typing.Optional[builtins.str] = None,
        serde_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        storage_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stored_as_sub_directories: typing.Optional[builtins.bool] = None,
        table_type: typing.Optional["TableType"] = None,
        target_table: typing.Optional["Table"] = None,
        view_expanded_text: typing.Optional[builtins.str] = None,
        view_original_text: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the Table class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param database: Database object to add Table to.
        :param columns: A list of the Columns in the table.
        :param compressed: True if the data in the table is compressed, or False if not.
        :param data_format: DataFormat object indicating the expected input/output format.
        :param description: A description for the Table.
        :param location: The physical location of the table. By default, this takes the form of the warehouse location, followed by the database location in the warehouse, followed by the table name.
        :param name: A name for the Table.
        :param owner: The table owner. Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations.
        :param parameters: These key-value pairs define properties associated with the table.
        :param partition_keys: A list of columns by which the table is partitioned. Only primitive types are supported as partition keys.
        :param retention: The retention time for this table.
        :param serde_name: Name of the SerDe.
        :param serde_parameters: These key-value pairs define initialization parameters for the SerDe.
        :param storage_parameters: The user-supplied properties in key-value form.
        :param stored_as_sub_directories: True if the table data is stored in subdirectories, or False if not.
        :param table_type: The type of this table. AWS Glue will create tables with the EXTERNAL_TABLE type. Other services, such as Athena, may create tables with additional table types.
        :param target_table: A TableIdentifier structure that describes a target table for resource linking.
        :param view_expanded_text: Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations.
        :param view_original_text: Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations. If the table is a VIRTUAL_VIEW, certain Athena configuration encoded in base64.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Table.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TableProps(
            database=database,
            columns=columns,
            compressed=compressed,
            data_format=data_format,
            description=description,
            location=location,
            name=name,
            owner=owner,
            parameters=parameters,
            partition_keys=partition_keys,
            retention=retention,
            serde_name=serde_name,
            serde_parameters=serde_parameters,
            storage_parameters=storage_parameters,
            stored_as_sub_directories=stored_as_sub_directories,
            table_type=table_type,
            target_table=target_table,
            view_expanded_text=view_expanded_text,
            view_original_text=view_original_text,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addColumn")
    def add_column(self, column: Column) -> None:
        '''
        :param column: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Table.add_column)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
        return typing.cast(None, jsii.invoke(self, "addColumn", [column]))

    @jsii.member(jsii_name="addParameter")
    def add_parameter(self, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Table.add_parameter)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addParameter", [key, value]))

    @jsii.member(jsii_name="addPartitionKey")
    def add_partition_key(self, column: Column) -> None:
        '''
        :param column: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Table.add_partition_key)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
        return typing.cast(None, jsii.invoke(self, "addPartitionKey", [column]))

    @jsii.member(jsii_name="addSerdeParameter")
    def add_serde_parameter(self, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Table.add_serde_parameter)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addSerdeParameter", [key, value]))

    @jsii.member(jsii_name="addStorageParameter")
    def add_storage_parameter(self, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Table.add_storage_parameter)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addStorageParameter", [key, value]))

    @jsii.member(jsii_name="renderStorageDescriptor")
    def _render_storage_descriptor(
        self,
    ) -> typing.Optional[aws_cdk.aws_glue.CfnTable.StorageDescriptorProperty]:
        return typing.cast(typing.Optional[aws_cdk.aws_glue.CfnTable.StorageDescriptorProperty], jsii.invoke(self, "renderStorageDescriptor", []))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> Database:
        '''{@link TableProps.database:}.'''
        return typing.cast(Database, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_glue.CfnTable:
        return typing.cast(aws_cdk.aws_glue.CfnTable, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="compressed")
    def compressed(self) -> typing.Optional[builtins.bool]:
        '''{@link TableProps.compressed}.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "compressed"))

    @builtins.property
    @jsii.member(jsii_name="dataFormat")
    def data_format(self) -> typing.Optional[DataFormat]:
        '''{@link TableProps.dataFormat}.'''
        return typing.cast(typing.Optional[DataFormat], jsii.get(self, "dataFormat"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''{@link TableProps.description}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> typing.Optional[builtins.str]:
        '''{@link TableProps.location}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''{@link TableProps.name}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> typing.Optional[builtins.str]:
        '''{@link TableProps.owner}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="retention")
    def retention(self) -> typing.Optional[aws_cdk.Duration]:
        '''{@link TableProps.retention}.'''
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "retention"))

    @builtins.property
    @jsii.member(jsii_name="serdeName")
    def serde_name(self) -> typing.Optional[builtins.str]:
        '''{@link TableProps.serdeName}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serdeName"))

    @builtins.property
    @jsii.member(jsii_name="storedAsSubDirectories")
    def stored_as_sub_directories(self) -> typing.Optional[builtins.bool]:
        '''{@link TableProps.storedAsSubDirectories}.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "storedAsSubDirectories"))

    @builtins.property
    @jsii.member(jsii_name="tableType")
    def table_type(self) -> typing.Optional["TableType"]:
        '''{@link TableProps.tableType}.'''
        return typing.cast(typing.Optional["TableType"], jsii.get(self, "tableType"))

    @builtins.property
    @jsii.member(jsii_name="targetTable")
    def target_table(self) -> typing.Optional["Table"]:
        '''{@link TableProps.targetTable}.'''
        return typing.cast(typing.Optional["Table"], jsii.get(self, "targetTable"))

    @builtins.property
    @jsii.member(jsii_name="viewExpandedText")
    def view_expanded_text(self) -> typing.Optional[builtins.str]:
        '''{@link TableProps.viewExpandedText}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "viewExpandedText"))

    @builtins.property
    @jsii.member(jsii_name="viewOriginalText")
    def view_original_text(self) -> typing.Optional[builtins.str]:
        '''{@link TableProps.viewOriginalText}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "viewOriginalText"))


@jsii.enum(jsii_type="cdk-extensions.glue.TableGroupingPolicy")
class TableGroupingPolicy(enum.Enum):
    COMBINE_COMPATIBLE_SCHEMAS = "COMBINE_COMPATIBLE_SCHEMAS"


@jsii.data_type(
    jsii_type="cdk-extensions.glue.TableProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "database": "database",
        "columns": "columns",
        "compressed": "compressed",
        "data_format": "dataFormat",
        "description": "description",
        "location": "location",
        "name": "name",
        "owner": "owner",
        "parameters": "parameters",
        "partition_keys": "partitionKeys",
        "retention": "retention",
        "serde_name": "serdeName",
        "serde_parameters": "serdeParameters",
        "storage_parameters": "storageParameters",
        "stored_as_sub_directories": "storedAsSubDirectories",
        "table_type": "tableType",
        "target_table": "targetTable",
        "view_expanded_text": "viewExpandedText",
        "view_original_text": "viewOriginalText",
    },
)
class TableProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        database: Database,
        columns: typing.Optional[typing.Sequence[Column]] = None,
        compressed: typing.Optional[builtins.bool] = None,
        data_format: typing.Optional[DataFormat] = None,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partition_keys: typing.Optional[typing.Sequence[Column]] = None,
        retention: typing.Optional[aws_cdk.Duration] = None,
        serde_name: typing.Optional[builtins.str] = None,
        serde_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        storage_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stored_as_sub_directories: typing.Optional[builtins.bool] = None,
        table_type: typing.Optional["TableType"] = None,
        target_table: typing.Optional[Table] = None,
        view_expanded_text: typing.Optional[builtins.str] = None,
        view_original_text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for Table.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param database: Database object to add Table to.
        :param columns: A list of the Columns in the table.
        :param compressed: True if the data in the table is compressed, or False if not.
        :param data_format: DataFormat object indicating the expected input/output format.
        :param description: A description for the Table.
        :param location: The physical location of the table. By default, this takes the form of the warehouse location, followed by the database location in the warehouse, followed by the table name.
        :param name: A name for the Table.
        :param owner: The table owner. Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations.
        :param parameters: These key-value pairs define properties associated with the table.
        :param partition_keys: A list of columns by which the table is partitioned. Only primitive types are supported as partition keys.
        :param retention: The retention time for this table.
        :param serde_name: Name of the SerDe.
        :param serde_parameters: These key-value pairs define initialization parameters for the SerDe.
        :param storage_parameters: The user-supplied properties in key-value form.
        :param stored_as_sub_directories: True if the table data is stored in subdirectories, or False if not.
        :param table_type: The type of this table. AWS Glue will create tables with the EXTERNAL_TABLE type. Other services, such as Athena, may create tables with additional table types.
        :param target_table: A TableIdentifier structure that describes a target table for resource linking.
        :param view_expanded_text: Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations.
        :param view_original_text: Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations. If the table is a VIRTUAL_VIEW, certain Athena configuration encoded in base64.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TableProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument compressed", value=compressed, expected_type=type_hints["compressed"])
            check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument partition_keys", value=partition_keys, expected_type=type_hints["partition_keys"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
            check_type(argname="argument serde_name", value=serde_name, expected_type=type_hints["serde_name"])
            check_type(argname="argument serde_parameters", value=serde_parameters, expected_type=type_hints["serde_parameters"])
            check_type(argname="argument storage_parameters", value=storage_parameters, expected_type=type_hints["storage_parameters"])
            check_type(argname="argument stored_as_sub_directories", value=stored_as_sub_directories, expected_type=type_hints["stored_as_sub_directories"])
            check_type(argname="argument table_type", value=table_type, expected_type=type_hints["table_type"])
            check_type(argname="argument target_table", value=target_table, expected_type=type_hints["target_table"])
            check_type(argname="argument view_expanded_text", value=view_expanded_text, expected_type=type_hints["view_expanded_text"])
            check_type(argname="argument view_original_text", value=view_original_text, expected_type=type_hints["view_original_text"])
        self._values: typing.Dict[str, typing.Any] = {
            "database": database,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if columns is not None:
            self._values["columns"] = columns
        if compressed is not None:
            self._values["compressed"] = compressed
        if data_format is not None:
            self._values["data_format"] = data_format
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if owner is not None:
            self._values["owner"] = owner
        if parameters is not None:
            self._values["parameters"] = parameters
        if partition_keys is not None:
            self._values["partition_keys"] = partition_keys
        if retention is not None:
            self._values["retention"] = retention
        if serde_name is not None:
            self._values["serde_name"] = serde_name
        if serde_parameters is not None:
            self._values["serde_parameters"] = serde_parameters
        if storage_parameters is not None:
            self._values["storage_parameters"] = storage_parameters
        if stored_as_sub_directories is not None:
            self._values["stored_as_sub_directories"] = stored_as_sub_directories
        if table_type is not None:
            self._values["table_type"] = table_type
        if target_table is not None:
            self._values["target_table"] = target_table
        if view_expanded_text is not None:
            self._values["view_expanded_text"] = view_expanded_text
        if view_original_text is not None:
            self._values["view_original_text"] = view_original_text

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database(self) -> Database:
        '''Database object to add Table to.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(Database, result)

    @builtins.property
    def columns(self) -> typing.Optional[typing.List[Column]]:
        '''A list of the Columns in the table.

        :see: `AWS::Glue::Table StorageDescriptor <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-columns>`_
        '''
        result = self._values.get("columns")
        return typing.cast(typing.Optional[typing.List[Column]], result)

    @builtins.property
    def compressed(self) -> typing.Optional[builtins.bool]:
        '''True if the data in the table is compressed, or False if not.

        :see: `AWS::Glue::Table StorageDescriptor <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-compressed>`_
        '''
        result = self._values.get("compressed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def data_format(self) -> typing.Optional[DataFormat]:
        '''DataFormat object indicating the expected input/output format.'''
        result = self._values.get("data_format")
        return typing.cast(typing.Optional[DataFormat], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the Table.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The physical location of the table.

        By default, this takes the form of the warehouse location, followed by the database location in the warehouse, followed by the table name.

        :see: `AWS::Glue::Table StorageDescriptor <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-location>`_
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the Table.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''The table owner.

        Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations.

        :see: `AWS::Glue::Table TableInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-owner>`_
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''These key-value pairs define properties associated with the table.

        :see: `AWS::Glue::Table TableInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-parameters>`_
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def partition_keys(self) -> typing.Optional[typing.List[Column]]:
        '''A list of columns by which the table is partitioned.

        Only primitive types are supported as partition keys.

        :see: `AWS::Glue::Table TableInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-parameterskeys>`_
        '''
        result = self._values.get("partition_keys")
        return typing.cast(typing.Optional[typing.List[Column]], result)

    @builtins.property
    def retention(self) -> typing.Optional[aws_cdk.Duration]:
        '''The retention time for this table.

        :see: `AWS::Glue::Table TableInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-retention>`_
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def serde_name(self) -> typing.Optional[builtins.str]:
        '''Name of the SerDe.

        :see: `AWS::Glue::Table SerdeInfo <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-serdeinfo.html#cfn-glue-table-serdeinfo-name>`_
        '''
        result = self._values.get("serde_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serde_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''These key-value pairs define initialization parameters for the SerDe.

        :see: `AWS::Glue::Table SerdeInfo <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-serdeinfo.html#cfn-glue-table-serdeinfo-parameters>`_
        '''
        result = self._values.get("serde_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def storage_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The user-supplied properties in key-value form.

        :see: `AWS::Glue::Table StorageDescriptor <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-parameters>`_
        '''
        result = self._values.get("storage_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def stored_as_sub_directories(self) -> typing.Optional[builtins.bool]:
        '''True if the table data is stored in subdirectories, or False if not.

        :see: `AWS::Glue::Table StorageDescriptor <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-storedassubdirectories>`_
        '''
        result = self._values.get("stored_as_sub_directories")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_type(self) -> typing.Optional["TableType"]:
        '''The type of this table.

        AWS Glue will create tables with the EXTERNAL_TABLE type. Other services, such as Athena, may create tables with additional table types.

        :see: `AWS::Glue::Table TableInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-tabletype>`_
        '''
        result = self._values.get("table_type")
        return typing.cast(typing.Optional["TableType"], result)

    @builtins.property
    def target_table(self) -> typing.Optional[Table]:
        '''A TableIdentifier structure that describes a target table for resource linking.

        :see: `AWS::Glue::Table TableInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-targettable>`_
        '''
        result = self._values.get("target_table")
        return typing.cast(typing.Optional[Table], result)

    @builtins.property
    def view_expanded_text(self) -> typing.Optional[builtins.str]:
        '''Included for Apache Hive compatibility.

        Not used in the normal course of AWS Glue operations.

        :see: `AWS::Glue::Table TableInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-viewexpandedtext>`_
        '''
        result = self._values.get("view_expanded_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def view_original_text(self) -> typing.Optional[builtins.str]:
        '''Included for Apache Hive compatibility.

        Not used in the normal course of AWS Glue operations. If the table is a VIRTUAL_VIEW, certain Athena configuration encoded in base64.

        :see: `AWS::Glue::Table TableInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-vieworiginaltext>`_
        '''
        result = self._values.get("view_original_text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.TableType")
class TableType(enum.Enum):
    EXTERNAL_TABLE = "EXTERNAL_TABLE"
    VIRTUAL_VIEW = "VIRTUAL_VIEW"


@jsii.enum(jsii_type="cdk-extensions.glue.TableUpdateBehavior")
class TableUpdateBehavior(enum.Enum):
    MERGE_NEW_COLUMNS = "MERGE_NEW_COLUMNS"


@jsii.implements(ITrigger)
class Trigger(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.Trigger",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        type: "TriggerType",
        actions: typing.Optional[typing.Sequence[ITriggerAction]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        predicate_conditions: typing.Optional[typing.Sequence[ITriggerPredicate]] = None,
        predicate_operator: typing.Optional[PredicateOperator] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        start_on_creation: typing.Optional[builtins.bool] = None,
        workflow: typing.Optional["Workflow"] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the Trigger class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param type: The type of trigger that this is.
        :param actions: A list of actions initiated by this trigger.
        :param description: A description for the trigger.
        :param name: A name for the trigger.
        :param predicate_conditions: A list of the conditions that determine when the trigger will fire.
        :param predicate_operator: Operator for chaining predicate conditions if multiple are given.
        :param schedule: A cron expression used to specify the schedule.
        :param start_on_creation: Set to true to start SCHEDULED and CONDITIONAL triggers when created. True is not supported for ON_DEMAND triggers.
        :param workflow: The name of the workflow associated with the trigger.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Trigger.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TriggerProps(
            type=type,
            actions=actions,
            description=description,
            name=name,
            predicate_conditions=predicate_conditions,
            predicate_operator=predicate_operator,
            schedule=schedule,
            start_on_creation=start_on_creation,
            workflow=workflow,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTriggerArn")
    @builtins.classmethod
    def from_trigger_arn(
        cls,
        scope: constructs.IConstruct,
        id: builtins.str,
        trigger_arn: builtins.str,
    ) -> ITrigger:
        '''Imports an existing trigger using its Amazon Resource Name (ARN).

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param trigger_arn: The ARN of the trigger to import.

        :return: An object representing the trigger that was imported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Trigger.from_trigger_arn)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument trigger_arn", value=trigger_arn, expected_type=type_hints["trigger_arn"])
        return typing.cast(ITrigger, jsii.sinvoke(cls, "fromTriggerArn", [scope, id, trigger_arn]))

    @jsii.member(jsii_name="fromTriggerName")
    @builtins.classmethod
    def from_trigger_name(
        cls,
        scope: constructs.IConstruct,
        id: builtins.str,
        trigger_name: builtins.str,
    ) -> ITrigger:
        '''Imports an existing trigger using its name.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param trigger_name: The name of the trigger to import.

        :return: An object representing the trigger that was imported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Trigger.from_trigger_name)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument trigger_name", value=trigger_name, expected_type=type_hints["trigger_name"])
        return typing.cast(ITrigger, jsii.sinvoke(cls, "fromTriggerName", [scope, id, trigger_name]))

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: ITriggerAction) -> "Trigger":
        '''Registers an action with the trigger.

        All actions associated with the
        trigger are run when the conditions to trigger the trigger are met.

        :param action: The action to be run by this trigger.

        :return: The trigger to which the action was added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Trigger.add_action)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
        return typing.cast("Trigger", jsii.invoke(self, "addAction", [action]))

    @jsii.member(jsii_name="addPredicate")
    def add_predicate(self, predicate: ITriggerPredicate) -> "Trigger":
        '''Registers a predicate with the trigger.

        Triggers with predicates must meet
        the conditions they specify in order to run.

        :param predicate: The predicate to be added to the trigger.

        :return: The trigger to which the predicate was added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Trigger.add_predicate)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        return typing.cast("Trigger", jsii.invoke(self, "addPredicate", [predicate]))

    @builtins.property
    @jsii.member(jsii_name="predicateOperator")
    def predicate_operator(self) -> PredicateOperator:
        '''Operator for chaining predicate conditions if multiple are given.

        :see: `Trigger Predicate.Logical <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-predicate.html#cfn-glue-trigger-predicate-logical>`_
        :group: Inputs
        '''
        return typing.cast(PredicateOperator, jsii.get(self, "predicateOperator"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_glue.CfnTrigger:
        '''The underlying Trigger CloudFormation resource.

        :see: `AWS::Glue::Trigger <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html>`_
        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_glue.CfnTrigger, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="triggerArn")
    def trigger_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the trigger.'''
        return typing.cast(builtins.str, jsii.get(self, "triggerArn"))

    @builtins.property
    @jsii.member(jsii_name="triggerName")
    def trigger_name(self) -> builtins.str:
        '''The name of the trigger.'''
        return typing.cast(builtins.str, jsii.get(self, "triggerName"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "TriggerType":
        '''The type of trigger that this is.

        :see: `Trigger Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-type>`_
        :group: Inputs
        '''
        return typing.cast("TriggerType", jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the trigger.

        :see: `Trigger Description <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-description>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the trigger.

        :see: `Trigger Name <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-name>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        '''A cron expression used to specify the schedule.

        :see: `Time-Based Schedules for Jobs and Crawlers <https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="startOnCreation")
    def start_on_creation(self) -> typing.Optional[builtins.bool]:
        '''Set to true to start SCHEDULED and CONDITIONAL triggers when created.

        True
        is not supported for ON_DEMAND triggers.

        :see: `Trigger StartOnCreation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-startoncreation>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "startOnCreation"))

    @builtins.property
    @jsii.member(jsii_name="workflow")
    def workflow(self) -> typing.Optional["Workflow"]:
        '''The name of the workflow associated with the trigger.

        :see: `Trigger WorkflowName <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-workflowname>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional["Workflow"], jsii.get(self, "workflow"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.TriggerOptions",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "type": "type",
        "actions": "actions",
        "description": "description",
        "name": "name",
        "predicate_conditions": "predicateConditions",
        "predicate_operator": "predicateOperator",
        "schedule": "schedule",
        "start_on_creation": "startOnCreation",
    },
)
class TriggerOptions(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        type: "TriggerType",
        actions: typing.Optional[typing.Sequence[ITriggerAction]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        predicate_conditions: typing.Optional[typing.Sequence[ITriggerPredicate]] = None,
        predicate_operator: typing.Optional[PredicateOperator] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        start_on_creation: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param type: 
        :param actions: 
        :param description: 
        :param name: 
        :param predicate_conditions: 
        :param predicate_operator: 
        :param schedule: 
        :param start_on_creation: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TriggerOptions.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument predicate_conditions", value=predicate_conditions, expected_type=type_hints["predicate_conditions"])
            check_type(argname="argument predicate_operator", value=predicate_operator, expected_type=type_hints["predicate_operator"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument start_on_creation", value=start_on_creation, expected_type=type_hints["start_on_creation"])
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if actions is not None:
            self._values["actions"] = actions
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if predicate_conditions is not None:
            self._values["predicate_conditions"] = predicate_conditions
        if predicate_operator is not None:
            self._values["predicate_operator"] = predicate_operator
        if schedule is not None:
            self._values["schedule"] = schedule
        if start_on_creation is not None:
            self._values["start_on_creation"] = start_on_creation

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> "TriggerType":
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("TriggerType", result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[ITriggerAction]]:
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[ITriggerAction]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predicate_conditions(self) -> typing.Optional[typing.List[ITriggerPredicate]]:
        result = self._values.get("predicate_conditions")
        return typing.cast(typing.Optional[typing.List[ITriggerPredicate]], result)

    @builtins.property
    def predicate_operator(self) -> typing.Optional[PredicateOperator]:
        result = self._values.get("predicate_operator")
        return typing.cast(typing.Optional[PredicateOperator], result)

    @builtins.property
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], result)

    @builtins.property
    def start_on_creation(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("start_on_creation")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TriggerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.glue.TriggerProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "type": "type",
        "actions": "actions",
        "description": "description",
        "name": "name",
        "predicate_conditions": "predicateConditions",
        "predicate_operator": "predicateOperator",
        "schedule": "schedule",
        "start_on_creation": "startOnCreation",
        "workflow": "workflow",
    },
)
class TriggerProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        type: "TriggerType",
        actions: typing.Optional[typing.Sequence[ITriggerAction]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        predicate_conditions: typing.Optional[typing.Sequence[ITriggerPredicate]] = None,
        predicate_operator: typing.Optional[PredicateOperator] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        start_on_creation: typing.Optional[builtins.bool] = None,
        workflow: typing.Optional["Workflow"] = None,
    ) -> None:
        '''Configuration for the GlueTrigger resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param type: The type of trigger that this is.
        :param actions: A list of actions initiated by this trigger.
        :param description: A description for the trigger.
        :param name: A name for the trigger.
        :param predicate_conditions: A list of the conditions that determine when the trigger will fire.
        :param predicate_operator: Operator for chaining predicate conditions if multiple are given.
        :param schedule: A cron expression used to specify the schedule.
        :param start_on_creation: Set to true to start SCHEDULED and CONDITIONAL triggers when created. True is not supported for ON_DEMAND triggers.
        :param workflow: The name of the workflow associated with the trigger.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TriggerProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument predicate_conditions", value=predicate_conditions, expected_type=type_hints["predicate_conditions"])
            check_type(argname="argument predicate_operator", value=predicate_operator, expected_type=type_hints["predicate_operator"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument start_on_creation", value=start_on_creation, expected_type=type_hints["start_on_creation"])
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if actions is not None:
            self._values["actions"] = actions
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if predicate_conditions is not None:
            self._values["predicate_conditions"] = predicate_conditions
        if predicate_operator is not None:
            self._values["predicate_operator"] = predicate_operator
        if schedule is not None:
            self._values["schedule"] = schedule
        if start_on_creation is not None:
            self._values["start_on_creation"] = start_on_creation
        if workflow is not None:
            self._values["workflow"] = workflow

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> "TriggerType":
        '''The type of trigger that this is.

        :see: `Trigger Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-type>`_
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("TriggerType", result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[ITriggerAction]]:
        '''A list of actions initiated by this trigger.

        :see: `Trigger Actions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-actions>`_
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[ITriggerAction]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the trigger.

        :see: `Trigger Description <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-description>`_
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the trigger.

        :see: `Trigger Name <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-name>`_
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predicate_conditions(self) -> typing.Optional[typing.List[ITriggerPredicate]]:
        '''A list of the conditions that determine when the trigger will fire.

        :see: `Trigger Predicate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-predicate.html>`_
        '''
        result = self._values.get("predicate_conditions")
        return typing.cast(typing.Optional[typing.List[ITriggerPredicate]], result)

    @builtins.property
    def predicate_operator(self) -> typing.Optional[PredicateOperator]:
        '''Operator for chaining predicate conditions if multiple are given.

        :see: `Trigger Predicate.Logical <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-predicate.html#cfn-glue-trigger-predicate-logical>`_
        '''
        result = self._values.get("predicate_operator")
        return typing.cast(typing.Optional[PredicateOperator], result)

    @builtins.property
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        '''A cron expression used to specify the schedule.

        :see: `Time-Based Schedules for Jobs and Crawlers <https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html>`_
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], result)

    @builtins.property
    def start_on_creation(self) -> typing.Optional[builtins.bool]:
        '''Set to true to start SCHEDULED and CONDITIONAL triggers when created.

        True
        is not supported for ON_DEMAND triggers.

        :see: `Trigger StartOnCreation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-startoncreation>`_
        '''
        result = self._values.get("start_on_creation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow(self) -> typing.Optional["Workflow"]:
        '''The name of the workflow associated with the trigger.

        :see: `Trigger WorkflowName <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-workflowname>`_
        '''
        result = self._values.get("workflow")
        return typing.cast(typing.Optional["Workflow"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TriggerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.glue.TriggerType")
class TriggerType(enum.Enum):
    CONDITIONAL = "CONDITIONAL"
    EVENT = "EVENT"
    ON_DEMAND = "ON_DEMAND"
    SCHEDULED = "SCHEDULED"


@jsii.enum(jsii_type="cdk-extensions.glue.UpdateBehavior")
class UpdateBehavior(enum.Enum):
    UPDATE_IN_DATABASE = "UPDATE_IN_DATABASE"
    LOG = "LOG"


class WorkerType(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.glue.WorkerType"):
    '''The type of predefined worker that is allocated when a job runs.

    If you need to use a WorkerType that doesn't exist as a static member, you
    can instantiate a ``WorkerType`` object, e.g: ``WorkerType.of('other type')``.
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, worker_type: builtins.str) -> "WorkerType":
        '''Custom worker type.

        :param worker_type: custom worker type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkerType.of)
            check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
        return typing.cast("WorkerType", jsii.sinvoke(cls, "of", [worker_type]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="G_1X")
    def G_1_X(cls) -> "WorkerType":
        '''Each worker maps to 1 DPU (4 vCPU, 16 GB of memory, 64 GB disk), and provides 1 executor per worker.

        Suitable for memory-intensive jobs.
        '''
        return typing.cast("WorkerType", jsii.sget(cls, "G_1X"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="G_2X")
    def G_2_X(cls) -> "WorkerType":
        '''Each worker maps to 2 DPU (8 vCPU, 32 GB of memory, 128 GB disk), and provides 1 executor per worker.

        Suitable for memory-intensive jobs.
        '''
        return typing.cast("WorkerType", jsii.sget(cls, "G_2X"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STANDARD")
    def STANDARD(cls) -> "WorkerType":
        '''Each worker provides 4 vCPU, 16 GB of memory and a 50GB disk, and 2 executors per worker.'''
        return typing.cast("WorkerType", jsii.sget(cls, "STANDARD"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of this WorkerType, as expected by Job resource.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class Workflow(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.Workflow",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the Workflow class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param description: A description of the Workflow.
        :param name: A name of the Workflow.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Workflow.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WorkflowProps(
            description=description,
            name=name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addTrigger")
    def add_trigger(
        self,
        id: builtins.str,
        *,
        type: TriggerType,
        actions: typing.Optional[typing.Sequence[ITriggerAction]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        predicate_conditions: typing.Optional[typing.Sequence[ITriggerPredicate]] = None,
        predicate_operator: typing.Optional[PredicateOperator] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        start_on_creation: typing.Optional[builtins.bool] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> ITrigger:
        '''
        :param id: -
        :param type: 
        :param actions: 
        :param description: 
        :param name: 
        :param predicate_conditions: 
        :param predicate_operator: 
        :param schedule: 
        :param start_on_creation: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Workflow.add_trigger)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = TriggerOptions(
            type=type,
            actions=actions,
            description=description,
            name=name,
            predicate_conditions=predicate_conditions,
            predicate_operator=predicate_operator,
            schedule=schedule,
            start_on_creation=start_on_creation,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast(ITrigger, jsii.invoke(self, "addTrigger", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_glue.CfnWorkflow:
        return typing.cast(aws_cdk.aws_glue.CfnWorkflow, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="workflowArn")
    def workflow_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowArn"))

    @builtins.property
    @jsii.member(jsii_name="workflowName")
    def workflow_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowName"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''{@link WorkflowProps.description}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''{@link WorkflowProps.name}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))


class WorkflowAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.WorkflowAction",
):
    '''Actions to be started by a Glue workflow trigger when it is activated.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="crawler")
    @builtins.classmethod
    def crawler(
        cls,
        crawler: ICrawler,
        *,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "WorkflowCrawlerAction":
        '''An action that runs a crawler as part of a Glue workflow.

        :param crawler: The crawler to run as part of the workflow.
        :param arguments: The arguments to use when the associated trigger fires. Jobs run via the associated trigger will have their default arguments replaced with the arguments specified. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this action.
        :param timeout: The ``JobRun`` timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 48 hours. This overrides the timeout value set in the parent job.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :return: A workflow action that runs the crawler with the given options.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowAction.crawler)
            check_type(argname="argument crawler", value=crawler, expected_type=type_hints["crawler"])
        options = WorkflowCrawlerActionOptions(
            arguments=arguments,
            notify_delay_after=notify_delay_after,
            security_configuration=security_configuration,
            timeout=timeout,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("WorkflowCrawlerAction", jsii.sinvoke(cls, "crawler", [crawler, options]))

    @jsii.member(jsii_name="job")
    @builtins.classmethod
    def job(
        cls,
        job: IJob,
        *,
        bookmark_configuration: typing.Optional[BookmarkConfiguration] = None,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "WorkflowJobAction":
        '''An action that runs a Glue job as part of a workflow.

        :param job: The job to run as part of the workflow.
        :param bookmark_configuration: The bookmark configuration override to use for the Glue job that is being triggered.
        :param arguments: The arguments to use when the associated trigger fires. Jobs run via the associated trigger will have their default arguments replaced with the arguments specified. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this action.
        :param timeout: The ``JobRun`` timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 48 hours. This overrides the timeout value set in the parent job.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :return: A workflow action that runs the job with the given options.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowAction.job)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        options = WorkflowJobActionOptions(
            bookmark_configuration=bookmark_configuration,
            arguments=arguments,
            notify_delay_after=notify_delay_after,
            security_configuration=security_configuration,
            timeout=timeout,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("WorkflowJobAction", jsii.sinvoke(cls, "job", [job, options]))


class WorkflowActionBase(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.WorkflowActionBase",
):
    '''Base class providing common functionality for workflow trigger actions.'''

    def __init__(
        self,
        *,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the WorkflowActionBase class.

        :param arguments: The arguments to use when the associated trigger fires. Jobs run via the associated trigger will have their default arguments replaced with the arguments specified. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this action.
        :param timeout: The ``JobRun`` timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 48 hours. This overrides the timeout value set in the parent job.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        options = WorkflowActionOptions(
            arguments=arguments,
            notify_delay_after=notify_delay_after,
            security_configuration=security_configuration,
            timeout=timeout,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addArgument")
    def add_argument(self, key: builtins.str, value: builtins.str) -> None:
        '''Adds an argument that will be passed to the specified action when triggered as part of a workflow.

        :param key: The name of the argument being set.
        :param value: The value to pass for the specified argument.

        :see: `AWS Glue job parameters <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowActionBase.add_argument)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addArgument", [key, value]))

    @jsii.member(jsii_name="bindOptions")
    def _bind_options(self, _scope: constructs.IConstruct) -> typing.Any:
        '''Associates the action with a construct that is configuring a trigger for a Glue workflow.

        :param _scope: The construct configuring the Glue trigger.

        :return:

        A configuration object that can be used to configure a triggered
        workflow action.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowActionBase._bind_options)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(typing.Any, jsii.invoke(self, "bindOptions", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="notifyDelayAfter")
    def notify_delay_after(self) -> typing.Optional[aws_cdk.Duration]:
        '''After a job run starts, the number of minutes to wait before sending a job run delay notification.

        :see: `Trigger Actions.NotificationProperty.NotifyDelayAfter <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-notificationproperty.html#cfn-glue-trigger-notificationproperty-notifydelayafter>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "notifyDelayAfter"))

    @builtins.property
    @jsii.member(jsii_name="securityConfiguration")
    def security_configuration(self) -> typing.Optional[builtins.str]:
        '''The name of the SecurityConfiguration structure to be used with this action.

        :see: `Trigger Actions.SecurityConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-securityconfiguration>`_
        :alpha: true
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[aws_cdk.Duration]:
        '''The ``JobRun`` timeout in minutes.

        This is the maximum time that a job run
        can consume resources before it is terminated and enters TIMEOUT status.
        The default is 48 hours. This overrides the timeout value set in the
        parent job.

        :see: `Trigger Actions.Timeout <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-timeout>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.WorkflowActionOptions",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "arguments": "arguments",
        "notify_delay_after": "notifyDelayAfter",
        "security_configuration": "securityConfiguration",
        "timeout": "timeout",
    },
)
class WorkflowActionOptions(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''Configuration for the Workflow Action resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param arguments: The arguments to use when the associated trigger fires. Jobs run via the associated trigger will have their default arguments replaced with the arguments specified. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this action.
        :param timeout: The ``JobRun`` timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 48 hours. This overrides the timeout value set in the parent job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowActionOptions.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument notify_delay_after", value=notify_delay_after, expected_type=type_hints["notify_delay_after"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if arguments is not None:
            self._values["arguments"] = arguments
        if notify_delay_after is not None:
            self._values["notify_delay_after"] = notify_delay_after
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def arguments(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The arguments to use when the associated trigger fires.

        Jobs run via the associated trigger will have their default arguments
        replaced with the arguments specified.

        You can specify arguments here that your own job-execution script
        consumes, in addition to arguments that AWS Glue itself consumes.

        :see: `Trigger Actions.Arguments <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-arguments>`_
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def notify_delay_after(self) -> typing.Optional[aws_cdk.Duration]:
        '''After a job run starts, the number of minutes to wait before sending a job run delay notification.

        :see: `Trigger Actions.NotificationProperty.NotifyDelayAfter <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-notificationproperty.html#cfn-glue-trigger-notificationproperty-notifydelayafter>`_
        '''
        result = self._values.get("notify_delay_after")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        '''The name of the SecurityConfiguration structure to be used with this action.

        :see: `Trigger Actions.SecurityConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-securityconfiguration>`_
        :alpha: true
        '''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.Duration]:
        '''The ``JobRun`` timeout in minutes.

        This is the maximum time that a job run
        can consume resources before it is terminated and enters TIMEOUT status.
        The default is 48 hours. This overrides the timeout value set in the
        parent job.

        :see: `Trigger Actions.Timeout <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-timeout>`_
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowActionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITriggerAction)
class WorkflowCrawlerAction(
    WorkflowActionBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.WorkflowCrawlerAction",
):
    '''Configuration options for the WorkflowCrawlerAction class.'''

    def __init__(
        self,
        crawler: ICrawler,
        *,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the WorkflowCrawlerAction class.

        :param crawler: The crawler that should be triggered as part of the workflow.
        :param arguments: The arguments to use when the associated trigger fires. Jobs run via the associated trigger will have their default arguments replaced with the arguments specified. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this action.
        :param timeout: The ``JobRun`` timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 48 hours. This overrides the timeout value set in the parent job.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowCrawlerAction.__init__)
            check_type(argname="argument crawler", value=crawler, expected_type=type_hints["crawler"])
        options = WorkflowCrawlerActionOptions(
            arguments=arguments,
            notify_delay_after=notify_delay_after,
            security_configuration=security_configuration,
            timeout=timeout,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [crawler, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_glue.CfnTrigger.ActionProperty:
        '''Associates this action with a resource that is configuring a Glue trigger.

        :param scope: The construct configuring the trigger that this action will be used in.

        :return:

        The configuration that can be used to configure the underlying
        trigger resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowCrawlerAction.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_glue.CfnTrigger.ActionProperty, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="crawler")
    def crawler(self) -> ICrawler:
        '''The Glue crawler to be triggered as part of the workflow.

        :group: Inputs
        '''
        return typing.cast(ICrawler, jsii.get(self, "crawler"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.WorkflowCrawlerActionOptions",
    jsii_struct_bases=[WorkflowActionOptions],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "arguments": "arguments",
        "notify_delay_after": "notifyDelayAfter",
        "security_configuration": "securityConfiguration",
        "timeout": "timeout",
    },
)
class WorkflowCrawlerActionOptions(WorkflowActionOptions):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''Configuration options for the WorkflowCrawlerAction class.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param arguments: The arguments to use when the associated trigger fires. Jobs run via the associated trigger will have their default arguments replaced with the arguments specified. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this action.
        :param timeout: The ``JobRun`` timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 48 hours. This overrides the timeout value set in the parent job.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowCrawlerActionOptions.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument notify_delay_after", value=notify_delay_after, expected_type=type_hints["notify_delay_after"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if arguments is not None:
            self._values["arguments"] = arguments
        if notify_delay_after is not None:
            self._values["notify_delay_after"] = notify_delay_after
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def arguments(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The arguments to use when the associated trigger fires.

        Jobs run via the associated trigger will have their default arguments
        replaced with the arguments specified.

        You can specify arguments here that your own job-execution script
        consumes, in addition to arguments that AWS Glue itself consumes.

        :see: `Trigger Actions.Arguments <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-arguments>`_
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def notify_delay_after(self) -> typing.Optional[aws_cdk.Duration]:
        '''After a job run starts, the number of minutes to wait before sending a job run delay notification.

        :see: `Trigger Actions.NotificationProperty.NotifyDelayAfter <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-notificationproperty.html#cfn-glue-trigger-notificationproperty-notifydelayafter>`_
        '''
        result = self._values.get("notify_delay_after")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        '''The name of the SecurityConfiguration structure to be used with this action.

        :see: `Trigger Actions.SecurityConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-securityconfiguration>`_
        :alpha: true
        '''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.Duration]:
        '''The ``JobRun`` timeout in minutes.

        This is the maximum time that a job run
        can consume resources before it is terminated and enters TIMEOUT status.
        The default is 48 hours. This overrides the timeout value set in the
        parent job.

        :see: `Trigger Actions.Timeout <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-timeout>`_
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowCrawlerActionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITriggerAction)
class WorkflowJobAction(
    WorkflowActionBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.WorkflowJobAction",
):
    '''Represents the configuration for a job that will be triggered as part of a workflow.'''

    def __init__(
        self,
        job: IJob,
        *,
        bookmark_configuration: typing.Optional[BookmarkConfiguration] = None,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the WorkflowJobAction class.

        :param job: The job that should be triggered as part of the workflow.
        :param bookmark_configuration: The bookmark configuration override to use for the Glue job that is being triggered.
        :param arguments: The arguments to use when the associated trigger fires. Jobs run via the associated trigger will have their default arguments replaced with the arguments specified. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this action.
        :param timeout: The ``JobRun`` timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 48 hours. This overrides the timeout value set in the parent job.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowJobAction.__init__)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        options = WorkflowJobActionOptions(
            bookmark_configuration=bookmark_configuration,
            arguments=arguments,
            notify_delay_after=notify_delay_after,
            security_configuration=security_configuration,
            timeout=timeout,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [job, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_glue.CfnTrigger.ActionProperty:
        '''Associates this action with a resource that is configuring a Glue trigger.

        :param scope: The construct configuring the trigger that this action will be used in.

        :return:

        The configuration that can be used to configure the underlying
        trigger resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowJobAction.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_glue.CfnTrigger.ActionProperty, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="job")
    def job(self) -> IJob:
        '''The Glue job to be triggered as part of the workflow.

        :group: Inputs
        '''
        return typing.cast(IJob, jsii.get(self, "job"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.WorkflowJobActionOptions",
    jsii_struct_bases=[WorkflowActionOptions],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "arguments": "arguments",
        "notify_delay_after": "notifyDelayAfter",
        "security_configuration": "securityConfiguration",
        "timeout": "timeout",
        "bookmark_configuration": "bookmarkConfiguration",
    },
)
class WorkflowJobActionOptions(WorkflowActionOptions):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        bookmark_configuration: typing.Optional[BookmarkConfiguration] = None,
    ) -> None:
        '''Configuration options for the WorkflowJobAction class.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param arguments: The arguments to use when the associated trigger fires. Jobs run via the associated trigger will have their default arguments replaced with the arguments specified. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this action.
        :param timeout: The ``JobRun`` timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 48 hours. This overrides the timeout value set in the parent job.
        :param bookmark_configuration: The bookmark configuration override to use for the Glue job that is being triggered.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowJobActionOptions.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument notify_delay_after", value=notify_delay_after, expected_type=type_hints["notify_delay_after"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument bookmark_configuration", value=bookmark_configuration, expected_type=type_hints["bookmark_configuration"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if arguments is not None:
            self._values["arguments"] = arguments
        if notify_delay_after is not None:
            self._values["notify_delay_after"] = notify_delay_after
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if timeout is not None:
            self._values["timeout"] = timeout
        if bookmark_configuration is not None:
            self._values["bookmark_configuration"] = bookmark_configuration

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def arguments(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The arguments to use when the associated trigger fires.

        Jobs run via the associated trigger will have their default arguments
        replaced with the arguments specified.

        You can specify arguments here that your own job-execution script
        consumes, in addition to arguments that AWS Glue itself consumes.

        :see: `Trigger Actions.Arguments <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-arguments>`_
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def notify_delay_after(self) -> typing.Optional[aws_cdk.Duration]:
        '''After a job run starts, the number of minutes to wait before sending a job run delay notification.

        :see: `Trigger Actions.NotificationProperty.NotifyDelayAfter <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-notificationproperty.html#cfn-glue-trigger-notificationproperty-notifydelayafter>`_
        '''
        result = self._values.get("notify_delay_after")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        '''The name of the SecurityConfiguration structure to be used with this action.

        :see: `Trigger Actions.SecurityConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-securityconfiguration>`_
        :alpha: true
        '''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.Duration]:
        '''The ``JobRun`` timeout in minutes.

        This is the maximum time that a job run
        can consume resources before it is terminated and enters TIMEOUT status.
        The default is 48 hours. This overrides the timeout value set in the
        parent job.

        :see: `Trigger Actions.Timeout <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-timeout>`_
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def bookmark_configuration(self) -> typing.Optional[BookmarkConfiguration]:
        '''The bookmark configuration override to use for the Glue job that is being triggered.'''
        result = self._values.get("bookmark_configuration")
        return typing.cast(typing.Optional[BookmarkConfiguration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowJobActionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkflowPredicate(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.WorkflowPredicate",
):
    '''Predicate conditions for controlling trigger activation in a Glue workflow.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="crawler")
    @builtins.classmethod
    def crawler(
        cls,
        crawler: ICrawler,
        *,
        logical_operator: typing.Optional[PredicateLogicalOperator] = None,
        state: typing.Optional[CrawlerState] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "WorkflowCrawlerPredicate":
        '''A predicate condition dependent on the completion of a Glue crawler.

        :param crawler: The crawler which must complete in order to meet the requirements to trigger the next stage of the workflow.
        :param logical_operator: The logical operator which should be applied in determining whether a crawler meets the requested conditions. At the moment, the only supported operator is ``EQUALS``.
        :param state: The state that the crawler must be in in order to meet the criteria to trigger the next stage of the workflow.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :return:

        A workflow condition that is predicated on the completion of the
        specified Glue crawler.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowPredicate.crawler)
            check_type(argname="argument crawler", value=crawler, expected_type=type_hints["crawler"])
        options = WorkflowCrawlerPredicateOptions(
            logical_operator=logical_operator,
            state=state,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("WorkflowCrawlerPredicate", jsii.sinvoke(cls, "crawler", [crawler, options]))

    @jsii.member(jsii_name="job")
    @builtins.classmethod
    def job(
        cls,
        job: IJob,
        *,
        logical_operator: typing.Optional[PredicateLogicalOperator] = None,
        state: typing.Optional[JobState] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "WorkflowJobPredicate":
        '''A predicate condition dependent on the completion of a Glue job.

        :param job: The job which must complete in order to meet the requirements to trigger the next stage of the workflow.
        :param logical_operator: The logical operator which should be applied in determining whether a job meets the requested conditions. At the moment, the only supported operator is ``EQUALS``.
        :param state: The state that the job must be in in order to meet the criteria to trigger the next stage of the workflow.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :return:

        A workflow condition that is predicated on the completion of the
        specified Glue crawler.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowPredicate.job)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        options = WorkflowJobPredicateOptions(
            logical_operator=logical_operator,
            state=state,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("WorkflowJobPredicate", jsii.sinvoke(cls, "job", [job, options]))


class WorkflowPredicateBase(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.WorkflowPredicateBase",
):
    '''Base class providing common functionality for trigger predicate conditions.'''

    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new instance of the WorkflowPredicateBase class.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        _options = WorkflowPredicateOptions(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [_options])

    @jsii.member(jsii_name="bindOptions")
    def _bind_options(self, _scope: constructs.IConstruct) -> typing.Any:
        '''Associates the predicate with a construct that is configuring a trigger for a Glue workflow.

        :param _scope: The construct configuring the Glue trigger.

        :return:

        A configuration object that can be used to configure a predicate
        condition for the Glue trigger.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowPredicateBase._bind_options)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(typing.Any, jsii.invoke(self, "bindOptions", [_scope]))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.WorkflowPredicateOptions",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
    },
)
class WorkflowPredicateOptions(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for a generic Glue Trigger predicate.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowPredicateOptions.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowPredicateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.glue.WorkflowProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "description": "description",
        "name": "name",
    },
)
class WorkflowProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the Glue Workflow resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param description: A description of the Workflow.
        :param name: A name of the Workflow.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the Workflow.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name of the Workflow.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArrayColumn(
    Column,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.ArrayColumn",
):
    def __init__(
        self,
        *,
        data: Column,
        comment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data: 
        :param comment: 
        :param name: 
        '''
        props = ArrayColumnProps(data=data, comment=comment, name=name)

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="typeString")
    def type_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeString"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.ArrayColumnProps",
    jsii_struct_bases=[ColumnProps],
    name_mapping={"comment": "comment", "name": "name", "data": "data"},
)
class ArrayColumnProps(ColumnProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        data: Column,
    ) -> None:
        '''
        :param comment: 
        :param name: 
        :param data: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ArrayColumnProps.__init__)
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[str, typing.Any] = {
            "data": data,
        }
        if comment is not None:
            self._values["comment"] = comment
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> Column:
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(Column, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArrayColumnProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AssetCode(
    Code,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.AssetCode",
):
    '''Job Code from a local file.'''

    def __init__(
        self,
        path: builtins.str,
        *,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[aws_cdk.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[aws_cdk.BundlingOptions, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param path: The path to the Code file.
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AssetCode.__init__)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        options = aws_cdk.AssetOptions(
            asset_hash=asset_hash, asset_hash_type=asset_hash_type, bundling=bundling
        )

        jsii.create(self.__class__, self, [path, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.Construct,
        grantable: aws_cdk.aws_iam.IGrantable,
    ) -> CodeConfig:
        '''Called when the Job is initialized to allow this object to bind.

        :param scope: -
        :param grantable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AssetCode.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument grantable", value=grantable, expected_type=type_hints["grantable"])
        return typing.cast(CodeConfig, jsii.invoke(self, "bind", [scope, grantable]))


class BasicColumn(
    Column,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.BasicColumn",
):
    def __init__(
        self,
        *,
        type: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: 
        :param comment: 
        :param name: 
        '''
        props = BasicColumnProps(type=type, comment=comment, name=name)

        jsii.create(self.__class__, self, [props])

    @builtins.property
    @jsii.member(jsii_name="typeString")
    def type_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeString"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.BasicColumnProps",
    jsii_struct_bases=[ColumnProps],
    name_mapping={"comment": "comment", "name": "name", "type": "type"},
)
class BasicColumnProps(ColumnProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: builtins.str,
    ) -> None:
        '''
        :param comment: 
        :param name: 
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BasicColumnProps.__init__)
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
        }
        if comment is not None:
            self._values["comment"] = comment
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicColumnProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ICrawler)
class Crawler(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.Crawler",
):
    '''Create a Crawler resource to pull information from the provided resource.

    :see: `AWS::Glue::Crawler <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html>`_
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[typing.Union[CrawlerConfiguration, typing.Dict[str, typing.Any]]] = None,
        database: typing.Optional[Database] = None,
        delete_behavior: typing.Optional[DeleteBehavior] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        recrawl_behavior: typing.Optional[RecrawlBehavior] = None,
        schedule_expression: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        security_configuration: typing.Optional[SecurityConfiguration] = None,
        table_prefix: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[ICrawlerTarget]] = None,
        update_behavior: typing.Optional[UpdateBehavior] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the Crawler class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param classifiers: A list of UTF-8 strings that specify the names of custom classifiers that are associated with the crawler.
        :param configuration: Crawler configuration information. This versioned JSON string allows users to specify aspects of a crawler's behavior. For more information, see Configuring a Crawler.
        :param database: The {@link aws-glue.Database | Database } object in which the crawler's output is stored.
        :param delete_behavior: The deletion behavior when the crawler finds a deleted object.
        :param description: Description of the Crawler.
        :param name: Name of the Crawler.
        :param recrawl_behavior: When crawling an Amazon S3 data source after the first crawl is complete, specifies whether to crawl the entire dataset again or to crawl only folders that were added since the last crawler run.
        :param schedule_expression: For scheduled crawlers, the schedule when the crawler runs.
        :param security_configuration: A {@link aws-glue.SecurityConfiguration | SecurityConfiguration } object to apply to the Crawler.
        :param table_prefix: The prefix added to the names of tables that are created.
        :param targets: A collection of targets to crawl.
        :param update_behavior: The update behavior when the crawler finds a changed schema.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Crawler.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CrawlerProps(
            classifiers=classifiers,
            configuration=configuration,
            database=database,
            delete_behavior=delete_behavior,
            description=description,
            name=name,
            recrawl_behavior=recrawl_behavior,
            schedule_expression=schedule_expression,
            security_configuration=security_configuration,
            table_prefix=table_prefix,
            targets=targets,
            update_behavior=update_behavior,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromCrawlerArn")
    @builtins.classmethod
    def from_crawler_arn(
        cls,
        scope: constructs.IConstruct,
        id: builtins.str,
        crawler_arn: builtins.str,
    ) -> ICrawler:
        '''Imports an existing crawler using its Amazon Resource Name (ARN).

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param crawler_arn: The ARN of the crawler to import.

        :return: An object representing the crawler that was imported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Crawler.from_crawler_arn)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument crawler_arn", value=crawler_arn, expected_type=type_hints["crawler_arn"])
        return typing.cast(ICrawler, jsii.sinvoke(cls, "fromCrawlerArn", [scope, id, crawler_arn]))

    @jsii.member(jsii_name="fromCrawlerName")
    @builtins.classmethod
    def from_crawler_name(
        cls,
        scope: constructs.IConstruct,
        id: builtins.str,
        crawler_name: builtins.str,
    ) -> ICrawler:
        '''Imports an existing crawler using its name.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param crawler_name: The name of the crawler to import.

        :return: An object representing the crawler that was imported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Crawler.from_crawler_name)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument crawler_name", value=crawler_name, expected_type=type_hints["crawler_name"])
        return typing.cast(ICrawler, jsii.sinvoke(cls, "fromCrawlerName", [scope, id, crawler_name]))

    @jsii.member(jsii_name="addClassifier")
    def add_classifier(self, classifier: builtins.str) -> None:
        '''
        :param classifier: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Crawler.add_classifier)
            check_type(argname="argument classifier", value=classifier, expected_type=type_hints["classifier"])
        return typing.cast(None, jsii.invoke(self, "addClassifier", [classifier]))

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: ICrawlerTarget) -> None:
        '''
        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Crawler.add_target)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(None, jsii.invoke(self, "addTarget", [target]))

    @builtins.property
    @jsii.member(jsii_name="crawlerArn")
    def crawler_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the crawler.'''
        return typing.cast(builtins.str, jsii.get(self, "crawlerArn"))

    @builtins.property
    @jsii.member(jsii_name="crawlerName")
    def crawler_name(self) -> builtins.str:
        '''The name of the crawler.'''
        return typing.cast(builtins.str, jsii.get(self, "crawlerName"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_glue.CfnCrawler:
        return typing.cast(aws_cdk.aws_glue.CfnCrawler, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.Role:
        return typing.cast(aws_cdk.aws_iam.Role, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> typing.Optional[CrawlerConfiguration]:
        '''{@link CrawlerProps.configuration}.'''
        return typing.cast(typing.Optional[CrawlerConfiguration], jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> typing.Optional[Database]:
        '''{@link CrawlerProps.database}.'''
        return typing.cast(typing.Optional[Database], jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="deleteBehavior")
    def delete_behavior(self) -> typing.Optional[DeleteBehavior]:
        '''{@link CrawlerProps.deleteBehavior}.'''
        return typing.cast(typing.Optional[DeleteBehavior], jsii.get(self, "deleteBehavior"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''{@link CrawlerProps.description}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''{@link CrawlerProps.name}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="recrawlBehavior")
    def recrawl_behavior(self) -> typing.Optional[RecrawlBehavior]:
        '''{@link CrawlerProps.recrawlBehavior}.'''
        return typing.cast(typing.Optional[RecrawlBehavior], jsii.get(self, "recrawlBehavior"))

    @builtins.property
    @jsii.member(jsii_name="scheduleExpression")
    def schedule_expression(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        '''{@link CrawlerProps.scheduleExpression}.'''
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], jsii.get(self, "scheduleExpression"))

    @builtins.property
    @jsii.member(jsii_name="securityConfiguration")
    def security_configuration(self) -> typing.Optional[SecurityConfiguration]:
        '''{@link CrawlerProps.securityConfiguration}.'''
        return typing.cast(typing.Optional[SecurityConfiguration], jsii.get(self, "securityConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="tablePrefix")
    def table_prefix(self) -> typing.Optional[builtins.str]:
        '''{@link CrawlerProps.tablePrefix}.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tablePrefix"))

    @builtins.property
    @jsii.member(jsii_name="updateBehavior")
    def update_behavior(self) -> typing.Optional[UpdateBehavior]:
        '''{@link CrawlerProps.updateBehavior}.'''
        return typing.cast(typing.Optional[UpdateBehavior], jsii.get(self, "updateBehavior"))


@jsii.implements(ITriggerPredicate)
class WorkflowCrawlerPredicate(
    WorkflowPredicateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.WorkflowCrawlerPredicate",
):
    '''Represents a condition that is predicated on a Glue crawler completion.

    The condition can be used to create a trigger that controls the execution of
    downstream tasks in a workflow.
    '''

    def __init__(
        self,
        crawler: ICrawler,
        *,
        logical_operator: typing.Optional[PredicateLogicalOperator] = None,
        state: typing.Optional[CrawlerState] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the WorkflowCrawlerPredicate class.

        :param crawler: The crawler which must complete in order to meet the requirements to trigger the next stage of the workflow.
        :param logical_operator: The logical operator which should be applied in determining whether a crawler meets the requested conditions. At the moment, the only supported operator is ``EQUALS``.
        :param state: The state that the crawler must be in in order to meet the criteria to trigger the next stage of the workflow.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowCrawlerPredicate.__init__)
            check_type(argname="argument crawler", value=crawler, expected_type=type_hints["crawler"])
        options = WorkflowCrawlerPredicateOptions(
            logical_operator=logical_operator,
            state=state,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [crawler, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_glue.CfnTrigger.ConditionProperty:
        '''Associates the predicate with a construct that is configuring a trigger for a Glue workflow.

        :param scope: The construct configuring the Glue trigger.

        :return:

        A configuration object that can be used to configure a predicate
        condition for the Glue trigger.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowCrawlerPredicate.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_glue.CfnTrigger.ConditionProperty, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="crawler")
    def crawler(self) -> ICrawler:
        '''The crawler which must complete in order to meet the requirements to trigger the next stage of the workflow.

        :see: `Trigger Predicate.Conditions.CrawlerName <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-crawlername>`_
        :group: Inputs
        '''
        return typing.cast(ICrawler, jsii.get(self, "crawler"))

    @builtins.property
    @jsii.member(jsii_name="logicalOperator")
    def logical_operator(self) -> PredicateLogicalOperator:
        '''The logical operator which should be applied in determining whether a crawler meets the requested conditions.

        At the moment, the only supported operator is ``EQUALS``.

        :see: `Trigger Predicate.Conditions.LogicalOperator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-logicaloperator>`_
        '''
        return typing.cast(PredicateLogicalOperator, jsii.get(self, "logicalOperator"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> CrawlerState:
        '''The state that the crawler must be in in order to meet the criteria to trigger the next stage of the workflow.

        :see: `Trigger Predicate.Conditions.CrawlState <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-crawlstate>`_
        '''
        return typing.cast(CrawlerState, jsii.get(self, "state"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.WorkflowCrawlerPredicateOptions",
    jsii_struct_bases=[WorkflowPredicateOptions],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logical_operator": "logicalOperator",
        "state": "state",
    },
)
class WorkflowCrawlerPredicateOptions(WorkflowPredicateOptions):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logical_operator: typing.Optional[PredicateLogicalOperator] = None,
        state: typing.Optional[CrawlerState] = None,
    ) -> None:
        '''Configuration options that specify the state a crawler must meet in order to satisfy the conditions of the predicate.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logical_operator: The logical operator which should be applied in determining whether a crawler meets the requested conditions. At the moment, the only supported operator is ``EQUALS``.
        :param state: The state that the crawler must be in in order to meet the criteria to trigger the next stage of the workflow.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowCrawlerPredicateOptions.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logical_operator", value=logical_operator, expected_type=type_hints["logical_operator"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logical_operator is not None:
            self._values["logical_operator"] = logical_operator
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logical_operator(self) -> typing.Optional[PredicateLogicalOperator]:
        '''The logical operator which should be applied in determining whether a crawler meets the requested conditions.

        At the moment, the only supported operator is ``EQUALS``.

        :see: `Trigger Predicate.Conditions.LogicalOperator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-logicaloperator>`_
        '''
        result = self._values.get("logical_operator")
        return typing.cast(typing.Optional[PredicateLogicalOperator], result)

    @builtins.property
    def state(self) -> typing.Optional[CrawlerState]:
        '''The state that the crawler must be in in order to meet the criteria to trigger the next stage of the workflow.

        :see: `Trigger Predicate.Conditions.CrawlState <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-crawlstate>`_
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[CrawlerState], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowCrawlerPredicateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITriggerPredicate)
class WorkflowJobPredicate(
    WorkflowPredicateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.glue.WorkflowJobPredicate",
):
    '''Represents a condition that is predicated on a Glue job completion.

    The condition can be used to create a trigger that controls the execution of
    downstream tasks in a workflow.
    '''

    def __init__(
        self,
        job: IJob,
        *,
        logical_operator: typing.Optional[PredicateLogicalOperator] = None,
        state: typing.Optional[JobState] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the WorkflowJobPredicate class.

        :param job: The job which must complete in order to meet the requirements to trigger the next stage of the workflow.
        :param logical_operator: The logical operator which should be applied in determining whether a job meets the requested conditions. At the moment, the only supported operator is ``EQUALS``.
        :param state: The state that the job must be in in order to meet the criteria to trigger the next stage of the workflow.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowJobPredicate.__init__)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        options = WorkflowJobPredicateOptions(
            logical_operator=logical_operator,
            state=state,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [job, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_glue.CfnTrigger.ConditionProperty:
        '''Associates the predicate with a construct that is configuring a trigger for a Glue workflow.

        :param scope: The construct configuring the Glue trigger.

        :return:

        A configuration object that can be used to configure a predicate
        condition for the Glue trigger.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowJobPredicate.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_glue.CfnTrigger.ConditionProperty, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="job")
    def job(self) -> IJob:
        '''The job which must complete in order to meet the requirements to trigger the next stage of the workflow.

        :see: `Trigger Predicate.Conditions.JobName <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-jobname>`_
        :group: Inputs
        '''
        return typing.cast(IJob, jsii.get(self, "job"))

    @builtins.property
    @jsii.member(jsii_name="logicalOperator")
    def logical_operator(self) -> PredicateLogicalOperator:
        '''The logical operator which should be applied in determining whether a job meets the requested conditions.

        At the moment, the only supported operator is ``EQUALS``.

        :see: `Trigger Predicate.Conditions.LogicalOperator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-logicaloperator>`_
        :group: Inputs
        '''
        return typing.cast(PredicateLogicalOperator, jsii.get(self, "logicalOperator"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> JobState:
        '''The state that the job must be in in order to meet the criteria to trigger the next stage of the workflow.

        :see: `Trigger Predicate.Conditions.State <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-state>`_
        :group: Inputs
        '''
        return typing.cast(JobState, jsii.get(self, "state"))


@jsii.data_type(
    jsii_type="cdk-extensions.glue.WorkflowJobPredicateOptions",
    jsii_struct_bases=[WorkflowPredicateOptions],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logical_operator": "logicalOperator",
        "state": "state",
    },
)
class WorkflowJobPredicateOptions(WorkflowPredicateOptions):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logical_operator: typing.Optional[PredicateLogicalOperator] = None,
        state: typing.Optional[JobState] = None,
    ) -> None:
        '''Configuration options that specify the state a job must meet in order to satisfy the conditions of the predicate.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logical_operator: The logical operator which should be applied in determining whether a job meets the requested conditions. At the moment, the only supported operator is ``EQUALS``.
        :param state: The state that the job must be in in order to meet the criteria to trigger the next stage of the workflow.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(WorkflowJobPredicateOptions.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logical_operator", value=logical_operator, expected_type=type_hints["logical_operator"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logical_operator is not None:
            self._values["logical_operator"] = logical_operator
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logical_operator(self) -> typing.Optional[PredicateLogicalOperator]:
        '''The logical operator which should be applied in determining whether a job meets the requested conditions.

        At the moment, the only supported operator is ``EQUALS``.

        :see: `Trigger Predicate.Conditions.LogicalOperator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-logicaloperator>`_
        '''
        result = self._values.get("logical_operator")
        return typing.cast(typing.Optional[PredicateLogicalOperator], result)

    @builtins.property
    def state(self) -> typing.Optional[JobState]:
        '''The state that the job must be in in order to meet the criteria to trigger the next stage of the workflow.

        :see: `Trigger Predicate.Conditions.State <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-state>`_
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[JobState], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowJobPredicateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ArrayColumn",
    "ArrayColumnProps",
    "AssetCode",
    "BasicColumn",
    "BasicColumnProps",
    "BookmarkConfiguration",
    "BookmarkRange",
    "ClassificationString",
    "CloudWatchEncryption",
    "CloudWatchEncryptionMode",
    "Code",
    "CodeConfig",
    "Column",
    "ColumnProps",
    "ConfigurationVersion",
    "Connection",
    "ConnectionProps",
    "ConnectionType",
    "ContinuousLoggingProps",
    "Crawler",
    "CrawlerConfiguration",
    "CrawlerProps",
    "CrawlerState",
    "CrawlerTargetCollection",
    "DataFormat",
    "DataFormatProps",
    "Database",
    "DatabaseProps",
    "DeleteBehavior",
    "GlueVersion",
    "ICrawler",
    "ICrawlerTarget",
    "IJob",
    "ITrigger",
    "ITriggerAction",
    "ITriggerPredicate",
    "InputFormat",
    "JdbcConnection",
    "JdbcConnectionProps",
    "JdbcTarget",
    "JdbcTargetOptions",
    "Job",
    "JobBookmarksEncryption",
    "JobBookmarksEncryptionMode",
    "JobExecutable",
    "JobExecutableConfig",
    "JobLanguage",
    "JobProps",
    "JobState",
    "JobType",
    "OutputFormat",
    "PartitionUpdateBehavior",
    "PredicateLogicalOperator",
    "PredicateOperator",
    "PythonShellExecutableProps",
    "PythonSparkJobExecutableProps",
    "PythonVersion",
    "RecrawlBehavior",
    "S3Code",
    "S3Encryption",
    "S3EncryptionMode",
    "S3Target",
    "S3TargetOptions",
    "ScalaJobExecutableProps",
    "SecurityConfiguration",
    "SecurityConfigurationProps",
    "SerializationLibrary",
    "StructColumn",
    "StructColumnProps",
    "Table",
    "TableGroupingPolicy",
    "TableProps",
    "TableType",
    "TableUpdateBehavior",
    "Trigger",
    "TriggerOptions",
    "TriggerProps",
    "TriggerType",
    "UpdateBehavior",
    "WorkerType",
    "Workflow",
    "WorkflowAction",
    "WorkflowActionBase",
    "WorkflowActionOptions",
    "WorkflowCrawlerAction",
    "WorkflowCrawlerActionOptions",
    "WorkflowCrawlerPredicate",
    "WorkflowCrawlerPredicateOptions",
    "WorkflowJobAction",
    "WorkflowJobActionOptions",
    "WorkflowJobPredicate",
    "WorkflowJobPredicateOptions",
    "WorkflowPredicate",
    "WorkflowPredicateBase",
    "WorkflowPredicateOptions",
    "WorkflowProps",
]

publication.publish()
