'''
# `azurerm_sql_database`

Refer to the Terraform Registory for docs: [`azurerm_sql_database`](https://www.terraform.io/docs/providers/azurerm/r/sql_database).
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


class SqlDatabase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlDatabase.SqlDatabase",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database azurerm_sql_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        server_name: builtins.str,
        collation: typing.Optional[builtins.str] = None,
        create_mode: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        elastic_pool_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        import_: typing.Optional[typing.Union["SqlDatabaseImport", typing.Dict[builtins.str, typing.Any]]] = None,
        max_size_bytes: typing.Optional[builtins.str] = None,
        max_size_gb: typing.Optional[builtins.str] = None,
        read_scale: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        requested_service_objective_id: typing.Optional[builtins.str] = None,
        requested_service_objective_name: typing.Optional[builtins.str] = None,
        restore_point_in_time: typing.Optional[builtins.str] = None,
        source_database_deletion_date: typing.Optional[builtins.str] = None,
        source_database_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        threat_detection_policy: typing.Optional[typing.Union["SqlDatabaseThreatDetectionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["SqlDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database azurerm_sql_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#location SqlDatabase#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#name SqlDatabase#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#resource_group_name SqlDatabase#resource_group_name}.
        :param server_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#server_name SqlDatabase#server_name}.
        :param collation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#collation SqlDatabase#collation}.
        :param create_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#create_mode SqlDatabase#create_mode}.
        :param edition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#edition SqlDatabase#edition}.
        :param elastic_pool_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#elastic_pool_name SqlDatabase#elastic_pool_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#id SqlDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_: import block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#import SqlDatabase#import}
        :param max_size_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#max_size_bytes SqlDatabase#max_size_bytes}.
        :param max_size_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#max_size_gb SqlDatabase#max_size_gb}.
        :param read_scale: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#read_scale SqlDatabase#read_scale}.
        :param requested_service_objective_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#requested_service_objective_id SqlDatabase#requested_service_objective_id}.
        :param requested_service_objective_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#requested_service_objective_name SqlDatabase#requested_service_objective_name}.
        :param restore_point_in_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#restore_point_in_time SqlDatabase#restore_point_in_time}.
        :param source_database_deletion_date: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#source_database_deletion_date SqlDatabase#source_database_deletion_date}.
        :param source_database_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#source_database_id SqlDatabase#source_database_id}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#tags SqlDatabase#tags}.
        :param threat_detection_policy: threat_detection_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#threat_detection_policy SqlDatabase#threat_detection_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#timeouts SqlDatabase#timeouts}
        :param zone_redundant: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#zone_redundant SqlDatabase#zone_redundant}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06b8a54307ec6e963d4f2b7b956f858b2a988e03048a46200c822deb3edcbb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SqlDatabaseConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            server_name=server_name,
            collation=collation,
            create_mode=create_mode,
            edition=edition,
            elastic_pool_name=elastic_pool_name,
            id=id,
            import_=import_,
            max_size_bytes=max_size_bytes,
            max_size_gb=max_size_gb,
            read_scale=read_scale,
            requested_service_objective_id=requested_service_objective_id,
            requested_service_objective_name=requested_service_objective_name,
            restore_point_in_time=restore_point_in_time,
            source_database_deletion_date=source_database_deletion_date,
            source_database_id=source_database_id,
            tags=tags,
            threat_detection_policy=threat_detection_policy,
            timeouts=timeouts,
            zone_redundant=zone_redundant,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putImport")
    def put_import(
        self,
        *,
        administrator_login: builtins.str,
        administrator_login_password: builtins.str,
        authentication_type: builtins.str,
        storage_key: builtins.str,
        storage_key_type: builtins.str,
        storage_uri: builtins.str,
        operation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param administrator_login: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#administrator_login SqlDatabase#administrator_login}.
        :param administrator_login_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#administrator_login_password SqlDatabase#administrator_login_password}.
        :param authentication_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#authentication_type SqlDatabase#authentication_type}.
        :param storage_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_key SqlDatabase#storage_key}.
        :param storage_key_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_key_type SqlDatabase#storage_key_type}.
        :param storage_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_uri SqlDatabase#storage_uri}.
        :param operation_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#operation_mode SqlDatabase#operation_mode}.
        '''
        value = SqlDatabaseImport(
            administrator_login=administrator_login,
            administrator_login_password=administrator_login_password,
            authentication_type=authentication_type,
            storage_key=storage_key,
            storage_key_type=storage_key_type,
            storage_uri=storage_uri,
            operation_mode=operation_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putImport", [value]))

    @jsii.member(jsii_name="putThreatDetectionPolicy")
    def put_threat_detection_policy(
        self,
        *,
        disabled_alerts: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_account_admins: typing.Optional[builtins.str] = None,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        state: typing.Optional[builtins.str] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disabled_alerts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#disabled_alerts SqlDatabase#disabled_alerts}.
        :param email_account_admins: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#email_account_admins SqlDatabase#email_account_admins}.
        :param email_addresses: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#email_addresses SqlDatabase#email_addresses}.
        :param retention_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#retention_days SqlDatabase#retention_days}.
        :param state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#state SqlDatabase#state}.
        :param storage_account_access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_account_access_key SqlDatabase#storage_account_access_key}.
        :param storage_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_endpoint SqlDatabase#storage_endpoint}.
        '''
        value = SqlDatabaseThreatDetectionPolicy(
            disabled_alerts=disabled_alerts,
            email_account_admins=email_account_admins,
            email_addresses=email_addresses,
            retention_days=retention_days,
            state=state,
            storage_account_access_key=storage_account_access_key,
            storage_endpoint=storage_endpoint,
        )

        return typing.cast(None, jsii.invoke(self, "putThreatDetectionPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#create SqlDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#delete SqlDatabase#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#read SqlDatabase#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#update SqlDatabase#update}.
        '''
        value = SqlDatabaseTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCollation")
    def reset_collation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollation", []))

    @jsii.member(jsii_name="resetCreateMode")
    def reset_create_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateMode", []))

    @jsii.member(jsii_name="resetEdition")
    def reset_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdition", []))

    @jsii.member(jsii_name="resetElasticPoolName")
    def reset_elastic_pool_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticPoolName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImport")
    def reset_import(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImport", []))

    @jsii.member(jsii_name="resetMaxSizeBytes")
    def reset_max_size_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSizeBytes", []))

    @jsii.member(jsii_name="resetMaxSizeGb")
    def reset_max_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSizeGb", []))

    @jsii.member(jsii_name="resetReadScale")
    def reset_read_scale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadScale", []))

    @jsii.member(jsii_name="resetRequestedServiceObjectiveId")
    def reset_requested_service_objective_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestedServiceObjectiveId", []))

    @jsii.member(jsii_name="resetRequestedServiceObjectiveName")
    def reset_requested_service_objective_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestedServiceObjectiveName", []))

    @jsii.member(jsii_name="resetRestorePointInTime")
    def reset_restore_point_in_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestorePointInTime", []))

    @jsii.member(jsii_name="resetSourceDatabaseDeletionDate")
    def reset_source_database_deletion_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceDatabaseDeletionDate", []))

    @jsii.member(jsii_name="resetSourceDatabaseId")
    def reset_source_database_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceDatabaseId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetThreatDetectionPolicy")
    def reset_threat_detection_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreatDetectionPolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetZoneRedundant")
    def reset_zone_redundant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneRedundant", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="creationDate")
    def creation_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationDate"))

    @builtins.property
    @jsii.member(jsii_name="defaultSecondaryLocation")
    def default_secondary_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSecondaryLocation"))

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryption"))

    @builtins.property
    @jsii.member(jsii_name="import")
    def import_(self) -> "SqlDatabaseImportOutputReference":
        return typing.cast("SqlDatabaseImportOutputReference", jsii.get(self, "import"))

    @builtins.property
    @jsii.member(jsii_name="threatDetectionPolicy")
    def threat_detection_policy(
        self,
    ) -> "SqlDatabaseThreatDetectionPolicyOutputReference":
        return typing.cast("SqlDatabaseThreatDetectionPolicyOutputReference", jsii.get(self, "threatDetectionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SqlDatabaseTimeoutsOutputReference":
        return typing.cast("SqlDatabaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="collationInput")
    def collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collationInput"))

    @builtins.property
    @jsii.member(jsii_name="createModeInput")
    def create_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createModeInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticPoolNameInput")
    def elastic_pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticPoolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importInput")
    def import_input(self) -> typing.Optional["SqlDatabaseImport"]:
        return typing.cast(typing.Optional["SqlDatabaseImport"], jsii.get(self, "importInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSizeBytesInput")
    def max_size_bytes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxSizeBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSizeGbInput")
    def max_size_gb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="readScaleInput")
    def read_scale_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readScaleInput"))

    @builtins.property
    @jsii.member(jsii_name="requestedServiceObjectiveIdInput")
    def requested_service_objective_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestedServiceObjectiveIdInput"))

    @builtins.property
    @jsii.member(jsii_name="requestedServiceObjectiveNameInput")
    def requested_service_objective_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestedServiceObjectiveNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="restorePointInTimeInput")
    def restore_point_in_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restorePointInTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="serverNameInput")
    def server_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDatabaseDeletionDateInput")
    def source_database_deletion_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDatabaseDeletionDateInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDatabaseIdInput")
    def source_database_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDatabaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="threatDetectionPolicyInput")
    def threat_detection_policy_input(
        self,
    ) -> typing.Optional["SqlDatabaseThreatDetectionPolicy"]:
        return typing.cast(typing.Optional["SqlDatabaseThreatDetectionPolicy"], jsii.get(self, "threatDetectionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["SqlDatabaseTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["SqlDatabaseTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneRedundantInput")
    def zone_redundant_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zoneRedundantInput"))

    @builtins.property
    @jsii.member(jsii_name="collation")
    def collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collation"))

    @collation.setter
    def collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51916fceb9339d271cb8ebe51957ebafdff29c3ea83df3d3a90cbcd04a55fcef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collation", value)

    @builtins.property
    @jsii.member(jsii_name="createMode")
    def create_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createMode"))

    @create_mode.setter
    def create_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2aea43b051be6afe36ad489c4eeda65b6934de42a65f1cbde33b93dbf4d1d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createMode", value)

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330f57049d31efbcc3c1ed3faeef2791ecedc9b053ce9c8b86e5b2490715a208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value)

    @builtins.property
    @jsii.member(jsii_name="elasticPoolName")
    def elastic_pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticPoolName"))

    @elastic_pool_name.setter
    def elastic_pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da18e7bdfa25c8aeec0717cde510f87f7806e2089c681c4cd54454f7ceae7502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticPoolName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f0f95b170f3b724cbe087fd17ca5d2b29d4aaa6eec90b7969b18c0e46a0a15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc1312bf1d6ec7940bfc07458d2bf6a32c1bc7da055f36448429e5eade9b0c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="maxSizeBytes")
    def max_size_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxSizeBytes"))

    @max_size_bytes.setter
    def max_size_bytes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e069f4cd2a425a84b9f218564d787875fb90339859f019929f0de2ebf2de16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSizeBytes", value)

    @builtins.property
    @jsii.member(jsii_name="maxSizeGb")
    def max_size_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxSizeGb"))

    @max_size_gb.setter
    def max_size_gb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27565f2480032b0fc544d75acf61e4f073cf67d806a156c61a324b753cdffdab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSizeGb", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ee022ed6c2dc7b87067ad1fbdd46cda139057ad49c2661010f0c60d19e815b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="readScale")
    def read_scale(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readScale"))

    @read_scale.setter
    def read_scale(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851c8be68d24b4a4a3889e7c6272330832aa356ef38f7e75c56ce2fb08af8cf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readScale", value)

    @builtins.property
    @jsii.member(jsii_name="requestedServiceObjectiveId")
    def requested_service_objective_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestedServiceObjectiveId"))

    @requested_service_objective_id.setter
    def requested_service_objective_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037be30f6c28d9993ccde04704dc83e020b2057860e3c24eec2e86c82c2ceef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedServiceObjectiveId", value)

    @builtins.property
    @jsii.member(jsii_name="requestedServiceObjectiveName")
    def requested_service_objective_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestedServiceObjectiveName"))

    @requested_service_objective_name.setter
    def requested_service_objective_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e48e6a0efa602b90e9a0a7c2f53040c43f05324813cdbca84eeaaf4ea1769db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestedServiceObjectiveName", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43902695fdea024823ab05edd4ac2047e3ba2283581c6ad45bac1a976d183d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="restorePointInTime")
    def restore_point_in_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restorePointInTime"))

    @restore_point_in_time.setter
    def restore_point_in_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7947358e1b90dc93981b1672788c064da78ed35a98b620f7689179478cdb2d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restorePointInTime", value)

    @builtins.property
    @jsii.member(jsii_name="serverName")
    def server_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverName"))

    @server_name.setter
    def server_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8625159f7b0520fd0ef783a7d9b463ec6532452dc499e55375a80131832eff97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverName", value)

    @builtins.property
    @jsii.member(jsii_name="sourceDatabaseDeletionDate")
    def source_database_deletion_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDatabaseDeletionDate"))

    @source_database_deletion_date.setter
    def source_database_deletion_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87dc6d5cf2cf1afa4d4418940d2a9b4c9c4c1c7595425c3c2e1429537a28271b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDatabaseDeletionDate", value)

    @builtins.property
    @jsii.member(jsii_name="sourceDatabaseId")
    def source_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDatabaseId"))

    @source_database_id.setter
    def source_database_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aef09c0af6b76e59c647647b1463c3a6e62af79ed002b93d9298ae678f7427b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDatabaseId", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e262578cf5a094fefadbfe8f27985597badaa0df8b06d18aca1934cefc30eba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="zoneRedundant")
    def zone_redundant(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zoneRedundant"))

    @zone_redundant.setter
    def zone_redundant(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae2bfd3a2a3bebc2c5f670e11982780944b4a34e84b9c76ff38df710851ab6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneRedundant", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlDatabase.SqlDatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "server_name": "serverName",
        "collation": "collation",
        "create_mode": "createMode",
        "edition": "edition",
        "elastic_pool_name": "elasticPoolName",
        "id": "id",
        "import_": "import",
        "max_size_bytes": "maxSizeBytes",
        "max_size_gb": "maxSizeGb",
        "read_scale": "readScale",
        "requested_service_objective_id": "requestedServiceObjectiveId",
        "requested_service_objective_name": "requestedServiceObjectiveName",
        "restore_point_in_time": "restorePointInTime",
        "source_database_deletion_date": "sourceDatabaseDeletionDate",
        "source_database_id": "sourceDatabaseId",
        "tags": "tags",
        "threat_detection_policy": "threatDetectionPolicy",
        "timeouts": "timeouts",
        "zone_redundant": "zoneRedundant",
    },
)
class SqlDatabaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        server_name: builtins.str,
        collation: typing.Optional[builtins.str] = None,
        create_mode: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        elastic_pool_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        import_: typing.Optional[typing.Union["SqlDatabaseImport", typing.Dict[builtins.str, typing.Any]]] = None,
        max_size_bytes: typing.Optional[builtins.str] = None,
        max_size_gb: typing.Optional[builtins.str] = None,
        read_scale: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        requested_service_objective_id: typing.Optional[builtins.str] = None,
        requested_service_objective_name: typing.Optional[builtins.str] = None,
        restore_point_in_time: typing.Optional[builtins.str] = None,
        source_database_deletion_date: typing.Optional[builtins.str] = None,
        source_database_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        threat_detection_policy: typing.Optional[typing.Union["SqlDatabaseThreatDetectionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["SqlDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#location SqlDatabase#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#name SqlDatabase#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#resource_group_name SqlDatabase#resource_group_name}.
        :param server_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#server_name SqlDatabase#server_name}.
        :param collation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#collation SqlDatabase#collation}.
        :param create_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#create_mode SqlDatabase#create_mode}.
        :param edition: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#edition SqlDatabase#edition}.
        :param elastic_pool_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#elastic_pool_name SqlDatabase#elastic_pool_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#id SqlDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_: import block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#import SqlDatabase#import}
        :param max_size_bytes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#max_size_bytes SqlDatabase#max_size_bytes}.
        :param max_size_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#max_size_gb SqlDatabase#max_size_gb}.
        :param read_scale: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#read_scale SqlDatabase#read_scale}.
        :param requested_service_objective_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#requested_service_objective_id SqlDatabase#requested_service_objective_id}.
        :param requested_service_objective_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#requested_service_objective_name SqlDatabase#requested_service_objective_name}.
        :param restore_point_in_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#restore_point_in_time SqlDatabase#restore_point_in_time}.
        :param source_database_deletion_date: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#source_database_deletion_date SqlDatabase#source_database_deletion_date}.
        :param source_database_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#source_database_id SqlDatabase#source_database_id}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#tags SqlDatabase#tags}.
        :param threat_detection_policy: threat_detection_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#threat_detection_policy SqlDatabase#threat_detection_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#timeouts SqlDatabase#timeouts}
        :param zone_redundant: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#zone_redundant SqlDatabase#zone_redundant}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(import_, dict):
            import_ = SqlDatabaseImport(**import_)
        if isinstance(threat_detection_policy, dict):
            threat_detection_policy = SqlDatabaseThreatDetectionPolicy(**threat_detection_policy)
        if isinstance(timeouts, dict):
            timeouts = SqlDatabaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed228f4839ff93ae68d240cda6a21b3333c680886cf675c4c9212b25dd8309f7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
            check_type(argname="argument collation", value=collation, expected_type=type_hints["collation"])
            check_type(argname="argument create_mode", value=create_mode, expected_type=type_hints["create_mode"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument elastic_pool_name", value=elastic_pool_name, expected_type=type_hints["elastic_pool_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument import_", value=import_, expected_type=type_hints["import_"])
            check_type(argname="argument max_size_bytes", value=max_size_bytes, expected_type=type_hints["max_size_bytes"])
            check_type(argname="argument max_size_gb", value=max_size_gb, expected_type=type_hints["max_size_gb"])
            check_type(argname="argument read_scale", value=read_scale, expected_type=type_hints["read_scale"])
            check_type(argname="argument requested_service_objective_id", value=requested_service_objective_id, expected_type=type_hints["requested_service_objective_id"])
            check_type(argname="argument requested_service_objective_name", value=requested_service_objective_name, expected_type=type_hints["requested_service_objective_name"])
            check_type(argname="argument restore_point_in_time", value=restore_point_in_time, expected_type=type_hints["restore_point_in_time"])
            check_type(argname="argument source_database_deletion_date", value=source_database_deletion_date, expected_type=type_hints["source_database_deletion_date"])
            check_type(argname="argument source_database_id", value=source_database_id, expected_type=type_hints["source_database_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument threat_detection_policy", value=threat_detection_policy, expected_type=type_hints["threat_detection_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zone_redundant", value=zone_redundant, expected_type=type_hints["zone_redundant"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "server_name": server_name,
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
        if collation is not None:
            self._values["collation"] = collation
        if create_mode is not None:
            self._values["create_mode"] = create_mode
        if edition is not None:
            self._values["edition"] = edition
        if elastic_pool_name is not None:
            self._values["elastic_pool_name"] = elastic_pool_name
        if id is not None:
            self._values["id"] = id
        if import_ is not None:
            self._values["import_"] = import_
        if max_size_bytes is not None:
            self._values["max_size_bytes"] = max_size_bytes
        if max_size_gb is not None:
            self._values["max_size_gb"] = max_size_gb
        if read_scale is not None:
            self._values["read_scale"] = read_scale
        if requested_service_objective_id is not None:
            self._values["requested_service_objective_id"] = requested_service_objective_id
        if requested_service_objective_name is not None:
            self._values["requested_service_objective_name"] = requested_service_objective_name
        if restore_point_in_time is not None:
            self._values["restore_point_in_time"] = restore_point_in_time
        if source_database_deletion_date is not None:
            self._values["source_database_deletion_date"] = source_database_deletion_date
        if source_database_id is not None:
            self._values["source_database_id"] = source_database_id
        if tags is not None:
            self._values["tags"] = tags
        if threat_detection_policy is not None:
            self._values["threat_detection_policy"] = threat_detection_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if zone_redundant is not None:
            self._values["zone_redundant"] = zone_redundant

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#location SqlDatabase#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#name SqlDatabase#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#resource_group_name SqlDatabase#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#server_name SqlDatabase#server_name}.'''
        result = self._values.get("server_name")
        assert result is not None, "Required property 'server_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def collation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#collation SqlDatabase#collation}.'''
        result = self._values.get("collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#create_mode SqlDatabase#create_mode}.'''
        result = self._values.get("create_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#edition SqlDatabase#edition}.'''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elastic_pool_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#elastic_pool_name SqlDatabase#elastic_pool_name}.'''
        result = self._values.get("elastic_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#id SqlDatabase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_(self) -> typing.Optional["SqlDatabaseImport"]:
        '''import block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#import SqlDatabase#import}
        '''
        result = self._values.get("import_")
        return typing.cast(typing.Optional["SqlDatabaseImport"], result)

    @builtins.property
    def max_size_bytes(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#max_size_bytes SqlDatabase#max_size_bytes}.'''
        result = self._values.get("max_size_bytes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_size_gb(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#max_size_gb SqlDatabase#max_size_gb}.'''
        result = self._values.get("max_size_gb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_scale(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#read_scale SqlDatabase#read_scale}.'''
        result = self._values.get("read_scale")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def requested_service_objective_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#requested_service_objective_id SqlDatabase#requested_service_objective_id}.'''
        result = self._values.get("requested_service_objective_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requested_service_objective_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#requested_service_objective_name SqlDatabase#requested_service_objective_name}.'''
        result = self._values.get("requested_service_objective_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_point_in_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#restore_point_in_time SqlDatabase#restore_point_in_time}.'''
        result = self._values.get("restore_point_in_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_database_deletion_date(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#source_database_deletion_date SqlDatabase#source_database_deletion_date}.'''
        result = self._values.get("source_database_deletion_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_database_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#source_database_id SqlDatabase#source_database_id}.'''
        result = self._values.get("source_database_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#tags SqlDatabase#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def threat_detection_policy(
        self,
    ) -> typing.Optional["SqlDatabaseThreatDetectionPolicy"]:
        '''threat_detection_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#threat_detection_policy SqlDatabase#threat_detection_policy}
        '''
        result = self._values.get("threat_detection_policy")
        return typing.cast(typing.Optional["SqlDatabaseThreatDetectionPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SqlDatabaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#timeouts SqlDatabase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SqlDatabaseTimeouts"], result)

    @builtins.property
    def zone_redundant(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#zone_redundant SqlDatabase#zone_redundant}.'''
        result = self._values.get("zone_redundant")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlDatabase.SqlDatabaseImport",
    jsii_struct_bases=[],
    name_mapping={
        "administrator_login": "administratorLogin",
        "administrator_login_password": "administratorLoginPassword",
        "authentication_type": "authenticationType",
        "storage_key": "storageKey",
        "storage_key_type": "storageKeyType",
        "storage_uri": "storageUri",
        "operation_mode": "operationMode",
    },
)
class SqlDatabaseImport:
    def __init__(
        self,
        *,
        administrator_login: builtins.str,
        administrator_login_password: builtins.str,
        authentication_type: builtins.str,
        storage_key: builtins.str,
        storage_key_type: builtins.str,
        storage_uri: builtins.str,
        operation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param administrator_login: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#administrator_login SqlDatabase#administrator_login}.
        :param administrator_login_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#administrator_login_password SqlDatabase#administrator_login_password}.
        :param authentication_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#authentication_type SqlDatabase#authentication_type}.
        :param storage_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_key SqlDatabase#storage_key}.
        :param storage_key_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_key_type SqlDatabase#storage_key_type}.
        :param storage_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_uri SqlDatabase#storage_uri}.
        :param operation_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#operation_mode SqlDatabase#operation_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c37de158041b9e6b00e33b1a0a0166a93e9bbe877d303bf100a61652526f35)
            check_type(argname="argument administrator_login", value=administrator_login, expected_type=type_hints["administrator_login"])
            check_type(argname="argument administrator_login_password", value=administrator_login_password, expected_type=type_hints["administrator_login_password"])
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument storage_key", value=storage_key, expected_type=type_hints["storage_key"])
            check_type(argname="argument storage_key_type", value=storage_key_type, expected_type=type_hints["storage_key_type"])
            check_type(argname="argument storage_uri", value=storage_uri, expected_type=type_hints["storage_uri"])
            check_type(argname="argument operation_mode", value=operation_mode, expected_type=type_hints["operation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "administrator_login": administrator_login,
            "administrator_login_password": administrator_login_password,
            "authentication_type": authentication_type,
            "storage_key": storage_key,
            "storage_key_type": storage_key_type,
            "storage_uri": storage_uri,
        }
        if operation_mode is not None:
            self._values["operation_mode"] = operation_mode

    @builtins.property
    def administrator_login(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#administrator_login SqlDatabase#administrator_login}.'''
        result = self._values.get("administrator_login")
        assert result is not None, "Required property 'administrator_login' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administrator_login_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#administrator_login_password SqlDatabase#administrator_login_password}.'''
        result = self._values.get("administrator_login_password")
        assert result is not None, "Required property 'administrator_login_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#authentication_type SqlDatabase#authentication_type}.'''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_key SqlDatabase#storage_key}.'''
        result = self._values.get("storage_key")
        assert result is not None, "Required property 'storage_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_key_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_key_type SqlDatabase#storage_key_type}.'''
        result = self._values.get("storage_key_type")
        assert result is not None, "Required property 'storage_key_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_uri SqlDatabase#storage_uri}.'''
        result = self._values.get("storage_uri")
        assert result is not None, "Required property 'storage_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operation_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#operation_mode SqlDatabase#operation_mode}.'''
        result = self._values.get("operation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseImport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseImportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlDatabase.SqlDatabaseImportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f6087ad7bb67b582885c59ff19d4d431adf0fb017faf97959a61675fcc1c8fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOperationMode")
    def reset_operation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationMode", []))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginInput")
    def administrator_login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginPasswordInput")
    def administrator_login_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypeInput")
    def authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="operationModeInput")
    def operation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageKeyInput")
    def storage_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageKeyTypeInput")
    def storage_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageUriInput")
    def storage_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLogin")
    def administrator_login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLogin"))

    @administrator_login.setter
    def administrator_login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfc8f36c15c47e368778f8fc43fa6b63772b3b3577f8715dc71dea1daa6415d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLogin", value)

    @builtins.property
    @jsii.member(jsii_name="administratorLoginPassword")
    def administrator_login_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLoginPassword"))

    @administrator_login_password.setter
    def administrator_login_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a6440248d3ea095d4a156d8e50b6de9946b9855b4f06efbfc6d2444849c1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLoginPassword", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe456081b8cfa504718d7994ef022af2f2a1f3be702b84c41fb4270abc06378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value)

    @builtins.property
    @jsii.member(jsii_name="operationMode")
    def operation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationMode"))

    @operation_mode.setter
    def operation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304f4317371fe933d3c52e22c7120b17799c3511622b29299a9f08464be0a416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationMode", value)

    @builtins.property
    @jsii.member(jsii_name="storageKey")
    def storage_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageKey"))

    @storage_key.setter
    def storage_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b02f2536de3cc3bca78ea15f99f51b202322759eab72ed3aa245c2d2cc172da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageKey", value)

    @builtins.property
    @jsii.member(jsii_name="storageKeyType")
    def storage_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageKeyType"))

    @storage_key_type.setter
    def storage_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2b4253dbfb76658d2c7c8a092b2f5e5f75056ed2d74ee5e70ef4c64c6e1677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageKeyType", value)

    @builtins.property
    @jsii.member(jsii_name="storageUri")
    def storage_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageUri"))

    @storage_uri.setter
    def storage_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d738abdc784445b8132636302c887ec735fa88a3a4fdd4c78c549b77032aa6b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageUri", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SqlDatabaseImport]:
        return typing.cast(typing.Optional[SqlDatabaseImport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SqlDatabaseImport]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20aafc1d789a49159f6920848bd8e4923363e814aaf539112982343f3312be84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlDatabase.SqlDatabaseThreatDetectionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "disabled_alerts": "disabledAlerts",
        "email_account_admins": "emailAccountAdmins",
        "email_addresses": "emailAddresses",
        "retention_days": "retentionDays",
        "state": "state",
        "storage_account_access_key": "storageAccountAccessKey",
        "storage_endpoint": "storageEndpoint",
    },
)
class SqlDatabaseThreatDetectionPolicy:
    def __init__(
        self,
        *,
        disabled_alerts: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_account_admins: typing.Optional[builtins.str] = None,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        state: typing.Optional[builtins.str] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disabled_alerts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#disabled_alerts SqlDatabase#disabled_alerts}.
        :param email_account_admins: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#email_account_admins SqlDatabase#email_account_admins}.
        :param email_addresses: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#email_addresses SqlDatabase#email_addresses}.
        :param retention_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#retention_days SqlDatabase#retention_days}.
        :param state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#state SqlDatabase#state}.
        :param storage_account_access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_account_access_key SqlDatabase#storage_account_access_key}.
        :param storage_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_endpoint SqlDatabase#storage_endpoint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de515d4984555dce410aa77a220159b76761c7d3e62a4eb7e90e589823d2d59)
            check_type(argname="argument disabled_alerts", value=disabled_alerts, expected_type=type_hints["disabled_alerts"])
            check_type(argname="argument email_account_admins", value=email_account_admins, expected_type=type_hints["email_account_admins"])
            check_type(argname="argument email_addresses", value=email_addresses, expected_type=type_hints["email_addresses"])
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument storage_account_access_key", value=storage_account_access_key, expected_type=type_hints["storage_account_access_key"])
            check_type(argname="argument storage_endpoint", value=storage_endpoint, expected_type=type_hints["storage_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled_alerts is not None:
            self._values["disabled_alerts"] = disabled_alerts
        if email_account_admins is not None:
            self._values["email_account_admins"] = email_account_admins
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses
        if retention_days is not None:
            self._values["retention_days"] = retention_days
        if state is not None:
            self._values["state"] = state
        if storage_account_access_key is not None:
            self._values["storage_account_access_key"] = storage_account_access_key
        if storage_endpoint is not None:
            self._values["storage_endpoint"] = storage_endpoint

    @builtins.property
    def disabled_alerts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#disabled_alerts SqlDatabase#disabled_alerts}.'''
        result = self._values.get("disabled_alerts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_account_admins(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#email_account_admins SqlDatabase#email_account_admins}.'''
        result = self._values.get("email_account_admins")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#email_addresses SqlDatabase#email_addresses}.'''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#retention_days SqlDatabase#retention_days}.'''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#state SqlDatabase#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_access_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_account_access_key SqlDatabase#storage_account_access_key}.'''
        result = self._values.get("storage_account_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#storage_endpoint SqlDatabase#storage_endpoint}.'''
        result = self._values.get("storage_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseThreatDetectionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseThreatDetectionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlDatabase.SqlDatabaseThreatDetectionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bc2a7f166947f249c71b5b5ff80a63c92f98202996a6be899119ab27e005546)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisabledAlerts")
    def reset_disabled_alerts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabledAlerts", []))

    @jsii.member(jsii_name="resetEmailAccountAdmins")
    def reset_email_account_admins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAccountAdmins", []))

    @jsii.member(jsii_name="resetEmailAddresses")
    def reset_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddresses", []))

    @jsii.member(jsii_name="resetRetentionDays")
    def reset_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDays", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetStorageAccountAccessKey")
    def reset_storage_account_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountAccessKey", []))

    @jsii.member(jsii_name="resetStorageEndpoint")
    def reset_storage_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageEndpoint", []))

    @builtins.property
    @jsii.member(jsii_name="disabledAlertsInput")
    def disabled_alerts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "disabledAlertsInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAccountAdminsInput")
    def email_account_admins_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailAccountAdminsInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddressesInput")
    def email_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDaysInput")
    def retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKeyInput")
    def storage_account_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageEndpointInput")
    def storage_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledAlerts")
    def disabled_alerts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "disabledAlerts"))

    @disabled_alerts.setter
    def disabled_alerts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5054cc4ec93b33ca182ce8f347453a7030b71b15989f8aabc43901e2b4c3b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabledAlerts", value)

    @builtins.property
    @jsii.member(jsii_name="emailAccountAdmins")
    def email_account_admins(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailAccountAdmins"))

    @email_account_admins.setter
    def email_account_admins(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93e7a43222ec5b57d218ebc4ea2426f1005cef6ca6a4e8e439dafe1a808e588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAccountAdmins", value)

    @builtins.property
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @email_addresses.setter
    def email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60705b73ee7753d200476a0d5418d6ccd9245f60f4ff3300fde5aa87aa88fd4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDays"))

    @retention_days.setter
    def retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837fb7466c220abe2c001b45913a088d3687104c0007110cf3b945e14668855e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDays", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72405cc86881515d28935f4592d50f11f8a8ff7fb87891bb5acdb202bc9340a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKey")
    def storage_account_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountAccessKey"))

    @storage_account_access_key.setter
    def storage_account_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f235ac10318b427935ef3d5c3e026be3d002cdac6cbfb28138926fc8a0faab2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountAccessKey", value)

    @builtins.property
    @jsii.member(jsii_name="storageEndpoint")
    def storage_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageEndpoint"))

    @storage_endpoint.setter
    def storage_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aefd8199dcc7e78176a1d7e3a57ba9e82565f86aee33b9930943468e7e8ed01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SqlDatabaseThreatDetectionPolicy]:
        return typing.cast(typing.Optional[SqlDatabaseThreatDetectionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseThreatDetectionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b565428ebc36e2d76570f23f6562a9317fd4bad77258f5f3beda3a1669a110e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlDatabase.SqlDatabaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SqlDatabaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#create SqlDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#delete SqlDatabase#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#read SqlDatabase#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#update SqlDatabase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b2032daa9581b2df5713dfb367011d0aa25a11f643037d9fa195cbd7be29f0)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#create SqlDatabase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#delete SqlDatabase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#read SqlDatabase#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_database#update SqlDatabase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlDatabase.SqlDatabaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41c8a8c0f93279b59c49d9904441a19ff174256fb0ad86e8251a705159ced890)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__34d38e8bd3f0b9bf4a48a3f8b81f3c51d81f63c42fb5265357e388ed5ae358b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d548feb3558e6d3669051846d5e90815ff87d6f1612caa744d44015ffc223d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cac0bcc7c350c56e05a22a384e19daf5ba95f7fad40d12955aa2a5d1729acc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e083c8dbeff59bd0cb3dc0be6219abbc7ec1cd7725a093e5594366660708330d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SqlDatabaseTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SqlDatabaseTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SqlDatabaseTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8153e3d2c316d6d8e0bc71900bd620d47c26b7edc157285d87bec7ebf82a21a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SqlDatabase",
    "SqlDatabaseConfig",
    "SqlDatabaseImport",
    "SqlDatabaseImportOutputReference",
    "SqlDatabaseThreatDetectionPolicy",
    "SqlDatabaseThreatDetectionPolicyOutputReference",
    "SqlDatabaseTimeouts",
    "SqlDatabaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e06b8a54307ec6e963d4f2b7b956f858b2a988e03048a46200c822deb3edcbb2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    server_name: builtins.str,
    collation: typing.Optional[builtins.str] = None,
    create_mode: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    elastic_pool_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    import_: typing.Optional[typing.Union[SqlDatabaseImport, typing.Dict[builtins.str, typing.Any]]] = None,
    max_size_bytes: typing.Optional[builtins.str] = None,
    max_size_gb: typing.Optional[builtins.str] = None,
    read_scale: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    requested_service_objective_id: typing.Optional[builtins.str] = None,
    requested_service_objective_name: typing.Optional[builtins.str] = None,
    restore_point_in_time: typing.Optional[builtins.str] = None,
    source_database_deletion_date: typing.Optional[builtins.str] = None,
    source_database_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    threat_detection_policy: typing.Optional[typing.Union[SqlDatabaseThreatDetectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[SqlDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__51916fceb9339d271cb8ebe51957ebafdff29c3ea83df3d3a90cbcd04a55fcef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2aea43b051be6afe36ad489c4eeda65b6934de42a65f1cbde33b93dbf4d1d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330f57049d31efbcc3c1ed3faeef2791ecedc9b053ce9c8b86e5b2490715a208(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da18e7bdfa25c8aeec0717cde510f87f7806e2089c681c4cd54454f7ceae7502(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f0f95b170f3b724cbe087fd17ca5d2b29d4aaa6eec90b7969b18c0e46a0a15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc1312bf1d6ec7940bfc07458d2bf6a32c1bc7da055f36448429e5eade9b0c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e069f4cd2a425a84b9f218564d787875fb90339859f019929f0de2ebf2de16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27565f2480032b0fc544d75acf61e4f073cf67d806a156c61a324b753cdffdab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ee022ed6c2dc7b87067ad1fbdd46cda139057ad49c2661010f0c60d19e815b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851c8be68d24b4a4a3889e7c6272330832aa356ef38f7e75c56ce2fb08af8cf9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037be30f6c28d9993ccde04704dc83e020b2057860e3c24eec2e86c82c2ceef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e48e6a0efa602b90e9a0a7c2f53040c43f05324813cdbca84eeaaf4ea1769db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43902695fdea024823ab05edd4ac2047e3ba2283581c6ad45bac1a976d183d9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7947358e1b90dc93981b1672788c064da78ed35a98b620f7689179478cdb2d35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8625159f7b0520fd0ef783a7d9b463ec6532452dc499e55375a80131832eff97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87dc6d5cf2cf1afa4d4418940d2a9b4c9c4c1c7595425c3c2e1429537a28271b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef09c0af6b76e59c647647b1463c3a6e62af79ed002b93d9298ae678f7427b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e262578cf5a094fefadbfe8f27985597badaa0df8b06d18aca1934cefc30eba5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae2bfd3a2a3bebc2c5f670e11982780944b4a34e84b9c76ff38df710851ab6e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed228f4839ff93ae68d240cda6a21b3333c680886cf675c4c9212b25dd8309f7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    server_name: builtins.str,
    collation: typing.Optional[builtins.str] = None,
    create_mode: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    elastic_pool_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    import_: typing.Optional[typing.Union[SqlDatabaseImport, typing.Dict[builtins.str, typing.Any]]] = None,
    max_size_bytes: typing.Optional[builtins.str] = None,
    max_size_gb: typing.Optional[builtins.str] = None,
    read_scale: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    requested_service_objective_id: typing.Optional[builtins.str] = None,
    requested_service_objective_name: typing.Optional[builtins.str] = None,
    restore_point_in_time: typing.Optional[builtins.str] = None,
    source_database_deletion_date: typing.Optional[builtins.str] = None,
    source_database_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    threat_detection_policy: typing.Optional[typing.Union[SqlDatabaseThreatDetectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[SqlDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c37de158041b9e6b00e33b1a0a0166a93e9bbe877d303bf100a61652526f35(
    *,
    administrator_login: builtins.str,
    administrator_login_password: builtins.str,
    authentication_type: builtins.str,
    storage_key: builtins.str,
    storage_key_type: builtins.str,
    storage_uri: builtins.str,
    operation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6087ad7bb67b582885c59ff19d4d431adf0fb017faf97959a61675fcc1c8fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfc8f36c15c47e368778f8fc43fa6b63772b3b3577f8715dc71dea1daa6415d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a6440248d3ea095d4a156d8e50b6de9946b9855b4f06efbfc6d2444849c1ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe456081b8cfa504718d7994ef022af2f2a1f3be702b84c41fb4270abc06378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304f4317371fe933d3c52e22c7120b17799c3511622b29299a9f08464be0a416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b02f2536de3cc3bca78ea15f99f51b202322759eab72ed3aa245c2d2cc172da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2b4253dbfb76658d2c7c8a092b2f5e5f75056ed2d74ee5e70ef4c64c6e1677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d738abdc784445b8132636302c887ec735fa88a3a4fdd4c78c549b77032aa6b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20aafc1d789a49159f6920848bd8e4923363e814aaf539112982343f3312be84(
    value: typing.Optional[SqlDatabaseImport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de515d4984555dce410aa77a220159b76761c7d3e62a4eb7e90e589823d2d59(
    *,
    disabled_alerts: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_account_admins: typing.Optional[builtins.str] = None,
    email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    retention_days: typing.Optional[jsii.Number] = None,
    state: typing.Optional[builtins.str] = None,
    storage_account_access_key: typing.Optional[builtins.str] = None,
    storage_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc2a7f166947f249c71b5b5ff80a63c92f98202996a6be899119ab27e005546(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5054cc4ec93b33ca182ce8f347453a7030b71b15989f8aabc43901e2b4c3b98(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93e7a43222ec5b57d218ebc4ea2426f1005cef6ca6a4e8e439dafe1a808e588(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60705b73ee7753d200476a0d5418d6ccd9245f60f4ff3300fde5aa87aa88fd4f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837fb7466c220abe2c001b45913a088d3687104c0007110cf3b945e14668855e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72405cc86881515d28935f4592d50f11f8a8ff7fb87891bb5acdb202bc9340a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f235ac10318b427935ef3d5c3e026be3d002cdac6cbfb28138926fc8a0faab2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aefd8199dcc7e78176a1d7e3a57ba9e82565f86aee33b9930943468e7e8ed01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b565428ebc36e2d76570f23f6562a9317fd4bad77258f5f3beda3a1669a110e3(
    value: typing.Optional[SqlDatabaseThreatDetectionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b2032daa9581b2df5713dfb367011d0aa25a11f643037d9fa195cbd7be29f0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c8a8c0f93279b59c49d9904441a19ff174256fb0ad86e8251a705159ced890(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d38e8bd3f0b9bf4a48a3f8b81f3c51d81f63c42fb5265357e388ed5ae358b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d548feb3558e6d3669051846d5e90815ff87d6f1612caa744d44015ffc223d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cac0bcc7c350c56e05a22a384e19daf5ba95f7fad40d12955aa2a5d1729acc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e083c8dbeff59bd0cb3dc0be6219abbc7ec1cd7725a093e5594366660708330d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8153e3d2c316d6d8e0bc71900bd620d47c26b7edc157285d87bec7ebf82a21a0(
    value: typing.Optional[typing.Union[SqlDatabaseTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
