'''
# `google_network_management_connectivity_test`

Refer to the Terraform Registory for docs: [`google_network_management_connectivity_test`](https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test).
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


class NetworkManagementConnectivityTest(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkManagementConnectivityTest.NetworkManagementConnectivityTest",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test google_network_management_connectivity_test}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination: typing.Union["NetworkManagementConnectivityTestDestination", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        source: typing.Union["NetworkManagementConnectivityTestSource", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        related_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["NetworkManagementConnectivityTestTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test google_network_management_connectivity_test} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination: destination block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#destination NetworkManagementConnectivityTest#destination}
        :param name: Unique name for the connectivity test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#name NetworkManagementConnectivityTest#name}
        :param source: source block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#source NetworkManagementConnectivityTest#source}
        :param description: The user-supplied description of the Connectivity Test. Maximum of 512 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#description NetworkManagementConnectivityTest#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#id NetworkManagementConnectivityTest#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user-provided metadata. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#labels NetworkManagementConnectivityTest#labels}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#project NetworkManagementConnectivityTest#project}.
        :param protocol: IP Protocol of the test. When not provided, "TCP" is assumed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#protocol NetworkManagementConnectivityTest#protocol}
        :param related_projects: Other projects that may be relevant for reachability analysis. This is applicable to scenarios where a test can cross project boundaries. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#related_projects NetworkManagementConnectivityTest#related_projects}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#timeouts NetworkManagementConnectivityTest#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec78ab3b0defbf5d7044d46b0ebe1135081cf08fdfe2e8b1100400f5a886012)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkManagementConnectivityTestConfig(
            destination=destination,
            name=name,
            source=source,
            description=description,
            id=id,
            labels=labels,
            project=project,
            protocol=protocol,
            related_projects=related_projects,
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

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: A Compute Engine instance URI. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#instance NetworkManagementConnectivityTest#instance}
        :param ip_address: The IP address of the endpoint, which can be an external or internal IP. An IPv6 address is only allowed when the test's destination is a global load balancer VIP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#ip_address NetworkManagementConnectivityTest#ip_address}
        :param network: A Compute Engine network URI. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#network NetworkManagementConnectivityTest#network}
        :param port: The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#port NetworkManagementConnectivityTest#port}
        :param project_id: Project ID where the endpoint is located. The Project ID can be derived from the URI if you provide a VM instance or network URI. The following are two cases where you must provide the project ID: 1. Only the IP address is specified, and the IP address is within a GCP project. 2. When you are using Shared VPC and the IP address that you provide is from the service project. In this case, the network that the IP address resides in is defined in the host project. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#project_id NetworkManagementConnectivityTest#project_id}
        '''
        value = NetworkManagementConnectivityTestDestination(
            instance=instance,
            ip_address=ip_address,
            network=network,
            port=port,
            project_id=project_id,
        )

        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: A Compute Engine instance URI. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#instance NetworkManagementConnectivityTest#instance}
        :param ip_address: The IP address of the endpoint, which can be an external or internal IP. An IPv6 address is only allowed when the test's destination is a global load balancer VIP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#ip_address NetworkManagementConnectivityTest#ip_address}
        :param network: A Compute Engine network URI. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#network NetworkManagementConnectivityTest#network}
        :param network_type: Type of the network where the endpoint is located. Possible values: ["GCP_NETWORK", "NON_GCP_NETWORK"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#network_type NetworkManagementConnectivityTest#network_type}
        :param port: The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#port NetworkManagementConnectivityTest#port}
        :param project_id: Project ID where the endpoint is located. The Project ID can be derived from the URI if you provide a VM instance or network URI. The following are two cases where you must provide the project ID: 1. Only the IP address is specified, and the IP address is within a GCP project. 2. When you are using Shared VPC and the IP address that you provide is from the service project. In this case, the network that the IP address resides in is defined in the host project. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#project_id NetworkManagementConnectivityTest#project_id}
        '''
        value = NetworkManagementConnectivityTestSource(
            instance=instance,
            ip_address=ip_address,
            network=network,
            network_type=network_type,
            port=port,
            project_id=project_id,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#create NetworkManagementConnectivityTest#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#delete NetworkManagementConnectivityTest#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#update NetworkManagementConnectivityTest#update}.
        '''
        value = NetworkManagementConnectivityTestTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetRelatedProjects")
    def reset_related_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelatedProjects", []))

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
    @jsii.member(jsii_name="destination")
    def destination(
        self,
    ) -> "NetworkManagementConnectivityTestDestinationOutputReference":
        return typing.cast("NetworkManagementConnectivityTestDestinationOutputReference", jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "NetworkManagementConnectivityTestSourceOutputReference":
        return typing.cast("NetworkManagementConnectivityTestSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkManagementConnectivityTestTimeoutsOutputReference":
        return typing.cast("NetworkManagementConnectivityTestTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(
        self,
    ) -> typing.Optional["NetworkManagementConnectivityTestDestination"]:
        return typing.cast(typing.Optional["NetworkManagementConnectivityTestDestination"], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="relatedProjectsInput")
    def related_projects_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "relatedProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["NetworkManagementConnectivityTestSource"]:
        return typing.cast(typing.Optional["NetworkManagementConnectivityTestSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["NetworkManagementConnectivityTestTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["NetworkManagementConnectivityTestTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39c38766fe20a7c3aae036a626eab534f394d46944e63011be66de31617aff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec6f9372db41096eab0be9691400f1cfcb56b83861c13ba65e28922b266155f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e02db07cdef4231a202703807500a7bf5536cce0e46fcb99dbd4f1aeda0f599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996c2d979e3c05bf3c41a3cc9c56250921c34670c1aa9f289a39afc1adc2206b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a542ac4045883c0bc8800685ab047ff8b67864bfc84f659085f214158b789cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d744fa4c3e755bb2dfe3cc3b06fbe59792ac8d2a83330be7919d9ee52bcfff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="relatedProjects")
    def related_projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "relatedProjects"))

    @related_projects.setter
    def related_projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50bdedbf16a0e4cc2f5da2ff6de984861ad630ca0d65352bad1d1008288eb5e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relatedProjects", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkManagementConnectivityTest.NetworkManagementConnectivityTestConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination": "destination",
        "name": "name",
        "source": "source",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "protocol": "protocol",
        "related_projects": "relatedProjects",
        "timeouts": "timeouts",
    },
)
class NetworkManagementConnectivityTestConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination: typing.Union["NetworkManagementConnectivityTestDestination", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        source: typing.Union["NetworkManagementConnectivityTestSource", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        related_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["NetworkManagementConnectivityTestTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination: destination block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#destination NetworkManagementConnectivityTest#destination}
        :param name: Unique name for the connectivity test. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#name NetworkManagementConnectivityTest#name}
        :param source: source block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#source NetworkManagementConnectivityTest#source}
        :param description: The user-supplied description of the Connectivity Test. Maximum of 512 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#description NetworkManagementConnectivityTest#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#id NetworkManagementConnectivityTest#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user-provided metadata. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#labels NetworkManagementConnectivityTest#labels}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#project NetworkManagementConnectivityTest#project}.
        :param protocol: IP Protocol of the test. When not provided, "TCP" is assumed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#protocol NetworkManagementConnectivityTest#protocol}
        :param related_projects: Other projects that may be relevant for reachability analysis. This is applicable to scenarios where a test can cross project boundaries. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#related_projects NetworkManagementConnectivityTest#related_projects}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#timeouts NetworkManagementConnectivityTest#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination, dict):
            destination = NetworkManagementConnectivityTestDestination(**destination)
        if isinstance(source, dict):
            source = NetworkManagementConnectivityTestSource(**source)
        if isinstance(timeouts, dict):
            timeouts = NetworkManagementConnectivityTestTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b265d0d528dd87040b6895af56f862a584ccba2465d42447f8b9b01ac48ad77)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument related_projects", value=related_projects, expected_type=type_hints["related_projects"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "name": name,
            "source": source,
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
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if protocol is not None:
            self._values["protocol"] = protocol
        if related_projects is not None:
            self._values["related_projects"] = related_projects
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
    def destination(self) -> "NetworkManagementConnectivityTestDestination":
        '''destination block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#destination NetworkManagementConnectivityTest#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("NetworkManagementConnectivityTestDestination", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Unique name for the connectivity test.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#name NetworkManagementConnectivityTest#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> "NetworkManagementConnectivityTestSource":
        '''source block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#source NetworkManagementConnectivityTest#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("NetworkManagementConnectivityTestSource", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The user-supplied description of the Connectivity Test. Maximum of 512 characters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#description NetworkManagementConnectivityTest#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#id NetworkManagementConnectivityTest#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource labels to represent user-provided metadata.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#labels NetworkManagementConnectivityTest#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#project NetworkManagementConnectivityTest#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''IP Protocol of the test. When not provided, "TCP" is assumed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#protocol NetworkManagementConnectivityTest#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def related_projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Other projects that may be relevant for reachability analysis. This is applicable to scenarios where a test can cross project boundaries.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#related_projects NetworkManagementConnectivityTest#related_projects}
        '''
        result = self._values.get("related_projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkManagementConnectivityTestTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#timeouts NetworkManagementConnectivityTest#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkManagementConnectivityTestTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkManagementConnectivityTestConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkManagementConnectivityTest.NetworkManagementConnectivityTestDestination",
    jsii_struct_bases=[],
    name_mapping={
        "instance": "instance",
        "ip_address": "ipAddress",
        "network": "network",
        "port": "port",
        "project_id": "projectId",
    },
)
class NetworkManagementConnectivityTestDestination:
    def __init__(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: A Compute Engine instance URI. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#instance NetworkManagementConnectivityTest#instance}
        :param ip_address: The IP address of the endpoint, which can be an external or internal IP. An IPv6 address is only allowed when the test's destination is a global load balancer VIP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#ip_address NetworkManagementConnectivityTest#ip_address}
        :param network: A Compute Engine network URI. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#network NetworkManagementConnectivityTest#network}
        :param port: The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#port NetworkManagementConnectivityTest#port}
        :param project_id: Project ID where the endpoint is located. The Project ID can be derived from the URI if you provide a VM instance or network URI. The following are two cases where you must provide the project ID: 1. Only the IP address is specified, and the IP address is within a GCP project. 2. When you are using Shared VPC and the IP address that you provide is from the service project. In this case, the network that the IP address resides in is defined in the host project. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#project_id NetworkManagementConnectivityTest#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1e8beaa6b24a58d6d898e8fcb08ccf92d06e23e107c48770ee290a4ef291fd)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance is not None:
            self._values["instance"] = instance
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if network is not None:
            self._values["network"] = network
        if port is not None:
            self._values["port"] = port
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''A Compute Engine instance URI.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#instance NetworkManagementConnectivityTest#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''The IP address of the endpoint, which can be an external or internal IP.

        An IPv6 address is only allowed when the test's
        destination is a global load balancer VIP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#ip_address NetworkManagementConnectivityTest#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''A Compute Engine network URI.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#network NetworkManagementConnectivityTest#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#port NetworkManagementConnectivityTest#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Project ID where the endpoint is located.

        The Project ID can be
        derived from the URI if you provide a VM instance or network URI.
        The following are two cases where you must provide the project ID:

        1. Only the IP address is specified, and the IP address is within
           a GCP project. 2. When you are using Shared VPC and the IP address
           that you provide is from the service project. In this case, the
           network that the IP address resides in is defined in the host
           project.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#project_id NetworkManagementConnectivityTest#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkManagementConnectivityTestDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkManagementConnectivityTestDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkManagementConnectivityTest.NetworkManagementConnectivityTestDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1eb22bf7355b52c4ed6ed751a491b896fd8689d07a920d4ecf0d82a9b7be49ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstance")
    def reset_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstance", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c595aca3c8fc49ec027c1758d9e7106334f625e24e14b8008b464acc450939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1099553e5061f99e3d17b5416afcbe1971c30b14b5135e8984ab6713e851c8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94260fad99a5f208c213e630e76635602d7739ff2c8e9970a565e0c80851acd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212489f562ab0a0ca04af5d04056d0a169d9218bfcdf62869917b8dcc618ef1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c577a2218738ab55078279bc3746887c19d93b39680b01effb5850f4a3fe23f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkManagementConnectivityTestDestination]:
        return typing.cast(typing.Optional[NetworkManagementConnectivityTestDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkManagementConnectivityTestDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4643de4bc3d1e2f9786adeaa571dc029164dcbd8b9cefda92674b399ae50dc0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkManagementConnectivityTest.NetworkManagementConnectivityTestSource",
    jsii_struct_bases=[],
    name_mapping={
        "instance": "instance",
        "ip_address": "ipAddress",
        "network": "network",
        "network_type": "networkType",
        "port": "port",
        "project_id": "projectId",
    },
)
class NetworkManagementConnectivityTestSource:
    def __init__(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: A Compute Engine instance URI. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#instance NetworkManagementConnectivityTest#instance}
        :param ip_address: The IP address of the endpoint, which can be an external or internal IP. An IPv6 address is only allowed when the test's destination is a global load balancer VIP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#ip_address NetworkManagementConnectivityTest#ip_address}
        :param network: A Compute Engine network URI. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#network NetworkManagementConnectivityTest#network}
        :param network_type: Type of the network where the endpoint is located. Possible values: ["GCP_NETWORK", "NON_GCP_NETWORK"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#network_type NetworkManagementConnectivityTest#network_type}
        :param port: The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#port NetworkManagementConnectivityTest#port}
        :param project_id: Project ID where the endpoint is located. The Project ID can be derived from the URI if you provide a VM instance or network URI. The following are two cases where you must provide the project ID: 1. Only the IP address is specified, and the IP address is within a GCP project. 2. When you are using Shared VPC and the IP address that you provide is from the service project. In this case, the network that the IP address resides in is defined in the host project. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#project_id NetworkManagementConnectivityTest#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9992e1b7bd475e625920bf34a9337fa85f066ded0a8746dcc049cb3e3949f960)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance is not None:
            self._values["instance"] = instance
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if network is not None:
            self._values["network"] = network
        if network_type is not None:
            self._values["network_type"] = network_type
        if port is not None:
            self._values["port"] = port
        if project_id is not None:
            self._values["project_id"] = project_id

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''A Compute Engine instance URI.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#instance NetworkManagementConnectivityTest#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''The IP address of the endpoint, which can be an external or internal IP.

        An IPv6 address is only allowed when the test's
        destination is a global load balancer VIP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#ip_address NetworkManagementConnectivityTest#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''A Compute Engine network URI.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#network NetworkManagementConnectivityTest#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Type of the network where the endpoint is located. Possible values: ["GCP_NETWORK", "NON_GCP_NETWORK"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#network_type NetworkManagementConnectivityTest#network_type}
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The IP protocol port of the endpoint. Only applicable when protocol is TCP or UDP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#port NetworkManagementConnectivityTest#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Project ID where the endpoint is located.

        The Project ID can be
        derived from the URI if you provide a VM instance or network URI.
        The following are two cases where you must provide the project ID:

        1. Only the IP address is specified, and the IP address is
           within a GCP project.
        2. When you are using Shared VPC and the IP address
           that you provide is from the service project. In this case,
           the network that the IP address resides in is defined in the
           host project.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#project_id NetworkManagementConnectivityTest#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkManagementConnectivityTestSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkManagementConnectivityTestSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkManagementConnectivityTest.NetworkManagementConnectivityTestSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12f71c8e53aaedee02f07ac2197c8c1162d0c3253a0325ec94d7efcace2ee7f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstance")
    def reset_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstance", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNetworkType")
    def reset_network_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkType", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTypeInput")
    def network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a290ca90ac8ee83ee5e3f4dd97c550aa9bf7d80a9bcf8ea546f663012a39360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f54a0ae9e35214c008755cdf6ac0585cbbd84851ff4884ce4825cfcf2d926a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86ed6f75e75bba6ffb0212c7967fb298324f6929df4f1f35910dc157c11ed10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value)

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3b812d0521866084be94b3686cb8de70fa68c5eae44e9292c7887780764c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c19e6f76d5bde3e950170d07834b78a9e3eac02e4ec1a2b6f14ca6bf88fc092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bd733e24144856b3582fa0f643aee6fdd6e39f63fafa1aa56bd472fa9c48ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkManagementConnectivityTestSource]:
        return typing.cast(typing.Optional[NetworkManagementConnectivityTestSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkManagementConnectivityTestSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3a5196a98833b5b1e414f1c8b21b36ba83032b4969e858e5770a13879bbc52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkManagementConnectivityTest.NetworkManagementConnectivityTestTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkManagementConnectivityTestTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#create NetworkManagementConnectivityTest#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#delete NetworkManagementConnectivityTest#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#update NetworkManagementConnectivityTest#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5679f7128f2e86a1bd9704cdcfc1e04c799d84cef5fcc59e8277c0730a05624d)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#create NetworkManagementConnectivityTest#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#delete NetworkManagementConnectivityTest#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/network_management_connectivity_test#update NetworkManagementConnectivityTest#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkManagementConnectivityTestTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkManagementConnectivityTestTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkManagementConnectivityTest.NetworkManagementConnectivityTestTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b327905feb625e4b5d495dbdd797a0f9030aaec63063175fc292e35faf80dc87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78e53e53d4bf77b301257a6c47067618283a798c98a3090ed2b3038920e92608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108683189140639cfb6ec5b39522d867862e1806a38d146af5b6d1e05fed5de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e089f17bec712acc43f8ffe9c6c57339ec8f8e13c0c773aef923239330ca8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[NetworkManagementConnectivityTestTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[NetworkManagementConnectivityTestTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[NetworkManagementConnectivityTestTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65601acb556602e4d91c960c7c6ec06f6ec983fbe9aa8bb1f9417b4c9648e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NetworkManagementConnectivityTest",
    "NetworkManagementConnectivityTestConfig",
    "NetworkManagementConnectivityTestDestination",
    "NetworkManagementConnectivityTestDestinationOutputReference",
    "NetworkManagementConnectivityTestSource",
    "NetworkManagementConnectivityTestSourceOutputReference",
    "NetworkManagementConnectivityTestTimeouts",
    "NetworkManagementConnectivityTestTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dec78ab3b0defbf5d7044d46b0ebe1135081cf08fdfe2e8b1100400f5a886012(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination: typing.Union[NetworkManagementConnectivityTestDestination, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    source: typing.Union[NetworkManagementConnectivityTestSource, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    related_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[NetworkManagementConnectivityTestTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c39c38766fe20a7c3aae036a626eab534f394d46944e63011be66de31617aff7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec6f9372db41096eab0be9691400f1cfcb56b83861c13ba65e28922b266155f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e02db07cdef4231a202703807500a7bf5536cce0e46fcb99dbd4f1aeda0f599(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996c2d979e3c05bf3c41a3cc9c56250921c34670c1aa9f289a39afc1adc2206b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a542ac4045883c0bc8800685ab047ff8b67864bfc84f659085f214158b789cdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d744fa4c3e755bb2dfe3cc3b06fbe59792ac8d2a83330be7919d9ee52bcfff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50bdedbf16a0e4cc2f5da2ff6de984861ad630ca0d65352bad1d1008288eb5e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b265d0d528dd87040b6895af56f862a584ccba2465d42447f8b9b01ac48ad77(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination: typing.Union[NetworkManagementConnectivityTestDestination, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    source: typing.Union[NetworkManagementConnectivityTestSource, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    related_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[NetworkManagementConnectivityTestTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1e8beaa6b24a58d6d898e8fcb08ccf92d06e23e107c48770ee290a4ef291fd(
    *,
    instance: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb22bf7355b52c4ed6ed751a491b896fd8689d07a920d4ecf0d82a9b7be49ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c595aca3c8fc49ec027c1758d9e7106334f625e24e14b8008b464acc450939(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1099553e5061f99e3d17b5416afcbe1971c30b14b5135e8984ab6713e851c8f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94260fad99a5f208c213e630e76635602d7739ff2c8e9970a565e0c80851acd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212489f562ab0a0ca04af5d04056d0a169d9218bfcdf62869917b8dcc618ef1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c577a2218738ab55078279bc3746887c19d93b39680b01effb5850f4a3fe23f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4643de4bc3d1e2f9786adeaa571dc029164dcbd8b9cefda92674b399ae50dc0c(
    value: typing.Optional[NetworkManagementConnectivityTestDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9992e1b7bd475e625920bf34a9337fa85f066ded0a8746dcc049cb3e3949f960(
    *,
    instance: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f71c8e53aaedee02f07ac2197c8c1162d0c3253a0325ec94d7efcace2ee7f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a290ca90ac8ee83ee5e3f4dd97c550aa9bf7d80a9bcf8ea546f663012a39360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f54a0ae9e35214c008755cdf6ac0585cbbd84851ff4884ce4825cfcf2d926a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86ed6f75e75bba6ffb0212c7967fb298324f6929df4f1f35910dc157c11ed10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3b812d0521866084be94b3686cb8de70fa68c5eae44e9292c7887780764c36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c19e6f76d5bde3e950170d07834b78a9e3eac02e4ec1a2b6f14ca6bf88fc092(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bd733e24144856b3582fa0f643aee6fdd6e39f63fafa1aa56bd472fa9c48ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3a5196a98833b5b1e414f1c8b21b36ba83032b4969e858e5770a13879bbc52(
    value: typing.Optional[NetworkManagementConnectivityTestSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5679f7128f2e86a1bd9704cdcfc1e04c799d84cef5fcc59e8277c0730a05624d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b327905feb625e4b5d495dbdd797a0f9030aaec63063175fc292e35faf80dc87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e53e53d4bf77b301257a6c47067618283a798c98a3090ed2b3038920e92608(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108683189140639cfb6ec5b39522d867862e1806a38d146af5b6d1e05fed5de8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e089f17bec712acc43f8ffe9c6c57339ec8f8e13c0c773aef923239330ca8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65601acb556602e4d91c960c7c6ec06f6ec983fbe9aa8bb1f9417b4c9648e94(
    value: typing.Optional[typing.Union[NetworkManagementConnectivityTestTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
