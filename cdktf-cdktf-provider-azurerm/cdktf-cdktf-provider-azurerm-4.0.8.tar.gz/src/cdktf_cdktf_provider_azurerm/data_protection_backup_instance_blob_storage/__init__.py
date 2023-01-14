'''
# `azurerm_data_protection_backup_instance_blob_storage`

Refer to the Terraform Registory for docs: [`azurerm_data_protection_backup_instance_blob_storage`](https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage).
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


class DataProtectionBackupInstanceBlobStorage(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupInstanceBlobStorage.DataProtectionBackupInstanceBlobStorage",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage azurerm_data_protection_backup_instance_blob_storage}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup_policy_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        storage_account_id: builtins.str,
        vault_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataProtectionBackupInstanceBlobStorageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage azurerm_data_protection_backup_instance_blob_storage} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup_policy_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#backup_policy_id DataProtectionBackupInstanceBlobStorage#backup_policy_id}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#location DataProtectionBackupInstanceBlobStorage#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#name DataProtectionBackupInstanceBlobStorage#name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#storage_account_id DataProtectionBackupInstanceBlobStorage#storage_account_id}.
        :param vault_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#vault_id DataProtectionBackupInstanceBlobStorage#vault_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#id DataProtectionBackupInstanceBlobStorage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#timeouts DataProtectionBackupInstanceBlobStorage#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5f0d354519fd4fedfa2c0bdf29427ba0d3f70b84aafeec3354c3093d83e0bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataProtectionBackupInstanceBlobStorageConfig(
            backup_policy_id=backup_policy_id,
            location=location,
            name=name,
            storage_account_id=storage_account_id,
            vault_id=vault_id,
            id=id,
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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#create DataProtectionBackupInstanceBlobStorage#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#delete DataProtectionBackupInstanceBlobStorage#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#read DataProtectionBackupInstanceBlobStorage#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#update DataProtectionBackupInstanceBlobStorage#update}.
        '''
        value = DataProtectionBackupInstanceBlobStorageTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "DataProtectionBackupInstanceBlobStorageTimeoutsOutputReference":
        return typing.cast("DataProtectionBackupInstanceBlobStorageTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backupPolicyIdInput")
    def backup_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DataProtectionBackupInstanceBlobStorageTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DataProtectionBackupInstanceBlobStorageTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultIdInput")
    def vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPolicyId")
    def backup_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupPolicyId"))

    @backup_policy_id.setter
    def backup_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb3a68380c492acfb77279e0ee0fbc860dfc8ebfe5becc146055152e0dbface)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a9b142e99e5fa33f8252909fc8cf4cb9eef84244c5fc5c257ec7e0457efd09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70042da963a2ffc5445e4919d8d05ad8e2c9a4ec9e34f8a61a382b364987c457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b58351f6f235e1cc2d6b8a6c01a7b827dceb3c3254ecbf95a049a29f432d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab44a751bd6af6252ff11083377f089ed2e9d1c9f919fb8153e258069727413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="vaultId")
    def vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultId"))

    @vault_id.setter
    def vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5338187665291a1eb9a5fa6af0bf3e8af205ed1cc8b36e1f53e3d6f04ce265cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupInstanceBlobStorage.DataProtectionBackupInstanceBlobStorageConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backup_policy_id": "backupPolicyId",
        "location": "location",
        "name": "name",
        "storage_account_id": "storageAccountId",
        "vault_id": "vaultId",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class DataProtectionBackupInstanceBlobStorageConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        backup_policy_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        storage_account_id: builtins.str,
        vault_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataProtectionBackupInstanceBlobStorageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backup_policy_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#backup_policy_id DataProtectionBackupInstanceBlobStorage#backup_policy_id}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#location DataProtectionBackupInstanceBlobStorage#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#name DataProtectionBackupInstanceBlobStorage#name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#storage_account_id DataProtectionBackupInstanceBlobStorage#storage_account_id}.
        :param vault_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#vault_id DataProtectionBackupInstanceBlobStorage#vault_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#id DataProtectionBackupInstanceBlobStorage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#timeouts DataProtectionBackupInstanceBlobStorage#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DataProtectionBackupInstanceBlobStorageTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78f7043e05d9ba4a4375a3af5ed13faeba0affe61fad88b2e5df47a2f3ba997)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backup_policy_id", value=backup_policy_id, expected_type=type_hints["backup_policy_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument vault_id", value=vault_id, expected_type=type_hints["vault_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_policy_id": backup_policy_id,
            "location": location,
            "name": name,
            "storage_account_id": storage_account_id,
            "vault_id": vault_id,
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
        if id is not None:
            self._values["id"] = id
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
    def backup_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#backup_policy_id DataProtectionBackupInstanceBlobStorage#backup_policy_id}.'''
        result = self._values.get("backup_policy_id")
        assert result is not None, "Required property 'backup_policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#location DataProtectionBackupInstanceBlobStorage#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#name DataProtectionBackupInstanceBlobStorage#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#storage_account_id DataProtectionBackupInstanceBlobStorage#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vault_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#vault_id DataProtectionBackupInstanceBlobStorage#vault_id}.'''
        result = self._values.get("vault_id")
        assert result is not None, "Required property 'vault_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#id DataProtectionBackupInstanceBlobStorage#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataProtectionBackupInstanceBlobStorageTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#timeouts DataProtectionBackupInstanceBlobStorage#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataProtectionBackupInstanceBlobStorageTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupInstanceBlobStorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupInstanceBlobStorage.DataProtectionBackupInstanceBlobStorageTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DataProtectionBackupInstanceBlobStorageTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#create DataProtectionBackupInstanceBlobStorage#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#delete DataProtectionBackupInstanceBlobStorage#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#read DataProtectionBackupInstanceBlobStorage#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#update DataProtectionBackupInstanceBlobStorage#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82afb0ef181d99d728163821dd817ab3b2168cb21a97e11a154993440ff4c7ab)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#create DataProtectionBackupInstanceBlobStorage#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#delete DataProtectionBackupInstanceBlobStorage#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#read DataProtectionBackupInstanceBlobStorage#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/data_protection_backup_instance_blob_storage#update DataProtectionBackupInstanceBlobStorage#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProtectionBackupInstanceBlobStorageTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProtectionBackupInstanceBlobStorageTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataProtectionBackupInstanceBlobStorage.DataProtectionBackupInstanceBlobStorageTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1362f6e7915b2a9b91787b9611bda6884133ceb7d40fc15bfb9fa8b0fd6824f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e67641ba82147b76d81b642667c6d903ab1c208bf1fd92f73c3cda7a2bdfea9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43dbdb0eac354422df39857e26ff7976625acd572a55e223521e4a1d881f0793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce6776f0870f9a3e086d1b9ad3003859e657972faa9f07c8f3052ec1c78a24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78c44eac81fa934c76120a24d56b988f7d964abe7f37072e33c1d0e8635b314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataProtectionBackupInstanceBlobStorageTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataProtectionBackupInstanceBlobStorageTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataProtectionBackupInstanceBlobStorageTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007f143c135992e5d53430453c6733c55de9f0b7f85886421fe3758b4959ec87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataProtectionBackupInstanceBlobStorage",
    "DataProtectionBackupInstanceBlobStorageConfig",
    "DataProtectionBackupInstanceBlobStorageTimeouts",
    "DataProtectionBackupInstanceBlobStorageTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bb5f0d354519fd4fedfa2c0bdf29427ba0d3f70b84aafeec3354c3093d83e0bd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup_policy_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    storage_account_id: builtins.str,
    vault_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataProtectionBackupInstanceBlobStorageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bcb3a68380c492acfb77279e0ee0fbc860dfc8ebfe5becc146055152e0dbface(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a9b142e99e5fa33f8252909fc8cf4cb9eef84244c5fc5c257ec7e0457efd09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70042da963a2ffc5445e4919d8d05ad8e2c9a4ec9e34f8a61a382b364987c457(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b58351f6f235e1cc2d6b8a6c01a7b827dceb3c3254ecbf95a049a29f432d3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab44a751bd6af6252ff11083377f089ed2e9d1c9f919fb8153e258069727413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5338187665291a1eb9a5fa6af0bf3e8af205ed1cc8b36e1f53e3d6f04ce265cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78f7043e05d9ba4a4375a3af5ed13faeba0affe61fad88b2e5df47a2f3ba997(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backup_policy_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    storage_account_id: builtins.str,
    vault_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataProtectionBackupInstanceBlobStorageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82afb0ef181d99d728163821dd817ab3b2168cb21a97e11a154993440ff4c7ab(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1362f6e7915b2a9b91787b9611bda6884133ceb7d40fc15bfb9fa8b0fd6824f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67641ba82147b76d81b642667c6d903ab1c208bf1fd92f73c3cda7a2bdfea9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43dbdb0eac354422df39857e26ff7976625acd572a55e223521e4a1d881f0793(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce6776f0870f9a3e086d1b9ad3003859e657972faa9f07c8f3052ec1c78a24c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78c44eac81fa934c76120a24d56b988f7d964abe7f37072e33c1d0e8635b314(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007f143c135992e5d53430453c6733c55de9f0b7f85886421fe3758b4959ec87(
    value: typing.Optional[typing.Union[DataProtectionBackupInstanceBlobStorageTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
