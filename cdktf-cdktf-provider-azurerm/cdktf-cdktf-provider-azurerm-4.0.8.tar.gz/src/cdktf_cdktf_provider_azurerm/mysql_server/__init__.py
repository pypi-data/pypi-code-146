'''
# `azurerm_mysql_server`

Refer to the Terraform Registory for docs: [`azurerm_mysql_server`](https://www.terraform.io/docs/providers/azurerm/r/mysql_server).
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


class MysqlServer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mysqlServer.MysqlServer",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server azurerm_mysql_server}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku_name: builtins.str,
        ssl_enforcement_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        version: builtins.str,
        administrator_login: typing.Optional[builtins.str] = None,
        administrator_login_password: typing.Optional[builtins.str] = None,
        auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backup_retention_days: typing.Optional[jsii.Number] = None,
        create_mode: typing.Optional[builtins.str] = None,
        creation_source_server_id: typing.Optional[builtins.str] = None,
        geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["MysqlServerIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restore_point_in_time: typing.Optional[builtins.str] = None,
        ssl_minimal_tls_version_enforced: typing.Optional[builtins.str] = None,
        storage_mb: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        threat_detection_policy: typing.Optional[typing.Union["MysqlServerThreatDetectionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MysqlServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server azurerm_mysql_server} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#location MysqlServer#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#name MysqlServer#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#resource_group_name MysqlServer#resource_group_name}.
        :param sku_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#sku_name MysqlServer#sku_name}.
        :param ssl_enforcement_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#ssl_enforcement_enabled MysqlServer#ssl_enforcement_enabled}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#version MysqlServer#version}.
        :param administrator_login: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#administrator_login MysqlServer#administrator_login}.
        :param administrator_login_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#administrator_login_password MysqlServer#administrator_login_password}.
        :param auto_grow_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#auto_grow_enabled MysqlServer#auto_grow_enabled}.
        :param backup_retention_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#backup_retention_days MysqlServer#backup_retention_days}.
        :param create_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#create_mode MysqlServer#create_mode}.
        :param creation_source_server_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#creation_source_server_id MysqlServer#creation_source_server_id}.
        :param geo_redundant_backup_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#geo_redundant_backup_enabled MysqlServer#geo_redundant_backup_enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#id MysqlServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#identity MysqlServer#identity}
        :param infrastructure_encryption_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#infrastructure_encryption_enabled MysqlServer#infrastructure_encryption_enabled}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#public_network_access_enabled MysqlServer#public_network_access_enabled}.
        :param restore_point_in_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#restore_point_in_time MysqlServer#restore_point_in_time}.
        :param ssl_minimal_tls_version_enforced: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#ssl_minimal_tls_version_enforced MysqlServer#ssl_minimal_tls_version_enforced}.
        :param storage_mb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#storage_mb MysqlServer#storage_mb}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#tags MysqlServer#tags}.
        :param threat_detection_policy: threat_detection_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#threat_detection_policy MysqlServer#threat_detection_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#timeouts MysqlServer#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628dd63da6aa03011cd6b6cce28294dfe9902e3e24f33f91b6dbd466239de012)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MysqlServerConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            sku_name=sku_name,
            ssl_enforcement_enabled=ssl_enforcement_enabled,
            version=version,
            administrator_login=administrator_login,
            administrator_login_password=administrator_login_password,
            auto_grow_enabled=auto_grow_enabled,
            backup_retention_days=backup_retention_days,
            create_mode=create_mode,
            creation_source_server_id=creation_source_server_id,
            geo_redundant_backup_enabled=geo_redundant_backup_enabled,
            id=id,
            identity=identity,
            infrastructure_encryption_enabled=infrastructure_encryption_enabled,
            public_network_access_enabled=public_network_access_enabled,
            restore_point_in_time=restore_point_in_time,
            ssl_minimal_tls_version_enforced=ssl_minimal_tls_version_enforced,
            storage_mb=storage_mb,
            tags=tags,
            threat_detection_policy=threat_detection_policy,
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

    @jsii.member(jsii_name="putIdentity")
    def put_identity(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#type MysqlServer#type}.
        '''
        value = MysqlServerIdentity(type=type)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putThreatDetectionPolicy")
    def put_threat_detection_policy(
        self,
        *,
        disabled_alerts: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_account_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disabled_alerts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#disabled_alerts MysqlServer#disabled_alerts}.
        :param email_account_admins: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#email_account_admins MysqlServer#email_account_admins}.
        :param email_addresses: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#email_addresses MysqlServer#email_addresses}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#enabled MysqlServer#enabled}.
        :param retention_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#retention_days MysqlServer#retention_days}.
        :param storage_account_access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#storage_account_access_key MysqlServer#storage_account_access_key}.
        :param storage_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#storage_endpoint MysqlServer#storage_endpoint}.
        '''
        value = MysqlServerThreatDetectionPolicy(
            disabled_alerts=disabled_alerts,
            email_account_admins=email_account_admins,
            email_addresses=email_addresses,
            enabled=enabled,
            retention_days=retention_days,
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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#create MysqlServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#delete MysqlServer#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#read MysqlServer#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#update MysqlServer#update}.
        '''
        value = MysqlServerTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdministratorLogin")
    def reset_administrator_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorLogin", []))

    @jsii.member(jsii_name="resetAdministratorLoginPassword")
    def reset_administrator_login_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorLoginPassword", []))

    @jsii.member(jsii_name="resetAutoGrowEnabled")
    def reset_auto_grow_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoGrowEnabled", []))

    @jsii.member(jsii_name="resetBackupRetentionDays")
    def reset_backup_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupRetentionDays", []))

    @jsii.member(jsii_name="resetCreateMode")
    def reset_create_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateMode", []))

    @jsii.member(jsii_name="resetCreationSourceServerId")
    def reset_creation_source_server_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreationSourceServerId", []))

    @jsii.member(jsii_name="resetGeoRedundantBackupEnabled")
    def reset_geo_redundant_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoRedundantBackupEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetInfrastructureEncryptionEnabled")
    def reset_infrastructure_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfrastructureEncryptionEnabled", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetRestorePointInTime")
    def reset_restore_point_in_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestorePointInTime", []))

    @jsii.member(jsii_name="resetSslMinimalTlsVersionEnforced")
    def reset_ssl_minimal_tls_version_enforced(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslMinimalTlsVersionEnforced", []))

    @jsii.member(jsii_name="resetStorageMb")
    def reset_storage_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageMb", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetThreatDetectionPolicy")
    def reset_threat_detection_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreatDetectionPolicy", []))

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
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "MysqlServerIdentityOutputReference":
        return typing.cast("MysqlServerIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="threatDetectionPolicy")
    def threat_detection_policy(
        self,
    ) -> "MysqlServerThreatDetectionPolicyOutputReference":
        return typing.cast("MysqlServerThreatDetectionPolicyOutputReference", jsii.get(self, "threatDetectionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MysqlServerTimeoutsOutputReference":
        return typing.cast("MysqlServerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginInput")
    def administrator_login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginPasswordInput")
    def administrator_login_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="autoGrowEnabledInput")
    def auto_grow_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoGrowEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionDaysInput")
    def backup_retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRetentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="createModeInput")
    def create_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createModeInput"))

    @builtins.property
    @jsii.member(jsii_name="creationSourceServerIdInput")
    def creation_source_server_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creationSourceServerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="geoRedundantBackupEnabledInput")
    def geo_redundant_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "geoRedundantBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["MysqlServerIdentity"]:
        return typing.cast(typing.Optional["MysqlServerIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureEncryptionEnabledInput")
    def infrastructure_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "infrastructureEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="restorePointInTimeInput")
    def restore_point_in_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restorePointInTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sslEnforcementEnabledInput")
    def ssl_enforcement_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sslEnforcementEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sslMinimalTlsVersionEnforcedInput")
    def ssl_minimal_tls_version_enforced_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslMinimalTlsVersionEnforcedInput"))

    @builtins.property
    @jsii.member(jsii_name="storageMbInput")
    def storage_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageMbInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="threatDetectionPolicyInput")
    def threat_detection_policy_input(
        self,
    ) -> typing.Optional["MysqlServerThreatDetectionPolicy"]:
        return typing.cast(typing.Optional["MysqlServerThreatDetectionPolicy"], jsii.get(self, "threatDetectionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MysqlServerTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MysqlServerTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLogin")
    def administrator_login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLogin"))

    @administrator_login.setter
    def administrator_login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062b2a5b52710076e46095051e9fd4f055efb700a766b2c93c638b0b89567306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLogin", value)

    @builtins.property
    @jsii.member(jsii_name="administratorLoginPassword")
    def administrator_login_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLoginPassword"))

    @administrator_login_password.setter
    def administrator_login_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d24a1ed03655a63569e51252bdc270593f64198c7ec688bf59093f165d3710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLoginPassword", value)

    @builtins.property
    @jsii.member(jsii_name="autoGrowEnabled")
    def auto_grow_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoGrowEnabled"))

    @auto_grow_enabled.setter
    def auto_grow_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ee89c4e4d382fc78e3575e5f0ce0f089e38b3404212eb268604126fbccc01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoGrowEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="backupRetentionDays")
    def backup_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRetentionDays"))

    @backup_retention_days.setter
    def backup_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ae265d45df0df404bf145e2b5179c10834430ce0a2d981dc1f81e39b5f0845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetentionDays", value)

    @builtins.property
    @jsii.member(jsii_name="createMode")
    def create_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createMode"))

    @create_mode.setter
    def create_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8231a286ca1bbe6a19cc132e93f9bb6946018f7ced11a6d6d3e3577623d5f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createMode", value)

    @builtins.property
    @jsii.member(jsii_name="creationSourceServerId")
    def creation_source_server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationSourceServerId"))

    @creation_source_server_id.setter
    def creation_source_server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b79c7c9c5d6e47dad75e4e4e34937085f787542a26d08cc267effec85fa7db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creationSourceServerId", value)

    @builtins.property
    @jsii.member(jsii_name="geoRedundantBackupEnabled")
    def geo_redundant_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "geoRedundantBackupEnabled"))

    @geo_redundant_backup_enabled.setter
    def geo_redundant_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f52f1da10c2015b0e73a8cca090965eca76121ba297d1edfb19600dbd32889e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geoRedundantBackupEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1e7a902af91f3f2598571c31113a23878ed8d013d25a485f5f892a95b49beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="infrastructureEncryptionEnabled")
    def infrastructure_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "infrastructureEncryptionEnabled"))

    @infrastructure_encryption_enabled.setter
    def infrastructure_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f069c7847502cd9e17ab006ef2327a99a28a711381a6fde3840ca2b5839079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureEncryptionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2c461b19c0eb5432a9e0b04cad29e10f6a0797564165f8f9d04ef51cb556b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786e737e1b951faa5370a3192dba617f49a0f5fe27bd3e21733218c158fa3140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicNetworkAccessEnabled"))

    @public_network_access_enabled.setter
    def public_network_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4449adaa536f67a2110da5300195f23a1cd41f96c65490a70016f65d35877afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d262b81ca025718130c96b3426d0763fcf9ad3952f63e5d9627277c3527403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="restorePointInTime")
    def restore_point_in_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restorePointInTime"))

    @restore_point_in_time.setter
    def restore_point_in_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29323bb5e5c5f66b52dfa258ea6fffa7e4873a68df1b8eab7da5d6e746140650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restorePointInTime", value)

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3dfe7bea72becf31d40f561250780bfc111b4d3cf49562a986e09e101d5c176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value)

    @builtins.property
    @jsii.member(jsii_name="sslEnforcementEnabled")
    def ssl_enforcement_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sslEnforcementEnabled"))

    @ssl_enforcement_enabled.setter
    def ssl_enforcement_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6167848e90b9c809ef3582f2b980a6347a63c973187ba880fae8c8cff7c70c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslEnforcementEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="sslMinimalTlsVersionEnforced")
    def ssl_minimal_tls_version_enforced(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslMinimalTlsVersionEnforced"))

    @ssl_minimal_tls_version_enforced.setter
    def ssl_minimal_tls_version_enforced(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625ff7da97aa623a0a3ab6e8321c8158da6fcfef5716da56c915e578968a6a5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslMinimalTlsVersionEnforced", value)

    @builtins.property
    @jsii.member(jsii_name="storageMb")
    def storage_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageMb"))

    @storage_mb.setter
    def storage_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34dba863205d26bf2fa80eee81dab0f7ca455985eb64ff25a79538b9d0c002a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageMb", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fad3aef2746cb6261ecdebb1c7a4dad4f5467235d17c705a4c3481430bdeef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e4db10b21f225f3f787f513f42d7d1e5d3d1bb6bd583bea64879c840d39d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mysqlServer.MysqlServerConfig",
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
        "sku_name": "skuName",
        "ssl_enforcement_enabled": "sslEnforcementEnabled",
        "version": "version",
        "administrator_login": "administratorLogin",
        "administrator_login_password": "administratorLoginPassword",
        "auto_grow_enabled": "autoGrowEnabled",
        "backup_retention_days": "backupRetentionDays",
        "create_mode": "createMode",
        "creation_source_server_id": "creationSourceServerId",
        "geo_redundant_backup_enabled": "geoRedundantBackupEnabled",
        "id": "id",
        "identity": "identity",
        "infrastructure_encryption_enabled": "infrastructureEncryptionEnabled",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "restore_point_in_time": "restorePointInTime",
        "ssl_minimal_tls_version_enforced": "sslMinimalTlsVersionEnforced",
        "storage_mb": "storageMb",
        "tags": "tags",
        "threat_detection_policy": "threatDetectionPolicy",
        "timeouts": "timeouts",
    },
)
class MysqlServerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        sku_name: builtins.str,
        ssl_enforcement_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        version: builtins.str,
        administrator_login: typing.Optional[builtins.str] = None,
        administrator_login_password: typing.Optional[builtins.str] = None,
        auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backup_retention_days: typing.Optional[jsii.Number] = None,
        create_mode: typing.Optional[builtins.str] = None,
        creation_source_server_id: typing.Optional[builtins.str] = None,
        geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["MysqlServerIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restore_point_in_time: typing.Optional[builtins.str] = None,
        ssl_minimal_tls_version_enforced: typing.Optional[builtins.str] = None,
        storage_mb: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        threat_detection_policy: typing.Optional[typing.Union["MysqlServerThreatDetectionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MysqlServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#location MysqlServer#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#name MysqlServer#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#resource_group_name MysqlServer#resource_group_name}.
        :param sku_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#sku_name MysqlServer#sku_name}.
        :param ssl_enforcement_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#ssl_enforcement_enabled MysqlServer#ssl_enforcement_enabled}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#version MysqlServer#version}.
        :param administrator_login: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#administrator_login MysqlServer#administrator_login}.
        :param administrator_login_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#administrator_login_password MysqlServer#administrator_login_password}.
        :param auto_grow_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#auto_grow_enabled MysqlServer#auto_grow_enabled}.
        :param backup_retention_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#backup_retention_days MysqlServer#backup_retention_days}.
        :param create_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#create_mode MysqlServer#create_mode}.
        :param creation_source_server_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#creation_source_server_id MysqlServer#creation_source_server_id}.
        :param geo_redundant_backup_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#geo_redundant_backup_enabled MysqlServer#geo_redundant_backup_enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#id MysqlServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#identity MysqlServer#identity}
        :param infrastructure_encryption_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#infrastructure_encryption_enabled MysqlServer#infrastructure_encryption_enabled}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#public_network_access_enabled MysqlServer#public_network_access_enabled}.
        :param restore_point_in_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#restore_point_in_time MysqlServer#restore_point_in_time}.
        :param ssl_minimal_tls_version_enforced: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#ssl_minimal_tls_version_enforced MysqlServer#ssl_minimal_tls_version_enforced}.
        :param storage_mb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#storage_mb MysqlServer#storage_mb}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#tags MysqlServer#tags}.
        :param threat_detection_policy: threat_detection_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#threat_detection_policy MysqlServer#threat_detection_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#timeouts MysqlServer#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = MysqlServerIdentity(**identity)
        if isinstance(threat_detection_policy, dict):
            threat_detection_policy = MysqlServerThreatDetectionPolicy(**threat_detection_policy)
        if isinstance(timeouts, dict):
            timeouts = MysqlServerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb875ae2c12c59346fad2a9f7c5267b419a10b982907cf46a8856082dae399c3)
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
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument ssl_enforcement_enabled", value=ssl_enforcement_enabled, expected_type=type_hints["ssl_enforcement_enabled"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument administrator_login", value=administrator_login, expected_type=type_hints["administrator_login"])
            check_type(argname="argument administrator_login_password", value=administrator_login_password, expected_type=type_hints["administrator_login_password"])
            check_type(argname="argument auto_grow_enabled", value=auto_grow_enabled, expected_type=type_hints["auto_grow_enabled"])
            check_type(argname="argument backup_retention_days", value=backup_retention_days, expected_type=type_hints["backup_retention_days"])
            check_type(argname="argument create_mode", value=create_mode, expected_type=type_hints["create_mode"])
            check_type(argname="argument creation_source_server_id", value=creation_source_server_id, expected_type=type_hints["creation_source_server_id"])
            check_type(argname="argument geo_redundant_backup_enabled", value=geo_redundant_backup_enabled, expected_type=type_hints["geo_redundant_backup_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument infrastructure_encryption_enabled", value=infrastructure_encryption_enabled, expected_type=type_hints["infrastructure_encryption_enabled"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument restore_point_in_time", value=restore_point_in_time, expected_type=type_hints["restore_point_in_time"])
            check_type(argname="argument ssl_minimal_tls_version_enforced", value=ssl_minimal_tls_version_enforced, expected_type=type_hints["ssl_minimal_tls_version_enforced"])
            check_type(argname="argument storage_mb", value=storage_mb, expected_type=type_hints["storage_mb"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument threat_detection_policy", value=threat_detection_policy, expected_type=type_hints["threat_detection_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "sku_name": sku_name,
            "ssl_enforcement_enabled": ssl_enforcement_enabled,
            "version": version,
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
        if administrator_login is not None:
            self._values["administrator_login"] = administrator_login
        if administrator_login_password is not None:
            self._values["administrator_login_password"] = administrator_login_password
        if auto_grow_enabled is not None:
            self._values["auto_grow_enabled"] = auto_grow_enabled
        if backup_retention_days is not None:
            self._values["backup_retention_days"] = backup_retention_days
        if create_mode is not None:
            self._values["create_mode"] = create_mode
        if creation_source_server_id is not None:
            self._values["creation_source_server_id"] = creation_source_server_id
        if geo_redundant_backup_enabled is not None:
            self._values["geo_redundant_backup_enabled"] = geo_redundant_backup_enabled
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if infrastructure_encryption_enabled is not None:
            self._values["infrastructure_encryption_enabled"] = infrastructure_encryption_enabled
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if restore_point_in_time is not None:
            self._values["restore_point_in_time"] = restore_point_in_time
        if ssl_minimal_tls_version_enforced is not None:
            self._values["ssl_minimal_tls_version_enforced"] = ssl_minimal_tls_version_enforced
        if storage_mb is not None:
            self._values["storage_mb"] = storage_mb
        if tags is not None:
            self._values["tags"] = tags
        if threat_detection_policy is not None:
            self._values["threat_detection_policy"] = threat_detection_policy
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#location MysqlServer#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#name MysqlServer#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#resource_group_name MysqlServer#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#sku_name MysqlServer#sku_name}.'''
        result = self._values.get("sku_name")
        assert result is not None, "Required property 'sku_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssl_enforcement_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#ssl_enforcement_enabled MysqlServer#ssl_enforcement_enabled}.'''
        result = self._values.get("ssl_enforcement_enabled")
        assert result is not None, "Required property 'ssl_enforcement_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#version MysqlServer#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administrator_login(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#administrator_login MysqlServer#administrator_login}.'''
        result = self._values.get("administrator_login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def administrator_login_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#administrator_login_password MysqlServer#administrator_login_password}.'''
        result = self._values.get("administrator_login_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_grow_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#auto_grow_enabled MysqlServer#auto_grow_enabled}.'''
        result = self._values.get("auto_grow_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backup_retention_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#backup_retention_days MysqlServer#backup_retention_days}.'''
        result = self._values.get("backup_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def create_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#create_mode MysqlServer#create_mode}.'''
        result = self._values.get("create_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creation_source_server_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#creation_source_server_id MysqlServer#creation_source_server_id}.'''
        result = self._values.get("creation_source_server_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geo_redundant_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#geo_redundant_backup_enabled MysqlServer#geo_redundant_backup_enabled}.'''
        result = self._values.get("geo_redundant_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#id MysqlServer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["MysqlServerIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#identity MysqlServer#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["MysqlServerIdentity"], result)

    @builtins.property
    def infrastructure_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#infrastructure_encryption_enabled MysqlServer#infrastructure_encryption_enabled}.'''
        result = self._values.get("infrastructure_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#public_network_access_enabled MysqlServer#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restore_point_in_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#restore_point_in_time MysqlServer#restore_point_in_time}.'''
        result = self._values.get("restore_point_in_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_minimal_tls_version_enforced(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#ssl_minimal_tls_version_enforced MysqlServer#ssl_minimal_tls_version_enforced}.'''
        result = self._values.get("ssl_minimal_tls_version_enforced")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#storage_mb MysqlServer#storage_mb}.'''
        result = self._values.get("storage_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#tags MysqlServer#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def threat_detection_policy(
        self,
    ) -> typing.Optional["MysqlServerThreatDetectionPolicy"]:
        '''threat_detection_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#threat_detection_policy MysqlServer#threat_detection_policy}
        '''
        result = self._values.get("threat_detection_policy")
        return typing.cast(typing.Optional["MysqlServerThreatDetectionPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MysqlServerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#timeouts MysqlServer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MysqlServerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MysqlServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mysqlServer.MysqlServerIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class MysqlServerIdentity:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#type MysqlServer#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cf241d45944ebd8ad9a8318bf7a4776bfa4e98583bc017a09bf06187c415f4f)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#type MysqlServer#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MysqlServerIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MysqlServerIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mysqlServer.MysqlServerIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8151e18a58961248c26f891421562cc44c695e3a79a3344f9fd5a2b2dce4c07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e4517dad8bcc2aea3a7bf8ea2dba57b3b66afba63b3e6506dd86ac8cd6ccb3d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MysqlServerIdentity]:
        return typing.cast(typing.Optional[MysqlServerIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MysqlServerIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182a5cfca00f73f7f2398de039c8f3737ecf60d2b19b454fc8bdef849bb40a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mysqlServer.MysqlServerThreatDetectionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "disabled_alerts": "disabledAlerts",
        "email_account_admins": "emailAccountAdmins",
        "email_addresses": "emailAddresses",
        "enabled": "enabled",
        "retention_days": "retentionDays",
        "storage_account_access_key": "storageAccountAccessKey",
        "storage_endpoint": "storageEndpoint",
    },
)
class MysqlServerThreatDetectionPolicy:
    def __init__(
        self,
        *,
        disabled_alerts: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_account_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disabled_alerts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#disabled_alerts MysqlServer#disabled_alerts}.
        :param email_account_admins: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#email_account_admins MysqlServer#email_account_admins}.
        :param email_addresses: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#email_addresses MysqlServer#email_addresses}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#enabled MysqlServer#enabled}.
        :param retention_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#retention_days MysqlServer#retention_days}.
        :param storage_account_access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#storage_account_access_key MysqlServer#storage_account_access_key}.
        :param storage_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#storage_endpoint MysqlServer#storage_endpoint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a27f37a54a1e3a927f011c001a3000cacdbd3dc9b5b09a451c95e345b9e9a92)
            check_type(argname="argument disabled_alerts", value=disabled_alerts, expected_type=type_hints["disabled_alerts"])
            check_type(argname="argument email_account_admins", value=email_account_admins, expected_type=type_hints["email_account_admins"])
            check_type(argname="argument email_addresses", value=email_addresses, expected_type=type_hints["email_addresses"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
            check_type(argname="argument storage_account_access_key", value=storage_account_access_key, expected_type=type_hints["storage_account_access_key"])
            check_type(argname="argument storage_endpoint", value=storage_endpoint, expected_type=type_hints["storage_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled_alerts is not None:
            self._values["disabled_alerts"] = disabled_alerts
        if email_account_admins is not None:
            self._values["email_account_admins"] = email_account_admins
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses
        if enabled is not None:
            self._values["enabled"] = enabled
        if retention_days is not None:
            self._values["retention_days"] = retention_days
        if storage_account_access_key is not None:
            self._values["storage_account_access_key"] = storage_account_access_key
        if storage_endpoint is not None:
            self._values["storage_endpoint"] = storage_endpoint

    @builtins.property
    def disabled_alerts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#disabled_alerts MysqlServer#disabled_alerts}.'''
        result = self._values.get("disabled_alerts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_account_admins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#email_account_admins MysqlServer#email_account_admins}.'''
        result = self._values.get("email_account_admins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#email_addresses MysqlServer#email_addresses}.'''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#enabled MysqlServer#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#retention_days MysqlServer#retention_days}.'''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_account_access_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#storage_account_access_key MysqlServer#storage_account_access_key}.'''
        result = self._values.get("storage_account_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#storage_endpoint MysqlServer#storage_endpoint}.'''
        result = self._values.get("storage_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MysqlServerThreatDetectionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MysqlServerThreatDetectionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mysqlServer.MysqlServerThreatDetectionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a06b7fac17f0ef79e3f5579a0325bb344000933c6df82bd55f1aa477f45af0fc)
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

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetRetentionDays")
    def reset_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDays", []))

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
    def email_account_admins_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "emailAccountAdminsInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddressesInput")
    def email_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDaysInput")
    def retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDaysInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4583bb6e7183cf0d1a6997e1cc47ce9d93dc477dee511bd1281bcc5bea178202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabledAlerts", value)

    @builtins.property
    @jsii.member(jsii_name="emailAccountAdmins")
    def email_account_admins(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "emailAccountAdmins"))

    @email_account_admins.setter
    def email_account_admins(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5afd68515e7818b98de855e1390d4bc90774b85257bf762941eb2b507158e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAccountAdmins", value)

    @builtins.property
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @email_addresses.setter
    def email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b605b410e8184e0abeab94c86bda9bab55c21c080a0d7319172a80f45deaa48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddresses", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__525195b2277333af59143a4ae3acdc32d7d830572b67280f0a300f83cbe2ab3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDays"))

    @retention_days.setter
    def retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc213c2ea0547edb19de3bfcf2170677380b3bf4f048ac54664e5dbdfa35268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDays", value)

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKey")
    def storage_account_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountAccessKey"))

    @storage_account_access_key.setter
    def storage_account_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b46cf9701537db53d44cf0135ed66bba3025bb6d9fd5596eb4d1b35b0fe1679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountAccessKey", value)

    @builtins.property
    @jsii.member(jsii_name="storageEndpoint")
    def storage_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageEndpoint"))

    @storage_endpoint.setter
    def storage_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdb1b31e18578b90956e23dfe4824874dd7cd50096b347c715ec61a18251202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MysqlServerThreatDetectionPolicy]:
        return typing.cast(typing.Optional[MysqlServerThreatDetectionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MysqlServerThreatDetectionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45961fabfd6651bf9ed794baf5eea3911677d6daaf466fcd02a3da85b7f95f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mysqlServer.MysqlServerTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MysqlServerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#create MysqlServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#delete MysqlServer#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#read MysqlServer#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#update MysqlServer#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bae36647cdb4e95f4eacdfc80edaa2c92f6687180eb49c59978d5169e8c1484)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#create MysqlServer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#delete MysqlServer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#read MysqlServer#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_server#update MysqlServer#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MysqlServerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MysqlServerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mysqlServer.MysqlServerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4af862609523b1bbc1a18afa4c04b2a204cf9927ce5a87b0afcdec0261a77c13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eda76553a9dca03318e462083e985f74caf0ab26a0304deeb091f57b77ca05cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b8b56500004cbdb4b3d9817b0f5f34fe55666a854a8a319a4b3e611aefcc0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4708d18aa9637bdeed00cee1e7912a8767128d7ff105a2c9e710ae9dfbbaee71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d48482299a56b3b8bf886618fb7be85e0eea8dd1a0dca4371285b81e67592dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MysqlServerTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MysqlServerTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MysqlServerTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e5a65b0cc0d934fd8fbf07e6bedfc4fc8fbb6ce04bd0e239c0adb2651fcabf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MysqlServer",
    "MysqlServerConfig",
    "MysqlServerIdentity",
    "MysqlServerIdentityOutputReference",
    "MysqlServerThreatDetectionPolicy",
    "MysqlServerThreatDetectionPolicyOutputReference",
    "MysqlServerTimeouts",
    "MysqlServerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__628dd63da6aa03011cd6b6cce28294dfe9902e3e24f33f91b6dbd466239de012(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku_name: builtins.str,
    ssl_enforcement_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    version: builtins.str,
    administrator_login: typing.Optional[builtins.str] = None,
    administrator_login_password: typing.Optional[builtins.str] = None,
    auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backup_retention_days: typing.Optional[jsii.Number] = None,
    create_mode: typing.Optional[builtins.str] = None,
    creation_source_server_id: typing.Optional[builtins.str] = None,
    geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[MysqlServerIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restore_point_in_time: typing.Optional[builtins.str] = None,
    ssl_minimal_tls_version_enforced: typing.Optional[builtins.str] = None,
    storage_mb: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    threat_detection_policy: typing.Optional[typing.Union[MysqlServerThreatDetectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MysqlServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__062b2a5b52710076e46095051e9fd4f055efb700a766b2c93c638b0b89567306(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d24a1ed03655a63569e51252bdc270593f64198c7ec688bf59093f165d3710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ee89c4e4d382fc78e3575e5f0ce0f089e38b3404212eb268604126fbccc01a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ae265d45df0df404bf145e2b5179c10834430ce0a2d981dc1f81e39b5f0845(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8231a286ca1bbe6a19cc132e93f9bb6946018f7ced11a6d6d3e3577623d5f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b79c7c9c5d6e47dad75e4e4e34937085f787542a26d08cc267effec85fa7db3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f52f1da10c2015b0e73a8cca090965eca76121ba297d1edfb19600dbd32889e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1e7a902af91f3f2598571c31113a23878ed8d013d25a485f5f892a95b49beb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f069c7847502cd9e17ab006ef2327a99a28a711381a6fde3840ca2b5839079(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2c461b19c0eb5432a9e0b04cad29e10f6a0797564165f8f9d04ef51cb556b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786e737e1b951faa5370a3192dba617f49a0f5fe27bd3e21733218c158fa3140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4449adaa536f67a2110da5300195f23a1cd41f96c65490a70016f65d35877afe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d262b81ca025718130c96b3426d0763fcf9ad3952f63e5d9627277c3527403(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29323bb5e5c5f66b52dfa258ea6fffa7e4873a68df1b8eab7da5d6e746140650(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3dfe7bea72becf31d40f561250780bfc111b4d3cf49562a986e09e101d5c176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6167848e90b9c809ef3582f2b980a6347a63c973187ba880fae8c8cff7c70c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625ff7da97aa623a0a3ab6e8321c8158da6fcfef5716da56c915e578968a6a5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34dba863205d26bf2fa80eee81dab0f7ca455985eb64ff25a79538b9d0c002a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fad3aef2746cb6261ecdebb1c7a4dad4f5467235d17c705a4c3481430bdeef(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e4db10b21f225f3f787f513f42d7d1e5d3d1bb6bd583bea64879c840d39d88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb875ae2c12c59346fad2a9f7c5267b419a10b982907cf46a8856082dae399c3(
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
    sku_name: builtins.str,
    ssl_enforcement_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    version: builtins.str,
    administrator_login: typing.Optional[builtins.str] = None,
    administrator_login_password: typing.Optional[builtins.str] = None,
    auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backup_retention_days: typing.Optional[jsii.Number] = None,
    create_mode: typing.Optional[builtins.str] = None,
    creation_source_server_id: typing.Optional[builtins.str] = None,
    geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[MysqlServerIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restore_point_in_time: typing.Optional[builtins.str] = None,
    ssl_minimal_tls_version_enforced: typing.Optional[builtins.str] = None,
    storage_mb: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    threat_detection_policy: typing.Optional[typing.Union[MysqlServerThreatDetectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MysqlServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf241d45944ebd8ad9a8318bf7a4776bfa4e98583bc017a09bf06187c415f4f(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8151e18a58961248c26f891421562cc44c695e3a79a3344f9fd5a2b2dce4c07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4517dad8bcc2aea3a7bf8ea2dba57b3b66afba63b3e6506dd86ac8cd6ccb3d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182a5cfca00f73f7f2398de039c8f3737ecf60d2b19b454fc8bdef849bb40a1a(
    value: typing.Optional[MysqlServerIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a27f37a54a1e3a927f011c001a3000cacdbd3dc9b5b09a451c95e345b9e9a92(
    *,
    disabled_alerts: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_account_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_days: typing.Optional[jsii.Number] = None,
    storage_account_access_key: typing.Optional[builtins.str] = None,
    storage_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06b7fac17f0ef79e3f5579a0325bb344000933c6df82bd55f1aa477f45af0fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4583bb6e7183cf0d1a6997e1cc47ce9d93dc477dee511bd1281bcc5bea178202(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5afd68515e7818b98de855e1390d4bc90774b85257bf762941eb2b507158e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b605b410e8184e0abeab94c86bda9bab55c21c080a0d7319172a80f45deaa48(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525195b2277333af59143a4ae3acdc32d7d830572b67280f0a300f83cbe2ab3c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc213c2ea0547edb19de3bfcf2170677380b3bf4f048ac54664e5dbdfa35268(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b46cf9701537db53d44cf0135ed66bba3025bb6d9fd5596eb4d1b35b0fe1679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdb1b31e18578b90956e23dfe4824874dd7cd50096b347c715ec61a18251202(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45961fabfd6651bf9ed794baf5eea3911677d6daaf466fcd02a3da85b7f95f3a(
    value: typing.Optional[MysqlServerThreatDetectionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bae36647cdb4e95f4eacdfc80edaa2c92f6687180eb49c59978d5169e8c1484(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af862609523b1bbc1a18afa4c04b2a204cf9927ce5a87b0afcdec0261a77c13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda76553a9dca03318e462083e985f74caf0ab26a0304deeb091f57b77ca05cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b8b56500004cbdb4b3d9817b0f5f34fe55666a854a8a319a4b3e611aefcc0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4708d18aa9637bdeed00cee1e7912a8767128d7ff105a2c9e710ae9dfbbaee71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48482299a56b3b8bf886618fb7be85e0eea8dd1a0dca4371285b81e67592dfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e5a65b0cc0d934fd8fbf07e6bedfc4fc8fbb6ce04bd0e239c0adb2651fcabf(
    value: typing.Optional[typing.Union[MysqlServerTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
