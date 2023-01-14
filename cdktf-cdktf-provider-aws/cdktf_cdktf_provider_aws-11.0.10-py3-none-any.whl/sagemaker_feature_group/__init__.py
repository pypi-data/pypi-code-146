'''
# `aws_sagemaker_feature_group`

Refer to the Terraform Registory for docs: [`aws_sagemaker_feature_group`](https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group).
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


class SagemakerFeatureGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroup",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group aws_sagemaker_feature_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        event_time_feature_name: builtins.str,
        feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerFeatureGroupFeatureDefinition", typing.Dict[builtins.str, typing.Any]]]],
        feature_group_name: builtins.str,
        record_identifier_feature_name: builtins.str,
        role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        offline_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        online_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group aws_sagemaker_feature_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param event_time_feature_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#event_time_feature_name SagemakerFeatureGroup#event_time_feature_name}.
        :param feature_definition: feature_definition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#feature_definition SagemakerFeatureGroup#feature_definition}
        :param feature_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#feature_group_name SagemakerFeatureGroup#feature_group_name}.
        :param record_identifier_feature_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#record_identifier_feature_name SagemakerFeatureGroup#record_identifier_feature_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#role_arn SagemakerFeatureGroup#role_arn}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#description SagemakerFeatureGroup#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#id SagemakerFeatureGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param offline_store_config: offline_store_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#offline_store_config SagemakerFeatureGroup#offline_store_config}
        :param online_store_config: online_store_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#online_store_config SagemakerFeatureGroup#online_store_config}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#tags SagemakerFeatureGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#tags_all SagemakerFeatureGroup#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c91ef1bb5461ff2a3c7186550b944001c7f829d03146414e1e2cf9493c4c31)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerFeatureGroupConfig(
            event_time_feature_name=event_time_feature_name,
            feature_definition=feature_definition,
            feature_group_name=feature_group_name,
            record_identifier_feature_name=record_identifier_feature_name,
            role_arn=role_arn,
            description=description,
            id=id,
            offline_store_config=offline_store_config,
            online_store_config=online_store_config,
            tags=tags,
            tags_all=tags_all,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putFeatureDefinition")
    def put_feature_definition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerFeatureGroupFeatureDefinition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2de7932f37b777e95eb6662069644c82c6c36b1c6c4106c7fecca1dd69d29d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFeatureDefinition", [value]))

    @jsii.member(jsii_name="putOfflineStoreConfig")
    def put_offline_store_config(
        self,
        *,
        s3_storage_config: typing.Union["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig", typing.Dict[builtins.str, typing.Any]],
        data_catalog_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_glue_table_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param s3_storage_config: s3_storage_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#s3_storage_config SagemakerFeatureGroup#s3_storage_config}
        :param data_catalog_config: data_catalog_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#data_catalog_config SagemakerFeatureGroup#data_catalog_config}
        :param disable_glue_table_creation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#disable_glue_table_creation SagemakerFeatureGroup#disable_glue_table_creation}.
        '''
        value = SagemakerFeatureGroupOfflineStoreConfig(
            s3_storage_config=s3_storage_config,
            data_catalog_config=data_catalog_config,
            disable_glue_table_creation=disable_glue_table_creation,
        )

        return typing.cast(None, jsii.invoke(self, "putOfflineStoreConfig", [value]))

    @jsii.member(jsii_name="putOnlineStoreConfig")
    def put_online_store_config(
        self,
        *,
        enable_online_store: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_online_store: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#enable_online_store SagemakerFeatureGroup#enable_online_store}.
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#security_config SagemakerFeatureGroup#security_config}
        '''
        value = SagemakerFeatureGroupOnlineStoreConfig(
            enable_online_store=enable_online_store, security_config=security_config
        )

        return typing.cast(None, jsii.invoke(self, "putOnlineStoreConfig", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOfflineStoreConfig")
    def reset_offline_store_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOfflineStoreConfig", []))

    @jsii.member(jsii_name="resetOnlineStoreConfig")
    def reset_online_store_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlineStoreConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="featureDefinition")
    def feature_definition(self) -> "SagemakerFeatureGroupFeatureDefinitionList":
        return typing.cast("SagemakerFeatureGroupFeatureDefinitionList", jsii.get(self, "featureDefinition"))

    @builtins.property
    @jsii.member(jsii_name="offlineStoreConfig")
    def offline_store_config(
        self,
    ) -> "SagemakerFeatureGroupOfflineStoreConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOfflineStoreConfigOutputReference", jsii.get(self, "offlineStoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="onlineStoreConfig")
    def online_store_config(
        self,
    ) -> "SagemakerFeatureGroupOnlineStoreConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOnlineStoreConfigOutputReference", jsii.get(self, "onlineStoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventTimeFeatureNameInput")
    def event_time_feature_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTimeFeatureNameInput"))

    @builtins.property
    @jsii.member(jsii_name="featureDefinitionInput")
    def feature_definition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]]], jsii.get(self, "featureDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="featureGroupNameInput")
    def feature_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="offlineStoreConfigInput")
    def offline_store_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"], jsii.get(self, "offlineStoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="onlineStoreConfigInput")
    def online_store_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"], jsii.get(self, "onlineStoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="recordIdentifierFeatureNameInput")
    def record_identifier_feature_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordIdentifierFeatureNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

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
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce93cdcfe3c93deb74350d340d2a5377eaec6f6a9c24694e9b549b5578cf6ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="eventTimeFeatureName")
    def event_time_feature_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventTimeFeatureName"))

    @event_time_feature_name.setter
    def event_time_feature_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ed91340de29fee123af2b2791b2399d18a233f5e3f0ddeb530343f756b63b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventTimeFeatureName", value)

    @builtins.property
    @jsii.member(jsii_name="featureGroupName")
    def feature_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureGroupName"))

    @feature_group_name.setter
    def feature_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4781ac5037a62f4cf2f1ac4ee77661ca9ba385a3a2ede76e33427636926c5d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab127bd874f0a0effd6a6cbb4d60de2bc769bc4b95037c4967137ff071555ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="recordIdentifierFeatureName")
    def record_identifier_feature_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordIdentifierFeatureName"))

    @record_identifier_feature_name.setter
    def record_identifier_feature_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fb40824f17ca9ab70382c14d7806c36df83ac3f11c3e77593020c7405d4568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordIdentifierFeatureName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce674253b30475b85d92cdcebb678b1d424bb93231c75bea90032ac401ea95b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347132f965339567d931d8d0c86e78e846312d822cc7d36f24b5ac3880401859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4d766541ef7bedb9ae130a71a0abddbafabf3c3ea7a2fdda59456113fe00fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "event_time_feature_name": "eventTimeFeatureName",
        "feature_definition": "featureDefinition",
        "feature_group_name": "featureGroupName",
        "record_identifier_feature_name": "recordIdentifierFeatureName",
        "role_arn": "roleArn",
        "description": "description",
        "id": "id",
        "offline_store_config": "offlineStoreConfig",
        "online_store_config": "onlineStoreConfig",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class SagemakerFeatureGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        event_time_feature_name: builtins.str,
        feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerFeatureGroupFeatureDefinition", typing.Dict[builtins.str, typing.Any]]]],
        feature_group_name: builtins.str,
        record_identifier_feature_name: builtins.str,
        role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        offline_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        online_store_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param event_time_feature_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#event_time_feature_name SagemakerFeatureGroup#event_time_feature_name}.
        :param feature_definition: feature_definition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#feature_definition SagemakerFeatureGroup#feature_definition}
        :param feature_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#feature_group_name SagemakerFeatureGroup#feature_group_name}.
        :param record_identifier_feature_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#record_identifier_feature_name SagemakerFeatureGroup#record_identifier_feature_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#role_arn SagemakerFeatureGroup#role_arn}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#description SagemakerFeatureGroup#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#id SagemakerFeatureGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param offline_store_config: offline_store_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#offline_store_config SagemakerFeatureGroup#offline_store_config}
        :param online_store_config: online_store_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#online_store_config SagemakerFeatureGroup#online_store_config}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#tags SagemakerFeatureGroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#tags_all SagemakerFeatureGroup#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(offline_store_config, dict):
            offline_store_config = SagemakerFeatureGroupOfflineStoreConfig(**offline_store_config)
        if isinstance(online_store_config, dict):
            online_store_config = SagemakerFeatureGroupOnlineStoreConfig(**online_store_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861775ad630b3d6478d6b4387d0af30f35c6c93a92148b2c5377dae9fcfb87d3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument event_time_feature_name", value=event_time_feature_name, expected_type=type_hints["event_time_feature_name"])
            check_type(argname="argument feature_definition", value=feature_definition, expected_type=type_hints["feature_definition"])
            check_type(argname="argument feature_group_name", value=feature_group_name, expected_type=type_hints["feature_group_name"])
            check_type(argname="argument record_identifier_feature_name", value=record_identifier_feature_name, expected_type=type_hints["record_identifier_feature_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument offline_store_config", value=offline_store_config, expected_type=type_hints["offline_store_config"])
            check_type(argname="argument online_store_config", value=online_store_config, expected_type=type_hints["online_store_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_time_feature_name": event_time_feature_name,
            "feature_definition": feature_definition,
            "feature_group_name": feature_group_name,
            "record_identifier_feature_name": record_identifier_feature_name,
            "role_arn": role_arn,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if offline_store_config is not None:
            self._values["offline_store_config"] = offline_store_config
        if online_store_config is not None:
            self._values["online_store_config"] = online_store_config
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def event_time_feature_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#event_time_feature_name SagemakerFeatureGroup#event_time_feature_name}.'''
        result = self._values.get("event_time_feature_name")
        assert result is not None, "Required property 'event_time_feature_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def feature_definition(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]]:
        '''feature_definition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#feature_definition SagemakerFeatureGroup#feature_definition}
        '''
        result = self._values.get("feature_definition")
        assert result is not None, "Required property 'feature_definition' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerFeatureGroupFeatureDefinition"]], result)

    @builtins.property
    def feature_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#feature_group_name SagemakerFeatureGroup#feature_group_name}.'''
        result = self._values.get("feature_group_name")
        assert result is not None, "Required property 'feature_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def record_identifier_feature_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#record_identifier_feature_name SagemakerFeatureGroup#record_identifier_feature_name}.'''
        result = self._values.get("record_identifier_feature_name")
        assert result is not None, "Required property 'record_identifier_feature_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#role_arn SagemakerFeatureGroup#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#description SagemakerFeatureGroup#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#id SagemakerFeatureGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def offline_store_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"]:
        '''offline_store_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#offline_store_config SagemakerFeatureGroup#offline_store_config}
        '''
        result = self._values.get("offline_store_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfig"], result)

    @builtins.property
    def online_store_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"]:
        '''online_store_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#online_store_config SagemakerFeatureGroup#online_store_config}
        '''
        result = self._values.get("online_store_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#tags SagemakerFeatureGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#tags_all SagemakerFeatureGroup#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinition",
    jsii_struct_bases=[],
    name_mapping={"feature_name": "featureName", "feature_type": "featureType"},
)
class SagemakerFeatureGroupFeatureDefinition:
    def __init__(
        self,
        *,
        feature_name: typing.Optional[builtins.str] = None,
        feature_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param feature_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#feature_name SagemakerFeatureGroup#feature_name}.
        :param feature_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#feature_type SagemakerFeatureGroup#feature_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6eedc76255d0dab12ba340b1de4b9c5b780e2db9a7924143c5bdf6a34a0944)
            check_type(argname="argument feature_name", value=feature_name, expected_type=type_hints["feature_name"])
            check_type(argname="argument feature_type", value=feature_type, expected_type=type_hints["feature_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if feature_name is not None:
            self._values["feature_name"] = feature_name
        if feature_type is not None:
            self._values["feature_type"] = feature_type

    @builtins.property
    def feature_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#feature_name SagemakerFeatureGroup#feature_name}.'''
        result = self._values.get("feature_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feature_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#feature_type SagemakerFeatureGroup#feature_type}.'''
        result = self._values.get("feature_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupFeatureDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupFeatureDefinitionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0f6bbea9a1d48ee01d23af83dce8a4961e496ebfefee50c336bf730a92c690b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerFeatureGroupFeatureDefinitionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368c85b1d5df5bb9cf37989cda3bbd5310a1fec7c5d0ee80206dbc62e0e9646b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerFeatureGroupFeatureDefinitionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31378e2885cc834747e93c343f1c3b28c7c9b0a64db180e578942819ab7f8643)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bf85ba093ddfa7140d7b758b793072e72b71a0f1950a465d8c69aefd5c5a2c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01151c73b99098dd965a2359421e038281a938d7164f55c0a3149fa659b1400a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93fba276ec50bb3b4b5b6e233c86b2a289ae208eff54bfd739301359da93213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerFeatureGroupFeatureDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupFeatureDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9674c82c678d33b7506969f1862ef9a2a329e01af1c76cad07a03f52d2969e3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFeatureName")
    def reset_feature_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureName", []))

    @jsii.member(jsii_name="resetFeatureType")
    def reset_feature_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureType", []))

    @builtins.property
    @jsii.member(jsii_name="featureNameInput")
    def feature_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureNameInput"))

    @builtins.property
    @jsii.member(jsii_name="featureTypeInput")
    def feature_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="featureName")
    def feature_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureName"))

    @feature_name.setter
    def feature_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc52de7ba6656292fac139223154d10062a8d48433aacc56552a225235be7b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureName", value)

    @builtins.property
    @jsii.member(jsii_name="featureType")
    def feature_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureType"))

    @feature_type.setter
    def feature_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330650f237758561954c21cfae24369f565116da3731e40db80f0c2f16499b68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SagemakerFeatureGroupFeatureDefinition, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SagemakerFeatureGroupFeatureDefinition, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SagemakerFeatureGroupFeatureDefinition, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4556ba2ffa88d3076f49222f4204a9ef042b09c7021e9e8f945e0e73546267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfig",
    jsii_struct_bases=[],
    name_mapping={
        "s3_storage_config": "s3StorageConfig",
        "data_catalog_config": "dataCatalogConfig",
        "disable_glue_table_creation": "disableGlueTableCreation",
    },
)
class SagemakerFeatureGroupOfflineStoreConfig:
    def __init__(
        self,
        *,
        s3_storage_config: typing.Union["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig", typing.Dict[builtins.str, typing.Any]],
        data_catalog_config: typing.Optional[typing.Union["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable_glue_table_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param s3_storage_config: s3_storage_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#s3_storage_config SagemakerFeatureGroup#s3_storage_config}
        :param data_catalog_config: data_catalog_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#data_catalog_config SagemakerFeatureGroup#data_catalog_config}
        :param disable_glue_table_creation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#disable_glue_table_creation SagemakerFeatureGroup#disable_glue_table_creation}.
        '''
        if isinstance(s3_storage_config, dict):
            s3_storage_config = SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig(**s3_storage_config)
        if isinstance(data_catalog_config, dict):
            data_catalog_config = SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig(**data_catalog_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9faef9544994fc2a7fa3833bf1730143d7164e904ea1635160e779628df790)
            check_type(argname="argument s3_storage_config", value=s3_storage_config, expected_type=type_hints["s3_storage_config"])
            check_type(argname="argument data_catalog_config", value=data_catalog_config, expected_type=type_hints["data_catalog_config"])
            check_type(argname="argument disable_glue_table_creation", value=disable_glue_table_creation, expected_type=type_hints["disable_glue_table_creation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_storage_config": s3_storage_config,
        }
        if data_catalog_config is not None:
            self._values["data_catalog_config"] = data_catalog_config
        if disable_glue_table_creation is not None:
            self._values["disable_glue_table_creation"] = disable_glue_table_creation

    @builtins.property
    def s3_storage_config(
        self,
    ) -> "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig":
        '''s3_storage_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#s3_storage_config SagemakerFeatureGroup#s3_storage_config}
        '''
        result = self._values.get("s3_storage_config")
        assert result is not None, "Required property 's3_storage_config' is missing"
        return typing.cast("SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig", result)

    @builtins.property
    def data_catalog_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig"]:
        '''data_catalog_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#data_catalog_config SagemakerFeatureGroup#data_catalog_config}
        '''
        result = self._values.get("data_catalog_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig"], result)

    @builtins.property
    def disable_glue_table_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#disable_glue_table_creation SagemakerFeatureGroup#disable_glue_table_creation}.'''
        result = self._values.get("disable_glue_table_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOfflineStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "catalog": "catalog",
        "database": "database",
        "table_name": "tableName",
    },
)
class SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig:
    def __init__(
        self,
        *,
        catalog: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param catalog: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#catalog SagemakerFeatureGroup#catalog}.
        :param database: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#database SagemakerFeatureGroup#database}.
        :param table_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#table_name SagemakerFeatureGroup#table_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb4c8164be71c6181be17ddc68e74a8a07b93fb60b02743b722131ebc9b1aa5)
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog is not None:
            self._values["catalog"] = catalog
        if database is not None:
            self._values["database"] = database
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#catalog SagemakerFeatureGroup#catalog}.'''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#database SagemakerFeatureGroup#database}.'''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#table_name SagemakerFeatureGroup#table_name}.'''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35e54bd70d779b4f1cc7fb68c15e289c683d38093b167f55661a612d66b1171c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCatalog")
    def reset_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalog", []))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetTableName")
    def reset_table_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableName", []))

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29e2c0a5b9abb18fc8fe3ea0b657fbb9896c18ce259d9875c858e18fa58c40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value)

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b80fc1fe2806e2e9c78489c5918f9d751d2f16099d14716bc0fafc8fcb5db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62c032b156044fb8e752b936d2edec2b19678b3d690e9509e22a7dc9629a3a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0da08df1b7cf5110cd3a0241655b35a8d02bcd89f687fa4cb147be316ff77de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerFeatureGroupOfflineStoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a77affbf109fd633cbed112763c946d5e26813a32ece9e749d27e8a8c049f10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataCatalogConfig")
    def put_data_catalog_config(
        self,
        *,
        catalog: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param catalog: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#catalog SagemakerFeatureGroup#catalog}.
        :param database: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#database SagemakerFeatureGroup#database}.
        :param table_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#table_name SagemakerFeatureGroup#table_name}.
        '''
        value = SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig(
            catalog=catalog, database=database, table_name=table_name
        )

        return typing.cast(None, jsii.invoke(self, "putDataCatalogConfig", [value]))

    @jsii.member(jsii_name="putS3StorageConfig")
    def put_s3_storage_config(
        self,
        *,
        s3_uri: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#s3_uri SagemakerFeatureGroup#s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        '''
        value = SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig(
            s3_uri=s3_uri, kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putS3StorageConfig", [value]))

    @jsii.member(jsii_name="resetDataCatalogConfig")
    def reset_data_catalog_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCatalogConfig", []))

    @jsii.member(jsii_name="resetDisableGlueTableCreation")
    def reset_disable_glue_table_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableGlueTableCreation", []))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogConfig")
    def data_catalog_config(
        self,
    ) -> SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference:
        return typing.cast(SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference, jsii.get(self, "dataCatalogConfig"))

    @builtins.property
    @jsii.member(jsii_name="s3StorageConfig")
    def s3_storage_config(
        self,
    ) -> "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference", jsii.get(self, "s3StorageConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataCatalogConfigInput")
    def data_catalog_config_input(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig], jsii.get(self, "dataCatalogConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="disableGlueTableCreationInput")
    def disable_glue_table_creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableGlueTableCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3StorageConfigInput")
    def s3_storage_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig"], jsii.get(self, "s3StorageConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="disableGlueTableCreation")
    def disable_glue_table_creation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableGlueTableCreation"))

    @disable_glue_table_creation.setter
    def disable_glue_table_creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9c1796c004820ba3e35d6f74763abe6f85bf54a5a422ae1d2db30416e83e03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableGlueTableCreation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fefb34ad884af5f9576c1fa3f4bd7830d0034c8bfbd622964f240332f946b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig",
    jsii_struct_bases=[],
    name_mapping={"s3_uri": "s3Uri", "kms_key_id": "kmsKeyId"},
)
class SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig:
    def __init__(
        self,
        *,
        s3_uri: builtins.str,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#s3_uri SagemakerFeatureGroup#s3_uri}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f12aa114b55b0a8c6fbcff2160da3c756f952f41afb70bfbce9863a1f1c1ef)
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_uri": s3_uri,
        }
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def s3_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#s3_uri SagemakerFeatureGroup#s3_uri}.'''
        result = self._values.get("s3_uri")
        assert result is not None, "Required property 's3_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dd0a276ab23170abeb40c6b1e01cfde1ce1963d4956ff954a75ab1b28b85557)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="s3UriInput")
    def s3_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3UriInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f59e0df8c7d615a714f6fcf4524611e726fea2557d46d601ce3285ed57bf6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="s3Uri")
    def s3_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Uri"))

    @s3_uri.setter
    def s3_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2a26e287eaeaf2b40803b833b44bc0510ecae085c8c014212e782322dbe48e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Uri", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b759b3977dfc64448d06dab3ce1a3acd5179cf41aebba5c8001e8bbda265aa63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_online_store": "enableOnlineStore",
        "security_config": "securityConfig",
    },
)
class SagemakerFeatureGroupOnlineStoreConfig:
    def __init__(
        self,
        *,
        enable_online_store: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_config: typing.Optional[typing.Union["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enable_online_store: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#enable_online_store SagemakerFeatureGroup#enable_online_store}.
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#security_config SagemakerFeatureGroup#security_config}
        '''
        if isinstance(security_config, dict):
            security_config = SagemakerFeatureGroupOnlineStoreConfigSecurityConfig(**security_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee38a4265fcad3cd94a875cfe91cdbdda34067619e0331af86857fc065525f70)
            check_type(argname="argument enable_online_store", value=enable_online_store, expected_type=type_hints["enable_online_store"])
            check_type(argname="argument security_config", value=security_config, expected_type=type_hints["security_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_online_store is not None:
            self._values["enable_online_store"] = enable_online_store
        if security_config is not None:
            self._values["security_config"] = security_config

    @builtins.property
    def enable_online_store(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#enable_online_store SagemakerFeatureGroup#enable_online_store}.'''
        result = self._values.get("enable_online_store")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_config(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"]:
        '''security_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#security_config SagemakerFeatureGroup#security_config}
        '''
        result = self._values.get("security_config")
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOnlineStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOnlineStoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98e465bc2b7251e530bb3eb7b175f3f18e1ecf6cee9d8a7b0a263b3adf589732)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecurityConfig")
    def put_security_config(
        self,
        *,
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        '''
        value = SagemakerFeatureGroupOnlineStoreConfigSecurityConfig(
            kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityConfig", [value]))

    @jsii.member(jsii_name="resetEnableOnlineStore")
    def reset_enable_online_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableOnlineStore", []))

    @jsii.member(jsii_name="resetSecurityConfig")
    def reset_security_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfig", []))

    @builtins.property
    @jsii.member(jsii_name="securityConfig")
    def security_config(
        self,
    ) -> "SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference":
        return typing.cast("SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference", jsii.get(self, "securityConfig"))

    @builtins.property
    @jsii.member(jsii_name="enableOnlineStoreInput")
    def enable_online_store_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableOnlineStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigInput")
    def security_config_input(
        self,
    ) -> typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"]:
        return typing.cast(typing.Optional["SagemakerFeatureGroupOnlineStoreConfigSecurityConfig"], jsii.get(self, "securityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="enableOnlineStore")
    def enable_online_store(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableOnlineStore"))

    @enable_online_store.setter
    def enable_online_store(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74eeba363b265caff78cd9277ecafb7cdb319301f34301ae0c5360998b52403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableOnlineStore", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerFeatureGroupOnlineStoreConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOnlineStoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf126879ae2cefdedbdf03be7795481e816ca36f92a5637790f0015537737df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_id": "kmsKeyId"},
)
class SagemakerFeatureGroupOnlineStoreConfigSecurityConfig:
    def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc686ddcfc2e3b1f14913382f521b738fb7b984a7539cef33008175b5c960ff)
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_feature_group#kms_key_id SagemakerFeatureGroup#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerFeatureGroupOnlineStoreConfigSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerFeatureGroup.SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4730cde9d9e63ec7353b59ba007e962d7ca7a1b87ce14bd65d04d3cd297f2ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d322ea30ecc45d77cc90d3c4ed0f7fbc1b3fa7b5423734fb56744ad73613bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig]:
        return typing.cast(typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6481d9b571161f96816872fe152bec1157d35db024fef078703d21bb8bb049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SagemakerFeatureGroup",
    "SagemakerFeatureGroupConfig",
    "SagemakerFeatureGroupFeatureDefinition",
    "SagemakerFeatureGroupFeatureDefinitionList",
    "SagemakerFeatureGroupFeatureDefinitionOutputReference",
    "SagemakerFeatureGroupOfflineStoreConfig",
    "SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig",
    "SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfigOutputReference",
    "SagemakerFeatureGroupOfflineStoreConfigOutputReference",
    "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig",
    "SagemakerFeatureGroupOfflineStoreConfigS3StorageConfigOutputReference",
    "SagemakerFeatureGroupOnlineStoreConfig",
    "SagemakerFeatureGroupOnlineStoreConfigOutputReference",
    "SagemakerFeatureGroupOnlineStoreConfigSecurityConfig",
    "SagemakerFeatureGroupOnlineStoreConfigSecurityConfigOutputReference",
]

publication.publish()

def _typecheckingstub__a9c91ef1bb5461ff2a3c7186550b944001c7f829d03146414e1e2cf9493c4c31(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    event_time_feature_name: builtins.str,
    feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerFeatureGroupFeatureDefinition, typing.Dict[builtins.str, typing.Any]]]],
    feature_group_name: builtins.str,
    record_identifier_feature_name: builtins.str,
    role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    offline_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOfflineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    online_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__9f2de7932f37b777e95eb6662069644c82c6c36b1c6c4106c7fecca1dd69d29d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerFeatureGroupFeatureDefinition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce93cdcfe3c93deb74350d340d2a5377eaec6f6a9c24694e9b549b5578cf6ddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ed91340de29fee123af2b2791b2399d18a233f5e3f0ddeb530343f756b63b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4781ac5037a62f4cf2f1ac4ee77661ca9ba385a3a2ede76e33427636926c5d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab127bd874f0a0effd6a6cbb4d60de2bc769bc4b95037c4967137ff071555ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fb40824f17ca9ab70382c14d7806c36df83ac3f11c3e77593020c7405d4568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce674253b30475b85d92cdcebb678b1d424bb93231c75bea90032ac401ea95b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347132f965339567d931d8d0c86e78e846312d822cc7d36f24b5ac3880401859(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4d766541ef7bedb9ae130a71a0abddbafabf3c3ea7a2fdda59456113fe00fa(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861775ad630b3d6478d6b4387d0af30f35c6c93a92148b2c5377dae9fcfb87d3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_time_feature_name: builtins.str,
    feature_definition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerFeatureGroupFeatureDefinition, typing.Dict[builtins.str, typing.Any]]]],
    feature_group_name: builtins.str,
    record_identifier_feature_name: builtins.str,
    role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    offline_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOfflineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    online_store_config: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6eedc76255d0dab12ba340b1de4b9c5b780e2db9a7924143c5bdf6a34a0944(
    *,
    feature_name: typing.Optional[builtins.str] = None,
    feature_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f6bbea9a1d48ee01d23af83dce8a4961e496ebfefee50c336bf730a92c690b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368c85b1d5df5bb9cf37989cda3bbd5310a1fec7c5d0ee80206dbc62e0e9646b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31378e2885cc834747e93c343f1c3b28c7c9b0a64db180e578942819ab7f8643(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf85ba093ddfa7140d7b758b793072e72b71a0f1950a465d8c69aefd5c5a2c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01151c73b99098dd965a2359421e038281a938d7164f55c0a3149fa659b1400a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93fba276ec50bb3b4b5b6e233c86b2a289ae208eff54bfd739301359da93213(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerFeatureGroupFeatureDefinition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9674c82c678d33b7506969f1862ef9a2a329e01af1c76cad07a03f52d2969e3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc52de7ba6656292fac139223154d10062a8d48433aacc56552a225235be7b1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330650f237758561954c21cfae24369f565116da3731e40db80f0c2f16499b68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4556ba2ffa88d3076f49222f4204a9ef042b09c7021e9e8f945e0e73546267(
    value: typing.Optional[typing.Union[SagemakerFeatureGroupFeatureDefinition, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9faef9544994fc2a7fa3833bf1730143d7164e904ea1635160e779628df790(
    *,
    s3_storage_config: typing.Union[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig, typing.Dict[builtins.str, typing.Any]],
    data_catalog_config: typing.Optional[typing.Union[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable_glue_table_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb4c8164be71c6181be17ddc68e74a8a07b93fb60b02743b722131ebc9b1aa5(
    *,
    catalog: typing.Optional[builtins.str] = None,
    database: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e54bd70d779b4f1cc7fb68c15e289c683d38093b167f55661a612d66b1171c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29e2c0a5b9abb18fc8fe3ea0b657fbb9896c18ce259d9875c858e18fa58c40f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b80fc1fe2806e2e9c78489c5918f9d751d2f16099d14716bc0fafc8fcb5db7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62c032b156044fb8e752b936d2edec2b19678b3d690e9509e22a7dc9629a3a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0da08df1b7cf5110cd3a0241655b35a8d02bcd89f687fa4cb147be316ff77de(
    value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigDataCatalogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a77affbf109fd633cbed112763c946d5e26813a32ece9e749d27e8a8c049f10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9c1796c004820ba3e35d6f74763abe6f85bf54a5a422ae1d2db30416e83e03(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fefb34ad884af5f9576c1fa3f4bd7830d0034c8bfbd622964f240332f946b67(
    value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f12aa114b55b0a8c6fbcff2160da3c756f952f41afb70bfbce9863a1f1c1ef(
    *,
    s3_uri: builtins.str,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd0a276ab23170abeb40c6b1e01cfde1ce1963d4956ff954a75ab1b28b85557(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f59e0df8c7d615a714f6fcf4524611e726fea2557d46d601ce3285ed57bf6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2a26e287eaeaf2b40803b833b44bc0510ecae085c8c014212e782322dbe48e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b759b3977dfc64448d06dab3ce1a3acd5179cf41aebba5c8001e8bbda265aa63(
    value: typing.Optional[SagemakerFeatureGroupOfflineStoreConfigS3StorageConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee38a4265fcad3cd94a875cfe91cdbdda34067619e0331af86857fc065525f70(
    *,
    enable_online_store: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_config: typing.Optional[typing.Union[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e465bc2b7251e530bb3eb7b175f3f18e1ecf6cee9d8a7b0a263b3adf589732(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74eeba363b265caff78cd9277ecafb7cdb319301f34301ae0c5360998b52403(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf126879ae2cefdedbdf03be7795481e816ca36f92a5637790f0015537737df(
    value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc686ddcfc2e3b1f14913382f521b738fb7b984a7539cef33008175b5c960ff(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4730cde9d9e63ec7353b59ba007e962d7ca7a1b87ce14bd65d04d3cd297f2ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d322ea30ecc45d77cc90d3c4ed0f7fbc1b3fa7b5423734fb56744ad73613bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6481d9b571161f96816872fe152bec1157d35db024fef078703d21bb8bb049(
    value: typing.Optional[SagemakerFeatureGroupOnlineStoreConfigSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass
