'''
# `aws_qldb_stream`

Refer to the Terraform Registory for docs: [`aws_qldb_stream`](https://www.terraform.io/docs/providers/aws/r/qldb_stream).
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


class QldbStream(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.qldbStream.QldbStream",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream aws_qldb_stream}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        inclusive_start_time: builtins.str,
        kinesis_configuration: typing.Union["QldbStreamKinesisConfiguration", typing.Dict[builtins.str, typing.Any]],
        ledger_name: builtins.str,
        role_arn: builtins.str,
        stream_name: builtins.str,
        exclusive_end_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream aws_qldb_stream} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param inclusive_start_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#inclusive_start_time QldbStream#inclusive_start_time}.
        :param kinesis_configuration: kinesis_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#kinesis_configuration QldbStream#kinesis_configuration}
        :param ledger_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#ledger_name QldbStream#ledger_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#role_arn QldbStream#role_arn}.
        :param stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#stream_name QldbStream#stream_name}.
        :param exclusive_end_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#exclusive_end_time QldbStream#exclusive_end_time}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#id QldbStream#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#tags QldbStream#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#tags_all QldbStream#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bad3c7049dc9219a5ade642708bf690aa6a3e3784d4c116c6872854e352d802)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = QldbStreamConfig(
            inclusive_start_time=inclusive_start_time,
            kinesis_configuration=kinesis_configuration,
            ledger_name=ledger_name,
            role_arn=role_arn,
            stream_name=stream_name,
            exclusive_end_time=exclusive_end_time,
            id=id,
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

    @jsii.member(jsii_name="putKinesisConfiguration")
    def put_kinesis_configuration(
        self,
        *,
        stream_arn: builtins.str,
        aggregation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param stream_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#stream_arn QldbStream#stream_arn}.
        :param aggregation_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#aggregation_enabled QldbStream#aggregation_enabled}.
        '''
        value = QldbStreamKinesisConfiguration(
            stream_arn=stream_arn, aggregation_enabled=aggregation_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisConfiguration", [value]))

    @jsii.member(jsii_name="resetExclusiveEndTime")
    def reset_exclusive_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusiveEndTime", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="kinesisConfiguration")
    def kinesis_configuration(self) -> "QldbStreamKinesisConfigurationOutputReference":
        return typing.cast("QldbStreamKinesisConfigurationOutputReference", jsii.get(self, "kinesisConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="exclusiveEndTimeInput")
    def exclusive_end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exclusiveEndTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusiveStartTimeInput")
    def inclusive_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inclusiveStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisConfigurationInput")
    def kinesis_configuration_input(
        self,
    ) -> typing.Optional["QldbStreamKinesisConfiguration"]:
        return typing.cast(typing.Optional["QldbStreamKinesisConfiguration"], jsii.get(self, "kinesisConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="ledgerNameInput")
    def ledger_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ledgerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="streamNameInput")
    def stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamNameInput"))

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
    @jsii.member(jsii_name="exclusiveEndTime")
    def exclusive_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exclusiveEndTime"))

    @exclusive_end_time.setter
    def exclusive_end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6f8cea32bcdaa4ff517ff4bac32d448a323669c4fc77ccb138ef0d24d8e376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusiveEndTime", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ffdcb20954b6c48856f93520469ca3a3d91ccf5a735b749727dcf50d8c366d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="inclusiveStartTime")
    def inclusive_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inclusiveStartTime"))

    @inclusive_start_time.setter
    def inclusive_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ef04e29e996b5d14fa51d649e9005260ce86f37baa557ed04bb0eb4fa80770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inclusiveStartTime", value)

    @builtins.property
    @jsii.member(jsii_name="ledgerName")
    def ledger_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ledgerName"))

    @ledger_name.setter
    def ledger_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17aaf65baf99ee4b9de5e2eccd67d2edf57760f77cce89873fc219f285037f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ledgerName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60118948ade695967a6ce4290a0e65a2af1e618153ae04902de3f765a921cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @stream_name.setter
    def stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f127c63f8954038e536dc569b2765f131bf8a4d253e8adec38a93b80133976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebad497e42907710464e091ee5ea91a2ac8963ea369be4abce9542820d5cc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433bb9c367410f1f59a29e536267e275918253677b70226d2fa09f9dd18f02a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.qldbStream.QldbStreamConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "inclusive_start_time": "inclusiveStartTime",
        "kinesis_configuration": "kinesisConfiguration",
        "ledger_name": "ledgerName",
        "role_arn": "roleArn",
        "stream_name": "streamName",
        "exclusive_end_time": "exclusiveEndTime",
        "id": "id",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class QldbStreamConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        inclusive_start_time: builtins.str,
        kinesis_configuration: typing.Union["QldbStreamKinesisConfiguration", typing.Dict[builtins.str, typing.Any]],
        ledger_name: builtins.str,
        role_arn: builtins.str,
        stream_name: builtins.str,
        exclusive_end_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
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
        :param inclusive_start_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#inclusive_start_time QldbStream#inclusive_start_time}.
        :param kinesis_configuration: kinesis_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#kinesis_configuration QldbStream#kinesis_configuration}
        :param ledger_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#ledger_name QldbStream#ledger_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#role_arn QldbStream#role_arn}.
        :param stream_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#stream_name QldbStream#stream_name}.
        :param exclusive_end_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#exclusive_end_time QldbStream#exclusive_end_time}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#id QldbStream#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#tags QldbStream#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#tags_all QldbStream#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(kinesis_configuration, dict):
            kinesis_configuration = QldbStreamKinesisConfiguration(**kinesis_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38675c1e8d10828b358d1862174e326740809a0d46a5f2ecece9e2866c544607)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument inclusive_start_time", value=inclusive_start_time, expected_type=type_hints["inclusive_start_time"])
            check_type(argname="argument kinesis_configuration", value=kinesis_configuration, expected_type=type_hints["kinesis_configuration"])
            check_type(argname="argument ledger_name", value=ledger_name, expected_type=type_hints["ledger_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            check_type(argname="argument exclusive_end_time", value=exclusive_end_time, expected_type=type_hints["exclusive_end_time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "inclusive_start_time": inclusive_start_time,
            "kinesis_configuration": kinesis_configuration,
            "ledger_name": ledger_name,
            "role_arn": role_arn,
            "stream_name": stream_name,
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
        if exclusive_end_time is not None:
            self._values["exclusive_end_time"] = exclusive_end_time
        if id is not None:
            self._values["id"] = id
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
    def inclusive_start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#inclusive_start_time QldbStream#inclusive_start_time}.'''
        result = self._values.get("inclusive_start_time")
        assert result is not None, "Required property 'inclusive_start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kinesis_configuration(self) -> "QldbStreamKinesisConfiguration":
        '''kinesis_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#kinesis_configuration QldbStream#kinesis_configuration}
        '''
        result = self._values.get("kinesis_configuration")
        assert result is not None, "Required property 'kinesis_configuration' is missing"
        return typing.cast("QldbStreamKinesisConfiguration", result)

    @builtins.property
    def ledger_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#ledger_name QldbStream#ledger_name}.'''
        result = self._values.get("ledger_name")
        assert result is not None, "Required property 'ledger_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#role_arn QldbStream#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#stream_name QldbStream#stream_name}.'''
        result = self._values.get("stream_name")
        assert result is not None, "Required property 'stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclusive_end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#exclusive_end_time QldbStream#exclusive_end_time}.'''
        result = self._values.get("exclusive_end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#id QldbStream#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#tags QldbStream#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#tags_all QldbStream#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QldbStreamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.qldbStream.QldbStreamKinesisConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "stream_arn": "streamArn",
        "aggregation_enabled": "aggregationEnabled",
    },
)
class QldbStreamKinesisConfiguration:
    def __init__(
        self,
        *,
        stream_arn: builtins.str,
        aggregation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param stream_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#stream_arn QldbStream#stream_arn}.
        :param aggregation_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#aggregation_enabled QldbStream#aggregation_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783f43a229f050e9d75989735af6b618571abe45efbc4ace60314c3296e38a9a)
            check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            check_type(argname="argument aggregation_enabled", value=aggregation_enabled, expected_type=type_hints["aggregation_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stream_arn": stream_arn,
        }
        if aggregation_enabled is not None:
            self._values["aggregation_enabled"] = aggregation_enabled

    @builtins.property
    def stream_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#stream_arn QldbStream#stream_arn}.'''
        result = self._values.get("stream_arn")
        assert result is not None, "Required property 'stream_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aggregation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/qldb_stream#aggregation_enabled QldbStream#aggregation_enabled}.'''
        result = self._values.get("aggregation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QldbStreamKinesisConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QldbStreamKinesisConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.qldbStream.QldbStreamKinesisConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f457aa39f9b894b3529bfe6254ffd99e1a57e3e3bfd8699d4d67e492ac4ebb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAggregationEnabled")
    def reset_aggregation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationEnabledInput")
    def aggregation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "aggregationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="streamArnInput")
    def stream_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamArnInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationEnabled")
    def aggregation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "aggregationEnabled"))

    @aggregation_enabled.setter
    def aggregation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99cd20ec0da2d504d9188aeea38658ba850f0a5805abee1b6ee2722f3573279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamArn"))

    @stream_arn.setter
    def stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd86e19223dadf56243afad0caf937fc1f0ef5a096a1c23ae2dc49ffcf518e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QldbStreamKinesisConfiguration]:
        return typing.cast(typing.Optional[QldbStreamKinesisConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QldbStreamKinesisConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f247cfcc30f9c5dd3401b1d3a8ff882984805167c102e20272ad2c5a09569bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "QldbStream",
    "QldbStreamConfig",
    "QldbStreamKinesisConfiguration",
    "QldbStreamKinesisConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__2bad3c7049dc9219a5ade642708bf690aa6a3e3784d4c116c6872854e352d802(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    inclusive_start_time: builtins.str,
    kinesis_configuration: typing.Union[QldbStreamKinesisConfiguration, typing.Dict[builtins.str, typing.Any]],
    ledger_name: builtins.str,
    role_arn: builtins.str,
    stream_name: builtins.str,
    exclusive_end_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ba6f8cea32bcdaa4ff517ff4bac32d448a323669c4fc77ccb138ef0d24d8e376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ffdcb20954b6c48856f93520469ca3a3d91ccf5a735b749727dcf50d8c366d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ef04e29e996b5d14fa51d649e9005260ce86f37baa557ed04bb0eb4fa80770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17aaf65baf99ee4b9de5e2eccd67d2edf57760f77cce89873fc219f285037f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60118948ade695967a6ce4290a0e65a2af1e618153ae04902de3f765a921cf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f127c63f8954038e536dc569b2765f131bf8a4d253e8adec38a93b80133976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebad497e42907710464e091ee5ea91a2ac8963ea369be4abce9542820d5cc8e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433bb9c367410f1f59a29e536267e275918253677b70226d2fa09f9dd18f02a0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38675c1e8d10828b358d1862174e326740809a0d46a5f2ecece9e2866c544607(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inclusive_start_time: builtins.str,
    kinesis_configuration: typing.Union[QldbStreamKinesisConfiguration, typing.Dict[builtins.str, typing.Any]],
    ledger_name: builtins.str,
    role_arn: builtins.str,
    stream_name: builtins.str,
    exclusive_end_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783f43a229f050e9d75989735af6b618571abe45efbc4ace60314c3296e38a9a(
    *,
    stream_arn: builtins.str,
    aggregation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f457aa39f9b894b3529bfe6254ffd99e1a57e3e3bfd8699d4d67e492ac4ebb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99cd20ec0da2d504d9188aeea38658ba850f0a5805abee1b6ee2722f3573279(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd86e19223dadf56243afad0caf937fc1f0ef5a096a1c23ae2dc49ffcf518e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f247cfcc30f9c5dd3401b1d3a8ff882984805167c102e20272ad2c5a09569bd4(
    value: typing.Optional[QldbStreamKinesisConfiguration],
) -> None:
    """Type checking stubs"""
    pass
