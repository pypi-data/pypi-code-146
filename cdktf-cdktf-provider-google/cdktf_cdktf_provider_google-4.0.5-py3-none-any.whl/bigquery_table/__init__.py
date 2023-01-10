'''
# `google_bigquery_table`

Refer to the Terraform Registory for docs: [`google_bigquery_table`](https://www.terraform.io/docs/providers/google/r/bigquery_table).
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


class BigqueryTable(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTable",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/bigquery_table google_bigquery_table}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset_id: builtins.str,
        table_id: builtins.str,
        clustering: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union["BigqueryTableEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        expiration_time: typing.Optional[jsii.Number] = None,
        external_data_configuration: typing.Optional[typing.Union["BigqueryTableExternalDataConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        materialized_view: typing.Optional[typing.Union["BigqueryTableMaterializedView", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        range_partitioning: typing.Optional[typing.Union["BigqueryTableRangePartitioning", typing.Dict[builtins.str, typing.Any]]] = None,
        schema: typing.Optional[builtins.str] = None,
        time_partitioning: typing.Optional[typing.Union["BigqueryTableTimePartitioning", typing.Dict[builtins.str, typing.Any]]] = None,
        view: typing.Optional[typing.Union["BigqueryTableView", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/bigquery_table google_bigquery_table} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset_id: The dataset ID to create the table in. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#dataset_id BigqueryTable#dataset_id}
        :param table_id: A unique ID for the resource. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#table_id BigqueryTable#table_id}
        :param clustering: Specifies column names to use for data clustering. Up to four top-level columns are allowed, and should be specified in descending priority order. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#clustering BigqueryTable#clustering}
        :param deletion_protection: Whether or not to allow Terraform to destroy the instance. Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#deletion_protection BigqueryTable#deletion_protection}
        :param description: The field description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#description BigqueryTable#description}
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#encryption_configuration BigqueryTable#encryption_configuration}
        :param expiration_time: The time when this table expires, in milliseconds since the epoch. If not present, the table will persist indefinitely. Expired tables will be deleted and their storage reclaimed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#expiration_time BigqueryTable#expiration_time}
        :param external_data_configuration: external_data_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#external_data_configuration BigqueryTable#external_data_configuration}
        :param friendly_name: A descriptive name for the table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#friendly_name BigqueryTable#friendly_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#id BigqueryTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A mapping of labels to assign to the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#labels BigqueryTable#labels}
        :param materialized_view: materialized_view block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#materialized_view BigqueryTable#materialized_view}
        :param project: The ID of the project in which the resource belongs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#project BigqueryTable#project}
        :param range_partitioning: range_partitioning block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#range_partitioning BigqueryTable#range_partitioning}
        :param schema: A JSON schema for the table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#schema BigqueryTable#schema}
        :param time_partitioning: time_partitioning block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#time_partitioning BigqueryTable#time_partitioning}
        :param view: view block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#view BigqueryTable#view}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b097032883d450d5b0dd2683567f8b829165b537d5a8be476cbb660ce43d5747)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryTableConfig(
            dataset_id=dataset_id,
            table_id=table_id,
            clustering=clustering,
            deletion_protection=deletion_protection,
            description=description,
            encryption_configuration=encryption_configuration,
            expiration_time=expiration_time,
            external_data_configuration=external_data_configuration,
            friendly_name=friendly_name,
            id=id,
            labels=labels,
            materialized_view=materialized_view,
            project=project,
            range_partitioning=range_partitioning,
            schema=schema,
            time_partitioning=time_partitioning,
            view=view,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The self link or full name of a key which should be used to encrypt this table. Note that the default bigquery service account will need to have encrypt/decrypt permissions on this key - you may want to see the google_bigquery_default_service_account datasource and the google_kms_crypto_key_iam_binding resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#kms_key_name BigqueryTable#kms_key_name}
        '''
        value = BigqueryTableEncryptionConfiguration(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putExternalDataConfiguration")
    def put_external_data_configuration(
        self,
        *,
        autodetect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        source_format: builtins.str,
        source_uris: typing.Sequence[builtins.str],
        avro_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationAvroOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression: typing.Optional[builtins.str] = None,
        connection_id: typing.Optional[builtins.str] = None,
        csv_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        google_sheets_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationGoogleSheetsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_partitioning_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationHivePartitioningOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        ignore_unknown_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_bad_records: typing.Optional[jsii.Number] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param autodetect: Let BigQuery try to autodetect the schema and format of the table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#autodetect BigqueryTable#autodetect}
        :param source_format: The data format. Supported values are: "CSV", "GOOGLE_SHEETS", "NEWLINE_DELIMITED_JSON", "AVRO", "PARQUET", "ORC" and "DATASTORE_BACKUP". To use "GOOGLE_SHEETS" the scopes must include "googleapis.com/auth/drive.readonly". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#source_format BigqueryTable#source_format}
        :param source_uris: A list of the fully-qualified URIs that point to your data in Google Cloud. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#source_uris BigqueryTable#source_uris}
        :param avro_options: avro_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#avro_options BigqueryTable#avro_options}
        :param compression: The compression type of the data source. Valid values are "NONE" or "GZIP". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#compression BigqueryTable#compression}
        :param connection_id: The connection specifying the credentials to be used to read external storage, such as Azure Blob, Cloud Storage, or S3. The connectionId can have the form "{{project}}.{{location}}.{{connection_id}}" or "projects/{{project}}/locations/{{location}}/connections/{{connection_id}}". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#connection_id BigqueryTable#connection_id}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#csv_options BigqueryTable#csv_options}
        :param google_sheets_options: google_sheets_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#google_sheets_options BigqueryTable#google_sheets_options}
        :param hive_partitioning_options: hive_partitioning_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#hive_partitioning_options BigqueryTable#hive_partitioning_options}
        :param ignore_unknown_values: Indicates if BigQuery should allow extra values that are not represented in the table schema. If true, the extra values are ignored. If false, records with extra columns are treated as bad records, and if there are too many bad records, an invalid error is returned in the job result. The default value is false. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#ignore_unknown_values BigqueryTable#ignore_unknown_values}
        :param max_bad_records: The maximum number of bad records that BigQuery can ignore when reading data. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#max_bad_records BigqueryTable#max_bad_records}
        :param schema: A JSON schema for the external table. Schema is required for CSV and JSON formats and is disallowed for Google Cloud Bigtable, Cloud Datastore backups, and Avro formats when using external tables. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#schema BigqueryTable#schema}
        '''
        value = BigqueryTableExternalDataConfiguration(
            autodetect=autodetect,
            source_format=source_format,
            source_uris=source_uris,
            avro_options=avro_options,
            compression=compression,
            connection_id=connection_id,
            csv_options=csv_options,
            google_sheets_options=google_sheets_options,
            hive_partitioning_options=hive_partitioning_options,
            ignore_unknown_values=ignore_unknown_values,
            max_bad_records=max_bad_records,
            schema=schema,
        )

        return typing.cast(None, jsii.invoke(self, "putExternalDataConfiguration", [value]))

    @jsii.member(jsii_name="putMaterializedView")
    def put_materialized_view(
        self,
        *,
        query: builtins.str,
        enable_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        refresh_interval_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: A query whose result is persisted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#query BigqueryTable#query}
        :param enable_refresh: Specifies if BigQuery should automatically refresh materialized view when the base table is updated. The default is true. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#enable_refresh BigqueryTable#enable_refresh}
        :param refresh_interval_ms: Specifies maximum frequency at which this materialized view will be refreshed. The default is 1800000. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#refresh_interval_ms BigqueryTable#refresh_interval_ms}
        '''
        value = BigqueryTableMaterializedView(
            query=query,
            enable_refresh=enable_refresh,
            refresh_interval_ms=refresh_interval_ms,
        )

        return typing.cast(None, jsii.invoke(self, "putMaterializedView", [value]))

    @jsii.member(jsii_name="putRangePartitioning")
    def put_range_partitioning(
        self,
        *,
        field: builtins.str,
        range: typing.Union["BigqueryTableRangePartitioningRange", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param field: The field used to determine how to create a range-based partition. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#field BigqueryTable#field}
        :param range: range block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#range BigqueryTable#range}
        '''
        value = BigqueryTableRangePartitioning(field=field, range=range)

        return typing.cast(None, jsii.invoke(self, "putRangePartitioning", [value]))

    @jsii.member(jsii_name="putTimePartitioning")
    def put_time_partitioning(
        self,
        *,
        type: builtins.str,
        expiration_ms: typing.Optional[jsii.Number] = None,
        field: typing.Optional[builtins.str] = None,
        require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: The supported types are DAY, HOUR, MONTH, and YEAR, which will generate one partition per day, hour, month, and year, respectively. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#type BigqueryTable#type}
        :param expiration_ms: Number of milliseconds for which to keep the storage for a partition. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#expiration_ms BigqueryTable#expiration_ms}
        :param field: The field used to determine how to create a time-based partition. If time-based partitioning is enabled without this value, the table is partitioned based on the load time. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#field BigqueryTable#field}
        :param require_partition_filter: If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        '''
        value = BigqueryTableTimePartitioning(
            type=type,
            expiration_ms=expiration_ms,
            field=field,
            require_partition_filter=require_partition_filter,
        )

        return typing.cast(None, jsii.invoke(self, "putTimePartitioning", [value]))

    @jsii.member(jsii_name="putView")
    def put_view(
        self,
        *,
        query: builtins.str,
        use_legacy_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query: A query that BigQuery executes when the view is referenced. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#query BigqueryTable#query}
        :param use_legacy_sql: Specifies whether to use BigQuery's legacy SQL for this view. The default value is true. If set to false, the view will use BigQuery's standard SQL Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#use_legacy_sql BigqueryTable#use_legacy_sql}
        '''
        value = BigqueryTableView(query=query, use_legacy_sql=use_legacy_sql)

        return typing.cast(None, jsii.invoke(self, "putView", [value]))

    @jsii.member(jsii_name="resetClustering")
    def reset_clustering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClustering", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncryptionConfiguration")
    def reset_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetExpirationTime")
    def reset_expiration_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationTime", []))

    @jsii.member(jsii_name="resetExternalDataConfiguration")
    def reset_external_data_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalDataConfiguration", []))

    @jsii.member(jsii_name="resetFriendlyName")
    def reset_friendly_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFriendlyName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaterializedView")
    def reset_materialized_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaterializedView", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRangePartitioning")
    def reset_range_partitioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangePartitioning", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @jsii.member(jsii_name="resetTimePartitioning")
    def reset_time_partitioning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimePartitioning", []))

    @jsii.member(jsii_name="resetView")
    def reset_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetView", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> "BigqueryTableEncryptionConfigurationOutputReference":
        return typing.cast("BigqueryTableEncryptionConfigurationOutputReference", jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="externalDataConfiguration")
    def external_data_configuration(
        self,
    ) -> "BigqueryTableExternalDataConfigurationOutputReference":
        return typing.cast("BigqueryTableExternalDataConfigurationOutputReference", jsii.get(self, "externalDataConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedTime")
    def last_modified_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastModifiedTime"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="materializedView")
    def materialized_view(self) -> "BigqueryTableMaterializedViewOutputReference":
        return typing.cast("BigqueryTableMaterializedViewOutputReference", jsii.get(self, "materializedView"))

    @builtins.property
    @jsii.member(jsii_name="numBytes")
    def num_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numBytes"))

    @builtins.property
    @jsii.member(jsii_name="numLongTermBytes")
    def num_long_term_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLongTermBytes"))

    @builtins.property
    @jsii.member(jsii_name="numRows")
    def num_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numRows"))

    @builtins.property
    @jsii.member(jsii_name="rangePartitioning")
    def range_partitioning(self) -> "BigqueryTableRangePartitioningOutputReference":
        return typing.cast("BigqueryTableRangePartitioningOutputReference", jsii.get(self, "rangePartitioning"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timePartitioning")
    def time_partitioning(self) -> "BigqueryTableTimePartitioningOutputReference":
        return typing.cast("BigqueryTableTimePartitioningOutputReference", jsii.get(self, "timePartitioning"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="view")
    def view(self) -> "BigqueryTableViewOutputReference":
        return typing.cast("BigqueryTableViewOutputReference", jsii.get(self, "view"))

    @builtins.property
    @jsii.member(jsii_name="clusteringInput")
    def clustering_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clusteringInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional["BigqueryTableEncryptionConfiguration"]:
        return typing.cast(typing.Optional["BigqueryTableEncryptionConfiguration"], jsii.get(self, "encryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationTimeInput")
    def expiration_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expirationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalDataConfigurationInput")
    def external_data_configuration_input(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfiguration"]:
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfiguration"], jsii.get(self, "externalDataConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="friendlyNameInput")
    def friendly_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "friendlyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="materializedViewInput")
    def materialized_view_input(
        self,
    ) -> typing.Optional["BigqueryTableMaterializedView"]:
        return typing.cast(typing.Optional["BigqueryTableMaterializedView"], jsii.get(self, "materializedViewInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rangePartitioningInput")
    def range_partitioning_input(
        self,
    ) -> typing.Optional["BigqueryTableRangePartitioning"]:
        return typing.cast(typing.Optional["BigqueryTableRangePartitioning"], jsii.get(self, "rangePartitioningInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timePartitioningInput")
    def time_partitioning_input(
        self,
    ) -> typing.Optional["BigqueryTableTimePartitioning"]:
        return typing.cast(typing.Optional["BigqueryTableTimePartitioning"], jsii.get(self, "timePartitioningInput"))

    @builtins.property
    @jsii.member(jsii_name="viewInput")
    def view_input(self) -> typing.Optional["BigqueryTableView"]:
        return typing.cast(typing.Optional["BigqueryTableView"], jsii.get(self, "viewInput"))

    @builtins.property
    @jsii.member(jsii_name="clustering")
    def clustering(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clustering"))

    @clustering.setter
    def clustering(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36a827767218e30e15ed46c620f1d6ac1649ac81e9a1f8fbf50b44994a8de7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clustering", value)

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ba56c49b068bbf8763ea0042060807cbf89b0406ef980ed1fc45513c07dca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value)

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62578b34b021403200b1036268e3acd655157cb771a72f5d129bf260f4c27cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c0bfe985825d9a80acd8f5aefedd8901d464dacf94af409b2a81efccfc3fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expirationTime"))

    @expiration_time.setter
    def expiration_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5413b10f3ec29a1d03f7c2f42f492fee9e3d71fa450c28d4bd6f46ef3ef51e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTime", value)

    @builtins.property
    @jsii.member(jsii_name="friendlyName")
    def friendly_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "friendlyName"))

    @friendly_name.setter
    def friendly_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b95bd39489b26bd16347f815db6f92fba878214004df53fa734ec6f798849ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "friendlyName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af66ed510248d931e4bb1f43b218cca02cd6069e76f18cdb7150e9530186201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c74889bf00ce24f484abd1bc28bf3cf7d61665b2ab8f55381086fce8f1291c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1a6d53539cb352313127bc88400bfb27109837e44e77e3c2445bb3a3ceaa22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570adc90f3ed8491972bb571ec80eb5f0b0fdf5931d71a249e93fd1f993d7b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ff67f97457c05dfe2bdc38c7d1b6d4d3ab19d3aed9a3b6ab5e87619edf6da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dataset_id": "datasetId",
        "table_id": "tableId",
        "clustering": "clustering",
        "deletion_protection": "deletionProtection",
        "description": "description",
        "encryption_configuration": "encryptionConfiguration",
        "expiration_time": "expirationTime",
        "external_data_configuration": "externalDataConfiguration",
        "friendly_name": "friendlyName",
        "id": "id",
        "labels": "labels",
        "materialized_view": "materializedView",
        "project": "project",
        "range_partitioning": "rangePartitioning",
        "schema": "schema",
        "time_partitioning": "timePartitioning",
        "view": "view",
    },
)
class BigqueryTableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dataset_id: builtins.str,
        table_id: builtins.str,
        clustering: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union["BigqueryTableEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        expiration_time: typing.Optional[jsii.Number] = None,
        external_data_configuration: typing.Optional[typing.Union["BigqueryTableExternalDataConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        materialized_view: typing.Optional[typing.Union["BigqueryTableMaterializedView", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        range_partitioning: typing.Optional[typing.Union["BigqueryTableRangePartitioning", typing.Dict[builtins.str, typing.Any]]] = None,
        schema: typing.Optional[builtins.str] = None,
        time_partitioning: typing.Optional[typing.Union["BigqueryTableTimePartitioning", typing.Dict[builtins.str, typing.Any]]] = None,
        view: typing.Optional[typing.Union["BigqueryTableView", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset_id: The dataset ID to create the table in. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#dataset_id BigqueryTable#dataset_id}
        :param table_id: A unique ID for the resource. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#table_id BigqueryTable#table_id}
        :param clustering: Specifies column names to use for data clustering. Up to four top-level columns are allowed, and should be specified in descending priority order. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#clustering BigqueryTable#clustering}
        :param deletion_protection: Whether or not to allow Terraform to destroy the instance. Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#deletion_protection BigqueryTable#deletion_protection}
        :param description: The field description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#description BigqueryTable#description}
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#encryption_configuration BigqueryTable#encryption_configuration}
        :param expiration_time: The time when this table expires, in milliseconds since the epoch. If not present, the table will persist indefinitely. Expired tables will be deleted and their storage reclaimed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#expiration_time BigqueryTable#expiration_time}
        :param external_data_configuration: external_data_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#external_data_configuration BigqueryTable#external_data_configuration}
        :param friendly_name: A descriptive name for the table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#friendly_name BigqueryTable#friendly_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#id BigqueryTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A mapping of labels to assign to the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#labels BigqueryTable#labels}
        :param materialized_view: materialized_view block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#materialized_view BigqueryTable#materialized_view}
        :param project: The ID of the project in which the resource belongs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#project BigqueryTable#project}
        :param range_partitioning: range_partitioning block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#range_partitioning BigqueryTable#range_partitioning}
        :param schema: A JSON schema for the table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#schema BigqueryTable#schema}
        :param time_partitioning: time_partitioning block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#time_partitioning BigqueryTable#time_partitioning}
        :param view: view block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#view BigqueryTable#view}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_configuration, dict):
            encryption_configuration = BigqueryTableEncryptionConfiguration(**encryption_configuration)
        if isinstance(external_data_configuration, dict):
            external_data_configuration = BigqueryTableExternalDataConfiguration(**external_data_configuration)
        if isinstance(materialized_view, dict):
            materialized_view = BigqueryTableMaterializedView(**materialized_view)
        if isinstance(range_partitioning, dict):
            range_partitioning = BigqueryTableRangePartitioning(**range_partitioning)
        if isinstance(time_partitioning, dict):
            time_partitioning = BigqueryTableTimePartitioning(**time_partitioning)
        if isinstance(view, dict):
            view = BigqueryTableView(**view)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a75785b12d60945a47678d02ebd6a12a808d31eb6207fa82349d07fd479f943)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
            check_type(argname="argument clustering", value=clustering, expected_type=type_hints["clustering"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument expiration_time", value=expiration_time, expected_type=type_hints["expiration_time"])
            check_type(argname="argument external_data_configuration", value=external_data_configuration, expected_type=type_hints["external_data_configuration"])
            check_type(argname="argument friendly_name", value=friendly_name, expected_type=type_hints["friendly_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument materialized_view", value=materialized_view, expected_type=type_hints["materialized_view"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument range_partitioning", value=range_partitioning, expected_type=type_hints["range_partitioning"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument time_partitioning", value=time_partitioning, expected_type=type_hints["time_partitioning"])
            check_type(argname="argument view", value=view, expected_type=type_hints["view"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "table_id": table_id,
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
        if clustering is not None:
            self._values["clustering"] = clustering
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if description is not None:
            self._values["description"] = description
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if expiration_time is not None:
            self._values["expiration_time"] = expiration_time
        if external_data_configuration is not None:
            self._values["external_data_configuration"] = external_data_configuration
        if friendly_name is not None:
            self._values["friendly_name"] = friendly_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if materialized_view is not None:
            self._values["materialized_view"] = materialized_view
        if project is not None:
            self._values["project"] = project
        if range_partitioning is not None:
            self._values["range_partitioning"] = range_partitioning
        if schema is not None:
            self._values["schema"] = schema
        if time_partitioning is not None:
            self._values["time_partitioning"] = time_partitioning
        if view is not None:
            self._values["view"] = view

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
    def dataset_id(self) -> builtins.str:
        '''The dataset ID to create the table in. Changing this forces a new resource to be created.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#dataset_id BigqueryTable#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''A unique ID for the resource. Changing this forces a new resource to be created.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#table_id BigqueryTable#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def clustering(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies column names to use for data clustering.

        Up to four top-level columns are allowed, and should be specified in descending priority order.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#clustering BigqueryTable#clustering}
        '''
        result = self._values.get("clustering")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to allow Terraform to destroy the instance.

        Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#deletion_protection BigqueryTable#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The field description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#description BigqueryTable#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional["BigqueryTableEncryptionConfiguration"]:
        '''encryption_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#encryption_configuration BigqueryTable#encryption_configuration}
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional["BigqueryTableEncryptionConfiguration"], result)

    @builtins.property
    def expiration_time(self) -> typing.Optional[jsii.Number]:
        '''The time when this table expires, in milliseconds since the epoch.

        If not present, the table will persist indefinitely. Expired tables will be deleted and their storage reclaimed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#expiration_time BigqueryTable#expiration_time}
        '''
        result = self._values.get("expiration_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_data_configuration(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfiguration"]:
        '''external_data_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#external_data_configuration BigqueryTable#external_data_configuration}
        '''
        result = self._values.get("external_data_configuration")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfiguration"], result)

    @builtins.property
    def friendly_name(self) -> typing.Optional[builtins.str]:
        '''A descriptive name for the table.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#friendly_name BigqueryTable#friendly_name}
        '''
        result = self._values.get("friendly_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#id BigqueryTable#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of labels to assign to the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#labels BigqueryTable#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def materialized_view(self) -> typing.Optional["BigqueryTableMaterializedView"]:
        '''materialized_view block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#materialized_view BigqueryTable#materialized_view}
        '''
        result = self._values.get("materialized_view")
        return typing.cast(typing.Optional["BigqueryTableMaterializedView"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#project BigqueryTable#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_partitioning(self) -> typing.Optional["BigqueryTableRangePartitioning"]:
        '''range_partitioning block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#range_partitioning BigqueryTable#range_partitioning}
        '''
        result = self._values.get("range_partitioning")
        return typing.cast(typing.Optional["BigqueryTableRangePartitioning"], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''A JSON schema for the table.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#schema BigqueryTable#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_partitioning(self) -> typing.Optional["BigqueryTableTimePartitioning"]:
        '''time_partitioning block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#time_partitioning BigqueryTable#time_partitioning}
        '''
        result = self._values.get("time_partitioning")
        return typing.cast(typing.Optional["BigqueryTableTimePartitioning"], result)

    @builtins.property
    def view(self) -> typing.Optional["BigqueryTableView"]:
        '''view block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#view BigqueryTable#view}
        '''
        result = self._values.get("view")
        return typing.cast(typing.Optional["BigqueryTableView"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class BigqueryTableEncryptionConfiguration:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The self link or full name of a key which should be used to encrypt this table. Note that the default bigquery service account will need to have encrypt/decrypt permissions on this key - you may want to see the google_bigquery_default_service_account datasource and the google_kms_crypto_key_iam_binding resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#kms_key_name BigqueryTable#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b602152e3492b2b9cf562d37b34e16cd46fcdd5aebb8344fde8383837c318d)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''The self link or full name of a key which should be used to encrypt this table.

        Note that the default bigquery service account will need to have encrypt/decrypt permissions on this key - you may want to see the google_bigquery_default_service_account datasource and the google_kms_crypto_key_iam_binding resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#kms_key_name BigqueryTable#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af10cc39b5f5ba6eded054f31ffbd4706d4231d04b57aedc127bf4e576f255b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyVersion")
    def kms_key_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyVersion"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159555baf2bda86fb2b1cb4f203eb8889cd2ec3395162f7d34f6b3bf4bdb405a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableEncryptionConfiguration]:
        return typing.cast(typing.Optional[BigqueryTableEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fca302717ac54bb59f5552189434c71d9bec42d7b2a28bf6430bf5e7c4f8c84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "autodetect": "autodetect",
        "source_format": "sourceFormat",
        "source_uris": "sourceUris",
        "avro_options": "avroOptions",
        "compression": "compression",
        "connection_id": "connectionId",
        "csv_options": "csvOptions",
        "google_sheets_options": "googleSheetsOptions",
        "hive_partitioning_options": "hivePartitioningOptions",
        "ignore_unknown_values": "ignoreUnknownValues",
        "max_bad_records": "maxBadRecords",
        "schema": "schema",
    },
)
class BigqueryTableExternalDataConfiguration:
    def __init__(
        self,
        *,
        autodetect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        source_format: builtins.str,
        source_uris: typing.Sequence[builtins.str],
        avro_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationAvroOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        compression: typing.Optional[builtins.str] = None,
        connection_id: typing.Optional[builtins.str] = None,
        csv_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationCsvOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        google_sheets_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationGoogleSheetsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_partitioning_options: typing.Optional[typing.Union["BigqueryTableExternalDataConfigurationHivePartitioningOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        ignore_unknown_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_bad_records: typing.Optional[jsii.Number] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param autodetect: Let BigQuery try to autodetect the schema and format of the table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#autodetect BigqueryTable#autodetect}
        :param source_format: The data format. Supported values are: "CSV", "GOOGLE_SHEETS", "NEWLINE_DELIMITED_JSON", "AVRO", "PARQUET", "ORC" and "DATASTORE_BACKUP". To use "GOOGLE_SHEETS" the scopes must include "googleapis.com/auth/drive.readonly". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#source_format BigqueryTable#source_format}
        :param source_uris: A list of the fully-qualified URIs that point to your data in Google Cloud. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#source_uris BigqueryTable#source_uris}
        :param avro_options: avro_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#avro_options BigqueryTable#avro_options}
        :param compression: The compression type of the data source. Valid values are "NONE" or "GZIP". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#compression BigqueryTable#compression}
        :param connection_id: The connection specifying the credentials to be used to read external storage, such as Azure Blob, Cloud Storage, or S3. The connectionId can have the form "{{project}}.{{location}}.{{connection_id}}" or "projects/{{project}}/locations/{{location}}/connections/{{connection_id}}". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#connection_id BigqueryTable#connection_id}
        :param csv_options: csv_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#csv_options BigqueryTable#csv_options}
        :param google_sheets_options: google_sheets_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#google_sheets_options BigqueryTable#google_sheets_options}
        :param hive_partitioning_options: hive_partitioning_options block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#hive_partitioning_options BigqueryTable#hive_partitioning_options}
        :param ignore_unknown_values: Indicates if BigQuery should allow extra values that are not represented in the table schema. If true, the extra values are ignored. If false, records with extra columns are treated as bad records, and if there are too many bad records, an invalid error is returned in the job result. The default value is false. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#ignore_unknown_values BigqueryTable#ignore_unknown_values}
        :param max_bad_records: The maximum number of bad records that BigQuery can ignore when reading data. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#max_bad_records BigqueryTable#max_bad_records}
        :param schema: A JSON schema for the external table. Schema is required for CSV and JSON formats and is disallowed for Google Cloud Bigtable, Cloud Datastore backups, and Avro formats when using external tables. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#schema BigqueryTable#schema}
        '''
        if isinstance(avro_options, dict):
            avro_options = BigqueryTableExternalDataConfigurationAvroOptions(**avro_options)
        if isinstance(csv_options, dict):
            csv_options = BigqueryTableExternalDataConfigurationCsvOptions(**csv_options)
        if isinstance(google_sheets_options, dict):
            google_sheets_options = BigqueryTableExternalDataConfigurationGoogleSheetsOptions(**google_sheets_options)
        if isinstance(hive_partitioning_options, dict):
            hive_partitioning_options = BigqueryTableExternalDataConfigurationHivePartitioningOptions(**hive_partitioning_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c60ab8fdd68e02c385fb19a744285eb35baeda52e37f6cea6837e2b0f015c1)
            check_type(argname="argument autodetect", value=autodetect, expected_type=type_hints["autodetect"])
            check_type(argname="argument source_format", value=source_format, expected_type=type_hints["source_format"])
            check_type(argname="argument source_uris", value=source_uris, expected_type=type_hints["source_uris"])
            check_type(argname="argument avro_options", value=avro_options, expected_type=type_hints["avro_options"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument csv_options", value=csv_options, expected_type=type_hints["csv_options"])
            check_type(argname="argument google_sheets_options", value=google_sheets_options, expected_type=type_hints["google_sheets_options"])
            check_type(argname="argument hive_partitioning_options", value=hive_partitioning_options, expected_type=type_hints["hive_partitioning_options"])
            check_type(argname="argument ignore_unknown_values", value=ignore_unknown_values, expected_type=type_hints["ignore_unknown_values"])
            check_type(argname="argument max_bad_records", value=max_bad_records, expected_type=type_hints["max_bad_records"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autodetect": autodetect,
            "source_format": source_format,
            "source_uris": source_uris,
        }
        if avro_options is not None:
            self._values["avro_options"] = avro_options
        if compression is not None:
            self._values["compression"] = compression
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if csv_options is not None:
            self._values["csv_options"] = csv_options
        if google_sheets_options is not None:
            self._values["google_sheets_options"] = google_sheets_options
        if hive_partitioning_options is not None:
            self._values["hive_partitioning_options"] = hive_partitioning_options
        if ignore_unknown_values is not None:
            self._values["ignore_unknown_values"] = ignore_unknown_values
        if max_bad_records is not None:
            self._values["max_bad_records"] = max_bad_records
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def autodetect(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Let BigQuery try to autodetect the schema and format of the table.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#autodetect BigqueryTable#autodetect}
        '''
        result = self._values.get("autodetect")
        assert result is not None, "Required property 'autodetect' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def source_format(self) -> builtins.str:
        '''The data format.

        Supported values are: "CSV", "GOOGLE_SHEETS", "NEWLINE_DELIMITED_JSON", "AVRO", "PARQUET", "ORC" and "DATASTORE_BACKUP". To use "GOOGLE_SHEETS" the scopes must include "googleapis.com/auth/drive.readonly".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#source_format BigqueryTable#source_format}
        '''
        result = self._values.get("source_format")
        assert result is not None, "Required property 'source_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_uris(self) -> typing.List[builtins.str]:
        '''A list of the fully-qualified URIs that point to your data in Google Cloud.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#source_uris BigqueryTable#source_uris}
        '''
        result = self._values.get("source_uris")
        assert result is not None, "Required property 'source_uris' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def avro_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationAvroOptions"]:
        '''avro_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#avro_options BigqueryTable#avro_options}
        '''
        result = self._values.get("avro_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationAvroOptions"], result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''The compression type of the data source. Valid values are "NONE" or "GZIP".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#compression BigqueryTable#compression}
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        '''The connection specifying the credentials to be used to read external storage, such as Azure Blob, Cloud Storage, or S3.

        The connectionId can have the form "{{project}}.{{location}}.{{connection_id}}" or "projects/{{project}}/locations/{{location}}/connections/{{connection_id}}".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#connection_id BigqueryTable#connection_id}
        '''
        result = self._values.get("connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csv_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationCsvOptions"]:
        '''csv_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#csv_options BigqueryTable#csv_options}
        '''
        result = self._values.get("csv_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationCsvOptions"], result)

    @builtins.property
    def google_sheets_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationGoogleSheetsOptions"]:
        '''google_sheets_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#google_sheets_options BigqueryTable#google_sheets_options}
        '''
        result = self._values.get("google_sheets_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationGoogleSheetsOptions"], result)

    @builtins.property
    def hive_partitioning_options(
        self,
    ) -> typing.Optional["BigqueryTableExternalDataConfigurationHivePartitioningOptions"]:
        '''hive_partitioning_options block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#hive_partitioning_options BigqueryTable#hive_partitioning_options}
        '''
        result = self._values.get("hive_partitioning_options")
        return typing.cast(typing.Optional["BigqueryTableExternalDataConfigurationHivePartitioningOptions"], result)

    @builtins.property
    def ignore_unknown_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if BigQuery should allow extra values that are not represented in the table schema.

        If true, the extra values are ignored. If false, records with extra columns are treated as bad records, and if there are too many bad records, an invalid error is returned in the job result. The default value is false.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#ignore_unknown_values BigqueryTable#ignore_unknown_values}
        '''
        result = self._values.get("ignore_unknown_values")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_bad_records(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of bad records that BigQuery can ignore when reading data.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#max_bad_records BigqueryTable#max_bad_records}
        '''
        result = self._values.get("max_bad_records")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''A JSON schema for the external table.

        Schema is required for CSV and JSON formats and is disallowed for Google Cloud Bigtable, Cloud Datastore backups, and Avro formats when using external tables.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#schema BigqueryTable#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationAvroOptions",
    jsii_struct_bases=[],
    name_mapping={"use_avro_logical_types": "useAvroLogicalTypes"},
)
class BigqueryTableExternalDataConfigurationAvroOptions:
    def __init__(
        self,
        *,
        use_avro_logical_types: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param use_avro_logical_types: If sourceFormat is set to "AVRO", indicates whether to interpret logical types as the corresponding BigQuery data type (for example, TIMESTAMP), instead of using the raw type (for example, INTEGER). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#use_avro_logical_types BigqueryTable#use_avro_logical_types}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020a0a10768b90ca49555c5e7a89b9faabb072bc6d5bf986be581e51358bb59e)
            check_type(argname="argument use_avro_logical_types", value=use_avro_logical_types, expected_type=type_hints["use_avro_logical_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "use_avro_logical_types": use_avro_logical_types,
        }

    @builtins.property
    def use_avro_logical_types(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If sourceFormat is set to "AVRO", indicates whether to interpret logical types as the corresponding BigQuery data type (for example, TIMESTAMP), instead of using the raw type (for example, INTEGER).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#use_avro_logical_types BigqueryTable#use_avro_logical_types}
        '''
        result = self._values.get("use_avro_logical_types")
        assert result is not None, "Required property 'use_avro_logical_types' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationAvroOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationAvroOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationAvroOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9fd5bb8fb0dfbc052fe96da13cf662d0ad0a733594bb360e47c8249fcf45082)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="useAvroLogicalTypesInput")
    def use_avro_logical_types_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useAvroLogicalTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="useAvroLogicalTypes")
    def use_avro_logical_types(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useAvroLogicalTypes"))

    @use_avro_logical_types.setter
    def use_avro_logical_types(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be785777b38b52889c2672086fa4df78e5b5176f5807463eaa63b17717b5921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAvroLogicalTypes", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fcc8f040d82e48ec6840d2bc03598108e4065f5975b2f5eee455518f4ece75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationCsvOptions",
    jsii_struct_bases=[],
    name_mapping={
        "quote": "quote",
        "allow_jagged_rows": "allowJaggedRows",
        "allow_quoted_newlines": "allowQuotedNewlines",
        "encoding": "encoding",
        "field_delimiter": "fieldDelimiter",
        "skip_leading_rows": "skipLeadingRows",
    },
)
class BigqueryTableExternalDataConfigurationCsvOptions:
    def __init__(
        self,
        *,
        quote: builtins.str,
        allow_jagged_rows: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_quoted_newlines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        skip_leading_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param quote: The value that is used to quote data sections in a CSV file. If your data does not contain quoted sections, set the property value to an empty string. If your data contains quoted newline characters, you must also set the allow_quoted_newlines property to true. The API-side default is ", specified in Terraform escaped as ". Due to limitations with Terraform default values, this value is required to be explicitly set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#quote BigqueryTable#quote}
        :param allow_jagged_rows: Indicates if BigQuery should accept rows that are missing trailing optional columns. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#allow_jagged_rows BigqueryTable#allow_jagged_rows}
        :param allow_quoted_newlines: Indicates if BigQuery should allow quoted data sections that contain newline characters in a CSV file. The default value is false. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#allow_quoted_newlines BigqueryTable#allow_quoted_newlines}
        :param encoding: The character encoding of the data. The supported values are UTF-8 or ISO-8859-1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#encoding BigqueryTable#encoding}
        :param field_delimiter: The separator for fields in a CSV file. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#field_delimiter BigqueryTable#field_delimiter}
        :param skip_leading_rows: The number of rows at the top of a CSV file that BigQuery will skip when reading the data. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbe70f4df9985ff876e0f2ae8cd3f32cc7a5d0424dcd4f97052fc74b0e00937)
            check_type(argname="argument quote", value=quote, expected_type=type_hints["quote"])
            check_type(argname="argument allow_jagged_rows", value=allow_jagged_rows, expected_type=type_hints["allow_jagged_rows"])
            check_type(argname="argument allow_quoted_newlines", value=allow_quoted_newlines, expected_type=type_hints["allow_quoted_newlines"])
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument field_delimiter", value=field_delimiter, expected_type=type_hints["field_delimiter"])
            check_type(argname="argument skip_leading_rows", value=skip_leading_rows, expected_type=type_hints["skip_leading_rows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "quote": quote,
        }
        if allow_jagged_rows is not None:
            self._values["allow_jagged_rows"] = allow_jagged_rows
        if allow_quoted_newlines is not None:
            self._values["allow_quoted_newlines"] = allow_quoted_newlines
        if encoding is not None:
            self._values["encoding"] = encoding
        if field_delimiter is not None:
            self._values["field_delimiter"] = field_delimiter
        if skip_leading_rows is not None:
            self._values["skip_leading_rows"] = skip_leading_rows

    @builtins.property
    def quote(self) -> builtins.str:
        '''The value that is used to quote data sections in a CSV file.

        If your data does not contain quoted sections, set the property value to an empty string. If your data contains quoted newline characters, you must also set the allow_quoted_newlines property to true. The API-side default is ", specified in Terraform escaped as ". Due to limitations with Terraform default values, this value is required to be explicitly set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#quote BigqueryTable#quote}
        '''
        result = self._values.get("quote")
        assert result is not None, "Required property 'quote' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_jagged_rows(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if BigQuery should accept rows that are missing trailing optional columns.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#allow_jagged_rows BigqueryTable#allow_jagged_rows}
        '''
        result = self._values.get("allow_jagged_rows")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_quoted_newlines(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if BigQuery should allow quoted data sections that contain newline characters in a CSV file.

        The default value is false.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#allow_quoted_newlines BigqueryTable#allow_quoted_newlines}
        '''
        result = self._values.get("allow_quoted_newlines")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The character encoding of the data. The supported values are UTF-8 or ISO-8859-1.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#encoding BigqueryTable#encoding}
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_delimiter(self) -> typing.Optional[builtins.str]:
        '''The separator for fields in a CSV file.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#field_delimiter BigqueryTable#field_delimiter}
        '''
        result = self._values.get("field_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_leading_rows(self) -> typing.Optional[jsii.Number]:
        '''The number of rows at the top of a CSV file that BigQuery will skip when reading the data.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        result = self._values.get("skip_leading_rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationCsvOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationCsvOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationCsvOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f60af4fc24e71e637c6fa900482563f246e261e062f3062c295a2bad98420962)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowJaggedRows")
    def reset_allow_jagged_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowJaggedRows", []))

    @jsii.member(jsii_name="resetAllowQuotedNewlines")
    def reset_allow_quoted_newlines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowQuotedNewlines", []))

    @jsii.member(jsii_name="resetEncoding")
    def reset_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncoding", []))

    @jsii.member(jsii_name="resetFieldDelimiter")
    def reset_field_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldDelimiter", []))

    @jsii.member(jsii_name="resetSkipLeadingRows")
    def reset_skip_leading_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipLeadingRows", []))

    @builtins.property
    @jsii.member(jsii_name="allowJaggedRowsInput")
    def allow_jagged_rows_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowJaggedRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowQuotedNewlinesInput")
    def allow_quoted_newlines_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowQuotedNewlinesInput"))

    @builtins.property
    @jsii.member(jsii_name="encodingInput")
    def encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encodingInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiterInput")
    def field_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="quoteInput")
    def quote_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quoteInput"))

    @builtins.property
    @jsii.member(jsii_name="skipLeadingRowsInput")
    def skip_leading_rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "skipLeadingRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowJaggedRows")
    def allow_jagged_rows(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowJaggedRows"))

    @allow_jagged_rows.setter
    def allow_jagged_rows(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e73d09915846f7821d69bbaafe21042ed21254594e34719c29494cb50b3a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowJaggedRows", value)

    @builtins.property
    @jsii.member(jsii_name="allowQuotedNewlines")
    def allow_quoted_newlines(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowQuotedNewlines"))

    @allow_quoted_newlines.setter
    def allow_quoted_newlines(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e69d30776a200962cdf1ae7dbfec1ed9bc8dd3a8bbc993e020ff52eee4a4e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowQuotedNewlines", value)

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @encoding.setter
    def encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a97b74c86bec5163696d29826bf6274501cc5d15f5a8981eecd353bafe0ad6d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encoding", value)

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiter")
    def field_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldDelimiter"))

    @field_delimiter.setter
    def field_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4ef4f6ceb6adf5f5e4f857fe2a3abfa9551e8515e1c01b43f46ad903e65a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldDelimiter", value)

    @builtins.property
    @jsii.member(jsii_name="quote")
    def quote(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quote"))

    @quote.setter
    def quote(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c97c66ebe5dd4be082754498f497e0dd3a039989089797867763631092e415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quote", value)

    @builtins.property
    @jsii.member(jsii_name="skipLeadingRows")
    def skip_leading_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "skipLeadingRows"))

    @skip_leading_rows.setter
    def skip_leading_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750a54e77026baaefd7596886e1ff0599ce1f18278039fa40bd4ab7b0e00e47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipLeadingRows", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49253d1d598fd8a759e5fb7260bd43f838344fc041171c17e9fdb960f0bca7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationGoogleSheetsOptions",
    jsii_struct_bases=[],
    name_mapping={"range": "range", "skip_leading_rows": "skipLeadingRows"},
)
class BigqueryTableExternalDataConfigurationGoogleSheetsOptions:
    def __init__(
        self,
        *,
        range: typing.Optional[builtins.str] = None,
        skip_leading_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param range: Range of a sheet to query from. Only used when non-empty. At least one of range or skip_leading_rows must be set. Typical format: "sheet_name!top_left_cell_id:bottom_right_cell_id" For example: "sheet1!A1:B20" Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#range BigqueryTable#range}
        :param skip_leading_rows: The number of rows at the top of the sheet that BigQuery will skip when reading the data. At least one of range or skip_leading_rows must be set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d038f67db09f696cd8f12f3dd998ac5d9aaa643c029b6323a5865470d5e1bb13)
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument skip_leading_rows", value=skip_leading_rows, expected_type=type_hints["skip_leading_rows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if range is not None:
            self._values["range"] = range
        if skip_leading_rows is not None:
            self._values["skip_leading_rows"] = skip_leading_rows

    @builtins.property
    def range(self) -> typing.Optional[builtins.str]:
        '''Range of a sheet to query from.

        Only used when non-empty. At least one of range or skip_leading_rows must be set. Typical format: "sheet_name!top_left_cell_id:bottom_right_cell_id" For example: "sheet1!A1:B20"

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#range BigqueryTable#range}
        '''
        result = self._values.get("range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_leading_rows(self) -> typing.Optional[jsii.Number]:
        '''The number of rows at the top of the sheet that BigQuery will skip when reading the data.

        At least one of range or skip_leading_rows must be set.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        result = self._values.get("skip_leading_rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationGoogleSheetsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationGoogleSheetsOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationGoogleSheetsOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdc19019d32a22a60c6a9ca6c1e9a76258e4553f4456f2df92bef8f673d7390c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRange")
    def reset_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRange", []))

    @jsii.member(jsii_name="resetSkipLeadingRows")
    def reset_skip_leading_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipLeadingRows", []))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="skipLeadingRowsInput")
    def skip_leading_rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "skipLeadingRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "range"))

    @range.setter
    def range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37f5f39bd5216808ff0bfd8dfaf4e99a1f1c79731e27bae75778a2d3136bea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "range", value)

    @builtins.property
    @jsii.member(jsii_name="skipLeadingRows")
    def skip_leading_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "skipLeadingRows"))

    @skip_leading_rows.setter
    def skip_leading_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52592b7fc99331f5d59d8b9949f4a4ec26a81695186d39a91dc86b408c9263e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipLeadingRows", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74e3e17939cb2af1a1dda80388692345f22ee6e9ebbbc005cef5c75e631246d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationHivePartitioningOptions",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "require_partition_filter": "requirePartitionFilter",
        "source_uri_prefix": "sourceUriPrefix",
    },
)
class BigqueryTableExternalDataConfigurationHivePartitioningOptions:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_uri_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: When set, what mode of hive partitioning to use when reading data. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#mode BigqueryTable#mode}
        :param require_partition_filter: If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        :param source_uri_prefix: When hive partition detection is requested, a common for all source uris must be required. The prefix must end immediately before the partition key encoding begins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#source_uri_prefix BigqueryTable#source_uri_prefix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810784a6342c4175b64b73278d9e89558c903464868b3a31434d1454105155a7)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument require_partition_filter", value=require_partition_filter, expected_type=type_hints["require_partition_filter"])
            check_type(argname="argument source_uri_prefix", value=source_uri_prefix, expected_type=type_hints["source_uri_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if require_partition_filter is not None:
            self._values["require_partition_filter"] = require_partition_filter
        if source_uri_prefix is not None:
            self._values["source_uri_prefix"] = source_uri_prefix

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''When set, what mode of hive partitioning to use when reading data.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#mode BigqueryTable#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_partition_filter(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        '''
        result = self._values.get("require_partition_filter")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_uri_prefix(self) -> typing.Optional[builtins.str]:
        '''When hive partition detection is requested, a common for all source uris must be required.

        The prefix must end immediately before the partition key encoding begins.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#source_uri_prefix BigqueryTable#source_uri_prefix}
        '''
        result = self._values.get("source_uri_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableExternalDataConfigurationHivePartitioningOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableExternalDataConfigurationHivePartitioningOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationHivePartitioningOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__427d241048413617b3bd3a828418f1d0ac690b71dfe0d2e2068199e9bddd2441)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetRequirePartitionFilter")
    def reset_require_partition_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequirePartitionFilter", []))

    @jsii.member(jsii_name="resetSourceUriPrefix")
    def reset_source_uri_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceUriPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="requirePartitionFilterInput")
    def require_partition_filter_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requirePartitionFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceUriPrefixInput")
    def source_uri_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceUriPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01a839fea9d2d522ebdb2c7d2a742aa9480bdbd7bb8032c9a1cb98fb08540e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="requirePartitionFilter")
    def require_partition_filter(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requirePartitionFilter"))

    @require_partition_filter.setter
    def require_partition_filter(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a766f84b3d43b2709c94c8f8521d26c341493a08ed89bef1a658cffcf736efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirePartitionFilter", value)

    @builtins.property
    @jsii.member(jsii_name="sourceUriPrefix")
    def source_uri_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUriPrefix"))

    @source_uri_prefix.setter
    def source_uri_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece8fc4dc9da2b45528b8120676c44420820ae71ca2379a6b811788655de2ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUriPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ea00c1a595be450f340f82ebd3b57198a01adae42a7d6bd7aa2a43f9bfbeb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BigqueryTableExternalDataConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableExternalDataConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aedd3ec19da32a66f5345c97d51ab2ec0daa172ece609031aadaa848060186d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAvroOptions")
    def put_avro_options(
        self,
        *,
        use_avro_logical_types: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param use_avro_logical_types: If sourceFormat is set to "AVRO", indicates whether to interpret logical types as the corresponding BigQuery data type (for example, TIMESTAMP), instead of using the raw type (for example, INTEGER). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#use_avro_logical_types BigqueryTable#use_avro_logical_types}
        '''
        value = BigqueryTableExternalDataConfigurationAvroOptions(
            use_avro_logical_types=use_avro_logical_types
        )

        return typing.cast(None, jsii.invoke(self, "putAvroOptions", [value]))

    @jsii.member(jsii_name="putCsvOptions")
    def put_csv_options(
        self,
        *,
        quote: builtins.str,
        allow_jagged_rows: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_quoted_newlines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encoding: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        skip_leading_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param quote: The value that is used to quote data sections in a CSV file. If your data does not contain quoted sections, set the property value to an empty string. If your data contains quoted newline characters, you must also set the allow_quoted_newlines property to true. The API-side default is ", specified in Terraform escaped as ". Due to limitations with Terraform default values, this value is required to be explicitly set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#quote BigqueryTable#quote}
        :param allow_jagged_rows: Indicates if BigQuery should accept rows that are missing trailing optional columns. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#allow_jagged_rows BigqueryTable#allow_jagged_rows}
        :param allow_quoted_newlines: Indicates if BigQuery should allow quoted data sections that contain newline characters in a CSV file. The default value is false. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#allow_quoted_newlines BigqueryTable#allow_quoted_newlines}
        :param encoding: The character encoding of the data. The supported values are UTF-8 or ISO-8859-1. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#encoding BigqueryTable#encoding}
        :param field_delimiter: The separator for fields in a CSV file. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#field_delimiter BigqueryTable#field_delimiter}
        :param skip_leading_rows: The number of rows at the top of a CSV file that BigQuery will skip when reading the data. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        value = BigqueryTableExternalDataConfigurationCsvOptions(
            quote=quote,
            allow_jagged_rows=allow_jagged_rows,
            allow_quoted_newlines=allow_quoted_newlines,
            encoding=encoding,
            field_delimiter=field_delimiter,
            skip_leading_rows=skip_leading_rows,
        )

        return typing.cast(None, jsii.invoke(self, "putCsvOptions", [value]))

    @jsii.member(jsii_name="putGoogleSheetsOptions")
    def put_google_sheets_options(
        self,
        *,
        range: typing.Optional[builtins.str] = None,
        skip_leading_rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param range: Range of a sheet to query from. Only used when non-empty. At least one of range or skip_leading_rows must be set. Typical format: "sheet_name!top_left_cell_id:bottom_right_cell_id" For example: "sheet1!A1:B20" Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#range BigqueryTable#range}
        :param skip_leading_rows: The number of rows at the top of the sheet that BigQuery will skip when reading the data. At least one of range or skip_leading_rows must be set. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#skip_leading_rows BigqueryTable#skip_leading_rows}
        '''
        value = BigqueryTableExternalDataConfigurationGoogleSheetsOptions(
            range=range, skip_leading_rows=skip_leading_rows
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleSheetsOptions", [value]))

    @jsii.member(jsii_name="putHivePartitioningOptions")
    def put_hive_partitioning_options(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_uri_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: When set, what mode of hive partitioning to use when reading data. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#mode BigqueryTable#mode}
        :param require_partition_filter: If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        :param source_uri_prefix: When hive partition detection is requested, a common for all source uris must be required. The prefix must end immediately before the partition key encoding begins. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#source_uri_prefix BigqueryTable#source_uri_prefix}
        '''
        value = BigqueryTableExternalDataConfigurationHivePartitioningOptions(
            mode=mode,
            require_partition_filter=require_partition_filter,
            source_uri_prefix=source_uri_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putHivePartitioningOptions", [value]))

    @jsii.member(jsii_name="resetAvroOptions")
    def reset_avro_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvroOptions", []))

    @jsii.member(jsii_name="resetCompression")
    def reset_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompression", []))

    @jsii.member(jsii_name="resetConnectionId")
    def reset_connection_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionId", []))

    @jsii.member(jsii_name="resetCsvOptions")
    def reset_csv_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsvOptions", []))

    @jsii.member(jsii_name="resetGoogleSheetsOptions")
    def reset_google_sheets_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleSheetsOptions", []))

    @jsii.member(jsii_name="resetHivePartitioningOptions")
    def reset_hive_partitioning_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHivePartitioningOptions", []))

    @jsii.member(jsii_name="resetIgnoreUnknownValues")
    def reset_ignore_unknown_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreUnknownValues", []))

    @jsii.member(jsii_name="resetMaxBadRecords")
    def reset_max_bad_records(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBadRecords", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @builtins.property
    @jsii.member(jsii_name="avroOptions")
    def avro_options(
        self,
    ) -> BigqueryTableExternalDataConfigurationAvroOptionsOutputReference:
        return typing.cast(BigqueryTableExternalDataConfigurationAvroOptionsOutputReference, jsii.get(self, "avroOptions"))

    @builtins.property
    @jsii.member(jsii_name="csvOptions")
    def csv_options(
        self,
    ) -> BigqueryTableExternalDataConfigurationCsvOptionsOutputReference:
        return typing.cast(BigqueryTableExternalDataConfigurationCsvOptionsOutputReference, jsii.get(self, "csvOptions"))

    @builtins.property
    @jsii.member(jsii_name="googleSheetsOptions")
    def google_sheets_options(
        self,
    ) -> BigqueryTableExternalDataConfigurationGoogleSheetsOptionsOutputReference:
        return typing.cast(BigqueryTableExternalDataConfigurationGoogleSheetsOptionsOutputReference, jsii.get(self, "googleSheetsOptions"))

    @builtins.property
    @jsii.member(jsii_name="hivePartitioningOptions")
    def hive_partitioning_options(
        self,
    ) -> BigqueryTableExternalDataConfigurationHivePartitioningOptionsOutputReference:
        return typing.cast(BigqueryTableExternalDataConfigurationHivePartitioningOptionsOutputReference, jsii.get(self, "hivePartitioningOptions"))

    @builtins.property
    @jsii.member(jsii_name="autodetectInput")
    def autodetect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autodetectInput"))

    @builtins.property
    @jsii.member(jsii_name="avroOptionsInput")
    def avro_options_input(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions], jsii.get(self, "avroOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionInput")
    def compression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionIdInput")
    def connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="csvOptionsInput")
    def csv_options_input(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions], jsii.get(self, "csvOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="googleSheetsOptionsInput")
    def google_sheets_options_input(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions], jsii.get(self, "googleSheetsOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="hivePartitioningOptionsInput")
    def hive_partitioning_options_input(
        self,
    ) -> typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions], jsii.get(self, "hivePartitioningOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreUnknownValuesInput")
    def ignore_unknown_values_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreUnknownValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBadRecordsInput")
    def max_bad_records_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBadRecordsInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFormatInput")
    def source_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceUrisInput")
    def source_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="autodetect")
    def autodetect(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autodetect"))

    @autodetect.setter
    def autodetect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa92013cd8c6f4654573bca59cada4acf1ab4fa24e0c33e4d4183250eea524a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autodetect", value)

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171e466428ef05f4c723a94ae4be4749554bd2eea5cd174382809e39dc1531e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value)

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b513971418e35e0889daa1af0c24cd9d68fe2c0c11f24a4107c11bdd933e16b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionId", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreUnknownValues")
    def ignore_unknown_values(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreUnknownValues"))

    @ignore_unknown_values.setter
    def ignore_unknown_values(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a59007098ead2bf4df9dc5cfcdcf21549a84089fbee66a5e258d3fd9a97d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreUnknownValues", value)

    @builtins.property
    @jsii.member(jsii_name="maxBadRecords")
    def max_bad_records(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBadRecords"))

    @max_bad_records.setter
    def max_bad_records(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d69f7654bb9a49339cdf5f1425dadb79c83dad7cad0ee4c0b95ee260bcf1b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBadRecords", value)

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0884b65b0bdd6567b088bb09c59a013f1c64f0c864984a8075b6a4e371875e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="sourceFormat")
    def source_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFormat"))

    @source_format.setter
    def source_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a03112d506997097f3ea5d211e0cd0d133f64fde4a35c3bc1ceafc857b28a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFormat", value)

    @builtins.property
    @jsii.member(jsii_name="sourceUris")
    def source_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceUris"))

    @source_uris.setter
    def source_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2411a1cf8a70ffbcaa7d39b40a4d65c9ac8a09f10bddc890f5e9f3dfa59fd1c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUris", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableExternalDataConfiguration]:
        return typing.cast(typing.Optional[BigqueryTableExternalDataConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableExternalDataConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a895f0de550b51ae084bc84300b10c9de0fb66c609b0968fc28545ce0c6a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableMaterializedView",
    jsii_struct_bases=[],
    name_mapping={
        "query": "query",
        "enable_refresh": "enableRefresh",
        "refresh_interval_ms": "refreshIntervalMs",
    },
)
class BigqueryTableMaterializedView:
    def __init__(
        self,
        *,
        query: builtins.str,
        enable_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        refresh_interval_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: A query whose result is persisted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#query BigqueryTable#query}
        :param enable_refresh: Specifies if BigQuery should automatically refresh materialized view when the base table is updated. The default is true. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#enable_refresh BigqueryTable#enable_refresh}
        :param refresh_interval_ms: Specifies maximum frequency at which this materialized view will be refreshed. The default is 1800000. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#refresh_interval_ms BigqueryTable#refresh_interval_ms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78bfac7ffc7a9089b8ef1d3b22082c499bb74076ee32063e98bfc14ba774af19)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument enable_refresh", value=enable_refresh, expected_type=type_hints["enable_refresh"])
            check_type(argname="argument refresh_interval_ms", value=refresh_interval_ms, expected_type=type_hints["refresh_interval_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if enable_refresh is not None:
            self._values["enable_refresh"] = enable_refresh
        if refresh_interval_ms is not None:
            self._values["refresh_interval_ms"] = refresh_interval_ms

    @builtins.property
    def query(self) -> builtins.str:
        '''A query whose result is persisted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#query BigqueryTable#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_refresh(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if BigQuery should automatically refresh materialized view when the base table is updated. The default is true.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#enable_refresh BigqueryTable#enable_refresh}
        '''
        result = self._values.get("enable_refresh")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def refresh_interval_ms(self) -> typing.Optional[jsii.Number]:
        '''Specifies maximum frequency at which this materialized view will be refreshed. The default is 1800000.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#refresh_interval_ms BigqueryTable#refresh_interval_ms}
        '''
        result = self._values.get("refresh_interval_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableMaterializedView(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableMaterializedViewOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableMaterializedViewOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a06199473432610a340d54e912a27a45d9838f276f5ddefb8ea5ed442551b84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableRefresh")
    def reset_enable_refresh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableRefresh", []))

    @jsii.member(jsii_name="resetRefreshIntervalMs")
    def reset_refresh_interval_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshIntervalMs", []))

    @builtins.property
    @jsii.member(jsii_name="enableRefreshInput")
    def enable_refresh_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableRefreshInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshIntervalMsInput")
    def refresh_interval_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "refreshIntervalMsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableRefresh")
    def enable_refresh(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableRefresh"))

    @enable_refresh.setter
    def enable_refresh(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95c47f7821838b81eb06f48bf5b0c5aed91c07011b4d48d8073fce2186f17bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRefresh", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9fea0c74fd4684d8ad56faaf0179f2f5bb721644dff852d3e6979f302106755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="refreshIntervalMs")
    def refresh_interval_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "refreshIntervalMs"))

    @refresh_interval_ms.setter
    def refresh_interval_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9657a3990dc569b85efe467953e2b35134c6d571e8a9003d13db7d882c11d771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshIntervalMs", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableMaterializedView]:
        return typing.cast(typing.Optional[BigqueryTableMaterializedView], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableMaterializedView],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35804a2287301e8b044546610ce9f0fb372c6b235f2ade6d86c3105305e0f8c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableRangePartitioning",
    jsii_struct_bases=[],
    name_mapping={"field": "field", "range": "range"},
)
class BigqueryTableRangePartitioning:
    def __init__(
        self,
        *,
        field: builtins.str,
        range: typing.Union["BigqueryTableRangePartitioningRange", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param field: The field used to determine how to create a range-based partition. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#field BigqueryTable#field}
        :param range: range block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#range BigqueryTable#range}
        '''
        if isinstance(range, dict):
            range = BigqueryTableRangePartitioningRange(**range)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cdcc485551cdda9350f0ec3b6f635fb181dfeb360e8a64dc8017a129edb17bf)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field": field,
            "range": range,
        }

    @builtins.property
    def field(self) -> builtins.str:
        '''The field used to determine how to create a range-based partition.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#field BigqueryTable#field}
        '''
        result = self._values.get("field")
        assert result is not None, "Required property 'field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def range(self) -> "BigqueryTableRangePartitioningRange":
        '''range block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#range BigqueryTable#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast("BigqueryTableRangePartitioningRange", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableRangePartitioning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableRangePartitioningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableRangePartitioningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5846667bda1a92cfa7b2128c33f2548d65ee779e39fcfee01fc1ed16c3071bdc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRange")
    def put_range(
        self,
        *,
        end: jsii.Number,
        interval: jsii.Number,
        start: jsii.Number,
    ) -> None:
        '''
        :param end: End of the range partitioning, exclusive. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#end BigqueryTable#end}
        :param interval: The width of each range within the partition. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#interval BigqueryTable#interval}
        :param start: Start of the range partitioning, inclusive. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#start BigqueryTable#start}
        '''
        value = BigqueryTableRangePartitioningRange(
            end=end, interval=interval, start=start
        )

        return typing.cast(None, jsii.invoke(self, "putRange", [value]))

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> "BigqueryTableRangePartitioningRangeOutputReference":
        return typing.cast("BigqueryTableRangePartitioningRangeOutputReference", jsii.get(self, "range"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(self) -> typing.Optional["BigqueryTableRangePartitioningRange"]:
        return typing.cast(typing.Optional["BigqueryTableRangePartitioningRange"], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395c6f6f36489faff4acf790a2a2cc1c21f8f9966c5ef9a170a50199315505e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableRangePartitioning]:
        return typing.cast(typing.Optional[BigqueryTableRangePartitioning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableRangePartitioning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ed36eb55e507419b8535e2c7cafa45c85bff6123571a8edb4886a44bacae48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableRangePartitioningRange",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "interval": "interval", "start": "start"},
)
class BigqueryTableRangePartitioningRange:
    def __init__(
        self,
        *,
        end: jsii.Number,
        interval: jsii.Number,
        start: jsii.Number,
    ) -> None:
        '''
        :param end: End of the range partitioning, exclusive. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#end BigqueryTable#end}
        :param interval: The width of each range within the partition. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#interval BigqueryTable#interval}
        :param start: Start of the range partitioning, inclusive. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#start BigqueryTable#start}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69572fe55635746c6c943f6472627f9914d257e914d14e8158134965b8a38fb4)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "interval": interval,
            "start": start,
        }

    @builtins.property
    def end(self) -> jsii.Number:
        '''End of the range partitioning, exclusive.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#end BigqueryTable#end}
        '''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval(self) -> jsii.Number:
        '''The width of each range within the partition.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#interval BigqueryTable#interval}
        '''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start(self) -> jsii.Number:
        '''Start of the range partitioning, inclusive.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#start BigqueryTable#start}
        '''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableRangePartitioningRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableRangePartitioningRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableRangePartitioningRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e346b07c1bf2602c604ad14a57886686548a1aa4a51a38351b11b562dc21085)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "end"))

    @end.setter
    def end(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2b695fdea4b4df8ca95b67883601572c7925871a37b6a6422ddb8f986cab0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value)

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3633200eb7491ca91f5312d0e52d612aafd64c3a611f85726166d54ad0765116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value)

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f689dce76260a1d7c60657cf8bca91a3d9a497d6f1788949e150195b1c9820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableRangePartitioningRange]:
        return typing.cast(typing.Optional[BigqueryTableRangePartitioningRange], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableRangePartitioningRange],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19729f38363279736c21ff6e0255ab435dae55bb7e61e454e836a44d18820d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTimePartitioning",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "expiration_ms": "expirationMs",
        "field": "field",
        "require_partition_filter": "requirePartitionFilter",
    },
)
class BigqueryTableTimePartitioning:
    def __init__(
        self,
        *,
        type: builtins.str,
        expiration_ms: typing.Optional[jsii.Number] = None,
        field: typing.Optional[builtins.str] = None,
        require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param type: The supported types are DAY, HOUR, MONTH, and YEAR, which will generate one partition per day, hour, month, and year, respectively. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#type BigqueryTable#type}
        :param expiration_ms: Number of milliseconds for which to keep the storage for a partition. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#expiration_ms BigqueryTable#expiration_ms}
        :param field: The field used to determine how to create a time-based partition. If time-based partitioning is enabled without this value, the table is partitioned based on the load time. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#field BigqueryTable#field}
        :param require_partition_filter: If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb89c8f47dc2aa75c98d1b70fe727492265de34a7f04fcc70fb2ac919a4b609)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument expiration_ms", value=expiration_ms, expected_type=type_hints["expiration_ms"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument require_partition_filter", value=require_partition_filter, expected_type=type_hints["require_partition_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if expiration_ms is not None:
            self._values["expiration_ms"] = expiration_ms
        if field is not None:
            self._values["field"] = field
        if require_partition_filter is not None:
            self._values["require_partition_filter"] = require_partition_filter

    @builtins.property
    def type(self) -> builtins.str:
        '''The supported types are DAY, HOUR, MONTH, and YEAR, which will generate one partition per day, hour, month, and year, respectively.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#type BigqueryTable#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_ms(self) -> typing.Optional[jsii.Number]:
        '''Number of milliseconds for which to keep the storage for a partition.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#expiration_ms BigqueryTable#expiration_ms}
        '''
        result = self._values.get("expiration_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def field(self) -> typing.Optional[builtins.str]:
        '''The field used to determine how to create a time-based partition.

        If time-based partitioning is enabled without this value, the table is partitioned based on the load time.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#field BigqueryTable#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_partition_filter(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#require_partition_filter BigqueryTable#require_partition_filter}
        '''
        result = self._values.get("require_partition_filter")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableTimePartitioning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableTimePartitioningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableTimePartitioningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bb1012c6f07e275e2c7ac99db9bd6af2dbbbe5b56308e74d8073d34cf791a6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExpirationMs")
    def reset_expiration_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationMs", []))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @jsii.member(jsii_name="resetRequirePartitionFilter")
    def reset_require_partition_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequirePartitionFilter", []))

    @builtins.property
    @jsii.member(jsii_name="expirationMsInput")
    def expiration_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expirationMsInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="requirePartitionFilterInput")
    def require_partition_filter_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requirePartitionFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationMs")
    def expiration_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expirationMs"))

    @expiration_ms.setter
    def expiration_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463cb583811d7bce632cdacc04ef7a813a9464f2fd0935bdb317acbdf50877af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationMs", value)

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9f1f7e339594c721b212be7ee4b6441e2e4cfba1f61b12bb2bf75f78fa8edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value)

    @builtins.property
    @jsii.member(jsii_name="requirePartitionFilter")
    def require_partition_filter(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requirePartitionFilter"))

    @require_partition_filter.setter
    def require_partition_filter(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d848604fbd9c70477cd62b8b91073abca4ee3d39caf376d82ad8cb379f3295c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirePartitionFilter", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e229f2df185e40b0ee1aec2c292b2f480e52700cd9e7d4e30c50fd2871166f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableTimePartitioning]:
        return typing.cast(typing.Optional[BigqueryTableTimePartitioning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryTableTimePartitioning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57aa79d96b36de527ea884cebcfcccaa556f71725930521bec3778b8be50e098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableView",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "use_legacy_sql": "useLegacySql"},
)
class BigqueryTableView:
    def __init__(
        self,
        *,
        query: builtins.str,
        use_legacy_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query: A query that BigQuery executes when the view is referenced. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#query BigqueryTable#query}
        :param use_legacy_sql: Specifies whether to use BigQuery's legacy SQL for this view. The default value is true. If set to false, the view will use BigQuery's standard SQL Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#use_legacy_sql BigqueryTable#use_legacy_sql}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a3916e2251c4ce938996c4d3230e60885f992563fbccd7813ffeeaec1eeada)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument use_legacy_sql", value=use_legacy_sql, expected_type=type_hints["use_legacy_sql"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if use_legacy_sql is not None:
            self._values["use_legacy_sql"] = use_legacy_sql

    @builtins.property
    def query(self) -> builtins.str:
        '''A query that BigQuery executes when the view is referenced.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#query BigqueryTable#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_legacy_sql(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to use BigQuery's legacy SQL for this view.

        The default value is true. If set to false, the view will use BigQuery's standard SQL

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_table#use_legacy_sql BigqueryTable#use_legacy_sql}
        '''
        result = self._values.get("use_legacy_sql")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryTableView(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryTableViewOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryTable.BigqueryTableViewOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5d3a89bee4916b9695c0ff59eb7dadc6367caaf6a57673b503046edf0dcc9bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUseLegacySql")
    def reset_use_legacy_sql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseLegacySql", []))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="useLegacySqlInput")
    def use_legacy_sql_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useLegacySqlInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722fbc23443a9a33d97f796a37943d92c33e8b32289d7ca8d1190dbf88ecbdea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="useLegacySql")
    def use_legacy_sql(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useLegacySql"))

    @use_legacy_sql.setter
    def use_legacy_sql(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7d9b7655097a8ae61f21e1a58fea8369d86360dab40227def1947e1e1193ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useLegacySql", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryTableView]:
        return typing.cast(typing.Optional[BigqueryTableView], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BigqueryTableView]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7686a49feb74dbf2c8805b0999264b2707d637196b1090f8df1405c64fa0fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "BigqueryTable",
    "BigqueryTableConfig",
    "BigqueryTableEncryptionConfiguration",
    "BigqueryTableEncryptionConfigurationOutputReference",
    "BigqueryTableExternalDataConfiguration",
    "BigqueryTableExternalDataConfigurationAvroOptions",
    "BigqueryTableExternalDataConfigurationAvroOptionsOutputReference",
    "BigqueryTableExternalDataConfigurationCsvOptions",
    "BigqueryTableExternalDataConfigurationCsvOptionsOutputReference",
    "BigqueryTableExternalDataConfigurationGoogleSheetsOptions",
    "BigqueryTableExternalDataConfigurationGoogleSheetsOptionsOutputReference",
    "BigqueryTableExternalDataConfigurationHivePartitioningOptions",
    "BigqueryTableExternalDataConfigurationHivePartitioningOptionsOutputReference",
    "BigqueryTableExternalDataConfigurationOutputReference",
    "BigqueryTableMaterializedView",
    "BigqueryTableMaterializedViewOutputReference",
    "BigqueryTableRangePartitioning",
    "BigqueryTableRangePartitioningOutputReference",
    "BigqueryTableRangePartitioningRange",
    "BigqueryTableRangePartitioningRangeOutputReference",
    "BigqueryTableTimePartitioning",
    "BigqueryTableTimePartitioningOutputReference",
    "BigqueryTableView",
    "BigqueryTableViewOutputReference",
]

publication.publish()

def _typecheckingstub__b097032883d450d5b0dd2683567f8b829165b537d5a8be476cbb660ce43d5747(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset_id: builtins.str,
    table_id: builtins.str,
    clustering: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[BigqueryTableEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    expiration_time: typing.Optional[jsii.Number] = None,
    external_data_configuration: typing.Optional[typing.Union[BigqueryTableExternalDataConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    materialized_view: typing.Optional[typing.Union[BigqueryTableMaterializedView, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    range_partitioning: typing.Optional[typing.Union[BigqueryTableRangePartitioning, typing.Dict[builtins.str, typing.Any]]] = None,
    schema: typing.Optional[builtins.str] = None,
    time_partitioning: typing.Optional[typing.Union[BigqueryTableTimePartitioning, typing.Dict[builtins.str, typing.Any]]] = None,
    view: typing.Optional[typing.Union[BigqueryTableView, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c36a827767218e30e15ed46c620f1d6ac1649ac81e9a1f8fbf50b44994a8de7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ba56c49b068bbf8763ea0042060807cbf89b0406ef980ed1fc45513c07dca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62578b34b021403200b1036268e3acd655157cb771a72f5d129bf260f4c27cf2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c0bfe985825d9a80acd8f5aefedd8901d464dacf94af409b2a81efccfc3fef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5413b10f3ec29a1d03f7c2f42f492fee9e3d71fa450c28d4bd6f46ef3ef51e77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b95bd39489b26bd16347f815db6f92fba878214004df53fa734ec6f798849ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af66ed510248d931e4bb1f43b218cca02cd6069e76f18cdb7150e9530186201(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c74889bf00ce24f484abd1bc28bf3cf7d61665b2ab8f55381086fce8f1291c4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1a6d53539cb352313127bc88400bfb27109837e44e77e3c2445bb3a3ceaa22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570adc90f3ed8491972bb571ec80eb5f0b0fdf5931d71a249e93fd1f993d7b40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ff67f97457c05dfe2bdc38c7d1b6d4d3ab19d3aed9a3b6ab5e87619edf6da4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a75785b12d60945a47678d02ebd6a12a808d31eb6207fa82349d07fd479f943(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset_id: builtins.str,
    table_id: builtins.str,
    clustering: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[BigqueryTableEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    expiration_time: typing.Optional[jsii.Number] = None,
    external_data_configuration: typing.Optional[typing.Union[BigqueryTableExternalDataConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    materialized_view: typing.Optional[typing.Union[BigqueryTableMaterializedView, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    range_partitioning: typing.Optional[typing.Union[BigqueryTableRangePartitioning, typing.Dict[builtins.str, typing.Any]]] = None,
    schema: typing.Optional[builtins.str] = None,
    time_partitioning: typing.Optional[typing.Union[BigqueryTableTimePartitioning, typing.Dict[builtins.str, typing.Any]]] = None,
    view: typing.Optional[typing.Union[BigqueryTableView, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b602152e3492b2b9cf562d37b34e16cd46fcdd5aebb8344fde8383837c318d(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af10cc39b5f5ba6eded054f31ffbd4706d4231d04b57aedc127bf4e576f255b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159555baf2bda86fb2b1cb4f203eb8889cd2ec3395162f7d34f6b3bf4bdb405a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fca302717ac54bb59f5552189434c71d9bec42d7b2a28bf6430bf5e7c4f8c84(
    value: typing.Optional[BigqueryTableEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c60ab8fdd68e02c385fb19a744285eb35baeda52e37f6cea6837e2b0f015c1(
    *,
    autodetect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    source_format: builtins.str,
    source_uris: typing.Sequence[builtins.str],
    avro_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationAvroOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    compression: typing.Optional[builtins.str] = None,
    connection_id: typing.Optional[builtins.str] = None,
    csv_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationCsvOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    google_sheets_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationGoogleSheetsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    hive_partitioning_options: typing.Optional[typing.Union[BigqueryTableExternalDataConfigurationHivePartitioningOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ignore_unknown_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_bad_records: typing.Optional[jsii.Number] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020a0a10768b90ca49555c5e7a89b9faabb072bc6d5bf986be581e51358bb59e(
    *,
    use_avro_logical_types: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9fd5bb8fb0dfbc052fe96da13cf662d0ad0a733594bb360e47c8249fcf45082(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be785777b38b52889c2672086fa4df78e5b5176f5807463eaa63b17717b5921(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fcc8f040d82e48ec6840d2bc03598108e4065f5975b2f5eee455518f4ece75(
    value: typing.Optional[BigqueryTableExternalDataConfigurationAvroOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbe70f4df9985ff876e0f2ae8cd3f32cc7a5d0424dcd4f97052fc74b0e00937(
    *,
    quote: builtins.str,
    allow_jagged_rows: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_quoted_newlines: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encoding: typing.Optional[builtins.str] = None,
    field_delimiter: typing.Optional[builtins.str] = None,
    skip_leading_rows: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60af4fc24e71e637c6fa900482563f246e261e062f3062c295a2bad98420962(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e73d09915846f7821d69bbaafe21042ed21254594e34719c29494cb50b3a92(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e69d30776a200962cdf1ae7dbfec1ed9bc8dd3a8bbc993e020ff52eee4a4e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97b74c86bec5163696d29826bf6274501cc5d15f5a8981eecd353bafe0ad6d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4ef4f6ceb6adf5f5e4f857fe2a3abfa9551e8515e1c01b43f46ad903e65a30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c97c66ebe5dd4be082754498f497e0dd3a039989089797867763631092e415(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750a54e77026baaefd7596886e1ff0599ce1f18278039fa40bd4ab7b0e00e47a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49253d1d598fd8a759e5fb7260bd43f838344fc041171c17e9fdb960f0bca7ac(
    value: typing.Optional[BigqueryTableExternalDataConfigurationCsvOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d038f67db09f696cd8f12f3dd998ac5d9aaa643c029b6323a5865470d5e1bb13(
    *,
    range: typing.Optional[builtins.str] = None,
    skip_leading_rows: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc19019d32a22a60c6a9ca6c1e9a76258e4553f4456f2df92bef8f673d7390c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37f5f39bd5216808ff0bfd8dfaf4e99a1f1c79731e27bae75778a2d3136bea5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52592b7fc99331f5d59d8b9949f4a4ec26a81695186d39a91dc86b408c9263e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74e3e17939cb2af1a1dda80388692345f22ee6e9ebbbc005cef5c75e631246d(
    value: typing.Optional[BigqueryTableExternalDataConfigurationGoogleSheetsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810784a6342c4175b64b73278d9e89558c903464868b3a31434d1454105155a7(
    *,
    mode: typing.Optional[builtins.str] = None,
    require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_uri_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427d241048413617b3bd3a828418f1d0ac690b71dfe0d2e2068199e9bddd2441(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01a839fea9d2d522ebdb2c7d2a742aa9480bdbd7bb8032c9a1cb98fb08540e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a766f84b3d43b2709c94c8f8521d26c341493a08ed89bef1a658cffcf736efc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece8fc4dc9da2b45528b8120676c44420820ae71ca2379a6b811788655de2ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ea00c1a595be450f340f82ebd3b57198a01adae42a7d6bd7aa2a43f9bfbeb3(
    value: typing.Optional[BigqueryTableExternalDataConfigurationHivePartitioningOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aedd3ec19da32a66f5345c97d51ab2ec0daa172ece609031aadaa848060186d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa92013cd8c6f4654573bca59cada4acf1ab4fa24e0c33e4d4183250eea524a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171e466428ef05f4c723a94ae4be4749554bd2eea5cd174382809e39dc1531e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b513971418e35e0889daa1af0c24cd9d68fe2c0c11f24a4107c11bdd933e16b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a59007098ead2bf4df9dc5cfcdcf21549a84089fbee66a5e258d3fd9a97d35(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d69f7654bb9a49339cdf5f1425dadb79c83dad7cad0ee4c0b95ee260bcf1b1b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0884b65b0bdd6567b088bb09c59a013f1c64f0c864984a8075b6a4e371875e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a03112d506997097f3ea5d211e0cd0d133f64fde4a35c3bc1ceafc857b28a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2411a1cf8a70ffbcaa7d39b40a4d65c9ac8a09f10bddc890f5e9f3dfa59fd1c4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a895f0de550b51ae084bc84300b10c9de0fb66c609b0968fc28545ce0c6a53(
    value: typing.Optional[BigqueryTableExternalDataConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bfac7ffc7a9089b8ef1d3b22082c499bb74076ee32063e98bfc14ba774af19(
    *,
    query: builtins.str,
    enable_refresh: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    refresh_interval_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a06199473432610a340d54e912a27a45d9838f276f5ddefb8ea5ed442551b84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95c47f7821838b81eb06f48bf5b0c5aed91c07011b4d48d8073fce2186f17bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9fea0c74fd4684d8ad56faaf0179f2f5bb721644dff852d3e6979f302106755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9657a3990dc569b85efe467953e2b35134c6d571e8a9003d13db7d882c11d771(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35804a2287301e8b044546610ce9f0fb372c6b235f2ade6d86c3105305e0f8c0(
    value: typing.Optional[BigqueryTableMaterializedView],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdcc485551cdda9350f0ec3b6f635fb181dfeb360e8a64dc8017a129edb17bf(
    *,
    field: builtins.str,
    range: typing.Union[BigqueryTableRangePartitioningRange, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5846667bda1a92cfa7b2128c33f2548d65ee779e39fcfee01fc1ed16c3071bdc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395c6f6f36489faff4acf790a2a2cc1c21f8f9966c5ef9a170a50199315505e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ed36eb55e507419b8535e2c7cafa45c85bff6123571a8edb4886a44bacae48(
    value: typing.Optional[BigqueryTableRangePartitioning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69572fe55635746c6c943f6472627f9914d257e914d14e8158134965b8a38fb4(
    *,
    end: jsii.Number,
    interval: jsii.Number,
    start: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e346b07c1bf2602c604ad14a57886686548a1aa4a51a38351b11b562dc21085(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2b695fdea4b4df8ca95b67883601572c7925871a37b6a6422ddb8f986cab0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3633200eb7491ca91f5312d0e52d612aafd64c3a611f85726166d54ad0765116(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f689dce76260a1d7c60657cf8bca91a3d9a497d6f1788949e150195b1c9820(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19729f38363279736c21ff6e0255ab435dae55bb7e61e454e836a44d18820d73(
    value: typing.Optional[BigqueryTableRangePartitioningRange],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb89c8f47dc2aa75c98d1b70fe727492265de34a7f04fcc70fb2ac919a4b609(
    *,
    type: builtins.str,
    expiration_ms: typing.Optional[jsii.Number] = None,
    field: typing.Optional[builtins.str] = None,
    require_partition_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb1012c6f07e275e2c7ac99db9bd6af2dbbbe5b56308e74d8073d34cf791a6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463cb583811d7bce632cdacc04ef7a813a9464f2fd0935bdb317acbdf50877af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9f1f7e339594c721b212be7ee4b6441e2e4cfba1f61b12bb2bf75f78fa8edb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d848604fbd9c70477cd62b8b91073abca4ee3d39caf376d82ad8cb379f3295c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e229f2df185e40b0ee1aec2c292b2f480e52700cd9e7d4e30c50fd2871166f62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57aa79d96b36de527ea884cebcfcccaa556f71725930521bec3778b8be50e098(
    value: typing.Optional[BigqueryTableTimePartitioning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a3916e2251c4ce938996c4d3230e60885f992563fbccd7813ffeeaec1eeada(
    *,
    query: builtins.str,
    use_legacy_sql: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d3a89bee4916b9695c0ff59eb7dadc6367caaf6a57673b503046edf0dcc9bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722fbc23443a9a33d97f796a37943d92c33e8b32289d7ca8d1190dbf88ecbdea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7d9b7655097a8ae61f21e1a58fea8369d86360dab40227def1947e1e1193ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7686a49feb74dbf2c8805b0999264b2707d637196b1090f8df1405c64fa0fc4(
    value: typing.Optional[BigqueryTableView],
) -> None:
    """Type checking stubs"""
    pass
