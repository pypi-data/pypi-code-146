'''
# `google_kms_crypto_key`

Refer to the Terraform Registory for docs: [`google_kms_crypto_key`](https://www.terraform.io/docs/providers/google/r/kms_crypto_key).
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


class KmsCryptoKey(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKey.KmsCryptoKey",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key google_kms_crypto_key}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        key_ring: builtins.str,
        name: builtins.str,
        destroy_scheduled_duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        import_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        purpose: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[builtins.str] = None,
        skip_initial_version_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["KmsCryptoKeyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_template: typing.Optional[typing.Union["KmsCryptoKeyVersionTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key google_kms_crypto_key} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key_ring: The KeyRing that this key belongs to. Format: ''projects/{{project}}/locations/{{location}}/keyRings/{{keyRing}}''. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#key_ring KmsCryptoKey#key_ring}
        :param name: The resource name for the CryptoKey. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#name KmsCryptoKey#name}
        :param destroy_scheduled_duration: The period of time that versions of this key spend in the DESTROY_SCHEDULED state before transitioning to DESTROYED. If not specified at creation time, the default duration is 24 hours. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#destroy_scheduled_duration KmsCryptoKey#destroy_scheduled_duration}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#id KmsCryptoKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_only: Whether this key may contain imported versions only. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#import_only KmsCryptoKey#import_only}
        :param labels: Labels with user-defined metadata to apply to this resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#labels KmsCryptoKey#labels}
        :param purpose: The immutable purpose of this CryptoKey. See the `purpose reference <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKeyPurpose>`_ for possible inputs. Default value: "ENCRYPT_DECRYPT" Possible values: ["ENCRYPT_DECRYPT", "ASYMMETRIC_SIGN", "ASYMMETRIC_DECRYPT", "MAC"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#purpose KmsCryptoKey#purpose}
        :param rotation_period: Every time this period passes, generate a new CryptoKeyVersion and set it as the primary. The first rotation will take place after the specified period. The rotation period has the format of a decimal number with up to 9 fractional digits, followed by the letter 's' (seconds). It must be greater than a day (ie, 86400). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#rotation_period KmsCryptoKey#rotation_period}
        :param skip_initial_version_creation: If set to true, the request will create a CryptoKey without any CryptoKeyVersions. You must use the 'google_kms_key_ring_import_job' resource to import the CryptoKeyVersion. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#skip_initial_version_creation KmsCryptoKey#skip_initial_version_creation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#timeouts KmsCryptoKey#timeouts}
        :param version_template: version_template block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#version_template KmsCryptoKey#version_template}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360e2f1b7348353484f40535f49bb7cf933f07f93f999fbb9e590db2da93b114)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KmsCryptoKeyConfig(
            key_ring=key_ring,
            name=name,
            destroy_scheduled_duration=destroy_scheduled_duration,
            id=id,
            import_only=import_only,
            labels=labels,
            purpose=purpose,
            rotation_period=rotation_period,
            skip_initial_version_creation=skip_initial_version_creation,
            timeouts=timeouts,
            version_template=version_template,
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
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#create KmsCryptoKey#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#delete KmsCryptoKey#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#update KmsCryptoKey#update}.
        '''
        value = KmsCryptoKeyTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVersionTemplate")
    def put_version_template(
        self,
        *,
        algorithm: builtins.str,
        protection_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: The algorithm to use when creating a version based on this template. See the `algorithm reference <https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm>`_ for possible inputs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#algorithm KmsCryptoKey#algorithm}
        :param protection_level: The protection level to use when creating a version based on this template. Possible values include "SOFTWARE", "HSM", "EXTERNAL", "EXTERNAL_VPC". Defaults to "SOFTWARE". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#protection_level KmsCryptoKey#protection_level}
        '''
        value = KmsCryptoKeyVersionTemplate(
            algorithm=algorithm, protection_level=protection_level
        )

        return typing.cast(None, jsii.invoke(self, "putVersionTemplate", [value]))

    @jsii.member(jsii_name="resetDestroyScheduledDuration")
    def reset_destroy_scheduled_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestroyScheduledDuration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImportOnly")
    def reset_import_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportOnly", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetPurpose")
    def reset_purpose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPurpose", []))

    @jsii.member(jsii_name="resetRotationPeriod")
    def reset_rotation_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRotationPeriod", []))

    @jsii.member(jsii_name="resetSkipInitialVersionCreation")
    def reset_skip_initial_version_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipInitialVersionCreation", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersionTemplate")
    def reset_version_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionTemplate", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KmsCryptoKeyTimeoutsOutputReference":
        return typing.cast("KmsCryptoKeyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="versionTemplate")
    def version_template(self) -> "KmsCryptoKeyVersionTemplateOutputReference":
        return typing.cast("KmsCryptoKeyVersionTemplateOutputReference", jsii.get(self, "versionTemplate"))

    @builtins.property
    @jsii.member(jsii_name="destroyScheduledDurationInput")
    def destroy_scheduled_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destroyScheduledDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importOnlyInput")
    def import_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "importOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyRingInput")
    def key_ring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyRingInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="purposeInput")
    def purpose_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "purposeInput"))

    @builtins.property
    @jsii.member(jsii_name="rotationPeriodInput")
    def rotation_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rotationPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="skipInitialVersionCreationInput")
    def skip_initial_version_creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipInitialVersionCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["KmsCryptoKeyTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["KmsCryptoKeyTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionTemplateInput")
    def version_template_input(self) -> typing.Optional["KmsCryptoKeyVersionTemplate"]:
        return typing.cast(typing.Optional["KmsCryptoKeyVersionTemplate"], jsii.get(self, "versionTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="destroyScheduledDuration")
    def destroy_scheduled_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destroyScheduledDuration"))

    @destroy_scheduled_duration.setter
    def destroy_scheduled_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a7e0e17cb5393b1b8dadfde6fcf87f3f6da725c9585c008e642769c4559500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destroyScheduledDuration", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785dad1320165fd05c6a8be2c6f989fbe5186ba2ab77fe16befe1f346b84ae4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="importOnly")
    def import_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "importOnly"))

    @import_only.setter
    def import_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e3efb9cf38a5ba359e387896b9e75c8c068b81b5eb094392c079d36f8d8a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importOnly", value)

    @builtins.property
    @jsii.member(jsii_name="keyRing")
    def key_ring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyRing"))

    @key_ring.setter
    def key_ring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f68f382ee14133da0a85d40332846e83a39bd0491cd6f1dcd9902fd2762eec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyRing", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9aec9b800c167502e555ba44373732f11bff9d9bb0fc79f54cc3c3487873f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ed17648da6a719106d8b1f774d1825a5488bef5a78df7b32328673c1753257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="purpose")
    def purpose(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "purpose"))

    @purpose.setter
    def purpose(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa495ee4c77f53f580dda6d6e53de6999619806e587efce4d2198a84ea279250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "purpose", value)

    @builtins.property
    @jsii.member(jsii_name="rotationPeriod")
    def rotation_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rotationPeriod"))

    @rotation_period.setter
    def rotation_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d42db38df52919e5b5b43ace5cb6a1310ba1ee14ebff2d69681d5c96d94da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rotationPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="skipInitialVersionCreation")
    def skip_initial_version_creation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipInitialVersionCreation"))

    @skip_initial_version_creation.setter
    def skip_initial_version_creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4949b7251ab3896462e52e83cd93cc98aeb1d84a138ed2e2f7d5e7a015483337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipInitialVersionCreation", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsCryptoKey.KmsCryptoKeyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "key_ring": "keyRing",
        "name": "name",
        "destroy_scheduled_duration": "destroyScheduledDuration",
        "id": "id",
        "import_only": "importOnly",
        "labels": "labels",
        "purpose": "purpose",
        "rotation_period": "rotationPeriod",
        "skip_initial_version_creation": "skipInitialVersionCreation",
        "timeouts": "timeouts",
        "version_template": "versionTemplate",
    },
)
class KmsCryptoKeyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        key_ring: builtins.str,
        name: builtins.str,
        destroy_scheduled_duration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        import_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        purpose: typing.Optional[builtins.str] = None,
        rotation_period: typing.Optional[builtins.str] = None,
        skip_initial_version_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["KmsCryptoKeyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_template: typing.Optional[typing.Union["KmsCryptoKeyVersionTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param key_ring: The KeyRing that this key belongs to. Format: ''projects/{{project}}/locations/{{location}}/keyRings/{{keyRing}}''. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#key_ring KmsCryptoKey#key_ring}
        :param name: The resource name for the CryptoKey. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#name KmsCryptoKey#name}
        :param destroy_scheduled_duration: The period of time that versions of this key spend in the DESTROY_SCHEDULED state before transitioning to DESTROYED. If not specified at creation time, the default duration is 24 hours. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#destroy_scheduled_duration KmsCryptoKey#destroy_scheduled_duration}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#id KmsCryptoKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_only: Whether this key may contain imported versions only. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#import_only KmsCryptoKey#import_only}
        :param labels: Labels with user-defined metadata to apply to this resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#labels KmsCryptoKey#labels}
        :param purpose: The immutable purpose of this CryptoKey. See the `purpose reference <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKeyPurpose>`_ for possible inputs. Default value: "ENCRYPT_DECRYPT" Possible values: ["ENCRYPT_DECRYPT", "ASYMMETRIC_SIGN", "ASYMMETRIC_DECRYPT", "MAC"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#purpose KmsCryptoKey#purpose}
        :param rotation_period: Every time this period passes, generate a new CryptoKeyVersion and set it as the primary. The first rotation will take place after the specified period. The rotation period has the format of a decimal number with up to 9 fractional digits, followed by the letter 's' (seconds). It must be greater than a day (ie, 86400). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#rotation_period KmsCryptoKey#rotation_period}
        :param skip_initial_version_creation: If set to true, the request will create a CryptoKey without any CryptoKeyVersions. You must use the 'google_kms_key_ring_import_job' resource to import the CryptoKeyVersion. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#skip_initial_version_creation KmsCryptoKey#skip_initial_version_creation}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#timeouts KmsCryptoKey#timeouts}
        :param version_template: version_template block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#version_template KmsCryptoKey#version_template}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = KmsCryptoKeyTimeouts(**timeouts)
        if isinstance(version_template, dict):
            version_template = KmsCryptoKeyVersionTemplate(**version_template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8b118d98fc9b758f5fe34a4a22c9d436b3addda6a8e890b7eef48c0c739d0f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument key_ring", value=key_ring, expected_type=type_hints["key_ring"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument destroy_scheduled_duration", value=destroy_scheduled_duration, expected_type=type_hints["destroy_scheduled_duration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument import_only", value=import_only, expected_type=type_hints["import_only"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument purpose", value=purpose, expected_type=type_hints["purpose"])
            check_type(argname="argument rotation_period", value=rotation_period, expected_type=type_hints["rotation_period"])
            check_type(argname="argument skip_initial_version_creation", value=skip_initial_version_creation, expected_type=type_hints["skip_initial_version_creation"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version_template", value=version_template, expected_type=type_hints["version_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_ring": key_ring,
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
        if destroy_scheduled_duration is not None:
            self._values["destroy_scheduled_duration"] = destroy_scheduled_duration
        if id is not None:
            self._values["id"] = id
        if import_only is not None:
            self._values["import_only"] = import_only
        if labels is not None:
            self._values["labels"] = labels
        if purpose is not None:
            self._values["purpose"] = purpose
        if rotation_period is not None:
            self._values["rotation_period"] = rotation_period
        if skip_initial_version_creation is not None:
            self._values["skip_initial_version_creation"] = skip_initial_version_creation
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version_template is not None:
            self._values["version_template"] = version_template

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
    def key_ring(self) -> builtins.str:
        '''The KeyRing that this key belongs to. Format: ''projects/{{project}}/locations/{{location}}/keyRings/{{keyRing}}''.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#key_ring KmsCryptoKey#key_ring}
        '''
        result = self._values.get("key_ring")
        assert result is not None, "Required property 'key_ring' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name for the CryptoKey.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#name KmsCryptoKey#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destroy_scheduled_duration(self) -> typing.Optional[builtins.str]:
        '''The period of time that versions of this key spend in the DESTROY_SCHEDULED state before transitioning to DESTROYED.

        If not specified at creation time, the default duration is 24 hours.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#destroy_scheduled_duration KmsCryptoKey#destroy_scheduled_duration}
        '''
        result = self._values.get("destroy_scheduled_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#id KmsCryptoKey#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this key may contain imported versions only.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#import_only KmsCryptoKey#import_only}
        '''
        result = self._values.get("import_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels with user-defined metadata to apply to this resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#labels KmsCryptoKey#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def purpose(self) -> typing.Optional[builtins.str]:
        '''The immutable purpose of this CryptoKey.

        See the
        `purpose reference <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKeyPurpose>`_
        for possible inputs. Default value: "ENCRYPT_DECRYPT" Possible values: ["ENCRYPT_DECRYPT", "ASYMMETRIC_SIGN", "ASYMMETRIC_DECRYPT", "MAC"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#purpose KmsCryptoKey#purpose}
        '''
        result = self._values.get("purpose")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_period(self) -> typing.Optional[builtins.str]:
        '''Every time this period passes, generate a new CryptoKeyVersion and set it as the primary.

        The first rotation will take place after the specified period. The rotation period has
        the format of a decimal number with up to 9 fractional digits, followed by the
        letter 's' (seconds). It must be greater than a day (ie, 86400).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#rotation_period KmsCryptoKey#rotation_period}
        '''
        result = self._values.get("rotation_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_initial_version_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the request will create a CryptoKey without any CryptoKeyVersions.

        You must use the 'google_kms_key_ring_import_job' resource to import the CryptoKeyVersion.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#skip_initial_version_creation KmsCryptoKey#skip_initial_version_creation}
        '''
        result = self._values.get("skip_initial_version_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KmsCryptoKeyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#timeouts KmsCryptoKey#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KmsCryptoKeyTimeouts"], result)

    @builtins.property
    def version_template(self) -> typing.Optional["KmsCryptoKeyVersionTemplate"]:
        '''version_template block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#version_template KmsCryptoKey#version_template}
        '''
        result = self._values.get("version_template")
        return typing.cast(typing.Optional["KmsCryptoKeyVersionTemplate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsCryptoKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsCryptoKey.KmsCryptoKeyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class KmsCryptoKeyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#create KmsCryptoKey#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#delete KmsCryptoKey#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#update KmsCryptoKey#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5c567a46814334f08063289a276571249fea37e3185cb7c2f8cbe143811195)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#create KmsCryptoKey#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#delete KmsCryptoKey#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#update KmsCryptoKey#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsCryptoKeyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KmsCryptoKeyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKey.KmsCryptoKeyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bfabd42387ccdcf346845bbc18065c16df9e4042f5db840b3e6ace270b3e7cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddf79fc78d8d4c045d90461166ce7acce1e67a63371474ae3456d5bea3969d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b20aebd575de5a4d904504d9e7c55f47cda61ea23ab14f793062d0475dcf4c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a554570467f5b8e9ec8c1d3881fe25871d5959e7b512da66823ce1c5de25336e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[KmsCryptoKeyTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[KmsCryptoKeyTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[KmsCryptoKeyTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3a990765a43c6c985c0555c925c0e7e2e5826aef7fe25f2af078b7e0625fd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsCryptoKey.KmsCryptoKeyVersionTemplate",
    jsii_struct_bases=[],
    name_mapping={"algorithm": "algorithm", "protection_level": "protectionLevel"},
)
class KmsCryptoKeyVersionTemplate:
    def __init__(
        self,
        *,
        algorithm: builtins.str,
        protection_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: The algorithm to use when creating a version based on this template. See the `algorithm reference <https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm>`_ for possible inputs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#algorithm KmsCryptoKey#algorithm}
        :param protection_level: The protection level to use when creating a version based on this template. Possible values include "SOFTWARE", "HSM", "EXTERNAL", "EXTERNAL_VPC". Defaults to "SOFTWARE". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#protection_level KmsCryptoKey#protection_level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7680affe6d56f10bb2e105bc16c6f2a3e5ec390e9b551d9b0957ac43d660e6a6)
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument protection_level", value=protection_level, expected_type=type_hints["protection_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "algorithm": algorithm,
        }
        if protection_level is not None:
            self._values["protection_level"] = protection_level

    @builtins.property
    def algorithm(self) -> builtins.str:
        '''The algorithm to use when creating a version based on this template. See the `algorithm reference <https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm>`_ for possible inputs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#algorithm KmsCryptoKey#algorithm}
        '''
        result = self._values.get("algorithm")
        assert result is not None, "Required property 'algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protection_level(self) -> typing.Optional[builtins.str]:
        '''The protection level to use when creating a version based on this template.

        Possible values include "SOFTWARE", "HSM", "EXTERNAL", "EXTERNAL_VPC". Defaults to "SOFTWARE".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/kms_crypto_key#protection_level KmsCryptoKey#protection_level}
        '''
        result = self._values.get("protection_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsCryptoKeyVersionTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KmsCryptoKeyVersionTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsCryptoKey.KmsCryptoKeyVersionTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e57518bbd90d3391d94f4e14823d1f6372d4f6c7f05ad10d0e476a542566c45a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProtectionLevel")
    def reset_protection_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectionLevel", []))

    @builtins.property
    @jsii.member(jsii_name="algorithmInput")
    def algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "algorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="protectionLevelInput")
    def protection_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectionLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @algorithm.setter
    def algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd74388a9d9a9be42e907321fd810aa05715a44cdfb655cd3efc0013099bf63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value)

    @builtins.property
    @jsii.member(jsii_name="protectionLevel")
    def protection_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectionLevel"))

    @protection_level.setter
    def protection_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7712280e3955395d3f6ea8a036c2544fc7026b8a3abae46c8544cea0a5faff80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectionLevel", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KmsCryptoKeyVersionTemplate]:
        return typing.cast(typing.Optional[KmsCryptoKeyVersionTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KmsCryptoKeyVersionTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac877cade0c0edd864105027171ca4e4329658996d36fce91b2b7cf85bb35e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "KmsCryptoKey",
    "KmsCryptoKeyConfig",
    "KmsCryptoKeyTimeouts",
    "KmsCryptoKeyTimeoutsOutputReference",
    "KmsCryptoKeyVersionTemplate",
    "KmsCryptoKeyVersionTemplateOutputReference",
]

publication.publish()

def _typecheckingstub__360e2f1b7348353484f40535f49bb7cf933f07f93f999fbb9e590db2da93b114(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    key_ring: builtins.str,
    name: builtins.str,
    destroy_scheduled_duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    import_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    purpose: typing.Optional[builtins.str] = None,
    rotation_period: typing.Optional[builtins.str] = None,
    skip_initial_version_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[KmsCryptoKeyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_template: typing.Optional[typing.Union[KmsCryptoKeyVersionTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f7a7e0e17cb5393b1b8dadfde6fcf87f3f6da725c9585c008e642769c4559500(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785dad1320165fd05c6a8be2c6f989fbe5186ba2ab77fe16befe1f346b84ae4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e3efb9cf38a5ba359e387896b9e75c8c068b81b5eb094392c079d36f8d8a74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f68f382ee14133da0a85d40332846e83a39bd0491cd6f1dcd9902fd2762eec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9aec9b800c167502e555ba44373732f11bff9d9bb0fc79f54cc3c3487873f40(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ed17648da6a719106d8b1f774d1825a5488bef5a78df7b32328673c1753257(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa495ee4c77f53f580dda6d6e53de6999619806e587efce4d2198a84ea279250(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d42db38df52919e5b5b43ace5cb6a1310ba1ee14ebff2d69681d5c96d94da7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4949b7251ab3896462e52e83cd93cc98aeb1d84a138ed2e2f7d5e7a015483337(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8b118d98fc9b758f5fe34a4a22c9d436b3addda6a8e890b7eef48c0c739d0f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_ring: builtins.str,
    name: builtins.str,
    destroy_scheduled_duration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    import_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    purpose: typing.Optional[builtins.str] = None,
    rotation_period: typing.Optional[builtins.str] = None,
    skip_initial_version_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[KmsCryptoKeyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_template: typing.Optional[typing.Union[KmsCryptoKeyVersionTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5c567a46814334f08063289a276571249fea37e3185cb7c2f8cbe143811195(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bfabd42387ccdcf346845bbc18065c16df9e4042f5db840b3e6ace270b3e7cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf79fc78d8d4c045d90461166ce7acce1e67a63371474ae3456d5bea3969d5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b20aebd575de5a4d904504d9e7c55f47cda61ea23ab14f793062d0475dcf4c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a554570467f5b8e9ec8c1d3881fe25871d5959e7b512da66823ce1c5de25336e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3a990765a43c6c985c0555c925c0e7e2e5826aef7fe25f2af078b7e0625fd8(
    value: typing.Optional[typing.Union[KmsCryptoKeyTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7680affe6d56f10bb2e105bc16c6f2a3e5ec390e9b551d9b0957ac43d660e6a6(
    *,
    algorithm: builtins.str,
    protection_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57518bbd90d3391d94f4e14823d1f6372d4f6c7f05ad10d0e476a542566c45a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd74388a9d9a9be42e907321fd810aa05715a44cdfb655cd3efc0013099bf63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7712280e3955395d3f6ea8a036c2544fc7026b8a3abae46c8544cea0a5faff80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac877cade0c0edd864105027171ca4e4329658996d36fce91b2b7cf85bb35e79(
    value: typing.Optional[KmsCryptoKeyVersionTemplate],
) -> None:
    """Type checking stubs"""
    pass
