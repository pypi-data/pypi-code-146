'''
# `aws_kinesis_firehose_delivery_stream`

Refer to the Terraform Registory for docs: [`aws_kinesis_firehose_delivery_stream`](https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream).
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class KinesisFirehoseDeliveryStream(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStream",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream aws_kinesis_firehose_delivery_stream}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination: builtins.str,
        name: builtins.str,
        arn: typing.Optional[builtins.str] = None,
        destination_id: typing.Optional[builtins.str] = None,
        elasticsearch_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        extended_s3_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
        http_endpoint_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kinesis_source_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamKinesisSourceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
        server_side_encryption: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamServerSideEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        splunk_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream aws_kinesis_firehose_delivery_stream} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#destination KinesisFirehoseDeliveryStream#destination}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#name KinesisFirehoseDeliveryStream#name}.
        :param arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#arn KinesisFirehoseDeliveryStream#arn}.
        :param destination_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#destination_id KinesisFirehoseDeliveryStream#destination_id}.
        :param elasticsearch_configuration: elasticsearch_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#elasticsearch_configuration KinesisFirehoseDeliveryStream#elasticsearch_configuration}
        :param extended_s3_configuration: extended_s3_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#extended_s3_configuration KinesisFirehoseDeliveryStream#extended_s3_configuration}
        :param http_endpoint_configuration: http_endpoint_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#http_endpoint_configuration KinesisFirehoseDeliveryStream#http_endpoint_configuration}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#id KinesisFirehoseDeliveryStream#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kinesis_source_configuration: kinesis_source_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kinesis_source_configuration KinesisFirehoseDeliveryStream#kinesis_source_configuration}
        :param redshift_configuration: redshift_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#redshift_configuration KinesisFirehoseDeliveryStream#redshift_configuration}
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_configuration KinesisFirehoseDeliveryStream#s3_configuration}
        :param server_side_encryption: server_side_encryption block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#server_side_encryption KinesisFirehoseDeliveryStream#server_side_encryption}
        :param splunk_configuration: splunk_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#splunk_configuration KinesisFirehoseDeliveryStream#splunk_configuration}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#tags KinesisFirehoseDeliveryStream#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#tags_all KinesisFirehoseDeliveryStream#tags_all}.
        :param version_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#version_id KinesisFirehoseDeliveryStream#version_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c84a08dbf9a56758729a4e9f505fc49a3af04c826ca89339f2cbbacef64da8d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KinesisFirehoseDeliveryStreamConfig(
            destination=destination,
            name=name,
            arn=arn,
            destination_id=destination_id,
            elasticsearch_configuration=elasticsearch_configuration,
            extended_s3_configuration=extended_s3_configuration,
            http_endpoint_configuration=http_endpoint_configuration,
            id=id,
            kinesis_source_configuration=kinesis_source_configuration,
            redshift_configuration=redshift_configuration,
            s3_configuration=s3_configuration,
            server_side_encryption=server_side_encryption,
            splunk_configuration=splunk_configuration,
            tags=tags,
            tags_all=tags_all,
            version_id=version_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putElasticsearchConfiguration")
    def put_elasticsearch_configuration(
        self,
        *,
        index_name: builtins.str,
        role_arn: builtins.str,
        buffering_interval: typing.Optional[jsii.Number] = None,
        buffering_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_endpoint: typing.Optional[builtins.str] = None,
        domain_arn: typing.Optional[builtins.str] = None,
        index_rotation_period: typing.Optional[builtins.str] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_duration: typing.Optional[jsii.Number] = None,
        s3_backup_mode: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param index_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#index_name KinesisFirehoseDeliveryStream#index_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param buffering_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_interval KinesisFirehoseDeliveryStream#buffering_interval}.
        :param buffering_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_size KinesisFirehoseDeliveryStream#buffering_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param cluster_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cluster_endpoint KinesisFirehoseDeliveryStream#cluster_endpoint}.
        :param domain_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#domain_arn KinesisFirehoseDeliveryStream#domain_arn}.
        :param index_rotation_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#index_rotation_period KinesisFirehoseDeliveryStream#index_rotation_period}.
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        :param retry_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.
        :param s3_backup_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.
        :param type_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type_name KinesisFirehoseDeliveryStream#type_name}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#vpc_config KinesisFirehoseDeliveryStream#vpc_config}
        '''
        value = KinesisFirehoseDeliveryStreamElasticsearchConfiguration(
            index_name=index_name,
            role_arn=role_arn,
            buffering_interval=buffering_interval,
            buffering_size=buffering_size,
            cloudwatch_logging_options=cloudwatch_logging_options,
            cluster_endpoint=cluster_endpoint,
            domain_arn=domain_arn,
            index_rotation_period=index_rotation_period,
            processing_configuration=processing_configuration,
            retry_duration=retry_duration,
            s3_backup_mode=s3_backup_mode,
            type_name=type_name,
            vpc_config=vpc_config,
        )

        return typing.cast(None, jsii.invoke(self, "putElasticsearchConfiguration", [value]))

    @jsii.member(jsii_name="putExtendedS3Configuration")
    def put_extended_s3_configuration(
        self,
        *,
        bucket_arn: builtins.str,
        role_arn: builtins.str,
        buffer_interval: typing.Optional[jsii.Number] = None,
        buffer_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_format: typing.Optional[builtins.str] = None,
        data_format_conversion_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamic_partitioning_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_backup_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_backup_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param buffer_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.
        :param buffer_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param compression_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.
        :param data_format_conversion_configuration: data_format_conversion_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#data_format_conversion_configuration KinesisFirehoseDeliveryStream#data_format_conversion_configuration}
        :param dynamic_partitioning_configuration: dynamic_partitioning_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#dynamic_partitioning_configuration KinesisFirehoseDeliveryStream#dynamic_partitioning_configuration}
        :param error_output_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        :param s3_backup_configuration: s3_backup_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_configuration KinesisFirehoseDeliveryStream#s3_backup_configuration}
        :param s3_backup_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3Configuration(
            bucket_arn=bucket_arn,
            role_arn=role_arn,
            buffer_interval=buffer_interval,
            buffer_size=buffer_size,
            cloudwatch_logging_options=cloudwatch_logging_options,
            compression_format=compression_format,
            data_format_conversion_configuration=data_format_conversion_configuration,
            dynamic_partitioning_configuration=dynamic_partitioning_configuration,
            error_output_prefix=error_output_prefix,
            kms_key_arn=kms_key_arn,
            prefix=prefix,
            processing_configuration=processing_configuration,
            s3_backup_configuration=s3_backup_configuration,
            s3_backup_mode=s3_backup_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putExtendedS3Configuration", [value]))

    @jsii.member(jsii_name="putHttpEndpointConfiguration")
    def put_http_endpoint_configuration(
        self,
        *,
        url: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        buffering_interval: typing.Optional[jsii.Number] = None,
        buffering_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        request_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_duration: typing.Optional[jsii.Number] = None,
        role_arn: typing.Optional[builtins.str] = None,
        s3_backup_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#url KinesisFirehoseDeliveryStream#url}.
        :param access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#access_key KinesisFirehoseDeliveryStream#access_key}.
        :param buffering_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_interval KinesisFirehoseDeliveryStream#buffering_interval}.
        :param buffering_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_size KinesisFirehoseDeliveryStream#buffering_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#name KinesisFirehoseDeliveryStream#name}.
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        :param request_configuration: request_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#request_configuration KinesisFirehoseDeliveryStream#request_configuration}
        :param retry_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param s3_backup_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.
        '''
        value = KinesisFirehoseDeliveryStreamHttpEndpointConfiguration(
            url=url,
            access_key=access_key,
            buffering_interval=buffering_interval,
            buffering_size=buffering_size,
            cloudwatch_logging_options=cloudwatch_logging_options,
            name=name,
            processing_configuration=processing_configuration,
            request_configuration=request_configuration,
            retry_duration=retry_duration,
            role_arn=role_arn,
            s3_backup_mode=s3_backup_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpEndpointConfiguration", [value]))

    @jsii.member(jsii_name="putKinesisSourceConfiguration")
    def put_kinesis_source_configuration(
        self,
        *,
        kinesis_stream_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param kinesis_stream_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kinesis_stream_arn KinesisFirehoseDeliveryStream#kinesis_stream_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        '''
        value = KinesisFirehoseDeliveryStreamKinesisSourceConfiguration(
            kinesis_stream_arn=kinesis_stream_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisSourceConfiguration", [value]))

    @jsii.member(jsii_name="putRedshiftConfiguration")
    def put_redshift_configuration(
        self,
        *,
        cluster_jdbcurl: builtins.str,
        data_table_name: builtins.str,
        password: builtins.str,
        role_arn: builtins.str,
        username: builtins.str,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        copy_options: typing.Optional[builtins.str] = None,
        data_table_columns: typing.Optional[builtins.str] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_duration: typing.Optional[jsii.Number] = None,
        s3_backup_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_backup_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_jdbcurl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cluster_jdbcurl KinesisFirehoseDeliveryStream#cluster_jdbcurl}.
        :param data_table_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#data_table_name KinesisFirehoseDeliveryStream#data_table_name}.
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#password KinesisFirehoseDeliveryStream#password}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#username KinesisFirehoseDeliveryStream#username}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param copy_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#copy_options KinesisFirehoseDeliveryStream#copy_options}.
        :param data_table_columns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#data_table_columns KinesisFirehoseDeliveryStream#data_table_columns}.
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        :param retry_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.
        :param s3_backup_configuration: s3_backup_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_configuration KinesisFirehoseDeliveryStream#s3_backup_configuration}
        :param s3_backup_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.
        '''
        value = KinesisFirehoseDeliveryStreamRedshiftConfiguration(
            cluster_jdbcurl=cluster_jdbcurl,
            data_table_name=data_table_name,
            password=password,
            role_arn=role_arn,
            username=username,
            cloudwatch_logging_options=cloudwatch_logging_options,
            copy_options=copy_options,
            data_table_columns=data_table_columns,
            processing_configuration=processing_configuration,
            retry_duration=retry_duration,
            s3_backup_configuration=s3_backup_configuration,
            s3_backup_mode=s3_backup_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putRedshiftConfiguration", [value]))

    @jsii.member(jsii_name="putS3Configuration")
    def put_s3_configuration(
        self,
        *,
        bucket_arn: builtins.str,
        role_arn: builtins.str,
        buffer_interval: typing.Optional[jsii.Number] = None,
        buffer_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_format: typing.Optional[builtins.str] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param buffer_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.
        :param buffer_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param compression_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.
        :param error_output_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.
        '''
        value = KinesisFirehoseDeliveryStreamS3Configuration(
            bucket_arn=bucket_arn,
            role_arn=role_arn,
            buffer_interval=buffer_interval,
            buffer_size=buffer_size,
            cloudwatch_logging_options=cloudwatch_logging_options,
            compression_format=compression_format,
            error_output_prefix=error_output_prefix,
            kms_key_arn=kms_key_arn,
            prefix=prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putS3Configuration", [value]))

    @jsii.member(jsii_name="putServerSideEncryption")
    def put_server_side_encryption(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_arn: typing.Optional[builtins.str] = None,
        key_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#key_arn KinesisFirehoseDeliveryStream#key_arn}.
        :param key_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#key_type KinesisFirehoseDeliveryStream#key_type}.
        '''
        value = KinesisFirehoseDeliveryStreamServerSideEncryption(
            enabled=enabled, key_arn=key_arn, key_type=key_type
        )

        return typing.cast(None, jsii.invoke(self, "putServerSideEncryption", [value]))

    @jsii.member(jsii_name="putSplunkConfiguration")
    def put_splunk_configuration(
        self,
        *,
        hec_endpoint: builtins.str,
        hec_token: builtins.str,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        hec_acknowledgment_timeout: typing.Optional[jsii.Number] = None,
        hec_endpoint_type: typing.Optional[builtins.str] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_duration: typing.Optional[jsii.Number] = None,
        s3_backup_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hec_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_endpoint KinesisFirehoseDeliveryStream#hec_endpoint}.
        :param hec_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_token KinesisFirehoseDeliveryStream#hec_token}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param hec_acknowledgment_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_acknowledgment_timeout KinesisFirehoseDeliveryStream#hec_acknowledgment_timeout}.
        :param hec_endpoint_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_endpoint_type KinesisFirehoseDeliveryStream#hec_endpoint_type}.
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        :param retry_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.
        :param s3_backup_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.
        '''
        value = KinesisFirehoseDeliveryStreamSplunkConfiguration(
            hec_endpoint=hec_endpoint,
            hec_token=hec_token,
            cloudwatch_logging_options=cloudwatch_logging_options,
            hec_acknowledgment_timeout=hec_acknowledgment_timeout,
            hec_endpoint_type=hec_endpoint_type,
            processing_configuration=processing_configuration,
            retry_duration=retry_duration,
            s3_backup_mode=s3_backup_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putSplunkConfiguration", [value]))

    @jsii.member(jsii_name="resetArn")
    def reset_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArn", []))

    @jsii.member(jsii_name="resetDestinationId")
    def reset_destination_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationId", []))

    @jsii.member(jsii_name="resetElasticsearchConfiguration")
    def reset_elasticsearch_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchConfiguration", []))

    @jsii.member(jsii_name="resetExtendedS3Configuration")
    def reset_extended_s3_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendedS3Configuration", []))

    @jsii.member(jsii_name="resetHttpEndpointConfiguration")
    def reset_http_endpoint_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpEndpointConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKinesisSourceConfiguration")
    def reset_kinesis_source_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisSourceConfiguration", []))

    @jsii.member(jsii_name="resetRedshiftConfiguration")
    def reset_redshift_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshiftConfiguration", []))

    @jsii.member(jsii_name="resetS3Configuration")
    def reset_s3_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Configuration", []))

    @jsii.member(jsii_name="resetServerSideEncryption")
    def reset_server_side_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerSideEncryption", []))

    @jsii.member(jsii_name="resetSplunkConfiguration")
    def reset_splunk_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSplunkConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetVersionId")
    def reset_version_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchConfiguration")
    def elasticsearch_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamElasticsearchConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamElasticsearchConfigurationOutputReference", jsii.get(self, "elasticsearchConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="extendedS3Configuration")
    def extended_s3_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationOutputReference", jsii.get(self, "extendedS3Configuration"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpointConfiguration")
    def http_endpoint_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamHttpEndpointConfigurationOutputReference", jsii.get(self, "httpEndpointConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="kinesisSourceConfiguration")
    def kinesis_source_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamKinesisSourceConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamKinesisSourceConfigurationOutputReference", jsii.get(self, "kinesisSourceConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="redshiftConfiguration")
    def redshift_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamRedshiftConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamRedshiftConfigurationOutputReference", jsii.get(self, "redshiftConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3Configuration")
    def s3_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamS3ConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamS3ConfigurationOutputReference", jsii.get(self, "s3Configuration"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryption")
    def server_side_encryption(
        self,
    ) -> "KinesisFirehoseDeliveryStreamServerSideEncryptionOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamServerSideEncryptionOutputReference", jsii.get(self, "serverSideEncryption"))

    @builtins.property
    @jsii.member(jsii_name="splunkConfiguration")
    def splunk_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamSplunkConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamSplunkConfigurationOutputReference", jsii.get(self, "splunkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationIdInput")
    def destination_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchConfigurationInput")
    def elasticsearch_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfiguration"], jsii.get(self, "elasticsearchConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedS3ConfigurationInput")
    def extended_s3_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3Configuration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3Configuration"], jsii.get(self, "extendedS3ConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpointConfigurationInput")
    def http_endpoint_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfiguration"], jsii.get(self, "httpEndpointConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisSourceConfigurationInput")
    def kinesis_source_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamKinesisSourceConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamKinesisSourceConfiguration"], jsii.get(self, "kinesisSourceConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftConfigurationInput")
    def redshift_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfiguration"], jsii.get(self, "redshiftConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3ConfigurationInput")
    def s3_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamS3Configuration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamS3Configuration"], jsii.get(self, "s3ConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionInput")
    def server_side_encryption_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamServerSideEncryption"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamServerSideEncryption"], jsii.get(self, "serverSideEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="splunkConfigurationInput")
    def splunk_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamSplunkConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamSplunkConfiguration"], jsii.get(self, "splunkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionIdInput")
    def version_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8201ff2f513d08f18566df5558d8afaca3e6b4db6aa25a762b1bed6112c84d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value)

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__877e27e61487773bbc33f661eb98222d5880d081a19eace08e1a3c45fff9eb9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value)

    @builtins.property
    @jsii.member(jsii_name="destinationId")
    def destination_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationId"))

    @destination_id.setter
    def destination_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f364be141796cddf9ae0d9359b8120617a1af322bdce9c0de93b12b207c39a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c74f315910b3945d0e8182e866399c21cdd19a6b152767172135611c41700ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29b89adfd7340592015e8dc562d4e4d29568db58c6ced05595a20734f2cb7bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4230c987497fa60348e73d8c266cf3326cace333f00c17e3984d07b14f594cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fbddf32b5fc27bd30f119ff02a4c9c09c2679dc307e0f92c8ea22c5f6fc19c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e53441beca05381b91046524e107600bb8149201dad06e1fd2ebf90760d8aaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination": "destination",
        "name": "name",
        "arn": "arn",
        "destination_id": "destinationId",
        "elasticsearch_configuration": "elasticsearchConfiguration",
        "extended_s3_configuration": "extendedS3Configuration",
        "http_endpoint_configuration": "httpEndpointConfiguration",
        "id": "id",
        "kinesis_source_configuration": "kinesisSourceConfiguration",
        "redshift_configuration": "redshiftConfiguration",
        "s3_configuration": "s3Configuration",
        "server_side_encryption": "serverSideEncryption",
        "splunk_configuration": "splunkConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
        "version_id": "versionId",
    },
)
class KinesisFirehoseDeliveryStreamConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        destination: builtins.str,
        name: builtins.str,
        arn: typing.Optional[builtins.str] = None,
        destination_id: typing.Optional[builtins.str] = None,
        elasticsearch_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        extended_s3_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
        http_endpoint_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kinesis_source_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamKinesisSourceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
        server_side_encryption: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamServerSideEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        splunk_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#destination KinesisFirehoseDeliveryStream#destination}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#name KinesisFirehoseDeliveryStream#name}.
        :param arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#arn KinesisFirehoseDeliveryStream#arn}.
        :param destination_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#destination_id KinesisFirehoseDeliveryStream#destination_id}.
        :param elasticsearch_configuration: elasticsearch_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#elasticsearch_configuration KinesisFirehoseDeliveryStream#elasticsearch_configuration}
        :param extended_s3_configuration: extended_s3_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#extended_s3_configuration KinesisFirehoseDeliveryStream#extended_s3_configuration}
        :param http_endpoint_configuration: http_endpoint_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#http_endpoint_configuration KinesisFirehoseDeliveryStream#http_endpoint_configuration}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#id KinesisFirehoseDeliveryStream#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kinesis_source_configuration: kinesis_source_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kinesis_source_configuration KinesisFirehoseDeliveryStream#kinesis_source_configuration}
        :param redshift_configuration: redshift_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#redshift_configuration KinesisFirehoseDeliveryStream#redshift_configuration}
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_configuration KinesisFirehoseDeliveryStream#s3_configuration}
        :param server_side_encryption: server_side_encryption block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#server_side_encryption KinesisFirehoseDeliveryStream#server_side_encryption}
        :param splunk_configuration: splunk_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#splunk_configuration KinesisFirehoseDeliveryStream#splunk_configuration}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#tags KinesisFirehoseDeliveryStream#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#tags_all KinesisFirehoseDeliveryStream#tags_all}.
        :param version_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#version_id KinesisFirehoseDeliveryStream#version_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(elasticsearch_configuration, dict):
            elasticsearch_configuration = KinesisFirehoseDeliveryStreamElasticsearchConfiguration(**elasticsearch_configuration)
        if isinstance(extended_s3_configuration, dict):
            extended_s3_configuration = KinesisFirehoseDeliveryStreamExtendedS3Configuration(**extended_s3_configuration)
        if isinstance(http_endpoint_configuration, dict):
            http_endpoint_configuration = KinesisFirehoseDeliveryStreamHttpEndpointConfiguration(**http_endpoint_configuration)
        if isinstance(kinesis_source_configuration, dict):
            kinesis_source_configuration = KinesisFirehoseDeliveryStreamKinesisSourceConfiguration(**kinesis_source_configuration)
        if isinstance(redshift_configuration, dict):
            redshift_configuration = KinesisFirehoseDeliveryStreamRedshiftConfiguration(**redshift_configuration)
        if isinstance(s3_configuration, dict):
            s3_configuration = KinesisFirehoseDeliveryStreamS3Configuration(**s3_configuration)
        if isinstance(server_side_encryption, dict):
            server_side_encryption = KinesisFirehoseDeliveryStreamServerSideEncryption(**server_side_encryption)
        if isinstance(splunk_configuration, dict):
            splunk_configuration = KinesisFirehoseDeliveryStreamSplunkConfiguration(**splunk_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2848a7d0b903f54cc81b571a9272298c8f5c4bad6e8558b19eca1b2f357d1e9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument destination_id", value=destination_id, expected_type=type_hints["destination_id"])
            check_type(argname="argument elasticsearch_configuration", value=elasticsearch_configuration, expected_type=type_hints["elasticsearch_configuration"])
            check_type(argname="argument extended_s3_configuration", value=extended_s3_configuration, expected_type=type_hints["extended_s3_configuration"])
            check_type(argname="argument http_endpoint_configuration", value=http_endpoint_configuration, expected_type=type_hints["http_endpoint_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kinesis_source_configuration", value=kinesis_source_configuration, expected_type=type_hints["kinesis_source_configuration"])
            check_type(argname="argument redshift_configuration", value=redshift_configuration, expected_type=type_hints["redshift_configuration"])
            check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            check_type(argname="argument server_side_encryption", value=server_side_encryption, expected_type=type_hints["server_side_encryption"])
            check_type(argname="argument splunk_configuration", value=splunk_configuration, expected_type=type_hints["splunk_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if arn is not None:
            self._values["arn"] = arn
        if destination_id is not None:
            self._values["destination_id"] = destination_id
        if elasticsearch_configuration is not None:
            self._values["elasticsearch_configuration"] = elasticsearch_configuration
        if extended_s3_configuration is not None:
            self._values["extended_s3_configuration"] = extended_s3_configuration
        if http_endpoint_configuration is not None:
            self._values["http_endpoint_configuration"] = http_endpoint_configuration
        if id is not None:
            self._values["id"] = id
        if kinesis_source_configuration is not None:
            self._values["kinesis_source_configuration"] = kinesis_source_configuration
        if redshift_configuration is not None:
            self._values["redshift_configuration"] = redshift_configuration
        if s3_configuration is not None:
            self._values["s3_configuration"] = s3_configuration
        if server_side_encryption is not None:
            self._values["server_side_encryption"] = server_side_encryption
        if splunk_configuration is not None:
            self._values["splunk_configuration"] = splunk_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#destination KinesisFirehoseDeliveryStream#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#name KinesisFirehoseDeliveryStream#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#arn KinesisFirehoseDeliveryStream#arn}.'''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#destination_id KinesisFirehoseDeliveryStream#destination_id}.'''
        result = self._values.get("destination_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfiguration"]:
        '''elasticsearch_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#elasticsearch_configuration KinesisFirehoseDeliveryStream#elasticsearch_configuration}
        '''
        result = self._values.get("elasticsearch_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfiguration"], result)

    @builtins.property
    def extended_s3_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3Configuration"]:
        '''extended_s3_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#extended_s3_configuration KinesisFirehoseDeliveryStream#extended_s3_configuration}
        '''
        result = self._values.get("extended_s3_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3Configuration"], result)

    @builtins.property
    def http_endpoint_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfiguration"]:
        '''http_endpoint_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#http_endpoint_configuration KinesisFirehoseDeliveryStream#http_endpoint_configuration}
        '''
        result = self._values.get("http_endpoint_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#id KinesisFirehoseDeliveryStream#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesis_source_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamKinesisSourceConfiguration"]:
        '''kinesis_source_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kinesis_source_configuration KinesisFirehoseDeliveryStream#kinesis_source_configuration}
        '''
        result = self._values.get("kinesis_source_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamKinesisSourceConfiguration"], result)

    @builtins.property
    def redshift_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfiguration"]:
        '''redshift_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#redshift_configuration KinesisFirehoseDeliveryStream#redshift_configuration}
        '''
        result = self._values.get("redshift_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfiguration"], result)

    @builtins.property
    def s3_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamS3Configuration"]:
        '''s3_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_configuration KinesisFirehoseDeliveryStream#s3_configuration}
        '''
        result = self._values.get("s3_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamS3Configuration"], result)

    @builtins.property
    def server_side_encryption(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamServerSideEncryption"]:
        '''server_side_encryption block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#server_side_encryption KinesisFirehoseDeliveryStream#server_side_encryption}
        '''
        result = self._values.get("server_side_encryption")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamServerSideEncryption"], result)

    @builtins.property
    def splunk_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamSplunkConfiguration"]:
        '''splunk_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#splunk_configuration KinesisFirehoseDeliveryStream#splunk_configuration}
        '''
        result = self._values.get("splunk_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamSplunkConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#tags KinesisFirehoseDeliveryStream#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#tags_all KinesisFirehoseDeliveryStream#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#version_id KinesisFirehoseDeliveryStream#version_id}.'''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "index_name": "indexName",
        "role_arn": "roleArn",
        "buffering_interval": "bufferingInterval",
        "buffering_size": "bufferingSize",
        "cloudwatch_logging_options": "cloudwatchLoggingOptions",
        "cluster_endpoint": "clusterEndpoint",
        "domain_arn": "domainArn",
        "index_rotation_period": "indexRotationPeriod",
        "processing_configuration": "processingConfiguration",
        "retry_duration": "retryDuration",
        "s3_backup_mode": "s3BackupMode",
        "type_name": "typeName",
        "vpc_config": "vpcConfig",
    },
)
class KinesisFirehoseDeliveryStreamElasticsearchConfiguration:
    def __init__(
        self,
        *,
        index_name: builtins.str,
        role_arn: builtins.str,
        buffering_interval: typing.Optional[jsii.Number] = None,
        buffering_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_endpoint: typing.Optional[builtins.str] = None,
        domain_arn: typing.Optional[builtins.str] = None,
        index_rotation_period: typing.Optional[builtins.str] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_duration: typing.Optional[jsii.Number] = None,
        s3_backup_mode: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param index_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#index_name KinesisFirehoseDeliveryStream#index_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param buffering_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_interval KinesisFirehoseDeliveryStream#buffering_interval}.
        :param buffering_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_size KinesisFirehoseDeliveryStream#buffering_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param cluster_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cluster_endpoint KinesisFirehoseDeliveryStream#cluster_endpoint}.
        :param domain_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#domain_arn KinesisFirehoseDeliveryStream#domain_arn}.
        :param index_rotation_period: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#index_rotation_period KinesisFirehoseDeliveryStream#index_rotation_period}.
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        :param retry_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.
        :param s3_backup_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.
        :param type_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type_name KinesisFirehoseDeliveryStream#type_name}.
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#vpc_config KinesisFirehoseDeliveryStream#vpc_config}
        '''
        if isinstance(cloudwatch_logging_options, dict):
            cloudwatch_logging_options = KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions(**cloudwatch_logging_options)
        if isinstance(processing_configuration, dict):
            processing_configuration = KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration(**processing_configuration)
        if isinstance(vpc_config, dict):
            vpc_config = KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig(**vpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e5d53e8a1149b73bb7a34aca6da0238e3887c8eaa251fca73adc908b6f9209)
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument buffering_interval", value=buffering_interval, expected_type=type_hints["buffering_interval"])
            check_type(argname="argument buffering_size", value=buffering_size, expected_type=type_hints["buffering_size"])
            check_type(argname="argument cloudwatch_logging_options", value=cloudwatch_logging_options, expected_type=type_hints["cloudwatch_logging_options"])
            check_type(argname="argument cluster_endpoint", value=cluster_endpoint, expected_type=type_hints["cluster_endpoint"])
            check_type(argname="argument domain_arn", value=domain_arn, expected_type=type_hints["domain_arn"])
            check_type(argname="argument index_rotation_period", value=index_rotation_period, expected_type=type_hints["index_rotation_period"])
            check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
            check_type(argname="argument retry_duration", value=retry_duration, expected_type=type_hints["retry_duration"])
            check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index_name": index_name,
            "role_arn": role_arn,
        }
        if buffering_interval is not None:
            self._values["buffering_interval"] = buffering_interval
        if buffering_size is not None:
            self._values["buffering_size"] = buffering_size
        if cloudwatch_logging_options is not None:
            self._values["cloudwatch_logging_options"] = cloudwatch_logging_options
        if cluster_endpoint is not None:
            self._values["cluster_endpoint"] = cluster_endpoint
        if domain_arn is not None:
            self._values["domain_arn"] = domain_arn
        if index_rotation_period is not None:
            self._values["index_rotation_period"] = index_rotation_period
        if processing_configuration is not None:
            self._values["processing_configuration"] = processing_configuration
        if retry_duration is not None:
            self._values["retry_duration"] = retry_duration
        if s3_backup_mode is not None:
            self._values["s3_backup_mode"] = s3_backup_mode
        if type_name is not None:
            self._values["type_name"] = type_name
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def index_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#index_name KinesisFirehoseDeliveryStream#index_name}.'''
        result = self._values.get("index_name")
        assert result is not None, "Required property 'index_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def buffering_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_interval KinesisFirehoseDeliveryStream#buffering_interval}.'''
        result = self._values.get("buffering_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def buffering_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_size KinesisFirehoseDeliveryStream#buffering_size}.'''
        result = self._values.get("buffering_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cloudwatch_logging_options(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions"]:
        '''cloudwatch_logging_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        '''
        result = self._values.get("cloudwatch_logging_options")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions"], result)

    @builtins.property
    def cluster_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cluster_endpoint KinesisFirehoseDeliveryStream#cluster_endpoint}.'''
        result = self._values.get("cluster_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#domain_arn KinesisFirehoseDeliveryStream#domain_arn}.'''
        result = self._values.get("domain_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_rotation_period(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#index_rotation_period KinesisFirehoseDeliveryStream#index_rotation_period}.'''
        result = self._values.get("index_rotation_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processing_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration"]:
        '''processing_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        '''
        result = self._values.get("processing_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration"], result)

    @builtins.property
    def retry_duration(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.'''
        result = self._values.get("retry_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def s3_backup_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.'''
        result = self._values.get("s3_backup_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type_name KinesisFirehoseDeliveryStream#type_name}.'''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig"]:
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#vpc_config KinesisFirehoseDeliveryStream#vpc_config}
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamElasticsearchConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92db2547d24288a6d32b4839d0d6b1f758cf47e8a1271ef7ebd1d76ceba10adb)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b8a714a86b5890e0f374d1eb78db073ce3368b1bf98adac13e43ad08b7f3ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba4e5ba4f13096ea96d1c7a1e9b7f296093eeb08538a7ad49aec743f664ec30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3de549d64d55857ef4958058b3f2105ab4228a1eb3f6cf273435365f8e10b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__724d208f17efa6ec8fb38c89dd13a3f38af5998df3a2594abafa69570afdbd17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22605ad780fbc318dc0a0782e97e0f143ca2e79dbf38dd620f160a921f8f61bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamElasticsearchConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61aea174db8e641acbc05de63eae211f433ab788e2fdb73bb43e25612ca759fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLoggingOptions")
    def put_cloudwatch_logging_options(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        value = KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions(
            enabled=enabled,
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingOptions", [value]))

    @jsii.member(jsii_name="putProcessingConfiguration")
    def put_processing_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param processors: processors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        value = KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration(
            enabled=enabled, processors=processors
        )

        return typing.cast(None, jsii.invoke(self, "putProcessingConfiguration", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        role_arn: builtins.str,
        security_group_ids: typing.Sequence[builtins.str],
        subnet_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#security_group_ids KinesisFirehoseDeliveryStream#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#subnet_ids KinesisFirehoseDeliveryStream#subnet_ids}.
        '''
        value = KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig(
            role_arn=role_arn,
            security_group_ids=security_group_ids,
            subnet_ids=subnet_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @jsii.member(jsii_name="resetBufferingInterval")
    def reset_buffering_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferingInterval", []))

    @jsii.member(jsii_name="resetBufferingSize")
    def reset_buffering_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferingSize", []))

    @jsii.member(jsii_name="resetCloudwatchLoggingOptions")
    def reset_cloudwatch_logging_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingOptions", []))

    @jsii.member(jsii_name="resetClusterEndpoint")
    def reset_cluster_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterEndpoint", []))

    @jsii.member(jsii_name="resetDomainArn")
    def reset_domain_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainArn", []))

    @jsii.member(jsii_name="resetIndexRotationPeriod")
    def reset_index_rotation_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexRotationPeriod", []))

    @jsii.member(jsii_name="resetProcessingConfiguration")
    def reset_processing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessingConfiguration", []))

    @jsii.member(jsii_name="resetRetryDuration")
    def reset_retry_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryDuration", []))

    @jsii.member(jsii_name="resetS3BackupMode")
    def reset_s3_backup_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BackupMode", []))

    @jsii.member(jsii_name="resetTypeName")
    def reset_type_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTypeName", []))

    @jsii.member(jsii_name="resetVpcConfig")
    def reset_vpc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConfig", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptions")
    def cloudwatch_logging_options(
        self,
    ) -> KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptionsOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptionsOutputReference, jsii.get(self, "cloudwatchLoggingOptions"))

    @builtins.property
    @jsii.member(jsii_name="processingConfiguration")
    def processing_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationOutputReference", jsii.get(self, "processingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> "KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfigOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="bufferingIntervalInput")
    def buffering_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferingSizeInput")
    def buffering_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferingSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptionsInput")
    def cloudwatch_logging_options_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions], jsii.get(self, "cloudwatchLoggingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterEndpointInput")
    def cluster_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="domainArnInput")
    def domain_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainArnInput"))

    @builtins.property
    @jsii.member(jsii_name="indexNameInput")
    def index_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexNameInput"))

    @builtins.property
    @jsii.member(jsii_name="indexRotationPeriodInput")
    def index_rotation_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexRotationPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="processingConfigurationInput")
    def processing_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration"], jsii.get(self, "processingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="retryDurationInput")
    def retry_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BackupModeInput")
    def s3_backup_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BackupModeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeNameInput")
    def type_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferingInterval")
    def buffering_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferingInterval"))

    @buffering_interval.setter
    def buffering_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f14c044f69d1e9dc442a2e9a181f4bbadd2ec9b558068239a2e6dbd7d01e2470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferingInterval", value)

    @builtins.property
    @jsii.member(jsii_name="bufferingSize")
    def buffering_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferingSize"))

    @buffering_size.setter
    def buffering_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1f7e124358e8a67004b002cb48709357152af52b60805c531d9099ab005fe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferingSize", value)

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterEndpoint"))

    @cluster_endpoint.setter
    def cluster_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8079e97677b173a3a88baf0b06436465233da029c31b7abb96d9d2d7aeedfd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @domain_arn.setter
    def domain_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f12aec65273f448c1a226ce576688528532ccd82b10d1ce2922950b1442293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainArn", value)

    @builtins.property
    @jsii.member(jsii_name="indexName")
    def index_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexName"))

    @index_name.setter
    def index_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba30ee5c9434dc5e0e50187484726f791326ed1df9704efba18ff23d81d058b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexName", value)

    @builtins.property
    @jsii.member(jsii_name="indexRotationPeriod")
    def index_rotation_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexRotationPeriod"))

    @index_rotation_period.setter
    def index_rotation_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe69bf6522a410c1486ae61ec710b45b97c7b71ab5a8d343f8b5dbc0e60e966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexRotationPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="retryDuration")
    def retry_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryDuration"))

    @retry_duration.setter
    def retry_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c02fd5b69c2b931c61e0ad4a279834ac0b7e68e5fd9035f41aa4aed94a6d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryDuration", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f435c7a89f5c0e878715eb0c72021e1bf668ecd37f8dea2fb766dfe02e5f733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="s3BackupMode")
    def s3_backup_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BackupMode"))

    @s3_backup_mode.setter
    def s3_backup_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bed0718d25dfa64cd15b696f55124b6f871b2b6e00084918637413b03a3491e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BackupMode", value)

    @builtins.property
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb8041f2ec1171d53b082cdde68f386f5ced9cfe84a77cde479f95e75ce7a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77165ef48a7bfbe87955e6830bd18106558b93667bc17e6c8f0042dbb6e8af93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "processors": "processors"},
)
class KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param processors: processors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1241c5658ea34c71d3427d1b7ae79ed9b508be04fbb962f9ff584d6a743fe4d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if processors is not None:
            self._values["processors"] = processors

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def processors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors"]]]:
        '''processors block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        result = self._values.get("processors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ebab5707568e759898a8bb1e55fda49e01d456f6736f257b949dbc4f4c813f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProcessors")
    def put_processors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b78428d8d8b1e9d8750afb1939543da1e684d5a33840e27948ef5c772003054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProcessors", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetProcessors")
    def reset_processors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessors", []))

    @builtins.property
    @jsii.member(jsii_name="processors")
    def processors(
        self,
    ) -> "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsList":
        return typing.cast("KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsList", jsii.get(self, "processors"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="processorsInput")
    def processors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors"]]], jsii.get(self, "processorsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e546fd6c8c628fcbfee57db64c67514bf29f1519a123dd6b5e108672d5abeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8148cad95c2366f996e44649a558665857a4bd671a92f65e24a4fe19961cb7d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "parameters": "parameters"},
)
class KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors:
    def __init__(
        self,
        *,
        type: builtins.str,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type KinesisFirehoseDeliveryStream#type}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameters KinesisFirehoseDeliveryStream#parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7186160cd0f4a6c9c1dd7c43efc8b00325374090a9699e123ae681f78961cac4)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type KinesisFirehoseDeliveryStream#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters"]]]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameters KinesisFirehoseDeliveryStream#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc17e36ecf726ddf369197ee51e7a30815c15f792cc376cf7707f3614632dc4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c3d68194d8bf42c3df9202cfee8a01aa15e5b8a4850e5cd2a7d340300c95e1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1470366b8ff694b279004ec04278b6815d94161fd7bd8c8b3b1234a9de01a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2e226002c072b38dc451cae7db645611801ea0f4c630219578d1dcc49c79b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216cf9b4c19da6a814fe821fdc0426ffd0cf85ad2f0f6db61a9106b5462168a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d663a4e82d49d1e15809515411298ffb3ad61d27acd7e4bea7cd7bbef3dc6b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29e12971f0d0eedf256272fb78b303ab1c269698df1ad3b22a4edaa5ed11d15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667169714862c29405734cd038125bad5c8eddfecf78e1b33e6fc95b5ee45bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParametersList":
        return typing.cast("KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters"]]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056b0a2b9f32bea629a1fab4c660da0c4839952995a2b39eae06438fcc99cda9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc3778e2d4830e0e7cc7562f24c9eb7abd8b40c3d8285f058a6ec64924e08ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_name": "parameterName",
        "parameter_value": "parameterValue",
    },
)
class KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters:
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        parameter_value: builtins.str,
    ) -> None:
        '''
        :param parameter_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_name KinesisFirehoseDeliveryStream#parameter_name}.
        :param parameter_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_value KinesisFirehoseDeliveryStream#parameter_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93218b79ba7709f0bc6ed837e92664eb73771a377c51fecea900f076b0f7edd9)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter_name": parameter_name,
            "parameter_value": parameter_value,
        }

    @builtins.property
    def parameter_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_name KinesisFirehoseDeliveryStream#parameter_name}.'''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_value KinesisFirehoseDeliveryStream#parameter_value}.'''
        result = self._values.get("parameter_value")
        assert result is not None, "Required property 'parameter_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParametersList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4180938c12da8256caa1cafa2fc90fce22286f2afd1e2796a7f3540b044f46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176fb4cbf6371d1227ae89079d6226a254a93fb905e23004a41c38aba45c8ac1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f81c3ce228a7a233f784677ff3681b439fb26e9daff9b2d5a9814aed739e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b470ed7577e2f5834e9be96567bf5d97712a27fb101955f932788a8108b3886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa7755d85033be6c7504c46b4c6827905cae9df8b28c5f4e1c85a254f9ab791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f636568e769afa069ef7ceaaa0ac4fea5611692db07feb131ca9d8e5c839cd32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParametersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff04729ea1eec1227c5bec9a2bddb688456c761e0b0d4780283207afc9ab4d7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="parameterNameInput")
    def parameter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterValueInput")
    def parameter_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterValueInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterName"))

    @parameter_name.setter
    def parameter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7728c836614e4dc40f05c62fecaf736328f4e4394ea55fb1ccaeb9221d6430eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterName", value)

    @builtins.property
    @jsii.member(jsii_name="parameterValue")
    def parameter_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterValue"))

    @parameter_value.setter
    def parameter_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e36426e81d9e9b78f83497e60bc4b6016d3b615ab85394a630ff43f7d2693e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98daf71b65dc12bb66354cbb583f3557d5907f7ee87be80fa91144bea86a6d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
    },
)
class KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        security_group_ids: typing.Sequence[builtins.str],
        subnet_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#security_group_ids KinesisFirehoseDeliveryStream#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#subnet_ids KinesisFirehoseDeliveryStream#subnet_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f477819807f784be4a9fffd7d6dc2cee4d167e93fdf988c3743b3c46e10dafd3)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "security_group_ids": security_group_ids,
            "subnet_ids": subnet_ids,
        }

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#security_group_ids KinesisFirehoseDeliveryStream#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#subnet_ids KinesisFirehoseDeliveryStream#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3ece1ac4097116d3b7ed335d3e08657fcd34b5c6e7a2b85cf65dddab6beebb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67946a5efc7190039c1c45b19c5ea69cc3e67a2a4cdaaf432fce923d1e9fccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d07d1ad2a5c43eabfe1c875573ae6195b535590dd2304d0d9a689e579ba533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb293b55bb7692c95cb9a0e536fd2c4e150fbacb70e4742a916317497fb7e50c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e741ed0ab60fba0e5f1b6357e37e75d3310bc2cb797441ce2231488ec36c9631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3Configuration",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "role_arn": "roleArn",
        "buffer_interval": "bufferInterval",
        "buffer_size": "bufferSize",
        "cloudwatch_logging_options": "cloudwatchLoggingOptions",
        "compression_format": "compressionFormat",
        "data_format_conversion_configuration": "dataFormatConversionConfiguration",
        "dynamic_partitioning_configuration": "dynamicPartitioningConfiguration",
        "error_output_prefix": "errorOutputPrefix",
        "kms_key_arn": "kmsKeyArn",
        "prefix": "prefix",
        "processing_configuration": "processingConfiguration",
        "s3_backup_configuration": "s3BackupConfiguration",
        "s3_backup_mode": "s3BackupMode",
    },
)
class KinesisFirehoseDeliveryStreamExtendedS3Configuration:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        role_arn: builtins.str,
        buffer_interval: typing.Optional[jsii.Number] = None,
        buffer_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_format: typing.Optional[builtins.str] = None,
        data_format_conversion_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamic_partitioning_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_backup_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_backup_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param buffer_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.
        :param buffer_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param compression_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.
        :param data_format_conversion_configuration: data_format_conversion_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#data_format_conversion_configuration KinesisFirehoseDeliveryStream#data_format_conversion_configuration}
        :param dynamic_partitioning_configuration: dynamic_partitioning_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#dynamic_partitioning_configuration KinesisFirehoseDeliveryStream#dynamic_partitioning_configuration}
        :param error_output_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        :param s3_backup_configuration: s3_backup_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_configuration KinesisFirehoseDeliveryStream#s3_backup_configuration}
        :param s3_backup_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.
        '''
        if isinstance(cloudwatch_logging_options, dict):
            cloudwatch_logging_options = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions(**cloudwatch_logging_options)
        if isinstance(data_format_conversion_configuration, dict):
            data_format_conversion_configuration = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration(**data_format_conversion_configuration)
        if isinstance(dynamic_partitioning_configuration, dict):
            dynamic_partitioning_configuration = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration(**dynamic_partitioning_configuration)
        if isinstance(processing_configuration, dict):
            processing_configuration = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration(**processing_configuration)
        if isinstance(s3_backup_configuration, dict):
            s3_backup_configuration = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration(**s3_backup_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd60f5bd69639f798ea3f5de680d6d0dbbd78a67566b2b6a093864b8214e70b)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument buffer_interval", value=buffer_interval, expected_type=type_hints["buffer_interval"])
            check_type(argname="argument buffer_size", value=buffer_size, expected_type=type_hints["buffer_size"])
            check_type(argname="argument cloudwatch_logging_options", value=cloudwatch_logging_options, expected_type=type_hints["cloudwatch_logging_options"])
            check_type(argname="argument compression_format", value=compression_format, expected_type=type_hints["compression_format"])
            check_type(argname="argument data_format_conversion_configuration", value=data_format_conversion_configuration, expected_type=type_hints["data_format_conversion_configuration"])
            check_type(argname="argument dynamic_partitioning_configuration", value=dynamic_partitioning_configuration, expected_type=type_hints["dynamic_partitioning_configuration"])
            check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
            check_type(argname="argument s3_backup_configuration", value=s3_backup_configuration, expected_type=type_hints["s3_backup_configuration"])
            check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "role_arn": role_arn,
        }
        if buffer_interval is not None:
            self._values["buffer_interval"] = buffer_interval
        if buffer_size is not None:
            self._values["buffer_size"] = buffer_size
        if cloudwatch_logging_options is not None:
            self._values["cloudwatch_logging_options"] = cloudwatch_logging_options
        if compression_format is not None:
            self._values["compression_format"] = compression_format
        if data_format_conversion_configuration is not None:
            self._values["data_format_conversion_configuration"] = data_format_conversion_configuration
        if dynamic_partitioning_configuration is not None:
            self._values["dynamic_partitioning_configuration"] = dynamic_partitioning_configuration
        if error_output_prefix is not None:
            self._values["error_output_prefix"] = error_output_prefix
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if prefix is not None:
            self._values["prefix"] = prefix
        if processing_configuration is not None:
            self._values["processing_configuration"] = processing_configuration
        if s3_backup_configuration is not None:
            self._values["s3_backup_configuration"] = s3_backup_configuration
        if s3_backup_mode is not None:
            self._values["s3_backup_mode"] = s3_backup_mode

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def buffer_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.'''
        result = self._values.get("buffer_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def buffer_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.'''
        result = self._values.get("buffer_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cloudwatch_logging_options(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions"]:
        '''cloudwatch_logging_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        '''
        result = self._values.get("cloudwatch_logging_options")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions"], result)

    @builtins.property
    def compression_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.'''
        result = self._values.get("compression_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_format_conversion_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration"]:
        '''data_format_conversion_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#data_format_conversion_configuration KinesisFirehoseDeliveryStream#data_format_conversion_configuration}
        '''
        result = self._values.get("data_format_conversion_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration"], result)

    @builtins.property
    def dynamic_partitioning_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration"]:
        '''dynamic_partitioning_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#dynamic_partitioning_configuration KinesisFirehoseDeliveryStream#dynamic_partitioning_configuration}
        '''
        result = self._values.get("dynamic_partitioning_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration"], result)

    @builtins.property
    def error_output_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.'''
        result = self._values.get("error_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processing_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration"]:
        '''processing_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        '''
        result = self._values.get("processing_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration"], result)

    @builtins.property
    def s3_backup_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration"]:
        '''s3_backup_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_configuration KinesisFirehoseDeliveryStream#s3_backup_configuration}
        '''
        result = self._values.get("s3_backup_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration"], result)

    @builtins.property
    def s3_backup_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.'''
        result = self._values.get("s3_backup_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83c4356a3e6b6f2e1a3e79e43dcb6c292d8a4824512a9ed9b34ce067089e12b)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584e24e78e61847096b7a4f086fa293fabadd149c22b9f3d462dc3e567e5bc58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf866496d39160e71916811e708b3c392e7cf94831821104ddf75fc80e086ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909d07e7ef4d08866b4a4a740126a57898474e20f8ddc6544e62dcbffd939ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5783c290f4ddfbb376c8b879171b1f2d3c5f81aa276d7419f33fb6d173f1491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9d23a60c2ccc73f56db4749bd8af07e250df912d6687d396f2fa0ad972921f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "input_format_configuration": "inputFormatConfiguration",
        "output_format_configuration": "outputFormatConfiguration",
        "schema_configuration": "schemaConfiguration",
        "enabled": "enabled",
    },
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration:
    def __init__(
        self,
        *,
        input_format_configuration: typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration", typing.Dict[builtins.str, typing.Any]],
        output_format_configuration: typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration", typing.Dict[builtins.str, typing.Any]],
        schema_configuration: typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param input_format_configuration: input_format_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#input_format_configuration KinesisFirehoseDeliveryStream#input_format_configuration}
        :param output_format_configuration: output_format_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#output_format_configuration KinesisFirehoseDeliveryStream#output_format_configuration}
        :param schema_configuration: schema_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#schema_configuration KinesisFirehoseDeliveryStream#schema_configuration}
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        '''
        if isinstance(input_format_configuration, dict):
            input_format_configuration = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration(**input_format_configuration)
        if isinstance(output_format_configuration, dict):
            output_format_configuration = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration(**output_format_configuration)
        if isinstance(schema_configuration, dict):
            schema_configuration = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration(**schema_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9346dfa62558d71cc9a8972fba82fbd17f616dd9559620356bd5d16d922c0139)
            check_type(argname="argument input_format_configuration", value=input_format_configuration, expected_type=type_hints["input_format_configuration"])
            check_type(argname="argument output_format_configuration", value=output_format_configuration, expected_type=type_hints["output_format_configuration"])
            check_type(argname="argument schema_configuration", value=schema_configuration, expected_type=type_hints["schema_configuration"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_format_configuration": input_format_configuration,
            "output_format_configuration": output_format_configuration,
            "schema_configuration": schema_configuration,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def input_format_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration":
        '''input_format_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#input_format_configuration KinesisFirehoseDeliveryStream#input_format_configuration}
        '''
        result = self._values.get("input_format_configuration")
        assert result is not None, "Required property 'input_format_configuration' is missing"
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration", result)

    @builtins.property
    def output_format_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration":
        '''output_format_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#output_format_configuration KinesisFirehoseDeliveryStream#output_format_configuration}
        '''
        result = self._values.get("output_format_configuration")
        assert result is not None, "Required property 'output_format_configuration' is missing"
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration", result)

    @builtins.property
    def schema_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration":
        '''schema_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#schema_configuration KinesisFirehoseDeliveryStream#schema_configuration}
        '''
        result = self._values.get("schema_configuration")
        assert result is not None, "Required property 'schema_configuration' is missing"
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration", result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration",
    jsii_struct_bases=[],
    name_mapping={"deserializer": "deserializer"},
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration:
    def __init__(
        self,
        *,
        deserializer: typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param deserializer: deserializer block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#deserializer KinesisFirehoseDeliveryStream#deserializer}
        '''
        if isinstance(deserializer, dict):
            deserializer = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer(**deserializer)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9bc70c06378be3f4a4a3e4e825e18ee74e442aa54d8a981a10d07af3222c517)
            check_type(argname="argument deserializer", value=deserializer, expected_type=type_hints["deserializer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deserializer": deserializer,
        }

    @builtins.property
    def deserializer(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer":
        '''deserializer block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#deserializer KinesisFirehoseDeliveryStream#deserializer}
        '''
        result = self._values.get("deserializer")
        assert result is not None, "Required property 'deserializer' is missing"
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer",
    jsii_struct_bases=[],
    name_mapping={
        "hive_json_ser_de": "hiveJsonSerDe",
        "open_x_json_ser_de": "openXJsonSerDe",
    },
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer:
    def __init__(
        self,
        *,
        hive_json_ser_de: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe", typing.Dict[builtins.str, typing.Any]]] = None,
        open_x_json_ser_de: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hive_json_ser_de: hive_json_ser_de block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hive_json_ser_de KinesisFirehoseDeliveryStream#hive_json_ser_de}
        :param open_x_json_ser_de: open_x_json_ser_de block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#open_x_json_ser_de KinesisFirehoseDeliveryStream#open_x_json_ser_de}
        '''
        if isinstance(hive_json_ser_de, dict):
            hive_json_ser_de = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe(**hive_json_ser_de)
        if isinstance(open_x_json_ser_de, dict):
            open_x_json_ser_de = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe(**open_x_json_ser_de)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd1e6e519b6346e502fbc1274efebad18b1c8992e95cc95486c0003585030e8)
            check_type(argname="argument hive_json_ser_de", value=hive_json_ser_de, expected_type=type_hints["hive_json_ser_de"])
            check_type(argname="argument open_x_json_ser_de", value=open_x_json_ser_de, expected_type=type_hints["open_x_json_ser_de"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hive_json_ser_de is not None:
            self._values["hive_json_ser_de"] = hive_json_ser_de
        if open_x_json_ser_de is not None:
            self._values["open_x_json_ser_de"] = open_x_json_ser_de

    @builtins.property
    def hive_json_ser_de(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe"]:
        '''hive_json_ser_de block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hive_json_ser_de KinesisFirehoseDeliveryStream#hive_json_ser_de}
        '''
        result = self._values.get("hive_json_ser_de")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe"], result)

    @builtins.property
    def open_x_json_ser_de(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe"]:
        '''open_x_json_ser_de block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#open_x_json_ser_de KinesisFirehoseDeliveryStream#open_x_json_ser_de}
        '''
        result = self._values.get("open_x_json_ser_de")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe",
    jsii_struct_bases=[],
    name_mapping={"timestamp_formats": "timestampFormats"},
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe:
    def __init__(
        self,
        *,
        timestamp_formats: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param timestamp_formats: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#timestamp_formats KinesisFirehoseDeliveryStream#timestamp_formats}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507f87d821b887bfdf43014c4dc811be3c9ed264e98be3a0bdbec39757c74355)
            check_type(argname="argument timestamp_formats", value=timestamp_formats, expected_type=type_hints["timestamp_formats"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if timestamp_formats is not None:
            self._values["timestamp_formats"] = timestamp_formats

    @builtins.property
    def timestamp_formats(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#timestamp_formats KinesisFirehoseDeliveryStream#timestamp_formats}.'''
        result = self._values.get("timestamp_formats")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a0bcea16353cd0e5c184bb909105cd4ce5829a3b58aa9bc54b449c090c95bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTimestampFormats")
    def reset_timestamp_formats(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampFormats", []))

    @builtins.property
    @jsii.member(jsii_name="timestampFormatsInput")
    def timestamp_formats_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "timestampFormatsInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampFormats")
    def timestamp_formats(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "timestampFormats"))

    @timestamp_formats.setter
    def timestamp_formats(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6304d8063aa05cd9bb4add221c1d0c24630d126ec6cfded4fb1db21ea778a016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampFormats", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eef3f4ec76c83c8e4c501e4fd3050f83f09bf601926de8c25c93d8650a23329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe",
    jsii_struct_bases=[],
    name_mapping={
        "case_insensitive": "caseInsensitive",
        "column_to_json_key_mappings": "columnToJsonKeyMappings",
        "convert_dots_in_json_keys_to_underscores": "convertDotsInJsonKeysToUnderscores",
    },
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe:
    def __init__(
        self,
        *,
        case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        column_to_json_key_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        convert_dots_in_json_keys_to_underscores: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param case_insensitive: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#case_insensitive KinesisFirehoseDeliveryStream#case_insensitive}.
        :param column_to_json_key_mappings: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#column_to_json_key_mappings KinesisFirehoseDeliveryStream#column_to_json_key_mappings}.
        :param convert_dots_in_json_keys_to_underscores: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#convert_dots_in_json_keys_to_underscores KinesisFirehoseDeliveryStream#convert_dots_in_json_keys_to_underscores}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e16173b491e1224d965035d0a848cba1d69cde788777dba005acad3cc4e1dc82)
            check_type(argname="argument case_insensitive", value=case_insensitive, expected_type=type_hints["case_insensitive"])
            check_type(argname="argument column_to_json_key_mappings", value=column_to_json_key_mappings, expected_type=type_hints["column_to_json_key_mappings"])
            check_type(argname="argument convert_dots_in_json_keys_to_underscores", value=convert_dots_in_json_keys_to_underscores, expected_type=type_hints["convert_dots_in_json_keys_to_underscores"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if case_insensitive is not None:
            self._values["case_insensitive"] = case_insensitive
        if column_to_json_key_mappings is not None:
            self._values["column_to_json_key_mappings"] = column_to_json_key_mappings
        if convert_dots_in_json_keys_to_underscores is not None:
            self._values["convert_dots_in_json_keys_to_underscores"] = convert_dots_in_json_keys_to_underscores

    @builtins.property
    def case_insensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#case_insensitive KinesisFirehoseDeliveryStream#case_insensitive}.'''
        result = self._values.get("case_insensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def column_to_json_key_mappings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#column_to_json_key_mappings KinesisFirehoseDeliveryStream#column_to_json_key_mappings}.'''
        result = self._values.get("column_to_json_key_mappings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def convert_dots_in_json_keys_to_underscores(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#convert_dots_in_json_keys_to_underscores KinesisFirehoseDeliveryStream#convert_dots_in_json_keys_to_underscores}.'''
        result = self._values.get("convert_dots_in_json_keys_to_underscores")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e59c13b1f7dbdf9b8806a4260c27657ccfb71db9289d2ee5acff1bdada36094)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCaseInsensitive")
    def reset_case_insensitive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaseInsensitive", []))

    @jsii.member(jsii_name="resetColumnToJsonKeyMappings")
    def reset_column_to_json_key_mappings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnToJsonKeyMappings", []))

    @jsii.member(jsii_name="resetConvertDotsInJsonKeysToUnderscores")
    def reset_convert_dots_in_json_keys_to_underscores(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConvertDotsInJsonKeysToUnderscores", []))

    @builtins.property
    @jsii.member(jsii_name="caseInsensitiveInput")
    def case_insensitive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "caseInsensitiveInput"))

    @builtins.property
    @jsii.member(jsii_name="columnToJsonKeyMappingsInput")
    def column_to_json_key_mappings_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "columnToJsonKeyMappingsInput"))

    @builtins.property
    @jsii.member(jsii_name="convertDotsInJsonKeysToUnderscoresInput")
    def convert_dots_in_json_keys_to_underscores_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "convertDotsInJsonKeysToUnderscoresInput"))

    @builtins.property
    @jsii.member(jsii_name="caseInsensitive")
    def case_insensitive(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "caseInsensitive"))

    @case_insensitive.setter
    def case_insensitive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec7924d7a930bbe42158440877d1248bcdea01304ab6fbdfa1099a4c832c81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caseInsensitive", value)

    @builtins.property
    @jsii.member(jsii_name="columnToJsonKeyMappings")
    def column_to_json_key_mappings(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "columnToJsonKeyMappings"))

    @column_to_json_key_mappings.setter
    def column_to_json_key_mappings(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b01b7bf34c98617302466da1a8cbfcfb78330dde97350648b1bef4090ccbbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnToJsonKeyMappings", value)

    @builtins.property
    @jsii.member(jsii_name="convertDotsInJsonKeysToUnderscores")
    def convert_dots_in_json_keys_to_underscores(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "convertDotsInJsonKeysToUnderscores"))

    @convert_dots_in_json_keys_to_underscores.setter
    def convert_dots_in_json_keys_to_underscores(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c0b10edced7e817a393048961d2f7dcd0a27d1fa6f95524e21785e9338b0f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "convertDotsInJsonKeysToUnderscores", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2593b5e95d9698af27f03fa0761645767d08876a661eeeca0e678b69873b5003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87a13ea702dc1cbf054430e11bcb2ebc7ba6688cf17ba99f8c00c4543cef6e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHiveJsonSerDe")
    def put_hive_json_ser_de(
        self,
        *,
        timestamp_formats: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param timestamp_formats: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#timestamp_formats KinesisFirehoseDeliveryStream#timestamp_formats}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe(
            timestamp_formats=timestamp_formats
        )

        return typing.cast(None, jsii.invoke(self, "putHiveJsonSerDe", [value]))

    @jsii.member(jsii_name="putOpenXJsonSerDe")
    def put_open_x_json_ser_de(
        self,
        *,
        case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        column_to_json_key_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        convert_dots_in_json_keys_to_underscores: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param case_insensitive: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#case_insensitive KinesisFirehoseDeliveryStream#case_insensitive}.
        :param column_to_json_key_mappings: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#column_to_json_key_mappings KinesisFirehoseDeliveryStream#column_to_json_key_mappings}.
        :param convert_dots_in_json_keys_to_underscores: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#convert_dots_in_json_keys_to_underscores KinesisFirehoseDeliveryStream#convert_dots_in_json_keys_to_underscores}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe(
            case_insensitive=case_insensitive,
            column_to_json_key_mappings=column_to_json_key_mappings,
            convert_dots_in_json_keys_to_underscores=convert_dots_in_json_keys_to_underscores,
        )

        return typing.cast(None, jsii.invoke(self, "putOpenXJsonSerDe", [value]))

    @jsii.member(jsii_name="resetHiveJsonSerDe")
    def reset_hive_json_ser_de(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHiveJsonSerDe", []))

    @jsii.member(jsii_name="resetOpenXJsonSerDe")
    def reset_open_x_json_ser_de(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenXJsonSerDe", []))

    @builtins.property
    @jsii.member(jsii_name="hiveJsonSerDe")
    def hive_json_ser_de(
        self,
    ) -> KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDeOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDeOutputReference, jsii.get(self, "hiveJsonSerDe"))

    @builtins.property
    @jsii.member(jsii_name="openXJsonSerDe")
    def open_x_json_ser_de(
        self,
    ) -> KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDeOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDeOutputReference, jsii.get(self, "openXJsonSerDe"))

    @builtins.property
    @jsii.member(jsii_name="hiveJsonSerDeInput")
    def hive_json_ser_de_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe], jsii.get(self, "hiveJsonSerDeInput"))

    @builtins.property
    @jsii.member(jsii_name="openXJsonSerDeInput")
    def open_x_json_ser_de_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe], jsii.get(self, "openXJsonSerDeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cf8b3946390f3bc6696146c05e5ad16bf9acbab38810247347af30a9a35304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fd0d204e2d8a3debc899bca6fffe96bb01a3908cea155bf4ed0d517ac7420b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeserializer")
    def put_deserializer(
        self,
        *,
        hive_json_ser_de: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe, typing.Dict[builtins.str, typing.Any]]] = None,
        open_x_json_ser_de: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hive_json_ser_de: hive_json_ser_de block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hive_json_ser_de KinesisFirehoseDeliveryStream#hive_json_ser_de}
        :param open_x_json_ser_de: open_x_json_ser_de block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#open_x_json_ser_de KinesisFirehoseDeliveryStream#open_x_json_ser_de}
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer(
            hive_json_ser_de=hive_json_ser_de, open_x_json_ser_de=open_x_json_ser_de
        )

        return typing.cast(None, jsii.invoke(self, "putDeserializer", [value]))

    @builtins.property
    @jsii.member(jsii_name="deserializer")
    def deserializer(
        self,
    ) -> KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOutputReference, jsii.get(self, "deserializer"))

    @builtins.property
    @jsii.member(jsii_name="deserializerInput")
    def deserializer_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer], jsii.get(self, "deserializerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b583a36167500b179a5a671dc13fe957071224a9af134ef77bf0ca7d03ee0a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration",
    jsii_struct_bases=[],
    name_mapping={"serializer": "serializer"},
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration:
    def __init__(
        self,
        *,
        serializer: typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param serializer: serializer block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#serializer KinesisFirehoseDeliveryStream#serializer}
        '''
        if isinstance(serializer, dict):
            serializer = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer(**serializer)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6a81e5aa30d50073775fa0844816fdeb6943f21ce859ea5a5edd190bc141c6)
            check_type(argname="argument serializer", value=serializer, expected_type=type_hints["serializer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "serializer": serializer,
        }

    @builtins.property
    def serializer(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer":
        '''serializer block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#serializer KinesisFirehoseDeliveryStream#serializer}
        '''
        result = self._values.get("serializer")
        assert result is not None, "Required property 'serializer' is missing"
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09b0c726e2b08b00a81239edabb6f19ff47826dacc4495614bbb579b2dbc315)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSerializer")
    def put_serializer(
        self,
        *,
        orc_ser_de: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe", typing.Dict[builtins.str, typing.Any]]] = None,
        parquet_ser_de: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param orc_ser_de: orc_ser_de block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#orc_ser_de KinesisFirehoseDeliveryStream#orc_ser_de}
        :param parquet_ser_de: parquet_ser_de block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parquet_ser_de KinesisFirehoseDeliveryStream#parquet_ser_de}
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer(
            orc_ser_de=orc_ser_de, parquet_ser_de=parquet_ser_de
        )

        return typing.cast(None, jsii.invoke(self, "putSerializer", [value]))

    @builtins.property
    @jsii.member(jsii_name="serializer")
    def serializer(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOutputReference", jsii.get(self, "serializer"))

    @builtins.property
    @jsii.member(jsii_name="serializerInput")
    def serializer_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer"], jsii.get(self, "serializerInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7f885407ff3209ec1989f2463f3ab99de650f420cecf2fcf134d81854552f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer",
    jsii_struct_bases=[],
    name_mapping={"orc_ser_de": "orcSerDe", "parquet_ser_de": "parquetSerDe"},
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer:
    def __init__(
        self,
        *,
        orc_ser_de: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe", typing.Dict[builtins.str, typing.Any]]] = None,
        parquet_ser_de: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param orc_ser_de: orc_ser_de block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#orc_ser_de KinesisFirehoseDeliveryStream#orc_ser_de}
        :param parquet_ser_de: parquet_ser_de block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parquet_ser_de KinesisFirehoseDeliveryStream#parquet_ser_de}
        '''
        if isinstance(orc_ser_de, dict):
            orc_ser_de = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe(**orc_ser_de)
        if isinstance(parquet_ser_de, dict):
            parquet_ser_de = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe(**parquet_ser_de)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9956e42b9af6dc8654cd64510177b0c6923e02b8e7ea15815017c0b4a6cd6a36)
            check_type(argname="argument orc_ser_de", value=orc_ser_de, expected_type=type_hints["orc_ser_de"])
            check_type(argname="argument parquet_ser_de", value=parquet_ser_de, expected_type=type_hints["parquet_ser_de"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if orc_ser_de is not None:
            self._values["orc_ser_de"] = orc_ser_de
        if parquet_ser_de is not None:
            self._values["parquet_ser_de"] = parquet_ser_de

    @builtins.property
    def orc_ser_de(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe"]:
        '''orc_ser_de block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#orc_ser_de KinesisFirehoseDeliveryStream#orc_ser_de}
        '''
        result = self._values.get("orc_ser_de")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe"], result)

    @builtins.property
    def parquet_ser_de(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe"]:
        '''parquet_ser_de block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parquet_ser_de KinesisFirehoseDeliveryStream#parquet_ser_de}
        '''
        result = self._values.get("parquet_ser_de")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe",
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
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe:
    def __init__(
        self,
        *,
        block_size_bytes: typing.Optional[jsii.Number] = None,
        bloom_filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        bloom_filter_false_positive_probability: typing.Optional[jsii.Number] = None,
        compression: typing.Optional[builtins.str] = None,
        dictionary_key_threshold: typing.Optional[jsii.Number] = None,
        enable_padding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        format_version: typing.Optional[builtins.str] = None,
        padding_tolerance: typing.Optional[jsii.Number] = None,
        row_index_stride: typing.Optional[jsii.Number] = None,
        stripe_size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param block_size_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#block_size_bytes KinesisFirehoseDeliveryStream#block_size_bytes}.
        :param bloom_filter_columns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bloom_filter_columns KinesisFirehoseDeliveryStream#bloom_filter_columns}.
        :param bloom_filter_false_positive_probability: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bloom_filter_false_positive_probability KinesisFirehoseDeliveryStream#bloom_filter_false_positive_probability}.
        :param compression: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression KinesisFirehoseDeliveryStream#compression}.
        :param dictionary_key_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#dictionary_key_threshold KinesisFirehoseDeliveryStream#dictionary_key_threshold}.
        :param enable_padding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enable_padding KinesisFirehoseDeliveryStream#enable_padding}.
        :param format_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#format_version KinesisFirehoseDeliveryStream#format_version}.
        :param padding_tolerance: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#padding_tolerance KinesisFirehoseDeliveryStream#padding_tolerance}.
        :param row_index_stride: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#row_index_stride KinesisFirehoseDeliveryStream#row_index_stride}.
        :param stripe_size_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#stripe_size_bytes KinesisFirehoseDeliveryStream#stripe_size_bytes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2a47207e3385fb05844df5af0d99c7bb5ec91ecb9e448d4ddc93b11860974a)
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
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#block_size_bytes KinesisFirehoseDeliveryStream#block_size_bytes}.'''
        result = self._values.get("block_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bloom_filter_columns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bloom_filter_columns KinesisFirehoseDeliveryStream#bloom_filter_columns}.'''
        result = self._values.get("bloom_filter_columns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def bloom_filter_false_positive_probability(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bloom_filter_false_positive_probability KinesisFirehoseDeliveryStream#bloom_filter_false_positive_probability}.'''
        result = self._values.get("bloom_filter_false_positive_probability")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression KinesisFirehoseDeliveryStream#compression}.'''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dictionary_key_threshold(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#dictionary_key_threshold KinesisFirehoseDeliveryStream#dictionary_key_threshold}.'''
        result = self._values.get("dictionary_key_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_padding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enable_padding KinesisFirehoseDeliveryStream#enable_padding}.'''
        result = self._values.get("enable_padding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def format_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#format_version KinesisFirehoseDeliveryStream#format_version}.'''
        result = self._values.get("format_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def padding_tolerance(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#padding_tolerance KinesisFirehoseDeliveryStream#padding_tolerance}.'''
        result = self._values.get("padding_tolerance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def row_index_stride(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#row_index_stride KinesisFirehoseDeliveryStream#row_index_stride}.'''
        result = self._values.get("row_index_stride")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stripe_size_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#stripe_size_bytes KinesisFirehoseDeliveryStream#stripe_size_bytes}.'''
        result = self._values.get("stripe_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cea19fecd537e2efa7d54cedaf8796e9ad54d08a342c39f78e8eb231ca5a2fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBlockSizeBytes")
    def reset_block_size_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockSizeBytes", []))

    @jsii.member(jsii_name="resetBloomFilterColumns")
    def reset_bloom_filter_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBloomFilterColumns", []))

    @jsii.member(jsii_name="resetBloomFilterFalsePositiveProbability")
    def reset_bloom_filter_false_positive_probability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBloomFilterFalsePositiveProbability", []))

    @jsii.member(jsii_name="resetCompression")
    def reset_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompression", []))

    @jsii.member(jsii_name="resetDictionaryKeyThreshold")
    def reset_dictionary_key_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDictionaryKeyThreshold", []))

    @jsii.member(jsii_name="resetEnablePadding")
    def reset_enable_padding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePadding", []))

    @jsii.member(jsii_name="resetFormatVersion")
    def reset_format_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFormatVersion", []))

    @jsii.member(jsii_name="resetPaddingTolerance")
    def reset_padding_tolerance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaddingTolerance", []))

    @jsii.member(jsii_name="resetRowIndexStride")
    def reset_row_index_stride(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowIndexStride", []))

    @jsii.member(jsii_name="resetStripeSizeBytes")
    def reset_stripe_size_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStripeSizeBytes", []))

    @builtins.property
    @jsii.member(jsii_name="blockSizeBytesInput")
    def block_size_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "blockSizeBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="bloomFilterColumnsInput")
    def bloom_filter_columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bloomFilterColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="bloomFilterFalsePositiveProbabilityInput")
    def bloom_filter_false_positive_probability_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bloomFilterFalsePositiveProbabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionInput")
    def compression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionInput"))

    @builtins.property
    @jsii.member(jsii_name="dictionaryKeyThresholdInput")
    def dictionary_key_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dictionaryKeyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePaddingInput")
    def enable_padding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePaddingInput"))

    @builtins.property
    @jsii.member(jsii_name="formatVersionInput")
    def format_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="paddingToleranceInput")
    def padding_tolerance_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "paddingToleranceInput"))

    @builtins.property
    @jsii.member(jsii_name="rowIndexStrideInput")
    def row_index_stride_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowIndexStrideInput"))

    @builtins.property
    @jsii.member(jsii_name="stripeSizeBytesInput")
    def stripe_size_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stripeSizeBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="blockSizeBytes")
    def block_size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "blockSizeBytes"))

    @block_size_bytes.setter
    def block_size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e8247c7957a06cc6108c7cd6daa033412b75d0ce5d68a127356b299fa4dc71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockSizeBytes", value)

    @builtins.property
    @jsii.member(jsii_name="bloomFilterColumns")
    def bloom_filter_columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "bloomFilterColumns"))

    @bloom_filter_columns.setter
    def bloom_filter_columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9ed8cd7d1ebf5935b6e8dd3ea98e45508b065b1cc56af8ad9ac5e097d5042c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bloomFilterColumns", value)

    @builtins.property
    @jsii.member(jsii_name="bloomFilterFalsePositiveProbability")
    def bloom_filter_false_positive_probability(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bloomFilterFalsePositiveProbability"))

    @bloom_filter_false_positive_probability.setter
    def bloom_filter_false_positive_probability(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee581abca9df89deaf6c461f4134c39332570ab3b483f29d6ce7a8ced3fcac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bloomFilterFalsePositiveProbability", value)

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60bde9509fcb7724c2c3bb47447cc182667437ee7e9d5251457be11ee290f951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value)

    @builtins.property
    @jsii.member(jsii_name="dictionaryKeyThreshold")
    def dictionary_key_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dictionaryKeyThreshold"))

    @dictionary_key_threshold.setter
    def dictionary_key_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3adaf5cea7b64a4441f0416409c7ce02f7b83e3f7d8098fdc8a350cfce72bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dictionaryKeyThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="enablePadding")
    def enable_padding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePadding"))

    @enable_padding.setter
    def enable_padding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199b7d38d451b29925a10a29e99bb44225a295d4d5061c4a972e92e0170d22dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePadding", value)

    @builtins.property
    @jsii.member(jsii_name="formatVersion")
    def format_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "formatVersion"))

    @format_version.setter
    def format_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f42dc05b72d98a35bf39ddf5e11516e24a7a6fac946ee8eb1de4b420d2048e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatVersion", value)

    @builtins.property
    @jsii.member(jsii_name="paddingTolerance")
    def padding_tolerance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "paddingTolerance"))

    @padding_tolerance.setter
    def padding_tolerance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2479469ebdc8c1a9efeb51e5dd6001e1cb9086fa99f4e19e8814e12c7c41b23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paddingTolerance", value)

    @builtins.property
    @jsii.member(jsii_name="rowIndexStride")
    def row_index_stride(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowIndexStride"))

    @row_index_stride.setter
    def row_index_stride(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b01fff2e657abc9c994a74b9747cdc5d0f032ebc064d24649e81e23dbe06d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowIndexStride", value)

    @builtins.property
    @jsii.member(jsii_name="stripeSizeBytes")
    def stripe_size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stripeSizeBytes"))

    @stripe_size_bytes.setter
    def stripe_size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bda27ab98cfd8254e50ceb9eb75a9960d821db43bf82ef1d0a61c4b4a5693aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stripeSizeBytes", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fe4aea218f36aa134859bc9d67a4eeee55f5c6880459932594d5363ee0deaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ab769c532208603f004b21200de34ef3b6069781f88bcf0fed355462a772f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOrcSerDe")
    def put_orc_ser_de(
        self,
        *,
        block_size_bytes: typing.Optional[jsii.Number] = None,
        bloom_filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        bloom_filter_false_positive_probability: typing.Optional[jsii.Number] = None,
        compression: typing.Optional[builtins.str] = None,
        dictionary_key_threshold: typing.Optional[jsii.Number] = None,
        enable_padding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        format_version: typing.Optional[builtins.str] = None,
        padding_tolerance: typing.Optional[jsii.Number] = None,
        row_index_stride: typing.Optional[jsii.Number] = None,
        stripe_size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param block_size_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#block_size_bytes KinesisFirehoseDeliveryStream#block_size_bytes}.
        :param bloom_filter_columns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bloom_filter_columns KinesisFirehoseDeliveryStream#bloom_filter_columns}.
        :param bloom_filter_false_positive_probability: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bloom_filter_false_positive_probability KinesisFirehoseDeliveryStream#bloom_filter_false_positive_probability}.
        :param compression: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression KinesisFirehoseDeliveryStream#compression}.
        :param dictionary_key_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#dictionary_key_threshold KinesisFirehoseDeliveryStream#dictionary_key_threshold}.
        :param enable_padding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enable_padding KinesisFirehoseDeliveryStream#enable_padding}.
        :param format_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#format_version KinesisFirehoseDeliveryStream#format_version}.
        :param padding_tolerance: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#padding_tolerance KinesisFirehoseDeliveryStream#padding_tolerance}.
        :param row_index_stride: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#row_index_stride KinesisFirehoseDeliveryStream#row_index_stride}.
        :param stripe_size_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#stripe_size_bytes KinesisFirehoseDeliveryStream#stripe_size_bytes}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe(
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

        return typing.cast(None, jsii.invoke(self, "putOrcSerDe", [value]))

    @jsii.member(jsii_name="putParquetSerDe")
    def put_parquet_ser_de(
        self,
        *,
        block_size_bytes: typing.Optional[jsii.Number] = None,
        compression: typing.Optional[builtins.str] = None,
        enable_dictionary_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_padding_bytes: typing.Optional[jsii.Number] = None,
        page_size_bytes: typing.Optional[jsii.Number] = None,
        writer_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param block_size_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#block_size_bytes KinesisFirehoseDeliveryStream#block_size_bytes}.
        :param compression: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression KinesisFirehoseDeliveryStream#compression}.
        :param enable_dictionary_compression: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enable_dictionary_compression KinesisFirehoseDeliveryStream#enable_dictionary_compression}.
        :param max_padding_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#max_padding_bytes KinesisFirehoseDeliveryStream#max_padding_bytes}.
        :param page_size_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#page_size_bytes KinesisFirehoseDeliveryStream#page_size_bytes}.
        :param writer_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#writer_version KinesisFirehoseDeliveryStream#writer_version}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe(
            block_size_bytes=block_size_bytes,
            compression=compression,
            enable_dictionary_compression=enable_dictionary_compression,
            max_padding_bytes=max_padding_bytes,
            page_size_bytes=page_size_bytes,
            writer_version=writer_version,
        )

        return typing.cast(None, jsii.invoke(self, "putParquetSerDe", [value]))

    @jsii.member(jsii_name="resetOrcSerDe")
    def reset_orc_ser_de(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrcSerDe", []))

    @jsii.member(jsii_name="resetParquetSerDe")
    def reset_parquet_ser_de(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParquetSerDe", []))

    @builtins.property
    @jsii.member(jsii_name="orcSerDe")
    def orc_ser_de(
        self,
    ) -> KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDeOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDeOutputReference, jsii.get(self, "orcSerDe"))

    @builtins.property
    @jsii.member(jsii_name="parquetSerDe")
    def parquet_ser_de(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDeOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDeOutputReference", jsii.get(self, "parquetSerDe"))

    @builtins.property
    @jsii.member(jsii_name="orcSerDeInput")
    def orc_ser_de_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe], jsii.get(self, "orcSerDeInput"))

    @builtins.property
    @jsii.member(jsii_name="parquetSerDeInput")
    def parquet_ser_de_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe"], jsii.get(self, "parquetSerDeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9537b814c43e37f86d893c0a53727d9e99c03fbf031b01a763cfc2d5789781d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe",
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
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe:
    def __init__(
        self,
        *,
        block_size_bytes: typing.Optional[jsii.Number] = None,
        compression: typing.Optional[builtins.str] = None,
        enable_dictionary_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_padding_bytes: typing.Optional[jsii.Number] = None,
        page_size_bytes: typing.Optional[jsii.Number] = None,
        writer_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param block_size_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#block_size_bytes KinesisFirehoseDeliveryStream#block_size_bytes}.
        :param compression: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression KinesisFirehoseDeliveryStream#compression}.
        :param enable_dictionary_compression: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enable_dictionary_compression KinesisFirehoseDeliveryStream#enable_dictionary_compression}.
        :param max_padding_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#max_padding_bytes KinesisFirehoseDeliveryStream#max_padding_bytes}.
        :param page_size_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#page_size_bytes KinesisFirehoseDeliveryStream#page_size_bytes}.
        :param writer_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#writer_version KinesisFirehoseDeliveryStream#writer_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fad077eca05bce0ccae6574cb9b742c95561cadceff7e6dc006e48bb90e5366)
            check_type(argname="argument block_size_bytes", value=block_size_bytes, expected_type=type_hints["block_size_bytes"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument enable_dictionary_compression", value=enable_dictionary_compression, expected_type=type_hints["enable_dictionary_compression"])
            check_type(argname="argument max_padding_bytes", value=max_padding_bytes, expected_type=type_hints["max_padding_bytes"])
            check_type(argname="argument page_size_bytes", value=page_size_bytes, expected_type=type_hints["page_size_bytes"])
            check_type(argname="argument writer_version", value=writer_version, expected_type=type_hints["writer_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#block_size_bytes KinesisFirehoseDeliveryStream#block_size_bytes}.'''
        result = self._values.get("block_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression KinesisFirehoseDeliveryStream#compression}.'''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_dictionary_compression(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enable_dictionary_compression KinesisFirehoseDeliveryStream#enable_dictionary_compression}.'''
        result = self._values.get("enable_dictionary_compression")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_padding_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#max_padding_bytes KinesisFirehoseDeliveryStream#max_padding_bytes}.'''
        result = self._values.get("max_padding_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def page_size_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#page_size_bytes KinesisFirehoseDeliveryStream#page_size_bytes}.'''
        result = self._values.get("page_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def writer_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#writer_version KinesisFirehoseDeliveryStream#writer_version}.'''
        result = self._values.get("writer_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5234d893d1ca5e8d7adc97bc7fd660eb8c5d11efd647b77453398dde04d919fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBlockSizeBytes")
    def reset_block_size_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockSizeBytes", []))

    @jsii.member(jsii_name="resetCompression")
    def reset_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompression", []))

    @jsii.member(jsii_name="resetEnableDictionaryCompression")
    def reset_enable_dictionary_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDictionaryCompression", []))

    @jsii.member(jsii_name="resetMaxPaddingBytes")
    def reset_max_padding_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPaddingBytes", []))

    @jsii.member(jsii_name="resetPageSizeBytes")
    def reset_page_size_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPageSizeBytes", []))

    @jsii.member(jsii_name="resetWriterVersion")
    def reset_writer_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriterVersion", []))

    @builtins.property
    @jsii.member(jsii_name="blockSizeBytesInput")
    def block_size_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "blockSizeBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionInput")
    def compression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDictionaryCompressionInput")
    def enable_dictionary_compression_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDictionaryCompressionInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPaddingBytesInput")
    def max_padding_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPaddingBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="pageSizeBytesInput")
    def page_size_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pageSizeBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="writerVersionInput")
    def writer_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writerVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="blockSizeBytes")
    def block_size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "blockSizeBytes"))

    @block_size_bytes.setter
    def block_size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6649e8de24fdfbedd35534a346da495cbe6f0d61101e43402488fce02e1139d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockSizeBytes", value)

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402a5ffb195c65f18b01448ad9fbac6bd618facc051316fe4bdff6e035effebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value)

    @builtins.property
    @jsii.member(jsii_name="enableDictionaryCompression")
    def enable_dictionary_compression(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDictionaryCompression"))

    @enable_dictionary_compression.setter
    def enable_dictionary_compression(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f5452c6cb743b9a48eef78715845216188bb7a3eccb61220a9b7bc80a87f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDictionaryCompression", value)

    @builtins.property
    @jsii.member(jsii_name="maxPaddingBytes")
    def max_padding_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPaddingBytes"))

    @max_padding_bytes.setter
    def max_padding_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6245a0429e366aa907a9a7b8d2a57316e5c4f12e355a5dbeaf1e7b9d01dc55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPaddingBytes", value)

    @builtins.property
    @jsii.member(jsii_name="pageSizeBytes")
    def page_size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pageSizeBytes"))

    @page_size_bytes.setter
    def page_size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d24688c6baf0c972a4f75945928f7da68a421f4f61bfda266d87ba2f324d776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pageSizeBytes", value)

    @builtins.property
    @jsii.member(jsii_name="writerVersion")
    def writer_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writerVersion"))

    @writer_version.setter
    def writer_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcef9b717798e6f004455c396f4005e209d8b7dfce09e3599029b6b9a38aa25d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writerVersion", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2eca011874b6b8cbb01821483d2455342efd1885ee5e954060fde68d171233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47b02740bb11b6e2f6f1ba47fcb668283105773b1b9c4f9913d86c1aa9e181b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInputFormatConfiguration")
    def put_input_format_configuration(
        self,
        *,
        deserializer: typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param deserializer: deserializer block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#deserializer KinesisFirehoseDeliveryStream#deserializer}
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration(
            deserializer=deserializer
        )

        return typing.cast(None, jsii.invoke(self, "putInputFormatConfiguration", [value]))

    @jsii.member(jsii_name="putOutputFormatConfiguration")
    def put_output_format_configuration(
        self,
        *,
        serializer: typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param serializer: serializer block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#serializer KinesisFirehoseDeliveryStream#serializer}
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration(
            serializer=serializer
        )

        return typing.cast(None, jsii.invoke(self, "putOutputFormatConfiguration", [value]))

    @jsii.member(jsii_name="putSchemaConfiguration")
    def put_schema_configuration(
        self,
        *,
        database_name: builtins.str,
        role_arn: builtins.str,
        table_name: builtins.str,
        catalog_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#database_name KinesisFirehoseDeliveryStream#database_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#table_name KinesisFirehoseDeliveryStream#table_name}.
        :param catalog_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#catalog_id KinesisFirehoseDeliveryStream#catalog_id}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#region KinesisFirehoseDeliveryStream#region}.
        :param version_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#version_id KinesisFirehoseDeliveryStream#version_id}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration(
            database_name=database_name,
            role_arn=role_arn,
            table_name=table_name,
            catalog_id=catalog_id,
            region=region,
            version_id=version_id,
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaConfiguration", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="inputFormatConfiguration")
    def input_format_configuration(
        self,
    ) -> KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationOutputReference, jsii.get(self, "inputFormatConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="outputFormatConfiguration")
    def output_format_configuration(
        self,
    ) -> KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationOutputReference, jsii.get(self, "outputFormatConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="schemaConfiguration")
    def schema_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfigurationOutputReference", jsii.get(self, "schemaConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="inputFormatConfigurationInput")
    def input_format_configuration_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration], jsii.get(self, "inputFormatConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="outputFormatConfigurationInput")
    def output_format_configuration_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration], jsii.get(self, "outputFormatConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaConfigurationInput")
    def schema_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration"], jsii.get(self, "schemaConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e074f92033b4f28efed796cf1c1af1851ec4c63d398cf01217270fef83c4e604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76671ab44b30963d20dedb4aaf742fee776f696ddec8a2f5dcc504027a372619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "role_arn": "roleArn",
        "table_name": "tableName",
        "catalog_id": "catalogId",
        "region": "region",
        "version_id": "versionId",
    },
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        role_arn: builtins.str,
        table_name: builtins.str,
        catalog_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#database_name KinesisFirehoseDeliveryStream#database_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#table_name KinesisFirehoseDeliveryStream#table_name}.
        :param catalog_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#catalog_id KinesisFirehoseDeliveryStream#catalog_id}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#region KinesisFirehoseDeliveryStream#region}.
        :param version_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#version_id KinesisFirehoseDeliveryStream#version_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4486293f22a12b15ec1118d2248742d7618f4a5c7bd762ea18f87ca0b223aeb)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "role_arn": role_arn,
            "table_name": table_name,
        }
        if catalog_id is not None:
            self._values["catalog_id"] = catalog_id
        if region is not None:
            self._values["region"] = region
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#database_name KinesisFirehoseDeliveryStream#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#table_name KinesisFirehoseDeliveryStream#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def catalog_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#catalog_id KinesisFirehoseDeliveryStream#catalog_id}.'''
        result = self._values.get("catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#region KinesisFirehoseDeliveryStream#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#version_id KinesisFirehoseDeliveryStream#version_id}.'''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4f4f9e4fad69ae901b3c42297d889a6bc26c2db083c9be85078bdf6a9b29e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCatalogId")
    def reset_catalog_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalogId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetVersionId")
    def reset_version_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionId", []))

    @builtins.property
    @jsii.member(jsii_name="catalogIdInput")
    def catalog_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogIdInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="versionIdInput")
    def version_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalogId"))

    @catalog_id.setter
    def catalog_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090beb74f9c623d84d6fa02f8460554107dcc0fbfdd0ba045e5a86ea74fceab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalogId", value)

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ee6dae6c388af32447b0f70454e4ff126b9f9dde68af1068f70f8362236bfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77979db73442f220a465aa4700f889dc5b8bbb1e4781917e471b5490561e304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a6f243e1af0ee7166a3d28a384abf606852cb6c7531f3fb92b365fd6a17076d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e00f48f81acac61cdb22cacca016eb626b622d7e8d4f38251ff6afa390ed8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value)

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519c05a3d5c1e08c8685eb082d7fdef6fe02f29b0dc89000aaadeac5c536f5e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bcfa030438e6c8c075cd3f9ab37139121e1c827af6bc2d815b44fe0595617b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "retry_duration": "retryDuration"},
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_duration: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param retry_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e9b8ca5ad4c612c5d7ae1b0f33846ec2dc4fd393f7865467c7260d1f691b80)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument retry_duration", value=retry_duration, expected_type=type_hints["retry_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if retry_duration is not None:
            self._values["retry_duration"] = retry_duration

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retry_duration(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.'''
        result = self._values.get("retry_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a08a20a8436d7368478d459b60fe7913ee980bf3b90920706606407db2f443)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetRetryDuration")
    def reset_retry_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryDuration", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="retryDurationInput")
    def retry_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7223a8a186746a62beb0c24a510fd6bad548728c420a4ec6b184dc21dc556ad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="retryDuration")
    def retry_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryDuration"))

    @retry_duration.setter
    def retry_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f642cdfa5884d818ff55923603a9a983660084ad5c2ae4e3d159dfec834159ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryDuration", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c78164708f0232901881a63ca3a052614030a542bfc3ed8abb92e6e96b131f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c56ac720587aa614e337a1105abd416c78d145fa4d42af1ec908f14e9f4a4ed6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLoggingOptions")
    def put_cloudwatch_logging_options(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions(
            enabled=enabled,
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingOptions", [value]))

    @jsii.member(jsii_name="putDataFormatConversionConfiguration")
    def put_data_format_conversion_configuration(
        self,
        *,
        input_format_configuration: typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration, typing.Dict[builtins.str, typing.Any]],
        output_format_configuration: typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration, typing.Dict[builtins.str, typing.Any]],
        schema_configuration: typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration, typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param input_format_configuration: input_format_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#input_format_configuration KinesisFirehoseDeliveryStream#input_format_configuration}
        :param output_format_configuration: output_format_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#output_format_configuration KinesisFirehoseDeliveryStream#output_format_configuration}
        :param schema_configuration: schema_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#schema_configuration KinesisFirehoseDeliveryStream#schema_configuration}
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration(
            input_format_configuration=input_format_configuration,
            output_format_configuration=output_format_configuration,
            schema_configuration=schema_configuration,
            enabled=enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putDataFormatConversionConfiguration", [value]))

    @jsii.member(jsii_name="putDynamicPartitioningConfiguration")
    def put_dynamic_partitioning_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retry_duration: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param retry_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration(
            enabled=enabled, retry_duration=retry_duration
        )

        return typing.cast(None, jsii.invoke(self, "putDynamicPartitioningConfiguration", [value]))

    @jsii.member(jsii_name="putProcessingConfiguration")
    def put_processing_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param processors: processors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration(
            enabled=enabled, processors=processors
        )

        return typing.cast(None, jsii.invoke(self, "putProcessingConfiguration", [value]))

    @jsii.member(jsii_name="putS3BackupConfiguration")
    def put_s3_backup_configuration(
        self,
        *,
        bucket_arn: builtins.str,
        role_arn: builtins.str,
        buffer_interval: typing.Optional[jsii.Number] = None,
        buffer_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_format: typing.Optional[builtins.str] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param buffer_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.
        :param buffer_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param compression_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.
        :param error_output_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration(
            bucket_arn=bucket_arn,
            role_arn=role_arn,
            buffer_interval=buffer_interval,
            buffer_size=buffer_size,
            cloudwatch_logging_options=cloudwatch_logging_options,
            compression_format=compression_format,
            error_output_prefix=error_output_prefix,
            kms_key_arn=kms_key_arn,
            prefix=prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putS3BackupConfiguration", [value]))

    @jsii.member(jsii_name="resetBufferInterval")
    def reset_buffer_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferInterval", []))

    @jsii.member(jsii_name="resetBufferSize")
    def reset_buffer_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferSize", []))

    @jsii.member(jsii_name="resetCloudwatchLoggingOptions")
    def reset_cloudwatch_logging_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingOptions", []))

    @jsii.member(jsii_name="resetCompressionFormat")
    def reset_compression_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionFormat", []))

    @jsii.member(jsii_name="resetDataFormatConversionConfiguration")
    def reset_data_format_conversion_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataFormatConversionConfiguration", []))

    @jsii.member(jsii_name="resetDynamicPartitioningConfiguration")
    def reset_dynamic_partitioning_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicPartitioningConfiguration", []))

    @jsii.member(jsii_name="resetErrorOutputPrefix")
    def reset_error_output_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOutputPrefix", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="resetProcessingConfiguration")
    def reset_processing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessingConfiguration", []))

    @jsii.member(jsii_name="resetS3BackupConfiguration")
    def reset_s3_backup_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BackupConfiguration", []))

    @jsii.member(jsii_name="resetS3BackupMode")
    def reset_s3_backup_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BackupMode", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptions")
    def cloudwatch_logging_options(
        self,
    ) -> KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptionsOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptionsOutputReference, jsii.get(self, "cloudwatchLoggingOptions"))

    @builtins.property
    @jsii.member(jsii_name="dataFormatConversionConfiguration")
    def data_format_conversion_configuration(
        self,
    ) -> KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputReference, jsii.get(self, "dataFormatConversionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="dynamicPartitioningConfiguration")
    def dynamic_partitioning_configuration(
        self,
    ) -> KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfigurationOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfigurationOutputReference, jsii.get(self, "dynamicPartitioningConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="processingConfiguration")
    def processing_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationOutputReference", jsii.get(self, "processingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3BackupConfiguration")
    def s3_backup_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationOutputReference", jsii.get(self, "s3BackupConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="bucketArnInput")
    def bucket_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferIntervalInput")
    def buffer_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferSizeInput")
    def buffer_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptionsInput")
    def cloudwatch_logging_options_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions], jsii.get(self, "cloudwatchLoggingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionFormatInput")
    def compression_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFormatConversionConfigurationInput")
    def data_format_conversion_configuration_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration], jsii.get(self, "dataFormatConversionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicPartitioningConfigurationInput")
    def dynamic_partitioning_configuration_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration], jsii.get(self, "dynamicPartitioningConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="errorOutputPrefixInput")
    def error_output_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorOutputPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="processingConfigurationInput")
    def processing_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration"], jsii.get(self, "processingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BackupConfigurationInput")
    def s3_backup_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration"], jsii.get(self, "s3BackupConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BackupModeInput")
    def s3_backup_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BackupModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @bucket_arn.setter
    def bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7a96d5c5974bac81062812905a95ab237c1f2a752c7ef241395c872c2a2de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketArn", value)

    @builtins.property
    @jsii.member(jsii_name="bufferInterval")
    def buffer_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferInterval"))

    @buffer_interval.setter
    def buffer_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe68f4748a3bd0c559e95401d16e1221a037e86b2ac36c04d5c2b1a0bf16620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferInterval", value)

    @builtins.property
    @jsii.member(jsii_name="bufferSize")
    def buffer_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferSize"))

    @buffer_size.setter
    def buffer_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2174deea0aa015dc64c79c8e28adbef47e6a9b70ce84a689f5db2356de063515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferSize", value)

    @builtins.property
    @jsii.member(jsii_name="compressionFormat")
    def compression_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionFormat"))

    @compression_format.setter
    def compression_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d034ff4f56d813c614883f53bb83020b3456e014fb79383790b1daf41c0bd253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionFormat", value)

    @builtins.property
    @jsii.member(jsii_name="errorOutputPrefix")
    def error_output_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorOutputPrefix"))

    @error_output_prefix.setter
    def error_output_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f8355d225062f602d519dfab718fcd27a72ba694753b2774594357f3ffa92e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOutputPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0f91326da7ce1532c423a7ff870061ac878e2338952badc8633d170c32097b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69fd8ee9f34556611169d4dca1013f4acba89be5575d1adffeca9b0e34d6eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c34eb23f09a0a041fdd64949b2997f8c45727043772eaf1e0c5acf75fea794e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="s3BackupMode")
    def s3_backup_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BackupMode"))

    @s3_backup_mode.setter
    def s3_backup_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a54a166c893806a91837f3b531a817c3930a1e0117481d2496817d572734c8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BackupMode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3Configuration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3Configuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3Configuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db197d8d8767183ec7a992f02f239e22fdccccc629e1cbceb4ddcbf9df078a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "processors": "processors"},
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param processors: processors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb05123eeedc628a96a0823ca8873237c26ac708cb6f452d39910a2eb4f8eef)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if processors is not None:
            self._values["processors"] = processors

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def processors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors"]]]:
        '''processors block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        result = self._values.get("processors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9933f649ee4677160784296a5d202939ae07e3a453b6506b631804b3c070b357)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProcessors")
    def put_processors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daea9d23f9a6ac89e4d156a824bdf0bfd3915568f22a4e1c784ae6dfa5a13c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProcessors", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetProcessors")
    def reset_processors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessors", []))

    @builtins.property
    @jsii.member(jsii_name="processors")
    def processors(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsList":
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsList", jsii.get(self, "processors"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="processorsInput")
    def processors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors"]]], jsii.get(self, "processorsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f56b6c7d450c85b443e267082349da036eabb36cdb40e2b699cafacbe11c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9fc4a60ecb6089be75c30eeddd95c37a8626a4934ada1433d8d740be2fe10c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "parameters": "parameters"},
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors:
    def __init__(
        self,
        *,
        type: builtins.str,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type KinesisFirehoseDeliveryStream#type}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameters KinesisFirehoseDeliveryStream#parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81a37cb26c6b63efd8400215045e7658998bedb8bfc911feeabc23e0c8ac6d1)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type KinesisFirehoseDeliveryStream#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters"]]]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameters KinesisFirehoseDeliveryStream#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903d5e62183d14094a710c30d4fb476023661b7a6677c69e8b533579da626859)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca701169a5515fbcac41ff7a5009e11d8b0bbf87e7dfe6ca59dd131b41612d61)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031b50045dc22c2f49aafdb7ebc1ad032ebe037321e9b41e0f96cad6d0bf521a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0823205acc0d12dbe8df44030573744302422a254a4e96d9f34754a849e476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea396d582d8f8251fde074c17ef6476af16e435e9c84bb334fd0875ba0af253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820d114072af030b7057bf2ad99bc88de2083ce27f127b898323dd9385511c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ba9d7635ae89507ff3f69020d8412618409c3dc622878edeb7a2b363048d56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545de61c20803285a8040402f19035de38642a697b4fd07e927b13783a3ac4f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParametersList":
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters"]]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40bc4458f461ee3920387e7088be81ef5c1c7e449dd1d421e18c49d6f531777a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ceb50bca5ca5871a90766788aa588b00f7937dff8e7d577aa9d5edad4650bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_name": "parameterName",
        "parameter_value": "parameterValue",
    },
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters:
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        parameter_value: builtins.str,
    ) -> None:
        '''
        :param parameter_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_name KinesisFirehoseDeliveryStream#parameter_name}.
        :param parameter_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_value KinesisFirehoseDeliveryStream#parameter_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178a07841625b0707053611dbf25492e35f8fcaf29c3c5787a7431c587d15784)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter_name": parameter_name,
            "parameter_value": parameter_value,
        }

    @builtins.property
    def parameter_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_name KinesisFirehoseDeliveryStream#parameter_name}.'''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_value KinesisFirehoseDeliveryStream#parameter_value}.'''
        result = self._values.get("parameter_value")
        assert result is not None, "Required property 'parameter_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParametersList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a910d0329193591963825a91ce8c2d61156185d264289f0f5859c4852c27c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0cfd84f4a7e1f2e9d86acb34b9d2ff837c3bc944f8ae0a430fa27c886acb40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499474030a21bcacfc93933b3f02bba178059ae0ad917d0eb48af97d6a2fba52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c91075e105d642acb8ead3d064899452f5b5e462cb84502b91e45ae00c6022f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2476f2bd26fb024c46b5402eee44c575ffd9c3018f5ccf878a5a3c79b5010b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188a207839013542c8250e27db0158dc71b5e868ae492ec25185db3a035b3ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParametersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6cbb44f74d71aff6aa73e4fbd629025ec1b82fdf6fc1ee3b0f6fec61daad5bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="parameterNameInput")
    def parameter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterValueInput")
    def parameter_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterValueInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterName"))

    @parameter_name.setter
    def parameter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de58fba0361b2efa657839b3cc1261ac1c3923c2b4d740d455b6c7f452be7b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterName", value)

    @builtins.property
    @jsii.member(jsii_name="parameterValue")
    def parameter_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterValue"))

    @parameter_value.setter
    def parameter_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78427fe8a531b9ad4abed00b8054f61ba6ed1d6a750e18ae422c2cc630ca777a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd3b8483256e9830b68f17a9ac458c3b53f90ed3ad28408bce3d7f25b03cf06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "role_arn": "roleArn",
        "buffer_interval": "bufferInterval",
        "buffer_size": "bufferSize",
        "cloudwatch_logging_options": "cloudwatchLoggingOptions",
        "compression_format": "compressionFormat",
        "error_output_prefix": "errorOutputPrefix",
        "kms_key_arn": "kmsKeyArn",
        "prefix": "prefix",
    },
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        role_arn: builtins.str,
        buffer_interval: typing.Optional[jsii.Number] = None,
        buffer_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_format: typing.Optional[builtins.str] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param buffer_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.
        :param buffer_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param compression_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.
        :param error_output_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.
        '''
        if isinstance(cloudwatch_logging_options, dict):
            cloudwatch_logging_options = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions(**cloudwatch_logging_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0def57bb238221e31d05302cf1cab6235cd81a8f4ee56966f597e09485a841f3)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument buffer_interval", value=buffer_interval, expected_type=type_hints["buffer_interval"])
            check_type(argname="argument buffer_size", value=buffer_size, expected_type=type_hints["buffer_size"])
            check_type(argname="argument cloudwatch_logging_options", value=cloudwatch_logging_options, expected_type=type_hints["cloudwatch_logging_options"])
            check_type(argname="argument compression_format", value=compression_format, expected_type=type_hints["compression_format"])
            check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "role_arn": role_arn,
        }
        if buffer_interval is not None:
            self._values["buffer_interval"] = buffer_interval
        if buffer_size is not None:
            self._values["buffer_size"] = buffer_size
        if cloudwatch_logging_options is not None:
            self._values["cloudwatch_logging_options"] = cloudwatch_logging_options
        if compression_format is not None:
            self._values["compression_format"] = compression_format
        if error_output_prefix is not None:
            self._values["error_output_prefix"] = error_output_prefix
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def buffer_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.'''
        result = self._values.get("buffer_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def buffer_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.'''
        result = self._values.get("buffer_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cloudwatch_logging_options(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions"]:
        '''cloudwatch_logging_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        '''
        result = self._values.get("cloudwatch_logging_options")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions"], result)

    @builtins.property
    def compression_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.'''
        result = self._values.get("compression_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_output_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.'''
        result = self._values.get("error_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b041930884248cee176c08446eb375b7433de35f638b41468b9249ac28b2f0e2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6799bb97d7b19008a044e63bb3a9f250f351b9ae7250392d45b1994d435b1f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ede5b17c2454cc4c8a54e9fbebfdf459f5de78bdd79ba1205f2767e0908ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9906e2a5bb037bf655cacc6673e491aac6ac786a6be9f01f5e2593342226abb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5709d81d806ef7d2759e1bbe5100917f455aae94a9d4b46d0916cf58cd47ae02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2aa13f7524ba3225ff41547655585df99084ededbab4826f7abfbbb4d31a05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea369930a8d0ecebd349fb517b148b60b34b7b7345d647505edd777a7796c6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLoggingOptions")
    def put_cloudwatch_logging_options(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        value = KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions(
            enabled=enabled,
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingOptions", [value]))

    @jsii.member(jsii_name="resetBufferInterval")
    def reset_buffer_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferInterval", []))

    @jsii.member(jsii_name="resetBufferSize")
    def reset_buffer_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferSize", []))

    @jsii.member(jsii_name="resetCloudwatchLoggingOptions")
    def reset_cloudwatch_logging_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingOptions", []))

    @jsii.member(jsii_name="resetCompressionFormat")
    def reset_compression_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionFormat", []))

    @jsii.member(jsii_name="resetErrorOutputPrefix")
    def reset_error_output_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOutputPrefix", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptions")
    def cloudwatch_logging_options(
        self,
    ) -> KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptionsOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptionsOutputReference, jsii.get(self, "cloudwatchLoggingOptions"))

    @builtins.property
    @jsii.member(jsii_name="bucketArnInput")
    def bucket_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferIntervalInput")
    def buffer_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferSizeInput")
    def buffer_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptionsInput")
    def cloudwatch_logging_options_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions], jsii.get(self, "cloudwatchLoggingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionFormatInput")
    def compression_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="errorOutputPrefixInput")
    def error_output_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorOutputPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @bucket_arn.setter
    def bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40815d1362eb1ba41b4e8791a2e75e203b2bf745e9ff517f1e19a4a4ff49ead1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketArn", value)

    @builtins.property
    @jsii.member(jsii_name="bufferInterval")
    def buffer_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferInterval"))

    @buffer_interval.setter
    def buffer_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b096b7abbf7b5ef6abcbfdcb22003c8ee30d98fda7eb28f3701dd3680791b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferInterval", value)

    @builtins.property
    @jsii.member(jsii_name="bufferSize")
    def buffer_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferSize"))

    @buffer_size.setter
    def buffer_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f1c9a60c888ed968d9980cb5c822b5f5b2f861bd3e4f04e9a7a0097b3e6c826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferSize", value)

    @builtins.property
    @jsii.member(jsii_name="compressionFormat")
    def compression_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionFormat"))

    @compression_format.setter
    def compression_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd6ee510f649e22b169258b235336f0876e67bd6b5eff7dcd7e7803cc4ca4e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionFormat", value)

    @builtins.property
    @jsii.member(jsii_name="errorOutputPrefix")
    def error_output_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorOutputPrefix"))

    @error_output_prefix.setter
    def error_output_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc980db4144cfb86a0447765255e74de6ee11dc419c4905ca790459e1ea5c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOutputPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635fe8547751eeda9f5c3aabde828840c35a617725e4796fbbd67d0b5e167bca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82ba506bcabca65df825d4afb2138a9a63d9e957eb08092a2e57b154bff8631c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc0b546830b1281945d525cf3df8ce6257ccea206518af37e01aa56f661f214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2428ec95305e876cc4ce3dbcba0b2d0b7f4cf0164034c84665bdabb74282f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "access_key": "accessKey",
        "buffering_interval": "bufferingInterval",
        "buffering_size": "bufferingSize",
        "cloudwatch_logging_options": "cloudwatchLoggingOptions",
        "name": "name",
        "processing_configuration": "processingConfiguration",
        "request_configuration": "requestConfiguration",
        "retry_duration": "retryDuration",
        "role_arn": "roleArn",
        "s3_backup_mode": "s3BackupMode",
    },
)
class KinesisFirehoseDeliveryStreamHttpEndpointConfiguration:
    def __init__(
        self,
        *,
        url: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        buffering_interval: typing.Optional[jsii.Number] = None,
        buffering_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        request_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_duration: typing.Optional[jsii.Number] = None,
        role_arn: typing.Optional[builtins.str] = None,
        s3_backup_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#url KinesisFirehoseDeliveryStream#url}.
        :param access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#access_key KinesisFirehoseDeliveryStream#access_key}.
        :param buffering_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_interval KinesisFirehoseDeliveryStream#buffering_interval}.
        :param buffering_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_size KinesisFirehoseDeliveryStream#buffering_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#name KinesisFirehoseDeliveryStream#name}.
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        :param request_configuration: request_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#request_configuration KinesisFirehoseDeliveryStream#request_configuration}
        :param retry_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param s3_backup_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.
        '''
        if isinstance(cloudwatch_logging_options, dict):
            cloudwatch_logging_options = KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions(**cloudwatch_logging_options)
        if isinstance(processing_configuration, dict):
            processing_configuration = KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration(**processing_configuration)
        if isinstance(request_configuration, dict):
            request_configuration = KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration(**request_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a747acc4bb42adf0b624fac1916283c4e7df6eec7c9a68e0d40e67f0386dd0de)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument buffering_interval", value=buffering_interval, expected_type=type_hints["buffering_interval"])
            check_type(argname="argument buffering_size", value=buffering_size, expected_type=type_hints["buffering_size"])
            check_type(argname="argument cloudwatch_logging_options", value=cloudwatch_logging_options, expected_type=type_hints["cloudwatch_logging_options"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
            check_type(argname="argument request_configuration", value=request_configuration, expected_type=type_hints["request_configuration"])
            check_type(argname="argument retry_duration", value=retry_duration, expected_type=type_hints["retry_duration"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if buffering_interval is not None:
            self._values["buffering_interval"] = buffering_interval
        if buffering_size is not None:
            self._values["buffering_size"] = buffering_size
        if cloudwatch_logging_options is not None:
            self._values["cloudwatch_logging_options"] = cloudwatch_logging_options
        if name is not None:
            self._values["name"] = name
        if processing_configuration is not None:
            self._values["processing_configuration"] = processing_configuration
        if request_configuration is not None:
            self._values["request_configuration"] = request_configuration
        if retry_duration is not None:
            self._values["retry_duration"] = retry_duration
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if s3_backup_mode is not None:
            self._values["s3_backup_mode"] = s3_backup_mode

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#url KinesisFirehoseDeliveryStream#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#access_key KinesisFirehoseDeliveryStream#access_key}.'''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def buffering_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_interval KinesisFirehoseDeliveryStream#buffering_interval}.'''
        result = self._values.get("buffering_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def buffering_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffering_size KinesisFirehoseDeliveryStream#buffering_size}.'''
        result = self._values.get("buffering_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cloudwatch_logging_options(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions"]:
        '''cloudwatch_logging_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        '''
        result = self._values.get("cloudwatch_logging_options")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#name KinesisFirehoseDeliveryStream#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processing_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration"]:
        '''processing_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        '''
        result = self._values.get("processing_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration"], result)

    @builtins.property
    def request_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration"]:
        '''request_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#request_configuration KinesisFirehoseDeliveryStream#request_configuration}
        '''
        result = self._values.get("request_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration"], result)

    @builtins.property
    def retry_duration(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.'''
        result = self._values.get("retry_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_backup_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.'''
        result = self._values.get("s3_backup_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamHttpEndpointConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d67c53c280e4c5670dffe48908832163e54ec29bc06135cb158bd758595ca95)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae19070ff624fcc8b69b42cf973fdbfb699e2be9ff57610074a8b398d017df6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1c7a208be69031389fd6e850de89196601c9e5f374a4fa71ed571de29d469d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a73130a1a5c9dc2aea33015ed7902e273f8f4efd93bbf9cf5f198774e17f379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67641925e955b946ffad339c74c80c1203179676d5e4a91f55ab54e5bbc9a1eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88f70922374dec4b3bb7091267a8216a5d3a490eeb3b65438c65464720f46b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa6e75809e742917bfd6d4debf6ffee9c7af46e332eef5de1185a5c48b13d44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLoggingOptions")
    def put_cloudwatch_logging_options(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        value = KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions(
            enabled=enabled,
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingOptions", [value]))

    @jsii.member(jsii_name="putProcessingConfiguration")
    def put_processing_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param processors: processors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        value = KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration(
            enabled=enabled, processors=processors
        )

        return typing.cast(None, jsii.invoke(self, "putProcessingConfiguration", [value]))

    @jsii.member(jsii_name="putRequestConfiguration")
    def put_request_configuration(
        self,
        *,
        common_attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        content_encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_attributes: common_attributes block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#common_attributes KinesisFirehoseDeliveryStream#common_attributes}
        :param content_encoding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#content_encoding KinesisFirehoseDeliveryStream#content_encoding}.
        '''
        value = KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration(
            common_attributes=common_attributes, content_encoding=content_encoding
        )

        return typing.cast(None, jsii.invoke(self, "putRequestConfiguration", [value]))

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

    @jsii.member(jsii_name="resetBufferingInterval")
    def reset_buffering_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferingInterval", []))

    @jsii.member(jsii_name="resetBufferingSize")
    def reset_buffering_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferingSize", []))

    @jsii.member(jsii_name="resetCloudwatchLoggingOptions")
    def reset_cloudwatch_logging_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingOptions", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProcessingConfiguration")
    def reset_processing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessingConfiguration", []))

    @jsii.member(jsii_name="resetRequestConfiguration")
    def reset_request_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestConfiguration", []))

    @jsii.member(jsii_name="resetRetryDuration")
    def reset_retry_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryDuration", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @jsii.member(jsii_name="resetS3BackupMode")
    def reset_s3_backup_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BackupMode", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptions")
    def cloudwatch_logging_options(
        self,
    ) -> KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptionsOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptionsOutputReference, jsii.get(self, "cloudwatchLoggingOptions"))

    @builtins.property
    @jsii.member(jsii_name="processingConfiguration")
    def processing_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationOutputReference", jsii.get(self, "processingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="requestConfiguration")
    def request_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationOutputReference", jsii.get(self, "requestConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferingIntervalInput")
    def buffering_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferingSizeInput")
    def buffering_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferingSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptionsInput")
    def cloudwatch_logging_options_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions], jsii.get(self, "cloudwatchLoggingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="processingConfigurationInput")
    def processing_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration"], jsii.get(self, "processingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="requestConfigurationInput")
    def request_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration"], jsii.get(self, "requestConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="retryDurationInput")
    def retry_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BackupModeInput")
    def s3_backup_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BackupModeInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035cd4ad58cd0fc198f418c81d7ddae12a90287c1c078c253c539470dec1b384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value)

    @builtins.property
    @jsii.member(jsii_name="bufferingInterval")
    def buffering_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferingInterval"))

    @buffering_interval.setter
    def buffering_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5182f1c74df3713755467a7fc9d99c82b55b17e4c9a6a374260988c5e9c851b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferingInterval", value)

    @builtins.property
    @jsii.member(jsii_name="bufferingSize")
    def buffering_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferingSize"))

    @buffering_size.setter
    def buffering_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3f952bd54a94fa3900f182e2afec52e545396025788ad834c32d247726a0b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferingSize", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392230e099081a08be7615446d429c8d70442b032d468477ebd1ce1f691d9f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="retryDuration")
    def retry_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryDuration"))

    @retry_duration.setter
    def retry_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117fb68503f1c7133bd2cf41b4d42ad46ded0964fabff37626a6de8d5bce3004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryDuration", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3971a258083a5ab6d3f61805833b9627f39e6ebe7254db680ab2fcff1107a2b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="s3BackupMode")
    def s3_backup_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BackupMode"))

    @s3_backup_mode.setter
    def s3_backup_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f501ba78914110feffc5c3f1190c49094a31e3fc2a5c99459340f1049772b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BackupMode", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f25d9db8a7097c5cf7373b0ce93c574f3255f8cbde950ab119a487f0e8320ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1c9d34428ce49085e844cbff4c51fbc72a2bf4e03964ea3a45ac05c40abb3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "processors": "processors"},
)
class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param processors: processors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703d7e2faa8207bfcc7375364e2506d84ae51fa2e29a9f2627337ad65ea1a81d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if processors is not None:
            self._values["processors"] = processors

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def processors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors"]]]:
        '''processors block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        result = self._values.get("processors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df30382e4e9c7dfe6d47a58b423ffecfc120662957609332e941c572f4a3e3f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProcessors")
    def put_processors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4f2cbb07f60a16fe5c8599748b8986503ff904ee513b92b2e475d121391ba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProcessors", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetProcessors")
    def reset_processors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessors", []))

    @builtins.property
    @jsii.member(jsii_name="processors")
    def processors(
        self,
    ) -> "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsList":
        return typing.cast("KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsList", jsii.get(self, "processors"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="processorsInput")
    def processors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors"]]], jsii.get(self, "processorsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05c7831ef2e4800665f64f927668a0cefcffd31fd826881aaae1d215aefcf63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1ae251384c8a3c842973beab36156617bb5d4b59429ea161a49b7d23c7647e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "parameters": "parameters"},
)
class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors:
    def __init__(
        self,
        *,
        type: builtins.str,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type KinesisFirehoseDeliveryStream#type}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameters KinesisFirehoseDeliveryStream#parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af241df6eaea7fd76c8e70a7486fa5aee0681616458fca095655f33e13313c7)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type KinesisFirehoseDeliveryStream#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters"]]]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameters KinesisFirehoseDeliveryStream#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ca9df1eb1794bc4b1e49c8583bcf8412728073c41a820585392d2706d99599)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d2743f377eadd578a232bc1429fab98c9d1c48dc8baf07a8c0828612d63c11)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb96360f6d9d70606e4c043dd63bb7100507ce360196dfce1ed9de45d63668a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc94b7ab9ca10df246eefdb0e05bbc0fd70b94be115e53e57f6d04896f099212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f15723a824b663fd47400078eb60d0724c7e206ed11a907a9e659005607edaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3388fc69287f2753098bdbd988ac9f917e6924e221dbf185c870898c42067d6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a8dfd90940ff13daa1780434d27a4f1c7760d117613ee9e4ac81ecb5026876)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b741d45c05197b1b56993f5fda88507b1103b718d4133ed505195883a122d497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParametersList":
        return typing.cast("KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters"]]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71a317e62a41537bff6124b579444fb5535873f5d3e54b81df932b992b167cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f24d5f9755773e355f5d0795fa9a589636a0e04ca018a510a2ad53b77c4da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_name": "parameterName",
        "parameter_value": "parameterValue",
    },
)
class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters:
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        parameter_value: builtins.str,
    ) -> None:
        '''
        :param parameter_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_name KinesisFirehoseDeliveryStream#parameter_name}.
        :param parameter_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_value KinesisFirehoseDeliveryStream#parameter_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426c13c8397c039144ef79914b1603c98d1a55024eccabb2677b173393d55fca)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter_name": parameter_name,
            "parameter_value": parameter_value,
        }

    @builtins.property
    def parameter_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_name KinesisFirehoseDeliveryStream#parameter_name}.'''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_value KinesisFirehoseDeliveryStream#parameter_value}.'''
        result = self._values.get("parameter_value")
        assert result is not None, "Required property 'parameter_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParametersList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c98f8fc45141f1b668c7720c99fbf3849a7d1a263ff7e6b5177fb9073cbcd3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4049ce79eeba9708c84d3d397fb189ae448bde236d4e3250bb17673fb5fd28f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db08b1b3b949c340b82fb77d1c24e5fec04fa83c89af8d056080347ebdcf127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5645df17bfdd7dc5319c041c87d590273da7323ef74aa81e31c249c4ae6e88d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a0386e7cde1078dcd5bdb2944c99cfb4f63d60b9de32f6b5828f6ffa70d7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265ee91fcdb132bee47b801ab73b46bba70aeeea1b81c18edfb48d8c6b483076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParametersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21235155e78bcaf03eb69b490302013f8a3c38a7c2ac9365998ec3abeff74d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="parameterNameInput")
    def parameter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterValueInput")
    def parameter_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterValueInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterName"))

    @parameter_name.setter
    def parameter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65861f04aabaa4d562288d45ae8163ef0e3fcd330874cd429ec3664a76b002b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterName", value)

    @builtins.property
    @jsii.member(jsii_name="parameterValue")
    def parameter_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterValue"))

    @parameter_value.setter
    def parameter_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2324b866788de3633508ca5224a841b90ef0d1dbfd5fd8362299bc4ea2f538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69964e78e21d860703a95559acbc14ca41ec50c763b8a30e8ffd8f5ca86358a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "common_attributes": "commonAttributes",
        "content_encoding": "contentEncoding",
    },
)
class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration:
    def __init__(
        self,
        *,
        common_attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        content_encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_attributes: common_attributes block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#common_attributes KinesisFirehoseDeliveryStream#common_attributes}
        :param content_encoding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#content_encoding KinesisFirehoseDeliveryStream#content_encoding}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70fe59e623f67cbff3e2a9c626614bb9e380ee0a70a0c991a917056d327482df)
            check_type(argname="argument common_attributes", value=common_attributes, expected_type=type_hints["common_attributes"])
            check_type(argname="argument content_encoding", value=content_encoding, expected_type=type_hints["content_encoding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if common_attributes is not None:
            self._values["common_attributes"] = common_attributes
        if content_encoding is not None:
            self._values["content_encoding"] = content_encoding

    @builtins.property
    def common_attributes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes"]]]:
        '''common_attributes block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#common_attributes KinesisFirehoseDeliveryStream#common_attributes}
        '''
        result = self._values.get("common_attributes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes"]]], result)

    @builtins.property
    def content_encoding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#content_encoding KinesisFirehoseDeliveryStream#content_encoding}.'''
        result = self._values.get("content_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#name KinesisFirehoseDeliveryStream#name}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#value KinesisFirehoseDeliveryStream#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b98eb725f278b3ad417470258dabdab55eadee41f992450ba944424a44bbf6a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#name KinesisFirehoseDeliveryStream#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#value KinesisFirehoseDeliveryStream#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef84572fbe52b7b90bb455594c800daf83ba0f17d30fe1b78f299580a565f8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fe5195ebdfcd54f1dd6389bd7698560bb894cffc889a7b1814ffbf94aa937e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd33cc9fd3bd1cb0fc62f0b2f3e45ba4702fc4fee5cb1f8949e44c42a2fe03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43bb4f602240c5edc045837e5f5cdd2d03528f4607d2dc3bff6e0605cafe51e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08eb4d652bb23ec6140336266af25035c325fbd9358160d45513f545e91d47c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d847c6ff6254c09462a50d04cde283b48cc2ec354c47eada1854dbc4bc34a693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9431ea8cd8f0a26dfc5ac15f24991d2d220dd535842a6808981028289d8d25b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2e1f21d6c910ebf52897ceb969903ad5ccc5d27b361e6f774ba2a3bc8f50f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acca243bc3a6e9b2ed7ba6cdc8dd5b15eea85834a161e7b232199a5fa2a399db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212a79ede6d8e62299f9c236bc0e2aebb7295435c88036828f9e1bc3c64fb2a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee28044b02f1e2665e01c009bb4afabae60169829aa493ce0e82bbec0501d3ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCommonAttributes")
    def put_common_attributes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5dac634455716452834ada27a4d50b8de35d5739001959d47c49acea1f6697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCommonAttributes", [value]))

    @jsii.member(jsii_name="resetCommonAttributes")
    def reset_common_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonAttributes", []))

    @jsii.member(jsii_name="resetContentEncoding")
    def reset_content_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentEncoding", []))

    @builtins.property
    @jsii.member(jsii_name="commonAttributes")
    def common_attributes(
        self,
    ) -> KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributesList:
        return typing.cast(KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributesList, jsii.get(self, "commonAttributes"))

    @builtins.property
    @jsii.member(jsii_name="commonAttributesInput")
    def common_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes]]], jsii.get(self, "commonAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="contentEncodingInput")
    def content_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="contentEncoding")
    def content_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentEncoding"))

    @content_encoding.setter
    def content_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2bfe89c7653e2ce7d0c69e8e98277b9681c466d4b7ba2dbc237726b985d02a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentEncoding", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95dc4b5c931a4b47728358206f307e5d885f44aeed05ce672b56ea26d341e789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamKinesisSourceConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kinesis_stream_arn": "kinesisStreamArn", "role_arn": "roleArn"},
)
class KinesisFirehoseDeliveryStreamKinesisSourceConfiguration:
    def __init__(
        self,
        *,
        kinesis_stream_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param kinesis_stream_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kinesis_stream_arn KinesisFirehoseDeliveryStream#kinesis_stream_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aba4c1e4766dae496ef1c8bfc1c1df5d42bae0a777760529f2cc156e3737d6e)
            check_type(argname="argument kinesis_stream_arn", value=kinesis_stream_arn, expected_type=type_hints["kinesis_stream_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kinesis_stream_arn": kinesis_stream_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def kinesis_stream_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kinesis_stream_arn KinesisFirehoseDeliveryStream#kinesis_stream_arn}.'''
        result = self._values.get("kinesis_stream_arn")
        assert result is not None, "Required property 'kinesis_stream_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamKinesisSourceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamKinesisSourceConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamKinesisSourceConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a7e58fc7609bb8e23662e4cd4e4665f71708c4c28ed8d1b0e93aae56f57778)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamArnInput")
    def kinesis_stream_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kinesisStreamArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamArn")
    def kinesis_stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kinesisStreamArn"))

    @kinesis_stream_arn.setter
    def kinesis_stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b1dee9549eae1ab7ae328d7d34a16ef4a1a2246d36422609f3017b648511aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisStreamArn", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812f977e142979aa3002dcb8282935c6f6b593d68996096623a04734cd847e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamKinesisSourceConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamKinesisSourceConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamKinesisSourceConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3d0d4ecb4bc059df3bee15a7189b65fbcbdc50ffd7772961f3e3d15c48a233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_jdbcurl": "clusterJdbcurl",
        "data_table_name": "dataTableName",
        "password": "password",
        "role_arn": "roleArn",
        "username": "username",
        "cloudwatch_logging_options": "cloudwatchLoggingOptions",
        "copy_options": "copyOptions",
        "data_table_columns": "dataTableColumns",
        "processing_configuration": "processingConfiguration",
        "retry_duration": "retryDuration",
        "s3_backup_configuration": "s3BackupConfiguration",
        "s3_backup_mode": "s3BackupMode",
    },
)
class KinesisFirehoseDeliveryStreamRedshiftConfiguration:
    def __init__(
        self,
        *,
        cluster_jdbcurl: builtins.str,
        data_table_name: builtins.str,
        password: builtins.str,
        role_arn: builtins.str,
        username: builtins.str,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        copy_options: typing.Optional[builtins.str] = None,
        data_table_columns: typing.Optional[builtins.str] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_duration: typing.Optional[jsii.Number] = None,
        s3_backup_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_backup_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_jdbcurl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cluster_jdbcurl KinesisFirehoseDeliveryStream#cluster_jdbcurl}.
        :param data_table_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#data_table_name KinesisFirehoseDeliveryStream#data_table_name}.
        :param password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#password KinesisFirehoseDeliveryStream#password}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#username KinesisFirehoseDeliveryStream#username}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param copy_options: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#copy_options KinesisFirehoseDeliveryStream#copy_options}.
        :param data_table_columns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#data_table_columns KinesisFirehoseDeliveryStream#data_table_columns}.
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        :param retry_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.
        :param s3_backup_configuration: s3_backup_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_configuration KinesisFirehoseDeliveryStream#s3_backup_configuration}
        :param s3_backup_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.
        '''
        if isinstance(cloudwatch_logging_options, dict):
            cloudwatch_logging_options = KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions(**cloudwatch_logging_options)
        if isinstance(processing_configuration, dict):
            processing_configuration = KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration(**processing_configuration)
        if isinstance(s3_backup_configuration, dict):
            s3_backup_configuration = KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration(**s3_backup_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19a8f62231062221bdfcd28279f8df98eb3f29b2489b587a4b4d4ee19c82ed3)
            check_type(argname="argument cluster_jdbcurl", value=cluster_jdbcurl, expected_type=type_hints["cluster_jdbcurl"])
            check_type(argname="argument data_table_name", value=data_table_name, expected_type=type_hints["data_table_name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument cloudwatch_logging_options", value=cloudwatch_logging_options, expected_type=type_hints["cloudwatch_logging_options"])
            check_type(argname="argument copy_options", value=copy_options, expected_type=type_hints["copy_options"])
            check_type(argname="argument data_table_columns", value=data_table_columns, expected_type=type_hints["data_table_columns"])
            check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
            check_type(argname="argument retry_duration", value=retry_duration, expected_type=type_hints["retry_duration"])
            check_type(argname="argument s3_backup_configuration", value=s3_backup_configuration, expected_type=type_hints["s3_backup_configuration"])
            check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_jdbcurl": cluster_jdbcurl,
            "data_table_name": data_table_name,
            "password": password,
            "role_arn": role_arn,
            "username": username,
        }
        if cloudwatch_logging_options is not None:
            self._values["cloudwatch_logging_options"] = cloudwatch_logging_options
        if copy_options is not None:
            self._values["copy_options"] = copy_options
        if data_table_columns is not None:
            self._values["data_table_columns"] = data_table_columns
        if processing_configuration is not None:
            self._values["processing_configuration"] = processing_configuration
        if retry_duration is not None:
            self._values["retry_duration"] = retry_duration
        if s3_backup_configuration is not None:
            self._values["s3_backup_configuration"] = s3_backup_configuration
        if s3_backup_mode is not None:
            self._values["s3_backup_mode"] = s3_backup_mode

    @builtins.property
    def cluster_jdbcurl(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cluster_jdbcurl KinesisFirehoseDeliveryStream#cluster_jdbcurl}.'''
        result = self._values.get("cluster_jdbcurl")
        assert result is not None, "Required property 'cluster_jdbcurl' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#data_table_name KinesisFirehoseDeliveryStream#data_table_name}.'''
        result = self._values.get("data_table_name")
        assert result is not None, "Required property 'data_table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#password KinesisFirehoseDeliveryStream#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#username KinesisFirehoseDeliveryStream#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwatch_logging_options(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions"]:
        '''cloudwatch_logging_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        '''
        result = self._values.get("cloudwatch_logging_options")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions"], result)

    @builtins.property
    def copy_options(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#copy_options KinesisFirehoseDeliveryStream#copy_options}.'''
        result = self._values.get("copy_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_table_columns(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#data_table_columns KinesisFirehoseDeliveryStream#data_table_columns}.'''
        result = self._values.get("data_table_columns")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processing_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration"]:
        '''processing_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        '''
        result = self._values.get("processing_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration"], result)

    @builtins.property
    def retry_duration(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.'''
        result = self._values.get("retry_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def s3_backup_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration"]:
        '''s3_backup_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_configuration KinesisFirehoseDeliveryStream#s3_backup_configuration}
        '''
        result = self._values.get("s3_backup_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration"], result)

    @builtins.property
    def s3_backup_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.'''
        result = self._values.get("s3_backup_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamRedshiftConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad0395a60a44cb9ac26cff1563c9ed6d6ba75d5686cee4853155fef3e69d216)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195f2f6fa843e59829574f048726a691a555a8a69802f8b9aafef15cb8e87b34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8bec4f3b33448db6a81f77a66aa1620a82a02e7b24510a8e954fa92d1b8d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bdd4b9b31ada5ff360dfa975e3cf692770a076dbf4fd2d14f50c3e3f40842d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c7f3cc39dbab6d5295f9d47376ae481be7f0874ec6c4689297f96a30e6f872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b1726c9a8f648e5f6ed45bd9d51a2aa17432b745d93675eb9bc55648e19f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamRedshiftConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00867147521939d0b351128e420c416ef84664a90a48b743ef76c722ab76b618)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLoggingOptions")
    def put_cloudwatch_logging_options(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        value = KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions(
            enabled=enabled,
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingOptions", [value]))

    @jsii.member(jsii_name="putProcessingConfiguration")
    def put_processing_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param processors: processors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        value = KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration(
            enabled=enabled, processors=processors
        )

        return typing.cast(None, jsii.invoke(self, "putProcessingConfiguration", [value]))

    @jsii.member(jsii_name="putS3BackupConfiguration")
    def put_s3_backup_configuration(
        self,
        *,
        bucket_arn: builtins.str,
        role_arn: builtins.str,
        buffer_interval: typing.Optional[jsii.Number] = None,
        buffer_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_format: typing.Optional[builtins.str] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param buffer_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.
        :param buffer_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param compression_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.
        :param error_output_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.
        '''
        value = KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration(
            bucket_arn=bucket_arn,
            role_arn=role_arn,
            buffer_interval=buffer_interval,
            buffer_size=buffer_size,
            cloudwatch_logging_options=cloudwatch_logging_options,
            compression_format=compression_format,
            error_output_prefix=error_output_prefix,
            kms_key_arn=kms_key_arn,
            prefix=prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putS3BackupConfiguration", [value]))

    @jsii.member(jsii_name="resetCloudwatchLoggingOptions")
    def reset_cloudwatch_logging_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingOptions", []))

    @jsii.member(jsii_name="resetCopyOptions")
    def reset_copy_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyOptions", []))

    @jsii.member(jsii_name="resetDataTableColumns")
    def reset_data_table_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataTableColumns", []))

    @jsii.member(jsii_name="resetProcessingConfiguration")
    def reset_processing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessingConfiguration", []))

    @jsii.member(jsii_name="resetRetryDuration")
    def reset_retry_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryDuration", []))

    @jsii.member(jsii_name="resetS3BackupConfiguration")
    def reset_s3_backup_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BackupConfiguration", []))

    @jsii.member(jsii_name="resetS3BackupMode")
    def reset_s3_backup_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BackupMode", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptions")
    def cloudwatch_logging_options(
        self,
    ) -> KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptionsOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptionsOutputReference, jsii.get(self, "cloudwatchLoggingOptions"))

    @builtins.property
    @jsii.member(jsii_name="processingConfiguration")
    def processing_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationOutputReference", jsii.get(self, "processingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3BackupConfiguration")
    def s3_backup_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationOutputReference", jsii.get(self, "s3BackupConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptionsInput")
    def cloudwatch_logging_options_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions], jsii.get(self, "cloudwatchLoggingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterJdbcurlInput")
    def cluster_jdbcurl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterJdbcurlInput"))

    @builtins.property
    @jsii.member(jsii_name="copyOptionsInput")
    def copy_options_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "copyOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTableColumnsInput")
    def data_table_columns_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTableColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTableNameInput")
    def data_table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="processingConfigurationInput")
    def processing_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration"], jsii.get(self, "processingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="retryDurationInput")
    def retry_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BackupConfigurationInput")
    def s3_backup_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration"], jsii.get(self, "s3BackupConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BackupModeInput")
    def s3_backup_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BackupModeInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterJdbcurl")
    def cluster_jdbcurl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterJdbcurl"))

    @cluster_jdbcurl.setter
    def cluster_jdbcurl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2afd6b2952dac277e9f0c1564f9bc4465aa22646e4d72055c62b0f198c7773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterJdbcurl", value)

    @builtins.property
    @jsii.member(jsii_name="copyOptions")
    def copy_options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copyOptions"))

    @copy_options.setter
    def copy_options(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52859c72a8200de6173fdea6f6968c89177428c738eb9e1ad18b60f1e26aec69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyOptions", value)

    @builtins.property
    @jsii.member(jsii_name="dataTableColumns")
    def data_table_columns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataTableColumns"))

    @data_table_columns.setter
    def data_table_columns(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1359d7a178edc95fcea97d8e0e22db5691276e821aabc3658af92e83c5570957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataTableColumns", value)

    @builtins.property
    @jsii.member(jsii_name="dataTableName")
    def data_table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataTableName"))

    @data_table_name.setter
    def data_table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10650f9d44eb2fbfa98ac50d07c434554b56e13d45455d78ab5388b7ab87ebae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataTableName", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35717a9df1e12f700b5f7d1fa992b93b927f70170a11413bb74f38995551a2fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="retryDuration")
    def retry_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryDuration"))

    @retry_duration.setter
    def retry_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c7a8cfdf053fb7fbad63e33e6571e2c3fed2a2ddb462eae68ac0464e2361c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryDuration", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b9fc4910242f39c485c8facdd77b1507ab389ae899c2cfef265f66fafeb32d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="s3BackupMode")
    def s3_backup_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BackupMode"))

    @s3_backup_mode.setter
    def s3_backup_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f542dc454e6944293857c5314928f9e9f0a883a6727447dad7b94ad618ea5be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BackupMode", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cef0c0dccdd9ea6a84a25ce9ca856d76c846df3422c95be9700d204bee7139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f078eb41b46440789a880d68900ec440d03936914bff0056329f40c355efffe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "processors": "processors"},
)
class KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param processors: processors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b9fc926a4d9643a40b455f0853cdc215cfcf6146fc34d538448990177c049c3)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if processors is not None:
            self._values["processors"] = processors

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def processors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors"]]]:
        '''processors block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        result = self._values.get("processors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4861e9b05115171bc9cd07b744153922b0a0a2c87bad2b780a569ac159686f83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProcessors")
    def put_processors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f583430e26de08da86d774a77e5f3479d67ca277e9a72f01e4cebd1ac2ff458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProcessors", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetProcessors")
    def reset_processors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessors", []))

    @builtins.property
    @jsii.member(jsii_name="processors")
    def processors(
        self,
    ) -> "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsList":
        return typing.cast("KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsList", jsii.get(self, "processors"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="processorsInput")
    def processors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors"]]], jsii.get(self, "processorsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ddaf659e8acab4c09c5e9eead4c951e2384eb7011127bf38a64463e8a37449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1fbc1e74aff8ade34e2cc754019fc635a950e472414701227e67e8b724972a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "parameters": "parameters"},
)
class KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors:
    def __init__(
        self,
        *,
        type: builtins.str,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type KinesisFirehoseDeliveryStream#type}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameters KinesisFirehoseDeliveryStream#parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837fecdeb27cfcd97f17d8780fc0f1ef2d2bf8aa0dbf5d585a2158846afb645e)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type KinesisFirehoseDeliveryStream#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters"]]]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameters KinesisFirehoseDeliveryStream#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a97a63248bae6ed48d923de7256d72fe754328b5263fe388a2f3944f9822be37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e94bec23373c668066b0f6988ff119d2a0259ea968fa91a4a82a2637f4ebce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c1bdfc3d96952252ef0e3d90a9eac9af96e7279b47e10485c959f486e58292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca89df8210939359fa933a27ae7747abd2b0b3b8c143b365875b68ef30f09eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aeb2cb61425768d6a1bce2a5936bff1357de7cf06bc668f9409e31ba0322856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f439c48afa7142e9f4109b5e53ab1c49a67e0a822df4230262e43103abe0a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262ed6c8f0366601b682b7b472bccecf624558fe1122fe31c1bfde9b58f7d7d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a684c9aa96f793d430afca035a1339c07eeb34e1b4b235e3266adb42b6431d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParametersList":
        return typing.cast("KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters"]]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90c74955a2193a3d126b68bcb798db1e2eee010e07b208f114109e2948d23e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8da2799bc40c7cbf049aa9f0506d7441a649db06c80dcc3403218f24c0e7e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_name": "parameterName",
        "parameter_value": "parameterValue",
    },
)
class KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters:
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        parameter_value: builtins.str,
    ) -> None:
        '''
        :param parameter_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_name KinesisFirehoseDeliveryStream#parameter_name}.
        :param parameter_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_value KinesisFirehoseDeliveryStream#parameter_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9526b521f1d5128d2a99bf45404cf3491a821235739e9e9bb0c96d1688fa9c)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter_name": parameter_name,
            "parameter_value": parameter_value,
        }

    @builtins.property
    def parameter_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_name KinesisFirehoseDeliveryStream#parameter_name}.'''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_value KinesisFirehoseDeliveryStream#parameter_value}.'''
        result = self._values.get("parameter_value")
        assert result is not None, "Required property 'parameter_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParametersList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cef3f866c4ed24cb23a35e83310d24611a19ca0c5959c5eb3d257e9e8e7767)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d35dd264da21ff44d311abe0733d736efb3fb9b31e11e1d5e958b468598c8f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b6de82efa42c264e7f991534c180c781fc049c07eb834b44851dc1ec5bfddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387842b8493e304976ae6b83d2bc0017a5e459c67273ec2e2683ecc749fa613b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3390a24a6f6b71d109b1ea3ca88ed9451ddbd9a70d354930e5616d1a8cecc4ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5348011f08f43dc5401a7932de362c45ea57e34ce394e81923d87148cd2f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParametersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2dbf4185641505c3c9557538116fd1c4df0ccdf4d7bb78507551242204884a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="parameterNameInput")
    def parameter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterValueInput")
    def parameter_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterValueInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterName"))

    @parameter_name.setter
    def parameter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a067fd7d06a8cd8d4d772cef3057aff566d02fbb8c2327b2bea64e5f2dbc5bb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterName", value)

    @builtins.property
    @jsii.member(jsii_name="parameterValue")
    def parameter_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterValue"))

    @parameter_value.setter
    def parameter_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84604f34a6754da082b6a84fbbc532913940a1e442fb5855143c74eec19ce953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a8c6939d6ece493e17a1699319173da6fdb0a597d65d1478c34aa505e81a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "role_arn": "roleArn",
        "buffer_interval": "bufferInterval",
        "buffer_size": "bufferSize",
        "cloudwatch_logging_options": "cloudwatchLoggingOptions",
        "compression_format": "compressionFormat",
        "error_output_prefix": "errorOutputPrefix",
        "kms_key_arn": "kmsKeyArn",
        "prefix": "prefix",
    },
)
class KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        role_arn: builtins.str,
        buffer_interval: typing.Optional[jsii.Number] = None,
        buffer_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_format: typing.Optional[builtins.str] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param buffer_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.
        :param buffer_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param compression_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.
        :param error_output_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.
        '''
        if isinstance(cloudwatch_logging_options, dict):
            cloudwatch_logging_options = KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions(**cloudwatch_logging_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__920ac070e2943e17bdd239eb1f163936200f454c083920af41c694625d63080d)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument buffer_interval", value=buffer_interval, expected_type=type_hints["buffer_interval"])
            check_type(argname="argument buffer_size", value=buffer_size, expected_type=type_hints["buffer_size"])
            check_type(argname="argument cloudwatch_logging_options", value=cloudwatch_logging_options, expected_type=type_hints["cloudwatch_logging_options"])
            check_type(argname="argument compression_format", value=compression_format, expected_type=type_hints["compression_format"])
            check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "role_arn": role_arn,
        }
        if buffer_interval is not None:
            self._values["buffer_interval"] = buffer_interval
        if buffer_size is not None:
            self._values["buffer_size"] = buffer_size
        if cloudwatch_logging_options is not None:
            self._values["cloudwatch_logging_options"] = cloudwatch_logging_options
        if compression_format is not None:
            self._values["compression_format"] = compression_format
        if error_output_prefix is not None:
            self._values["error_output_prefix"] = error_output_prefix
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def buffer_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.'''
        result = self._values.get("buffer_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def buffer_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.'''
        result = self._values.get("buffer_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cloudwatch_logging_options(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions"]:
        '''cloudwatch_logging_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        '''
        result = self._values.get("cloudwatch_logging_options")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions"], result)

    @builtins.property
    def compression_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.'''
        result = self._values.get("compression_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_output_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.'''
        result = self._values.get("error_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e772db66a08ed9cd070345953a3933246c87b81aaaeff583bb2c252863e7225)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8cb7676b4e74dc09275a926fb66d4114db573d46807a621d703afe1a27d29c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09508b0672fa2e3892b83cfb25997e16b24695c5b83888690403275656c942a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867d72ea30c25ad794f29ae48c54425eac144fb02e47e06e3d09062410185de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236db44a85168698c3774894c116e491c9753cc6bf4d75524ad41d8a93afa387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b268c2126e68bc086b1cc7e59939912caa32dc75f66a33727fc313c108489ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c31958496faec3ce582eabaa65dd11167a90f223394287956aa4f5f41955f9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLoggingOptions")
    def put_cloudwatch_logging_options(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        value = KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions(
            enabled=enabled,
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingOptions", [value]))

    @jsii.member(jsii_name="resetBufferInterval")
    def reset_buffer_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferInterval", []))

    @jsii.member(jsii_name="resetBufferSize")
    def reset_buffer_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferSize", []))

    @jsii.member(jsii_name="resetCloudwatchLoggingOptions")
    def reset_cloudwatch_logging_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingOptions", []))

    @jsii.member(jsii_name="resetCompressionFormat")
    def reset_compression_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionFormat", []))

    @jsii.member(jsii_name="resetErrorOutputPrefix")
    def reset_error_output_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOutputPrefix", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptions")
    def cloudwatch_logging_options(
        self,
    ) -> KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptionsOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptionsOutputReference, jsii.get(self, "cloudwatchLoggingOptions"))

    @builtins.property
    @jsii.member(jsii_name="bucketArnInput")
    def bucket_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferIntervalInput")
    def buffer_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferSizeInput")
    def buffer_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptionsInput")
    def cloudwatch_logging_options_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions], jsii.get(self, "cloudwatchLoggingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionFormatInput")
    def compression_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="errorOutputPrefixInput")
    def error_output_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorOutputPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @bucket_arn.setter
    def bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f418f387ba509d41754828bbf5fb6b5ed932d37ae992e24fc92cebaa25cf5f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketArn", value)

    @builtins.property
    @jsii.member(jsii_name="bufferInterval")
    def buffer_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferInterval"))

    @buffer_interval.setter
    def buffer_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc73144cf0a41f21e6da4f8468bf9284c84357c473dfc48d3d0c2b422ecac80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferInterval", value)

    @builtins.property
    @jsii.member(jsii_name="bufferSize")
    def buffer_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferSize"))

    @buffer_size.setter
    def buffer_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a06804d7e654677f29e4b8d6265696d468480a1b15035599a44f7f0ee1e91b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferSize", value)

    @builtins.property
    @jsii.member(jsii_name="compressionFormat")
    def compression_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionFormat"))

    @compression_format.setter
    def compression_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4786f71dc572eedf4c574c3cb49957a40bc79c3504d466f3ea4c420649de7616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionFormat", value)

    @builtins.property
    @jsii.member(jsii_name="errorOutputPrefix")
    def error_output_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorOutputPrefix"))

    @error_output_prefix.setter
    def error_output_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0279fa76fb860005f6b376754abaf728b6a95d743cd8138201c89c410656558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOutputPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153ed85e2d4b0d1b79ef687f188275215f912a800822440ee048688c9a067243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d457c9ca46695deeea522c7f09e2bb6ea6f0e04582c15c9bcc66f3b6e0af8696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44ee511eb190c35bcbb066b1cced19aa45f9ee6120d8e4897d7cc386afd5408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b5122458f909f30f372a6d016e72b211e0744f736634c37d2e50e13091f400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamS3Configuration",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "role_arn": "roleArn",
        "buffer_interval": "bufferInterval",
        "buffer_size": "bufferSize",
        "cloudwatch_logging_options": "cloudwatchLoggingOptions",
        "compression_format": "compressionFormat",
        "error_output_prefix": "errorOutputPrefix",
        "kms_key_arn": "kmsKeyArn",
        "prefix": "prefix",
    },
)
class KinesisFirehoseDeliveryStreamS3Configuration:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        role_arn: builtins.str,
        buffer_interval: typing.Optional[jsii.Number] = None,
        buffer_size: typing.Optional[jsii.Number] = None,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression_format: typing.Optional[builtins.str] = None,
        error_output_prefix: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.
        :param buffer_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.
        :param buffer_size: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param compression_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.
        :param error_output_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.
        '''
        if isinstance(cloudwatch_logging_options, dict):
            cloudwatch_logging_options = KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions(**cloudwatch_logging_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0408ee6e6b97447f2f1132f2029bac5c79ef06e29f386a8e1d78fa767d666dd1)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument buffer_interval", value=buffer_interval, expected_type=type_hints["buffer_interval"])
            check_type(argname="argument buffer_size", value=buffer_size, expected_type=type_hints["buffer_size"])
            check_type(argname="argument cloudwatch_logging_options", value=cloudwatch_logging_options, expected_type=type_hints["cloudwatch_logging_options"])
            check_type(argname="argument compression_format", value=compression_format, expected_type=type_hints["compression_format"])
            check_type(argname="argument error_output_prefix", value=error_output_prefix, expected_type=type_hints["error_output_prefix"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "role_arn": role_arn,
        }
        if buffer_interval is not None:
            self._values["buffer_interval"] = buffer_interval
        if buffer_size is not None:
            self._values["buffer_size"] = buffer_size
        if cloudwatch_logging_options is not None:
            self._values["cloudwatch_logging_options"] = cloudwatch_logging_options
        if compression_format is not None:
            self._values["compression_format"] = compression_format
        if error_output_prefix is not None:
            self._values["error_output_prefix"] = error_output_prefix
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#bucket_arn KinesisFirehoseDeliveryStream#bucket_arn}.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#role_arn KinesisFirehoseDeliveryStream#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def buffer_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_interval KinesisFirehoseDeliveryStream#buffer_interval}.'''
        result = self._values.get("buffer_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def buffer_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#buffer_size KinesisFirehoseDeliveryStream#buffer_size}.'''
        result = self._values.get("buffer_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cloudwatch_logging_options(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions"]:
        '''cloudwatch_logging_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        '''
        result = self._values.get("cloudwatch_logging_options")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions"], result)

    @builtins.property
    def compression_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#compression_format KinesisFirehoseDeliveryStream#compression_format}.'''
        result = self._values.get("compression_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_output_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#error_output_prefix KinesisFirehoseDeliveryStream#error_output_prefix}.'''
        result = self._values.get("error_output_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#kms_key_arn KinesisFirehoseDeliveryStream#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#prefix KinesisFirehoseDeliveryStream#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamS3Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3779e815fe3b2c543558ee95d579ebb0f705ee99b5b001c3cdfd0ad238e7082)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ded24101297aeb625ab01541c93f2b4ba0f4297297688cd05a36da7a2c06235)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb73fa49cd754427b81e551284a4403423fda1227931a92adfe4755b0872c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b862d43ac8690389234a5b1fa494bbbce155bd817732ea13de720a87148a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7daa2301c47fa37c45de007ec87484e028ec1fccd1368399e432110435ddfb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3831f97a2d3a07ed582333ea3ddc22756e7c69dbf85a1e068cbb28abf671e515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamS3ConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamS3ConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4c47793765944c2be616fa55bfa879fc17ba8bbe32924233c245c1fabaf517)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLoggingOptions")
    def put_cloudwatch_logging_options(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        value = KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions(
            enabled=enabled,
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingOptions", [value]))

    @jsii.member(jsii_name="resetBufferInterval")
    def reset_buffer_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferInterval", []))

    @jsii.member(jsii_name="resetBufferSize")
    def reset_buffer_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBufferSize", []))

    @jsii.member(jsii_name="resetCloudwatchLoggingOptions")
    def reset_cloudwatch_logging_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingOptions", []))

    @jsii.member(jsii_name="resetCompressionFormat")
    def reset_compression_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionFormat", []))

    @jsii.member(jsii_name="resetErrorOutputPrefix")
    def reset_error_output_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOutputPrefix", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptions")
    def cloudwatch_logging_options(
        self,
    ) -> KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptionsOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptionsOutputReference, jsii.get(self, "cloudwatchLoggingOptions"))

    @builtins.property
    @jsii.member(jsii_name="bucketArnInput")
    def bucket_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferIntervalInput")
    def buffer_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferSizeInput")
    def buffer_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptionsInput")
    def cloudwatch_logging_options_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions], jsii.get(self, "cloudwatchLoggingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionFormatInput")
    def compression_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="errorOutputPrefixInput")
    def error_output_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorOutputPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @bucket_arn.setter
    def bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b1a424fa74f3e46f74caf9be00fcf0c13a9bba736b3d9cb22cefb78b8bc42f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketArn", value)

    @builtins.property
    @jsii.member(jsii_name="bufferInterval")
    def buffer_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferInterval"))

    @buffer_interval.setter
    def buffer_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd52422a904fee7c623d6aa981d99dc8907098baf3148d75fddad6fd69b21128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferInterval", value)

    @builtins.property
    @jsii.member(jsii_name="bufferSize")
    def buffer_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferSize"))

    @buffer_size.setter
    def buffer_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35e864ea13e639f0b1c377a68c51837508e31b94ede92d54e2f27cc30e3b443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferSize", value)

    @builtins.property
    @jsii.member(jsii_name="compressionFormat")
    def compression_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionFormat"))

    @compression_format.setter
    def compression_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053a3a89206e86e1665e12a6d0e486ec665000188875f87b9a381937481bfe96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionFormat", value)

    @builtins.property
    @jsii.member(jsii_name="errorOutputPrefix")
    def error_output_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorOutputPrefix"))

    @error_output_prefix.setter
    def error_output_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f44cb9b19f7e3905bf4d8bb01385ab99281203e648c892b40228530fd458358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOutputPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07969a3ef33cb12e9eaa6aa8af5e4536a20ba21b3860916e026ed37ca8a137b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889edfdb7b97700e7c0fdedfc747cc4b7f0fbc941e8127b17fe4ee7eceb3daa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ddb6293c9498149ccf29ca119063a617fe24b837f15592689331e13d52eabe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamS3Configuration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamS3Configuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamS3Configuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b27484e5854439638e1d460560e2c4e5ea73c3456e30a016ae99182a4a167e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamServerSideEncryption",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "key_arn": "keyArn", "key_type": "keyType"},
)
class KinesisFirehoseDeliveryStreamServerSideEncryption:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_arn: typing.Optional[builtins.str] = None,
        key_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#key_arn KinesisFirehoseDeliveryStream#key_arn}.
        :param key_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#key_type KinesisFirehoseDeliveryStream#key_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1bfaf8e5fcf63ea5e1de1eb395bcd32d26f33d582130b9ff49abd4260c1030)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
            check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if key_arn is not None:
            self._values["key_arn"] = key_arn
        if key_type is not None:
            self._values["key_type"] = key_type

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#key_arn KinesisFirehoseDeliveryStream#key_arn}.'''
        result = self._values.get("key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#key_type KinesisFirehoseDeliveryStream#key_type}.'''
        result = self._values.get("key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamServerSideEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamServerSideEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamServerSideEncryptionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123ba4bbd9240f864ddf45ddd5cf3cc26df68623dd5c01bd8ba440f0c76bba3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetKeyArn")
    def reset_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyArn", []))

    @jsii.member(jsii_name="resetKeyType")
    def reset_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyType", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="keyArnInput")
    def key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="keyTypeInput")
    def key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5131b2585024b55d069acb69aff58a6d00e91e10ead2b9e419ccec83b6ba77b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyArn"))

    @key_arn.setter
    def key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0203c27e3352f8e97bc38bf21c5c47d69b2fa1e6a37eecc3368e74c66a8bf9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyArn", value)

    @builtins.property
    @jsii.member(jsii_name="keyType")
    def key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyType"))

    @key_type.setter
    def key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4ed1bca1176e22fdb80ec74eb6dcc2a37a4a4e9ed67f9d0b77d28a22b28008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamServerSideEncryption]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamServerSideEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamServerSideEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49deb60f22347c756905a1058ee94e5b216d1966363e19fccb8d675d04d39792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "hec_endpoint": "hecEndpoint",
        "hec_token": "hecToken",
        "cloudwatch_logging_options": "cloudwatchLoggingOptions",
        "hec_acknowledgment_timeout": "hecAcknowledgmentTimeout",
        "hec_endpoint_type": "hecEndpointType",
        "processing_configuration": "processingConfiguration",
        "retry_duration": "retryDuration",
        "s3_backup_mode": "s3BackupMode",
    },
)
class KinesisFirehoseDeliveryStreamSplunkConfiguration:
    def __init__(
        self,
        *,
        hec_endpoint: builtins.str,
        hec_token: builtins.str,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        hec_acknowledgment_timeout: typing.Optional[jsii.Number] = None,
        hec_endpoint_type: typing.Optional[builtins.str] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_duration: typing.Optional[jsii.Number] = None,
        s3_backup_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hec_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_endpoint KinesisFirehoseDeliveryStream#hec_endpoint}.
        :param hec_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_token KinesisFirehoseDeliveryStream#hec_token}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        :param hec_acknowledgment_timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_acknowledgment_timeout KinesisFirehoseDeliveryStream#hec_acknowledgment_timeout}.
        :param hec_endpoint_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_endpoint_type KinesisFirehoseDeliveryStream#hec_endpoint_type}.
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        :param retry_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.
        :param s3_backup_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.
        '''
        if isinstance(cloudwatch_logging_options, dict):
            cloudwatch_logging_options = KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions(**cloudwatch_logging_options)
        if isinstance(processing_configuration, dict):
            processing_configuration = KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration(**processing_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8077da78b1628abc9a9ac2254a1b0b92b91425fee0ba3edc4ec0db346a92ee7d)
            check_type(argname="argument hec_endpoint", value=hec_endpoint, expected_type=type_hints["hec_endpoint"])
            check_type(argname="argument hec_token", value=hec_token, expected_type=type_hints["hec_token"])
            check_type(argname="argument cloudwatch_logging_options", value=cloudwatch_logging_options, expected_type=type_hints["cloudwatch_logging_options"])
            check_type(argname="argument hec_acknowledgment_timeout", value=hec_acknowledgment_timeout, expected_type=type_hints["hec_acknowledgment_timeout"])
            check_type(argname="argument hec_endpoint_type", value=hec_endpoint_type, expected_type=type_hints["hec_endpoint_type"])
            check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
            check_type(argname="argument retry_duration", value=retry_duration, expected_type=type_hints["retry_duration"])
            check_type(argname="argument s3_backup_mode", value=s3_backup_mode, expected_type=type_hints["s3_backup_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hec_endpoint": hec_endpoint,
            "hec_token": hec_token,
        }
        if cloudwatch_logging_options is not None:
            self._values["cloudwatch_logging_options"] = cloudwatch_logging_options
        if hec_acknowledgment_timeout is not None:
            self._values["hec_acknowledgment_timeout"] = hec_acknowledgment_timeout
        if hec_endpoint_type is not None:
            self._values["hec_endpoint_type"] = hec_endpoint_type
        if processing_configuration is not None:
            self._values["processing_configuration"] = processing_configuration
        if retry_duration is not None:
            self._values["retry_duration"] = retry_duration
        if s3_backup_mode is not None:
            self._values["s3_backup_mode"] = s3_backup_mode

    @builtins.property
    def hec_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_endpoint KinesisFirehoseDeliveryStream#hec_endpoint}.'''
        result = self._values.get("hec_endpoint")
        assert result is not None, "Required property 'hec_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hec_token(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_token KinesisFirehoseDeliveryStream#hec_token}.'''
        result = self._values.get("hec_token")
        assert result is not None, "Required property 'hec_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwatch_logging_options(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions"]:
        '''cloudwatch_logging_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#cloudwatch_logging_options KinesisFirehoseDeliveryStream#cloudwatch_logging_options}
        '''
        result = self._values.get("cloudwatch_logging_options")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions"], result)

    @builtins.property
    def hec_acknowledgment_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_acknowledgment_timeout KinesisFirehoseDeliveryStream#hec_acknowledgment_timeout}.'''
        result = self._values.get("hec_acknowledgment_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hec_endpoint_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#hec_endpoint_type KinesisFirehoseDeliveryStream#hec_endpoint_type}.'''
        result = self._values.get("hec_endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processing_configuration(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration"]:
        '''processing_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processing_configuration KinesisFirehoseDeliveryStream#processing_configuration}
        '''
        result = self._values.get("processing_configuration")
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration"], result)

    @builtins.property
    def retry_duration(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#retry_duration KinesisFirehoseDeliveryStream#retry_duration}.'''
        result = self._values.get("retry_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def s3_backup_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#s3_backup_mode KinesisFirehoseDeliveryStream#s3_backup_mode}.'''
        result = self._values.get("s3_backup_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamSplunkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd33b3ac115279dad091a28eecbba09f4d2b65586835f3de0fc202cde8bdfaa)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.'''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b8ad102b2c94c74d04ee51b33ba488af85a4ab146d0c23975e4f4db5fa280b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogStreamName")
    def reset_log_stream_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamName", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNameInput")
    def log_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec89cc14f6f4e35f524ec2f5c79d6bc6ab5d2339f96ee5231a1b6fdab24d70b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__379c2caba5b3a98323d9fc2384108c3957b923ea61af73afaad6292384ca661d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b6807a273c6968290f95bdf920fd6a3b574046eb3f78d39fac6e318c5e3649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__723137a9953e64a018b0bec51a67b643e0ee84b526a825198b1dcebccad18989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamSplunkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ab391a32976930c384d864f74c08838da916dd2bd92bfce8565375eb0426c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLoggingOptions")
    def put_cloudwatch_logging_options(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_group_name KinesisFirehoseDeliveryStream#log_group_name}.
        :param log_stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#log_stream_name KinesisFirehoseDeliveryStream#log_stream_name}.
        '''
        value = KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions(
            enabled=enabled,
            log_group_name=log_group_name,
            log_stream_name=log_stream_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingOptions", [value]))

    @jsii.member(jsii_name="putProcessingConfiguration")
    def put_processing_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param processors: processors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        value = KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration(
            enabled=enabled, processors=processors
        )

        return typing.cast(None, jsii.invoke(self, "putProcessingConfiguration", [value]))

    @jsii.member(jsii_name="resetCloudwatchLoggingOptions")
    def reset_cloudwatch_logging_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingOptions", []))

    @jsii.member(jsii_name="resetHecAcknowledgmentTimeout")
    def reset_hec_acknowledgment_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHecAcknowledgmentTimeout", []))

    @jsii.member(jsii_name="resetHecEndpointType")
    def reset_hec_endpoint_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHecEndpointType", []))

    @jsii.member(jsii_name="resetProcessingConfiguration")
    def reset_processing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessingConfiguration", []))

    @jsii.member(jsii_name="resetRetryDuration")
    def reset_retry_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryDuration", []))

    @jsii.member(jsii_name="resetS3BackupMode")
    def reset_s3_backup_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BackupMode", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptions")
    def cloudwatch_logging_options(
        self,
    ) -> KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptionsOutputReference:
        return typing.cast(KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptionsOutputReference, jsii.get(self, "cloudwatchLoggingOptions"))

    @builtins.property
    @jsii.member(jsii_name="processingConfiguration")
    def processing_configuration(
        self,
    ) -> "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationOutputReference":
        return typing.cast("KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationOutputReference", jsii.get(self, "processingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptionsInput")
    def cloudwatch_logging_options_input(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions], jsii.get(self, "cloudwatchLoggingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="hecAcknowledgmentTimeoutInput")
    def hec_acknowledgment_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hecAcknowledgmentTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="hecEndpointInput")
    def hec_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hecEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="hecEndpointTypeInput")
    def hec_endpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hecEndpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="hecTokenInput")
    def hec_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hecTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="processingConfigurationInput")
    def processing_configuration_input(
        self,
    ) -> typing.Optional["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration"]:
        return typing.cast(typing.Optional["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration"], jsii.get(self, "processingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="retryDurationInput")
    def retry_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BackupModeInput")
    def s3_backup_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BackupModeInput"))

    @builtins.property
    @jsii.member(jsii_name="hecAcknowledgmentTimeout")
    def hec_acknowledgment_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hecAcknowledgmentTimeout"))

    @hec_acknowledgment_timeout.setter
    def hec_acknowledgment_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4019b803bd9702961a60d0356882ca987952c15071688576a8a0952edf67af46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hecAcknowledgmentTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="hecEndpoint")
    def hec_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hecEndpoint"))

    @hec_endpoint.setter
    def hec_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0939813722a179aa5ccc26ec387a0923a23a03a33122a97788ab296484c4030b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hecEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="hecEndpointType")
    def hec_endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hecEndpointType"))

    @hec_endpoint_type.setter
    def hec_endpoint_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1dc4317071fa4bafd40c320350eeac41ffb7e2865e7829342b5a4674c92a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hecEndpointType", value)

    @builtins.property
    @jsii.member(jsii_name="hecToken")
    def hec_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hecToken"))

    @hec_token.setter
    def hec_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53fe9af74bfd37d75bcb44b55c710cbf4b73bb90cf7561e45443d846549fc2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hecToken", value)

    @builtins.property
    @jsii.member(jsii_name="retryDuration")
    def retry_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryDuration"))

    @retry_duration.setter
    def retry_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29852517b83cf31fa922256b6507053f4608a2241854d2489810adaaf81c9f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryDuration", value)

    @builtins.property
    @jsii.member(jsii_name="s3BackupMode")
    def s3_backup_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BackupMode"))

    @s3_backup_mode.setter
    def s3_backup_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e66ac9fff83b6b55ca1ef2af0f3d0ea61d68097d510e61b4bf81fb6ecd2be37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BackupMode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c12a24a192f7a221fdc43e7d4126288f06cba259b09abf20c04a5693713921f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "processors": "processors"},
)
class KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.
        :param processors: processors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43860ca298e581371f4041394fc6cad874d2534c48c330c4eedd2f162eea474d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if processors is not None:
            self._values["processors"] = processors

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#enabled KinesisFirehoseDeliveryStream#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def processors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors"]]]:
        '''processors block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#processors KinesisFirehoseDeliveryStream#processors}
        '''
        result = self._values.get("processors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71ace754f38df2a5ea95a29cf715c9504d420aaffe650f7ac62ec687303cb07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putProcessors")
    def put_processors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1104f6dce1c7ee944018827567e884d837096f26c141a4027a2eb0dbf880dd11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProcessors", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetProcessors")
    def reset_processors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessors", []))

    @builtins.property
    @jsii.member(jsii_name="processors")
    def processors(
        self,
    ) -> "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsList":
        return typing.cast("KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsList", jsii.get(self, "processors"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="processorsInput")
    def processors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors"]]], jsii.get(self, "processorsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a289e4d07ec67e598a9a641af17f34d0ed55ee47b21f88f5069e3fbf9a37e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration]:
        return typing.cast(typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__181bd8e135ca9038e859c67309ff7f7949388aac9e1a8f3bcdd627673740e661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "parameters": "parameters"},
)
class KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors:
    def __init__(
        self,
        *,
        type: builtins.str,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type KinesisFirehoseDeliveryStream#type}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameters KinesisFirehoseDeliveryStream#parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39ea866c8b026e19c7e592ca0db9d43e36ee4b342d876bfbdcc9fd1b53f31dfc)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#type KinesisFirehoseDeliveryStream#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters"]]]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameters KinesisFirehoseDeliveryStream#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244ca2d90d27d7fda0de239c0c8390aa5b727622734c4182c051487e714b15c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10430b50afe80cafb69fe9ab048076997044d3ca833f74227defd4929399613d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc433e6670917304d4e88e99bbb75bb5e7a72277ef122652f22e822ef989c569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d608c1360b081fbd25f0a2dc71d2ee63ac686e43a938d5e81639c422b81c23cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897c6d325766ccdbd0f77aab48fe9e018b7da9097dfeb85ff098c259d7870e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320fd3b082f7972cc7efc6d987f1032d6a8b99919aba8b402e88c509a4fb3fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__476e041bb5d499a9944811a6d1a43245b586044dea564902ad78957bb8715a5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b7c06bf601b7c77f1d9aca96adca660dd28aecf6a896304c209bce0830eab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParametersList":
        return typing.cast("KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters"]]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a8b94c2e4dab3ca993758a3e89a2465ef8fb7ef6bcdd6e604ed491222d0883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73b4b659ca7d818135774c3fa4f509ddb694ba85d7c24b4fa56c8cf6df2adc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_name": "parameterName",
        "parameter_value": "parameterValue",
    },
)
class KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters:
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        parameter_value: builtins.str,
    ) -> None:
        '''
        :param parameter_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_name KinesisFirehoseDeliveryStream#parameter_name}.
        :param parameter_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_value KinesisFirehoseDeliveryStream#parameter_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a555d69117299cc952ca17152e878579e8d163d823988d17b728343c9e75783c)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter_name": parameter_name,
            "parameter_value": parameter_value,
        }

    @builtins.property
    def parameter_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_name KinesisFirehoseDeliveryStream#parameter_name}.'''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/kinesis_firehose_delivery_stream#parameter_value KinesisFirehoseDeliveryStream#parameter_value}.'''
        result = self._values.get("parameter_value")
        assert result is not None, "Required property 'parameter_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParametersList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765751b10ae0efda28f3059fb2ea23b03044505581886075d09fbf0cb755c705)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010ba0fc40cab47ecf8aa4ef7ea7cdf9cb981a4c1c742feecf53f9fcd4134c7b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591d7ba9c1235b608a74e10f5727b294c030f42e3a8abe0a5c0901e685c7998e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f7b7bf1cf772550e8ce47399da52390a477c113b57cf400656005d6fcf4267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c371edb77b37220b5c4ece30dcc4718dd3677ff98536c4f836ca5754a1a61862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e51f4ed60e452777964501d8b5a16d9352677908ee030569c67ca14e9eef2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kinesisFirehoseDeliveryStream.KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParametersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bfd23f92b7d63722dac6e255e9d59cfe1d588068dc040c68e82adb30474d8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="parameterNameInput")
    def parameter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterValueInput")
    def parameter_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterValueInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterName"))

    @parameter_name.setter
    def parameter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f459ea134e76727b19707f551c9a48428835c2096ce41f6384577559f17a4fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterName", value)

    @builtins.property
    @jsii.member(jsii_name="parameterValue")
    def parameter_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterValue"))

    @parameter_value.setter
    def parameter_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ca814d6bde2dd4aedffe8d0da5b9d96b37b88ee8aa3ba347070cef41e457df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef95976f644ef3e7255f0ecbe5777e5da027a520b024d733a80a7295402f712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "KinesisFirehoseDeliveryStream",
    "KinesisFirehoseDeliveryStreamConfig",
    "KinesisFirehoseDeliveryStreamElasticsearchConfiguration",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptionsOutputReference",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsList",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsOutputReference",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParametersList",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParametersOutputReference",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig",
    "KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfigOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3Configuration",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptionsOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDeOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDeOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDeOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDeOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsList",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParametersList",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParametersOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptionsOutputReference",
    "KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfiguration",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptionsOutputReference",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsList",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsOutputReference",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParametersList",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParametersOutputReference",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributesList",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributesOutputReference",
    "KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamKinesisSourceConfiguration",
    "KinesisFirehoseDeliveryStreamKinesisSourceConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamRedshiftConfiguration",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptionsOutputReference",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsList",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsOutputReference",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParametersList",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParametersOutputReference",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptionsOutputReference",
    "KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamS3Configuration",
    "KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions",
    "KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptionsOutputReference",
    "KinesisFirehoseDeliveryStreamS3ConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamServerSideEncryption",
    "KinesisFirehoseDeliveryStreamServerSideEncryptionOutputReference",
    "KinesisFirehoseDeliveryStreamSplunkConfiguration",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptionsOutputReference",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationOutputReference",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsList",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsOutputReference",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParametersList",
    "KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParametersOutputReference",
]

publication.publish()

def _typecheckingstub__0c84a08dbf9a56758729a4e9f505fc49a3af04c826ca89339f2cbbacef64da8d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination: builtins.str,
    name: builtins.str,
    arn: typing.Optional[builtins.str] = None,
    destination_id: typing.Optional[builtins.str] = None,
    elasticsearch_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    extended_s3_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3Configuration, typing.Dict[builtins.str, typing.Any]]] = None,
    http_endpoint_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kinesis_source_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamKinesisSourceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamS3Configuration, typing.Dict[builtins.str, typing.Any]]] = None,
    server_side_encryption: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamServerSideEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    splunk_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version_id: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8201ff2f513d08f18566df5558d8afaca3e6b4db6aa25a762b1bed6112c84d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877e27e61487773bbc33f661eb98222d5880d081a19eace08e1a3c45fff9eb9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f364be141796cddf9ae0d9359b8120617a1af322bdce9c0de93b12b207c39a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c74f315910b3945d0e8182e866399c21cdd19a6b152767172135611c41700ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29b89adfd7340592015e8dc562d4e4d29568db58c6ced05595a20734f2cb7bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4230c987497fa60348e73d8c266cf3326cace333f00c17e3984d07b14f594cac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fbddf32b5fc27bd30f119ff02a4c9c09c2679dc307e0f92c8ea22c5f6fc19c7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e53441beca05381b91046524e107600bb8149201dad06e1fd2ebf90760d8aaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2848a7d0b903f54cc81b571a9272298c8f5c4bad6e8558b19eca1b2f357d1e9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination: builtins.str,
    name: builtins.str,
    arn: typing.Optional[builtins.str] = None,
    destination_id: typing.Optional[builtins.str] = None,
    elasticsearch_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    extended_s3_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3Configuration, typing.Dict[builtins.str, typing.Any]]] = None,
    http_endpoint_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kinesis_source_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamKinesisSourceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamS3Configuration, typing.Dict[builtins.str, typing.Any]]] = None,
    server_side_encryption: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamServerSideEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    splunk_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e5d53e8a1149b73bb7a34aca6da0238e3887c8eaa251fca73adc908b6f9209(
    *,
    index_name: builtins.str,
    role_arn: builtins.str,
    buffering_interval: typing.Optional[jsii.Number] = None,
    buffering_size: typing.Optional[jsii.Number] = None,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_endpoint: typing.Optional[builtins.str] = None,
    domain_arn: typing.Optional[builtins.str] = None,
    index_rotation_period: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_duration: typing.Optional[jsii.Number] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
    type_name: typing.Optional[builtins.str] = None,
    vpc_config: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92db2547d24288a6d32b4839d0d6b1f758cf47e8a1271ef7ebd1d76ceba10adb(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b8a714a86b5890e0f374d1eb78db073ce3368b1bf98adac13e43ad08b7f3ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba4e5ba4f13096ea96d1c7a1e9b7f296093eeb08538a7ad49aec743f664ec30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3de549d64d55857ef4958058b3f2105ab4228a1eb3f6cf273435365f8e10b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724d208f17efa6ec8fb38c89dd13a3f38af5998df3a2594abafa69570afdbd17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22605ad780fbc318dc0a0782e97e0f143ca2e79dbf38dd620f160a921f8f61bc(
    value: typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationCloudwatchLoggingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61aea174db8e641acbc05de63eae211f433ab788e2fdb73bb43e25612ca759fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f14c044f69d1e9dc442a2e9a181f4bbadd2ec9b558068239a2e6dbd7d01e2470(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1f7e124358e8a67004b002cb48709357152af52b60805c531d9099ab005fe5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8079e97677b173a3a88baf0b06436465233da029c31b7abb96d9d2d7aeedfd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f12aec65273f448c1a226ce576688528532ccd82b10d1ce2922950b1442293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba30ee5c9434dc5e0e50187484726f791326ed1df9704efba18ff23d81d058b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe69bf6522a410c1486ae61ec710b45b97c7b71ab5a8d343f8b5dbc0e60e966(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c02fd5b69c2b931c61e0ad4a279834ac0b7e68e5fd9035f41aa4aed94a6d4c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f435c7a89f5c0e878715eb0c72021e1bf668ecd37f8dea2fb766dfe02e5f733(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bed0718d25dfa64cd15b696f55124b6f871b2b6e00084918637413b03a3491e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb8041f2ec1171d53b082cdde68f386f5ced9cfe84a77cde479f95e75ce7a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77165ef48a7bfbe87955e6830bd18106558b93667bc17e6c8f0042dbb6e8af93(
    value: typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1241c5658ea34c71d3427d1b7ae79ed9b508be04fbb962f9ff584d6a743fe4d(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebab5707568e759898a8bb1e55fda49e01d456f6736f257b949dbc4f4c813f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b78428d8d8b1e9d8750afb1939543da1e684d5a33840e27948ef5c772003054(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e546fd6c8c628fcbfee57db64c67514bf29f1519a123dd6b5e108672d5abeb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8148cad95c2366f996e44649a558665857a4bd671a92f65e24a4fe19961cb7d6(
    value: typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7186160cd0f4a6c9c1dd7c43efc8b00325374090a9699e123ae681f78961cac4(
    *,
    type: builtins.str,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc17e36ecf726ddf369197ee51e7a30815c15f792cc376cf7707f3614632dc4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c3d68194d8bf42c3df9202cfee8a01aa15e5b8a4850e5cd2a7d340300c95e1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1470366b8ff694b279004ec04278b6815d94161fd7bd8c8b3b1234a9de01a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2e226002c072b38dc451cae7db645611801ea0f4c630219578d1dcc49c79b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216cf9b4c19da6a814fe821fdc0426ffd0cf85ad2f0f6db61a9106b5462168a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d663a4e82d49d1e15809515411298ffb3ad61d27acd7e4bea7cd7bbef3dc6b5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29e12971f0d0eedf256272fb78b303ab1c269698df1ad3b22a4edaa5ed11d15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667169714862c29405734cd038125bad5c8eddfecf78e1b33e6fc95b5ee45bc7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056b0a2b9f32bea629a1fab4c660da0c4839952995a2b39eae06438fcc99cda9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc3778e2d4830e0e7cc7562f24c9eb7abd8b40c3d8285f058a6ec64924e08ba(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93218b79ba7709f0bc6ed837e92664eb73771a377c51fecea900f076b0f7edd9(
    *,
    parameter_name: builtins.str,
    parameter_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4180938c12da8256caa1cafa2fc90fce22286f2afd1e2796a7f3540b044f46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176fb4cbf6371d1227ae89079d6226a254a93fb905e23004a41c38aba45c8ac1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f81c3ce228a7a233f784677ff3681b439fb26e9daff9b2d5a9814aed739e98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b470ed7577e2f5834e9be96567bf5d97712a27fb101955f932788a8108b3886(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa7755d85033be6c7504c46b4c6827905cae9df8b28c5f4e1c85a254f9ab791(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f636568e769afa069ef7ceaaa0ac4fea5611692db07feb131ca9d8e5c839cd32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff04729ea1eec1227c5bec9a2bddb688456c761e0b0d4780283207afc9ab4d7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7728c836614e4dc40f05c62fecaf736328f4e4394ea55fb1ccaeb9221d6430eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e36426e81d9e9b78f83497e60bc4b6016d3b615ab85394a630ff43f7d2693e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98daf71b65dc12bb66354cbb583f3557d5907f7ee87be80fa91144bea86a6d28(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamElasticsearchConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f477819807f784be4a9fffd7d6dc2cee4d167e93fdf988c3743b3c46e10dafd3(
    *,
    role_arn: builtins.str,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3ece1ac4097116d3b7ed335d3e08657fcd34b5c6e7a2b85cf65dddab6beebb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67946a5efc7190039c1c45b19c5ea69cc3e67a2a4cdaaf432fce923d1e9fccc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d07d1ad2a5c43eabfe1c875573ae6195b535590dd2304d0d9a689e579ba533(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb293b55bb7692c95cb9a0e536fd2c4e150fbacb70e4742a916317497fb7e50c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e741ed0ab60fba0e5f1b6357e37e75d3310bc2cb797441ce2231488ec36c9631(
    value: typing.Optional[KinesisFirehoseDeliveryStreamElasticsearchConfigurationVpcConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd60f5bd69639f798ea3f5de680d6d0dbbd78a67566b2b6a093864b8214e70b(
    *,
    bucket_arn: builtins.str,
    role_arn: builtins.str,
    buffer_interval: typing.Optional[jsii.Number] = None,
    buffer_size: typing.Optional[jsii.Number] = None,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_format: typing.Optional[builtins.str] = None,
    data_format_conversion_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamic_partitioning_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    error_output_prefix: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_backup_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83c4356a3e6b6f2e1a3e79e43dcb6c292d8a4824512a9ed9b34ce067089e12b(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584e24e78e61847096b7a4f086fa293fabadd149c22b9f3d462dc3e567e5bc58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf866496d39160e71916811e708b3c392e7cf94831821104ddf75fc80e086ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909d07e7ef4d08866b4a4a740126a57898474e20f8ddc6544e62dcbffd939ab7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5783c290f4ddfbb376c8b879171b1f2d3c5f81aa276d7419f33fb6d173f1491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9d23a60c2ccc73f56db4749bd8af07e250df912d6687d396f2fa0ad972921f(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationCloudwatchLoggingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9346dfa62558d71cc9a8972fba82fbd17f616dd9559620356bd5d16d922c0139(
    *,
    input_format_configuration: typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration, typing.Dict[builtins.str, typing.Any]],
    output_format_configuration: typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration, typing.Dict[builtins.str, typing.Any]],
    schema_configuration: typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bc70c06378be3f4a4a3e4e825e18ee74e442aa54d8a981a10d07af3222c517(
    *,
    deserializer: typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd1e6e519b6346e502fbc1274efebad18b1c8992e95cc95486c0003585030e8(
    *,
    hive_json_ser_de: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe, typing.Dict[builtins.str, typing.Any]]] = None,
    open_x_json_ser_de: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507f87d821b887bfdf43014c4dc811be3c9ed264e98be3a0bdbec39757c74355(
    *,
    timestamp_formats: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a0bcea16353cd0e5c184bb909105cd4ce5829a3b58aa9bc54b449c090c95bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6304d8063aa05cd9bb4add221c1d0c24630d126ec6cfded4fb1db21ea778a016(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eef3f4ec76c83c8e4c501e4fd3050f83f09bf601926de8c25c93d8650a23329(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerHiveJsonSerDe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16173b491e1224d965035d0a848cba1d69cde788777dba005acad3cc4e1dc82(
    *,
    case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    column_to_json_key_mappings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    convert_dots_in_json_keys_to_underscores: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e59c13b1f7dbdf9b8806a4260c27657ccfb71db9289d2ee5acff1bdada36094(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec7924d7a930bbe42158440877d1248bcdea01304ab6fbdfa1099a4c832c81d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b01b7bf34c98617302466da1a8cbfcfb78330dde97350648b1bef4090ccbbb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c0b10edced7e817a393048961d2f7dcd0a27d1fa6f95524e21785e9338b0f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2593b5e95d9698af27f03fa0761645767d08876a661eeeca0e678b69873b5003(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializerOpenXJsonSerDe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87a13ea702dc1cbf054430e11bcb2ebc7ba6688cf17ba99f8c00c4543cef6e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cf8b3946390f3bc6696146c05e5ad16bf9acbab38810247347af30a9a35304(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfigurationDeserializer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fd0d204e2d8a3debc899bca6fffe96bb01a3908cea155bf4ed0d517ac7420b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b583a36167500b179a5a671dc13fe957071224a9af134ef77bf0ca7d03ee0a96(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationInputFormatConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6a81e5aa30d50073775fa0844816fdeb6943f21ce859ea5a5edd190bc141c6(
    *,
    serializer: typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09b0c726e2b08b00a81239edabb6f19ff47826dacc4495614bbb579b2dbc315(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7f885407ff3209ec1989f2463f3ab99de650f420cecf2fcf134d81854552f3(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9956e42b9af6dc8654cd64510177b0c6923e02b8e7ea15815017c0b4a6cd6a36(
    *,
    orc_ser_de: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe, typing.Dict[builtins.str, typing.Any]]] = None,
    parquet_ser_de: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2a47207e3385fb05844df5af0d99c7bb5ec91ecb9e448d4ddc93b11860974a(
    *,
    block_size_bytes: typing.Optional[jsii.Number] = None,
    bloom_filter_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    bloom_filter_false_positive_probability: typing.Optional[jsii.Number] = None,
    compression: typing.Optional[builtins.str] = None,
    dictionary_key_threshold: typing.Optional[jsii.Number] = None,
    enable_padding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    format_version: typing.Optional[builtins.str] = None,
    padding_tolerance: typing.Optional[jsii.Number] = None,
    row_index_stride: typing.Optional[jsii.Number] = None,
    stripe_size_bytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cea19fecd537e2efa7d54cedaf8796e9ad54d08a342c39f78e8eb231ca5a2fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e8247c7957a06cc6108c7cd6daa033412b75d0ce5d68a127356b299fa4dc71(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9ed8cd7d1ebf5935b6e8dd3ea98e45508b065b1cc56af8ad9ac5e097d5042c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee581abca9df89deaf6c461f4134c39332570ab3b483f29d6ce7a8ced3fcac9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60bde9509fcb7724c2c3bb47447cc182667437ee7e9d5251457be11ee290f951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3adaf5cea7b64a4441f0416409c7ce02f7b83e3f7d8098fdc8a350cfce72bfb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199b7d38d451b29925a10a29e99bb44225a295d4d5061c4a972e92e0170d22dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f42dc05b72d98a35bf39ddf5e11516e24a7a6fac946ee8eb1de4b420d2048e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2479469ebdc8c1a9efeb51e5dd6001e1cb9086fa99f4e19e8814e12c7c41b23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b01fff2e657abc9c994a74b9747cdc5d0f032ebc064d24649e81e23dbe06d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bda27ab98cfd8254e50ceb9eb75a9960d821db43bf82ef1d0a61c4b4a5693aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fe4aea218f36aa134859bc9d67a4eeee55f5c6880459932594d5363ee0deaa(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerOrcSerDe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ab769c532208603f004b21200de34ef3b6069781f88bcf0fed355462a772f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9537b814c43e37f86d893c0a53727d9e99c03fbf031b01a763cfc2d5789781d8(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fad077eca05bce0ccae6574cb9b742c95561cadceff7e6dc006e48bb90e5366(
    *,
    block_size_bytes: typing.Optional[jsii.Number] = None,
    compression: typing.Optional[builtins.str] = None,
    enable_dictionary_compression: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_padding_bytes: typing.Optional[jsii.Number] = None,
    page_size_bytes: typing.Optional[jsii.Number] = None,
    writer_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5234d893d1ca5e8d7adc97bc7fd660eb8c5d11efd647b77453398dde04d919fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6649e8de24fdfbedd35534a346da495cbe6f0d61101e43402488fce02e1139d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402a5ffb195c65f18b01448ad9fbac6bd618facc051316fe4bdff6e035effebb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f5452c6cb743b9a48eef78715845216188bb7a3eccb61220a9b7bc80a87f70(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6245a0429e366aa907a9a7b8d2a57316e5c4f12e355a5dbeaf1e7b9d01dc55(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d24688c6baf0c972a4f75945928f7da68a421f4f61bfda266d87ba2f324d776(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcef9b717798e6f004455c396f4005e209d8b7dfce09e3599029b6b9a38aa25d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2eca011874b6b8cbb01821483d2455342efd1885ee5e954060fde68d171233(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationOutputFormatConfigurationSerializerParquetSerDe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b02740bb11b6e2f6f1ba47fcb668283105773b1b9c4f9913d86c1aa9e181b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e074f92033b4f28efed796cf1c1af1851ec4c63d398cf01217270fef83c4e604(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76671ab44b30963d20dedb4aaf742fee776f696ddec8a2f5dcc504027a372619(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4486293f22a12b15ec1118d2248742d7618f4a5c7bd762ea18f87ca0b223aeb(
    *,
    database_name: builtins.str,
    role_arn: builtins.str,
    table_name: builtins.str,
    catalog_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4f4f9e4fad69ae901b3c42297d889a6bc26c2db083c9be85078bdf6a9b29e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090beb74f9c623d84d6fa02f8460554107dcc0fbfdd0ba045e5a86ea74fceab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ee6dae6c388af32447b0f70454e4ff126b9f9dde68af1068f70f8362236bfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77979db73442f220a465aa4700f889dc5b8bbb1e4781917e471b5490561e304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6f243e1af0ee7166a3d28a384abf606852cb6c7531f3fb92b365fd6a17076d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e00f48f81acac61cdb22cacca016eb626b622d7e8d4f38251ff6afa390ed8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519c05a3d5c1e08c8685eb082d7fdef6fe02f29b0dc89000aaadeac5c536f5e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bcfa030438e6c8c075cd3f9ab37139121e1c827af6bc2d815b44fe0595617b6(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDataFormatConversionConfigurationSchemaConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e9b8ca5ad4c612c5d7ae1b0f33846ec2dc4fd393f7865467c7260d1f691b80(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retry_duration: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a08a20a8436d7368478d459b60fe7913ee980bf3b90920706606407db2f443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7223a8a186746a62beb0c24a510fd6bad548728c420a4ec6b184dc21dc556ad1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f642cdfa5884d818ff55923603a9a983660084ad5c2ae4e3d159dfec834159ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c78164708f0232901881a63ca3a052614030a542bfc3ed8abb92e6e96b131f5(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationDynamicPartitioningConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56ac720587aa614e337a1105abd416c78d145fa4d42af1ec908f14e9f4a4ed6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7a96d5c5974bac81062812905a95ab237c1f2a752c7ef241395c872c2a2de6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe68f4748a3bd0c559e95401d16e1221a037e86b2ac36c04d5c2b1a0bf16620(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2174deea0aa015dc64c79c8e28adbef47e6a9b70ce84a689f5db2356de063515(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d034ff4f56d813c614883f53bb83020b3456e014fb79383790b1daf41c0bd253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f8355d225062f602d519dfab718fcd27a72ba694753b2774594357f3ffa92e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0f91326da7ce1532c423a7ff870061ac878e2338952badc8633d170c32097b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69fd8ee9f34556611169d4dca1013f4acba89be5575d1adffeca9b0e34d6eda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c34eb23f09a0a041fdd64949b2997f8c45727043772eaf1e0c5acf75fea794e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a54a166c893806a91837f3b531a817c3930a1e0117481d2496817d572734c8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db197d8d8767183ec7a992f02f239e22fdccccc629e1cbceb4ddcbf9df078a4(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3Configuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb05123eeedc628a96a0823ca8873237c26ac708cb6f452d39910a2eb4f8eef(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9933f649ee4677160784296a5d202939ae07e3a453b6506b631804b3c070b357(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daea9d23f9a6ac89e4d156a824bdf0bfd3915568f22a4e1c784ae6dfa5a13c94(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f56b6c7d450c85b443e267082349da036eabb36cdb40e2b699cafacbe11c8c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9fc4a60ecb6089be75c30eeddd95c37a8626a4934ada1433d8d740be2fe10c(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81a37cb26c6b63efd8400215045e7658998bedb8bfc911feeabc23e0c8ac6d1(
    *,
    type: builtins.str,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903d5e62183d14094a710c30d4fb476023661b7a6677c69e8b533579da626859(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca701169a5515fbcac41ff7a5009e11d8b0bbf87e7dfe6ca59dd131b41612d61(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031b50045dc22c2f49aafdb7ebc1ad032ebe037321e9b41e0f96cad6d0bf521a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0823205acc0d12dbe8df44030573744302422a254a4e96d9f34754a849e476(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea396d582d8f8251fde074c17ef6476af16e435e9c84bb334fd0875ba0af253(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820d114072af030b7057bf2ad99bc88de2083ce27f127b898323dd9385511c2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ba9d7635ae89507ff3f69020d8412618409c3dc622878edeb7a2b363048d56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545de61c20803285a8040402f19035de38642a697b4fd07e927b13783a3ac4f6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40bc4458f461ee3920387e7088be81ef5c1c7e449dd1d421e18c49d6f531777a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ceb50bca5ca5871a90766788aa588b00f7937dff8e7d577aa9d5edad4650bed(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178a07841625b0707053611dbf25492e35f8fcaf29c3c5787a7431c587d15784(
    *,
    parameter_name: builtins.str,
    parameter_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a910d0329193591963825a91ce8c2d61156185d264289f0f5859c4852c27c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0cfd84f4a7e1f2e9d86acb34b9d2ff837c3bc944f8ae0a430fa27c886acb40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499474030a21bcacfc93933b3f02bba178059ae0ad917d0eb48af97d6a2fba52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c91075e105d642acb8ead3d064899452f5b5e462cb84502b91e45ae00c6022f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2476f2bd26fb024c46b5402eee44c575ffd9c3018f5ccf878a5a3c79b5010b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188a207839013542c8250e27db0158dc71b5e868ae492ec25185db3a035b3ac1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6cbb44f74d71aff6aa73e4fbd629025ec1b82fdf6fc1ee3b0f6fec61daad5bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de58fba0361b2efa657839b3cc1261ac1c3923c2b4d740d455b6c7f452be7b3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78427fe8a531b9ad4abed00b8054f61ba6ed1d6a750e18ae422c2cc630ca777a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd3b8483256e9830b68f17a9ac458c3b53f90ed3ad28408bce3d7f25b03cf06(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0def57bb238221e31d05302cf1cab6235cd81a8f4ee56966f597e09485a841f3(
    *,
    bucket_arn: builtins.str,
    role_arn: builtins.str,
    buffer_interval: typing.Optional[jsii.Number] = None,
    buffer_size: typing.Optional[jsii.Number] = None,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_format: typing.Optional[builtins.str] = None,
    error_output_prefix: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b041930884248cee176c08446eb375b7433de35f638b41468b9249ac28b2f0e2(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6799bb97d7b19008a044e63bb3a9f250f351b9ae7250392d45b1994d435b1f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ede5b17c2454cc4c8a54e9fbebfdf459f5de78bdd79ba1205f2767e0908ba5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9906e2a5bb037bf655cacc6673e491aac6ac786a6be9f01f5e2593342226abb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5709d81d806ef7d2759e1bbe5100917f455aae94a9d4b46d0916cf58cd47ae02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2aa13f7524ba3225ff41547655585df99084ededbab4826f7abfbbb4d31a05(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfigurationCloudwatchLoggingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea369930a8d0ecebd349fb517b148b60b34b7b7345d647505edd777a7796c6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40815d1362eb1ba41b4e8791a2e75e203b2bf745e9ff517f1e19a4a4ff49ead1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b096b7abbf7b5ef6abcbfdcb22003c8ee30d98fda7eb28f3701dd3680791b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1c9a60c888ed968d9980cb5c822b5f5b2f861bd3e4f04e9a7a0097b3e6c826(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd6ee510f649e22b169258b235336f0876e67bd6b5eff7dcd7e7803cc4ca4e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc980db4144cfb86a0447765255e74de6ee11dc419c4905ca790459e1ea5c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635fe8547751eeda9f5c3aabde828840c35a617725e4796fbbd67d0b5e167bca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ba506bcabca65df825d4afb2138a9a63d9e957eb08092a2e57b154bff8631c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc0b546830b1281945d525cf3df8ce6257ccea206518af37e01aa56f661f214(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2428ec95305e876cc4ce3dbcba0b2d0b7f4cf0164034c84665bdabb74282f47(
    value: typing.Optional[KinesisFirehoseDeliveryStreamExtendedS3ConfigurationS3BackupConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a747acc4bb42adf0b624fac1916283c4e7df6eec7c9a68e0d40e67f0386dd0de(
    *,
    url: builtins.str,
    access_key: typing.Optional[builtins.str] = None,
    buffering_interval: typing.Optional[jsii.Number] = None,
    buffering_size: typing.Optional[jsii.Number] = None,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    request_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_duration: typing.Optional[jsii.Number] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d67c53c280e4c5670dffe48908832163e54ec29bc06135cb158bd758595ca95(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae19070ff624fcc8b69b42cf973fdbfb699e2be9ff57610074a8b398d017df6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1c7a208be69031389fd6e850de89196601c9e5f374a4fa71ed571de29d469d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a73130a1a5c9dc2aea33015ed7902e273f8f4efd93bbf9cf5f198774e17f379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67641925e955b946ffad339c74c80c1203179676d5e4a91f55ab54e5bbc9a1eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f70922374dec4b3bb7091267a8216a5d3a490eeb3b65438c65464720f46b34(
    value: typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationCloudwatchLoggingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa6e75809e742917bfd6d4debf6ffee9c7af46e332eef5de1185a5c48b13d44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035cd4ad58cd0fc198f418c81d7ddae12a90287c1c078c253c539470dec1b384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5182f1c74df3713755467a7fc9d99c82b55b17e4c9a6a374260988c5e9c851b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3f952bd54a94fa3900f182e2afec52e545396025788ad834c32d247726a0b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392230e099081a08be7615446d429c8d70442b032d468477ebd1ce1f691d9f63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117fb68503f1c7133bd2cf41b4d42ad46ded0964fabff37626a6de8d5bce3004(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3971a258083a5ab6d3f61805833b9627f39e6ebe7254db680ab2fcff1107a2b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f501ba78914110feffc5c3f1190c49094a31e3fc2a5c99459340f1049772b91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f25d9db8a7097c5cf7373b0ce93c574f3255f8cbde950ab119a487f0e8320ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1c9d34428ce49085e844cbff4c51fbc72a2bf4e03964ea3a45ac05c40abb3f(
    value: typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703d7e2faa8207bfcc7375364e2506d84ae51fa2e29a9f2627337ad65ea1a81d(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df30382e4e9c7dfe6d47a58b423ffecfc120662957609332e941c572f4a3e3f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4f2cbb07f60a16fe5c8599748b8986503ff904ee513b92b2e475d121391ba2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05c7831ef2e4800665f64f927668a0cefcffd31fd826881aaae1d215aefcf63(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1ae251384c8a3c842973beab36156617bb5d4b59429ea161a49b7d23c7647e(
    value: typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af241df6eaea7fd76c8e70a7486fa5aee0681616458fca095655f33e13313c7(
    *,
    type: builtins.str,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ca9df1eb1794bc4b1e49c8583bcf8412728073c41a820585392d2706d99599(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d2743f377eadd578a232bc1429fab98c9d1c48dc8baf07a8c0828612d63c11(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb96360f6d9d70606e4c043dd63bb7100507ce360196dfce1ed9de45d63668a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc94b7ab9ca10df246eefdb0e05bbc0fd70b94be115e53e57f6d04896f099212(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f15723a824b663fd47400078eb60d0724c7e206ed11a907a9e659005607edaa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3388fc69287f2753098bdbd988ac9f917e6924e221dbf185c870898c42067d6d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a8dfd90940ff13daa1780434d27a4f1c7760d117613ee9e4ac81ecb5026876(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b741d45c05197b1b56993f5fda88507b1103b718d4133ed505195883a122d497(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71a317e62a41537bff6124b579444fb5535873f5d3e54b81df932b992b167cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f24d5f9755773e355f5d0795fa9a589636a0e04ca018a510a2ad53b77c4da6(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426c13c8397c039144ef79914b1603c98d1a55024eccabb2677b173393d55fca(
    *,
    parameter_name: builtins.str,
    parameter_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c98f8fc45141f1b668c7720c99fbf3849a7d1a263ff7e6b5177fb9073cbcd3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4049ce79eeba9708c84d3d397fb189ae448bde236d4e3250bb17673fb5fd28f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db08b1b3b949c340b82fb77d1c24e5fec04fa83c89af8d056080347ebdcf127(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5645df17bfdd7dc5319c041c87d590273da7323ef74aa81e31c249c4ae6e88d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a0386e7cde1078dcd5bdb2944c99cfb4f63d60b9de32f6b5828f6ffa70d7c0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265ee91fcdb132bee47b801ab73b46bba70aeeea1b81c18edfb48d8c6b483076(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21235155e78bcaf03eb69b490302013f8a3c38a7c2ac9365998ec3abeff74d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65861f04aabaa4d562288d45ae8163ef0e3fcd330874cd429ec3664a76b002b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2324b866788de3633508ca5224a841b90ef0d1dbfd5fd8362299bc4ea2f538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69964e78e21d860703a95559acbc14ca41ec50c763b8a30e8ffd8f5ca86358a(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70fe59e623f67cbff3e2a9c626614bb9e380ee0a70a0c991a917056d327482df(
    *,
    common_attributes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    content_encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b98eb725f278b3ad417470258dabdab55eadee41f992450ba944424a44bbf6a(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef84572fbe52b7b90bb455594c800daf83ba0f17d30fe1b78f299580a565f8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fe5195ebdfcd54f1dd6389bd7698560bb894cffc889a7b1814ffbf94aa937e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd33cc9fd3bd1cb0fc62f0b2f3e45ba4702fc4fee5cb1f8949e44c42a2fe03a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43bb4f602240c5edc045837e5f5cdd2d03528f4607d2dc3bff6e0605cafe51e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08eb4d652bb23ec6140336266af25035c325fbd9358160d45513f545e91d47c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d847c6ff6254c09462a50d04cde283b48cc2ec354c47eada1854dbc4bc34a693(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9431ea8cd8f0a26dfc5ac15f24991d2d220dd535842a6808981028289d8d25b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2e1f21d6c910ebf52897ceb969903ad5ccc5d27b361e6f774ba2a3bc8f50f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acca243bc3a6e9b2ed7ba6cdc8dd5b15eea85834a161e7b232199a5fa2a399db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212a79ede6d8e62299f9c236bc0e2aebb7295435c88036828f9e1bc3c64fb2a8(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee28044b02f1e2665e01c009bb4afabae60169829aa493ce0e82bbec0501d3ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5dac634455716452834ada27a4d50b8de35d5739001959d47c49acea1f6697(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfigurationCommonAttributes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2bfe89c7653e2ce7d0c69e8e98277b9681c466d4b7ba2dbc237726b985d02a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95dc4b5c931a4b47728358206f307e5d885f44aeed05ce672b56ea26d341e789(
    value: typing.Optional[KinesisFirehoseDeliveryStreamHttpEndpointConfigurationRequestConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aba4c1e4766dae496ef1c8bfc1c1df5d42bae0a777760529f2cc156e3737d6e(
    *,
    kinesis_stream_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a7e58fc7609bb8e23662e4cd4e4665f71708c4c28ed8d1b0e93aae56f57778(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b1dee9549eae1ab7ae328d7d34a16ef4a1a2246d36422609f3017b648511aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812f977e142979aa3002dcb8282935c6f6b593d68996096623a04734cd847e06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3d0d4ecb4bc059df3bee15a7189b65fbcbdc50ffd7772961f3e3d15c48a233(
    value: typing.Optional[KinesisFirehoseDeliveryStreamKinesisSourceConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19a8f62231062221bdfcd28279f8df98eb3f29b2489b587a4b4d4ee19c82ed3(
    *,
    cluster_jdbcurl: builtins.str,
    data_table_name: builtins.str,
    password: builtins.str,
    role_arn: builtins.str,
    username: builtins.str,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    copy_options: typing.Optional[builtins.str] = None,
    data_table_columns: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_duration: typing.Optional[jsii.Number] = None,
    s3_backup_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad0395a60a44cb9ac26cff1563c9ed6d6ba75d5686cee4853155fef3e69d216(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195f2f6fa843e59829574f048726a691a555a8a69802f8b9aafef15cb8e87b34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8bec4f3b33448db6a81f77a66aa1620a82a02e7b24510a8e954fa92d1b8d9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bdd4b9b31ada5ff360dfa975e3cf692770a076dbf4fd2d14f50c3e3f40842d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c7f3cc39dbab6d5295f9d47376ae481be7f0874ec6c4689297f96a30e6f872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b1726c9a8f648e5f6ed45bd9d51a2aa17432b745d93675eb9bc55648e19f8e(
    value: typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationCloudwatchLoggingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00867147521939d0b351128e420c416ef84664a90a48b743ef76c722ab76b618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2afd6b2952dac277e9f0c1564f9bc4465aa22646e4d72055c62b0f198c7773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52859c72a8200de6173fdea6f6968c89177428c738eb9e1ad18b60f1e26aec69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1359d7a178edc95fcea97d8e0e22db5691276e821aabc3658af92e83c5570957(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10650f9d44eb2fbfa98ac50d07c434554b56e13d45455d78ab5388b7ab87ebae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35717a9df1e12f700b5f7d1fa992b93b927f70170a11413bb74f38995551a2fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c7a8cfdf053fb7fbad63e33e6571e2c3fed2a2ddb462eae68ac0464e2361c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b9fc4910242f39c485c8facdd77b1507ab389ae899c2cfef265f66fafeb32d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f542dc454e6944293857c5314928f9e9f0a883a6727447dad7b94ad618ea5be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cef0c0dccdd9ea6a84a25ce9ca856d76c846df3422c95be9700d204bee7139(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f078eb41b46440789a880d68900ec440d03936914bff0056329f40c355efffe3(
    value: typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9fc926a4d9643a40b455f0853cdc215cfcf6146fc34d538448990177c049c3(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4861e9b05115171bc9cd07b744153922b0a0a2c87bad2b780a569ac159686f83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f583430e26de08da86d774a77e5f3479d67ca277e9a72f01e4cebd1ac2ff458(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ddaf659e8acab4c09c5e9eead4c951e2384eb7011127bf38a64463e8a37449(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fbc1e74aff8ade34e2cc754019fc635a950e472414701227e67e8b724972a8(
    value: typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837fecdeb27cfcd97f17d8780fc0f1ef2d2bf8aa0dbf5d585a2158846afb645e(
    *,
    type: builtins.str,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97a63248bae6ed48d923de7256d72fe754328b5263fe388a2f3944f9822be37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e94bec23373c668066b0f6988ff119d2a0259ea968fa91a4a82a2637f4ebce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c1bdfc3d96952252ef0e3d90a9eac9af96e7279b47e10485c959f486e58292(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca89df8210939359fa933a27ae7747abd2b0b3b8c143b365875b68ef30f09eb6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aeb2cb61425768d6a1bce2a5936bff1357de7cf06bc668f9409e31ba0322856(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f439c48afa7142e9f4109b5e53ab1c49a67e0a822df4230262e43103abe0a78(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262ed6c8f0366601b682b7b472bccecf624558fe1122fe31c1bfde9b58f7d7d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a684c9aa96f793d430afca035a1339c07eeb34e1b4b235e3266adb42b6431d4e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90c74955a2193a3d126b68bcb798db1e2eee010e07b208f114109e2948d23e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8da2799bc40c7cbf049aa9f0506d7441a649db06c80dcc3403218f24c0e7e30(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9526b521f1d5128d2a99bf45404cf3491a821235739e9e9bb0c96d1688fa9c(
    *,
    parameter_name: builtins.str,
    parameter_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cef3f866c4ed24cb23a35e83310d24611a19ca0c5959c5eb3d257e9e8e7767(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d35dd264da21ff44d311abe0733d736efb3fb9b31e11e1d5e958b468598c8f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b6de82efa42c264e7f991534c180c781fc049c07eb834b44851dc1ec5bfddc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387842b8493e304976ae6b83d2bc0017a5e459c67273ec2e2683ecc749fa613b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3390a24a6f6b71d109b1ea3ca88ed9451ddbd9a70d354930e5616d1a8cecc4ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5348011f08f43dc5401a7932de362c45ea57e34ce394e81923d87148cd2f3d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2dbf4185641505c3c9557538116fd1c4df0ccdf4d7bb78507551242204884a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a067fd7d06a8cd8d4d772cef3057aff566d02fbb8c2327b2bea64e5f2dbc5bb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84604f34a6754da082b6a84fbbc532913940a1e442fb5855143c74eec19ce953(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a8c6939d6ece493e17a1699319173da6fdb0a597d65d1478c34aa505e81a80(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920ac070e2943e17bdd239eb1f163936200f454c083920af41c694625d63080d(
    *,
    bucket_arn: builtins.str,
    role_arn: builtins.str,
    buffer_interval: typing.Optional[jsii.Number] = None,
    buffer_size: typing.Optional[jsii.Number] = None,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_format: typing.Optional[builtins.str] = None,
    error_output_prefix: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e772db66a08ed9cd070345953a3933246c87b81aaaeff583bb2c252863e7225(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8cb7676b4e74dc09275a926fb66d4114db573d46807a621d703afe1a27d29c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09508b0672fa2e3892b83cfb25997e16b24695c5b83888690403275656c942a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867d72ea30c25ad794f29ae48c54425eac144fb02e47e06e3d09062410185de8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236db44a85168698c3774894c116e491c9753cc6bf4d75524ad41d8a93afa387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b268c2126e68bc086b1cc7e59939912caa32dc75f66a33727fc313c108489ad(
    value: typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfigurationCloudwatchLoggingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c31958496faec3ce582eabaa65dd11167a90f223394287956aa4f5f41955f9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f418f387ba509d41754828bbf5fb6b5ed932d37ae992e24fc92cebaa25cf5f99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc73144cf0a41f21e6da4f8468bf9284c84357c473dfc48d3d0c2b422ecac80(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a06804d7e654677f29e4b8d6265696d468480a1b15035599a44f7f0ee1e91b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4786f71dc572eedf4c574c3cb49957a40bc79c3504d466f3ea4c420649de7616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0279fa76fb860005f6b376754abaf728b6a95d743cd8138201c89c410656558(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153ed85e2d4b0d1b79ef687f188275215f912a800822440ee048688c9a067243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d457c9ca46695deeea522c7f09e2bb6ea6f0e04582c15c9bcc66f3b6e0af8696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44ee511eb190c35bcbb066b1cced19aa45f9ee6120d8e4897d7cc386afd5408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b5122458f909f30f372a6d016e72b211e0744f736634c37d2e50e13091f400(
    value: typing.Optional[KinesisFirehoseDeliveryStreamRedshiftConfigurationS3BackupConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0408ee6e6b97447f2f1132f2029bac5c79ef06e29f386a8e1d78fa767d666dd1(
    *,
    bucket_arn: builtins.str,
    role_arn: builtins.str,
    buffer_interval: typing.Optional[jsii.Number] = None,
    buffer_size: typing.Optional[jsii.Number] = None,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    compression_format: typing.Optional[builtins.str] = None,
    error_output_prefix: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3779e815fe3b2c543558ee95d579ebb0f705ee99b5b001c3cdfd0ad238e7082(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ded24101297aeb625ab01541c93f2b4ba0f4297297688cd05a36da7a2c06235(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb73fa49cd754427b81e551284a4403423fda1227931a92adfe4755b0872c87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b862d43ac8690389234a5b1fa494bbbce155bd817732ea13de720a87148a99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7daa2301c47fa37c45de007ec87484e028ec1fccd1368399e432110435ddfb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3831f97a2d3a07ed582333ea3ddc22756e7c69dbf85a1e068cbb28abf671e515(
    value: typing.Optional[KinesisFirehoseDeliveryStreamS3ConfigurationCloudwatchLoggingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4c47793765944c2be616fa55bfa879fc17ba8bbe32924233c245c1fabaf517(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b1a424fa74f3e46f74caf9be00fcf0c13a9bba736b3d9cb22cefb78b8bc42f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd52422a904fee7c623d6aa981d99dc8907098baf3148d75fddad6fd69b21128(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35e864ea13e639f0b1c377a68c51837508e31b94ede92d54e2f27cc30e3b443(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053a3a89206e86e1665e12a6d0e486ec665000188875f87b9a381937481bfe96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f44cb9b19f7e3905bf4d8bb01385ab99281203e648c892b40228530fd458358(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07969a3ef33cb12e9eaa6aa8af5e4536a20ba21b3860916e026ed37ca8a137b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889edfdb7b97700e7c0fdedfc747cc4b7f0fbc941e8127b17fe4ee7eceb3daa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ddb6293c9498149ccf29ca119063a617fe24b837f15592689331e13d52eabe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b27484e5854439638e1d460560e2c4e5ea73c3456e30a016ae99182a4a167e(
    value: typing.Optional[KinesisFirehoseDeliveryStreamS3Configuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1bfaf8e5fcf63ea5e1de1eb395bcd32d26f33d582130b9ff49abd4260c1030(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_arn: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123ba4bbd9240f864ddf45ddd5cf3cc26df68623dd5c01bd8ba440f0c76bba3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5131b2585024b55d069acb69aff58a6d00e91e10ead2b9e419ccec83b6ba77b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0203c27e3352f8e97bc38bf21c5c47d69b2fa1e6a37eecc3368e74c66a8bf9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4ed1bca1176e22fdb80ec74eb6dcc2a37a4a4e9ed67f9d0b77d28a22b28008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49deb60f22347c756905a1058ee94e5b216d1966363e19fccb8d675d04d39792(
    value: typing.Optional[KinesisFirehoseDeliveryStreamServerSideEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8077da78b1628abc9a9ac2254a1b0b92b91425fee0ba3edc4ec0db346a92ee7d(
    *,
    hec_endpoint: builtins.str,
    hec_token: builtins.str,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    hec_acknowledgment_timeout: typing.Optional[jsii.Number] = None,
    hec_endpoint_type: typing.Optional[builtins.str] = None,
    processing_configuration: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_duration: typing.Optional[jsii.Number] = None,
    s3_backup_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd33b3ac115279dad091a28eecbba09f4d2b65586835f3de0fc202cde8bdfaa(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b8ad102b2c94c74d04ee51b33ba488af85a4ab146d0c23975e4f4db5fa280b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec89cc14f6f4e35f524ec2f5c79d6bc6ab5d2339f96ee5231a1b6fdab24d70b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379c2caba5b3a98323d9fc2384108c3957b923ea61af73afaad6292384ca661d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b6807a273c6968290f95bdf920fd6a3b574046eb3f78d39fac6e318c5e3649(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723137a9953e64a018b0bec51a67b643e0ee84b526a825198b1dcebccad18989(
    value: typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfigurationCloudwatchLoggingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ab391a32976930c384d864f74c08838da916dd2bd92bfce8565375eb0426c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4019b803bd9702961a60d0356882ca987952c15071688576a8a0952edf67af46(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0939813722a179aa5ccc26ec387a0923a23a03a33122a97788ab296484c4030b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1dc4317071fa4bafd40c320350eeac41ffb7e2865e7829342b5a4674c92a25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53fe9af74bfd37d75bcb44b55c710cbf4b73bb90cf7561e45443d846549fc2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29852517b83cf31fa922256b6507053f4608a2241854d2489810adaaf81c9f2b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e66ac9fff83b6b55ca1ef2af0f3d0ea61d68097d510e61b4bf81fb6ecd2be37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c12a24a192f7a221fdc43e7d4126288f06cba259b09abf20c04a5693713921f(
    value: typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43860ca298e581371f4041394fc6cad874d2534c48c330c4eedd2f162eea474d(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    processors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71ace754f38df2a5ea95a29cf715c9504d420aaffe650f7ac62ec687303cb07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1104f6dce1c7ee944018827567e884d837096f26c141a4027a2eb0dbf880dd11(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a289e4d07ec67e598a9a641af17f34d0ed55ee47b21f88f5069e3fbf9a37e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181bd8e135ca9038e859c67309ff7f7949388aac9e1a8f3bcdd627673740e661(
    value: typing.Optional[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ea866c8b026e19c7e592ca0db9d43e36ee4b342d876bfbdcc9fd1b53f31dfc(
    *,
    type: builtins.str,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244ca2d90d27d7fda0de239c0c8390aa5b727622734c4182c051487e714b15c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10430b50afe80cafb69fe9ab048076997044d3ca833f74227defd4929399613d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc433e6670917304d4e88e99bbb75bb5e7a72277ef122652f22e822ef989c569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d608c1360b081fbd25f0a2dc71d2ee63ac686e43a938d5e81639c422b81c23cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897c6d325766ccdbd0f77aab48fe9e018b7da9097dfeb85ff098c259d7870e06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320fd3b082f7972cc7efc6d987f1032d6a8b99919aba8b402e88c509a4fb3fc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476e041bb5d499a9944811a6d1a43245b586044dea564902ad78957bb8715a5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b7c06bf601b7c77f1d9aca96adca660dd28aecf6a896304c209bce0830eab3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a8b94c2e4dab3ca993758a3e89a2465ef8fb7ef6bcdd6e604ed491222d0883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73b4b659ca7d818135774c3fa4f509ddb694ba85d7c24b4fa56c8cf6df2adc2(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessors, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a555d69117299cc952ca17152e878579e8d163d823988d17b728343c9e75783c(
    *,
    parameter_name: builtins.str,
    parameter_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765751b10ae0efda28f3059fb2ea23b03044505581886075d09fbf0cb755c705(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010ba0fc40cab47ecf8aa4ef7ea7cdf9cb981a4c1c742feecf53f9fcd4134c7b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591d7ba9c1235b608a74e10f5727b294c030f42e3a8abe0a5c0901e685c7998e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f7b7bf1cf772550e8ce47399da52390a477c113b57cf400656005d6fcf4267(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c371edb77b37220b5c4ece30dcc4718dd3677ff98536c4f836ca5754a1a61862(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e51f4ed60e452777964501d8b5a16d9352677908ee030569c67ca14e9eef2f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bfd23f92b7d63722dac6e255e9d59cfe1d588068dc040c68e82adb30474d8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f459ea134e76727b19707f551c9a48428835c2096ce41f6384577559f17a4fdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ca814d6bde2dd4aedffe8d0da5b9d96b37b88ee8aa3ba347070cef41e457df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef95976f644ef3e7255f0ecbe5777e5da027a520b024d733a80a7295402f712(
    value: typing.Optional[typing.Union[KinesisFirehoseDeliveryStreamSplunkConfigurationProcessingConfigurationProcessorsParameters, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
