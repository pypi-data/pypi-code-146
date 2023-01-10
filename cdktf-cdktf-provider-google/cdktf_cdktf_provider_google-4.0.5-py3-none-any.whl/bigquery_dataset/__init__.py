'''
# `google_bigquery_dataset`

Refer to the Terraform Registory for docs: [`google_bigquery_dataset`](https://www.terraform.io/docs/providers/google/r/bigquery_dataset).
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


class BigqueryDataset(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDataset",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset google_bigquery_dataset}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset_id: builtins.str,
        access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryDatasetAccess", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_encryption_configuration: typing.Optional[typing.Union["BigqueryDatasetDefaultEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        default_partition_expiration_ms: typing.Optional[jsii.Number] = None,
        default_table_expiration_ms: typing.Optional[jsii.Number] = None,
        delete_contents_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        max_time_travel_hours: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryDatasetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset google_bigquery_dataset} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset_id: A unique ID for this dataset, without the project name. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        :param access: access block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#access BigqueryDataset#access}
        :param default_encryption_configuration: default_encryption_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#default_encryption_configuration BigqueryDataset#default_encryption_configuration}
        :param default_partition_expiration_ms: The default partition expiration for all partitioned tables in the dataset, in milliseconds. Once this property is set, all newly-created partitioned tables in the dataset will have an 'expirationMs' property in the 'timePartitioning' settings set to this value, and changing the value will only affect new tables, not existing ones. The storage in a partition will have an expiration time of its partition time plus this value. Setting this property overrides the use of 'defaultTableExpirationMs' for partitioned tables: only one of 'defaultTableExpirationMs' and 'defaultPartitionExpirationMs' will be used for any new partitioned table. If you provide an explicit 'timePartitioning.expirationMs' when creating or updating a partitioned table, that value takes precedence over the default partition expiration time indicated by this property. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#default_partition_expiration_ms BigqueryDataset#default_partition_expiration_ms}
        :param default_table_expiration_ms: The default lifetime of all tables in the dataset, in milliseconds. The minimum value is 3600000 milliseconds (one hour). Once this property is set, all newly-created tables in the dataset will have an 'expirationTime' property set to the creation time plus the value in this property, and changing the value will only affect new tables, not existing ones. When the 'expirationTime' for a given table is reached, that table will be deleted automatically. If a table's 'expirationTime' is modified or removed before the table expires, or if you provide an explicit 'expirationTime' when creating a table, that value takes precedence over the default expiration time indicated by this property. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#default_table_expiration_ms BigqueryDataset#default_table_expiration_ms}
        :param delete_contents_on_destroy: If set to 'true', delete all the tables in the dataset when destroying the resource; otherwise, destroying the resource will fail if tables are present. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#delete_contents_on_destroy BigqueryDataset#delete_contents_on_destroy}
        :param description: A user-friendly description of the dataset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#description BigqueryDataset#description}
        :param friendly_name: A descriptive name for the dataset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#friendly_name BigqueryDataset#friendly_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#id BigqueryDataset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this dataset. You can use these to organize and group your datasets. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#labels BigqueryDataset#labels}
        :param location: The geographic location where the dataset should reside. See `official docs <https://cloud.google.com/bigquery/docs/dataset-locations>`_. There are two types of locations, regional or multi-regional. A regional location is a specific geographic place, such as Tokyo, and a multi-regional location is a large geographic area, such as the United States, that contains at least two geographic places. The default value is multi-regional location 'US'. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#location BigqueryDataset#location}
        :param max_time_travel_hours: Defines the time travel window in hours. The value can be from 48 to 168 hours (2 to 7 days). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#max_time_travel_hours BigqueryDataset#max_time_travel_hours}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project BigqueryDataset#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#timeouts BigqueryDataset#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde78446a567ffcfe555a60df59390d3994a90f69a6b4c670af3a7b14b3077e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryDatasetConfig(
            dataset_id=dataset_id,
            access=access,
            default_encryption_configuration=default_encryption_configuration,
            default_partition_expiration_ms=default_partition_expiration_ms,
            default_table_expiration_ms=default_table_expiration_ms,
            delete_contents_on_destroy=delete_contents_on_destroy,
            description=description,
            friendly_name=friendly_name,
            id=id,
            labels=labels,
            location=location,
            max_time_travel_hours=max_time_travel_hours,
            project=project,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAccess")
    def put_access(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryDatasetAccess", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d4d21efbc51ff45e90e370bd516b2cbc9b0c728930d461955ce5afd6c63c657)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccess", [value]))

    @jsii.member(jsii_name="putDefaultEncryptionConfiguration")
    def put_default_encryption_configuration(
        self,
        *,
        kms_key_name: builtins.str,
    ) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table. The BigQuery Service Account associated with your project requires access to this encryption key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#kms_key_name BigqueryDataset#kms_key_name}
        '''
        value = BigqueryDatasetDefaultEncryptionConfiguration(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#create BigqueryDataset#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#delete BigqueryDataset#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#update BigqueryDataset#update}.
        '''
        value = BigqueryDatasetTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccess")
    def reset_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccess", []))

    @jsii.member(jsii_name="resetDefaultEncryptionConfiguration")
    def reset_default_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetDefaultPartitionExpirationMs")
    def reset_default_partition_expiration_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPartitionExpirationMs", []))

    @jsii.member(jsii_name="resetDefaultTableExpirationMs")
    def reset_default_table_expiration_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTableExpirationMs", []))

    @jsii.member(jsii_name="resetDeleteContentsOnDestroy")
    def reset_delete_contents_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteContentsOnDestroy", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFriendlyName")
    def reset_friendly_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFriendlyName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMaxTimeTravelHours")
    def reset_max_time_travel_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTimeTravelHours", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="access")
    def access(self) -> "BigqueryDatasetAccessList":
        return typing.cast("BigqueryDatasetAccessList", jsii.get(self, "access"))

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="defaultEncryptionConfiguration")
    def default_encryption_configuration(
        self,
    ) -> "BigqueryDatasetDefaultEncryptionConfigurationOutputReference":
        return typing.cast("BigqueryDatasetDefaultEncryptionConfigurationOutputReference", jsii.get(self, "defaultEncryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedTime")
    def last_modified_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastModifiedTime"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryDatasetTimeoutsOutputReference":
        return typing.cast("BigqueryDatasetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryDatasetAccess"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryDatasetAccess"]]], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultEncryptionConfigurationInput")
    def default_encryption_configuration_input(
        self,
    ) -> typing.Optional["BigqueryDatasetDefaultEncryptionConfiguration"]:
        return typing.cast(typing.Optional["BigqueryDatasetDefaultEncryptionConfiguration"], jsii.get(self, "defaultEncryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPartitionExpirationMsInput")
    def default_partition_expiration_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultPartitionExpirationMsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTableExpirationMsInput")
    def default_table_expiration_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTableExpirationMsInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteContentsOnDestroyInput")
    def delete_contents_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteContentsOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTimeTravelHoursInput")
    def max_time_travel_hours_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxTimeTravelHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["BigqueryDatasetTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["BigqueryDatasetTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb46cd5295db3e61e2a9094649f6b027f24051da64ee359f6994801a150b9aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value)

    @builtins.property
    @jsii.member(jsii_name="defaultPartitionExpirationMs")
    def default_partition_expiration_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultPartitionExpirationMs"))

    @default_partition_expiration_ms.setter
    def default_partition_expiration_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d067825aea050ada3f718344eeede28fb691a0a0e07cc02ea1a00ca998e42e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPartitionExpirationMs", value)

    @builtins.property
    @jsii.member(jsii_name="defaultTableExpirationMs")
    def default_table_expiration_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTableExpirationMs"))

    @default_table_expiration_ms.setter
    def default_table_expiration_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4bc674b806bfde180d967cbe9ad7018bffbdb3e7777625facbc149fed480fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTableExpirationMs", value)

    @builtins.property
    @jsii.member(jsii_name="deleteContentsOnDestroy")
    def delete_contents_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteContentsOnDestroy"))

    @delete_contents_on_destroy.setter
    def delete_contents_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c93d97487c85ca462f8d701f3436af5f721133e8d6e87574b7b1bfc81c550e16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteContentsOnDestroy", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db038df5799d7363640daa5b0ffdd02d7d217d05b10778f3ff8e92db08f2cecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="friendlyName")
    def friendly_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "friendlyName"))

    @friendly_name.setter
    def friendly_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44c2e233a73bac585e9766446ff6195850868b8400ca78f44b5f8de4e7c1c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "friendlyName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e32bcd1a6cb6163769ef1769a2ccf0f5be691c02b8c18e1c94f44d2e38974a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaaa96b59bd35882f01138eebb0a9d3fad8a890fec27b8f242f19cec8b1d38a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d8b00fb7a73df6f1e7c7d1fb8d54bd3e4f7db4ee524f56865807a5850d5b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="maxTimeTravelHours")
    def max_time_travel_hours(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTimeTravelHours"))

    @max_time_travel_hours.setter
    def max_time_travel_hours(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8772ae43064081f5bad6d292dff6999f4d9c4b2e98246e5b5eb9eabdc7cb73a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTimeTravelHours", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee1ba45eb45b69c2acc36338dcaedf85b17fa555991beb83e8e3cf431a25f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccess",
    jsii_struct_bases=[],
    name_mapping={
        "dataset": "dataset",
        "domain": "domain",
        "group_by_email": "groupByEmail",
        "role": "role",
        "routine": "routine",
        "special_group": "specialGroup",
        "user_by_email": "userByEmail",
        "view": "view",
    },
)
class BigqueryDatasetAccess:
    def __init__(
        self,
        *,
        dataset: typing.Optional[typing.Union["BigqueryDatasetAccessDataset", typing.Dict[builtins.str, typing.Any]]] = None,
        domain: typing.Optional[builtins.str] = None,
        group_by_email: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        routine: typing.Optional[typing.Union["BigqueryDatasetAccessRoutine", typing.Dict[builtins.str, typing.Any]]] = None,
        special_group: typing.Optional[builtins.str] = None,
        user_by_email: typing.Optional[builtins.str] = None,
        view: typing.Optional[typing.Union["BigqueryDatasetAccessView", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dataset: dataset block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset BigqueryDataset#dataset}
        :param domain: A domain to grant access to. Any users signed in with the domain specified will be granted the specified access. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#domain BigqueryDataset#domain}
        :param group_by_email: An email address of a Google Group to grant access to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#group_by_email BigqueryDataset#group_by_email}
        :param role: Describes the rights granted to the user specified by the other member of the access object. Basic, predefined, and custom roles are supported. Predefined roles that have equivalent basic roles are swapped by the API to their basic counterparts. See `official docs <https://cloud.google.com/bigquery/docs/access-control>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#role BigqueryDataset#role}
        :param routine: routine block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#routine BigqueryDataset#routine}
        :param special_group: A special group to grant access to. Possible values include:. 'projectOwners': Owners of the enclosing project. 'projectReaders': Readers of the enclosing project. 'projectWriters': Writers of the enclosing project. 'allAuthenticatedUsers': All authenticated BigQuery users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#special_group BigqueryDataset#special_group}
        :param user_by_email: An email address of a user to grant access to. For example: fred@example.com. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#user_by_email BigqueryDataset#user_by_email}
        :param view: view block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#view BigqueryDataset#view}
        '''
        if isinstance(dataset, dict):
            dataset = BigqueryDatasetAccessDataset(**dataset)
        if isinstance(routine, dict):
            routine = BigqueryDatasetAccessRoutine(**routine)
        if isinstance(view, dict):
            view = BigqueryDatasetAccessView(**view)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287916a5f71b6a04177d4681bff0030770924918c28fc96ab562c9e788e398de)
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument group_by_email", value=group_by_email, expected_type=type_hints["group_by_email"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument routine", value=routine, expected_type=type_hints["routine"])
            check_type(argname="argument special_group", value=special_group, expected_type=type_hints["special_group"])
            check_type(argname="argument user_by_email", value=user_by_email, expected_type=type_hints["user_by_email"])
            check_type(argname="argument view", value=view, expected_type=type_hints["view"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset is not None:
            self._values["dataset"] = dataset
        if domain is not None:
            self._values["domain"] = domain
        if group_by_email is not None:
            self._values["group_by_email"] = group_by_email
        if role is not None:
            self._values["role"] = role
        if routine is not None:
            self._values["routine"] = routine
        if special_group is not None:
            self._values["special_group"] = special_group
        if user_by_email is not None:
            self._values["user_by_email"] = user_by_email
        if view is not None:
            self._values["view"] = view

    @builtins.property
    def dataset(self) -> typing.Optional["BigqueryDatasetAccessDataset"]:
        '''dataset block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset BigqueryDataset#dataset}
        '''
        result = self._values.get("dataset")
        return typing.cast(typing.Optional["BigqueryDatasetAccessDataset"], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''A domain to grant access to. Any users signed in with the domain specified will be granted the specified access.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#domain BigqueryDataset#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_by_email(self) -> typing.Optional[builtins.str]:
        '''An email address of a Google Group to grant access to.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#group_by_email BigqueryDataset#group_by_email}
        '''
        result = self._values.get("group_by_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''Describes the rights granted to the user specified by the other member of the access object.

        Basic, predefined, and custom roles
        are supported. Predefined roles that have equivalent basic roles
        are swapped by the API to their basic counterparts. See
        `official docs <https://cloud.google.com/bigquery/docs/access-control>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#role BigqueryDataset#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routine(self) -> typing.Optional["BigqueryDatasetAccessRoutine"]:
        '''routine block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#routine BigqueryDataset#routine}
        '''
        result = self._values.get("routine")
        return typing.cast(typing.Optional["BigqueryDatasetAccessRoutine"], result)

    @builtins.property
    def special_group(self) -> typing.Optional[builtins.str]:
        '''A special group to grant access to. Possible values include:.

        'projectOwners': Owners of the enclosing project.

        'projectReaders': Readers of the enclosing project.

        'projectWriters': Writers of the enclosing project.

        'allAuthenticatedUsers': All authenticated BigQuery users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#special_group BigqueryDataset#special_group}
        '''
        result = self._values.get("special_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_by_email(self) -> typing.Optional[builtins.str]:
        '''An email address of a user to grant access to. For example: fred@example.com.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#user_by_email BigqueryDataset#user_by_email}
        '''
        result = self._values.get("user_by_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def view(self) -> typing.Optional["BigqueryDatasetAccessView"]:
        '''view block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#view BigqueryDataset#view}
        '''
        result = self._values.get("view")
        return typing.cast(typing.Optional["BigqueryDatasetAccessView"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccessDataset",
    jsii_struct_bases=[],
    name_mapping={"dataset": "dataset", "target_types": "targetTypes"},
)
class BigqueryDatasetAccessDataset:
    def __init__(
        self,
        *,
        dataset: typing.Union["BigqueryDatasetAccessDatasetDataset", typing.Dict[builtins.str, typing.Any]],
        target_types: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param dataset: dataset block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset BigqueryDataset#dataset}
        :param target_types: Which resources in the dataset this entry applies to. Currently, only views are supported, but additional target types may be added in the future. Possible values: VIEWS Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#target_types BigqueryDataset#target_types}
        '''
        if isinstance(dataset, dict):
            dataset = BigqueryDatasetAccessDatasetDataset(**dataset)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290d3a37251144656fe743be1aefff00d890695defbc01bcc31f25b797b5bc66)
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument target_types", value=target_types, expected_type=type_hints["target_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset": dataset,
            "target_types": target_types,
        }

    @builtins.property
    def dataset(self) -> "BigqueryDatasetAccessDatasetDataset":
        '''dataset block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset BigqueryDataset#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast("BigqueryDatasetAccessDatasetDataset", result)

    @builtins.property
    def target_types(self) -> typing.List[builtins.str]:
        '''Which resources in the dataset this entry applies to.

        Currently, only views are supported,
        but additional target types may be added in the future. Possible values: VIEWS

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#target_types BigqueryDataset#target_types}
        '''
        result = self._values.get("target_types")
        assert result is not None, "Required property 'target_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccessDatasetDataset",
    jsii_struct_bases=[],
    name_mapping={"dataset_id": "datasetId", "project_id": "projectId"},
)
class BigqueryDatasetAccessDatasetDataset:
    def __init__(self, *, dataset_id: builtins.str, project_id: builtins.str) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project_id BigqueryDataset#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1167e14e44ed6f97aa2788b749d75e526c7e9ecc2878e3e7c9bbbdbf3b0a0af2)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "project_id": project_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project_id BigqueryDataset#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessDatasetDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetAccessDatasetDatasetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccessDatasetDatasetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95fd9bb788c61de20940463298d1247babb3f636826a18fe5b4edbc665e7e0ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72540e4cd428e4a583f31fde49c13022fc13f6708f5a1d4f2809eb3635e0880f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991c34cd3f8b9bd8b3fff1137789ae451c5c561de97eb77c1a8593b3f162c115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryDatasetAccessDatasetDataset]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessDatasetDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDatasetAccessDatasetDataset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3e555c610aaa4678e69b01e3f8290b626b00dc6bd1386cbb739a64f31efa91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BigqueryDatasetAccessDatasetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccessDatasetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79595b89be2e6996bc22f7b04b0a410720ef9156fde07c874b40a02985943b7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataset")
    def put_dataset(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project_id BigqueryDataset#project_id}
        '''
        value = BigqueryDatasetAccessDatasetDataset(
            dataset_id=dataset_id, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putDataset", [value]))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> BigqueryDatasetAccessDatasetDatasetOutputReference:
        return typing.cast(BigqueryDatasetAccessDatasetDatasetOutputReference, jsii.get(self, "dataset"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[BigqueryDatasetAccessDatasetDataset]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessDatasetDataset], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetTypesInput")
    def target_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetTypes")
    def target_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetTypes"))

    @target_types.setter
    def target_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c06dcf9d8a5c2faaec1d2b5848239fc45fbf0b6d124fbf82dc2a573875fc8f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetTypes", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryDatasetAccessDataset]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDatasetAccessDataset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47101b7e050d7cd85ffdd7f76e60269039027acd95d5266ce751afddb78a026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BigqueryDatasetAccessList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccessList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8677a50f0dc60c5c14161b3e9a9e10b065f4d5d7e6baf7526ca8a99689bc19b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BigqueryDatasetAccessOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385844bda02c838a44251c0e52017a4742b21124e71d5408a08208430f969955)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BigqueryDatasetAccessOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e115979489fb43fe2eb33bf2bb33af63791fc7590efd2826f712937db0c1071)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ea109d9c79ab1f8b05eb1660a95c9aa29ef343eca6da1bca44bb46c6ea2c73b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8db7e3993e36e10410b94a4705ce038a93d6ef6b26529bac7d6042bfe8517c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryDatasetAccess]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryDatasetAccess]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryDatasetAccess]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0149d16916e9623ad8fb91bc0eb1c85ac176638b37e0692714f5938d34aede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BigqueryDatasetAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78aeb68c8f0dc2574f8a237fdc110ca93221c6e486af9e13130142e60119d965)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataset")
    def put_dataset(
        self,
        *,
        dataset: typing.Union[BigqueryDatasetAccessDatasetDataset, typing.Dict[builtins.str, typing.Any]],
        target_types: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param dataset: dataset block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset BigqueryDataset#dataset}
        :param target_types: Which resources in the dataset this entry applies to. Currently, only views are supported, but additional target types may be added in the future. Possible values: VIEWS Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#target_types BigqueryDataset#target_types}
        '''
        value = BigqueryDatasetAccessDataset(
            dataset=dataset, target_types=target_types
        )

        return typing.cast(None, jsii.invoke(self, "putDataset", [value]))

    @jsii.member(jsii_name="putRoutine")
    def put_routine(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        routine_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project_id BigqueryDataset#project_id}
        :param routine_id: The ID of the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#routine_id BigqueryDataset#routine_id}
        '''
        value = BigqueryDatasetAccessRoutine(
            dataset_id=dataset_id, project_id=project_id, routine_id=routine_id
        )

        return typing.cast(None, jsii.invoke(self, "putRoutine", [value]))

    @jsii.member(jsii_name="putView")
    def put_view(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project_id BigqueryDataset#project_id}
        :param table_id: The ID of the table. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#table_id BigqueryDataset#table_id}
        '''
        value = BigqueryDatasetAccessView(
            dataset_id=dataset_id, project_id=project_id, table_id=table_id
        )

        return typing.cast(None, jsii.invoke(self, "putView", [value]))

    @jsii.member(jsii_name="resetDataset")
    def reset_dataset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataset", []))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetGroupByEmail")
    def reset_group_by_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupByEmail", []))

    @jsii.member(jsii_name="resetRole")
    def reset_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRole", []))

    @jsii.member(jsii_name="resetRoutine")
    def reset_routine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutine", []))

    @jsii.member(jsii_name="resetSpecialGroup")
    def reset_special_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecialGroup", []))

    @jsii.member(jsii_name="resetUserByEmail")
    def reset_user_by_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserByEmail", []))

    @jsii.member(jsii_name="resetView")
    def reset_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetView", []))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> BigqueryDatasetAccessDatasetOutputReference:
        return typing.cast(BigqueryDatasetAccessDatasetOutputReference, jsii.get(self, "dataset"))

    @builtins.property
    @jsii.member(jsii_name="routine")
    def routine(self) -> "BigqueryDatasetAccessRoutineOutputReference":
        return typing.cast("BigqueryDatasetAccessRoutineOutputReference", jsii.get(self, "routine"))

    @builtins.property
    @jsii.member(jsii_name="view")
    def view(self) -> "BigqueryDatasetAccessViewOutputReference":
        return typing.cast("BigqueryDatasetAccessViewOutputReference", jsii.get(self, "view"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[BigqueryDatasetAccessDataset]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessDataset], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="groupByEmailInput")
    def group_by_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupByEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="routineInput")
    def routine_input(self) -> typing.Optional["BigqueryDatasetAccessRoutine"]:
        return typing.cast(typing.Optional["BigqueryDatasetAccessRoutine"], jsii.get(self, "routineInput"))

    @builtins.property
    @jsii.member(jsii_name="specialGroupInput")
    def special_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "specialGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="userByEmailInput")
    def user_by_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userByEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="viewInput")
    def view_input(self) -> typing.Optional["BigqueryDatasetAccessView"]:
        return typing.cast(typing.Optional["BigqueryDatasetAccessView"], jsii.get(self, "viewInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__401405ee0621575a8e9ee407f2d0fba39abf6e24c6d89495401728d9a1baee2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="groupByEmail")
    def group_by_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupByEmail"))

    @group_by_email.setter
    def group_by_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abe40d49e1ace1fc154fe19a53de74a5f7c9c4d542511db55c97b1fd3446ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupByEmail", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec3891bf8953761d3a71443c49f1b018321f2433dbbc15db6002194975af797)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="specialGroup")
    def special_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specialGroup"))

    @special_group.setter
    def special_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22ace0a1386a19c5a9a5f14d9ab4c661073c366190fa60df904ad908f1f4578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "specialGroup", value)

    @builtins.property
    @jsii.member(jsii_name="userByEmail")
    def user_by_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userByEmail"))

    @user_by_email.setter
    def user_by_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ab8b2c64aff79ee08c160b25f4caf9aff92c77bb4accfca6b41764ff2cc8af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userByEmail", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[BigqueryDatasetAccess, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BigqueryDatasetAccess, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BigqueryDatasetAccess, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7591a0caf9055256e77f0c49de8fd12b81e872458a9526015864baf814afbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccessRoutine",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "routine_id": "routineId",
    },
)
class BigqueryDatasetAccessRoutine:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        routine_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project_id BigqueryDataset#project_id}
        :param routine_id: The ID of the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#routine_id BigqueryDataset#routine_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8485303031bcc7135fe06deb6d596899714051d684bf0e686aff013332fbdd9d)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument routine_id", value=routine_id, expected_type=type_hints["routine_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "project_id": project_id,
            "routine_id": routine_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project_id BigqueryDataset#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routine_id(self) -> builtins.str:
        '''The ID of the routine.

        The ID must contain only letters (a-z,
        A-Z), numbers (0-9), or underscores (_). The maximum length
        is 256 characters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#routine_id BigqueryDataset#routine_id}
        '''
        result = self._values.get("routine_id")
        assert result is not None, "Required property 'routine_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessRoutine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetAccessRoutineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccessRoutineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc7b8ff8013da35e3dad9ae3e519f264a93f569d2370c44b5387c1611826c34d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="routineIdInput")
    def routine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43bad032e56a881e5a80a3702724180d62cc326f28e757c3de75e278cac3c6a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f63de689481c5696c9288e78a1558043b3812b2c3d9eed099875c1efd132857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="routineId")
    def routine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routineId"))

    @routine_id.setter
    def routine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56a276080ad1d5f447e9c291423452f74b69a7246d09e6a1062e86e0f8f9693)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routineId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryDatasetAccessRoutine]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessRoutine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDatasetAccessRoutine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ceeafd7227e5e29b3fa465ab936f2de83cb1fef4b23fcaea518e31baa567b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccessView",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_id": "datasetId",
        "project_id": "projectId",
        "table_id": "tableId",
    },
)
class BigqueryDatasetAccessView:
    def __init__(
        self,
        *,
        dataset_id: builtins.str,
        project_id: builtins.str,
        table_id: builtins.str,
    ) -> None:
        '''
        :param dataset_id: The ID of the dataset containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        :param project_id: The ID of the project containing this table. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project_id BigqueryDataset#project_id}
        :param table_id: The ID of the table. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#table_id BigqueryDataset#table_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2680768b8c40629c345ff321162b0f4791ffcb33f3768d2796538d8921dacfbb)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "project_id": project_id,
            "table_id": table_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this table.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The ID of the project containing this table.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project_id BigqueryDataset#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_id(self) -> builtins.str:
        '''The ID of the table.

        The ID must contain only letters (a-z,
        A-Z), numbers (0-9), or underscores (_). The maximum length
        is 1,024 characters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#table_id BigqueryDataset#table_id}
        '''
        result = self._values.get("table_id")
        assert result is not None, "Required property 'table_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetAccessView(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetAccessViewOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetAccessViewOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02f68d0a40b043b13fba2ade8e03363892a6f54c13570de086a9b5eca464b520)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableIdInput")
    def table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f3e37fcd1c7f60af190d8fe14eb7f22a853dedcecd1058e78870f426244444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__529a5e415e74198cc9caf6d001a1f012e0a055f8f7e88c98409dee0bfe2e6af3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="tableId")
    def table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableId"))

    @table_id.setter
    def table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b32f3c59b2c07f2dd6bcd09894e9b38775905cd785fab099d8955ff28fbab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryDatasetAccessView]:
        return typing.cast(typing.Optional[BigqueryDatasetAccessView], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BigqueryDatasetAccessView]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b999ff20620ec789c8dd4f0b00f5ebd01e75eb18fe097e3e32c55d3d02ce085a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetConfig",
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
        "access": "access",
        "default_encryption_configuration": "defaultEncryptionConfiguration",
        "default_partition_expiration_ms": "defaultPartitionExpirationMs",
        "default_table_expiration_ms": "defaultTableExpirationMs",
        "delete_contents_on_destroy": "deleteContentsOnDestroy",
        "description": "description",
        "friendly_name": "friendlyName",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "max_time_travel_hours": "maxTimeTravelHours",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class BigqueryDatasetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryDatasetAccess, typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_encryption_configuration: typing.Optional[typing.Union["BigqueryDatasetDefaultEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        default_partition_expiration_ms: typing.Optional[jsii.Number] = None,
        default_table_expiration_ms: typing.Optional[jsii.Number] = None,
        delete_contents_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        max_time_travel_hours: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryDatasetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset_id: A unique ID for this dataset, without the project name. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 1,024 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        :param access: access block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#access BigqueryDataset#access}
        :param default_encryption_configuration: default_encryption_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#default_encryption_configuration BigqueryDataset#default_encryption_configuration}
        :param default_partition_expiration_ms: The default partition expiration for all partitioned tables in the dataset, in milliseconds. Once this property is set, all newly-created partitioned tables in the dataset will have an 'expirationMs' property in the 'timePartitioning' settings set to this value, and changing the value will only affect new tables, not existing ones. The storage in a partition will have an expiration time of its partition time plus this value. Setting this property overrides the use of 'defaultTableExpirationMs' for partitioned tables: only one of 'defaultTableExpirationMs' and 'defaultPartitionExpirationMs' will be used for any new partitioned table. If you provide an explicit 'timePartitioning.expirationMs' when creating or updating a partitioned table, that value takes precedence over the default partition expiration time indicated by this property. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#default_partition_expiration_ms BigqueryDataset#default_partition_expiration_ms}
        :param default_table_expiration_ms: The default lifetime of all tables in the dataset, in milliseconds. The minimum value is 3600000 milliseconds (one hour). Once this property is set, all newly-created tables in the dataset will have an 'expirationTime' property set to the creation time plus the value in this property, and changing the value will only affect new tables, not existing ones. When the 'expirationTime' for a given table is reached, that table will be deleted automatically. If a table's 'expirationTime' is modified or removed before the table expires, or if you provide an explicit 'expirationTime' when creating a table, that value takes precedence over the default expiration time indicated by this property. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#default_table_expiration_ms BigqueryDataset#default_table_expiration_ms}
        :param delete_contents_on_destroy: If set to 'true', delete all the tables in the dataset when destroying the resource; otherwise, destroying the resource will fail if tables are present. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#delete_contents_on_destroy BigqueryDataset#delete_contents_on_destroy}
        :param description: A user-friendly description of the dataset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#description BigqueryDataset#description}
        :param friendly_name: A descriptive name for the dataset. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#friendly_name BigqueryDataset#friendly_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#id BigqueryDataset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this dataset. You can use these to organize and group your datasets. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#labels BigqueryDataset#labels}
        :param location: The geographic location where the dataset should reside. See `official docs <https://cloud.google.com/bigquery/docs/dataset-locations>`_. There are two types of locations, regional or multi-regional. A regional location is a specific geographic place, such as Tokyo, and a multi-regional location is a large geographic area, such as the United States, that contains at least two geographic places. The default value is multi-regional location 'US'. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#location BigqueryDataset#location}
        :param max_time_travel_hours: Defines the time travel window in hours. The value can be from 48 to 168 hours (2 to 7 days). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#max_time_travel_hours BigqueryDataset#max_time_travel_hours}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project BigqueryDataset#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#timeouts BigqueryDataset#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_encryption_configuration, dict):
            default_encryption_configuration = BigqueryDatasetDefaultEncryptionConfiguration(**default_encryption_configuration)
        if isinstance(timeouts, dict):
            timeouts = BigqueryDatasetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ad3a490729260a76cd3c033b4c7544a51603e23030f3bcf44d114574a1be57)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument default_encryption_configuration", value=default_encryption_configuration, expected_type=type_hints["default_encryption_configuration"])
            check_type(argname="argument default_partition_expiration_ms", value=default_partition_expiration_ms, expected_type=type_hints["default_partition_expiration_ms"])
            check_type(argname="argument default_table_expiration_ms", value=default_table_expiration_ms, expected_type=type_hints["default_table_expiration_ms"])
            check_type(argname="argument delete_contents_on_destroy", value=delete_contents_on_destroy, expected_type=type_hints["delete_contents_on_destroy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument friendly_name", value=friendly_name, expected_type=type_hints["friendly_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument max_time_travel_hours", value=max_time_travel_hours, expected_type=type_hints["max_time_travel_hours"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
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
        if access is not None:
            self._values["access"] = access
        if default_encryption_configuration is not None:
            self._values["default_encryption_configuration"] = default_encryption_configuration
        if default_partition_expiration_ms is not None:
            self._values["default_partition_expiration_ms"] = default_partition_expiration_ms
        if default_table_expiration_ms is not None:
            self._values["default_table_expiration_ms"] = default_table_expiration_ms
        if delete_contents_on_destroy is not None:
            self._values["delete_contents_on_destroy"] = delete_contents_on_destroy
        if description is not None:
            self._values["description"] = description
        if friendly_name is not None:
            self._values["friendly_name"] = friendly_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if max_time_travel_hours is not None:
            self._values["max_time_travel_hours"] = max_time_travel_hours
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
        '''A unique ID for this dataset, without the project name.

        The ID
        must contain only letters (a-z, A-Z), numbers (0-9), or
        underscores (_). The maximum length is 1,024 characters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#dataset_id BigqueryDataset#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryDatasetAccess]]]:
        '''access block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#access BigqueryDataset#access}
        '''
        result = self._values.get("access")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryDatasetAccess]]], result)

    @builtins.property
    def default_encryption_configuration(
        self,
    ) -> typing.Optional["BigqueryDatasetDefaultEncryptionConfiguration"]:
        '''default_encryption_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#default_encryption_configuration BigqueryDataset#default_encryption_configuration}
        '''
        result = self._values.get("default_encryption_configuration")
        return typing.cast(typing.Optional["BigqueryDatasetDefaultEncryptionConfiguration"], result)

    @builtins.property
    def default_partition_expiration_ms(self) -> typing.Optional[jsii.Number]:
        '''The default partition expiration for all partitioned tables in the dataset, in milliseconds.

        Once this property is set, all newly-created partitioned tables in
        the dataset will have an 'expirationMs' property in the 'timePartitioning'
        settings set to this value, and changing the value will only
        affect new tables, not existing ones. The storage in a partition will
        have an expiration time of its partition time plus this value.
        Setting this property overrides the use of 'defaultTableExpirationMs'
        for partitioned tables: only one of 'defaultTableExpirationMs' and
        'defaultPartitionExpirationMs' will be used for any new partitioned
        table. If you provide an explicit 'timePartitioning.expirationMs' when
        creating or updating a partitioned table, that value takes precedence
        over the default partition expiration time indicated by this property.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#default_partition_expiration_ms BigqueryDataset#default_partition_expiration_ms}
        '''
        result = self._values.get("default_partition_expiration_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_table_expiration_ms(self) -> typing.Optional[jsii.Number]:
        '''The default lifetime of all tables in the dataset, in milliseconds. The minimum value is 3600000 milliseconds (one hour).

        Once this property is set, all newly-created tables in the dataset
        will have an 'expirationTime' property set to the creation time plus
        the value in this property, and changing the value will only affect
        new tables, not existing ones. When the 'expirationTime' for a given
        table is reached, that table will be deleted automatically.
        If a table's 'expirationTime' is modified or removed before the
        table expires, or if you provide an explicit 'expirationTime' when
        creating a table, that value takes precedence over the default
        expiration time indicated by this property.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#default_table_expiration_ms BigqueryDataset#default_table_expiration_ms}
        '''
        result = self._values.get("default_table_expiration_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete_contents_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', delete all the tables in the dataset when destroying the resource;

        otherwise,
        destroying the resource will fail if tables are present.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#delete_contents_on_destroy BigqueryDataset#delete_contents_on_destroy}
        '''
        result = self._values.get("delete_contents_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A user-friendly description of the dataset.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#description BigqueryDataset#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def friendly_name(self) -> typing.Optional[builtins.str]:
        '''A descriptive name for the dataset.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#friendly_name BigqueryDataset#friendly_name}
        '''
        result = self._values.get("friendly_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#id BigqueryDataset#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels associated with this dataset. You can use these to organize and group your datasets.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#labels BigqueryDataset#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The geographic location where the dataset should reside. See `official docs <https://cloud.google.com/bigquery/docs/dataset-locations>`_.

        There are two types of locations, regional or multi-regional. A regional
        location is a specific geographic place, such as Tokyo, and a multi-regional
        location is a large geographic area, such as the United States, that
        contains at least two geographic places.

        The default value is multi-regional location 'US'.
        Changing this forces a new resource to be created.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#location BigqueryDataset#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_time_travel_hours(self) -> typing.Optional[builtins.str]:
        '''Defines the time travel window in hours.

        The value can be from 48 to 168 hours (2 to 7 days).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#max_time_travel_hours BigqueryDataset#max_time_travel_hours}
        '''
        result = self._values.get("max_time_travel_hours")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#project BigqueryDataset#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryDatasetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#timeouts BigqueryDataset#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryDatasetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetDefaultEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class BigqueryDatasetDefaultEncryptionConfiguration:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table. The BigQuery Service Account associated with your project requires access to this encryption key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#kms_key_name BigqueryDataset#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31e48fe1ce46b4b766a491a45d859bd363a08dee807560ccfa20ada56f2bfe6)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table.

        The BigQuery Service Account associated with your project requires
        access to this encryption key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#kms_key_name BigqueryDataset#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetDefaultEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetDefaultEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetDefaultEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7c98ff2c14cddb752074d9d879425dc1935b72d2e008bb000b05eb74db68e02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__ec06a7ff35965a0900c66d11543952fff30e06fe2e7ab053280a4b5ccee7f5cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryDatasetDefaultEncryptionConfiguration]:
        return typing.cast(typing.Optional[BigqueryDatasetDefaultEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryDatasetDefaultEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ee7fb5079fd004d19d4dfd043681589c6daaefd2120ac4b6b9f03d6f8b339a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigqueryDatasetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#create BigqueryDataset#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#delete BigqueryDataset#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#update BigqueryDataset#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8ad720db3c8fcaf10ba3ce06f02e53cc76402a667602d753a3c71810df85fb)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#create BigqueryDataset#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#delete BigqueryDataset#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_dataset#update BigqueryDataset#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryDatasetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryDatasetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryDataset.BigqueryDatasetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7770982714327f581c38ae8b48a77b5b8a2fdb66a8ee894203275e9b05a46d97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37aae72c942f316292790cc869f6485139067fd062c7391036b1e4535672f304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63cae1c30204af4af7d7add61288fa63fb3085ea9249fe0591ca97befbb59723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622939b163bef1db4fd7a7af135b108023bd483d982ce8f17ddfca4a87ca3663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[BigqueryDatasetTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BigqueryDatasetTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BigqueryDatasetTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b0ed5dd05c95a25e87b789e8978e64a679c860a0ef8c55680b3ebc0dadd9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "BigqueryDataset",
    "BigqueryDatasetAccess",
    "BigqueryDatasetAccessDataset",
    "BigqueryDatasetAccessDatasetDataset",
    "BigqueryDatasetAccessDatasetDatasetOutputReference",
    "BigqueryDatasetAccessDatasetOutputReference",
    "BigqueryDatasetAccessList",
    "BigqueryDatasetAccessOutputReference",
    "BigqueryDatasetAccessRoutine",
    "BigqueryDatasetAccessRoutineOutputReference",
    "BigqueryDatasetAccessView",
    "BigqueryDatasetAccessViewOutputReference",
    "BigqueryDatasetConfig",
    "BigqueryDatasetDefaultEncryptionConfiguration",
    "BigqueryDatasetDefaultEncryptionConfigurationOutputReference",
    "BigqueryDatasetTimeouts",
    "BigqueryDatasetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bde78446a567ffcfe555a60df59390d3994a90f69a6b4c670af3a7b14b3077e3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset_id: builtins.str,
    access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryDatasetAccess, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_encryption_configuration: typing.Optional[typing.Union[BigqueryDatasetDefaultEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    default_partition_expiration_ms: typing.Optional[jsii.Number] = None,
    default_table_expiration_ms: typing.Optional[jsii.Number] = None,
    delete_contents_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    max_time_travel_hours: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigqueryDatasetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9d4d21efbc51ff45e90e370bd516b2cbc9b0c728930d461955ce5afd6c63c657(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryDatasetAccess, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb46cd5295db3e61e2a9094649f6b027f24051da64ee359f6994801a150b9aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d067825aea050ada3f718344eeede28fb691a0a0e07cc02ea1a00ca998e42e99(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4bc674b806bfde180d967cbe9ad7018bffbdb3e7777625facbc149fed480fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93d97487c85ca462f8d701f3436af5f721133e8d6e87574b7b1bfc81c550e16(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db038df5799d7363640daa5b0ffdd02d7d217d05b10778f3ff8e92db08f2cecc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44c2e233a73bac585e9766446ff6195850868b8400ca78f44b5f8de4e7c1c11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e32bcd1a6cb6163769ef1769a2ccf0f5be691c02b8c18e1c94f44d2e38974a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaaa96b59bd35882f01138eebb0a9d3fad8a890fec27b8f242f19cec8b1d38a8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d8b00fb7a73df6f1e7c7d1fb8d54bd3e4f7db4ee524f56865807a5850d5b94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8772ae43064081f5bad6d292dff6999f4d9c4b2e98246e5b5eb9eabdc7cb73a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee1ba45eb45b69c2acc36338dcaedf85b17fa555991beb83e8e3cf431a25f91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287916a5f71b6a04177d4681bff0030770924918c28fc96ab562c9e788e398de(
    *,
    dataset: typing.Optional[typing.Union[BigqueryDatasetAccessDataset, typing.Dict[builtins.str, typing.Any]]] = None,
    domain: typing.Optional[builtins.str] = None,
    group_by_email: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
    routine: typing.Optional[typing.Union[BigqueryDatasetAccessRoutine, typing.Dict[builtins.str, typing.Any]]] = None,
    special_group: typing.Optional[builtins.str] = None,
    user_by_email: typing.Optional[builtins.str] = None,
    view: typing.Optional[typing.Union[BigqueryDatasetAccessView, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290d3a37251144656fe743be1aefff00d890695defbc01bcc31f25b797b5bc66(
    *,
    dataset: typing.Union[BigqueryDatasetAccessDatasetDataset, typing.Dict[builtins.str, typing.Any]],
    target_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1167e14e44ed6f97aa2788b749d75e526c7e9ecc2878e3e7c9bbbdbf3b0a0af2(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fd9bb788c61de20940463298d1247babb3f636826a18fe5b4edbc665e7e0ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72540e4cd428e4a583f31fde49c13022fc13f6708f5a1d4f2809eb3635e0880f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991c34cd3f8b9bd8b3fff1137789ae451c5c561de97eb77c1a8593b3f162c115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3e555c610aaa4678e69b01e3f8290b626b00dc6bd1386cbb739a64f31efa91(
    value: typing.Optional[BigqueryDatasetAccessDatasetDataset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79595b89be2e6996bc22f7b04b0a410720ef9156fde07c874b40a02985943b7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06dcf9d8a5c2faaec1d2b5848239fc45fbf0b6d124fbf82dc2a573875fc8f5d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47101b7e050d7cd85ffdd7f76e60269039027acd95d5266ce751afddb78a026(
    value: typing.Optional[BigqueryDatasetAccessDataset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8677a50f0dc60c5c14161b3e9a9e10b065f4d5d7e6baf7526ca8a99689bc19b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385844bda02c838a44251c0e52017a4742b21124e71d5408a08208430f969955(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e115979489fb43fe2eb33bf2bb33af63791fc7590efd2826f712937db0c1071(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea109d9c79ab1f8b05eb1660a95c9aa29ef343eca6da1bca44bb46c6ea2c73b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db7e3993e36e10410b94a4705ce038a93d6ef6b26529bac7d6042bfe8517c8b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0149d16916e9623ad8fb91bc0eb1c85ac176638b37e0692714f5938d34aede(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryDatasetAccess]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78aeb68c8f0dc2574f8a237fdc110ca93221c6e486af9e13130142e60119d965(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401405ee0621575a8e9ee407f2d0fba39abf6e24c6d89495401728d9a1baee2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abe40d49e1ace1fc154fe19a53de74a5f7c9c4d542511db55c97b1fd3446ef4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec3891bf8953761d3a71443c49f1b018321f2433dbbc15db6002194975af797(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22ace0a1386a19c5a9a5f14d9ab4c661073c366190fa60df904ad908f1f4578(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ab8b2c64aff79ee08c160b25f4caf9aff92c77bb4accfca6b41764ff2cc8af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7591a0caf9055256e77f0c49de8fd12b81e872458a9526015864baf814afbd(
    value: typing.Optional[typing.Union[BigqueryDatasetAccess, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8485303031bcc7135fe06deb6d596899714051d684bf0e686aff013332fbdd9d(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    routine_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7b8ff8013da35e3dad9ae3e519f264a93f569d2370c44b5387c1611826c34d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bad032e56a881e5a80a3702724180d62cc326f28e757c3de75e278cac3c6a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f63de689481c5696c9288e78a1558043b3812b2c3d9eed099875c1efd132857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56a276080ad1d5f447e9c291423452f74b69a7246d09e6a1062e86e0f8f9693(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ceeafd7227e5e29b3fa465ab936f2de83cb1fef4b23fcaea518e31baa567b41(
    value: typing.Optional[BigqueryDatasetAccessRoutine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2680768b8c40629c345ff321162b0f4791ffcb33f3768d2796538d8921dacfbb(
    *,
    dataset_id: builtins.str,
    project_id: builtins.str,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f68d0a40b043b13fba2ade8e03363892a6f54c13570de086a9b5eca464b520(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f3e37fcd1c7f60af190d8fe14eb7f22a853dedcecd1058e78870f426244444(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529a5e415e74198cc9caf6d001a1f012e0a055f8f7e88c98409dee0bfe2e6af3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b32f3c59b2c07f2dd6bcd09894e9b38775905cd785fab099d8955ff28fbab3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b999ff20620ec789c8dd4f0b00f5ebd01e75eb18fe097e3e32c55d3d02ce085a(
    value: typing.Optional[BigqueryDatasetAccessView],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ad3a490729260a76cd3c033b4c7544a51603e23030f3bcf44d114574a1be57(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset_id: builtins.str,
    access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryDatasetAccess, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_encryption_configuration: typing.Optional[typing.Union[BigqueryDatasetDefaultEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    default_partition_expiration_ms: typing.Optional[jsii.Number] = None,
    default_table_expiration_ms: typing.Optional[jsii.Number] = None,
    delete_contents_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    max_time_travel_hours: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigqueryDatasetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31e48fe1ce46b4b766a491a45d859bd363a08dee807560ccfa20ada56f2bfe6(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c98ff2c14cddb752074d9d879425dc1935b72d2e008bb000b05eb74db68e02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec06a7ff35965a0900c66d11543952fff30e06fe2e7ab053280a4b5ccee7f5cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ee7fb5079fd004d19d4dfd043681589c6daaefd2120ac4b6b9f03d6f8b339a(
    value: typing.Optional[BigqueryDatasetDefaultEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8ad720db3c8fcaf10ba3ce06f02e53cc76402a667602d753a3c71810df85fb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7770982714327f581c38ae8b48a77b5b8a2fdb66a8ee894203275e9b05a46d97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37aae72c942f316292790cc869f6485139067fd062c7391036b1e4535672f304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cae1c30204af4af7d7add61288fa63fb3085ea9249fe0591ca97befbb59723(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622939b163bef1db4fd7a7af135b108023bd483d982ce8f17ddfca4a87ca3663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b0ed5dd05c95a25e87b789e8978e64a679c860a0ef8c55680b3ebc0dadd9cb(
    value: typing.Optional[typing.Union[BigqueryDatasetTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
