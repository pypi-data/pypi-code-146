'''
# `data_aws_rds_orderable_db_instance`

Refer to the Terraform Registory for docs: [`data_aws_rds_orderable_db_instance`](https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance).
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


class DataAwsRdsOrderableDbInstance(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsRdsOrderableDbInstance.DataAwsRdsOrderableDbInstance",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance aws_rds_orderable_db_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        engine: builtins.str,
        availability_zone_group: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_class: typing.Optional[builtins.str] = None,
        license_model: typing.Optional[builtins.str] = None,
        preferred_engine_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_instance_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        supports_enhanced_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_global_databases: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_iam_database_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_iops: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_kerberos_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_performance_insights: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_storage_autoscaling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_storage_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vpc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance aws_rds_orderable_db_instance} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param engine: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#engine DataAwsRdsOrderableDbInstance#engine}.
        :param availability_zone_group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#availability_zone_group DataAwsRdsOrderableDbInstance#availability_zone_group}.
        :param engine_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#engine_version DataAwsRdsOrderableDbInstance#engine_version}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#id DataAwsRdsOrderableDbInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_class: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#instance_class DataAwsRdsOrderableDbInstance#instance_class}.
        :param license_model: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#license_model DataAwsRdsOrderableDbInstance#license_model}.
        :param preferred_engine_versions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#preferred_engine_versions DataAwsRdsOrderableDbInstance#preferred_engine_versions}.
        :param preferred_instance_classes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#preferred_instance_classes DataAwsRdsOrderableDbInstance#preferred_instance_classes}.
        :param storage_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#storage_type DataAwsRdsOrderableDbInstance#storage_type}.
        :param supports_enhanced_monitoring: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_enhanced_monitoring DataAwsRdsOrderableDbInstance#supports_enhanced_monitoring}.
        :param supports_global_databases: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_global_databases DataAwsRdsOrderableDbInstance#supports_global_databases}.
        :param supports_iam_database_authentication: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_iam_database_authentication DataAwsRdsOrderableDbInstance#supports_iam_database_authentication}.
        :param supports_iops: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_iops DataAwsRdsOrderableDbInstance#supports_iops}.
        :param supports_kerberos_authentication: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_kerberos_authentication DataAwsRdsOrderableDbInstance#supports_kerberos_authentication}.
        :param supports_performance_insights: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_performance_insights DataAwsRdsOrderableDbInstance#supports_performance_insights}.
        :param supports_storage_autoscaling: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_storage_autoscaling DataAwsRdsOrderableDbInstance#supports_storage_autoscaling}.
        :param supports_storage_encryption: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_storage_encryption DataAwsRdsOrderableDbInstance#supports_storage_encryption}.
        :param vpc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#vpc DataAwsRdsOrderableDbInstance#vpc}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c4623ba3f443494243a54e605e7b8fa87c1bf03e3864039c9d62e59512c70e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataAwsRdsOrderableDbInstanceConfig(
            engine=engine,
            availability_zone_group=availability_zone_group,
            engine_version=engine_version,
            id=id,
            instance_class=instance_class,
            license_model=license_model,
            preferred_engine_versions=preferred_engine_versions,
            preferred_instance_classes=preferred_instance_classes,
            storage_type=storage_type,
            supports_enhanced_monitoring=supports_enhanced_monitoring,
            supports_global_databases=supports_global_databases,
            supports_iam_database_authentication=supports_iam_database_authentication,
            supports_iops=supports_iops,
            supports_kerberos_authentication=supports_kerberos_authentication,
            supports_performance_insights=supports_performance_insights,
            supports_storage_autoscaling=supports_storage_autoscaling,
            supports_storage_encryption=supports_storage_encryption,
            vpc=vpc,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAvailabilityZoneGroup")
    def reset_availability_zone_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZoneGroup", []))

    @jsii.member(jsii_name="resetEngineVersion")
    def reset_engine_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEngineVersion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceClass")
    def reset_instance_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceClass", []))

    @jsii.member(jsii_name="resetLicenseModel")
    def reset_license_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseModel", []))

    @jsii.member(jsii_name="resetPreferredEngineVersions")
    def reset_preferred_engine_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredEngineVersions", []))

    @jsii.member(jsii_name="resetPreferredInstanceClasses")
    def reset_preferred_instance_classes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredInstanceClasses", []))

    @jsii.member(jsii_name="resetStorageType")
    def reset_storage_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageType", []))

    @jsii.member(jsii_name="resetSupportsEnhancedMonitoring")
    def reset_supports_enhanced_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportsEnhancedMonitoring", []))

    @jsii.member(jsii_name="resetSupportsGlobalDatabases")
    def reset_supports_global_databases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportsGlobalDatabases", []))

    @jsii.member(jsii_name="resetSupportsIamDatabaseAuthentication")
    def reset_supports_iam_database_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportsIamDatabaseAuthentication", []))

    @jsii.member(jsii_name="resetSupportsIops")
    def reset_supports_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportsIops", []))

    @jsii.member(jsii_name="resetSupportsKerberosAuthentication")
    def reset_supports_kerberos_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportsKerberosAuthentication", []))

    @jsii.member(jsii_name="resetSupportsPerformanceInsights")
    def reset_supports_performance_insights(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportsPerformanceInsights", []))

    @jsii.member(jsii_name="resetSupportsStorageAutoscaling")
    def reset_supports_storage_autoscaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportsStorageAutoscaling", []))

    @jsii.member(jsii_name="resetSupportsStorageEncryption")
    def reset_supports_storage_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportsStorageEncryption", []))

    @jsii.member(jsii_name="resetVpc")
    def reset_vpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpc", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @builtins.property
    @jsii.member(jsii_name="maxIopsPerDbInstance")
    def max_iops_per_db_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIopsPerDbInstance"))

    @builtins.property
    @jsii.member(jsii_name="maxIopsPerGib")
    def max_iops_per_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIopsPerGib"))

    @builtins.property
    @jsii.member(jsii_name="maxStorageSize")
    def max_storage_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxStorageSize"))

    @builtins.property
    @jsii.member(jsii_name="minIopsPerDbInstance")
    def min_iops_per_db_instance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minIopsPerDbInstance"))

    @builtins.property
    @jsii.member(jsii_name="minIopsPerGib")
    def min_iops_per_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minIopsPerGib"))

    @builtins.property
    @jsii.member(jsii_name="minStorageSize")
    def min_storage_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minStorageSize"))

    @builtins.property
    @jsii.member(jsii_name="multiAzCapable")
    def multi_az_capable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "multiAzCapable"))

    @builtins.property
    @jsii.member(jsii_name="outpostCapable")
    def outpost_capable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "outpostCapable"))

    @builtins.property
    @jsii.member(jsii_name="readReplicaCapable")
    def read_replica_capable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "readReplicaCapable"))

    @builtins.property
    @jsii.member(jsii_name="supportedEngineModes")
    def supported_engine_modes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedEngineModes"))

    @builtins.property
    @jsii.member(jsii_name="supportedNetworkTypes")
    def supported_network_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedNetworkTypes"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneGroupInput")
    def availability_zone_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="engineInput")
    def engine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineInput"))

    @builtins.property
    @jsii.member(jsii_name="engineVersionInput")
    def engine_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceClassInput")
    def instance_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceClassInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseModelInput")
    def license_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseModelInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredEngineVersionsInput")
    def preferred_engine_versions_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "preferredEngineVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredInstanceClassesInput")
    def preferred_instance_classes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "preferredInstanceClassesInput"))

    @builtins.property
    @jsii.member(jsii_name="storageTypeInput")
    def storage_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="supportsEnhancedMonitoringInput")
    def supports_enhanced_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportsEnhancedMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="supportsGlobalDatabasesInput")
    def supports_global_databases_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportsGlobalDatabasesInput"))

    @builtins.property
    @jsii.member(jsii_name="supportsIamDatabaseAuthenticationInput")
    def supports_iam_database_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportsIamDatabaseAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="supportsIopsInput")
    def supports_iops_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportsIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="supportsKerberosAuthenticationInput")
    def supports_kerberos_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportsKerberosAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="supportsPerformanceInsightsInput")
    def supports_performance_insights_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportsPerformanceInsightsInput"))

    @builtins.property
    @jsii.member(jsii_name="supportsStorageAutoscalingInput")
    def supports_storage_autoscaling_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportsStorageAutoscalingInput"))

    @builtins.property
    @jsii.member(jsii_name="supportsStorageEncryptionInput")
    def supports_storage_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportsStorageEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneGroup")
    def availability_zone_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZoneGroup"))

    @availability_zone_group.setter
    def availability_zone_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f11d01c154a0b21abb3a3b612a1984f0daa5b0b58adca93921d960028c44dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZoneGroup", value)

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec091db38b40043cb52b14e4af2d086290a58a790b2feea19105af083ae03aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9c8dccbb208680a78af6f9fffe89c75b38684b00cb8a970fe6d627998ef720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d67520f7c00e6f08ead1dd5f8e73e4b7842646694ecb6469dedc4fadaf02718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="instanceClass")
    def instance_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceClass"))

    @instance_class.setter
    def instance_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4545d2613fd2a8b70148722f3185e06ef52492ce42121da105fc51930392ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceClass", value)

    @builtins.property
    @jsii.member(jsii_name="licenseModel")
    def license_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseModel"))

    @license_model.setter
    def license_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f847fa8b56be8ea0a4e3ed5a20075cdf27c469410617acb3ec317c4da0485279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseModel", value)

    @builtins.property
    @jsii.member(jsii_name="preferredEngineVersions")
    def preferred_engine_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "preferredEngineVersions"))

    @preferred_engine_versions.setter
    def preferred_engine_versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc9946d6c75df3e20d4046c5b5557e26e2557e3398707c25778e583274ff7b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredEngineVersions", value)

    @builtins.property
    @jsii.member(jsii_name="preferredInstanceClasses")
    def preferred_instance_classes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "preferredInstanceClasses"))

    @preferred_instance_classes.setter
    def preferred_instance_classes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509c304f2aa0944e3615afde766b288d3cad0e2106caa26fd396fd3c0483ea1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredInstanceClasses", value)

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageType"))

    @storage_type.setter
    def storage_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c235a1aecad722d97ba92006d0e8b5b4ced00ca1c1773e9de554d22ae7a872b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageType", value)

    @builtins.property
    @jsii.member(jsii_name="supportsEnhancedMonitoring")
    def supports_enhanced_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportsEnhancedMonitoring"))

    @supports_enhanced_monitoring.setter
    def supports_enhanced_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01c6012e0b0abd56c886094a81e82827639f32cd3fdd06048d2222e9237a93d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportsEnhancedMonitoring", value)

    @builtins.property
    @jsii.member(jsii_name="supportsGlobalDatabases")
    def supports_global_databases(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportsGlobalDatabases"))

    @supports_global_databases.setter
    def supports_global_databases(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6bef463bb56ff65b0887c9a47dd263fda40b349b552893ca5f3edf1a2df13d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportsGlobalDatabases", value)

    @builtins.property
    @jsii.member(jsii_name="supportsIamDatabaseAuthentication")
    def supports_iam_database_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportsIamDatabaseAuthentication"))

    @supports_iam_database_authentication.setter
    def supports_iam_database_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f980bac7212093646f0198780ccc270b9780b77712501e812ec27b6f22508cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportsIamDatabaseAuthentication", value)

    @builtins.property
    @jsii.member(jsii_name="supportsIops")
    def supports_iops(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportsIops"))

    @supports_iops.setter
    def supports_iops(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ac9ad0103cfb611508babea90f80233e9d4039555ec08f7d14be6c03f326c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportsIops", value)

    @builtins.property
    @jsii.member(jsii_name="supportsKerberosAuthentication")
    def supports_kerberos_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportsKerberosAuthentication"))

    @supports_kerberos_authentication.setter
    def supports_kerberos_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a875b3d9f13ba6917ce1edd1090cd15fa1b7856cfcc6dbf7b7bb2eba4ca40b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportsKerberosAuthentication", value)

    @builtins.property
    @jsii.member(jsii_name="supportsPerformanceInsights")
    def supports_performance_insights(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportsPerformanceInsights"))

    @supports_performance_insights.setter
    def supports_performance_insights(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595365d5d6e7d5b899ba6f50c3f6dbde4f0cabb678b3f0f2fef3b98113b7ea84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportsPerformanceInsights", value)

    @builtins.property
    @jsii.member(jsii_name="supportsStorageAutoscaling")
    def supports_storage_autoscaling(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportsStorageAutoscaling"))

    @supports_storage_autoscaling.setter
    def supports_storage_autoscaling(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e912de7f508c75ff5a119a05cc296379467006b95aab1c3a48bb92e5c8e5f4cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportsStorageAutoscaling", value)

    @builtins.property
    @jsii.member(jsii_name="supportsStorageEncryption")
    def supports_storage_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportsStorageEncryption"))

    @supports_storage_encryption.setter
    def supports_storage_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b3a2e911a4aded362e786fece3e4f458d9c250f15b92cd1d6410b1e47d1047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportsStorageEncryption", value)

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec17d063e3670785e239b90ce7558352b8518a65d3f36f00e50e46e6e5d990a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsRdsOrderableDbInstance.DataAwsRdsOrderableDbInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "engine": "engine",
        "availability_zone_group": "availabilityZoneGroup",
        "engine_version": "engineVersion",
        "id": "id",
        "instance_class": "instanceClass",
        "license_model": "licenseModel",
        "preferred_engine_versions": "preferredEngineVersions",
        "preferred_instance_classes": "preferredInstanceClasses",
        "storage_type": "storageType",
        "supports_enhanced_monitoring": "supportsEnhancedMonitoring",
        "supports_global_databases": "supportsGlobalDatabases",
        "supports_iam_database_authentication": "supportsIamDatabaseAuthentication",
        "supports_iops": "supportsIops",
        "supports_kerberos_authentication": "supportsKerberosAuthentication",
        "supports_performance_insights": "supportsPerformanceInsights",
        "supports_storage_autoscaling": "supportsStorageAutoscaling",
        "supports_storage_encryption": "supportsStorageEncryption",
        "vpc": "vpc",
    },
)
class DataAwsRdsOrderableDbInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        engine: builtins.str,
        availability_zone_group: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_class: typing.Optional[builtins.str] = None,
        license_model: typing.Optional[builtins.str] = None,
        preferred_engine_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_instance_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        supports_enhanced_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_global_databases: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_iam_database_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_iops: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_kerberos_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_performance_insights: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_storage_autoscaling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        supports_storage_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vpc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param engine: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#engine DataAwsRdsOrderableDbInstance#engine}.
        :param availability_zone_group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#availability_zone_group DataAwsRdsOrderableDbInstance#availability_zone_group}.
        :param engine_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#engine_version DataAwsRdsOrderableDbInstance#engine_version}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#id DataAwsRdsOrderableDbInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_class: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#instance_class DataAwsRdsOrderableDbInstance#instance_class}.
        :param license_model: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#license_model DataAwsRdsOrderableDbInstance#license_model}.
        :param preferred_engine_versions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#preferred_engine_versions DataAwsRdsOrderableDbInstance#preferred_engine_versions}.
        :param preferred_instance_classes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#preferred_instance_classes DataAwsRdsOrderableDbInstance#preferred_instance_classes}.
        :param storage_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#storage_type DataAwsRdsOrderableDbInstance#storage_type}.
        :param supports_enhanced_monitoring: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_enhanced_monitoring DataAwsRdsOrderableDbInstance#supports_enhanced_monitoring}.
        :param supports_global_databases: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_global_databases DataAwsRdsOrderableDbInstance#supports_global_databases}.
        :param supports_iam_database_authentication: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_iam_database_authentication DataAwsRdsOrderableDbInstance#supports_iam_database_authentication}.
        :param supports_iops: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_iops DataAwsRdsOrderableDbInstance#supports_iops}.
        :param supports_kerberos_authentication: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_kerberos_authentication DataAwsRdsOrderableDbInstance#supports_kerberos_authentication}.
        :param supports_performance_insights: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_performance_insights DataAwsRdsOrderableDbInstance#supports_performance_insights}.
        :param supports_storage_autoscaling: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_storage_autoscaling DataAwsRdsOrderableDbInstance#supports_storage_autoscaling}.
        :param supports_storage_encryption: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_storage_encryption DataAwsRdsOrderableDbInstance#supports_storage_encryption}.
        :param vpc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#vpc DataAwsRdsOrderableDbInstance#vpc}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143a9c31cbfeea0112249cb6624fb5d77c38bbf21c1fbad2b063a1c949806fb5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument availability_zone_group", value=availability_zone_group, expected_type=type_hints["availability_zone_group"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_class", value=instance_class, expected_type=type_hints["instance_class"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument preferred_engine_versions", value=preferred_engine_versions, expected_type=type_hints["preferred_engine_versions"])
            check_type(argname="argument preferred_instance_classes", value=preferred_instance_classes, expected_type=type_hints["preferred_instance_classes"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument supports_enhanced_monitoring", value=supports_enhanced_monitoring, expected_type=type_hints["supports_enhanced_monitoring"])
            check_type(argname="argument supports_global_databases", value=supports_global_databases, expected_type=type_hints["supports_global_databases"])
            check_type(argname="argument supports_iam_database_authentication", value=supports_iam_database_authentication, expected_type=type_hints["supports_iam_database_authentication"])
            check_type(argname="argument supports_iops", value=supports_iops, expected_type=type_hints["supports_iops"])
            check_type(argname="argument supports_kerberos_authentication", value=supports_kerberos_authentication, expected_type=type_hints["supports_kerberos_authentication"])
            check_type(argname="argument supports_performance_insights", value=supports_performance_insights, expected_type=type_hints["supports_performance_insights"])
            check_type(argname="argument supports_storage_autoscaling", value=supports_storage_autoscaling, expected_type=type_hints["supports_storage_autoscaling"])
            check_type(argname="argument supports_storage_encryption", value=supports_storage_encryption, expected_type=type_hints["supports_storage_encryption"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine": engine,
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
        if availability_zone_group is not None:
            self._values["availability_zone_group"] = availability_zone_group
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if id is not None:
            self._values["id"] = id
        if instance_class is not None:
            self._values["instance_class"] = instance_class
        if license_model is not None:
            self._values["license_model"] = license_model
        if preferred_engine_versions is not None:
            self._values["preferred_engine_versions"] = preferred_engine_versions
        if preferred_instance_classes is not None:
            self._values["preferred_instance_classes"] = preferred_instance_classes
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if supports_enhanced_monitoring is not None:
            self._values["supports_enhanced_monitoring"] = supports_enhanced_monitoring
        if supports_global_databases is not None:
            self._values["supports_global_databases"] = supports_global_databases
        if supports_iam_database_authentication is not None:
            self._values["supports_iam_database_authentication"] = supports_iam_database_authentication
        if supports_iops is not None:
            self._values["supports_iops"] = supports_iops
        if supports_kerberos_authentication is not None:
            self._values["supports_kerberos_authentication"] = supports_kerberos_authentication
        if supports_performance_insights is not None:
            self._values["supports_performance_insights"] = supports_performance_insights
        if supports_storage_autoscaling is not None:
            self._values["supports_storage_autoscaling"] = supports_storage_autoscaling
        if supports_storage_encryption is not None:
            self._values["supports_storage_encryption"] = supports_storage_encryption
        if vpc is not None:
            self._values["vpc"] = vpc

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
    def engine(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#engine DataAwsRdsOrderableDbInstance#engine}.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def availability_zone_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#availability_zone_group DataAwsRdsOrderableDbInstance#availability_zone_group}.'''
        result = self._values.get("availability_zone_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#engine_version DataAwsRdsOrderableDbInstance#engine_version}.'''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#id DataAwsRdsOrderableDbInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_class(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#instance_class DataAwsRdsOrderableDbInstance#instance_class}.'''
        result = self._values.get("instance_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_model(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#license_model DataAwsRdsOrderableDbInstance#license_model}.'''
        result = self._values.get("license_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_engine_versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#preferred_engine_versions DataAwsRdsOrderableDbInstance#preferred_engine_versions}.'''
        result = self._values.get("preferred_engine_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preferred_instance_classes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#preferred_instance_classes DataAwsRdsOrderableDbInstance#preferred_instance_classes}.'''
        result = self._values.get("preferred_instance_classes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#storage_type DataAwsRdsOrderableDbInstance#storage_type}.'''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def supports_enhanced_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_enhanced_monitoring DataAwsRdsOrderableDbInstance#supports_enhanced_monitoring}.'''
        result = self._values.get("supports_enhanced_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def supports_global_databases(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_global_databases DataAwsRdsOrderableDbInstance#supports_global_databases}.'''
        result = self._values.get("supports_global_databases")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def supports_iam_database_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_iam_database_authentication DataAwsRdsOrderableDbInstance#supports_iam_database_authentication}.'''
        result = self._values.get("supports_iam_database_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def supports_iops(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_iops DataAwsRdsOrderableDbInstance#supports_iops}.'''
        result = self._values.get("supports_iops")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def supports_kerberos_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_kerberos_authentication DataAwsRdsOrderableDbInstance#supports_kerberos_authentication}.'''
        result = self._values.get("supports_kerberos_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def supports_performance_insights(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_performance_insights DataAwsRdsOrderableDbInstance#supports_performance_insights}.'''
        result = self._values.get("supports_performance_insights")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def supports_storage_autoscaling(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_storage_autoscaling DataAwsRdsOrderableDbInstance#supports_storage_autoscaling}.'''
        result = self._values.get("supports_storage_autoscaling")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def supports_storage_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#supports_storage_encryption DataAwsRdsOrderableDbInstance#supports_storage_encryption}.'''
        result = self._values.get("supports_storage_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vpc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/rds_orderable_db_instance#vpc DataAwsRdsOrderableDbInstance#vpc}.'''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsRdsOrderableDbInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataAwsRdsOrderableDbInstance",
    "DataAwsRdsOrderableDbInstanceConfig",
]

publication.publish()

def _typecheckingstub__17c4623ba3f443494243a54e605e7b8fa87c1bf03e3864039c9d62e59512c70e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    engine: builtins.str,
    availability_zone_group: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_class: typing.Optional[builtins.str] = None,
    license_model: typing.Optional[builtins.str] = None,
    preferred_engine_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_instance_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_type: typing.Optional[builtins.str] = None,
    supports_enhanced_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_global_databases: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_iam_database_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_iops: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_kerberos_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_performance_insights: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_storage_autoscaling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_storage_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vpc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__73f11d01c154a0b21abb3a3b612a1984f0daa5b0b58adca93921d960028c44dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec091db38b40043cb52b14e4af2d086290a58a790b2feea19105af083ae03aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9c8dccbb208680a78af6f9fffe89c75b38684b00cb8a970fe6d627998ef720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d67520f7c00e6f08ead1dd5f8e73e4b7842646694ecb6469dedc4fadaf02718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4545d2613fd2a8b70148722f3185e06ef52492ce42121da105fc51930392ade(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f847fa8b56be8ea0a4e3ed5a20075cdf27c469410617acb3ec317c4da0485279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc9946d6c75df3e20d4046c5b5557e26e2557e3398707c25778e583274ff7b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509c304f2aa0944e3615afde766b288d3cad0e2106caa26fd396fd3c0483ea1a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c235a1aecad722d97ba92006d0e8b5b4ced00ca1c1773e9de554d22ae7a872b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01c6012e0b0abd56c886094a81e82827639f32cd3fdd06048d2222e9237a93d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6bef463bb56ff65b0887c9a47dd263fda40b349b552893ca5f3edf1a2df13d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f980bac7212093646f0198780ccc270b9780b77712501e812ec27b6f22508cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ac9ad0103cfb611508babea90f80233e9d4039555ec08f7d14be6c03f326c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a875b3d9f13ba6917ce1edd1090cd15fa1b7856cfcc6dbf7b7bb2eba4ca40b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595365d5d6e7d5b899ba6f50c3f6dbde4f0cabb678b3f0f2fef3b98113b7ea84(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e912de7f508c75ff5a119a05cc296379467006b95aab1c3a48bb92e5c8e5f4cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b3a2e911a4aded362e786fece3e4f458d9c250f15b92cd1d6410b1e47d1047(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec17d063e3670785e239b90ce7558352b8518a65d3f36f00e50e46e6e5d990a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143a9c31cbfeea0112249cb6624fb5d77c38bbf21c1fbad2b063a1c949806fb5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    engine: builtins.str,
    availability_zone_group: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_class: typing.Optional[builtins.str] = None,
    license_model: typing.Optional[builtins.str] = None,
    preferred_engine_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_instance_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_type: typing.Optional[builtins.str] = None,
    supports_enhanced_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_global_databases: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_iam_database_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_iops: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_kerberos_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_performance_insights: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_storage_autoscaling: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    supports_storage_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vpc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
