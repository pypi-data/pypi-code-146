'''
# `datadog_service_level_objective`

Refer to the Terraform Registory for docs: [`datadog_service_level_objective`](https://www.terraform.io/docs/providers/datadog/r/service_level_objective).
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


class ServiceLevelObjective(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjective",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective datadog_service_level_objective}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        thresholds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLevelObjectiveThresholds", typing.Dict[builtins.str, typing.Any]]]],
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        monitor_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        query: typing.Optional[typing.Union["ServiceLevelObjectiveQuery", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective datadog_service_level_objective} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of Datadog service level objective. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#name ServiceLevelObjective#name}
        :param thresholds: thresholds block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#thresholds ServiceLevelObjective#thresholds}
        :param type: The type of the service level objective. The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API `documentation page <https://docs.datadoghq.com/api/v1/service-level-objectives/#create-a-slo-object>`_. Valid values are ``metric``, ``monitor``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#type ServiceLevelObjective#type}
        :param description: A description of this service level objective. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#description ServiceLevelObjective#description}
        :param force_delete: A boolean indicating whether this monitor can be deleted even if it’s referenced by other resources (e.g. dashboards). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#force_delete ServiceLevelObjective#force_delete}
        :param groups: A static set of groups to filter monitor-based SLOs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#groups ServiceLevelObjective#groups}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#id ServiceLevelObjective#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param monitor_ids: A static set of monitor IDs to use as part of the SLO. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#monitor_ids ServiceLevelObjective#monitor_ids}
        :param query: query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#query ServiceLevelObjective#query}
        :param tags: A list of tags to associate with your service level objective. This can help you categorize and filter service level objectives in the service level objectives page of the UI. Note: it's not currently possible to filter by these tags when querying via the API Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#tags ServiceLevelObjective#tags}
        :param validate: Whether or not to validate the SLO. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#validate ServiceLevelObjective#validate}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5669eb7d0a788a9ff8e3d4a94593d009065ab0f39c51364f8a864ee7cee06cdb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceLevelObjectiveConfig(
            name=name,
            thresholds=thresholds,
            type=type,
            description=description,
            force_delete=force_delete,
            groups=groups,
            id=id,
            monitor_ids=monitor_ids,
            query=query,
            tags=tags,
            validate=validate,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putQuery")
    def put_query(self, *, denominator: builtins.str, numerator: builtins.str) -> None:
        '''
        :param denominator: The sum of the ``total`` events. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#denominator ServiceLevelObjective#denominator}
        :param numerator: The sum of all the ``good`` events. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#numerator ServiceLevelObjective#numerator}
        '''
        value = ServiceLevelObjectiveQuery(
            denominator=denominator, numerator=numerator
        )

        return typing.cast(None, jsii.invoke(self, "putQuery", [value]))

    @jsii.member(jsii_name="putThresholds")
    def put_thresholds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLevelObjectiveThresholds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee0511af88251ff3f841d3eea5ddfae23448ff8113c58f2442ba1d879da05cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putThresholds", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetForceDelete")
    def reset_force_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDelete", []))

    @jsii.member(jsii_name="resetGroups")
    def reset_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroups", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMonitorIds")
    def reset_monitor_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorIds", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetValidate")
    def reset_validate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidate", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> "ServiceLevelObjectiveQueryOutputReference":
        return typing.cast("ServiceLevelObjectiveQueryOutputReference", jsii.get(self, "query"))

    @builtins.property
    @jsii.member(jsii_name="thresholds")
    def thresholds(self) -> "ServiceLevelObjectiveThresholdsList":
        return typing.cast("ServiceLevelObjectiveThresholdsList", jsii.get(self, "thresholds"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDeleteInput")
    def force_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorIdsInput")
    def monitor_ids_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "monitorIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional["ServiceLevelObjectiveQuery"]:
        return typing.cast(typing.Optional["ServiceLevelObjectiveQuery"], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdsInput")
    def thresholds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveThresholds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveThresholds"]]], jsii.get(self, "thresholdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39031ab392683477559697ddae937aba45de71a24aeee6f1860bb8ded7d4a191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="forceDelete")
    def force_delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDelete"))

    @force_delete.setter
    def force_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be66be45447e983a11753a2a43dfed8f135ec6bea325e43e7f41147a746f821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDelete", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e1582c8809eacae55ab6262e514d73bd474c3a4386d4b216a68d186f6c6b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__343bb9d1720006fee8bee5d7220cd6e701cc049ee331f3658295935fdb08b50b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="monitorIds")
    def monitor_ids(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "monitorIds"))

    @monitor_ids.setter
    def monitor_ids(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b620492081cf94a200a179acd0ec1d18cca903c91fbbca92b6ebdb36dab24f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorIds", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d059cc07aef428d6b75797df742892160cb0478a746367237d856810e41af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ac89e98ad2f05f3ce61005b9732c79759b2a629e1dae672e4f481801805b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f84ca6c2b8ce36ac1f21df52416dbdfadad39016d5620908a0f69f7cdac9710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validate"))

    @validate.setter
    def validate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8c766fdd59364dc581779f7e3153bb8b804e3502fffcda0db5fd026afa27ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validate", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "thresholds": "thresholds",
        "type": "type",
        "description": "description",
        "force_delete": "forceDelete",
        "groups": "groups",
        "id": "id",
        "monitor_ids": "monitorIds",
        "query": "query",
        "tags": "tags",
        "validate": "validate",
    },
)
class ServiceLevelObjectiveConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        thresholds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLevelObjectiveThresholds", typing.Dict[builtins.str, typing.Any]]]],
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        monitor_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
        query: typing.Optional[typing.Union["ServiceLevelObjectiveQuery", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of Datadog service level objective. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#name ServiceLevelObjective#name}
        :param thresholds: thresholds block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#thresholds ServiceLevelObjective#thresholds}
        :param type: The type of the service level objective. The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API `documentation page <https://docs.datadoghq.com/api/v1/service-level-objectives/#create-a-slo-object>`_. Valid values are ``metric``, ``monitor``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#type ServiceLevelObjective#type}
        :param description: A description of this service level objective. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#description ServiceLevelObjective#description}
        :param force_delete: A boolean indicating whether this monitor can be deleted even if it’s referenced by other resources (e.g. dashboards). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#force_delete ServiceLevelObjective#force_delete}
        :param groups: A static set of groups to filter monitor-based SLOs. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#groups ServiceLevelObjective#groups}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#id ServiceLevelObjective#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param monitor_ids: A static set of monitor IDs to use as part of the SLO. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#monitor_ids ServiceLevelObjective#monitor_ids}
        :param query: query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#query ServiceLevelObjective#query}
        :param tags: A list of tags to associate with your service level objective. This can help you categorize and filter service level objectives in the service level objectives page of the UI. Note: it's not currently possible to filter by these tags when querying via the API Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#tags ServiceLevelObjective#tags}
        :param validate: Whether or not to validate the SLO. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#validate ServiceLevelObjective#validate}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(query, dict):
            query = ServiceLevelObjectiveQuery(**query)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0a882d3049307ffc9d9cb776c8bc8d93f7c9d9482c4275c660dbe2be37fb18)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument thresholds", value=thresholds, expected_type=type_hints["thresholds"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument monitor_ids", value=monitor_ids, expected_type=type_hints["monitor_ids"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument validate", value=validate, expected_type=type_hints["validate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "thresholds": thresholds,
            "type": type,
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
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if groups is not None:
            self._values["groups"] = groups
        if id is not None:
            self._values["id"] = id
        if monitor_ids is not None:
            self._values["monitor_ids"] = monitor_ids
        if query is not None:
            self._values["query"] = query
        if tags is not None:
            self._values["tags"] = tags
        if validate is not None:
            self._values["validate"] = validate

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
    def name(self) -> builtins.str:
        '''Name of Datadog service level objective.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#name ServiceLevelObjective#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def thresholds(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveThresholds"]]:
        '''thresholds block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#thresholds ServiceLevelObjective#thresholds}
        '''
        result = self._values.get("thresholds")
        assert result is not None, "Required property 'thresholds' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLevelObjectiveThresholds"]], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the service level objective.

        The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API `documentation page <https://docs.datadoghq.com/api/v1/service-level-objectives/#create-a-slo-object>`_. Valid values are ``metric``, ``monitor``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#type ServiceLevelObjective#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this service level objective.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#description ServiceLevelObjective#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A boolean indicating whether this monitor can be deleted even if it’s referenced by other resources (e.g. dashboards).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#force_delete ServiceLevelObjective#force_delete}
        '''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A static set of groups to filter monitor-based SLOs.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#groups ServiceLevelObjective#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#id ServiceLevelObjective#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_ids(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''A static set of monitor IDs to use as part of the SLO.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#monitor_ids ServiceLevelObjective#monitor_ids}
        '''
        result = self._values.get("monitor_ids")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def query(self) -> typing.Optional["ServiceLevelObjectiveQuery"]:
        '''query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#query ServiceLevelObjective#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional["ServiceLevelObjectiveQuery"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tags to associate with your service level objective.

        This can help you categorize and filter service level objectives in the service level objectives page of the UI. Note: it's not currently possible to filter by these tags when querying via the API

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#tags ServiceLevelObjective#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def validate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not to validate the SLO.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#validate ServiceLevelObjective#validate}
        '''
        result = self._values.get("validate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveQuery",
    jsii_struct_bases=[],
    name_mapping={"denominator": "denominator", "numerator": "numerator"},
)
class ServiceLevelObjectiveQuery:
    def __init__(self, *, denominator: builtins.str, numerator: builtins.str) -> None:
        '''
        :param denominator: The sum of the ``total`` events. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#denominator ServiceLevelObjective#denominator}
        :param numerator: The sum of all the ``good`` events. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#numerator ServiceLevelObjective#numerator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268e427658d3899ed81ea172f685c0cee60658032a0441d2aa0184c1e8b51c42)
            check_type(argname="argument denominator", value=denominator, expected_type=type_hints["denominator"])
            check_type(argname="argument numerator", value=numerator, expected_type=type_hints["numerator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "denominator": denominator,
            "numerator": numerator,
        }

    @builtins.property
    def denominator(self) -> builtins.str:
        '''The sum of the ``total`` events.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#denominator ServiceLevelObjective#denominator}
        '''
        result = self._values.get("denominator")
        assert result is not None, "Required property 'denominator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def numerator(self) -> builtins.str:
        '''The sum of all the ``good`` events.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#numerator ServiceLevelObjective#numerator}
        '''
        result = self._values.get("numerator")
        assert result is not None, "Required property 'numerator' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__948c92f863d870165d686218a2d822ea36ebb8a4f0e54b9f6650800d78e25af2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="denominatorInput")
    def denominator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "denominatorInput"))

    @builtins.property
    @jsii.member(jsii_name="numeratorInput")
    def numerator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "numeratorInput"))

    @builtins.property
    @jsii.member(jsii_name="denominator")
    def denominator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "denominator"))

    @denominator.setter
    def denominator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568d34e5d5567f6262fe2ddb2b0fc7c52f21c63b9c69b1e521cb95ceeb704e29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "denominator", value)

    @builtins.property
    @jsii.member(jsii_name="numerator")
    def numerator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "numerator"))

    @numerator.setter
    def numerator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee039ac7735b0e9d3480fe92c2b851b92b1dec39b3570be3dbbc61163f9b09bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numerator", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceLevelObjectiveQuery]:
        return typing.cast(typing.Optional[ServiceLevelObjectiveQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceLevelObjectiveQuery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4008a8ababe5e2b3440b456ca2274d7187a3aaa582a19257d8d87740f7fb68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveThresholds",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "timeframe": "timeframe", "warning": "warning"},
)
class ServiceLevelObjectiveThresholds:
    def __init__(
        self,
        *,
        target: jsii.Number,
        timeframe: builtins.str,
        warning: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target: The objective's target in``[0,100]``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#target ServiceLevelObjective#target}
        :param timeframe: The time frame for the objective. The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API documentation page. Valid values are ``7d``, ``30d``, ``90d``, ``custom``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#timeframe ServiceLevelObjective#timeframe}
        :param warning: The objective's warning value in ``[0,100]``. This must be greater than the target value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#warning ServiceLevelObjective#warning}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708fb67636caab56311bbb3038cac267a56a064003dfa3c0a8eb18ed80f260db)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument timeframe", value=timeframe, expected_type=type_hints["timeframe"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
            "timeframe": timeframe,
        }
        if warning is not None:
            self._values["warning"] = warning

    @builtins.property
    def target(self) -> jsii.Number:
        '''The objective's target in``[0,100]``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#target ServiceLevelObjective#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def timeframe(self) -> builtins.str:
        '''The time frame for the objective.

        The mapping from these types to the types found in the Datadog Web UI can be found in the Datadog API documentation page. Valid values are ``7d``, ``30d``, ``90d``, ``custom``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#timeframe ServiceLevelObjective#timeframe}
        '''
        result = self._values.get("timeframe")
        assert result is not None, "Required property 'timeframe' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def warning(self) -> typing.Optional[jsii.Number]:
        '''The objective's warning value in ``[0,100]``. This must be greater than the target value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/datadog/r/service_level_objective#warning ServiceLevelObjective#warning}
        '''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLevelObjectiveThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLevelObjectiveThresholdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveThresholdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10bae5ad06a4cc14c9785d193dee23f14166e1cd064ecd9f65db1de50f2d475c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceLevelObjectiveThresholdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2457d740e602f90234fc0792d09948873f207d015b3d5a61fb40f8ca432c280)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceLevelObjectiveThresholdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe2801235acef66be7304bbc8e64c524858f07ff3bcc4e2cca40a81f4c49c83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__709e17a06465337b2e143a3554798620bd8194f96ec05ad03e9ae4409044d66d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cea3c1a886a7d5504f55b05582f49064a3db93548381357683d38ea4272a1826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveThresholds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveThresholds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveThresholds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e440c67b79888a615dc177d1e0ab34011448230699b02011ad660663a7281937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ServiceLevelObjectiveThresholdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.serviceLevelObjective.ServiceLevelObjectiveThresholdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2895a3f729396c9ee63ac73a5449707ed2c9b6c639b356eda51187c1f0d64f3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetWarning")
    def reset_warning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarning", []))

    @builtins.property
    @jsii.member(jsii_name="targetDisplay")
    def target_display(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetDisplay"))

    @builtins.property
    @jsii.member(jsii_name="warningDisplay")
    def warning_display(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warningDisplay"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeframeInput")
    def timeframe_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeframeInput"))

    @builtins.property
    @jsii.member(jsii_name="warningInput")
    def warning_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "warningInput"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8827b9c81c1133d50084136c83bf1237767f26d8bc25ee61c33d9a941610f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)

    @builtins.property
    @jsii.member(jsii_name="timeframe")
    def timeframe(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeframe"))

    @timeframe.setter
    def timeframe(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a04afe1ff2379ca673330d58dba4ffe3fd345c187cee7f13b7fcae389b2c676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeframe", value)

    @builtins.property
    @jsii.member(jsii_name="warning")
    def warning(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "warning"))

    @warning.setter
    def warning(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3dacb7b155ac13089cbc9eeb17a38c6e1b463a513342fdd58f3a51dfe79ee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warning", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ServiceLevelObjectiveThresholds, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ServiceLevelObjectiveThresholds, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ServiceLevelObjectiveThresholds, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4132001a03036d397b5948c2ad78e307bfb4015fa93750ffb3a1b41901f740ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ServiceLevelObjective",
    "ServiceLevelObjectiveConfig",
    "ServiceLevelObjectiveQuery",
    "ServiceLevelObjectiveQueryOutputReference",
    "ServiceLevelObjectiveThresholds",
    "ServiceLevelObjectiveThresholdsList",
    "ServiceLevelObjectiveThresholdsOutputReference",
]

publication.publish()

def _typecheckingstub__5669eb7d0a788a9ff8e3d4a94593d009065ab0f39c51364f8a864ee7cee06cdb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    thresholds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLevelObjectiveThresholds, typing.Dict[builtins.str, typing.Any]]]],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    monitor_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    query: typing.Optional[typing.Union[ServiceLevelObjectiveQuery, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__eee0511af88251ff3f841d3eea5ddfae23448ff8113c58f2442ba1d879da05cb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLevelObjectiveThresholds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39031ab392683477559697ddae937aba45de71a24aeee6f1860bb8ded7d4a191(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be66be45447e983a11753a2a43dfed8f135ec6bea325e43e7f41147a746f821(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e1582c8809eacae55ab6262e514d73bd474c3a4386d4b216a68d186f6c6b6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343bb9d1720006fee8bee5d7220cd6e701cc049ee331f3658295935fdb08b50b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b620492081cf94a200a179acd0ec1d18cca903c91fbbca92b6ebdb36dab24f09(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d059cc07aef428d6b75797df742892160cb0478a746367237d856810e41af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ac89e98ad2f05f3ce61005b9732c79759b2a629e1dae672e4f481801805b69(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f84ca6c2b8ce36ac1f21df52416dbdfadad39016d5620908a0f69f7cdac9710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8c766fdd59364dc581779f7e3153bb8b804e3502fffcda0db5fd026afa27ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0a882d3049307ffc9d9cb776c8bc8d93f7c9d9482c4275c660dbe2be37fb18(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    thresholds: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLevelObjectiveThresholds, typing.Dict[builtins.str, typing.Any]]]],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    monitor_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    query: typing.Optional[typing.Union[ServiceLevelObjectiveQuery, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268e427658d3899ed81ea172f685c0cee60658032a0441d2aa0184c1e8b51c42(
    *,
    denominator: builtins.str,
    numerator: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948c92f863d870165d686218a2d822ea36ebb8a4f0e54b9f6650800d78e25af2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568d34e5d5567f6262fe2ddb2b0fc7c52f21c63b9c69b1e521cb95ceeb704e29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee039ac7735b0e9d3480fe92c2b851b92b1dec39b3570be3dbbc61163f9b09bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4008a8ababe5e2b3440b456ca2274d7187a3aaa582a19257d8d87740f7fb68f(
    value: typing.Optional[ServiceLevelObjectiveQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708fb67636caab56311bbb3038cac267a56a064003dfa3c0a8eb18ed80f260db(
    *,
    target: jsii.Number,
    timeframe: builtins.str,
    warning: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bae5ad06a4cc14c9785d193dee23f14166e1cd064ecd9f65db1de50f2d475c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2457d740e602f90234fc0792d09948873f207d015b3d5a61fb40f8ca432c280(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe2801235acef66be7304bbc8e64c524858f07ff3bcc4e2cca40a81f4c49c83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709e17a06465337b2e143a3554798620bd8194f96ec05ad03e9ae4409044d66d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea3c1a886a7d5504f55b05582f49064a3db93548381357683d38ea4272a1826(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e440c67b79888a615dc177d1e0ab34011448230699b02011ad660663a7281937(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLevelObjectiveThresholds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2895a3f729396c9ee63ac73a5449707ed2c9b6c639b356eda51187c1f0d64f3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8827b9c81c1133d50084136c83bf1237767f26d8bc25ee61c33d9a941610f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a04afe1ff2379ca673330d58dba4ffe3fd345c187cee7f13b7fcae389b2c676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3dacb7b155ac13089cbc9eeb17a38c6e1b463a513342fdd58f3a51dfe79ee2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4132001a03036d397b5948c2ad78e307bfb4015fa93750ffb3a1b41901f740ad(
    value: typing.Optional[typing.Union[ServiceLevelObjectiveThresholds, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
