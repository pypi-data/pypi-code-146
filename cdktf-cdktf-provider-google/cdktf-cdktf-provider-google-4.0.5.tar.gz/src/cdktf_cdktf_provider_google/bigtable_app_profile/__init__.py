'''
# `google_bigtable_app_profile`

Refer to the Terraform Registory for docs: [`google_bigtable_app_profile`](https://www.terraform.io/docs/providers/google/r/bigtable_app_profile).
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


class BigtableAppProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableAppProfile.BigtableAppProfile",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile google_bigtable_app_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_profile_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        instance: typing.Optional[builtins.str] = None,
        multi_cluster_routing_cluster_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        multi_cluster_routing_use_any: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        single_cluster_routing: typing.Optional[typing.Union["BigtableAppProfileSingleClusterRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigtableAppProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile google_bigtable_app_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_profile_id: The unique name of the app profile in the form '[*a-zA-Z0-9][-*.a-zA-Z0-9]*'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#app_profile_id BigtableAppProfile#app_profile_id}
        :param description: Long form description of the use case for this app profile. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#description BigtableAppProfile#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#id BigtableAppProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_warnings: If true, ignore safety checks when deleting/updating the app profile. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#ignore_warnings BigtableAppProfile#ignore_warnings}
        :param instance: The name of the instance to create the app profile within. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#instance BigtableAppProfile#instance}
        :param multi_cluster_routing_cluster_ids: The set of clusters to route to. The order is ignored; clusters will be tried in order of distance. If left empty, all clusters are eligible. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#multi_cluster_routing_cluster_ids BigtableAppProfile#multi_cluster_routing_cluster_ids}
        :param multi_cluster_routing_use_any: If true, read/write requests are routed to the nearest cluster in the instance, and will fail over to the nearest cluster that is available in the event of transient errors or delays. Clusters in a region are considered equidistant. Choosing this option sacrifices read-your-writes consistency to improve availability. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#multi_cluster_routing_use_any BigtableAppProfile#multi_cluster_routing_use_any}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#project BigtableAppProfile#project}.
        :param single_cluster_routing: single_cluster_routing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#single_cluster_routing BigtableAppProfile#single_cluster_routing}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#timeouts BigtableAppProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27863197938520701b05d7a30d1fb04da983af6eba61a600310e896aed45da06)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigtableAppProfileConfig(
            app_profile_id=app_profile_id,
            description=description,
            id=id,
            ignore_warnings=ignore_warnings,
            instance=instance,
            multi_cluster_routing_cluster_ids=multi_cluster_routing_cluster_ids,
            multi_cluster_routing_use_any=multi_cluster_routing_use_any,
            project=project,
            single_cluster_routing=single_cluster_routing,
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

    @jsii.member(jsii_name="putSingleClusterRouting")
    def put_single_cluster_routing(
        self,
        *,
        cluster_id: builtins.str,
        allow_transactional_writes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cluster_id: The cluster to which read/write requests should be routed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#cluster_id BigtableAppProfile#cluster_id}
        :param allow_transactional_writes: If true, CheckAndMutateRow and ReadModifyWriteRow requests are allowed by this app profile. It is unsafe to send these requests to the same table/row/column in multiple clusters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#allow_transactional_writes BigtableAppProfile#allow_transactional_writes}
        '''
        value = BigtableAppProfileSingleClusterRouting(
            cluster_id=cluster_id,
            allow_transactional_writes=allow_transactional_writes,
        )

        return typing.cast(None, jsii.invoke(self, "putSingleClusterRouting", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#create BigtableAppProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#delete BigtableAppProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#update BigtableAppProfile#update}.
        '''
        value = BigtableAppProfileTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreWarnings")
    def reset_ignore_warnings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreWarnings", []))

    @jsii.member(jsii_name="resetInstance")
    def reset_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstance", []))

    @jsii.member(jsii_name="resetMultiClusterRoutingClusterIds")
    def reset_multi_cluster_routing_cluster_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiClusterRoutingClusterIds", []))

    @jsii.member(jsii_name="resetMultiClusterRoutingUseAny")
    def reset_multi_cluster_routing_use_any(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiClusterRoutingUseAny", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSingleClusterRouting")
    def reset_single_cluster_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleClusterRouting", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="singleClusterRouting")
    def single_cluster_routing(
        self,
    ) -> "BigtableAppProfileSingleClusterRoutingOutputReference":
        return typing.cast("BigtableAppProfileSingleClusterRoutingOutputReference", jsii.get(self, "singleClusterRouting"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigtableAppProfileTimeoutsOutputReference":
        return typing.cast("BigtableAppProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appProfileIdInput")
    def app_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreWarningsInput")
    def ignore_warnings_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreWarningsInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="multiClusterRoutingClusterIdsInput")
    def multi_cluster_routing_cluster_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "multiClusterRoutingClusterIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="multiClusterRoutingUseAnyInput")
    def multi_cluster_routing_use_any_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multiClusterRoutingUseAnyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="singleClusterRoutingInput")
    def single_cluster_routing_input(
        self,
    ) -> typing.Optional["BigtableAppProfileSingleClusterRouting"]:
        return typing.cast(typing.Optional["BigtableAppProfileSingleClusterRouting"], jsii.get(self, "singleClusterRoutingInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["BigtableAppProfileTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["BigtableAppProfileTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="appProfileId")
    def app_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appProfileId"))

    @app_profile_id.setter
    def app_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba4d94a1af53e36bdfe0f69810805a56cda1fbdda9bea981c95754f6c391ad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a996eacf5ac424f8fec8c537ae6fadb833b7e8a319704b6b83f32b8598912125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d8e83e0d57ffb8196a44a013c8862080b66e455a4a2ad8baf9e2b83196ab328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreWarnings")
    def ignore_warnings(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreWarnings"))

    @ignore_warnings.setter
    def ignore_warnings(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c267975930518764c5c4b1ee925b37007471afe457fbf869928c6294f42e6a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreWarnings", value)

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c68bbd2f9f48496ff309e30a896bd0d37cedde384299f0ba81fe966fd840587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value)

    @builtins.property
    @jsii.member(jsii_name="multiClusterRoutingClusterIds")
    def multi_cluster_routing_cluster_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "multiClusterRoutingClusterIds"))

    @multi_cluster_routing_cluster_ids.setter
    def multi_cluster_routing_cluster_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67ccb6a274cde3e5cb3476c27a59d1fc6670e3bb59bf0fdfaf17837978d881a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiClusterRoutingClusterIds", value)

    @builtins.property
    @jsii.member(jsii_name="multiClusterRoutingUseAny")
    def multi_cluster_routing_use_any(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multiClusterRoutingUseAny"))

    @multi_cluster_routing_use_any.setter
    def multi_cluster_routing_use_any(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b096bb956b8a076d0248576b2d945617a2161b6401e7ba00e1c35d571f9f25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiClusterRoutingUseAny", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c21b0896cd8890dc8a9194ad1e5273face9c4f9f54951bd5944eaef401fc74ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableAppProfile.BigtableAppProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_profile_id": "appProfileId",
        "description": "description",
        "id": "id",
        "ignore_warnings": "ignoreWarnings",
        "instance": "instance",
        "multi_cluster_routing_cluster_ids": "multiClusterRoutingClusterIds",
        "multi_cluster_routing_use_any": "multiClusterRoutingUseAny",
        "project": "project",
        "single_cluster_routing": "singleClusterRouting",
        "timeouts": "timeouts",
    },
)
class BigtableAppProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        app_profile_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        instance: typing.Optional[builtins.str] = None,
        multi_cluster_routing_cluster_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        multi_cluster_routing_use_any: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        single_cluster_routing: typing.Optional[typing.Union["BigtableAppProfileSingleClusterRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigtableAppProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_profile_id: The unique name of the app profile in the form '[*a-zA-Z0-9][-*.a-zA-Z0-9]*'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#app_profile_id BigtableAppProfile#app_profile_id}
        :param description: Long form description of the use case for this app profile. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#description BigtableAppProfile#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#id BigtableAppProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_warnings: If true, ignore safety checks when deleting/updating the app profile. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#ignore_warnings BigtableAppProfile#ignore_warnings}
        :param instance: The name of the instance to create the app profile within. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#instance BigtableAppProfile#instance}
        :param multi_cluster_routing_cluster_ids: The set of clusters to route to. The order is ignored; clusters will be tried in order of distance. If left empty, all clusters are eligible. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#multi_cluster_routing_cluster_ids BigtableAppProfile#multi_cluster_routing_cluster_ids}
        :param multi_cluster_routing_use_any: If true, read/write requests are routed to the nearest cluster in the instance, and will fail over to the nearest cluster that is available in the event of transient errors or delays. Clusters in a region are considered equidistant. Choosing this option sacrifices read-your-writes consistency to improve availability. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#multi_cluster_routing_use_any BigtableAppProfile#multi_cluster_routing_use_any}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#project BigtableAppProfile#project}.
        :param single_cluster_routing: single_cluster_routing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#single_cluster_routing BigtableAppProfile#single_cluster_routing}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#timeouts BigtableAppProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(single_cluster_routing, dict):
            single_cluster_routing = BigtableAppProfileSingleClusterRouting(**single_cluster_routing)
        if isinstance(timeouts, dict):
            timeouts = BigtableAppProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddecfaed9082652a3c38820634adbe4d134b16f8627c7867492573235e067935)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_profile_id", value=app_profile_id, expected_type=type_hints["app_profile_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_warnings", value=ignore_warnings, expected_type=type_hints["ignore_warnings"])
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument multi_cluster_routing_cluster_ids", value=multi_cluster_routing_cluster_ids, expected_type=type_hints["multi_cluster_routing_cluster_ids"])
            check_type(argname="argument multi_cluster_routing_use_any", value=multi_cluster_routing_use_any, expected_type=type_hints["multi_cluster_routing_use_any"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument single_cluster_routing", value=single_cluster_routing, expected_type=type_hints["single_cluster_routing"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_profile_id": app_profile_id,
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
        if ignore_warnings is not None:
            self._values["ignore_warnings"] = ignore_warnings
        if instance is not None:
            self._values["instance"] = instance
        if multi_cluster_routing_cluster_ids is not None:
            self._values["multi_cluster_routing_cluster_ids"] = multi_cluster_routing_cluster_ids
        if multi_cluster_routing_use_any is not None:
            self._values["multi_cluster_routing_use_any"] = multi_cluster_routing_use_any
        if project is not None:
            self._values["project"] = project
        if single_cluster_routing is not None:
            self._values["single_cluster_routing"] = single_cluster_routing
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
    def app_profile_id(self) -> builtins.str:
        '''The unique name of the app profile in the form '[*a-zA-Z0-9][-*.a-zA-Z0-9]*'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#app_profile_id BigtableAppProfile#app_profile_id}
        '''
        result = self._values.get("app_profile_id")
        assert result is not None, "Required property 'app_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Long form description of the use case for this app profile.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#description BigtableAppProfile#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#id BigtableAppProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, ignore safety checks when deleting/updating the app profile.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#ignore_warnings BigtableAppProfile#ignore_warnings}
        '''
        result = self._values.get("ignore_warnings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''The name of the instance to create the app profile within.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#instance BigtableAppProfile#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_cluster_routing_cluster_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of clusters to route to.

        The order is ignored; clusters will be tried in order of distance. If left empty, all clusters are eligible.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#multi_cluster_routing_cluster_ids BigtableAppProfile#multi_cluster_routing_cluster_ids}
        '''
        result = self._values.get("multi_cluster_routing_cluster_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def multi_cluster_routing_use_any(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, read/write requests are routed to the nearest cluster in the instance, and will fail over to the nearest cluster that is available in the event of transient errors or delays.

        Clusters in a region are considered equidistant. Choosing this option sacrifices read-your-writes
        consistency to improve availability.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#multi_cluster_routing_use_any BigtableAppProfile#multi_cluster_routing_use_any}
        '''
        result = self._values.get("multi_cluster_routing_use_any")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#project BigtableAppProfile#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_cluster_routing(
        self,
    ) -> typing.Optional["BigtableAppProfileSingleClusterRouting"]:
        '''single_cluster_routing block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#single_cluster_routing BigtableAppProfile#single_cluster_routing}
        '''
        result = self._values.get("single_cluster_routing")
        return typing.cast(typing.Optional["BigtableAppProfileSingleClusterRouting"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigtableAppProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#timeouts BigtableAppProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigtableAppProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableAppProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableAppProfile.BigtableAppProfileSingleClusterRouting",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_id": "clusterId",
        "allow_transactional_writes": "allowTransactionalWrites",
    },
)
class BigtableAppProfileSingleClusterRouting:
    def __init__(
        self,
        *,
        cluster_id: builtins.str,
        allow_transactional_writes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cluster_id: The cluster to which read/write requests should be routed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#cluster_id BigtableAppProfile#cluster_id}
        :param allow_transactional_writes: If true, CheckAndMutateRow and ReadModifyWriteRow requests are allowed by this app profile. It is unsafe to send these requests to the same table/row/column in multiple clusters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#allow_transactional_writes BigtableAppProfile#allow_transactional_writes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a833910dd152ae59642d4512e9e03b2d448cf050bcab4cffb9dd70be79fd5fa)
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument allow_transactional_writes", value=allow_transactional_writes, expected_type=type_hints["allow_transactional_writes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
        }
        if allow_transactional_writes is not None:
            self._values["allow_transactional_writes"] = allow_transactional_writes

    @builtins.property
    def cluster_id(self) -> builtins.str:
        '''The cluster to which read/write requests should be routed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#cluster_id BigtableAppProfile#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_transactional_writes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, CheckAndMutateRow and ReadModifyWriteRow requests are allowed by this app profile.

        It is unsafe to send these requests to the same table/row/column in multiple clusters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#allow_transactional_writes BigtableAppProfile#allow_transactional_writes}
        '''
        result = self._values.get("allow_transactional_writes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableAppProfileSingleClusterRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigtableAppProfileSingleClusterRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableAppProfile.BigtableAppProfileSingleClusterRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31f8c41cb369c0441145716c3f3512d444b2c05443663ac64bbd1a9badd43758)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowTransactionalWrites")
    def reset_allow_transactional_writes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowTransactionalWrites", []))

    @builtins.property
    @jsii.member(jsii_name="allowTransactionalWritesInput")
    def allow_transactional_writes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowTransactionalWritesInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="allowTransactionalWrites")
    def allow_transactional_writes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowTransactionalWrites"))

    @allow_transactional_writes.setter
    def allow_transactional_writes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec09754a1c8cffb264737b393a7e4c18161a784fae6777ceb6035b0d4e1031c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowTransactionalWrites", value)

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3aca3c4280958e3f0eae67c241b31831d323bf8938382365bb46e7df1a68e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigtableAppProfileSingleClusterRouting]:
        return typing.cast(typing.Optional[BigtableAppProfileSingleClusterRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigtableAppProfileSingleClusterRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a330880dd2381feda1727860abd0ca6e00aa00623923a68d078f471dc27269b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableAppProfile.BigtableAppProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigtableAppProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#create BigtableAppProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#delete BigtableAppProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#update BigtableAppProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c25353c7b47b312b949e2e33c9edbf2155f7a6e9f03bc8c19e5657dfea1e0e3)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#create BigtableAppProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#delete BigtableAppProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigtable_app_profile#update BigtableAppProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableAppProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigtableAppProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableAppProfile.BigtableAppProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79501d18aaed7263802a505dfe29454ad11e9b2eeb28d4d40a7d8f8d0102faa9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d98b737991b787809dbe4985a52be445c7fc1d47aa7b3f724e2844141110005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3368b1a1337649f55cb5babc5e2eee7361602415542bcc964dcc62ed3bc3fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36626487a53ca1bed9f591c1b5cefcb897368222bf73d9c8c47d2fd439f4a032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[BigtableAppProfileTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BigtableAppProfileTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BigtableAppProfileTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390e11b818538444d22ded338e8425c74082aad20913de77690a6a01f10bede3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "BigtableAppProfile",
    "BigtableAppProfileConfig",
    "BigtableAppProfileSingleClusterRouting",
    "BigtableAppProfileSingleClusterRoutingOutputReference",
    "BigtableAppProfileTimeouts",
    "BigtableAppProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__27863197938520701b05d7a30d1fb04da983af6eba61a600310e896aed45da06(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_profile_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    instance: typing.Optional[builtins.str] = None,
    multi_cluster_routing_cluster_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    multi_cluster_routing_use_any: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    single_cluster_routing: typing.Optional[typing.Union[BigtableAppProfileSingleClusterRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigtableAppProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9ba4d94a1af53e36bdfe0f69810805a56cda1fbdda9bea981c95754f6c391ad3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a996eacf5ac424f8fec8c537ae6fadb833b7e8a319704b6b83f32b8598912125(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8e83e0d57ffb8196a44a013c8862080b66e455a4a2ad8baf9e2b83196ab328(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c267975930518764c5c4b1ee925b37007471afe457fbf869928c6294f42e6a0a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c68bbd2f9f48496ff309e30a896bd0d37cedde384299f0ba81fe966fd840587(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67ccb6a274cde3e5cb3476c27a59d1fc6670e3bb59bf0fdfaf17837978d881a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b096bb956b8a076d0248576b2d945617a2161b6401e7ba00e1c35d571f9f25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21b0896cd8890dc8a9194ad1e5273face9c4f9f54951bd5944eaef401fc74ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddecfaed9082652a3c38820634adbe4d134b16f8627c7867492573235e067935(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_profile_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_warnings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    instance: typing.Optional[builtins.str] = None,
    multi_cluster_routing_cluster_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    multi_cluster_routing_use_any: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    single_cluster_routing: typing.Optional[typing.Union[BigtableAppProfileSingleClusterRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigtableAppProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a833910dd152ae59642d4512e9e03b2d448cf050bcab4cffb9dd70be79fd5fa(
    *,
    cluster_id: builtins.str,
    allow_transactional_writes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f8c41cb369c0441145716c3f3512d444b2c05443663ac64bbd1a9badd43758(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec09754a1c8cffb264737b393a7e4c18161a784fae6777ceb6035b0d4e1031c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3aca3c4280958e3f0eae67c241b31831d323bf8938382365bb46e7df1a68e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a330880dd2381feda1727860abd0ca6e00aa00623923a68d078f471dc27269b5(
    value: typing.Optional[BigtableAppProfileSingleClusterRouting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c25353c7b47b312b949e2e33c9edbf2155f7a6e9f03bc8c19e5657dfea1e0e3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79501d18aaed7263802a505dfe29454ad11e9b2eeb28d4d40a7d8f8d0102faa9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d98b737991b787809dbe4985a52be445c7fc1d47aa7b3f724e2844141110005(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3368b1a1337649f55cb5babc5e2eee7361602415542bcc964dcc62ed3bc3fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36626487a53ca1bed9f591c1b5cefcb897368222bf73d9c8c47d2fd439f4a032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390e11b818538444d22ded338e8425c74082aad20913de77690a6a01f10bede3(
    value: typing.Optional[typing.Union[BigtableAppProfileTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
