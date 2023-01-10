'''
# `aws_macie_s3_bucket_association`

Refer to the Terraform Registory for docs: [`aws_macie_s3_bucket_association`](https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association).
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


class MacieS3BucketAssociation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macieS3BucketAssociation.MacieS3BucketAssociation",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association aws_macie_s3_bucket_association}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket_name: builtins.str,
        classification_type: typing.Optional[typing.Union["MacieS3BucketAssociationClassificationType", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        member_account_id: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association aws_macie_s3_bucket_association} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#bucket_name MacieS3BucketAssociation#bucket_name}.
        :param classification_type: classification_type block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#classification_type MacieS3BucketAssociation#classification_type}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#id MacieS3BucketAssociation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param member_account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#member_account_id MacieS3BucketAssociation#member_account_id}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#prefix MacieS3BucketAssociation#prefix}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041f56caa8f9eb91a247ae92db538ed6ea986c2d8fb90c457006acdc19301aef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MacieS3BucketAssociationConfig(
            bucket_name=bucket_name,
            classification_type=classification_type,
            id=id,
            member_account_id=member_account_id,
            prefix=prefix,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putClassificationType")
    def put_classification_type(
        self,
        *,
        continuous: typing.Optional[builtins.str] = None,
        one_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param continuous: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#continuous MacieS3BucketAssociation#continuous}.
        :param one_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#one_time MacieS3BucketAssociation#one_time}.
        '''
        value = MacieS3BucketAssociationClassificationType(
            continuous=continuous, one_time=one_time
        )

        return typing.cast(None, jsii.invoke(self, "putClassificationType", [value]))

    @jsii.member(jsii_name="resetClassificationType")
    def reset_classification_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClassificationType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMemberAccountId")
    def reset_member_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberAccountId", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="classificationType")
    def classification_type(
        self,
    ) -> "MacieS3BucketAssociationClassificationTypeOutputReference":
        return typing.cast("MacieS3BucketAssociationClassificationTypeOutputReference", jsii.get(self, "classificationType"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="classificationTypeInput")
    def classification_type_input(
        self,
    ) -> typing.Optional["MacieS3BucketAssociationClassificationType"]:
        return typing.cast(typing.Optional["MacieS3BucketAssociationClassificationType"], jsii.get(self, "classificationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="memberAccountIdInput")
    def member_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memberAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e627efc0b7480cb0bba3fac2e885efa79ced9f19b150ae1b92fb88c7f5ec5f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155d9b07fc58d6f54ee89218d5d38592cb28763c5d874caf59af07342f639691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="memberAccountId")
    def member_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memberAccountId"))

    @member_account_id.setter
    def member_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd5181874321f60fe965a764cf08019aa028813197ec993e4ae68e0b756aa6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c748410b693a86dbd849395d5ec035d77259959e2d08c23f0e051795157843c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macieS3BucketAssociation.MacieS3BucketAssociationClassificationType",
    jsii_struct_bases=[],
    name_mapping={"continuous": "continuous", "one_time": "oneTime"},
)
class MacieS3BucketAssociationClassificationType:
    def __init__(
        self,
        *,
        continuous: typing.Optional[builtins.str] = None,
        one_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param continuous: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#continuous MacieS3BucketAssociation#continuous}.
        :param one_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#one_time MacieS3BucketAssociation#one_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e09d1305a79f8ecc55d7f3238e3b82d09e6d8cbd2e07a652bf6c515d5409ba3)
            check_type(argname="argument continuous", value=continuous, expected_type=type_hints["continuous"])
            check_type(argname="argument one_time", value=one_time, expected_type=type_hints["one_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if continuous is not None:
            self._values["continuous"] = continuous
        if one_time is not None:
            self._values["one_time"] = one_time

    @builtins.property
    def continuous(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#continuous MacieS3BucketAssociation#continuous}.'''
        result = self._values.get("continuous")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def one_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#one_time MacieS3BucketAssociation#one_time}.'''
        result = self._values.get("one_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MacieS3BucketAssociationClassificationType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MacieS3BucketAssociationClassificationTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.macieS3BucketAssociation.MacieS3BucketAssociationClassificationTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00ee14470c596f326f296aa131018a26bde150ec4a2b75039de72bf362aeb2ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContinuous")
    def reset_continuous(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinuous", []))

    @jsii.member(jsii_name="resetOneTime")
    def reset_one_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOneTime", []))

    @builtins.property
    @jsii.member(jsii_name="continuousInput")
    def continuous_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "continuousInput"))

    @builtins.property
    @jsii.member(jsii_name="oneTimeInput")
    def one_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oneTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="continuous")
    def continuous(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "continuous"))

    @continuous.setter
    def continuous(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0846ee3a9fdb0f4210d29594dc6eaf40a4ffbdf0496455991cd3d0a39b15d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continuous", value)

    @builtins.property
    @jsii.member(jsii_name="oneTime")
    def one_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oneTime"))

    @one_time.setter
    def one_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2883f0d519668fc0882c984bfb0d8f56d40835079b9f3a41a3f53e22b54aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oneTime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MacieS3BucketAssociationClassificationType]:
        return typing.cast(typing.Optional[MacieS3BucketAssociationClassificationType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MacieS3BucketAssociationClassificationType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__781e8f16c6efc2452f6f793387cff6f0f0dcb966d779b85c19fa4574de699619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.macieS3BucketAssociation.MacieS3BucketAssociationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket_name": "bucketName",
        "classification_type": "classificationType",
        "id": "id",
        "member_account_id": "memberAccountId",
        "prefix": "prefix",
    },
)
class MacieS3BucketAssociationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bucket_name: builtins.str,
        classification_type: typing.Optional[typing.Union[MacieS3BucketAssociationClassificationType, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        member_account_id: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#bucket_name MacieS3BucketAssociation#bucket_name}.
        :param classification_type: classification_type block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#classification_type MacieS3BucketAssociation#classification_type}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#id MacieS3BucketAssociation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param member_account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#member_account_id MacieS3BucketAssociation#member_account_id}.
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#prefix MacieS3BucketAssociation#prefix}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(classification_type, dict):
            classification_type = MacieS3BucketAssociationClassificationType(**classification_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08447c94b6d8172869931eb2290eafa84758d69cadd39d450c515aaff4c643f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument classification_type", value=classification_type, expected_type=type_hints["classification_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument member_account_id", value=member_account_id, expected_type=type_hints["member_account_id"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
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
        if classification_type is not None:
            self._values["classification_type"] = classification_type
        if id is not None:
            self._values["id"] = id
        if member_account_id is not None:
            self._values["member_account_id"] = member_account_id
        if prefix is not None:
            self._values["prefix"] = prefix

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
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#bucket_name MacieS3BucketAssociation#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def classification_type(
        self,
    ) -> typing.Optional[MacieS3BucketAssociationClassificationType]:
        '''classification_type block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#classification_type MacieS3BucketAssociation#classification_type}
        '''
        result = self._values.get("classification_type")
        return typing.cast(typing.Optional[MacieS3BucketAssociationClassificationType], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#id MacieS3BucketAssociation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#member_account_id MacieS3BucketAssociation#member_account_id}.'''
        result = self._values.get("member_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/macie_s3_bucket_association#prefix MacieS3BucketAssociation#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MacieS3BucketAssociationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "MacieS3BucketAssociation",
    "MacieS3BucketAssociationClassificationType",
    "MacieS3BucketAssociationClassificationTypeOutputReference",
    "MacieS3BucketAssociationConfig",
]

publication.publish()

def _typecheckingstub__041f56caa8f9eb91a247ae92db538ed6ea986c2d8fb90c457006acdc19301aef(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket_name: builtins.str,
    classification_type: typing.Optional[typing.Union[MacieS3BucketAssociationClassificationType, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    member_account_id: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4e627efc0b7480cb0bba3fac2e885efa79ced9f19b150ae1b92fb88c7f5ec5f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155d9b07fc58d6f54ee89218d5d38592cb28763c5d874caf59af07342f639691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd5181874321f60fe965a764cf08019aa028813197ec993e4ae68e0b756aa6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c748410b693a86dbd849395d5ec035d77259959e2d08c23f0e051795157843c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e09d1305a79f8ecc55d7f3238e3b82d09e6d8cbd2e07a652bf6c515d5409ba3(
    *,
    continuous: typing.Optional[builtins.str] = None,
    one_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ee14470c596f326f296aa131018a26bde150ec4a2b75039de72bf362aeb2ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0846ee3a9fdb0f4210d29594dc6eaf40a4ffbdf0496455991cd3d0a39b15d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2883f0d519668fc0882c984bfb0d8f56d40835079b9f3a41a3f53e22b54aa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781e8f16c6efc2452f6f793387cff6f0f0dcb966d779b85c19fa4574de699619(
    value: typing.Optional[MacieS3BucketAssociationClassificationType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08447c94b6d8172869931eb2290eafa84758d69cadd39d450c515aaff4c643f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket_name: builtins.str,
    classification_type: typing.Optional[typing.Union[MacieS3BucketAssociationClassificationType, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    member_account_id: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
