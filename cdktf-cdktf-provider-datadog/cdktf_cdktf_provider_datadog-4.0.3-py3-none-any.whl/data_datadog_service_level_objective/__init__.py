'''
# `data_datadog_service_level_objective`

Refer to the Terraform Registory for docs: [`data_datadog_service_level_objective`](https://www.terraform.io/docs/providers/datadog/d/service_level_objective).
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


class DataDatadogServiceLevelObjective(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.dataDatadogServiceLevelObjective.DataDatadogServiceLevelObjective",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective datadog_service_level_objective}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        metrics_query: typing.Optional[builtins.str] = None,
        name_query: typing.Optional[builtins.str] = None,
        tags_query: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective datadog_service_level_objective} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: A SLO ID to limit the search. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#id DataDatadogServiceLevelObjective#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metrics_query: Filter results based on SLO numerator and denominator. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#metrics_query DataDatadogServiceLevelObjective#metrics_query}
        :param name_query: Filter results based on SLO names. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#name_query DataDatadogServiceLevelObjective#name_query}
        :param tags_query: Filter results based on a single SLO tag. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#tags_query DataDatadogServiceLevelObjective#tags_query}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6e54c89c4645eecd050e696fde778f4b6656a35c92bc833cf935e5b3aab1fb0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataDatadogServiceLevelObjectiveConfig(
            id=id,
            metrics_query=metrics_query,
            name_query=name_query,
            tags_query=tags_query,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMetricsQuery")
    def reset_metrics_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsQuery", []))

    @jsii.member(jsii_name="resetNameQuery")
    def reset_name_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameQuery", []))

    @jsii.member(jsii_name="resetTagsQuery")
    def reset_tags_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsQuery", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsQueryInput")
    def metrics_query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricsQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameQueryInput")
    def name_query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsQueryInput")
    def tags_query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagsQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388e9b2c7615d750837a98d900f41444bb1db72305cb674ba5726d450b8231b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="metricsQuery")
    def metrics_query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricsQuery"))

    @metrics_query.setter
    def metrics_query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf55250e0438e977dd5a71f069388f9721fd77b2cf31dc500c4b3bf72accc779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsQuery", value)

    @builtins.property
    @jsii.member(jsii_name="nameQuery")
    def name_query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameQuery"))

    @name_query.setter
    def name_query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa6c722e5394ddc49c1cfae66dea1cd8ed6bfd5902b800d1cc134b2514bdad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameQuery", value)

    @builtins.property
    @jsii.member(jsii_name="tagsQuery")
    def tags_query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagsQuery"))

    @tags_query.setter
    def tags_query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52fa3ff00453002e8d175e83d6e32b6969bb44e2ebcd748fa54e8f47829a3ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsQuery", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.dataDatadogServiceLevelObjective.DataDatadogServiceLevelObjectiveConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "metrics_query": "metricsQuery",
        "name_query": "nameQuery",
        "tags_query": "tagsQuery",
    },
)
class DataDatadogServiceLevelObjectiveConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        metrics_query: typing.Optional[builtins.str] = None,
        name_query: typing.Optional[builtins.str] = None,
        tags_query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: A SLO ID to limit the search. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#id DataDatadogServiceLevelObjective#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metrics_query: Filter results based on SLO numerator and denominator. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#metrics_query DataDatadogServiceLevelObjective#metrics_query}
        :param name_query: Filter results based on SLO names. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#name_query DataDatadogServiceLevelObjective#name_query}
        :param tags_query: Filter results based on a single SLO tag. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#tags_query DataDatadogServiceLevelObjective#tags_query}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d3f2c85aad5f520795f1f73d3f3662524715908e78a1397d3f2beff312ce01)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metrics_query", value=metrics_query, expected_type=type_hints["metrics_query"])
            check_type(argname="argument name_query", value=name_query, expected_type=type_hints["name_query"])
            check_type(argname="argument tags_query", value=tags_query, expected_type=type_hints["tags_query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if metrics_query is not None:
            self._values["metrics_query"] = metrics_query
        if name_query is not None:
            self._values["name_query"] = name_query
        if tags_query is not None:
            self._values["tags_query"] = tags_query

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
    def id(self) -> typing.Optional[builtins.str]:
        '''A SLO ID to limit the search.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#id DataDatadogServiceLevelObjective#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metrics_query(self) -> typing.Optional[builtins.str]:
        '''Filter results based on SLO numerator and denominator.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#metrics_query DataDatadogServiceLevelObjective#metrics_query}
        '''
        result = self._values.get("metrics_query")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_query(self) -> typing.Optional[builtins.str]:
        '''Filter results based on SLO names.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#name_query DataDatadogServiceLevelObjective#name_query}
        '''
        result = self._values.get("name_query")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags_query(self) -> typing.Optional[builtins.str]:
        '''Filter results based on a single SLO tag.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/d/service_level_objective#tags_query DataDatadogServiceLevelObjective#tags_query}
        '''
        result = self._values.get("tags_query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatadogServiceLevelObjectiveConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataDatadogServiceLevelObjective",
    "DataDatadogServiceLevelObjectiveConfig",
]

publication.publish()

def _typecheckingstub__e6e54c89c4645eecd050e696fde778f4b6656a35c92bc833cf935e5b3aab1fb0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    metrics_query: typing.Optional[builtins.str] = None,
    name_query: typing.Optional[builtins.str] = None,
    tags_query: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__388e9b2c7615d750837a98d900f41444bb1db72305cb674ba5726d450b8231b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf55250e0438e977dd5a71f069388f9721fd77b2cf31dc500c4b3bf72accc779(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa6c722e5394ddc49c1cfae66dea1cd8ed6bfd5902b800d1cc134b2514bdad7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fa3ff00453002e8d175e83d6e32b6969bb44e2ebcd748fa54e8f47829a3ff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d3f2c85aad5f520795f1f73d3f3662524715908e78a1397d3f2beff312ce01(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    metrics_query: typing.Optional[builtins.str] = None,
    name_query: typing.Optional[builtins.str] = None,
    tags_query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
