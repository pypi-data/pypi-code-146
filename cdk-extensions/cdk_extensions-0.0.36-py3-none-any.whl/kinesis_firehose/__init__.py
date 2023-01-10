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
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_kinesisfirehose
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_s3
import constructs
from ..glue import Database as _Database_5971ae38, Table as _Table_114d5aef


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.AppendDelimiterProcessorOptions",
    jsii_struct_bases=[],
    name_mapping={"delimiter": "delimiter"},
)
class AppendDelimiterProcessorOptions:
    def __init__(self, *, delimiter: builtins.str) -> None:
        '''
        :param delimiter: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AppendDelimiterProcessorOptions.__init__)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
        self._values: typing.Dict[str, typing.Any] = {
            "delimiter": delimiter,
        }

    @builtins.property
    def delimiter(self) -> builtins.str:
        result = self._values.get("delimiter")
        assert result is not None, "Required property 'delimiter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppendDelimiterProcessorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.BackupConfiguration",
):
    def __init__(
        self,
        *,
        destination: "IDeliveryStreamBackupDestination",
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param destination: 
        :param enabled: 
        '''
        options = BackupConfigurationOptions(destination=destination, enabled=enabled)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> "BackupConfigurationResult":
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BackupConfiguration.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("BackupConfigurationResult", jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> "IDeliveryStreamBackupDestination":
        return typing.cast("IDeliveryStreamBackupDestination", jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.BackupConfigurationOptions",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "enabled": "enabled"},
)
class BackupConfigurationOptions:
    def __init__(
        self,
        *,
        destination: "IDeliveryStreamBackupDestination",
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param destination: 
        :param enabled: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BackupConfigurationOptions.__init__)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[str, typing.Any] = {
            "destination": destination,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def destination(self) -> "IDeliveryStreamBackupDestination":
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("IDeliveryStreamBackupDestination", result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupConfigurationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.BackupConfigurationResult",
    jsii_struct_bases=[],
    name_mapping={
        "s3_backup_configuration": "s3BackupConfiguration",
        "s3_backup_mode": "s3BackupMode",
    },
)
class BackupConfigurationResult:
    def __init__(
        self,
        *,
        s3_backup_configuration: typing.Union[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty, typing.Dict[str, typing.Any]],
        s3_backup_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_backup_configuration: 
        :param s3_backup_mode: 
        '''
        if isinstance(s3_backup_configuration, dict):
            s3_backup_configuration = aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty(**s3_backup_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(BackupConfigurationResult.__init__)
            check_type(argname="argument s3_backup_configuration", value=s3_backup_configuration, expected_type=type_hints["s3_backup_configuration"])
            check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
        self._values: typing.Dict[str, typing.Any] = {
            "s3_backup_configuration": s3_backup_configuration,
        }
        if s3_backup_mode is not None:
            self._values["s3_backup_mode"] = s3_backup_mode

    @builtins.property
    def s3_backup_configuration(
        self,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty:
        result = self._values.get("s3_backup_configuration")
        assert result is not None, "Required property 's3_backup_configuration' is missing"
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty, result)

    @builtins.property
    def s3_backup_mode(self) -> typing.Optional[builtins.str]:
        result = self._values.get("s3_backup_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupConfigurationResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BufferingConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.BufferingConfiguration",
):
    def __init__(
        self,
        *,
        interval: typing.Optional[aws_cdk.Duration] = None,
        size_in_mb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: 
        :param size_in_mb: 
        '''
        options = BufferingConfigurationOptions(
            interval=interval, size_in_mb=size_in_mb
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.IConstruct,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.BufferingHintsProperty]:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BufferingConfiguration.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.BufferingHintsProperty], jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> typing.Optional[aws_cdk.Duration]:
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "interval"))

    @builtins.property
    @jsii.member(jsii_name="sizeInMb")
    def size_in_mb(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInMb"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.BufferingConfigurationOptions",
    jsii_struct_bases=[],
    name_mapping={"interval": "interval", "size_in_mb": "sizeInMb"},
)
class BufferingConfigurationOptions:
    def __init__(
        self,
        *,
        interval: typing.Optional[aws_cdk.Duration] = None,
        size_in_mb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: 
        :param size_in_mb: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BufferingConfigurationOptions.__init__)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument size_in_mb", value=size_in_mb, expected_type=type_hints["size_in_mb"])
        self._values: typing.Dict[str, typing.Any] = {}
        if interval is not None:
            self._values["interval"] = interval
        if size_in_mb is not None:
            self._values["size_in_mb"] = size_in_mb

    @builtins.property
    def interval(self) -> typing.Optional[aws_cdk.Duration]:
        result = self._values.get("interval")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def size_in_mb(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("size_in_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BufferingConfigurationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudWatchLoggingConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.CloudWatchLoggingConfiguration",
):
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup] = None,
        log_stream: typing.Optional[aws_cdk.aws_logs.ILogStream] = None,
    ) -> None:
        '''
        :param enabled: 
        :param log_group: 
        :param log_stream: 
        '''
        options = CloudWatchLoggingConfigurationOptions(
            enabled=enabled, log_group=log_group, log_stream=log_stream
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.CloudWatchLoggingOptionsProperty]:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudWatchLoggingConfiguration.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.CloudWatchLoggingOptionsProperty], jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogGroup], jsii.get(self, "logGroup"))

    @builtins.property
    @jsii.member(jsii_name="logStream")
    def log_stream(self) -> typing.Optional[aws_cdk.aws_logs.ILogStream]:
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogStream], jsii.get(self, "logStream"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.CloudWatchLoggingConfigurationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group": "logGroup",
        "log_stream": "logStream",
    },
)
class CloudWatchLoggingConfigurationOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup] = None,
        log_stream: typing.Optional[aws_cdk.aws_logs.ILogStream] = None,
    ) -> None:
        '''
        :param enabled: 
        :param log_group: 
        :param log_stream: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CloudWatchLoggingConfigurationOptions.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_stream", value=log_stream, expected_type=type_hints["log_stream"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_group is not None:
            self._values["log_group"] = log_group
        if log_stream is not None:
            self._values["log_stream"] = log_stream

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogGroup], result)

    @builtins.property
    def log_stream(self) -> typing.Optional[aws_cdk.aws_logs.ILogStream]:
        result = self._values.get("log_stream")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogStream], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchLoggingConfigurationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.CommonPartitioningOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "retry_interval": "retryInterval"},
)
class CommonPartitioningOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        retry_interval: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param enabled: 
        :param retry_interval: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CommonPartitioningOptions.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument retry_interval", value=retry_interval, expected_type=type_hints["retry_interval"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if retry_interval is not None:
            self._values["retry_interval"] = retry_interval

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retry_interval(self) -> typing.Optional[aws_cdk.Duration]:
        result = self._values.get("retry_interval")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonPartitioningOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.kinesis_firehose.ContentEncoding")
class ContentEncoding(enum.Enum):
    GZIP = "GZIP"
    NONE = "NONE"


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.CustomProcessorOptions",
    jsii_struct_bases=[],
    name_mapping={"processor_type": "processorType", "parameters": "parameters"},
)
class CustomProcessorOptions:
    def __init__(
        self,
        *,
        processor_type: "ProcessorType",
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param processor_type: 
        :param parameters: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomProcessorOptions.__init__)
            check_type(argname="argument processor_type", value=processor_type, expected_type=type_hints["processor_type"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[str, typing.Any] = {
            "processor_type": processor_type,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def processor_type(self) -> "ProcessorType":
        result = self._values.get("processor_type")
        assert result is not None, "Required property 'processor_type' is missing"
        return typing.cast("ProcessorType", result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomProcessorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFormatConversion(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.DataFormatConversion",
):
    def __init__(
        self,
        *,
        database: _Database_5971ae38,
        input_format: "InputFormat",
        output_format: "OutputFormat",
        table: _Table_114d5aef,
        catalog_id: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        version: typing.Optional["TableVersion"] = None,
    ) -> None:
        '''
        :param database: 
        :param input_format: 
        :param output_format: 
        :param table: 
        :param catalog_id: 
        :param enabled: 
        :param region: 
        :param role: 
        :param version: 
        '''
        options = DataFormatConversionOptions(
            database=database,
            input_format=input_format,
            output_format=output_format,
            table=table,
            catalog_id=catalog_id,
            enabled=enabled,
            region=region,
            role=role,
            version=version,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.DataFormatConversionConfigurationProperty:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataFormatConversion.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.DataFormatConversionConfigurationProperty, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _Database_5971ae38:
        return typing.cast(_Database_5971ae38, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="inputFormat")
    def input_format(self) -> "InputFormat":
        return typing.cast("InputFormat", jsii.get(self, "inputFormat"))

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> "OutputFormat":
        return typing.cast("OutputFormat", jsii.get(self, "outputFormat"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _Table_114d5aef:
        return typing.cast(_Table_114d5aef, jsii.get(self, "table"))

    @builtins.property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogId"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional["TableVersion"]:
        return typing.cast(typing.Optional["TableVersion"], jsii.get(self, "version"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.DataFormatConversionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "input_format": "inputFormat",
        "output_format": "outputFormat",
        "table": "table",
        "catalog_id": "catalogId",
        "enabled": "enabled",
        "region": "region",
        "role": "role",
        "version": "version",
    },
)
class DataFormatConversionOptions:
    def __init__(
        self,
        *,
        database: _Database_5971ae38,
        input_format: "InputFormat",
        output_format: "OutputFormat",
        table: _Table_114d5aef,
        catalog_id: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        version: typing.Optional["TableVersion"] = None,
    ) -> None:
        '''
        :param database: 
        :param input_format: 
        :param output_format: 
        :param table: 
        :param catalog_id: 
        :param enabled: 
        :param region: 
        :param role: 
        :param version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataFormatConversionOptions.__init__)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument input_format", value=input_format, expected_type=type_hints["input_format"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[str, typing.Any] = {
            "database": database,
            "input_format": input_format,
            "output_format": output_format,
            "table": table,
        }
        if catalog_id is not None:
            self._values["catalog_id"] = catalog_id
        if enabled is not None:
            self._values["enabled"] = enabled
        if region is not None:
            self._values["region"] = region
        if role is not None:
            self._values["role"] = role
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def database(self) -> _Database_5971ae38:
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(_Database_5971ae38, result)

    @builtins.property
    def input_format(self) -> "InputFormat":
        result = self._values.get("input_format")
        assert result is not None, "Required property 'input_format' is missing"
        return typing.cast("InputFormat", result)

    @builtins.property
    def output_format(self) -> "OutputFormat":
        result = self._values.get("output_format")
        assert result is not None, "Required property 'output_format' is missing"
        return typing.cast("OutputFormat", result)

    @builtins.property
    def table(self) -> _Table_114d5aef:
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(_Table_114d5aef, result)

    @builtins.property
    def catalog_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def version(self) -> typing.Optional["TableVersion"]:
        result = self._values.get("version")
        return typing.cast(typing.Optional["TableVersion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFormatConversionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.DelimitedDeaggregationOptions",
    jsii_struct_bases=[],
    name_mapping={"delimiter": "delimiter"},
)
class DelimitedDeaggregationOptions:
    def __init__(self, *, delimiter: builtins.str) -> None:
        '''
        :param delimiter: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DelimitedDeaggregationOptions.__init__)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
        self._values: typing.Dict[str, typing.Any] = {
            "delimiter": delimiter,
        }

    @builtins.property
    def delimiter(self) -> builtins.str:
        result = self._values.get("delimiter")
        assert result is not None, "Required property 'delimiter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DelimitedDeaggregationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.DeliveryStreamAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_stream_arn": "deliveryStreamArn",
        "delivery_stream_name": "deliveryStreamName",
        "role": "role",
    },
)
class DeliveryStreamAttributes:
    def __init__(
        self,
        *,
        delivery_stream_arn: typing.Optional[builtins.str] = None,
        delivery_stream_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        '''
        :param delivery_stream_arn: 
        :param delivery_stream_name: 
        :param role: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStreamAttributes.__init__)
            check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
            check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[str, typing.Any] = {}
        if delivery_stream_arn is not None:
            self._values["delivery_stream_arn"] = delivery_stream_arn
        if delivery_stream_name is not None:
            self._values["delivery_stream_name"] = delivery_stream_name
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def delivery_stream_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("delivery_stream_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delivery_stream_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("delivery_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeliveryStreamAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeliveryStreamDestination(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.kinesis_firehose.DeliveryStreamDestination",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> "DeliveryStreamDestinationConfiguration":
        '''
        :param scope: -
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], jsii.get(self, "role"))


class _DeliveryStreamDestinationProxy(DeliveryStreamDestination):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> "DeliveryStreamDestinationConfiguration":
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStreamDestination.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("DeliveryStreamDestinationConfiguration", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DeliveryStreamDestination).__jsii_proxy_class__ = lambda : _DeliveryStreamDestinationProxy


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.DeliveryStreamDestinationConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "amazonopensearchservice_destination_configuration": "amazonopensearchserviceDestinationConfiguration",
        "elasticsearch_destination_configuration": "elasticsearchDestinationConfiguration",
        "extended_s3_destination_configuration": "extendedS3DestinationConfiguration",
        "http_endpoint_destination_configuration": "httpEndpointDestinationConfiguration",
        "redshift_destination_configuration": "redshiftDestinationConfiguration",
        "s3_destination_configuration": "s3DestinationConfiguration",
        "splunk_destination_configuration": "splunkDestinationConfiguration",
    },
)
class DeliveryStreamDestinationConfiguration:
    def __init__(
        self,
        *,
        amazonopensearchservice_destination_configuration: typing.Optional[typing.Union[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.AmazonopensearchserviceDestinationConfigurationProperty, typing.Dict[str, typing.Any]]] = None,
        elasticsearch_destination_configuration: typing.Optional[typing.Union[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty, typing.Dict[str, typing.Any]]] = None,
        extended_s3_destination_configuration: typing.Optional[typing.Union[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty, typing.Dict[str, typing.Any]]] = None,
        http_endpoint_destination_configuration: typing.Optional[typing.Union[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty, typing.Dict[str, typing.Any]]] = None,
        redshift_destination_configuration: typing.Optional[typing.Union[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.RedshiftDestinationConfigurationProperty, typing.Dict[str, typing.Any]]] = None,
        s3_destination_configuration: typing.Optional[typing.Union[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty, typing.Dict[str, typing.Any]]] = None,
        splunk_destination_configuration: typing.Optional[typing.Union[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.SplunkDestinationConfigurationProperty, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amazonopensearchservice_destination_configuration: 
        :param elasticsearch_destination_configuration: 
        :param extended_s3_destination_configuration: 
        :param http_endpoint_destination_configuration: 
        :param redshift_destination_configuration: 
        :param s3_destination_configuration: 
        :param splunk_destination_configuration: 
        '''
        if isinstance(amazonopensearchservice_destination_configuration, dict):
            amazonopensearchservice_destination_configuration = aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.AmazonopensearchserviceDestinationConfigurationProperty(**amazonopensearchservice_destination_configuration)
        if isinstance(elasticsearch_destination_configuration, dict):
            elasticsearch_destination_configuration = aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty(**elasticsearch_destination_configuration)
        if isinstance(extended_s3_destination_configuration, dict):
            extended_s3_destination_configuration = aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty(**extended_s3_destination_configuration)
        if isinstance(http_endpoint_destination_configuration, dict):
            http_endpoint_destination_configuration = aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty(**http_endpoint_destination_configuration)
        if isinstance(redshift_destination_configuration, dict):
            redshift_destination_configuration = aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.RedshiftDestinationConfigurationProperty(**redshift_destination_configuration)
        if isinstance(s3_destination_configuration, dict):
            s3_destination_configuration = aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty(**s3_destination_configuration)
        if isinstance(splunk_destination_configuration, dict):
            splunk_destination_configuration = aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.SplunkDestinationConfigurationProperty(**splunk_destination_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStreamDestinationConfiguration.__init__)
            check_type(argname="argument amazonopensearchservice_destination_configuration", value=amazonopensearchservice_destination_configuration, expected_type=type_hints["amazonopensearchservice_destination_configuration"])
            check_type(argname="argument elasticsearch_destination_configuration", value=elasticsearch_destination_configuration, expected_type=type_hints["elasticsearch_destination_configuration"])
            check_type(argname="argument extended_s3_destination_configuration", value=extended_s3_destination_configuration, expected_type=type_hints["extended_s3_destination_configuration"])
            check_type(argname="argument http_endpoint_destination_configuration", value=http_endpoint_destination_configuration, expected_type=type_hints["http_endpoint_destination_configuration"])
            check_type(argname="argument redshift_destination_configuration", value=redshift_destination_configuration, expected_type=type_hints["redshift_destination_configuration"])
            check_type(argname="argument s3_destination_configuration", value=s3_destination_configuration, expected_type=type_hints["s3_destination_configuration"])
            check_type(argname="argument splunk_destination_configuration", value=splunk_destination_configuration, expected_type=type_hints["splunk_destination_configuration"])
        self._values: typing.Dict[str, typing.Any] = {}
        if amazonopensearchservice_destination_configuration is not None:
            self._values["amazonopensearchservice_destination_configuration"] = amazonopensearchservice_destination_configuration
        if elasticsearch_destination_configuration is not None:
            self._values["elasticsearch_destination_configuration"] = elasticsearch_destination_configuration
        if extended_s3_destination_configuration is not None:
            self._values["extended_s3_destination_configuration"] = extended_s3_destination_configuration
        if http_endpoint_destination_configuration is not None:
            self._values["http_endpoint_destination_configuration"] = http_endpoint_destination_configuration
        if redshift_destination_configuration is not None:
            self._values["redshift_destination_configuration"] = redshift_destination_configuration
        if s3_destination_configuration is not None:
            self._values["s3_destination_configuration"] = s3_destination_configuration
        if splunk_destination_configuration is not None:
            self._values["splunk_destination_configuration"] = splunk_destination_configuration

    @builtins.property
    def amazonopensearchservice_destination_configuration(
        self,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.AmazonopensearchserviceDestinationConfigurationProperty]:
        result = self._values.get("amazonopensearchservice_destination_configuration")
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.AmazonopensearchserviceDestinationConfigurationProperty], result)

    @builtins.property
    def elasticsearch_destination_configuration(
        self,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty]:
        result = self._values.get("elasticsearch_destination_configuration")
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty], result)

    @builtins.property
    def extended_s3_destination_configuration(
        self,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty]:
        result = self._values.get("extended_s3_destination_configuration")
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty], result)

    @builtins.property
    def http_endpoint_destination_configuration(
        self,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty]:
        result = self._values.get("http_endpoint_destination_configuration")
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.HttpEndpointDestinationConfigurationProperty], result)

    @builtins.property
    def redshift_destination_configuration(
        self,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.RedshiftDestinationConfigurationProperty]:
        result = self._values.get("redshift_destination_configuration")
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.RedshiftDestinationConfigurationProperty], result)

    @builtins.property
    def s3_destination_configuration(
        self,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty]:
        result = self._values.get("s3_destination_configuration")
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty], result)

    @builtins.property
    def splunk_destination_configuration(
        self,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.SplunkDestinationConfigurationProperty]:
        result = self._values.get("splunk_destination_configuration")
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.SplunkDestinationConfigurationProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeliveryStreamDestinationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeliveryStreamProcessor(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.DeliveryStreamProcessor",
):
    def __init__(
        self,
        *,
        processor_type: "ProcessorType",
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param processor_type: 
        :param parameters: 
        '''
        options = DeliveryStreamProcessorOptions(
            processor_type=processor_type, parameters=parameters
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addProcessorParameter")
    def _add_processor_parameter(self, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStreamProcessor._add_processor_parameter)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addProcessorParameter", [name, value]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ProcessorProperty:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStreamProcessor.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ProcessorProperty, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="processorType")
    def processor_type(self) -> "ProcessorType":
        return typing.cast("ProcessorType", jsii.get(self, "processorType"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.DeliveryStreamProcessorOptions",
    jsii_struct_bases=[],
    name_mapping={"processor_type": "processorType", "parameters": "parameters"},
)
class DeliveryStreamProcessorOptions:
    def __init__(
        self,
        *,
        processor_type: "ProcessorType",
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param processor_type: 
        :param parameters: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStreamProcessorOptions.__init__)
            check_type(argname="argument processor_type", value=processor_type, expected_type=type_hints["processor_type"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[str, typing.Any] = {
            "processor_type": processor_type,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def processor_type(self) -> "ProcessorType":
        result = self._values.get("processor_type")
        assert result is not None, "Required property 'processor_type' is missing"
        return typing.cast("ProcessorType", result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeliveryStreamProcessorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.DeliveryStreamProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "destination": "destination",
        "name": "name",
        "stream_type": "streamType",
    },
)
class DeliveryStreamProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        destination: DeliveryStreamDestination,
        name: typing.Optional[builtins.str] = None,
        stream_type: typing.Optional["DeliveryStreamType"] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param destination: 
        :param name: 
        :param stream_type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStreamProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stream_type", value=stream_type, expected_type=type_hints["stream_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "destination": destination,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if name is not None:
            self._values["name"] = name
        if stream_type is not None:
            self._values["stream_type"] = stream_type

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
    def destination(self) -> DeliveryStreamDestination:
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(DeliveryStreamDestination, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream_type(self) -> typing.Optional["DeliveryStreamType"]:
        result = self._values.get("stream_type")
        return typing.cast(typing.Optional["DeliveryStreamType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeliveryStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.kinesis_firehose.DeliveryStreamType")
class DeliveryStreamType(enum.Enum):
    DIRECT_PUT = "DIRECT_PUT"
    KINESIS_STREAM_AS_SOURCE = "KINESIS_STREAM_AS_SOURCE"


class DynamicPartitioning(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.DynamicPartitioning",
):
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        retry_interval: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param enabled: 
        :param retry_interval: 
        '''
        options = CommonPartitioningOptions(
            enabled=enabled, retry_interval=retry_interval
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="fromJson")
    @builtins.classmethod
    def from_json(
        cls,
        *,
        partitions: typing.Mapping[builtins.str, builtins.str],
        enabled: typing.Optional[builtins.bool] = None,
        retry_interval: typing.Optional[aws_cdk.Duration] = None,
    ) -> "JsonPartitioningSource":
        '''
        :param partitions: 
        :param enabled: 
        :param retry_interval: 
        '''
        options = JsonPartitioningOptions(
            partitions=partitions, enabled=enabled, retry_interval=retry_interval
        )

        return typing.cast("JsonPartitioningSource", jsii.sinvoke(cls, "fromJson", [options]))

    @jsii.member(jsii_name="fromLambda")
    @builtins.classmethod
    def from_lambda(
        cls,
        *,
        lambda_function: aws_cdk.aws_lambda.IFunction,
        enabled: typing.Optional[builtins.bool] = None,
        retry_interval: typing.Optional[aws_cdk.Duration] = None,
    ) -> "LambdaPartitioningSource":
        '''
        :param lambda_function: 
        :param enabled: 
        :param retry_interval: 
        '''
        options = LambdaPartitioningOptions(
            lambda_function=lambda_function,
            enabled=enabled,
            retry_interval=retry_interval,
        )

        return typing.cast("LambdaPartitioningSource", jsii.sinvoke(cls, "fromLambda", [options]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> "DynamicPartitioningConfiguration":
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DynamicPartitioning.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast("DynamicPartitioningConfiguration", jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="retryInterval")
    def retry_interval(self) -> typing.Optional[aws_cdk.Duration]:
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "retryInterval"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.DynamicPartitioningConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "partitioning_configuration": "partitioningConfiguration",
        "processors": "processors",
    },
)
class DynamicPartitioningConfiguration:
    def __init__(
        self,
        *,
        partitioning_configuration: typing.Union[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.DynamicPartitioningConfigurationProperty, typing.Dict[str, typing.Any]],
        processors: typing.Optional[typing.Sequence[DeliveryStreamProcessor]] = None,
    ) -> None:
        '''
        :param partitioning_configuration: 
        :param processors: 
        '''
        if isinstance(partitioning_configuration, dict):
            partitioning_configuration = aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.DynamicPartitioningConfigurationProperty(**partitioning_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(DynamicPartitioningConfiguration.__init__)
            check_type(argname="argument partitioning_configuration", value=partitioning_configuration, expected_type=type_hints["partitioning_configuration"])
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
        self._values: typing.Dict[str, typing.Any] = {
            "partitioning_configuration": partitioning_configuration,
        }
        if processors is not None:
            self._values["processors"] = processors

    @builtins.property
    def partitioning_configuration(
        self,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.DynamicPartitioningConfigurationProperty:
        result = self._values.get("partitioning_configuration")
        assert result is not None, "Required property 'partitioning_configuration' is missing"
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.DynamicPartitioningConfigurationProperty, result)

    @builtins.property
    def processors(self) -> typing.Optional[typing.List[DeliveryStreamProcessor]]:
        result = self._values.get("processors")
        return typing.cast(typing.Optional[typing.List[DeliveryStreamProcessor]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamicPartitioningConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.HiveJsonInputSerDeOptions",
    jsii_struct_bases=[],
    name_mapping={"timestamp_formats": "timestampFormats"},
)
class HiveJsonInputSerDeOptions:
    def __init__(
        self,
        *,
        timestamp_formats: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param timestamp_formats: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HiveJsonInputSerDeOptions.__init__)
            check_type(argname="argument timestamp_formats", value=timestamp_formats, expected_type=type_hints["timestamp_formats"])
        self._values: typing.Dict[str, typing.Any] = {}
        if timestamp_formats is not None:
            self._values["timestamp_formats"] = timestamp_formats

    @builtins.property
    def timestamp_formats(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("timestamp_formats")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HiveJsonInputSerDeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpEndpointDestination(
    DeliveryStreamDestination,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.HttpEndpointDestination",
):
    def __init__(
        self,
        url: builtins.str,
        *,
        access_key: typing.Optional[aws_cdk.SecretValue] = None,
        backup_configuration: typing.Optional[BackupConfiguration] = None,
        buffering: typing.Optional[BufferingConfiguration] = None,
        cloudwatch_logging_configuration: typing.Optional[CloudWatchLoggingConfiguration] = None,
        common_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        content_encoding: typing.Optional[ContentEncoding] = None,
        endpoint_name: typing.Optional[builtins.str] = None,
        processor_configuration: typing.Optional["ProcessorConfiguration"] = None,
        retry_duration: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param url: -
        :param access_key: 
        :param backup_configuration: 
        :param buffering: 
        :param cloudwatch_logging_configuration: 
        :param common_attributes: 
        :param content_encoding: 
        :param endpoint_name: 
        :param processor_configuration: 
        :param retry_duration: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpEndpointDestination.__init__)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        options = HttpEndpointDestinationOptions(
            access_key=access_key,
            backup_configuration=backup_configuration,
            buffering=buffering,
            cloudwatch_logging_configuration=cloudwatch_logging_configuration,
            common_attributes=common_attributes,
            content_encoding=content_encoding,
            endpoint_name=endpoint_name,
            processor_configuration=processor_configuration,
            retry_duration=retry_duration,
        )

        jsii.create(self.__class__, self, [url, options])

    @jsii.member(jsii_name="addCommonAttribute")
    def add_common_attribute(
        self,
        name: builtins.str,
        value: builtins.str,
    ) -> "HttpEndpointDestination":
        '''
        :param name: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpEndpointDestination.add_common_attribute)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("HttpEndpointDestination", jsii.invoke(self, "addCommonAttribute", [name, value]))

    @jsii.member(jsii_name="addProcessor")
    def add_processor(
        self,
        processor: DeliveryStreamProcessor,
    ) -> "HttpEndpointDestination":
        '''
        :param processor: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpEndpointDestination.add_processor)
            check_type(argname="argument processor", value=processor, expected_type=type_hints["processor"])
        return typing.cast("HttpEndpointDestination", jsii.invoke(self, "addProcessor", [processor]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> DeliveryStreamDestinationConfiguration:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpEndpointDestination.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(DeliveryStreamDestinationConfiguration, jsii.invoke(self, "bind", [scope]))

    @jsii.member(jsii_name="buildBackupConfiguration")
    def _build_backup_configuration(
        self,
        scope: constructs.IConstruct,
    ) -> BackupConfiguration:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpEndpointDestination._build_backup_configuration)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(BackupConfiguration, jsii.invoke(self, "buildBackupConfiguration", [scope]))

    @jsii.member(jsii_name="getOrCreateRole")
    def _get_or_create_role(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_iam.IRole:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpEndpointDestination._get_or_create_role)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.invoke(self, "getOrCreateRole", [scope]))

    @jsii.member(jsii_name="renderProcessorConfiguration")
    def _render_processor_configuration(
        self,
        scope: constructs.IConstruct,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty]:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpEndpointDestination._render_processor_configuration)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty], jsii.invoke(self, "renderProcessorConfiguration", [scope]))

    @builtins.property
    @jsii.member(jsii_name="endpointUrl")
    def endpoint_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointUrl"))

    @builtins.property
    @jsii.member(jsii_name="processingEnabled")
    def processing_enabled(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "processingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> typing.Optional[aws_cdk.SecretValue]:
        return typing.cast(typing.Optional[aws_cdk.SecretValue], jsii.get(self, "accessKey"))

    @builtins.property
    @jsii.member(jsii_name="backupConfiguration")
    def backup_configuration(self) -> typing.Optional[BackupConfiguration]:
        return typing.cast(typing.Optional[BackupConfiguration], jsii.get(self, "backupConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="buffering")
    def buffering(self) -> typing.Optional[BufferingConfiguration]:
        return typing.cast(typing.Optional[BufferingConfiguration], jsii.get(self, "buffering"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingConfiguration")
    def cloudwatch_logging_configuration(
        self,
    ) -> typing.Optional[CloudWatchLoggingConfiguration]:
        return typing.cast(typing.Optional[CloudWatchLoggingConfiguration], jsii.get(self, "cloudwatchLoggingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="commonAttributes")
    def common_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "commonAttributes"))

    @builtins.property
    @jsii.member(jsii_name="contentEncoding")
    def content_encoding(self) -> typing.Optional[ContentEncoding]:
        return typing.cast(typing.Optional[ContentEncoding], jsii.get(self, "contentEncoding"))

    @builtins.property
    @jsii.member(jsii_name="endpointName")
    def endpoint_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointName"))

    @builtins.property
    @jsii.member(jsii_name="processorConfiguration")
    def processor_configuration(self) -> typing.Optional["ProcessorConfiguration"]:
        return typing.cast(typing.Optional["ProcessorConfiguration"], jsii.get(self, "processorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="retryDuration")
    def retry_duration(self) -> typing.Optional[aws_cdk.Duration]:
        return typing.cast(typing.Optional[aws_cdk.Duration], jsii.get(self, "retryDuration"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.HttpEndpointDestinationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "backup_configuration": "backupConfiguration",
        "buffering": "buffering",
        "cloudwatch_logging_configuration": "cloudwatchLoggingConfiguration",
        "common_attributes": "commonAttributes",
        "content_encoding": "contentEncoding",
        "endpoint_name": "endpointName",
        "processor_configuration": "processorConfiguration",
        "retry_duration": "retryDuration",
    },
)
class HttpEndpointDestinationOptions:
    def __init__(
        self,
        *,
        access_key: typing.Optional[aws_cdk.SecretValue] = None,
        backup_configuration: typing.Optional[BackupConfiguration] = None,
        buffering: typing.Optional[BufferingConfiguration] = None,
        cloudwatch_logging_configuration: typing.Optional[CloudWatchLoggingConfiguration] = None,
        common_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        content_encoding: typing.Optional[ContentEncoding] = None,
        endpoint_name: typing.Optional[builtins.str] = None,
        processor_configuration: typing.Optional["ProcessorConfiguration"] = None,
        retry_duration: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param access_key: 
        :param backup_configuration: 
        :param buffering: 
        :param cloudwatch_logging_configuration: 
        :param common_attributes: 
        :param content_encoding: 
        :param endpoint_name: 
        :param processor_configuration: 
        :param retry_duration: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HttpEndpointDestinationOptions.__init__)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument backup_configuration", value=backup_configuration, expected_type=type_hints["backup_configuration"])
            check_type(argname="argument buffering", value=buffering, expected_type=type_hints["buffering"])
            check_type(argname="argument cloudwatch_logging_configuration", value=cloudwatch_logging_configuration, expected_type=type_hints["cloudwatch_logging_configuration"])
            check_type(argname="argument common_attributes", value=common_attributes, expected_type=type_hints["common_attributes"])
            check_type(argname="argument content_encoding", value=content_encoding, expected_type=type_hints["content_encoding"])
            check_type(argname="argument endpoint_name", value=endpoint_name, expected_type=type_hints["endpoint_name"])
            check_type(argname="argument processor_configuration", value=processor_configuration, expected_type=type_hints["processor_configuration"])
            check_type(argname="argument retry_duration", value=retry_duration, expected_type=type_hints["retry_duration"])
        self._values: typing.Dict[str, typing.Any] = {}
        if access_key is not None:
            self._values["access_key"] = access_key
        if backup_configuration is not None:
            self._values["backup_configuration"] = backup_configuration
        if buffering is not None:
            self._values["buffering"] = buffering
        if cloudwatch_logging_configuration is not None:
            self._values["cloudwatch_logging_configuration"] = cloudwatch_logging_configuration
        if common_attributes is not None:
            self._values["common_attributes"] = common_attributes
        if content_encoding is not None:
            self._values["content_encoding"] = content_encoding
        if endpoint_name is not None:
            self._values["endpoint_name"] = endpoint_name
        if processor_configuration is not None:
            self._values["processor_configuration"] = processor_configuration
        if retry_duration is not None:
            self._values["retry_duration"] = retry_duration

    @builtins.property
    def access_key(self) -> typing.Optional[aws_cdk.SecretValue]:
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[aws_cdk.SecretValue], result)

    @builtins.property
    def backup_configuration(self) -> typing.Optional[BackupConfiguration]:
        result = self._values.get("backup_configuration")
        return typing.cast(typing.Optional[BackupConfiguration], result)

    @builtins.property
    def buffering(self) -> typing.Optional[BufferingConfiguration]:
        result = self._values.get("buffering")
        return typing.cast(typing.Optional[BufferingConfiguration], result)

    @builtins.property
    def cloudwatch_logging_configuration(
        self,
    ) -> typing.Optional[CloudWatchLoggingConfiguration]:
        result = self._values.get("cloudwatch_logging_configuration")
        return typing.cast(typing.Optional[CloudWatchLoggingConfiguration], result)

    @builtins.property
    def common_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("common_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def content_encoding(self) -> typing.Optional[ContentEncoding]:
        result = self._values.get("content_encoding")
        return typing.cast(typing.Optional[ContentEncoding], result)

    @builtins.property
    def endpoint_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("endpoint_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processor_configuration(self) -> typing.Optional["ProcessorConfiguration"]:
        result = self._values.get("processor_configuration")
        return typing.cast(typing.Optional["ProcessorConfiguration"], result)

    @builtins.property
    def retry_duration(self) -> typing.Optional[aws_cdk.Duration]:
        result = self._values.get("retry_duration")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpEndpointDestinationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-extensions.kinesis_firehose.IDeliveryStream")
class IDeliveryStream(
    aws_cdk.IResource,
    aws_cdk.aws_iam.IGrantable,
    aws_cdk.aws_ec2.IConnectable,
    typing_extensions.Protocol,
):
    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        '''
        :param grantee: -
        :param actions: -
        '''
        ...

    @jsii.member(jsii_name="grantPutRecords")
    def grant_put_records(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        '''
        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...

    @jsii.member(jsii_name="metricBackupToS3Bytes")
    def metric_backup_to_s3_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...

    @jsii.member(jsii_name="metricBackupToS3DataFreshness")
    def metric_backup_to_s3_data_freshness(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...

    @jsii.member(jsii_name="metricBackupToS3Records")
    def metric_backup_to_s3_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...

    @jsii.member(jsii_name="metricIncomingBytes")
    def metric_incoming_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...

    @jsii.member(jsii_name="metricIncomingRecords")
    def metric_incoming_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...


class _IDeliveryStreamProxy(
    jsii.proxy_for(aws_cdk.IResource), # type: ignore[misc]
    jsii.proxy_for(aws_cdk.aws_iam.IGrantable), # type: ignore[misc]
    jsii.proxy_for(aws_cdk.aws_ec2.IConnectable), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.kinesis_firehose.IDeliveryStream"

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamArn"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        '''
        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IDeliveryStream.grant)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantPutRecords")
    def grant_put_records(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        '''
        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IDeliveryStream.grant_put_records)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantPutRecords", [grantee]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IDeliveryStream.metric)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricBackupToS3Bytes")
    def metric_backup_to_s3_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricBackupToS3Bytes", [props]))

    @jsii.member(jsii_name="metricBackupToS3DataFreshness")
    def metric_backup_to_s3_data_freshness(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricBackupToS3DataFreshness", [props]))

    @jsii.member(jsii_name="metricBackupToS3Records")
    def metric_backup_to_s3_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricBackupToS3Records", [props]))

    @jsii.member(jsii_name="metricIncomingBytes")
    def metric_incoming_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIncomingBytes", [props]))

    @jsii.member(jsii_name="metricIncomingRecords")
    def metric_incoming_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIncomingRecords", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDeliveryStream).__jsii_proxy_class__ = lambda : _IDeliveryStreamProxy


@jsii.interface(
    jsii_type="cdk-extensions.kinesis_firehose.IDeliveryStreamBackupDestination"
)
class IDeliveryStreamBackupDestination(typing_extensions.Protocol):
    @jsii.member(jsii_name="renderBackupConfiguration")
    def render_backup_configuration(
        self,
        scope: constructs.IConstruct,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> BackupConfigurationResult:
        '''
        :param scope: -
        :param enabled: -
        '''
        ...


class _IDeliveryStreamBackupDestinationProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.kinesis_firehose.IDeliveryStreamBackupDestination"

    @jsii.member(jsii_name="renderBackupConfiguration")
    def render_backup_configuration(
        self,
        scope: constructs.IConstruct,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> BackupConfigurationResult:
        '''
        :param scope: -
        :param enabled: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IDeliveryStreamBackupDestination.render_backup_configuration)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        return typing.cast(BackupConfigurationResult, jsii.invoke(self, "renderBackupConfiguration", [scope, enabled]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDeliveryStreamBackupDestination).__jsii_proxy_class__ = lambda : _IDeliveryStreamBackupDestinationProxy


class InputFormat(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.kinesis_firehose.InputFormat",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="hiveJson")
    @builtins.classmethod
    def hive_json(
        cls,
        *,
        timestamp_formats: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "HiveJsonInputSerDe":
        '''
        :param timestamp_formats: 
        '''
        options = HiveJsonInputSerDeOptions(timestamp_formats=timestamp_formats)

        return typing.cast("HiveJsonInputSerDe", jsii.sinvoke(cls, "hiveJson", [options]))

    @jsii.member(jsii_name="openxJson")
    @builtins.classmethod
    def openx_json(
        cls,
        *,
        case_insensitive: typing.Optional[builtins.bool] = None,
        column_key_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        convert_dots_to_underscores: typing.Optional[builtins.bool] = None,
    ) -> "OpenxJsonInputSerDe":
        '''
        :param case_insensitive: 
        :param column_key_mappings: 
        :param convert_dots_to_underscores: 
        '''
        options = OpenxJsonInputSerDeOptions(
            case_insensitive=case_insensitive,
            column_key_mappings=column_key_mappings,
            convert_dots_to_underscores=convert_dots_to_underscores,
        )

        return typing.cast("OpenxJsonInputSerDe", jsii.sinvoke(cls, "openxJson", [options]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.InputFormatConfigurationProperty:
        '''
        :param scope: -
        '''
        ...


class _InputFormatProxy(InputFormat):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.InputFormatConfigurationProperty:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(InputFormat.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.InputFormatConfigurationProperty, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, InputFormat).__jsii_proxy_class__ = lambda : _InputFormatProxy


@jsii.enum(jsii_type="cdk-extensions.kinesis_firehose.JsonParsingEngine")
class JsonParsingEngine(enum.Enum):
    JQ_1_6 = "JQ_1_6"


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.JsonPartitioningOptions",
    jsii_struct_bases=[CommonPartitioningOptions],
    name_mapping={
        "enabled": "enabled",
        "retry_interval": "retryInterval",
        "partitions": "partitions",
    },
)
class JsonPartitioningOptions(CommonPartitioningOptions):
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        retry_interval: typing.Optional[aws_cdk.Duration] = None,
        partitions: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param enabled: 
        :param retry_interval: 
        :param partitions: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JsonPartitioningOptions.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument retry_interval", value=retry_interval, expected_type=type_hints["retry_interval"])
            check_type(argname="argument partitions", value=partitions, expected_type=type_hints["partitions"])
        self._values: typing.Dict[str, typing.Any] = {
            "partitions": partitions,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if retry_interval is not None:
            self._values["retry_interval"] = retry_interval

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retry_interval(self) -> typing.Optional[aws_cdk.Duration]:
        result = self._values.get("retry_interval")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def partitions(self) -> typing.Mapping[builtins.str, builtins.str]:
        result = self._values.get("partitions")
        assert result is not None, "Required property 'partitions' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsonPartitioningOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JsonPartitioningSource(
    DynamicPartitioning,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.JsonPartitioningSource",
):
    def __init__(
        self,
        *,
        partitions: typing.Mapping[builtins.str, builtins.str],
        enabled: typing.Optional[builtins.bool] = None,
        retry_interval: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param partitions: 
        :param enabled: 
        :param retry_interval: 
        '''
        options = JsonPartitioningOptions(
            partitions=partitions, enabled=enabled, retry_interval=retry_interval
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addPartition")
    def add_partition(self, name: builtins.str, query: builtins.str) -> None:
        '''
        :param name: -
        :param query: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JsonPartitioningSource.add_partition)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        return typing.cast(None, jsii.invoke(self, "addPartition", [name, query]))

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> DynamicPartitioningConfiguration:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JsonPartitioningSource.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(DynamicPartitioningConfiguration, jsii.invoke(self, "bind", [scope]))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.LambdaPartitioningOptions",
    jsii_struct_bases=[CommonPartitioningOptions],
    name_mapping={
        "enabled": "enabled",
        "retry_interval": "retryInterval",
        "lambda_function": "lambdaFunction",
    },
)
class LambdaPartitioningOptions(CommonPartitioningOptions):
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        retry_interval: typing.Optional[aws_cdk.Duration] = None,
        lambda_function: aws_cdk.aws_lambda.IFunction,
    ) -> None:
        '''
        :param enabled: 
        :param retry_interval: 
        :param lambda_function: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LambdaPartitioningOptions.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument retry_interval", value=retry_interval, expected_type=type_hints["retry_interval"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        self._values: typing.Dict[str, typing.Any] = {
            "lambda_function": lambda_function,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if retry_interval is not None:
            self._values["retry_interval"] = retry_interval

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retry_interval(self) -> typing.Optional[aws_cdk.Duration]:
        result = self._values.get("retry_interval")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def lambda_function(self) -> aws_cdk.aws_lambda.IFunction:
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(aws_cdk.aws_lambda.IFunction, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaPartitioningOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaPartitioningSource(
    DynamicPartitioning,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.LambdaPartitioningSource",
):
    def __init__(
        self,
        *,
        lambda_function: aws_cdk.aws_lambda.IFunction,
        enabled: typing.Optional[builtins.bool] = None,
        retry_interval: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param lambda_function: 
        :param enabled: 
        :param retry_interval: 
        '''
        options = LambdaPartitioningOptions(
            lambda_function=lambda_function,
            enabled=enabled,
            retry_interval=retry_interval,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> DynamicPartitioningConfiguration:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LambdaPartitioningSource.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(DynamicPartitioningConfiguration, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.IFunction:
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "lambdaFunction"))


class LambdaProcessor(
    DeliveryStreamProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.LambdaProcessor",
):
    def __init__(self, *, lambda_function: aws_cdk.aws_lambda.IFunction) -> None:
        '''
        :param lambda_function: 
        '''
        options = LambdaProcessorOptions(lambda_function=lambda_function)

        jsii.create(self.__class__, self, [options])

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.IFunction:
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "lambdaFunction"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.LambdaProcessorOptions",
    jsii_struct_bases=[],
    name_mapping={"lambda_function": "lambdaFunction"},
)
class LambdaProcessorOptions:
    def __init__(self, *, lambda_function: aws_cdk.aws_lambda.IFunction) -> None:
        '''
        :param lambda_function: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LambdaProcessorOptions.__init__)
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        self._values: typing.Dict[str, typing.Any] = {
            "lambda_function": lambda_function,
        }

    @builtins.property
    def lambda_function(self) -> aws_cdk.aws_lambda.IFunction:
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(aws_cdk.aws_lambda.IFunction, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaProcessorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetaDataExtractionQuery(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.MetaDataExtractionQuery",
):
    def __init__(self, query: builtins.str) -> None:
        '''
        :param query: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MetaDataExtractionQuery.__init__)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        jsii.create(self.__class__, self, [query])

    @jsii.member(jsii_name="jq")
    @builtins.classmethod
    def jq(cls, fields: typing.Mapping[builtins.str, builtins.str]) -> "JsonQuery":
        '''
        :param fields: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MetaDataExtractionQuery.jq)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
        return typing.cast("JsonQuery", jsii.sinvoke(cls, "jq", [fields]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, query: builtins.str) -> "MetaDataExtractionQuery":
        '''
        :param query: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MetaDataExtractionQuery.of)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        return typing.cast("MetaDataExtractionQuery", jsii.sinvoke(cls, "of", [query]))

    @jsii.member(jsii_name="render")
    def render(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "render", []))

    @builtins.property
    @jsii.member(jsii_name="query")
    def _query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @_query.setter
    def _query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(MetaDataExtractionQuery, "_query").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)


class MetadataExtractionProcessor(
    DeliveryStreamProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.MetadataExtractionProcessor",
):
    def __init__(
        self,
        *,
        query: MetaDataExtractionQuery,
        engine: typing.Optional[JsonParsingEngine] = None,
    ) -> None:
        '''
        :param query: 
        :param engine: 
        '''
        options = MetadataExtractionProcessorOptions(query=query, engine=engine)

        jsii.create(self.__class__, self, [options])

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> JsonParsingEngine:
        return typing.cast(JsonParsingEngine, jsii.get(self, "engine"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> MetaDataExtractionQuery:
        return typing.cast(MetaDataExtractionQuery, jsii.get(self, "query"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.MetadataExtractionProcessorOptions",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "engine": "engine"},
)
class MetadataExtractionProcessorOptions:
    def __init__(
        self,
        *,
        query: MetaDataExtractionQuery,
        engine: typing.Optional[JsonParsingEngine] = None,
    ) -> None:
        '''
        :param query: 
        :param engine: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MetadataExtractionProcessorOptions.__init__)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
        self._values: typing.Dict[str, typing.Any] = {
            "query": query,
        }
        if engine is not None:
            self._values["engine"] = engine

    @builtins.property
    def query(self) -> MetaDataExtractionQuery:
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(MetaDataExtractionQuery, result)

    @builtins.property
    def engine(self) -> typing.Optional[JsonParsingEngine]:
        result = self._values.get("engine")
        return typing.cast(typing.Optional[JsonParsingEngine], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetadataExtractionProcessorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OpenxJsonInputSerDe(
    InputFormat,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.OpenxJsonInputSerDe",
):
    def __init__(
        self,
        *,
        case_insensitive: typing.Optional[builtins.bool] = None,
        column_key_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        convert_dots_to_underscores: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param case_insensitive: 
        :param column_key_mappings: 
        :param convert_dots_to_underscores: 
        '''
        options = OpenxJsonInputSerDeOptions(
            case_insensitive=case_insensitive,
            column_key_mappings=column_key_mappings,
            convert_dots_to_underscores=convert_dots_to_underscores,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addColumnKeyMapping")
    def add_column_key_mapping(
        self,
        column_name: builtins.str,
        json_key: builtins.str,
    ) -> "OpenxJsonInputSerDe":
        '''
        :param column_name: -
        :param json_key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OpenxJsonInputSerDe.add_column_key_mapping)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument json_key", value=json_key, expected_type=type_hints["json_key"])
        return typing.cast("OpenxJsonInputSerDe", jsii.invoke(self, "addColumnKeyMapping", [column_name, json_key]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.InputFormatConfigurationProperty:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OpenxJsonInputSerDe.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.InputFormatConfigurationProperty, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="caseInsensitive")
    def case_insensitive(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "caseInsensitive"))

    @builtins.property
    @jsii.member(jsii_name="convertDotsToUnderscores")
    def convert_dots_to_underscores(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "convertDotsToUnderscores"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.OpenxJsonInputSerDeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "case_insensitive": "caseInsensitive",
        "column_key_mappings": "columnKeyMappings",
        "convert_dots_to_underscores": "convertDotsToUnderscores",
    },
)
class OpenxJsonInputSerDeOptions:
    def __init__(
        self,
        *,
        case_insensitive: typing.Optional[builtins.bool] = None,
        column_key_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        convert_dots_to_underscores: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param case_insensitive: 
        :param column_key_mappings: 
        :param convert_dots_to_underscores: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OpenxJsonInputSerDeOptions.__init__)
            check_type(argname="argument case_insensitive", value=case_insensitive, expected_type=type_hints["case_insensitive"])
            check_type(argname="argument column_key_mappings", value=column_key_mappings, expected_type=type_hints["column_key_mappings"])
            check_type(argname="argument convert_dots_to_underscores", value=convert_dots_to_underscores, expected_type=type_hints["convert_dots_to_underscores"])
        self._values: typing.Dict[str, typing.Any] = {}
        if case_insensitive is not None:
            self._values["case_insensitive"] = case_insensitive
        if column_key_mappings is not None:
            self._values["column_key_mappings"] = column_key_mappings
        if convert_dots_to_underscores is not None:
            self._values["convert_dots_to_underscores"] = convert_dots_to_underscores

    @builtins.property
    def case_insensitive(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("case_insensitive")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def column_key_mappings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("column_key_mappings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def convert_dots_to_underscores(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("convert_dots_to_underscores")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenxJsonInputSerDeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.kinesis_firehose.OrcCompressionFormat")
class OrcCompressionFormat(enum.Enum):
    NONE = "NONE"
    SNAPPY = "SNAPPY"
    ZLIB = "ZLIB"


@jsii.enum(jsii_type="cdk-extensions.kinesis_firehose.OrcFormatVersion")
class OrcFormatVersion(enum.Enum):
    V0_11 = "V0_11"
    V0_12 = "V0_12"


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.OrcOutputSerDeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "block_size_bytes": "blockSizeBytes",
        "bloom_filter_columns": "bloomFilterColumns",
        "bloom_filter_false_positive_probability": "bloomFilterFalsePositiveProbability",
        "compression": "compression",
        "dictionary_key_threshold": "dictionaryKeyThreshold",
        "enable_padding": "enablePadding",
        "format_version": "formatVersion",
        "padding_tolerance": "paddingTolerance",
        "row_index_stride": "rowIndexStride",
        "stripe_size_bytes": "stripeSizeBytes",
    },
)
class OrcOutputSerDeOptions:
    def __init__(
        self,
        *,
        block_size_bytes: typing.Optional[jsii.Number] = None,
        bloom_filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        bloom_filter_false_positive_probability: typing.Optional[jsii.Number] = None,
        compression: typing.Optional[OrcCompressionFormat] = None,
        dictionary_key_threshold: typing.Optional[jsii.Number] = None,
        enable_padding: typing.Optional[builtins.bool] = None,
        format_version: typing.Optional[OrcFormatVersion] = None,
        padding_tolerance: typing.Optional[jsii.Number] = None,
        row_index_stride: typing.Optional[jsii.Number] = None,
        stripe_size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param block_size_bytes: 
        :param bloom_filter_columns: 
        :param bloom_filter_false_positive_probability: 
        :param compression: 
        :param dictionary_key_threshold: 
        :param enable_padding: 
        :param format_version: 
        :param padding_tolerance: 
        :param row_index_stride: 
        :param stripe_size_bytes: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OrcOutputSerDeOptions.__init__)
            check_type(argname="argument block_size_bytes", value=block_size_bytes, expected_type=type_hints["block_size_bytes"])
            check_type(argname="argument bloom_filter_columns", value=bloom_filter_columns, expected_type=type_hints["bloom_filter_columns"])
            check_type(argname="argument bloom_filter_false_positive_probability", value=bloom_filter_false_positive_probability, expected_type=type_hints["bloom_filter_false_positive_probability"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument dictionary_key_threshold", value=dictionary_key_threshold, expected_type=type_hints["dictionary_key_threshold"])
            check_type(argname="argument enable_padding", value=enable_padding, expected_type=type_hints["enable_padding"])
            check_type(argname="argument format_version", value=format_version, expected_type=type_hints["format_version"])
            check_type(argname="argument padding_tolerance", value=padding_tolerance, expected_type=type_hints["padding_tolerance"])
            check_type(argname="argument row_index_stride", value=row_index_stride, expected_type=type_hints["row_index_stride"])
            check_type(argname="argument stripe_size_bytes", value=stripe_size_bytes, expected_type=type_hints["stripe_size_bytes"])
        self._values: typing.Dict[str, typing.Any] = {}
        if block_size_bytes is not None:
            self._values["block_size_bytes"] = block_size_bytes
        if bloom_filter_columns is not None:
            self._values["bloom_filter_columns"] = bloom_filter_columns
        if bloom_filter_false_positive_probability is not None:
            self._values["bloom_filter_false_positive_probability"] = bloom_filter_false_positive_probability
        if compression is not None:
            self._values["compression"] = compression
        if dictionary_key_threshold is not None:
            self._values["dictionary_key_threshold"] = dictionary_key_threshold
        if enable_padding is not None:
            self._values["enable_padding"] = enable_padding
        if format_version is not None:
            self._values["format_version"] = format_version
        if padding_tolerance is not None:
            self._values["padding_tolerance"] = padding_tolerance
        if row_index_stride is not None:
            self._values["row_index_stride"] = row_index_stride
        if stripe_size_bytes is not None:
            self._values["stripe_size_bytes"] = stripe_size_bytes

    @builtins.property
    def block_size_bytes(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("block_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bloom_filter_columns(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("bloom_filter_columns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def bloom_filter_false_positive_probability(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("bloom_filter_false_positive_probability")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def compression(self) -> typing.Optional[OrcCompressionFormat]:
        result = self._values.get("compression")
        return typing.cast(typing.Optional[OrcCompressionFormat], result)

    @builtins.property
    def dictionary_key_threshold(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("dictionary_key_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_padding(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_padding")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def format_version(self) -> typing.Optional[OrcFormatVersion]:
        result = self._values.get("format_version")
        return typing.cast(typing.Optional[OrcFormatVersion], result)

    @builtins.property
    def padding_tolerance(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("padding_tolerance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def row_index_stride(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("row_index_stride")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stripe_size_bytes(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("stripe_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrcOutputSerDeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OutputFormat(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.kinesis_firehose.OutputFormat",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="orc")
    @builtins.classmethod
    def orc(
        cls,
        *,
        block_size_bytes: typing.Optional[jsii.Number] = None,
        bloom_filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        bloom_filter_false_positive_probability: typing.Optional[jsii.Number] = None,
        compression: typing.Optional[OrcCompressionFormat] = None,
        dictionary_key_threshold: typing.Optional[jsii.Number] = None,
        enable_padding: typing.Optional[builtins.bool] = None,
        format_version: typing.Optional[OrcFormatVersion] = None,
        padding_tolerance: typing.Optional[jsii.Number] = None,
        row_index_stride: typing.Optional[jsii.Number] = None,
        stripe_size_bytes: typing.Optional[jsii.Number] = None,
    ) -> "OrcOutputSerDe":
        '''
        :param block_size_bytes: 
        :param bloom_filter_columns: 
        :param bloom_filter_false_positive_probability: 
        :param compression: 
        :param dictionary_key_threshold: 
        :param enable_padding: 
        :param format_version: 
        :param padding_tolerance: 
        :param row_index_stride: 
        :param stripe_size_bytes: 
        '''
        options = OrcOutputSerDeOptions(
            block_size_bytes=block_size_bytes,
            bloom_filter_columns=bloom_filter_columns,
            bloom_filter_false_positive_probability=bloom_filter_false_positive_probability,
            compression=compression,
            dictionary_key_threshold=dictionary_key_threshold,
            enable_padding=enable_padding,
            format_version=format_version,
            padding_tolerance=padding_tolerance,
            row_index_stride=row_index_stride,
            stripe_size_bytes=stripe_size_bytes,
        )

        return typing.cast("OrcOutputSerDe", jsii.sinvoke(cls, "orc", [options]))

    @jsii.member(jsii_name="parquet")
    @builtins.classmethod
    def parquet(
        cls,
        *,
        block_size_bytes: typing.Optional[jsii.Number] = None,
        compression: typing.Optional["ParquetCompressionFormat"] = None,
        enable_dictionary_compression: typing.Optional[builtins.bool] = None,
        max_padding_bytes: typing.Optional[jsii.Number] = None,
        page_size_bytes: typing.Optional[jsii.Number] = None,
        writer_version: typing.Optional["ParquetWriterVersion"] = None,
    ) -> "ParquetOutputSerDe":
        '''
        :param block_size_bytes: 
        :param compression: 
        :param enable_dictionary_compression: 
        :param max_padding_bytes: 
        :param page_size_bytes: 
        :param writer_version: 
        '''
        options = ParquetOutputSerDeOptions(
            block_size_bytes=block_size_bytes,
            compression=compression,
            enable_dictionary_compression=enable_dictionary_compression,
            max_padding_bytes=max_padding_bytes,
            page_size_bytes=page_size_bytes,
            writer_version=writer_version,
        )

        return typing.cast("ParquetOutputSerDe", jsii.sinvoke(cls, "parquet", [options]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.OutputFormatConfigurationProperty:
        '''
        :param scope: -
        '''
        ...


class _OutputFormatProxy(OutputFormat):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.OutputFormatConfigurationProperty:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OutputFormat.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.OutputFormatConfigurationProperty, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, OutputFormat).__jsii_proxy_class__ = lambda : _OutputFormatProxy


@jsii.enum(jsii_type="cdk-extensions.kinesis_firehose.ParquetCompressionFormat")
class ParquetCompressionFormat(enum.Enum):
    GZIP = "GZIP"
    SNAPPY = "SNAPPY"
    UNCOMPRESSED = "UNCOMPRESSED"


class ParquetOutputSerDe(
    OutputFormat,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.ParquetOutputSerDe",
):
    def __init__(
        self,
        *,
        block_size_bytes: typing.Optional[jsii.Number] = None,
        compression: typing.Optional[ParquetCompressionFormat] = None,
        enable_dictionary_compression: typing.Optional[builtins.bool] = None,
        max_padding_bytes: typing.Optional[jsii.Number] = None,
        page_size_bytes: typing.Optional[jsii.Number] = None,
        writer_version: typing.Optional["ParquetWriterVersion"] = None,
    ) -> None:
        '''
        :param block_size_bytes: 
        :param compression: 
        :param enable_dictionary_compression: 
        :param max_padding_bytes: 
        :param page_size_bytes: 
        :param writer_version: 
        '''
        options = ParquetOutputSerDeOptions(
            block_size_bytes=block_size_bytes,
            compression=compression,
            enable_dictionary_compression=enable_dictionary_compression,
            max_padding_bytes=max_padding_bytes,
            page_size_bytes=page_size_bytes,
            writer_version=writer_version,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.OutputFormatConfigurationProperty:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParquetOutputSerDe.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.OutputFormatConfigurationProperty, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="blockSizeBytes")
    def block_size_bytes(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "blockSizeBytes"))

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> typing.Optional[ParquetCompressionFormat]:
        return typing.cast(typing.Optional[ParquetCompressionFormat], jsii.get(self, "compression"))

    @builtins.property
    @jsii.member(jsii_name="enableDictionaryCompression")
    def enable_dictionary_compression(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableDictionaryCompression"))

    @builtins.property
    @jsii.member(jsii_name="maxPaddingBytes")
    def max_padding_bytes(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPaddingBytes"))

    @builtins.property
    @jsii.member(jsii_name="pageSizeBytes")
    def page_size_bytes(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pageSizeBytes"))

    @builtins.property
    @jsii.member(jsii_name="writerVersion")
    def writer_version(self) -> typing.Optional["ParquetWriterVersion"]:
        return typing.cast(typing.Optional["ParquetWriterVersion"], jsii.get(self, "writerVersion"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.ParquetOutputSerDeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "block_size_bytes": "blockSizeBytes",
        "compression": "compression",
        "enable_dictionary_compression": "enableDictionaryCompression",
        "max_padding_bytes": "maxPaddingBytes",
        "page_size_bytes": "pageSizeBytes",
        "writer_version": "writerVersion",
    },
)
class ParquetOutputSerDeOptions:
    def __init__(
        self,
        *,
        block_size_bytes: typing.Optional[jsii.Number] = None,
        compression: typing.Optional[ParquetCompressionFormat] = None,
        enable_dictionary_compression: typing.Optional[builtins.bool] = None,
        max_padding_bytes: typing.Optional[jsii.Number] = None,
        page_size_bytes: typing.Optional[jsii.Number] = None,
        writer_version: typing.Optional["ParquetWriterVersion"] = None,
    ) -> None:
        '''
        :param block_size_bytes: 
        :param compression: 
        :param enable_dictionary_compression: 
        :param max_padding_bytes: 
        :param page_size_bytes: 
        :param writer_version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ParquetOutputSerDeOptions.__init__)
            check_type(argname="argument block_size_bytes", value=block_size_bytes, expected_type=type_hints["block_size_bytes"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument enable_dictionary_compression", value=enable_dictionary_compression, expected_type=type_hints["enable_dictionary_compression"])
            check_type(argname="argument max_padding_bytes", value=max_padding_bytes, expected_type=type_hints["max_padding_bytes"])
            check_type(argname="argument page_size_bytes", value=page_size_bytes, expected_type=type_hints["page_size_bytes"])
            check_type(argname="argument writer_version", value=writer_version, expected_type=type_hints["writer_version"])
        self._values: typing.Dict[str, typing.Any] = {}
        if block_size_bytes is not None:
            self._values["block_size_bytes"] = block_size_bytes
        if compression is not None:
            self._values["compression"] = compression
        if enable_dictionary_compression is not None:
            self._values["enable_dictionary_compression"] = enable_dictionary_compression
        if max_padding_bytes is not None:
            self._values["max_padding_bytes"] = max_padding_bytes
        if page_size_bytes is not None:
            self._values["page_size_bytes"] = page_size_bytes
        if writer_version is not None:
            self._values["writer_version"] = writer_version

    @builtins.property
    def block_size_bytes(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("block_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def compression(self) -> typing.Optional[ParquetCompressionFormat]:
        result = self._values.get("compression")
        return typing.cast(typing.Optional[ParquetCompressionFormat], result)

    @builtins.property
    def enable_dictionary_compression(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dictionary_compression")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_padding_bytes(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_padding_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def page_size_bytes(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("page_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def writer_version(self) -> typing.Optional["ParquetWriterVersion"]:
        result = self._values.get("writer_version")
        return typing.cast(typing.Optional["ParquetWriterVersion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParquetOutputSerDeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.kinesis_firehose.ParquetWriterVersion")
class ParquetWriterVersion(enum.Enum):
    V1 = "V1"
    V2 = "V2"


class ProcessorConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.ProcessorConfiguration",
):
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        processors: typing.Optional[typing.Sequence[DeliveryStreamProcessor]] = None,
    ) -> None:
        '''
        :param enabled: 
        :param processors: 
        '''
        options = ProcessorConfigurationOptions(enabled=enabled, processors=processors)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: constructs.IConstruct) -> "ProcessorConfigurationResult":
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ProcessorConfiguration.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast("ProcessorConfigurationResult", jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="processors")
    def processors(self) -> typing.Optional[typing.List[DeliveryStreamProcessor]]:
        return typing.cast(typing.Optional[typing.List[DeliveryStreamProcessor]], jsii.get(self, "processors"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.ProcessorConfigurationOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "processors": "processors"},
)
class ProcessorConfigurationOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        processors: typing.Optional[typing.Sequence[DeliveryStreamProcessor]] = None,
    ) -> None:
        '''
        :param enabled: 
        :param processors: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ProcessorConfigurationOptions.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if processors is not None:
            self._values["processors"] = processors

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def processors(self) -> typing.Optional[typing.List[DeliveryStreamProcessor]]:
        result = self._values.get("processors")
        return typing.cast(typing.Optional[typing.List[DeliveryStreamProcessor]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcessorConfigurationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.ProcessorConfigurationResult",
    jsii_struct_bases=[],
    name_mapping={"processors": "processors", "enabled": "enabled"},
)
class ProcessorConfigurationResult:
    def __init__(
        self,
        *,
        processors: typing.Sequence[DeliveryStreamProcessor],
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param processors: 
        :param enabled: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ProcessorConfigurationResult.__init__)
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[str, typing.Any] = {
            "processors": processors,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def processors(self) -> typing.List[DeliveryStreamProcessor]:
        result = self._values.get("processors")
        assert result is not None, "Required property 'processors' is missing"
        return typing.cast(typing.List[DeliveryStreamProcessor], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcessorConfigurationResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcessorType(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.ProcessorType",
):
    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "ProcessorType":
        '''
        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ProcessorType.of)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("ProcessorType", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPEND_DELIMITER_TO_RECORD")
    def APPEND_DELIMITER_TO_RECORD(cls) -> "ProcessorType":
        return typing.cast("ProcessorType", jsii.sget(cls, "APPEND_DELIMITER_TO_RECORD"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LAMBDA")
    def LAMBDA_(cls) -> "ProcessorType":
        return typing.cast("ProcessorType", jsii.sget(cls, "LAMBDA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="METADATA_EXTRACTION")
    def METADATA_EXTRACTION(cls) -> "ProcessorType":
        return typing.cast("ProcessorType", jsii.sget(cls, "METADATA_EXTRACTION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RECORD_DEAGGREGATION")
    def RECORD_DEAGGREGATION(cls) -> "ProcessorType":
        return typing.cast("ProcessorType", jsii.sget(cls, "RECORD_DEAGGREGATION"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the processor to apply to the delivery stream.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class RecordDeaggregationProcessor(
    DeliveryStreamProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.RecordDeaggregationProcessor",
):
    def __init__(
        self,
        *,
        sub_record_type: "SubRecordType",
        delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sub_record_type: 
        :param delimiter: 
        '''
        options = RecordDeaggregationProcessorOptions(
            sub_record_type=sub_record_type, delimiter=delimiter
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="delimited")
    @builtins.classmethod
    def delimited(cls, *, delimiter: builtins.str) -> "RecordDeaggregationProcessor":
        '''
        :param delimiter: 
        '''
        options = DelimitedDeaggregationOptions(delimiter=delimiter)

        return typing.cast("RecordDeaggregationProcessor", jsii.sinvoke(cls, "delimited", [options]))

    @jsii.member(jsii_name="json")
    @builtins.classmethod
    def json(cls) -> "RecordDeaggregationProcessor":
        return typing.cast("RecordDeaggregationProcessor", jsii.sinvoke(cls, "json", []))

    @builtins.property
    @jsii.member(jsii_name="subRecordType")
    def sub_record_type(self) -> "SubRecordType":
        return typing.cast("SubRecordType", jsii.get(self, "subRecordType"))

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiter"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.RecordDeaggregationProcessorOptions",
    jsii_struct_bases=[],
    name_mapping={"sub_record_type": "subRecordType", "delimiter": "delimiter"},
)
class RecordDeaggregationProcessorOptions:
    def __init__(
        self,
        *,
        sub_record_type: "SubRecordType",
        delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sub_record_type: 
        :param delimiter: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RecordDeaggregationProcessorOptions.__init__)
            check_type(argname="argument sub_record_type", value=sub_record_type, expected_type=type_hints["sub_record_type"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
        self._values: typing.Dict[str, typing.Any] = {
            "sub_record_type": sub_record_type,
        }
        if delimiter is not None:
            self._values["delimiter"] = delimiter

    @builtins.property
    def sub_record_type(self) -> "SubRecordType":
        result = self._values.get("sub_record_type")
        assert result is not None, "Required property 'sub_record_type' is missing"
        return typing.cast("SubRecordType", result)

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RecordDeaggregationProcessorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-extensions.kinesis_firehose.S3CompressionFormat")
class S3CompressionFormat(enum.Enum):
    GZIP = "GZIP"
    HADOOP_SNAPPY = "HADOOP_SNAPPY"
    SNAPPY = "SNAPPY"
    UNCOMPRESSED = "UNCOMPRESSED"
    ZIP = "ZIP"


@jsii.implements(IDeliveryStreamBackupDestination)
class S3Destination(
    DeliveryStreamDestination,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.S3Destination",
):
    def __init__(
        self,
        bucket: aws_cdk.aws_s3.IBucket,
        *,
        buffering: typing.Optional[BufferingConfiguration] = None,
        cloudwatch_logging_configuration: typing.Optional[CloudWatchLoggingConfiguration] = None,
        compression_format: typing.Optional[S3CompressionFormat] = None,
        encryption_enabled: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        '''
        :param bucket: -
        :param buffering: 
        :param cloudwatch_logging_configuration: 
        :param compression_format: 
        :param encryption_enabled: 
        :param encryption_key: 
        :param error_output_prefix: 
        :param key_prefix: 
        :param role: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Destination.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        options = S3DestinationOptions(
            buffering=buffering,
            cloudwatch_logging_configuration=cloudwatch_logging_configuration,
            compression_format=compression_format,
            encryption_enabled=encryption_enabled,
            encryption_key=encryption_key,
            error_output_prefix=error_output_prefix,
            key_prefix=key_prefix,
            role=role,
        )

        jsii.create(self.__class__, self, [bucket, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> DeliveryStreamDestinationConfiguration:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Destination.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(DeliveryStreamDestinationConfiguration, jsii.invoke(self, "bind", [scope]))

    @jsii.member(jsii_name="buildConfiguration")
    def _build_configuration(
        self,
        scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Destination._build_configuration)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty, jsii.invoke(self, "buildConfiguration", [scope]))

    @jsii.member(jsii_name="renderBackupConfiguration")
    def render_backup_configuration(
        self,
        scope: constructs.IConstruct,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> BackupConfigurationResult:
        '''
        :param scope: -
        :param enabled: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3Destination.render_backup_configuration)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        return typing.cast(BackupConfigurationResult, jsii.invoke(self, "renderBackupConfiguration", [scope, enabled]))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        return typing.cast(aws_cdk.aws_s3.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="buffering")
    def buffering(self) -> typing.Optional[BufferingConfiguration]:
        return typing.cast(typing.Optional[BufferingConfiguration], jsii.get(self, "buffering"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingConfiguration")
    def cloudwatch_logging_configuration(
        self,
    ) -> typing.Optional[CloudWatchLoggingConfiguration]:
        return typing.cast(typing.Optional[CloudWatchLoggingConfiguration], jsii.get(self, "cloudwatchLoggingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="compressionFormat")
    def compression_format(self) -> typing.Optional[S3CompressionFormat]:
        return typing.cast(typing.Optional[S3CompressionFormat], jsii.get(self, "compressionFormat"))

    @builtins.property
    @jsii.member(jsii_name="encryptionEnabled")
    def encryption_enabled(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "encryptionEnabled"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="errorOutputPrefix")
    def error_output_prefix(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorOutputPrefix"))

    @builtins.property
    @jsii.member(jsii_name="keyPrefix")
    def key_prefix(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPrefix"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.S3DestinationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "buffering": "buffering",
        "cloudwatch_logging_configuration": "cloudwatchLoggingConfiguration",
        "compression_format": "compressionFormat",
        "encryption_enabled": "encryptionEnabled",
        "encryption_key": "encryptionKey",
        "error_output_prefix": "errorOutputPrefix",
        "key_prefix": "keyPrefix",
        "role": "role",
    },
)
class S3DestinationOptions:
    def __init__(
        self,
        *,
        buffering: typing.Optional[BufferingConfiguration] = None,
        cloudwatch_logging_configuration: typing.Optional[CloudWatchLoggingConfiguration] = None,
        compression_format: typing.Optional[S3CompressionFormat] = None,
        encryption_enabled: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        '''
        :param buffering: 
        :param cloudwatch_logging_configuration: 
        :param compression_format: 
        :param encryption_enabled: 
        :param encryption_key: 
        :param error_output_prefix: 
        :param key_prefix: 
        :param role: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3DestinationOptions.__init__)
            check_type(argname="argument buffering", value=buffering, expected_type=type_hints["buffering"])
            check_type(argname="argument cloudwatch_logging_configuration", value=cloudwatch_logging_configuration, expected_type=type_hints["cloudwatch_logging_configuration"])
            check_type(argname="argument compression_format", value=compression_format, expected_type=type_hints["compression_format"])
            check_type(argname="argument encryption_enabled", value=encryption_enabled, expected_type=type_hints["encryption_enabled"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
            check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[str, typing.Any] = {}
        if buffering is not None:
            self._values["buffering"] = buffering
        if cloudwatch_logging_configuration is not None:
            self._values["cloudwatch_logging_configuration"] = cloudwatch_logging_configuration
        if compression_format is not None:
            self._values["compression_format"] = compression_format
        if encryption_enabled is not None:
            self._values["encryption_enabled"] = encryption_enabled
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if error_output_prefix is not None:
            self._values["error_output_prefix"] = error_output_prefix
        if key_prefix is not None:
            self._values["key_prefix"] = key_prefix
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def buffering(self) -> typing.Optional[BufferingConfiguration]:
        result = self._values.get("buffering")
        return typing.cast(typing.Optional[BufferingConfiguration], result)

    @builtins.property
    def cloudwatch_logging_configuration(
        self,
    ) -> typing.Optional[CloudWatchLoggingConfiguration]:
        result = self._values.get("cloudwatch_logging_configuration")
        return typing.cast(typing.Optional[CloudWatchLoggingConfiguration], result)

    @builtins.property
    def compression_format(self) -> typing.Optional[S3CompressionFormat]:
        result = self._values.get("compression_format")
        return typing.cast(typing.Optional[S3CompressionFormat], result)

    @builtins.property
    def encryption_enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("encryption_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    @builtins.property
    def error_output_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("error_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3DestinationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SubRecordType(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.SubRecordType",
):
    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "SubRecordType":
        '''
        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SubRecordType.of)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("SubRecordType", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DELIMITED")
    def DELIMITED(cls) -> "SubRecordType":
        return typing.cast("SubRecordType", jsii.sget(cls, "DELIMITED"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="JSON")
    def JSON(cls) -> "SubRecordType":
        return typing.cast("SubRecordType", jsii.sget(cls, "JSON"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


class TableVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.TableVersion",
):
    @jsii.member(jsii_name="fixed")
    @builtins.classmethod
    def fixed(cls, version: jsii.Number) -> "TableVersion":
        '''
        :param version: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TableVersion.fixed)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("TableVersion", jsii.sinvoke(cls, "fixed", [version]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LATEST")
    def LATEST(cls) -> "TableVersion":
        return typing.cast("TableVersion", jsii.sget(cls, "LATEST"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))


class AppendDelimiterProcessor(
    DeliveryStreamProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.AppendDelimiterProcessor",
):
    def __init__(self, *, delimiter: builtins.str) -> None:
        '''
        :param delimiter: 
        '''
        options = AppendDelimiterProcessorOptions(delimiter=delimiter)

        jsii.create(self.__class__, self, [options])

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))


class CustomProcessor(
    DeliveryStreamProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.CustomProcessor",
):
    def __init__(
        self,
        *,
        processor_type: ProcessorType,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param processor_type: 
        :param parameters: 
        '''
        options = CustomProcessorOptions(
            processor_type=processor_type, parameters=parameters
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addParameter")
    def add_parameter(self, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomProcessor.add_parameter)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addParameter", [name, value]))


@jsii.implements(IDeliveryStream)
class DeliveryStream(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.DeliveryStream",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        destination: DeliveryStreamDestination,
        name: typing.Optional[builtins.str] = None,
        stream_type: typing.Optional[DeliveryStreamType] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param destination: 
        :param name: 
        :param stream_type: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStream.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DeliveryStreamProps(
            destination=destination,
            name=name,
            stream_type=stream_type,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDeliveryStreamArn")
    @builtins.classmethod
    def from_delivery_stream_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        delivery_stream_arn: builtins.str,
    ) -> IDeliveryStream:
        '''
        :param scope: -
        :param id: -
        :param delivery_stream_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStream.from_delivery_stream_arn)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
        return typing.cast(IDeliveryStream, jsii.sinvoke(cls, "fromDeliveryStreamArn", [scope, id, delivery_stream_arn]))

    @jsii.member(jsii_name="fromDeliveryStreamAttributes")
    @builtins.classmethod
    def from_delivery_stream_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        delivery_stream_arn: typing.Optional[builtins.str] = None,
        delivery_stream_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> IDeliveryStream:
        '''
        :param scope: -
        :param id: -
        :param delivery_stream_arn: 
        :param delivery_stream_name: 
        :param role: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStream.from_delivery_stream_attributes)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = DeliveryStreamAttributes(
            delivery_stream_arn=delivery_stream_arn,
            delivery_stream_name=delivery_stream_name,
            role=role,
        )

        return typing.cast(IDeliveryStream, jsii.sinvoke(cls, "fromDeliveryStreamAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromDeliveryStreamName")
    @builtins.classmethod
    def from_delivery_stream_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        delivery_stream_name: builtins.str,
    ) -> IDeliveryStream:
        '''
        :param scope: -
        :param id: -
        :param delivery_stream_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStream.from_delivery_stream_name)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
        return typing.cast(IDeliveryStream, jsii.sinvoke(cls, "fromDeliveryStreamName", [scope, id, delivery_stream_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        '''
        :param grantee: -
        :param actions: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStream.grant)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantPutRecords")
    def grant_put_records(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        '''
        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStream.grant_put_records)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantPutRecords", [grantee]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DeliveryStream.metric)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricBackupToS3Bytes")
    def metric_backup_to_s3_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricBackupToS3Bytes", [props]))

    @jsii.member(jsii_name="metricBackupToS3DataFreshness")
    def metric_backup_to_s3_data_freshness(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricBackupToS3DataFreshness", [props]))

    @jsii.member(jsii_name="metricBackupToS3Records")
    def metric_backup_to_s3_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricBackupToS3Records", [props]))

    @jsii.member(jsii_name="metricIncomingBytes")
    def metric_incoming_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIncomingBytes", [props]))

    @jsii.member(jsii_name="metricIncomingRecords")
    def metric_incoming_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[aws_cdk.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit] = None,
    ) -> aws_cdk.aws_cloudwatch.Metric:
        '''
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Use the factory functions on the ``Stats`` object to construct valid input strings. Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = aws_cdk.aws_cloudwatch.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(aws_cdk.aws_cloudwatch.Metric, jsii.invoke(self, "metricIncomingRecords", [props]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        '''The network connections associated with this resource.'''
        return typing.cast(aws_cdk.aws_ec2.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamArn"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamName"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> DeliveryStreamDestination:
        return typing.cast(DeliveryStreamDestination, jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(aws_cdk.aws_iam.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream:
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="streamType")
    def stream_type(self) -> typing.Optional[DeliveryStreamType]:
        return typing.cast(typing.Optional[DeliveryStreamType], jsii.get(self, "streamType"))


class ExtendedS3Destination(
    S3Destination,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.ExtendedS3Destination",
):
    def __init__(
        self,
        bucket: aws_cdk.aws_s3.IBucket,
        *,
        backup_configuration: typing.Optional[BackupConfiguration] = None,
        data_format_conversion: typing.Optional[DataFormatConversion] = None,
        dynamic_partitioning: typing.Optional[DynamicPartitioning] = None,
        processor_configuration: typing.Optional[ProcessorConfiguration] = None,
        buffering: typing.Optional[BufferingConfiguration] = None,
        cloudwatch_logging_configuration: typing.Optional[CloudWatchLoggingConfiguration] = None,
        compression_format: typing.Optional[S3CompressionFormat] = None,
        encryption_enabled: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        '''
        :param bucket: -
        :param backup_configuration: 
        :param data_format_conversion: 
        :param dynamic_partitioning: 
        :param processor_configuration: 
        :param buffering: 
        :param cloudwatch_logging_configuration: 
        :param compression_format: 
        :param encryption_enabled: 
        :param encryption_key: 
        :param error_output_prefix: 
        :param key_prefix: 
        :param role: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExtendedS3Destination.__init__)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        options = ExtendedS3DestinationOptions(
            backup_configuration=backup_configuration,
            data_format_conversion=data_format_conversion,
            dynamic_partitioning=dynamic_partitioning,
            processor_configuration=processor_configuration,
            buffering=buffering,
            cloudwatch_logging_configuration=cloudwatch_logging_configuration,
            compression_format=compression_format,
            encryption_enabled=encryption_enabled,
            encryption_key=encryption_key,
            error_output_prefix=error_output_prefix,
            key_prefix=key_prefix,
            role=role,
        )

        jsii.create(self.__class__, self, [bucket, options])

    @jsii.member(jsii_name="addProcessor")
    def add_processor(
        self,
        processor: DeliveryStreamProcessor,
    ) -> "ExtendedS3Destination":
        '''
        :param processor: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExtendedS3Destination.add_processor)
            check_type(argname="argument processor", value=processor, expected_type=type_hints["processor"])
        return typing.cast("ExtendedS3Destination", jsii.invoke(self, "addProcessor", [processor]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.IConstruct,
    ) -> DeliveryStreamDestinationConfiguration:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExtendedS3Destination.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(DeliveryStreamDestinationConfiguration, jsii.invoke(self, "bind", [scope]))

    @jsii.member(jsii_name="renderProcessorConfiguration")
    def _render_processor_configuration(
        self,
        scope: constructs.IConstruct,
    ) -> typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty]:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExtendedS3Destination._render_processor_configuration)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.Optional[aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty], jsii.invoke(self, "renderProcessorConfiguration", [scope]))

    @builtins.property
    @jsii.member(jsii_name="processingEnabled")
    def processing_enabled(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "processingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="processors")
    def processors(self) -> typing.List[DeliveryStreamProcessor]:
        return typing.cast(typing.List[DeliveryStreamProcessor], jsii.get(self, "processors"))

    @builtins.property
    @jsii.member(jsii_name="backupConfiguration")
    def backup_configuration(self) -> typing.Optional[BackupConfiguration]:
        return typing.cast(typing.Optional[BackupConfiguration], jsii.get(self, "backupConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="dataFormatConversion")
    def data_format_conversion(self) -> typing.Optional[DataFormatConversion]:
        return typing.cast(typing.Optional[DataFormatConversion], jsii.get(self, "dataFormatConversion"))

    @builtins.property
    @jsii.member(jsii_name="dynamicPartitioning")
    def dynamic_partitioning(self) -> typing.Optional[DynamicPartitioning]:
        return typing.cast(typing.Optional[DynamicPartitioning], jsii.get(self, "dynamicPartitioning"))

    @builtins.property
    @jsii.member(jsii_name="processorConfiguration")
    def processor_configuration(self) -> typing.Optional[ProcessorConfiguration]:
        return typing.cast(typing.Optional[ProcessorConfiguration], jsii.get(self, "processorConfiguration"))


@jsii.data_type(
    jsii_type="cdk-extensions.kinesis_firehose.ExtendedS3DestinationOptions",
    jsii_struct_bases=[S3DestinationOptions],
    name_mapping={
        "buffering": "buffering",
        "cloudwatch_logging_configuration": "cloudwatchLoggingConfiguration",
        "compression_format": "compressionFormat",
        "encryption_enabled": "encryptionEnabled",
        "encryption_key": "encryptionKey",
        "error_output_prefix": "errorOutputPrefix",
        "key_prefix": "keyPrefix",
        "role": "role",
        "backup_configuration": "backupConfiguration",
        "data_format_conversion": "dataFormatConversion",
        "dynamic_partitioning": "dynamicPartitioning",
        "processor_configuration": "processorConfiguration",
    },
)
class ExtendedS3DestinationOptions(S3DestinationOptions):
    def __init__(
        self,
        *,
        buffering: typing.Optional[BufferingConfiguration] = None,
        cloudwatch_logging_configuration: typing.Optional[CloudWatchLoggingConfiguration] = None,
        compression_format: typing.Optional[S3CompressionFormat] = None,
        encryption_enabled: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        backup_configuration: typing.Optional[BackupConfiguration] = None,
        data_format_conversion: typing.Optional[DataFormatConversion] = None,
        dynamic_partitioning: typing.Optional[DynamicPartitioning] = None,
        processor_configuration: typing.Optional[ProcessorConfiguration] = None,
    ) -> None:
        '''
        :param buffering: 
        :param cloudwatch_logging_configuration: 
        :param compression_format: 
        :param encryption_enabled: 
        :param encryption_key: 
        :param error_output_prefix: 
        :param key_prefix: 
        :param role: 
        :param backup_configuration: 
        :param data_format_conversion: 
        :param dynamic_partitioning: 
        :param processor_configuration: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ExtendedS3DestinationOptions.__init__)
            check_type(argname="argument buffering", value=buffering, expected_type=type_hints["buffering"])
            check_type(argname="argument cloudwatch_logging_configuration", value=cloudwatch_logging_configuration, expected_type=type_hints["cloudwatch_logging_configuration"])
            check_type(argname="argument compression_format", value=compression_format, expected_type=type_hints["compression_format"])
            check_type(argname="argument encryption_enabled", value=encryption_enabled, expected_type=type_hints["encryption_enabled"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
            check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument backup_configuration", value=backup_configuration, expected_type=type_hints["backup_configuration"])
            check_type(argname="argument data_format_conversion", value=data_format_conversion, expected_type=type_hints["data_format_conversion"])
            check_type(argname="argument dynamic_partitioning", value=dynamic_partitioning, expected_type=type_hints["dynamic_partitioning"])
            check_type(argname="argument processor_configuration", value=processor_configuration, expected_type=type_hints["processor_configuration"])
        self._values: typing.Dict[str, typing.Any] = {}
        if buffering is not None:
            self._values["buffering"] = buffering
        if cloudwatch_logging_configuration is not None:
            self._values["cloudwatch_logging_configuration"] = cloudwatch_logging_configuration
        if compression_format is not None:
            self._values["compression_format"] = compression_format
        if encryption_enabled is not None:
            self._values["encryption_enabled"] = encryption_enabled
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if error_output_prefix is not None:
            self._values["error_output_prefix"] = error_output_prefix
        if key_prefix is not None:
            self._values["key_prefix"] = key_prefix
        if role is not None:
            self._values["role"] = role
        if backup_configuration is not None:
            self._values["backup_configuration"] = backup_configuration
        if data_format_conversion is not None:
            self._values["data_format_conversion"] = data_format_conversion
        if dynamic_partitioning is not None:
            self._values["dynamic_partitioning"] = dynamic_partitioning
        if processor_configuration is not None:
            self._values["processor_configuration"] = processor_configuration

    @builtins.property
    def buffering(self) -> typing.Optional[BufferingConfiguration]:
        result = self._values.get("buffering")
        return typing.cast(typing.Optional[BufferingConfiguration], result)

    @builtins.property
    def cloudwatch_logging_configuration(
        self,
    ) -> typing.Optional[CloudWatchLoggingConfiguration]:
        result = self._values.get("cloudwatch_logging_configuration")
        return typing.cast(typing.Optional[CloudWatchLoggingConfiguration], result)

    @builtins.property
    def compression_format(self) -> typing.Optional[S3CompressionFormat]:
        result = self._values.get("compression_format")
        return typing.cast(typing.Optional[S3CompressionFormat], result)

    @builtins.property
    def encryption_enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("encryption_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    @builtins.property
    def error_output_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("error_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def backup_configuration(self) -> typing.Optional[BackupConfiguration]:
        result = self._values.get("backup_configuration")
        return typing.cast(typing.Optional[BackupConfiguration], result)

    @builtins.property
    def data_format_conversion(self) -> typing.Optional[DataFormatConversion]:
        result = self._values.get("data_format_conversion")
        return typing.cast(typing.Optional[DataFormatConversion], result)

    @builtins.property
    def dynamic_partitioning(self) -> typing.Optional[DynamicPartitioning]:
        result = self._values.get("dynamic_partitioning")
        return typing.cast(typing.Optional[DynamicPartitioning], result)

    @builtins.property
    def processor_configuration(self) -> typing.Optional[ProcessorConfiguration]:
        result = self._values.get("processor_configuration")
        return typing.cast(typing.Optional[ProcessorConfiguration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExtendedS3DestinationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HiveJsonInputSerDe(
    InputFormat,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.HiveJsonInputSerDe",
):
    def __init__(
        self,
        *,
        timestamp_formats: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param timestamp_formats: 
        '''
        options = HiveJsonInputSerDeOptions(timestamp_formats=timestamp_formats)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addTimestampFormat")
    def add_timestamp_format(self, format: builtins.str) -> "HiveJsonInputSerDe":
        '''
        :param format: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HiveJsonInputSerDe.add_timestamp_format)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        return typing.cast("HiveJsonInputSerDe", jsii.invoke(self, "addTimestampFormat", [format]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.InputFormatConfigurationProperty:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HiveJsonInputSerDe.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.InputFormatConfigurationProperty, jsii.invoke(self, "bind", [_scope]))


class JsonQuery(
    MetaDataExtractionQuery,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.JsonQuery",
):
    def __init__(
        self,
        fields: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param fields: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JsonQuery.__init__)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
        jsii.create(self.__class__, self, [fields])

    @jsii.member(jsii_name="addField")
    def add_field(self, name: builtins.str, query: builtins.str) -> "JsonQuery":
        '''
        :param name: -
        :param query: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(JsonQuery.add_field)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        return typing.cast("JsonQuery", jsii.invoke(self, "addField", [name, query]))


class OrcOutputSerDe(
    OutputFormat,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.kinesis_firehose.OrcOutputSerDe",
):
    def __init__(
        self,
        *,
        block_size_bytes: typing.Optional[jsii.Number] = None,
        bloom_filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        bloom_filter_false_positive_probability: typing.Optional[jsii.Number] = None,
        compression: typing.Optional[OrcCompressionFormat] = None,
        dictionary_key_threshold: typing.Optional[jsii.Number] = None,
        enable_padding: typing.Optional[builtins.bool] = None,
        format_version: typing.Optional[OrcFormatVersion] = None,
        padding_tolerance: typing.Optional[jsii.Number] = None,
        row_index_stride: typing.Optional[jsii.Number] = None,
        stripe_size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param block_size_bytes: 
        :param bloom_filter_columns: 
        :param bloom_filter_false_positive_probability: 
        :param compression: 
        :param dictionary_key_threshold: 
        :param enable_padding: 
        :param format_version: 
        :param padding_tolerance: 
        :param row_index_stride: 
        :param stripe_size_bytes: 
        '''
        options = OrcOutputSerDeOptions(
            block_size_bytes=block_size_bytes,
            bloom_filter_columns=bloom_filter_columns,
            bloom_filter_false_positive_probability=bloom_filter_false_positive_probability,
            compression=compression,
            dictionary_key_threshold=dictionary_key_threshold,
            enable_padding=enable_padding,
            format_version=format_version,
            padding_tolerance=padding_tolerance,
            row_index_stride=row_index_stride,
            stripe_size_bytes=stripe_size_bytes,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addBloomFilterColumn")
    def add_bloom_filter_column(self, column: builtins.str) -> "OrcOutputSerDe":
        '''
        :param column: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OrcOutputSerDe.add_bloom_filter_column)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
        return typing.cast("OrcOutputSerDe", jsii.invoke(self, "addBloomFilterColumn", [column]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.IConstruct,
    ) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.OutputFormatConfigurationProperty:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(OrcOutputSerDe.bind)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream.OutputFormatConfigurationProperty, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="blockSizeBytes")
    def block_size_bytes(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "blockSizeBytes"))

    @builtins.property
    @jsii.member(jsii_name="bloomFilterColumns")
    def bloom_filter_columns(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bloomFilterColumns"))

    @builtins.property
    @jsii.member(jsii_name="bloomFilterFalsePositiveProbability")
    def bloom_filter_false_positive_probability(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bloomFilterFalsePositiveProbability"))

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> typing.Optional[OrcCompressionFormat]:
        return typing.cast(typing.Optional[OrcCompressionFormat], jsii.get(self, "compression"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryKeyThreshold")
    def dictionary_key_threshold(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dictionaryKeyThreshold"))

    @builtins.property
    @jsii.member(jsii_name="enablePadding")
    def enable_padding(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enablePadding"))

    @builtins.property
    @jsii.member(jsii_name="formatVersion")
    def format_version(self) -> typing.Optional[OrcFormatVersion]:
        return typing.cast(typing.Optional[OrcFormatVersion], jsii.get(self, "formatVersion"))

    @builtins.property
    @jsii.member(jsii_name="paddingTolerance")
    def padding_tolerance(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "paddingTolerance"))

    @builtins.property
    @jsii.member(jsii_name="rowIndexStride")
    def row_index_stride(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowIndexStride"))

    @builtins.property
    @jsii.member(jsii_name="stripeSizeBytes")
    def stripe_size_bytes(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stripeSizeBytes"))


__all__ = [
    "AppendDelimiterProcessor",
    "AppendDelimiterProcessorOptions",
    "BackupConfiguration",
    "BackupConfigurationOptions",
    "BackupConfigurationResult",
    "BufferingConfiguration",
    "BufferingConfigurationOptions",
    "CloudWatchLoggingConfiguration",
    "CloudWatchLoggingConfigurationOptions",
    "CommonPartitioningOptions",
    "ContentEncoding",
    "CustomProcessor",
    "CustomProcessorOptions",
    "DataFormatConversion",
    "DataFormatConversionOptions",
    "DelimitedDeaggregationOptions",
    "DeliveryStream",
    "DeliveryStreamAttributes",
    "DeliveryStreamDestination",
    "DeliveryStreamDestinationConfiguration",
    "DeliveryStreamProcessor",
    "DeliveryStreamProcessorOptions",
    "DeliveryStreamProps",
    "DeliveryStreamType",
    "DynamicPartitioning",
    "DynamicPartitioningConfiguration",
    "ExtendedS3Destination",
    "ExtendedS3DestinationOptions",
    "HiveJsonInputSerDe",
    "HiveJsonInputSerDeOptions",
    "HttpEndpointDestination",
    "HttpEndpointDestinationOptions",
    "IDeliveryStream",
    "IDeliveryStreamBackupDestination",
    "InputFormat",
    "JsonParsingEngine",
    "JsonPartitioningOptions",
    "JsonPartitioningSource",
    "JsonQuery",
    "LambdaPartitioningOptions",
    "LambdaPartitioningSource",
    "LambdaProcessor",
    "LambdaProcessorOptions",
    "MetaDataExtractionQuery",
    "MetadataExtractionProcessor",
    "MetadataExtractionProcessorOptions",
    "OpenxJsonInputSerDe",
    "OpenxJsonInputSerDeOptions",
    "OrcCompressionFormat",
    "OrcFormatVersion",
    "OrcOutputSerDe",
    "OrcOutputSerDeOptions",
    "OutputFormat",
    "ParquetCompressionFormat",
    "ParquetOutputSerDe",
    "ParquetOutputSerDeOptions",
    "ParquetWriterVersion",
    "ProcessorConfiguration",
    "ProcessorConfigurationOptions",
    "ProcessorConfigurationResult",
    "ProcessorType",
    "RecordDeaggregationProcessor",
    "RecordDeaggregationProcessorOptions",
    "S3CompressionFormat",
    "S3Destination",
    "S3DestinationOptions",
    "SubRecordType",
    "TableVersion",
]

publication.publish()
