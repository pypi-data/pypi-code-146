'''
# `google_dataproc_cluster`

Refer to the Terraform Registory for docs: [`google_dataproc_cluster`](https://www.terraform.io/docs/providers/google/r/dataproc_cluster).
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


class DataprocCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocCluster",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster google_dataproc_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        cluster_config: typing.Optional[typing.Union["DataprocClusterClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        graceful_decommission_timeout: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataprocClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_cluster_config: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster google_dataproc_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the cluster, unique within the project and zone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#name DataprocCluster#name}
        :param cluster_config: cluster_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cluster_config DataprocCluster#cluster_config}
        :param graceful_decommission_timeout: The timeout duration which allows graceful decomissioning when you change the number of worker nodes directly through a terraform apply. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#graceful_decommission_timeout DataprocCluster#graceful_decommission_timeout}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#id DataprocCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The list of labels (key/value pairs) to be applied to instances in the cluster. GCP generates some itself including goog-dataproc-cluster-name which is the name of the cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#labels DataprocCluster#labels}
        :param project: The ID of the project in which the cluster will exist. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#project DataprocCluster#project}
        :param region: The region in which the cluster and associated nodes will be created in. Defaults to global. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#region DataprocCluster#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#timeouts DataprocCluster#timeouts}
        :param virtual_cluster_config: virtual_cluster_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#virtual_cluster_config DataprocCluster#virtual_cluster_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1361c52459d7f5c317fb6cc412435b35c41ec48fe8ebbb4ddb93198b939b35d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataprocClusterConfig(
            name=name,
            cluster_config=cluster_config,
            graceful_decommission_timeout=graceful_decommission_timeout,
            id=id,
            labels=labels,
            project=project,
            region=region,
            timeouts=timeouts,
            virtual_cluster_config=virtual_cluster_config,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putClusterConfig")
    def put_cluster_config(
        self,
        *,
        autoscaling_config: typing.Optional[typing.Union["DataprocClusterClusterConfigAutoscalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_config: typing.Optional[typing.Union["DataprocClusterClusterConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_config: typing.Optional[typing.Union["DataprocClusterClusterConfigEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gce_cluster_config: typing.Optional[typing.Union["DataprocClusterClusterConfigGceClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        initialization_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocClusterClusterConfigInitializationAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lifecycle_config: typing.Optional[typing.Union["DataprocClusterClusterConfigLifecycleConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        master_config: typing.Optional[typing.Union["DataprocClusterClusterConfigMasterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metastore_config: typing.Optional[typing.Union["DataprocClusterClusterConfigMetastoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible_worker_config: typing.Optional[typing.Union["DataprocClusterClusterConfigPreemptibleWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["DataprocClusterClusterConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        software_config: typing.Optional[typing.Union["DataprocClusterClusterConfigSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
        temp_bucket: typing.Optional[builtins.str] = None,
        worker_config: typing.Optional[typing.Union["DataprocClusterClusterConfigWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#autoscaling_config DataprocCluster#autoscaling_config}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#encryption_config DataprocCluster#encryption_config}
        :param endpoint_config: endpoint_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#endpoint_config DataprocCluster#endpoint_config}
        :param gce_cluster_config: gce_cluster_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#gce_cluster_config DataprocCluster#gce_cluster_config}
        :param initialization_action: initialization_action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#initialization_action DataprocCluster#initialization_action}
        :param lifecycle_config: lifecycle_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#lifecycle_config DataprocCluster#lifecycle_config}
        :param master_config: master_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#master_config DataprocCluster#master_config}
        :param metastore_config: metastore_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#metastore_config DataprocCluster#metastore_config}
        :param preemptible_worker_config: preemptible_worker_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#preemptible_worker_config DataprocCluster#preemptible_worker_config}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#security_config DataprocCluster#security_config}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#software_config DataprocCluster#software_config}
        :param staging_bucket: The Cloud Storage staging bucket used to stage files, such as Hadoop jars, between client machines and the cluster. Note: If you don't explicitly specify a staging_bucket then GCP will auto create / assign one for you. However, you are not guaranteed an auto generated bucket which is solely dedicated to your cluster; it may be shared with other clusters in the same region/zone also choosing to use the auto generation option. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#staging_bucket DataprocCluster#staging_bucket}
        :param temp_bucket: The Cloud Storage temp bucket used to store ephemeral cluster and jobs data, such as Spark and MapReduce history files. Note: If you don't explicitly specify a temp_bucket then GCP will auto create / assign one for you. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#temp_bucket DataprocCluster#temp_bucket}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#worker_config DataprocCluster#worker_config}
        '''
        value = DataprocClusterClusterConfig(
            autoscaling_config=autoscaling_config,
            encryption_config=encryption_config,
            endpoint_config=endpoint_config,
            gce_cluster_config=gce_cluster_config,
            initialization_action=initialization_action,
            lifecycle_config=lifecycle_config,
            master_config=master_config,
            metastore_config=metastore_config,
            preemptible_worker_config=preemptible_worker_config,
            security_config=security_config,
            software_config=software_config,
            staging_bucket=staging_bucket,
            temp_bucket=temp_bucket,
            worker_config=worker_config,
        )

        return typing.cast(None, jsii.invoke(self, "putClusterConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#create DataprocCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#delete DataprocCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#update DataprocCluster#update}.
        '''
        value = DataprocClusterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualClusterConfig")
    def put_virtual_cluster_config(
        self,
        *,
        auxiliary_services_config: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes_cluster_config: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfigKubernetesClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auxiliary_services_config: auxiliary_services_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#auxiliary_services_config DataprocCluster#auxiliary_services_config}
        :param kubernetes_cluster_config: kubernetes_cluster_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kubernetes_cluster_config DataprocCluster#kubernetes_cluster_config}
        :param staging_bucket: A Cloud Storage bucket used to stage job dependencies, config files, and job driver console output. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's staging bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#staging_bucket DataprocCluster#staging_bucket}
        '''
        value = DataprocClusterVirtualClusterConfig(
            auxiliary_services_config=auxiliary_services_config,
            kubernetes_cluster_config=kubernetes_cluster_config,
            staging_bucket=staging_bucket,
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualClusterConfig", [value]))

    @jsii.member(jsii_name="resetClusterConfig")
    def reset_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterConfig", []))

    @jsii.member(jsii_name="resetGracefulDecommissionTimeout")
    def reset_graceful_decommission_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGracefulDecommissionTimeout", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualClusterConfig")
    def reset_virtual_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualClusterConfig", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="clusterConfig")
    def cluster_config(self) -> "DataprocClusterClusterConfigOutputReference":
        return typing.cast("DataprocClusterClusterConfigOutputReference", jsii.get(self, "clusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataprocClusterTimeoutsOutputReference":
        return typing.cast("DataprocClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="virtualClusterConfig")
    def virtual_cluster_config(
        self,
    ) -> "DataprocClusterVirtualClusterConfigOutputReference":
        return typing.cast("DataprocClusterVirtualClusterConfigOutputReference", jsii.get(self, "virtualClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="clusterConfigInput")
    def cluster_config_input(self) -> typing.Optional["DataprocClusterClusterConfig"]:
        return typing.cast(typing.Optional["DataprocClusterClusterConfig"], jsii.get(self, "clusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gracefulDecommissionTimeoutInput")
    def graceful_decommission_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gracefulDecommissionTimeoutInput"))

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
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DataprocClusterTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DataprocClusterTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualClusterConfigInput")
    def virtual_cluster_config_input(
        self,
    ) -> typing.Optional["DataprocClusterVirtualClusterConfig"]:
        return typing.cast(typing.Optional["DataprocClusterVirtualClusterConfig"], jsii.get(self, "virtualClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gracefulDecommissionTimeout")
    def graceful_decommission_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gracefulDecommissionTimeout"))

    @graceful_decommission_timeout.setter
    def graceful_decommission_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99428885c5edc513fa19b3666d1d528528b90948555f984820be4779a2e22637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gracefulDecommissionTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9811bc19c8bd8c28166c100e6000d42d9636e644b896af1cab00ae33671bfb41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d925271068a9f55f483d80781a7edc9de81abe68cddecbb8738f7d4baddd68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79750a7321d8526e006c1c436690e363a135499d4f46ff6681bc7c11635d9bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4ccd87d3fc961930eb7d4d4ea2434e52c0da104a946c9f097380388457b4cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03fcf68ef8cf3dc3fcb9bdddf5c1e8c5fdfd3973b5497bca5bf29ca92db2f081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "autoscaling_config": "autoscalingConfig",
        "encryption_config": "encryptionConfig",
        "endpoint_config": "endpointConfig",
        "gce_cluster_config": "gceClusterConfig",
        "initialization_action": "initializationAction",
        "lifecycle_config": "lifecycleConfig",
        "master_config": "masterConfig",
        "metastore_config": "metastoreConfig",
        "preemptible_worker_config": "preemptibleWorkerConfig",
        "security_config": "securityConfig",
        "software_config": "softwareConfig",
        "staging_bucket": "stagingBucket",
        "temp_bucket": "tempBucket",
        "worker_config": "workerConfig",
    },
)
class DataprocClusterClusterConfig:
    def __init__(
        self,
        *,
        autoscaling_config: typing.Optional[typing.Union["DataprocClusterClusterConfigAutoscalingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_config: typing.Optional[typing.Union["DataprocClusterClusterConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_config: typing.Optional[typing.Union["DataprocClusterClusterConfigEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gce_cluster_config: typing.Optional[typing.Union["DataprocClusterClusterConfigGceClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        initialization_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocClusterClusterConfigInitializationAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lifecycle_config: typing.Optional[typing.Union["DataprocClusterClusterConfigLifecycleConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        master_config: typing.Optional[typing.Union["DataprocClusterClusterConfigMasterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metastore_config: typing.Optional[typing.Union["DataprocClusterClusterConfigMetastoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible_worker_config: typing.Optional[typing.Union["DataprocClusterClusterConfigPreemptibleWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        security_config: typing.Optional[typing.Union["DataprocClusterClusterConfigSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        software_config: typing.Optional[typing.Union["DataprocClusterClusterConfigSoftwareConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
        temp_bucket: typing.Optional[builtins.str] = None,
        worker_config: typing.Optional[typing.Union["DataprocClusterClusterConfigWorkerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscaling_config: autoscaling_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#autoscaling_config DataprocCluster#autoscaling_config}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#encryption_config DataprocCluster#encryption_config}
        :param endpoint_config: endpoint_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#endpoint_config DataprocCluster#endpoint_config}
        :param gce_cluster_config: gce_cluster_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#gce_cluster_config DataprocCluster#gce_cluster_config}
        :param initialization_action: initialization_action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#initialization_action DataprocCluster#initialization_action}
        :param lifecycle_config: lifecycle_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#lifecycle_config DataprocCluster#lifecycle_config}
        :param master_config: master_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#master_config DataprocCluster#master_config}
        :param metastore_config: metastore_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#metastore_config DataprocCluster#metastore_config}
        :param preemptible_worker_config: preemptible_worker_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#preemptible_worker_config DataprocCluster#preemptible_worker_config}
        :param security_config: security_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#security_config DataprocCluster#security_config}
        :param software_config: software_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#software_config DataprocCluster#software_config}
        :param staging_bucket: The Cloud Storage staging bucket used to stage files, such as Hadoop jars, between client machines and the cluster. Note: If you don't explicitly specify a staging_bucket then GCP will auto create / assign one for you. However, you are not guaranteed an auto generated bucket which is solely dedicated to your cluster; it may be shared with other clusters in the same region/zone also choosing to use the auto generation option. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#staging_bucket DataprocCluster#staging_bucket}
        :param temp_bucket: The Cloud Storage temp bucket used to store ephemeral cluster and jobs data, such as Spark and MapReduce history files. Note: If you don't explicitly specify a temp_bucket then GCP will auto create / assign one for you. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#temp_bucket DataprocCluster#temp_bucket}
        :param worker_config: worker_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#worker_config DataprocCluster#worker_config}
        '''
        if isinstance(autoscaling_config, dict):
            autoscaling_config = DataprocClusterClusterConfigAutoscalingConfig(**autoscaling_config)
        if isinstance(encryption_config, dict):
            encryption_config = DataprocClusterClusterConfigEncryptionConfig(**encryption_config)
        if isinstance(endpoint_config, dict):
            endpoint_config = DataprocClusterClusterConfigEndpointConfig(**endpoint_config)
        if isinstance(gce_cluster_config, dict):
            gce_cluster_config = DataprocClusterClusterConfigGceClusterConfig(**gce_cluster_config)
        if isinstance(lifecycle_config, dict):
            lifecycle_config = DataprocClusterClusterConfigLifecycleConfig(**lifecycle_config)
        if isinstance(master_config, dict):
            master_config = DataprocClusterClusterConfigMasterConfig(**master_config)
        if isinstance(metastore_config, dict):
            metastore_config = DataprocClusterClusterConfigMetastoreConfig(**metastore_config)
        if isinstance(preemptible_worker_config, dict):
            preemptible_worker_config = DataprocClusterClusterConfigPreemptibleWorkerConfig(**preemptible_worker_config)
        if isinstance(security_config, dict):
            security_config = DataprocClusterClusterConfigSecurityConfig(**security_config)
        if isinstance(software_config, dict):
            software_config = DataprocClusterClusterConfigSoftwareConfig(**software_config)
        if isinstance(worker_config, dict):
            worker_config = DataprocClusterClusterConfigWorkerConfig(**worker_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ebd1a663f62e6eb4ba021ba34bffb4f0b66deca8669a703806ddd54a6269f9)
            check_type(argname="argument autoscaling_config", value=autoscaling_config, expected_type=type_hints["autoscaling_config"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument endpoint_config", value=endpoint_config, expected_type=type_hints["endpoint_config"])
            check_type(argname="argument gce_cluster_config", value=gce_cluster_config, expected_type=type_hints["gce_cluster_config"])
            check_type(argname="argument initialization_action", value=initialization_action, expected_type=type_hints["initialization_action"])
            check_type(argname="argument lifecycle_config", value=lifecycle_config, expected_type=type_hints["lifecycle_config"])
            check_type(argname="argument master_config", value=master_config, expected_type=type_hints["master_config"])
            check_type(argname="argument metastore_config", value=metastore_config, expected_type=type_hints["metastore_config"])
            check_type(argname="argument preemptible_worker_config", value=preemptible_worker_config, expected_type=type_hints["preemptible_worker_config"])
            check_type(argname="argument security_config", value=security_config, expected_type=type_hints["security_config"])
            check_type(argname="argument software_config", value=software_config, expected_type=type_hints["software_config"])
            check_type(argname="argument staging_bucket", value=staging_bucket, expected_type=type_hints["staging_bucket"])
            check_type(argname="argument temp_bucket", value=temp_bucket, expected_type=type_hints["temp_bucket"])
            check_type(argname="argument worker_config", value=worker_config, expected_type=type_hints["worker_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autoscaling_config is not None:
            self._values["autoscaling_config"] = autoscaling_config
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if endpoint_config is not None:
            self._values["endpoint_config"] = endpoint_config
        if gce_cluster_config is not None:
            self._values["gce_cluster_config"] = gce_cluster_config
        if initialization_action is not None:
            self._values["initialization_action"] = initialization_action
        if lifecycle_config is not None:
            self._values["lifecycle_config"] = lifecycle_config
        if master_config is not None:
            self._values["master_config"] = master_config
        if metastore_config is not None:
            self._values["metastore_config"] = metastore_config
        if preemptible_worker_config is not None:
            self._values["preemptible_worker_config"] = preemptible_worker_config
        if security_config is not None:
            self._values["security_config"] = security_config
        if software_config is not None:
            self._values["software_config"] = software_config
        if staging_bucket is not None:
            self._values["staging_bucket"] = staging_bucket
        if temp_bucket is not None:
            self._values["temp_bucket"] = temp_bucket
        if worker_config is not None:
            self._values["worker_config"] = worker_config

    @builtins.property
    def autoscaling_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigAutoscalingConfig"]:
        '''autoscaling_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#autoscaling_config DataprocCluster#autoscaling_config}
        '''
        result = self._values.get("autoscaling_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigAutoscalingConfig"], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#encryption_config DataprocCluster#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigEncryptionConfig"], result)

    @builtins.property
    def endpoint_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigEndpointConfig"]:
        '''endpoint_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#endpoint_config DataprocCluster#endpoint_config}
        '''
        result = self._values.get("endpoint_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigEndpointConfig"], result)

    @builtins.property
    def gce_cluster_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigGceClusterConfig"]:
        '''gce_cluster_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#gce_cluster_config DataprocCluster#gce_cluster_config}
        '''
        result = self._values.get("gce_cluster_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigGceClusterConfig"], result)

    @builtins.property
    def initialization_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocClusterClusterConfigInitializationAction"]]]:
        '''initialization_action block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#initialization_action DataprocCluster#initialization_action}
        '''
        result = self._values.get("initialization_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocClusterClusterConfigInitializationAction"]]], result)

    @builtins.property
    def lifecycle_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigLifecycleConfig"]:
        '''lifecycle_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#lifecycle_config DataprocCluster#lifecycle_config}
        '''
        result = self._values.get("lifecycle_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigLifecycleConfig"], result)

    @builtins.property
    def master_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigMasterConfig"]:
        '''master_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#master_config DataprocCluster#master_config}
        '''
        result = self._values.get("master_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigMasterConfig"], result)

    @builtins.property
    def metastore_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigMetastoreConfig"]:
        '''metastore_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#metastore_config DataprocCluster#metastore_config}
        '''
        result = self._values.get("metastore_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigMetastoreConfig"], result)

    @builtins.property
    def preemptible_worker_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigPreemptibleWorkerConfig"]:
        '''preemptible_worker_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#preemptible_worker_config DataprocCluster#preemptible_worker_config}
        '''
        result = self._values.get("preemptible_worker_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigPreemptibleWorkerConfig"], result)

    @builtins.property
    def security_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigSecurityConfig"]:
        '''security_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#security_config DataprocCluster#security_config}
        '''
        result = self._values.get("security_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigSecurityConfig"], result)

    @builtins.property
    def software_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigSoftwareConfig"]:
        '''software_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#software_config DataprocCluster#software_config}
        '''
        result = self._values.get("software_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigSoftwareConfig"], result)

    @builtins.property
    def staging_bucket(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage staging bucket used to stage files, such as Hadoop jars, between client machines and the cluster.

        Note: If you don't explicitly specify a staging_bucket then GCP will auto create / assign one for you. However, you are not guaranteed an auto generated bucket which is solely dedicated to your cluster; it may be shared with other clusters in the same region/zone also choosing to use the auto generation option.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#staging_bucket DataprocCluster#staging_bucket}
        '''
        result = self._values.get("staging_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def temp_bucket(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage temp bucket used to store ephemeral cluster and jobs data, such as Spark and MapReduce history files.

        Note: If you don't explicitly specify a temp_bucket then GCP will auto create / assign one for you.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#temp_bucket DataprocCluster#temp_bucket}
        '''
        result = self._values.get("temp_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigWorkerConfig"]:
        '''worker_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#worker_config DataprocCluster#worker_config}
        '''
        result = self._values.get("worker_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigWorkerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigAutoscalingConfig",
    jsii_struct_bases=[],
    name_mapping={"policy_uri": "policyUri"},
)
class DataprocClusterClusterConfigAutoscalingConfig:
    def __init__(self, *, policy_uri: builtins.str) -> None:
        '''
        :param policy_uri: The autoscaling policy used by the cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#policy_uri DataprocCluster#policy_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2b0e0bb924cd4fa2603b98d6f0c96f70afb7418caf8d7b567c88aba62caeb6)
            check_type(argname="argument policy_uri", value=policy_uri, expected_type=type_hints["policy_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_uri": policy_uri,
        }

    @builtins.property
    def policy_uri(self) -> builtins.str:
        '''The autoscaling policy used by the cluster.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#policy_uri DataprocCluster#policy_uri}
        '''
        result = self._values.get("policy_uri")
        assert result is not None, "Required property 'policy_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigAutoscalingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigAutoscalingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigAutoscalingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86e9baf4b634027e17b8c766049ba97bf2e64f181afa12425c0666db38c27895)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="policyUriInput")
    def policy_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyUriInput"))

    @builtins.property
    @jsii.member(jsii_name="policyUri")
    def policy_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyUri"))

    @policy_uri.setter
    def policy_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7766db844ace0cde2ec40b5c6bbb0b8847c37562d8e72e0c4bac2d128ac58952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyUri", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigAutoscalingConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigAutoscalingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigAutoscalingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6a45447babcf4de794be24fbf08704f8187ede924f3c70bd82c00d16cf5c13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class DataprocClusterClusterConfigEncryptionConfig:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The Cloud KMS key name to use for PD disk encryption for all instances in the cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kms_key_name DataprocCluster#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f323d9285643fc922bf8cb378c44546565832cb5fc9f82a1309cb8cf668652)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''The Cloud KMS key name to use for PD disk encryption for all instances in the cluster.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kms_key_name DataprocCluster#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5558ad8aedc494571a717e99d3181c16f3988f4c73979762496b0efee27f6421)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a724eff7b84509369fc46c2668e13c2a011e9fad3b5f36e57e907a4a70fb3ae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigEncryptionConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eca4696922f8e886d6b10b18cfa659e4f462ca9ef089e536b082ea1904deed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigEndpointConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_http_port_access": "enableHttpPortAccess"},
)
class DataprocClusterClusterConfigEndpointConfig:
    def __init__(
        self,
        *,
        enable_http_port_access: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_http_port_access: The flag to enable http access to specific ports on the cluster from external sources (aka Component Gateway). Defaults to false. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_http_port_access DataprocCluster#enable_http_port_access}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abed7dd0e9404699d2efde3c9cc15ca624114579ad97c088a16df6c79a5f398a)
            check_type(argname="argument enable_http_port_access", value=enable_http_port_access, expected_type=type_hints["enable_http_port_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_http_port_access": enable_http_port_access,
        }

    @builtins.property
    def enable_http_port_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''The flag to enable http access to specific ports on the cluster from external sources (aka Component Gateway).

        Defaults to false.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_http_port_access DataprocCluster#enable_http_port_access}
        '''
        result = self._values.get("enable_http_port_access")
        assert result is not None, "Required property 'enable_http_port_access' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigEndpointConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigEndpointConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__601f361f41b67c9ba6e7edc31dec832e9b876469710bc150c92796062069d3cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="httpPorts")
    def http_ports(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "httpPorts"))

    @builtins.property
    @jsii.member(jsii_name="enableHttpPortAccessInput")
    def enable_http_port_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHttpPortAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHttpPortAccess")
    def enable_http_port_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHttpPortAccess"))

    @enable_http_port_access.setter
    def enable_http_port_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2217068902d6c92148027089e087d05d05f71f130e404300ee9f1c7b478c2741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHttpPortAccess", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigEndpointConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigEndpointConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigEndpointConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d36ba828aadfa3b73df3b372ccb7f2cfea6d090f816b6a44d972113e573ed1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigGceClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "internal_ip_only": "internalIpOnly",
        "metadata": "metadata",
        "network": "network",
        "service_account": "serviceAccount",
        "service_account_scopes": "serviceAccountScopes",
        "shielded_instance_config": "shieldedInstanceConfig",
        "subnetwork": "subnetwork",
        "tags": "tags",
        "zone": "zone",
    },
)
class DataprocClusterClusterConfigGceClusterConfig:
    def __init__(
        self,
        *,
        internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        shielded_instance_config: typing.Optional[typing.Union["DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param internal_ip_only: By default, clusters are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each instance. If set to true, all instances in the cluster will only have internal IP addresses. Note: Private Google Access (also known as privateIpGoogleAccess) must be enabled on the subnetwork that the cluster will be launched in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#internal_ip_only DataprocCluster#internal_ip_only}
        :param metadata: A map of the Compute Engine metadata entries to add to all instances. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#metadata DataprocCluster#metadata}
        :param network: The name or self_link of the Google Compute Engine network to the cluster will be part of. Conflicts with subnetwork. If neither is specified, this defaults to the "default" network. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#network DataprocCluster#network}
        :param service_account: The service account to be used by the Node VMs. If not specified, the "default" service account is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#service_account DataprocCluster#service_account}
        :param service_account_scopes: The set of Google API scopes to be made available on all of the node VMs under the service_account specified. These can be either FQDNs, or scope aliases. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#service_account_scopes DataprocCluster#service_account_scopes}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#shielded_instance_config DataprocCluster#shielded_instance_config}
        :param subnetwork: The name or self_link of the Google Compute Engine subnetwork the cluster will be part of. Conflicts with network. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#subnetwork DataprocCluster#subnetwork}
        :param tags: The list of instance tags applied to instances in the cluster. Tags are used to identify valid sources or targets for network firewalls. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#tags DataprocCluster#tags}
        :param zone: The GCP zone where your data is stored and used (i.e. where the master and the worker nodes will be created in). If region is set to 'global' (default) then zone is mandatory, otherwise GCP is able to make use of Auto Zone Placement to determine this automatically for you. Note: This setting additionally determines and restricts which computing resources are available for use with other configs such as cluster_config.master_config.machine_type and cluster_config.worker_config.machine_type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#zone DataprocCluster#zone}
        '''
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig(**shielded_instance_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae83a0087abf138cdc7686f6ddf05150339cb235982ce2197d5b9d0330bcecc9)
            check_type(argname="argument internal_ip_only", value=internal_ip_only, expected_type=type_hints["internal_ip_only"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument service_account_scopes", value=service_account_scopes, expected_type=type_hints["service_account_scopes"])
            check_type(argname="argument shielded_instance_config", value=shielded_instance_config, expected_type=type_hints["shielded_instance_config"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if internal_ip_only is not None:
            self._values["internal_ip_only"] = internal_ip_only
        if metadata is not None:
            self._values["metadata"] = metadata
        if network is not None:
            self._values["network"] = network
        if service_account is not None:
            self._values["service_account"] = service_account
        if service_account_scopes is not None:
            self._values["service_account_scopes"] = service_account_scopes
        if shielded_instance_config is not None:
            self._values["shielded_instance_config"] = shielded_instance_config
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if tags is not None:
            self._values["tags"] = tags
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def internal_ip_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''By default, clusters are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each instance.

        If set to true, all instances in the cluster will only have internal IP addresses. Note: Private Google Access (also known as privateIpGoogleAccess) must be enabled on the subnetwork that the cluster will be launched in.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#internal_ip_only DataprocCluster#internal_ip_only}
        '''
        result = self._values.get("internal_ip_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of the Compute Engine metadata entries to add to all instances.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#metadata DataprocCluster#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the Google Compute Engine network to the cluster will be part of.

        Conflicts with subnetwork. If neither is specified, this defaults to the "default" network.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#network DataprocCluster#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The service account to be used by the Node VMs. If not specified, the "default" service account is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#service_account DataprocCluster#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of Google API scopes to be made available on all of the node VMs under the service_account specified.

        These can be either FQDNs, or scope aliases.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#service_account_scopes DataprocCluster#service_account_scopes}
        '''
        result = self._values.get("service_account_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#shielded_instance_config DataprocCluster#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig"], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the Google Compute Engine subnetwork the cluster will be part of. Conflicts with network.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#subnetwork DataprocCluster#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of instance tags applied to instances in the cluster.

        Tags are used to identify valid sources or targets for network firewalls.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#tags DataprocCluster#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The GCP zone where your data is stored and used (i.e. where the master and the worker nodes will be created in). If region is set to 'global' (default) then zone is mandatory, otherwise GCP is able to make use of Auto Zone Placement to determine this automatically for you. Note: This setting additionally determines and restricts which computing resources are available for use with other configs such as cluster_config.master_config.machine_type and cluster_config.worker_config.machine_type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#zone DataprocCluster#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigGceClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigGceClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigGceClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f07a54ac970aedfda79ca17b4e387af422fb6e6bab6acf0393979d22e4c804a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putShieldedInstanceConfig")
    def put_shielded_instance_config(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether instances have integrity monitoring enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_integrity_monitoring DataprocCluster#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether instances have Secure Boot enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_secure_boot DataprocCluster#enable_secure_boot}
        :param enable_vtpm: Defines whether instances have the vTPM enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_vtpm DataprocCluster#enable_vtpm}
        '''
        value = DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig(
            enable_integrity_monitoring=enable_integrity_monitoring,
            enable_secure_boot=enable_secure_boot,
            enable_vtpm=enable_vtpm,
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedInstanceConfig", [value]))

    @jsii.member(jsii_name="resetInternalIpOnly")
    def reset_internal_ip_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalIpOnly", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetServiceAccountScopes")
    def reset_service_account_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountScopes", []))

    @jsii.member(jsii_name="resetShieldedInstanceConfig")
    def reset_shielded_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedInstanceConfig", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference":
        return typing.cast("DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="internalIpOnlyInput")
    def internal_ip_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalIpOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountScopesInput")
    def service_account_scopes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceAccountScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpOnly")
    def internal_ip_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "internalIpOnly"))

    @internal_ip_only.setter
    def internal_ip_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e0c7723e6560e795a88604889c7a387b26dd89159cab44fd60151b7de8cba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpOnly", value)

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b8dc5b947381789c0b69b355432d60c698e51d7e0b410a9d1c50eee8094143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value)

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195487a66a38bab7efae39d603a8d69c7f5ae38781705c1caf237636fcaac74b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value)

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9664424eb7fc135c5bd9ea0ecc624c7d6e522b4ff961167049558f8ee71bb84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value)

    @builtins.property
    @jsii.member(jsii_name="serviceAccountScopes")
    def service_account_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAccountScopes"))

    @service_account_scopes.setter
    def service_account_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f79b12413004321591219dbabb574961196a94151161e626b1ab2969584475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountScopes", value)

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3195e710ad97f345964cb5b925c6d72cffe3235acffe9600aeb71c45942c538c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579954a5eee5480b5dcdad68fe5639712dfdb275d4697e9d4626013fda8adce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b59eb7dcfce186512f0891d8d2b6e89e2c3f3cb9da9ee080891f14bcffb443b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigGceClusterConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigGceClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigGceClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a98e35f1468dd367d15d28f7d96fbaca8626ead1872f2324ad7f56c9ef2584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether instances have integrity monitoring enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_integrity_monitoring DataprocCluster#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether instances have Secure Boot enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_secure_boot DataprocCluster#enable_secure_boot}
        :param enable_vtpm: Defines whether instances have the vTPM enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_vtpm DataprocCluster#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90fa2722da5048a09b9da96543437b900ab95e0d826e784041d26ed59c6a5694)
            check_type(argname="argument enable_integrity_monitoring", value=enable_integrity_monitoring, expected_type=type_hints["enable_integrity_monitoring"])
            check_type(argname="argument enable_secure_boot", value=enable_secure_boot, expected_type=type_hints["enable_secure_boot"])
            check_type(argname="argument enable_vtpm", value=enable_vtpm, expected_type=type_hints["enable_vtpm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_integrity_monitoring is not None:
            self._values["enable_integrity_monitoring"] = enable_integrity_monitoring
        if enable_secure_boot is not None:
            self._values["enable_secure_boot"] = enable_secure_boot
        if enable_vtpm is not None:
            self._values["enable_vtpm"] = enable_vtpm

    @builtins.property
    def enable_integrity_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether instances have integrity monitoring enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_integrity_monitoring DataprocCluster#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether instances have Secure Boot enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_secure_boot DataprocCluster#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether instances have the vTPM enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_vtpm DataprocCluster#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d49a209a43b6bd308d44a5f3ec87c4bb35a0bff7077a2f40de72b88408d92326)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableIntegrityMonitoring")
    def reset_enable_integrity_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIntegrityMonitoring", []))

    @jsii.member(jsii_name="resetEnableSecureBoot")
    def reset_enable_secure_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSecureBoot", []))

    @jsii.member(jsii_name="resetEnableVtpm")
    def reset_enable_vtpm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableVtpm", []))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoringInput")
    def enable_integrity_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIntegrityMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSecureBootInput")
    def enable_secure_boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSecureBootInput"))

    @builtins.property
    @jsii.member(jsii_name="enableVtpmInput")
    def enable_vtpm_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableVtpmInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoring")
    def enable_integrity_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIntegrityMonitoring"))

    @enable_integrity_monitoring.setter
    def enable_integrity_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece8824f4ec90422e2a376866ba25c2787da45b972aa2eb7cf3ffebc5293a35b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIntegrityMonitoring", value)

    @builtins.property
    @jsii.member(jsii_name="enableSecureBoot")
    def enable_secure_boot(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSecureBoot"))

    @enable_secure_boot.setter
    def enable_secure_boot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5ba5e87d20f40258260bacdfd2436e966fadfffad99073720eeedc99487214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSecureBoot", value)

    @builtins.property
    @jsii.member(jsii_name="enableVtpm")
    def enable_vtpm(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableVtpm"))

    @enable_vtpm.setter
    def enable_vtpm(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf580c6c825f799be4f68366ea6d9dc7a89641883ba4dde7004cc33480e0719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9dcbf40159e03977aeb677f488b9ff16e070efd3a263b1a8cf3f4717b50a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigInitializationAction",
    jsii_struct_bases=[],
    name_mapping={"script": "script", "timeout_sec": "timeoutSec"},
)
class DataprocClusterClusterConfigInitializationAction:
    def __init__(
        self,
        *,
        script: builtins.str,
        timeout_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param script: The script to be executed during initialization of the cluster. The script must be a GCS file with a gs:// prefix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#script DataprocCluster#script}
        :param timeout_sec: The maximum duration (in seconds) which script is allowed to take to execute its action. GCP will default to a predetermined computed value if not set (currently 300). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#timeout_sec DataprocCluster#timeout_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc72500ea70f15d82e3d65c6b55037e0dfffef4e4d6d02c100c77323098b962)
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument timeout_sec", value=timeout_sec, expected_type=type_hints["timeout_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "script": script,
        }
        if timeout_sec is not None:
            self._values["timeout_sec"] = timeout_sec

    @builtins.property
    def script(self) -> builtins.str:
        '''The script to be executed during initialization of the cluster.

        The script must be a GCS file with a gs:// prefix.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#script DataprocCluster#script}
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''The maximum duration (in seconds) which script is allowed to take to execute its action.

        GCP will default to a predetermined computed value if not set (currently 300).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#timeout_sec DataprocCluster#timeout_sec}
        '''
        result = self._values.get("timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigInitializationAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigInitializationActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigInitializationActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__109f97ed3f310c9e978fd9e953ab4f58b20d0fb36ce736f9e4e3b89db5f0ae96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocClusterClusterConfigInitializationActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3100838196617f2c2d48faa6c47cbc0b8f3ca34918bac0c88ab18446428387b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocClusterClusterConfigInitializationActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0a00c9d6281f1bb95bea56f1b3ffbaec2b64c289a412e0b88cd4d95cd5ef26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4418148e3e220cf70a1b0c2d2cfb72e1b64c3fb6052ff6eae5c72aa5529fdeef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0eee2acf3690873a8cf26afb7e02a9ca92f469461eb6ad8e90ff381b62763bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigInitializationAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigInitializationAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigInitializationAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ef30e367814905f4c96c40f7e8db6bb8af46fa52550b29c467c9f41fca82d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterClusterConfigInitializationActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigInitializationActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e213029e5d8e2886dec7c4a9d5b6fc6686d37d4a985a3ffdfdb82ee44f30a80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTimeoutSec")
    def reset_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSec", []))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecInput")
    def timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be3a38bd1c8f321dfbf1a9dd6747255259258948b267c7c51ff48bf285665ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutSec")
    def timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSec"))

    @timeout_sec.setter
    def timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1b2f74b47e1b717c8246b6d281c651556dfac2b467e22835355efc99ed7bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSec", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataprocClusterClusterConfigInitializationAction, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataprocClusterClusterConfigInitializationAction, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataprocClusterClusterConfigInitializationAction, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca6b3bc6d029fa0cc0497bb9224185d8772412e2512f91ac3bf02be5434c888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigLifecycleConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auto_delete_time": "autoDeleteTime",
        "idle_delete_ttl": "idleDeleteTtl",
    },
)
class DataprocClusterClusterConfigLifecycleConfig:
    def __init__(
        self,
        *,
        auto_delete_time: typing.Optional[builtins.str] = None,
        idle_delete_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_delete_time: The time when cluster will be auto-deleted. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#auto_delete_time DataprocCluster#auto_delete_time}
        :param idle_delete_ttl: The duration to keep the cluster alive while idling (no jobs running). After this TTL, the cluster will be deleted. Valid range: [10m, 14d]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#idle_delete_ttl DataprocCluster#idle_delete_ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f8e00bbd6f14c5a419f1acf6ec406dbca1194438c02d56e29750513ccd8bd0)
            check_type(argname="argument auto_delete_time", value=auto_delete_time, expected_type=type_hints["auto_delete_time"])
            check_type(argname="argument idle_delete_ttl", value=idle_delete_ttl, expected_type=type_hints["idle_delete_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_delete_time is not None:
            self._values["auto_delete_time"] = auto_delete_time
        if idle_delete_ttl is not None:
            self._values["idle_delete_ttl"] = idle_delete_ttl

    @builtins.property
    def auto_delete_time(self) -> typing.Optional[builtins.str]:
        '''The time when cluster will be auto-deleted. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#auto_delete_time DataprocCluster#auto_delete_time}
        '''
        result = self._values.get("auto_delete_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_delete_ttl(self) -> typing.Optional[builtins.str]:
        '''The duration to keep the cluster alive while idling (no jobs running).

        After this TTL, the cluster will be deleted. Valid range: [10m, 14d].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#idle_delete_ttl DataprocCluster#idle_delete_ttl}
        '''
        result = self._values.get("idle_delete_ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigLifecycleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigLifecycleConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigLifecycleConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c44c95af8e1a85bc95f04daf1cb0cd641c3f037641fbb98b3fe1e84498c119e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAutoDeleteTime")
    def reset_auto_delete_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDeleteTime", []))

    @jsii.member(jsii_name="resetIdleDeleteTtl")
    def reset_idle_delete_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleDeleteTtl", []))

    @builtins.property
    @jsii.member(jsii_name="idleStartTime")
    def idle_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleStartTime"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteTimeInput")
    def auto_delete_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoDeleteTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="idleDeleteTtlInput")
    def idle_delete_ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idleDeleteTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteTime")
    def auto_delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDeleteTime"))

    @auto_delete_time.setter
    def auto_delete_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53736dc1f675ef3228450f0c022a37a8ade4eff7b328cccde8a2307cd3ec9aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDeleteTime", value)

    @builtins.property
    @jsii.member(jsii_name="idleDeleteTtl")
    def idle_delete_ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idleDeleteTtl"))

    @idle_delete_ttl.setter
    def idle_delete_ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d537c8a347e055f319508c502046b10c6a8bda10f9724ec3aaaef9d6697231d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleDeleteTtl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigLifecycleConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigLifecycleConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigLifecycleConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8278d4a6ca217e008667e322158926176b84265b3a9e462232dcf270bc9c06a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigMasterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "disk_config": "diskConfig",
        "image_uri": "imageUri",
        "machine_type": "machineType",
        "min_cpu_platform": "minCpuPlatform",
        "num_instances": "numInstances",
    },
)
class DataprocClusterClusterConfigMasterConfig:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocClusterClusterConfigMasterConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["DataprocClusterClusterConfigMasterConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerators DataprocCluster#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#disk_config DataprocCluster#disk_config}
        :param image_uri: The URI for the image to use for this master/worker. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#image_uri DataprocCluster#image_uri}
        :param machine_type: The name of a Google Compute Engine machine type to create for the master/worker. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#machine_type DataprocCluster#machine_type}
        :param min_cpu_platform: The name of a minimum generation of CPU family for the master/worker. If not specified, GCP will default to a predetermined computed value for each zone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_cpu_platform DataprocCluster#min_cpu_platform}
        :param num_instances: Specifies the number of master/worker nodes to create. If not specified, GCP will default to a predetermined computed value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_instances DataprocCluster#num_instances}
        '''
        if isinstance(disk_config, dict):
            disk_config = DataprocClusterClusterConfigMasterConfigDiskConfig(**disk_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45854c553ce00b06aa99bf4b4ef1a7e404000a802afc2165eebd5980398c2447)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument disk_config", value=disk_config, expected_type=type_hints["disk_config"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument num_instances", value=num_instances, expected_type=type_hints["num_instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if disk_config is not None:
            self._values["disk_config"] = disk_config
        if image_uri is not None:
            self._values["image_uri"] = image_uri
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if num_instances is not None:
            self._values["num_instances"] = num_instances

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocClusterClusterConfigMasterConfigAccelerators"]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerators DataprocCluster#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocClusterClusterConfigMasterConfigAccelerators"]]], result)

    @builtins.property
    def disk_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigMasterConfigDiskConfig"]:
        '''disk_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#disk_config DataprocCluster#disk_config}
        '''
        result = self._values.get("disk_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigMasterConfigDiskConfig"], result)

    @builtins.property
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''The URI for the image to use for this master/worker.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#image_uri DataprocCluster#image_uri}
        '''
        result = self._values.get("image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The name of a Google Compute Engine machine type to create for the master/worker.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#machine_type DataprocCluster#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''The name of a minimum generation of CPU family for the master/worker.

        If not specified, GCP will default to a predetermined computed value for each zone.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_cpu_platform DataprocCluster#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_instances(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of master/worker nodes to create. If not specified, GCP will default to a predetermined computed value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_instances DataprocCluster#num_instances}
        '''
        result = self._values.get("num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigMasterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigMasterConfigAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class DataprocClusterClusterConfigMasterConfigAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: jsii.Number,
        accelerator_type: builtins.str,
    ) -> None:
        '''
        :param accelerator_count: The number of the accelerator cards of this type exposed to this instance. Often restricted to one of 1, 2, 4, or 8. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerator_count DataprocCluster#accelerator_count}
        :param accelerator_type: The short name of the accelerator type to expose to this instance. For example, nvidia-tesla-k80. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerator_type DataprocCluster#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d24ab99db5c0b11130c2347390148fc4f94c8218263d89a9ddc0ac1fb2d7e53)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator_count": accelerator_count,
            "accelerator_type": accelerator_type,
        }

    @builtins.property
    def accelerator_count(self) -> jsii.Number:
        '''The number of the accelerator cards of this type exposed to this instance.

        Often restricted to one of 1, 2, 4, or 8.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerator_count DataprocCluster#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        assert result is not None, "Required property 'accelerator_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def accelerator_type(self) -> builtins.str:
        '''The short name of the accelerator type to expose to this instance. For example, nvidia-tesla-k80.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerator_type DataprocCluster#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        assert result is not None, "Required property 'accelerator_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigMasterConfigAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigMasterConfigAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigMasterConfigAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aeae9fe2ae8421b2c40d55cb25448207691e609571c756c34972581e71fdac0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocClusterClusterConfigMasterConfigAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa948c1668e28e6e8edb6460a26a01f87e35b7ea34cf6cdd3d86e923e384e368)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocClusterClusterConfigMasterConfigAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c9c7688d9af86f73b6777aa66579886cf5bc75a74db4e25aaaf35af2c4296f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4dde6362eaeeae6005d6d248281cce3dde9c442ef74dbe7d5ebf887a864b019)
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
            type_hints = typing.get_type_hints(_typecheckingstub__443a29293231a08226a5aba1a335c75905e2a036bb3d819a4a1d0010110593b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigMasterConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigMasterConfigAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigMasterConfigAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0b414a0942bc5e90153e7b37ffd4fc6963c2ef42180240d048c29d30095d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterClusterConfigMasterConfigAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigMasterConfigAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e354d6d7ce05e91d59ba7e3e2cb33a96e6f9e415f330d39f3bfb4032bdc497df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @accelerator_count.setter
    def accelerator_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c698fc19ebb1eabb8abc04bf52c166a62a1f4c43606e14650e3927623ef9ff1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value)

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d227f31be2690d8490080dff407ef65ffed9480726daf29e683ee33cb814216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataprocClusterClusterConfigMasterConfigAccelerators, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataprocClusterClusterConfigMasterConfigAccelerators, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataprocClusterClusterConfigMasterConfigAccelerators, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f760252aec18ca06104f40f6eb0491e316d62fab64b64c2feb8d1ad12822dc35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigMasterConfigDiskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "num_local_ssds": "numLocalSsds",
    },
)
class DataprocClusterClusterConfigMasterConfigDiskConfig:
    def __init__(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each node, specified in GB. The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_size_gb DataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_type DataprocCluster#boot_disk_type}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_local_ssds DataprocCluster#num_local_ssds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b8b0871bd095581c9baef18e9ed02aedea04b46ac26b41be557d8dd6a24ded)
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument num_local_ssds", value=num_local_ssds, expected_type=type_hints["num_local_ssds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if num_local_ssds is not None:
            self._values["num_local_ssds"] = num_local_ssds

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the primary disk attached to each node, specified in GB.

        The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_size_gb DataprocCluster#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_type DataprocCluster#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_local_ssds(self) -> typing.Optional[jsii.Number]:
        '''The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_local_ssds DataprocCluster#num_local_ssds}
        '''
        result = self._values.get("num_local_ssds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigMasterConfigDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigMasterConfigDiskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigMasterConfigDiskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d66e2395115c39953bc1872f8c9ce6812f4ccc1d9d30b17ebc0e84e0ab7cf0ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetNumLocalSsds")
    def reset_num_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLocalSsds", []))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="numLocalSsdsInput")
    def num_local_ssds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLocalSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee5960fb15c857b2ebeff6847d45c862b64434208a91b4706e364fc42e61eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value)

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7a7717affe46cbf85ae01d1fb5bc03cd6977d2f744a4d603a8f9d6b2e4e5ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value)

    @builtins.property
    @jsii.member(jsii_name="numLocalSsds")
    def num_local_ssds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLocalSsds"))

    @num_local_ssds.setter
    def num_local_ssds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3c41ae9388e75de7d1267eae8980e8b6c99cbb014ed32a3be09efd012b73e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLocalSsds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigMasterConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigMasterConfigDiskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigMasterConfigDiskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d2e3f2f749c6af41dcce6f1d688a8fd7b5d91ae5883f292ffb4e2ec66a99fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterClusterConfigMasterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigMasterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71c3770ff05025df38a717c3164d46140d2d4cca76400f690cb8469370ff7e57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65114f1d1fe2f53a4b2aeccde75ff4dd8e114f89c21b8b5ce1eb096d9aa8a922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putDiskConfig")
    def put_disk_config(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each node, specified in GB. The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_size_gb DataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_type DataprocCluster#boot_disk_type}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_local_ssds DataprocCluster#num_local_ssds}
        '''
        value = DataprocClusterClusterConfigMasterConfigDiskConfig(
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            num_local_ssds=num_local_ssds,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskConfig", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetDiskConfig")
    def reset_disk_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConfig", []))

    @jsii.member(jsii_name="resetImageUri")
    def reset_image_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageUri", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetNumInstances")
    def reset_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumInstances", []))

    @builtins.property
    @jsii.member(jsii_name="accelerators")
    def accelerators(self) -> DataprocClusterClusterConfigMasterConfigAcceleratorsList:
        return typing.cast(DataprocClusterClusterConfigMasterConfigAcceleratorsList, jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="diskConfig")
    def disk_config(
        self,
    ) -> DataprocClusterClusterConfigMasterConfigDiskConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigMasterConfigDiskConfigOutputReference, jsii.get(self, "diskConfig"))

    @builtins.property
    @jsii.member(jsii_name="instanceNames")
    def instance_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNames"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigMasterConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigMasterConfigAccelerators]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskConfigInput")
    def disk_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigMasterConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigMasterConfigDiskConfig], jsii.get(self, "diskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstancesInput")
    def num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6564616b831c52281f910975a25b3109d5d92289dcf835ce26de652237ca2f87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value)

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c199e37d83b5df23772ade3f88cc9c2345e8ab5986fbbf3ae2444ef9dc2d37ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value)

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a6e1da4c7a23550712f8c3664269721fdb6d94ad1033db18e678a0a8670296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value)

    @builtins.property
    @jsii.member(jsii_name="numInstances")
    def num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numInstances"))

    @num_instances.setter
    def num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19348ea95b15abdd232872e6550b64ba37464e48f4472cf04153075e0d07fa0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numInstances", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigMasterConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigMasterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigMasterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352aedd8d4b5f3980fe15cf5a5dcdf47aff40c6e00c7b88ca4c4bb92f4d6af9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigMetastoreConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_metastore_service": "dataprocMetastoreService"},
)
class DataprocClusterClusterConfigMetastoreConfig:
    def __init__(self, *, dataproc_metastore_service: builtins.str) -> None:
        '''
        :param dataproc_metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#dataproc_metastore_service DataprocCluster#dataproc_metastore_service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d078ca40cdff638ab61c7c480d496ab7765500ff85fe007c73fedc875e16b0)
            check_type(argname="argument dataproc_metastore_service", value=dataproc_metastore_service, expected_type=type_hints["dataproc_metastore_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataproc_metastore_service": dataproc_metastore_service,
        }

    @builtins.property
    def dataproc_metastore_service(self) -> builtins.str:
        '''Resource name of an existing Dataproc Metastore service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#dataproc_metastore_service DataprocCluster#dataproc_metastore_service}
        '''
        result = self._values.get("dataproc_metastore_service")
        assert result is not None, "Required property 'dataproc_metastore_service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigMetastoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigMetastoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigMetastoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aba729f4bdc9f6d373a0d0d3c3c8f7509e99a16e4afaf933f0df6ead8c33a530)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dataprocMetastoreServiceInput")
    def dataproc_metastore_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocMetastoreServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocMetastoreService")
    def dataproc_metastore_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataprocMetastoreService"))

    @dataproc_metastore_service.setter
    def dataproc_metastore_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4855fe35b045b79b5547b658b97b3fc996feeb3d71791d371c3da93ebaa37ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocMetastoreService", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigMetastoreConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigMetastoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigMetastoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bc5c0b97177cfcf9ad58b98d2cb136187d475c23b502be3c976d05f8fc8d4d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97d786ca78e84d1a0aa8b4147f8fee7ea7c567690ad0f6cc4f8e43ecac653454)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingConfig")
    def put_autoscaling_config(self, *, policy_uri: builtins.str) -> None:
        '''
        :param policy_uri: The autoscaling policy used by the cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#policy_uri DataprocCluster#policy_uri}
        '''
        value = DataprocClusterClusterConfigAutoscalingConfig(policy_uri=policy_uri)

        return typing.cast(None, jsii.invoke(self, "putAutoscalingConfig", [value]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: The Cloud KMS key name to use for PD disk encryption for all instances in the cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kms_key_name DataprocCluster#kms_key_name}
        '''
        value = DataprocClusterClusterConfigEncryptionConfig(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putEndpointConfig")
    def put_endpoint_config(
        self,
        *,
        enable_http_port_access: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_http_port_access: The flag to enable http access to specific ports on the cluster from external sources (aka Component Gateway). Defaults to false. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_http_port_access DataprocCluster#enable_http_port_access}
        '''
        value = DataprocClusterClusterConfigEndpointConfig(
            enable_http_port_access=enable_http_port_access
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointConfig", [value]))

    @jsii.member(jsii_name="putGceClusterConfig")
    def put_gce_cluster_config(
        self,
        *,
        internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        shielded_instance_config: typing.Optional[typing.Union[DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param internal_ip_only: By default, clusters are not restricted to internal IP addresses, and will have ephemeral external IP addresses assigned to each instance. If set to true, all instances in the cluster will only have internal IP addresses. Note: Private Google Access (also known as privateIpGoogleAccess) must be enabled on the subnetwork that the cluster will be launched in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#internal_ip_only DataprocCluster#internal_ip_only}
        :param metadata: A map of the Compute Engine metadata entries to add to all instances. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#metadata DataprocCluster#metadata}
        :param network: The name or self_link of the Google Compute Engine network to the cluster will be part of. Conflicts with subnetwork. If neither is specified, this defaults to the "default" network. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#network DataprocCluster#network}
        :param service_account: The service account to be used by the Node VMs. If not specified, the "default" service account is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#service_account DataprocCluster#service_account}
        :param service_account_scopes: The set of Google API scopes to be made available on all of the node VMs under the service_account specified. These can be either FQDNs, or scope aliases. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#service_account_scopes DataprocCluster#service_account_scopes}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#shielded_instance_config DataprocCluster#shielded_instance_config}
        :param subnetwork: The name or self_link of the Google Compute Engine subnetwork the cluster will be part of. Conflicts with network. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#subnetwork DataprocCluster#subnetwork}
        :param tags: The list of instance tags applied to instances in the cluster. Tags are used to identify valid sources or targets for network firewalls. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#tags DataprocCluster#tags}
        :param zone: The GCP zone where your data is stored and used (i.e. where the master and the worker nodes will be created in). If region is set to 'global' (default) then zone is mandatory, otherwise GCP is able to make use of Auto Zone Placement to determine this automatically for you. Note: This setting additionally determines and restricts which computing resources are available for use with other configs such as cluster_config.master_config.machine_type and cluster_config.worker_config.machine_type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#zone DataprocCluster#zone}
        '''
        value = DataprocClusterClusterConfigGceClusterConfig(
            internal_ip_only=internal_ip_only,
            metadata=metadata,
            network=network,
            service_account=service_account,
            service_account_scopes=service_account_scopes,
            shielded_instance_config=shielded_instance_config,
            subnetwork=subnetwork,
            tags=tags,
            zone=zone,
        )

        return typing.cast(None, jsii.invoke(self, "putGceClusterConfig", [value]))

    @jsii.member(jsii_name="putInitializationAction")
    def put_initialization_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterClusterConfigInitializationAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c514f3665386fd2ebd5b1c0a3a917b5b75a0b5175c60d087cf152d767b3c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInitializationAction", [value]))

    @jsii.member(jsii_name="putLifecycleConfig")
    def put_lifecycle_config(
        self,
        *,
        auto_delete_time: typing.Optional[builtins.str] = None,
        idle_delete_ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_delete_time: The time when cluster will be auto-deleted. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#auto_delete_time DataprocCluster#auto_delete_time}
        :param idle_delete_ttl: The duration to keep the cluster alive while idling (no jobs running). After this TTL, the cluster will be deleted. Valid range: [10m, 14d]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#idle_delete_ttl DataprocCluster#idle_delete_ttl}
        '''
        value = DataprocClusterClusterConfigLifecycleConfig(
            auto_delete_time=auto_delete_time, idle_delete_ttl=idle_delete_ttl
        )

        return typing.cast(None, jsii.invoke(self, "putLifecycleConfig", [value]))

    @jsii.member(jsii_name="putMasterConfig")
    def put_master_config(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union[DataprocClusterClusterConfigMasterConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerators DataprocCluster#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#disk_config DataprocCluster#disk_config}
        :param image_uri: The URI for the image to use for this master/worker. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#image_uri DataprocCluster#image_uri}
        :param machine_type: The name of a Google Compute Engine machine type to create for the master/worker. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#machine_type DataprocCluster#machine_type}
        :param min_cpu_platform: The name of a minimum generation of CPU family for the master/worker. If not specified, GCP will default to a predetermined computed value for each zone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_cpu_platform DataprocCluster#min_cpu_platform}
        :param num_instances: Specifies the number of master/worker nodes to create. If not specified, GCP will default to a predetermined computed value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_instances DataprocCluster#num_instances}
        '''
        value = DataprocClusterClusterConfigMasterConfig(
            accelerators=accelerators,
            disk_config=disk_config,
            image_uri=image_uri,
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
            num_instances=num_instances,
        )

        return typing.cast(None, jsii.invoke(self, "putMasterConfig", [value]))

    @jsii.member(jsii_name="putMetastoreConfig")
    def put_metastore_config(self, *, dataproc_metastore_service: builtins.str) -> None:
        '''
        :param dataproc_metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#dataproc_metastore_service DataprocCluster#dataproc_metastore_service}
        '''
        value = DataprocClusterClusterConfigMetastoreConfig(
            dataproc_metastore_service=dataproc_metastore_service
        )

        return typing.cast(None, jsii.invoke(self, "putMetastoreConfig", [value]))

    @jsii.member(jsii_name="putPreemptibleWorkerConfig")
    def put_preemptible_worker_config(
        self,
        *,
        disk_config: typing.Optional[typing.Union["DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        num_instances: typing.Optional[jsii.Number] = None,
        preemptibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#disk_config DataprocCluster#disk_config}
        :param num_instances: Specifies the number of preemptible nodes to create. Defaults to 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_instances DataprocCluster#num_instances}
        :param preemptibility: Specifies the preemptibility of the secondary nodes. Defaults to PREEMPTIBLE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#preemptibility DataprocCluster#preemptibility}
        '''
        value = DataprocClusterClusterConfigPreemptibleWorkerConfig(
            disk_config=disk_config,
            num_instances=num_instances,
            preemptibility=preemptibility,
        )

        return typing.cast(None, jsii.invoke(self, "putPreemptibleWorkerConfig", [value]))

    @jsii.member(jsii_name="putSecurityConfig")
    def put_security_config(
        self,
        *,
        kerberos_config: typing.Union["DataprocClusterClusterConfigSecurityConfigKerberosConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param kerberos_config: kerberos_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kerberos_config DataprocCluster#kerberos_config}
        '''
        value = DataprocClusterClusterConfigSecurityConfig(
            kerberos_config=kerberos_config
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityConfig", [value]))

    @jsii.member(jsii_name="putSoftwareConfig")
    def put_software_config(
        self,
        *,
        image_version: typing.Optional[builtins.str] = None,
        optional_components: typing.Optional[typing.Sequence[builtins.str]] = None,
        override_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param image_version: The Cloud Dataproc image version to use for the cluster - this controls the sets of software versions installed onto the nodes when you create clusters. If not specified, defaults to the latest version. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#image_version DataprocCluster#image_version}
        :param optional_components: The set of optional components to activate on the cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#optional_components DataprocCluster#optional_components}
        :param override_properties: A list of override and additional properties (key/value pairs) used to modify various aspects of the common configuration files used when creating a cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#override_properties DataprocCluster#override_properties}
        '''
        value = DataprocClusterClusterConfigSoftwareConfig(
            image_version=image_version,
            optional_components=optional_components,
            override_properties=override_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putSoftwareConfig", [value]))

    @jsii.member(jsii_name="putWorkerConfig")
    def put_worker_config(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocClusterClusterConfigWorkerConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["DataprocClusterClusterConfigWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerators DataprocCluster#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#disk_config DataprocCluster#disk_config}
        :param image_uri: The URI for the image to use for this master/worker. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#image_uri DataprocCluster#image_uri}
        :param machine_type: The name of a Google Compute Engine machine type to create for the master/worker. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#machine_type DataprocCluster#machine_type}
        :param min_cpu_platform: The name of a minimum generation of CPU family for the master/worker. If not specified, GCP will default to a predetermined computed value for each zone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_cpu_platform DataprocCluster#min_cpu_platform}
        :param num_instances: Specifies the number of master/worker nodes to create. If not specified, GCP will default to a predetermined computed value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_instances DataprocCluster#num_instances}
        '''
        value = DataprocClusterClusterConfigWorkerConfig(
            accelerators=accelerators,
            disk_config=disk_config,
            image_uri=image_uri,
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
            num_instances=num_instances,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkerConfig", [value]))

    @jsii.member(jsii_name="resetAutoscalingConfig")
    def reset_autoscaling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingConfig", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetEndpointConfig")
    def reset_endpoint_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointConfig", []))

    @jsii.member(jsii_name="resetGceClusterConfig")
    def reset_gce_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGceClusterConfig", []))

    @jsii.member(jsii_name="resetInitializationAction")
    def reset_initialization_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitializationAction", []))

    @jsii.member(jsii_name="resetLifecycleConfig")
    def reset_lifecycle_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfig", []))

    @jsii.member(jsii_name="resetMasterConfig")
    def reset_master_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterConfig", []))

    @jsii.member(jsii_name="resetMetastoreConfig")
    def reset_metastore_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastoreConfig", []))

    @jsii.member(jsii_name="resetPreemptibleWorkerConfig")
    def reset_preemptible_worker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptibleWorkerConfig", []))

    @jsii.member(jsii_name="resetSecurityConfig")
    def reset_security_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfig", []))

    @jsii.member(jsii_name="resetSoftwareConfig")
    def reset_software_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoftwareConfig", []))

    @jsii.member(jsii_name="resetStagingBucket")
    def reset_staging_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagingBucket", []))

    @jsii.member(jsii_name="resetTempBucket")
    def reset_temp_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTempBucket", []))

    @jsii.member(jsii_name="resetWorkerConfig")
    def reset_worker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerConfig", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingConfig")
    def autoscaling_config(
        self,
    ) -> DataprocClusterClusterConfigAutoscalingConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigAutoscalingConfigOutputReference, jsii.get(self, "autoscalingConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> DataprocClusterClusterConfigEncryptionConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigEncryptionConfigOutputReference, jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfig")
    def endpoint_config(
        self,
    ) -> DataprocClusterClusterConfigEndpointConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigEndpointConfigOutputReference, jsii.get(self, "endpointConfig"))

    @builtins.property
    @jsii.member(jsii_name="gceClusterConfig")
    def gce_cluster_config(
        self,
    ) -> DataprocClusterClusterConfigGceClusterConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigGceClusterConfigOutputReference, jsii.get(self, "gceClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="initializationAction")
    def initialization_action(
        self,
    ) -> DataprocClusterClusterConfigInitializationActionList:
        return typing.cast(DataprocClusterClusterConfigInitializationActionList, jsii.get(self, "initializationAction"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfig")
    def lifecycle_config(
        self,
    ) -> DataprocClusterClusterConfigLifecycleConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigLifecycleConfigOutputReference, jsii.get(self, "lifecycleConfig"))

    @builtins.property
    @jsii.member(jsii_name="masterConfig")
    def master_config(self) -> DataprocClusterClusterConfigMasterConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigMasterConfigOutputReference, jsii.get(self, "masterConfig"))

    @builtins.property
    @jsii.member(jsii_name="metastoreConfig")
    def metastore_config(
        self,
    ) -> DataprocClusterClusterConfigMetastoreConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigMetastoreConfigOutputReference, jsii.get(self, "metastoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="preemptibleWorkerConfig")
    def preemptible_worker_config(
        self,
    ) -> "DataprocClusterClusterConfigPreemptibleWorkerConfigOutputReference":
        return typing.cast("DataprocClusterClusterConfigPreemptibleWorkerConfigOutputReference", jsii.get(self, "preemptibleWorkerConfig"))

    @builtins.property
    @jsii.member(jsii_name="securityConfig")
    def security_config(
        self,
    ) -> "DataprocClusterClusterConfigSecurityConfigOutputReference":
        return typing.cast("DataprocClusterClusterConfigSecurityConfigOutputReference", jsii.get(self, "securityConfig"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfig")
    def software_config(
        self,
    ) -> "DataprocClusterClusterConfigSoftwareConfigOutputReference":
        return typing.cast("DataprocClusterClusterConfigSoftwareConfigOutputReference", jsii.get(self, "softwareConfig"))

    @builtins.property
    @jsii.member(jsii_name="workerConfig")
    def worker_config(
        self,
    ) -> "DataprocClusterClusterConfigWorkerConfigOutputReference":
        return typing.cast("DataprocClusterClusterConfigWorkerConfigOutputReference", jsii.get(self, "workerConfig"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingConfigInput")
    def autoscaling_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigAutoscalingConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigAutoscalingConfig], jsii.get(self, "autoscalingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigEncryptionConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigEncryptionConfig], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfigInput")
    def endpoint_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigEndpointConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigEndpointConfig], jsii.get(self, "endpointConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="gceClusterConfigInput")
    def gce_cluster_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigGceClusterConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigGceClusterConfig], jsii.get(self, "gceClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="initializationActionInput")
    def initialization_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigInitializationAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigInitializationAction]]], jsii.get(self, "initializationActionInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigInput")
    def lifecycle_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigLifecycleConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigLifecycleConfig], jsii.get(self, "lifecycleConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="masterConfigInput")
    def master_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigMasterConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigMasterConfig], jsii.get(self, "masterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metastoreConfigInput")
    def metastore_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigMetastoreConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigMetastoreConfig], jsii.get(self, "metastoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibleWorkerConfigInput")
    def preemptible_worker_config_input(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigPreemptibleWorkerConfig"]:
        return typing.cast(typing.Optional["DataprocClusterClusterConfigPreemptibleWorkerConfig"], jsii.get(self, "preemptibleWorkerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigInput")
    def security_config_input(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigSecurityConfig"]:
        return typing.cast(typing.Optional["DataprocClusterClusterConfigSecurityConfig"], jsii.get(self, "securityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="softwareConfigInput")
    def software_config_input(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigSoftwareConfig"]:
        return typing.cast(typing.Optional["DataprocClusterClusterConfigSoftwareConfig"], jsii.get(self, "softwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucketInput")
    def staging_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="tempBucketInput")
    def temp_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tempBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="workerConfigInput")
    def worker_config_input(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigWorkerConfig"]:
        return typing.cast(typing.Optional["DataprocClusterClusterConfigWorkerConfig"], jsii.get(self, "workerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucket")
    def staging_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingBucket"))

    @staging_bucket.setter
    def staging_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9577ed9e732b663f0d86025c39fcd68a1f51b55213d09d9d7c76c9e91226433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingBucket", value)

    @builtins.property
    @jsii.member(jsii_name="tempBucket")
    def temp_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tempBucket"))

    @temp_bucket.setter
    def temp_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9aef639e8148b47aeb33614b5e3cdc7fad7f9a7b1c34904f1ecb4de1c8c3fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tempBucket", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocClusterClusterConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69266c0b3947471dc43cd9a334e6dba69f148a709926f2c86b7f6b734916e6fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigPreemptibleWorkerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "disk_config": "diskConfig",
        "num_instances": "numInstances",
        "preemptibility": "preemptibility",
    },
)
class DataprocClusterClusterConfigPreemptibleWorkerConfig:
    def __init__(
        self,
        *,
        disk_config: typing.Optional[typing.Union["DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        num_instances: typing.Optional[jsii.Number] = None,
        preemptibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#disk_config DataprocCluster#disk_config}
        :param num_instances: Specifies the number of preemptible nodes to create. Defaults to 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_instances DataprocCluster#num_instances}
        :param preemptibility: Specifies the preemptibility of the secondary nodes. Defaults to PREEMPTIBLE. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#preemptibility DataprocCluster#preemptibility}
        '''
        if isinstance(disk_config, dict):
            disk_config = DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig(**disk_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49bf03f523760e43e550b4f98a609b968d5ef099cf4a9e0dc44d9dd5215922c1)
            check_type(argname="argument disk_config", value=disk_config, expected_type=type_hints["disk_config"])
            check_type(argname="argument num_instances", value=num_instances, expected_type=type_hints["num_instances"])
            check_type(argname="argument preemptibility", value=preemptibility, expected_type=type_hints["preemptibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_config is not None:
            self._values["disk_config"] = disk_config
        if num_instances is not None:
            self._values["num_instances"] = num_instances
        if preemptibility is not None:
            self._values["preemptibility"] = preemptibility

    @builtins.property
    def disk_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig"]:
        '''disk_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#disk_config DataprocCluster#disk_config}
        '''
        result = self._values.get("disk_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig"], result)

    @builtins.property
    def num_instances(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of preemptible nodes to create. Defaults to 0.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_instances DataprocCluster#num_instances}
        '''
        result = self._values.get("num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preemptibility(self) -> typing.Optional[builtins.str]:
        '''Specifies the preemptibility of the secondary nodes. Defaults to PREEMPTIBLE.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#preemptibility DataprocCluster#preemptibility}
        '''
        result = self._values.get("preemptibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigPreemptibleWorkerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "num_local_ssds": "numLocalSsds",
    },
)
class DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig:
    def __init__(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each preemptible worker node, specified in GB. The smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_size_gb DataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each preemptible worker node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_type DataprocCluster#boot_disk_type}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each preemptible worker node. Defaults to 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_local_ssds DataprocCluster#num_local_ssds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6285385062cd45cee0d2d61128dc4b4d340e186e4b621012f4f52abad1000067)
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument num_local_ssds", value=num_local_ssds, expected_type=type_hints["num_local_ssds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if num_local_ssds is not None:
            self._values["num_local_ssds"] = num_local_ssds

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the primary disk attached to each preemptible worker node, specified in GB.

        The smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_size_gb DataprocCluster#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''The disk type of the primary disk attached to each preemptible worker node.

        Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_type DataprocCluster#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_local_ssds(self) -> typing.Optional[jsii.Number]:
        '''The amount of local SSD disks that will be attached to each preemptible worker node. Defaults to 0.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_local_ssds DataprocCluster#num_local_ssds}
        '''
        result = self._values.get("num_local_ssds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5665c060036ddc6b12495e64980e3c69be44dc4755649d87434f4c7ddf134d52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetNumLocalSsds")
    def reset_num_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLocalSsds", []))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="numLocalSsdsInput")
    def num_local_ssds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLocalSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085d649f74d2278f8c18895b22fe17f4a0fa58574dc66ac4de21fd06ebe8cc5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value)

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be222f0640520593d58c2d5a603e39fb5040909f97cf6dbebcf5de378c753424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value)

    @builtins.property
    @jsii.member(jsii_name="numLocalSsds")
    def num_local_ssds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLocalSsds"))

    @num_local_ssds.setter
    def num_local_ssds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e552a83c928b054a735d1a845c18e90bce9c2a57f2e4355595c4d3d9197cd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLocalSsds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea3c1ce490dbde957d5cbfee16cd4847b814a9d9513b9cc5442294ced16716d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterClusterConfigPreemptibleWorkerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigPreemptibleWorkerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b548f1b6c480c65f9c245698eb78bcb20a397e9c9fa4e10bb7e8cf1e0314304a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDiskConfig")
    def put_disk_config(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each preemptible worker node, specified in GB. The smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_size_gb DataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each preemptible worker node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_type DataprocCluster#boot_disk_type}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each preemptible worker node. Defaults to 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_local_ssds DataprocCluster#num_local_ssds}
        '''
        value = DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig(
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            num_local_ssds=num_local_ssds,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskConfig", [value]))

    @jsii.member(jsii_name="resetDiskConfig")
    def reset_disk_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConfig", []))

    @jsii.member(jsii_name="resetNumInstances")
    def reset_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumInstances", []))

    @jsii.member(jsii_name="resetPreemptibility")
    def reset_preemptibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptibility", []))

    @builtins.property
    @jsii.member(jsii_name="diskConfig")
    def disk_config(
        self,
    ) -> DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfigOutputReference, jsii.get(self, "diskConfig"))

    @builtins.property
    @jsii.member(jsii_name="instanceNames")
    def instance_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNames"))

    @builtins.property
    @jsii.member(jsii_name="diskConfigInput")
    def disk_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig], jsii.get(self, "diskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstancesInput")
    def num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibilityInput")
    def preemptibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstances")
    def num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numInstances"))

    @num_instances.setter
    def num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547ff68502839cf6258112376af9a49ef86cccd429ef88083a60624d499a3c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numInstances", value)

    @builtins.property
    @jsii.member(jsii_name="preemptibility")
    def preemptibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptibility"))

    @preemptibility.setter
    def preemptibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3add78efaaf5d613d77783fdd67354d8c0f2ad69e538ffc9ccd1ddcb8a0cb79c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptibility", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigPreemptibleWorkerConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigPreemptibleWorkerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigPreemptibleWorkerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f8bcd5221db8064a8553b94eaaef714ec31e7a53061f31e3efd24736056e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"kerberos_config": "kerberosConfig"},
)
class DataprocClusterClusterConfigSecurityConfig:
    def __init__(
        self,
        *,
        kerberos_config: typing.Union["DataprocClusterClusterConfigSecurityConfigKerberosConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param kerberos_config: kerberos_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kerberos_config DataprocCluster#kerberos_config}
        '''
        if isinstance(kerberos_config, dict):
            kerberos_config = DataprocClusterClusterConfigSecurityConfigKerberosConfig(**kerberos_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d38c767b44cb6f9387afc5039914ebe605b98825b9055955ae32395941951629)
            check_type(argname="argument kerberos_config", value=kerberos_config, expected_type=type_hints["kerberos_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kerberos_config": kerberos_config,
        }

    @builtins.property
    def kerberos_config(
        self,
    ) -> "DataprocClusterClusterConfigSecurityConfigKerberosConfig":
        '''kerberos_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kerberos_config DataprocCluster#kerberos_config}
        '''
        result = self._values.get("kerberos_config")
        assert result is not None, "Required property 'kerberos_config' is missing"
        return typing.cast("DataprocClusterClusterConfigSecurityConfigKerberosConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigSecurityConfigKerberosConfig",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_uri": "kmsKeyUri",
        "root_principal_password_uri": "rootPrincipalPasswordUri",
        "cross_realm_trust_admin_server": "crossRealmTrustAdminServer",
        "cross_realm_trust_kdc": "crossRealmTrustKdc",
        "cross_realm_trust_realm": "crossRealmTrustRealm",
        "cross_realm_trust_shared_password_uri": "crossRealmTrustSharedPasswordUri",
        "enable_kerberos": "enableKerberos",
        "kdc_db_key_uri": "kdcDbKeyUri",
        "key_password_uri": "keyPasswordUri",
        "keystore_password_uri": "keystorePasswordUri",
        "keystore_uri": "keystoreUri",
        "realm": "realm",
        "tgt_lifetime_hours": "tgtLifetimeHours",
        "truststore_password_uri": "truststorePasswordUri",
        "truststore_uri": "truststoreUri",
    },
)
class DataprocClusterClusterConfigSecurityConfigKerberosConfig:
    def __init__(
        self,
        *,
        kms_key_uri: builtins.str,
        root_principal_password_uri: builtins.str,
        cross_realm_trust_admin_server: typing.Optional[builtins.str] = None,
        cross_realm_trust_kdc: typing.Optional[builtins.str] = None,
        cross_realm_trust_realm: typing.Optional[builtins.str] = None,
        cross_realm_trust_shared_password_uri: typing.Optional[builtins.str] = None,
        enable_kerberos: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kdc_db_key_uri: typing.Optional[builtins.str] = None,
        key_password_uri: typing.Optional[builtins.str] = None,
        keystore_password_uri: typing.Optional[builtins.str] = None,
        keystore_uri: typing.Optional[builtins.str] = None,
        realm: typing.Optional[builtins.str] = None,
        tgt_lifetime_hours: typing.Optional[jsii.Number] = None,
        truststore_password_uri: typing.Optional[builtins.str] = None,
        truststore_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_uri: The uri of the KMS key used to encrypt various sensitive files. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kms_key_uri DataprocCluster#kms_key_uri}
        :param root_principal_password_uri: The cloud Storage URI of a KMS encrypted file containing the root principal password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#root_principal_password_uri DataprocCluster#root_principal_password_uri}
        :param cross_realm_trust_admin_server: The admin server (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_admin_server DataprocCluster#cross_realm_trust_admin_server}
        :param cross_realm_trust_kdc: The KDC (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_kdc DataprocCluster#cross_realm_trust_kdc}
        :param cross_realm_trust_realm: The remote realm the Dataproc on-cluster KDC will trust, should the user enable cross realm trust. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_realm DataprocCluster#cross_realm_trust_realm}
        :param cross_realm_trust_shared_password_uri: The Cloud Storage URI of a KMS encrypted file containing the shared password between the on-cluster Kerberos realm and the remote trusted realm, in a cross realm trust relationship. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_shared_password_uri DataprocCluster#cross_realm_trust_shared_password_uri}
        :param enable_kerberos: Flag to indicate whether to Kerberize the cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_kerberos DataprocCluster#enable_kerberos}
        :param kdc_db_key_uri: The Cloud Storage URI of a KMS encrypted file containing the master key of the KDC database. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kdc_db_key_uri DataprocCluster#kdc_db_key_uri}
        :param key_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided key. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#key_password_uri DataprocCluster#key_password_uri}
        :param keystore_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided keystore. For the self-signed certificate, this password is generated by Dataproc Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#keystore_password_uri DataprocCluster#keystore_password_uri}
        :param keystore_uri: The Cloud Storage URI of the keystore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#keystore_uri DataprocCluster#keystore_uri}
        :param realm: The name of the on-cluster Kerberos realm. If not specified, the uppercased domain of hostnames will be the realm. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#realm DataprocCluster#realm}
        :param tgt_lifetime_hours: The lifetime of the ticket granting ticket, in hours. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#tgt_lifetime_hours DataprocCluster#tgt_lifetime_hours}
        :param truststore_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided truststore. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#truststore_password_uri DataprocCluster#truststore_password_uri}
        :param truststore_uri: The Cloud Storage URI of the truststore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#truststore_uri DataprocCluster#truststore_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503f77456cabd2cfc22147b6e67e4dc96357f993b34d929ac452aee3125d2e0c)
            check_type(argname="argument kms_key_uri", value=kms_key_uri, expected_type=type_hints["kms_key_uri"])
            check_type(argname="argument root_principal_password_uri", value=root_principal_password_uri, expected_type=type_hints["root_principal_password_uri"])
            check_type(argname="argument cross_realm_trust_admin_server", value=cross_realm_trust_admin_server, expected_type=type_hints["cross_realm_trust_admin_server"])
            check_type(argname="argument cross_realm_trust_kdc", value=cross_realm_trust_kdc, expected_type=type_hints["cross_realm_trust_kdc"])
            check_type(argname="argument cross_realm_trust_realm", value=cross_realm_trust_realm, expected_type=type_hints["cross_realm_trust_realm"])
            check_type(argname="argument cross_realm_trust_shared_password_uri", value=cross_realm_trust_shared_password_uri, expected_type=type_hints["cross_realm_trust_shared_password_uri"])
            check_type(argname="argument enable_kerberos", value=enable_kerberos, expected_type=type_hints["enable_kerberos"])
            check_type(argname="argument kdc_db_key_uri", value=kdc_db_key_uri, expected_type=type_hints["kdc_db_key_uri"])
            check_type(argname="argument key_password_uri", value=key_password_uri, expected_type=type_hints["key_password_uri"])
            check_type(argname="argument keystore_password_uri", value=keystore_password_uri, expected_type=type_hints["keystore_password_uri"])
            check_type(argname="argument keystore_uri", value=keystore_uri, expected_type=type_hints["keystore_uri"])
            check_type(argname="argument realm", value=realm, expected_type=type_hints["realm"])
            check_type(argname="argument tgt_lifetime_hours", value=tgt_lifetime_hours, expected_type=type_hints["tgt_lifetime_hours"])
            check_type(argname="argument truststore_password_uri", value=truststore_password_uri, expected_type=type_hints["truststore_password_uri"])
            check_type(argname="argument truststore_uri", value=truststore_uri, expected_type=type_hints["truststore_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_uri": kms_key_uri,
            "root_principal_password_uri": root_principal_password_uri,
        }
        if cross_realm_trust_admin_server is not None:
            self._values["cross_realm_trust_admin_server"] = cross_realm_trust_admin_server
        if cross_realm_trust_kdc is not None:
            self._values["cross_realm_trust_kdc"] = cross_realm_trust_kdc
        if cross_realm_trust_realm is not None:
            self._values["cross_realm_trust_realm"] = cross_realm_trust_realm
        if cross_realm_trust_shared_password_uri is not None:
            self._values["cross_realm_trust_shared_password_uri"] = cross_realm_trust_shared_password_uri
        if enable_kerberos is not None:
            self._values["enable_kerberos"] = enable_kerberos
        if kdc_db_key_uri is not None:
            self._values["kdc_db_key_uri"] = kdc_db_key_uri
        if key_password_uri is not None:
            self._values["key_password_uri"] = key_password_uri
        if keystore_password_uri is not None:
            self._values["keystore_password_uri"] = keystore_password_uri
        if keystore_uri is not None:
            self._values["keystore_uri"] = keystore_uri
        if realm is not None:
            self._values["realm"] = realm
        if tgt_lifetime_hours is not None:
            self._values["tgt_lifetime_hours"] = tgt_lifetime_hours
        if truststore_password_uri is not None:
            self._values["truststore_password_uri"] = truststore_password_uri
        if truststore_uri is not None:
            self._values["truststore_uri"] = truststore_uri

    @builtins.property
    def kms_key_uri(self) -> builtins.str:
        '''The uri of the KMS key used to encrypt various sensitive files.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kms_key_uri DataprocCluster#kms_key_uri}
        '''
        result = self._values.get("kms_key_uri")
        assert result is not None, "Required property 'kms_key_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_principal_password_uri(self) -> builtins.str:
        '''The cloud Storage URI of a KMS encrypted file containing the root principal password.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#root_principal_password_uri DataprocCluster#root_principal_password_uri}
        '''
        result = self._values.get("root_principal_password_uri")
        assert result is not None, "Required property 'root_principal_password_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cross_realm_trust_admin_server(self) -> typing.Optional[builtins.str]:
        '''The admin server (IP or hostname) for the remote trusted realm in a cross realm trust relationship.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_admin_server DataprocCluster#cross_realm_trust_admin_server}
        '''
        result = self._values.get("cross_realm_trust_admin_server")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_realm_trust_kdc(self) -> typing.Optional[builtins.str]:
        '''The KDC (IP or hostname) for the remote trusted realm in a cross realm trust relationship.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_kdc DataprocCluster#cross_realm_trust_kdc}
        '''
        result = self._values.get("cross_realm_trust_kdc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_realm_trust_realm(self) -> typing.Optional[builtins.str]:
        '''The remote realm the Dataproc on-cluster KDC will trust, should the user enable cross realm trust.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_realm DataprocCluster#cross_realm_trust_realm}
        '''
        result = self._values.get("cross_realm_trust_realm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cross_realm_trust_shared_password_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of a KMS encrypted file containing the shared password between the on-cluster Kerberos realm and the remote trusted realm, in a cross realm trust relationship.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_shared_password_uri DataprocCluster#cross_realm_trust_shared_password_uri}
        '''
        result = self._values.get("cross_realm_trust_shared_password_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_kerberos(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag to indicate whether to Kerberize the cluster.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_kerberos DataprocCluster#enable_kerberos}
        '''
        result = self._values.get("enable_kerberos")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kdc_db_key_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of a KMS encrypted file containing the master key of the KDC database.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kdc_db_key_uri DataprocCluster#kdc_db_key_uri}
        '''
        result = self._values.get("kdc_db_key_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_password_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of a KMS encrypted file containing the password to the user provided key.

        For the self-signed certificate, this password is generated by Dataproc.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#key_password_uri DataprocCluster#key_password_uri}
        '''
        result = self._values.get("key_password_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keystore_password_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of a KMS encrypted file containing the password to the user provided keystore.

        For the self-signed certificate, this password is generated
        by Dataproc

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#keystore_password_uri DataprocCluster#keystore_password_uri}
        '''
        result = self._values.get("keystore_password_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keystore_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of the keystore file used for SSL encryption.

        If not provided, Dataproc will provide a self-signed certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#keystore_uri DataprocCluster#keystore_uri}
        '''
        result = self._values.get("keystore_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realm(self) -> typing.Optional[builtins.str]:
        '''The name of the on-cluster Kerberos realm. If not specified, the uppercased domain of hostnames will be the realm.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#realm DataprocCluster#realm}
        '''
        result = self._values.get("realm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tgt_lifetime_hours(self) -> typing.Optional[jsii.Number]:
        '''The lifetime of the ticket granting ticket, in hours.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#tgt_lifetime_hours DataprocCluster#tgt_lifetime_hours}
        '''
        result = self._values.get("tgt_lifetime_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def truststore_password_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of a KMS encrypted file containing the password to the user provided truststore.

        For the self-signed certificate, this password is generated by Dataproc.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#truststore_password_uri DataprocCluster#truststore_password_uri}
        '''
        result = self._values.get("truststore_password_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def truststore_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of the truststore file used for SSL encryption.

        If not provided, Dataproc will provide a self-signed certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#truststore_uri DataprocCluster#truststore_uri}
        '''
        result = self._values.get("truststore_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigSecurityConfigKerberosConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigSecurityConfigKerberosConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigSecurityConfigKerberosConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1f76ab8feebdd90b10fca4b9da15a0cdd7cc685206c0bb2bb7bca50055cf40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCrossRealmTrustAdminServer")
    def reset_cross_realm_trust_admin_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustAdminServer", []))

    @jsii.member(jsii_name="resetCrossRealmTrustKdc")
    def reset_cross_realm_trust_kdc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustKdc", []))

    @jsii.member(jsii_name="resetCrossRealmTrustRealm")
    def reset_cross_realm_trust_realm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustRealm", []))

    @jsii.member(jsii_name="resetCrossRealmTrustSharedPasswordUri")
    def reset_cross_realm_trust_shared_password_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossRealmTrustSharedPasswordUri", []))

    @jsii.member(jsii_name="resetEnableKerberos")
    def reset_enable_kerberos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableKerberos", []))

    @jsii.member(jsii_name="resetKdcDbKeyUri")
    def reset_kdc_db_key_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKdcDbKeyUri", []))

    @jsii.member(jsii_name="resetKeyPasswordUri")
    def reset_key_password_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPasswordUri", []))

    @jsii.member(jsii_name="resetKeystorePasswordUri")
    def reset_keystore_password_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeystorePasswordUri", []))

    @jsii.member(jsii_name="resetKeystoreUri")
    def reset_keystore_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeystoreUri", []))

    @jsii.member(jsii_name="resetRealm")
    def reset_realm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealm", []))

    @jsii.member(jsii_name="resetTgtLifetimeHours")
    def reset_tgt_lifetime_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTgtLifetimeHours", []))

    @jsii.member(jsii_name="resetTruststorePasswordUri")
    def reset_truststore_password_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTruststorePasswordUri", []))

    @jsii.member(jsii_name="resetTruststoreUri")
    def reset_truststore_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTruststoreUri", []))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustAdminServerInput")
    def cross_realm_trust_admin_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustAdminServerInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustKdcInput")
    def cross_realm_trust_kdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustKdcInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustRealmInput")
    def cross_realm_trust_realm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustRealmInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustSharedPasswordUriInput")
    def cross_realm_trust_shared_password_uri_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crossRealmTrustSharedPasswordUriInput"))

    @builtins.property
    @jsii.member(jsii_name="enableKerberosInput")
    def enable_kerberos_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableKerberosInput"))

    @builtins.property
    @jsii.member(jsii_name="kdcDbKeyUriInput")
    def kdc_db_key_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kdcDbKeyUriInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPasswordUriInput")
    def key_password_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPasswordUriInput"))

    @builtins.property
    @jsii.member(jsii_name="keystorePasswordUriInput")
    def keystore_password_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keystorePasswordUriInput"))

    @builtins.property
    @jsii.member(jsii_name="keystoreUriInput")
    def keystore_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keystoreUriInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyUriInput")
    def kms_key_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyUriInput"))

    @builtins.property
    @jsii.member(jsii_name="realmInput")
    def realm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "realmInput"))

    @builtins.property
    @jsii.member(jsii_name="rootPrincipalPasswordUriInput")
    def root_principal_password_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootPrincipalPasswordUriInput"))

    @builtins.property
    @jsii.member(jsii_name="tgtLifetimeHoursInput")
    def tgt_lifetime_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tgtLifetimeHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="truststorePasswordUriInput")
    def truststore_password_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "truststorePasswordUriInput"))

    @builtins.property
    @jsii.member(jsii_name="truststoreUriInput")
    def truststore_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "truststoreUriInput"))

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustAdminServer")
    def cross_realm_trust_admin_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustAdminServer"))

    @cross_realm_trust_admin_server.setter
    def cross_realm_trust_admin_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c857382d99784846617c163b38357eedd6160b4fe0b44a8bad3ef0725e9fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustAdminServer", value)

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustKdc")
    def cross_realm_trust_kdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustKdc"))

    @cross_realm_trust_kdc.setter
    def cross_realm_trust_kdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc68b74a37e183b36a95614a8c98ee78b22be75644aae34cfca307507d5ab45e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustKdc", value)

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustRealm")
    def cross_realm_trust_realm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustRealm"))

    @cross_realm_trust_realm.setter
    def cross_realm_trust_realm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c62d8205ba2cd9fc1d1f3ff858b334088c6a859cc2dc1c414f80d3adef8de56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustRealm", value)

    @builtins.property
    @jsii.member(jsii_name="crossRealmTrustSharedPasswordUri")
    def cross_realm_trust_shared_password_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crossRealmTrustSharedPasswordUri"))

    @cross_realm_trust_shared_password_uri.setter
    def cross_realm_trust_shared_password_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ccb42ac4d70700feafaca9597ca55cef69c9d773f315de69ba887b3844d6d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossRealmTrustSharedPasswordUri", value)

    @builtins.property
    @jsii.member(jsii_name="enableKerberos")
    def enable_kerberos(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableKerberos"))

    @enable_kerberos.setter
    def enable_kerberos(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7649ed1719c159650dfcd1121a4f531eaab6abccf8719e74a2e48cbd5e7eeeb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableKerberos", value)

    @builtins.property
    @jsii.member(jsii_name="kdcDbKeyUri")
    def kdc_db_key_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kdcDbKeyUri"))

    @kdc_db_key_uri.setter
    def kdc_db_key_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34d10ee17bd5ee2aa03c5590d39537f098a8168459be86eedcfa7f09ac58286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kdcDbKeyUri", value)

    @builtins.property
    @jsii.member(jsii_name="keyPasswordUri")
    def key_password_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPasswordUri"))

    @key_password_uri.setter
    def key_password_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7909933b45bcf127354ceb6ad8a0c1583277622c0845b59528738b9c6af5b85f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPasswordUri", value)

    @builtins.property
    @jsii.member(jsii_name="keystorePasswordUri")
    def keystore_password_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keystorePasswordUri"))

    @keystore_password_uri.setter
    def keystore_password_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ebc695b7860885e735e24231d278622ccb8435a9249bb4960e43c97b237ea76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keystorePasswordUri", value)

    @builtins.property
    @jsii.member(jsii_name="keystoreUri")
    def keystore_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keystoreUri"))

    @keystore_uri.setter
    def keystore_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d096fb4dd14930d329a8766f2ecdb675b4416eb2a167f6737b86bb0a1abcebce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keystoreUri", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyUri")
    def kms_key_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyUri"))

    @kms_key_uri.setter
    def kms_key_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30252b51699c7a6aeb55cb6f8d709cd603e48a627b74a45f92e34bfe47649d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyUri", value)

    @builtins.property
    @jsii.member(jsii_name="realm")
    def realm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "realm"))

    @realm.setter
    def realm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc61ddd934955620a0faf36d05ad19361909ff4840a330c9a111259bfb2b9d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realm", value)

    @builtins.property
    @jsii.member(jsii_name="rootPrincipalPasswordUri")
    def root_principal_password_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootPrincipalPasswordUri"))

    @root_principal_password_uri.setter
    def root_principal_password_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1471d82a4e2d2a62880475502a480f159f1168d68729197c15df7d6391e9a080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootPrincipalPasswordUri", value)

    @builtins.property
    @jsii.member(jsii_name="tgtLifetimeHours")
    def tgt_lifetime_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tgtLifetimeHours"))

    @tgt_lifetime_hours.setter
    def tgt_lifetime_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf143e76e934023f34e235bb4afc6c0501a7b5b11b3c5120cdefeb2d0ff82c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tgtLifetimeHours", value)

    @builtins.property
    @jsii.member(jsii_name="truststorePasswordUri")
    def truststore_password_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "truststorePasswordUri"))

    @truststore_password_uri.setter
    def truststore_password_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513c826694d88ea71467943e006dd54ab8682b47cc8d1091a01473b34b5a185a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "truststorePasswordUri", value)

    @builtins.property
    @jsii.member(jsii_name="truststoreUri")
    def truststore_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "truststoreUri"))

    @truststore_uri.setter
    def truststore_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8536f375df9ea149c53018763dcdc0e3a075c2f2e159c8fa7390aa3ce4c69ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "truststoreUri", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigSecurityConfigKerberosConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigSecurityConfigKerberosConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigSecurityConfigKerberosConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4b362c6c0cb5a503a03fb0c84eb3bbadf83279304be7e0c2c0ae51cd541b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterClusterConfigSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__587cc146cd670c4af43c7d5eb6a5c57c83c963779b74127e325bee895e94b216)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKerberosConfig")
    def put_kerberos_config(
        self,
        *,
        kms_key_uri: builtins.str,
        root_principal_password_uri: builtins.str,
        cross_realm_trust_admin_server: typing.Optional[builtins.str] = None,
        cross_realm_trust_kdc: typing.Optional[builtins.str] = None,
        cross_realm_trust_realm: typing.Optional[builtins.str] = None,
        cross_realm_trust_shared_password_uri: typing.Optional[builtins.str] = None,
        enable_kerberos: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kdc_db_key_uri: typing.Optional[builtins.str] = None,
        key_password_uri: typing.Optional[builtins.str] = None,
        keystore_password_uri: typing.Optional[builtins.str] = None,
        keystore_uri: typing.Optional[builtins.str] = None,
        realm: typing.Optional[builtins.str] = None,
        tgt_lifetime_hours: typing.Optional[jsii.Number] = None,
        truststore_password_uri: typing.Optional[builtins.str] = None,
        truststore_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_uri: The uri of the KMS key used to encrypt various sensitive files. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kms_key_uri DataprocCluster#kms_key_uri}
        :param root_principal_password_uri: The cloud Storage URI of a KMS encrypted file containing the root principal password. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#root_principal_password_uri DataprocCluster#root_principal_password_uri}
        :param cross_realm_trust_admin_server: The admin server (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_admin_server DataprocCluster#cross_realm_trust_admin_server}
        :param cross_realm_trust_kdc: The KDC (IP or hostname) for the remote trusted realm in a cross realm trust relationship. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_kdc DataprocCluster#cross_realm_trust_kdc}
        :param cross_realm_trust_realm: The remote realm the Dataproc on-cluster KDC will trust, should the user enable cross realm trust. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_realm DataprocCluster#cross_realm_trust_realm}
        :param cross_realm_trust_shared_password_uri: The Cloud Storage URI of a KMS encrypted file containing the shared password between the on-cluster Kerberos realm and the remote trusted realm, in a cross realm trust relationship. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cross_realm_trust_shared_password_uri DataprocCluster#cross_realm_trust_shared_password_uri}
        :param enable_kerberos: Flag to indicate whether to Kerberize the cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#enable_kerberos DataprocCluster#enable_kerberos}
        :param kdc_db_key_uri: The Cloud Storage URI of a KMS encrypted file containing the master key of the KDC database. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kdc_db_key_uri DataprocCluster#kdc_db_key_uri}
        :param key_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided key. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#key_password_uri DataprocCluster#key_password_uri}
        :param keystore_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided keystore. For the self-signed certificate, this password is generated by Dataproc Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#keystore_password_uri DataprocCluster#keystore_password_uri}
        :param keystore_uri: The Cloud Storage URI of the keystore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#keystore_uri DataprocCluster#keystore_uri}
        :param realm: The name of the on-cluster Kerberos realm. If not specified, the uppercased domain of hostnames will be the realm. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#realm DataprocCluster#realm}
        :param tgt_lifetime_hours: The lifetime of the ticket granting ticket, in hours. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#tgt_lifetime_hours DataprocCluster#tgt_lifetime_hours}
        :param truststore_password_uri: The Cloud Storage URI of a KMS encrypted file containing the password to the user provided truststore. For the self-signed certificate, this password is generated by Dataproc. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#truststore_password_uri DataprocCluster#truststore_password_uri}
        :param truststore_uri: The Cloud Storage URI of the truststore file used for SSL encryption. If not provided, Dataproc will provide a self-signed certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#truststore_uri DataprocCluster#truststore_uri}
        '''
        value = DataprocClusterClusterConfigSecurityConfigKerberosConfig(
            kms_key_uri=kms_key_uri,
            root_principal_password_uri=root_principal_password_uri,
            cross_realm_trust_admin_server=cross_realm_trust_admin_server,
            cross_realm_trust_kdc=cross_realm_trust_kdc,
            cross_realm_trust_realm=cross_realm_trust_realm,
            cross_realm_trust_shared_password_uri=cross_realm_trust_shared_password_uri,
            enable_kerberos=enable_kerberos,
            kdc_db_key_uri=kdc_db_key_uri,
            key_password_uri=key_password_uri,
            keystore_password_uri=keystore_password_uri,
            keystore_uri=keystore_uri,
            realm=realm,
            tgt_lifetime_hours=tgt_lifetime_hours,
            truststore_password_uri=truststore_password_uri,
            truststore_uri=truststore_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putKerberosConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="kerberosConfig")
    def kerberos_config(
        self,
    ) -> DataprocClusterClusterConfigSecurityConfigKerberosConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigSecurityConfigKerberosConfigOutputReference, jsii.get(self, "kerberosConfig"))

    @builtins.property
    @jsii.member(jsii_name="kerberosConfigInput")
    def kerberos_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigSecurityConfigKerberosConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigSecurityConfigKerberosConfig], jsii.get(self, "kerberosConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigSecurityConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a0ff51af259e6f827745832125cad8c9064aa86ef6bc2920d018fdf2008ef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigSoftwareConfig",
    jsii_struct_bases=[],
    name_mapping={
        "image_version": "imageVersion",
        "optional_components": "optionalComponents",
        "override_properties": "overrideProperties",
    },
)
class DataprocClusterClusterConfigSoftwareConfig:
    def __init__(
        self,
        *,
        image_version: typing.Optional[builtins.str] = None,
        optional_components: typing.Optional[typing.Sequence[builtins.str]] = None,
        override_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param image_version: The Cloud Dataproc image version to use for the cluster - this controls the sets of software versions installed onto the nodes when you create clusters. If not specified, defaults to the latest version. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#image_version DataprocCluster#image_version}
        :param optional_components: The set of optional components to activate on the cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#optional_components DataprocCluster#optional_components}
        :param override_properties: A list of override and additional properties (key/value pairs) used to modify various aspects of the common configuration files used when creating a cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#override_properties DataprocCluster#override_properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822dc890087f54c3079a5cd83118c8967c5cf55741543ad25a9fbaf94a6a4d2b)
            check_type(argname="argument image_version", value=image_version, expected_type=type_hints["image_version"])
            check_type(argname="argument optional_components", value=optional_components, expected_type=type_hints["optional_components"])
            check_type(argname="argument override_properties", value=override_properties, expected_type=type_hints["override_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image_version is not None:
            self._values["image_version"] = image_version
        if optional_components is not None:
            self._values["optional_components"] = optional_components
        if override_properties is not None:
            self._values["override_properties"] = override_properties

    @builtins.property
    def image_version(self) -> typing.Optional[builtins.str]:
        '''The Cloud Dataproc image version to use for the cluster - this controls the sets of software versions installed onto the nodes when you create clusters.

        If not specified, defaults to the latest version.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#image_version DataprocCluster#image_version}
        '''
        result = self._values.get("image_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of optional components to activate on the cluster.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#optional_components DataprocCluster#optional_components}
        '''
        result = self._values.get("optional_components")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def override_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of override and additional properties (key/value pairs) used to modify various aspects of the common configuration files used when creating a cluster.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#override_properties DataprocCluster#override_properties}
        '''
        result = self._values.get("override_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ecd818e2d794e372cef09a7a5f022a01664b523df7b7d72625e08ac1decf825)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImageVersion")
    def reset_image_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersion", []))

    @jsii.member(jsii_name="resetOptionalComponents")
    def reset_optional_components(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptionalComponents", []))

    @jsii.member(jsii_name="resetOverrideProperties")
    def reset_override_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideProperties", []))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionInput")
    def image_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalComponentsInput")
    def optional_components_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "optionalComponentsInput"))

    @builtins.property
    @jsii.member(jsii_name="overridePropertiesInput")
    def override_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "overridePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersion")
    def image_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageVersion"))

    @image_version.setter
    def image_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6279c96483c2112deb0699f09ac348e95b95f02809f905d4ccccffb10c3ddd96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersion", value)

    @builtins.property
    @jsii.member(jsii_name="optionalComponents")
    def optional_components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "optionalComponents"))

    @optional_components.setter
    def optional_components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b432dbafdddf77ea37d675405878a35e5e8d745cfb266c7640ee06d19df1b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionalComponents", value)

    @builtins.property
    @jsii.member(jsii_name="overrideProperties")
    def override_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "overrideProperties"))

    @override_properties.setter
    def override_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40edc46650ec73be08cb3f8f30b3d4a241eee69c15c4adb0e55de09e5d9cd817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideProperties", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigSoftwareConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93fef1c414888a1facc48cc25b826de6d8e21c27bc151aad1d1a994e922c046e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigWorkerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "accelerators": "accelerators",
        "disk_config": "diskConfig",
        "image_uri": "imageUri",
        "machine_type": "machineType",
        "min_cpu_platform": "minCpuPlatform",
        "num_instances": "numInstances",
    },
)
class DataprocClusterClusterConfigWorkerConfig:
    def __init__(
        self,
        *,
        accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocClusterClusterConfigWorkerConfigAccelerators", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disk_config: typing.Optional[typing.Union["DataprocClusterClusterConfigWorkerConfigDiskConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        image_uri: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        num_instances: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param accelerators: accelerators block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerators DataprocCluster#accelerators}
        :param disk_config: disk_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#disk_config DataprocCluster#disk_config}
        :param image_uri: The URI for the image to use for this master/worker. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#image_uri DataprocCluster#image_uri}
        :param machine_type: The name of a Google Compute Engine machine type to create for the master/worker. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#machine_type DataprocCluster#machine_type}
        :param min_cpu_platform: The name of a minimum generation of CPU family for the master/worker. If not specified, GCP will default to a predetermined computed value for each zone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_cpu_platform DataprocCluster#min_cpu_platform}
        :param num_instances: Specifies the number of master/worker nodes to create. If not specified, GCP will default to a predetermined computed value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_instances DataprocCluster#num_instances}
        '''
        if isinstance(disk_config, dict):
            disk_config = DataprocClusterClusterConfigWorkerConfigDiskConfig(**disk_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80262d5e41f8aaefcdc1c316e17493d27924312c55b0b8b0ee553ac3f6a188c)
            check_type(argname="argument accelerators", value=accelerators, expected_type=type_hints["accelerators"])
            check_type(argname="argument disk_config", value=disk_config, expected_type=type_hints["disk_config"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument num_instances", value=num_instances, expected_type=type_hints["num_instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerators is not None:
            self._values["accelerators"] = accelerators
        if disk_config is not None:
            self._values["disk_config"] = disk_config
        if image_uri is not None:
            self._values["image_uri"] = image_uri
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if num_instances is not None:
            self._values["num_instances"] = num_instances

    @builtins.property
    def accelerators(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocClusterClusterConfigWorkerConfigAccelerators"]]]:
        '''accelerators block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerators DataprocCluster#accelerators}
        '''
        result = self._values.get("accelerators")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocClusterClusterConfigWorkerConfigAccelerators"]]], result)

    @builtins.property
    def disk_config(
        self,
    ) -> typing.Optional["DataprocClusterClusterConfigWorkerConfigDiskConfig"]:
        '''disk_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#disk_config DataprocCluster#disk_config}
        '''
        result = self._values.get("disk_config")
        return typing.cast(typing.Optional["DataprocClusterClusterConfigWorkerConfigDiskConfig"], result)

    @builtins.property
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''The URI for the image to use for this master/worker.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#image_uri DataprocCluster#image_uri}
        '''
        result = self._values.get("image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The name of a Google Compute Engine machine type to create for the master/worker.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#machine_type DataprocCluster#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''The name of a minimum generation of CPU family for the master/worker.

        If not specified, GCP will default to a predetermined computed value for each zone.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_cpu_platform DataprocCluster#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_instances(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of master/worker nodes to create. If not specified, GCP will default to a predetermined computed value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_instances DataprocCluster#num_instances}
        '''
        result = self._values.get("num_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigWorkerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigWorkerConfigAccelerators",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
    },
)
class DataprocClusterClusterConfigWorkerConfigAccelerators:
    def __init__(
        self,
        *,
        accelerator_count: jsii.Number,
        accelerator_type: builtins.str,
    ) -> None:
        '''
        :param accelerator_count: The number of the accelerator cards of this type exposed to this instance. Often restricted to one of 1, 2, 4, or 8. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerator_count DataprocCluster#accelerator_count}
        :param accelerator_type: The short name of the accelerator type to expose to this instance. For example, nvidia-tesla-k80. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerator_type DataprocCluster#accelerator_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb8115d8b88c41af0fec9d9404aaa9477e5a18061f1f00937dcb25bd82b6d98)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator_count": accelerator_count,
            "accelerator_type": accelerator_type,
        }

    @builtins.property
    def accelerator_count(self) -> jsii.Number:
        '''The number of the accelerator cards of this type exposed to this instance.

        Often restricted to one of 1, 2, 4, or 8.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerator_count DataprocCluster#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        assert result is not None, "Required property 'accelerator_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def accelerator_type(self) -> builtins.str:
        '''The short name of the accelerator type to expose to this instance. For example, nvidia-tesla-k80.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#accelerator_type DataprocCluster#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        assert result is not None, "Required property 'accelerator_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigWorkerConfigAccelerators(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigWorkerConfigAcceleratorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigWorkerConfigAcceleratorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3a8f9892f6a6b08c882be9e79e05d109a4cfe1315f89311eabf917684446848)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocClusterClusterConfigWorkerConfigAcceleratorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22bd8599b11dc1616270dcac3f30c0a64220d2d83e7167d92a1f86adbc86979)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocClusterClusterConfigWorkerConfigAcceleratorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6249924a07f26231202b327e9c4a59e1af9630be8759101195b0b55ffa4c9d39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c21c77f4e28eaeb3270c6c096b72960b7cc13a52eea9990b82b80546d0a3f23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc120ca5376ffbd963899ac4fbd6b74e2ec77cd44d18da8318d206532b63434f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigWorkerConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigWorkerConfigAccelerators]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigWorkerConfigAccelerators]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6eb31dabebb89233b1c85a885e37b1861902da8bafcf690d2b2a753be33982d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterClusterConfigWorkerConfigAcceleratorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigWorkerConfigAcceleratorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04a1b699b22520a45f78c4101403f4831dc68ec322088e6ba170f9ae4db4d2e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @accelerator_count.setter
    def accelerator_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66974c73a7fe0b96f177730402895a3d7ee0825c9c226fddfc4861974b86f67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value)

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7affed043b1f92f2cc6251d5467d730fa7141b2d3cac75590af5ed4310d88a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataprocClusterClusterConfigWorkerConfigAccelerators, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataprocClusterClusterConfigWorkerConfigAccelerators, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataprocClusterClusterConfigWorkerConfigAccelerators, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30ef421d1ed58432ca9b7cc4f6a2d2023b53ab6ad143f82e086435b7804addb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigWorkerConfigDiskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "num_local_ssds": "numLocalSsds",
    },
)
class DataprocClusterClusterConfigWorkerConfigDiskConfig:
    def __init__(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each node, specified in GB. The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_size_gb DataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_type DataprocCluster#boot_disk_type}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_local_ssds DataprocCluster#num_local_ssds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205b56d220620927788db71e1d60b1eb6741f8e84eabe90e2fdf75d4c5257df5)
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument num_local_ssds", value=num_local_ssds, expected_type=type_hints["num_local_ssds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if num_local_ssds is not None:
            self._values["num_local_ssds"] = num_local_ssds

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the primary disk attached to each node, specified in GB.

        The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_size_gb DataprocCluster#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_type DataprocCluster#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_local_ssds(self) -> typing.Optional[jsii.Number]:
        '''The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_local_ssds DataprocCluster#num_local_ssds}
        '''
        result = self._values.get("num_local_ssds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterClusterConfigWorkerConfigDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterClusterConfigWorkerConfigDiskConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigWorkerConfigDiskConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9bd2fc4fd91ba1b55cc32a8f25c62e7af3f22f4ea1bdc647b2c217ad0bafa00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetNumLocalSsds")
    def reset_num_local_ssds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLocalSsds", []))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="numLocalSsdsInput")
    def num_local_ssds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLocalSsdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10732c9735c28d76f47daba77b4d8fadee3b3235347bcccfaa7b6275782e39b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value)

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ce9c602c615bfecf33d6b023dca8344fc9b3a98622f9b8f33f6f3a0e09e68e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value)

    @builtins.property
    @jsii.member(jsii_name="numLocalSsds")
    def num_local_ssds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLocalSsds"))

    @num_local_ssds.setter
    def num_local_ssds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1a9a97af819d5324f85cb4446798835ade60a3c63d50d4c25ee6bcc872d82f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLocalSsds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigWorkerConfigDiskConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigWorkerConfigDiskConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d78fd349314051492bef38bd53824bf6b19e5ff304a98356c41d6d79249762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterClusterConfigWorkerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterClusterConfigWorkerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74524adbe1b1735e0513e4072fc67add33e7c03f1a226662aa9fb1f3e2d63f21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccelerators")
    def put_accelerators(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterClusterConfigWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebcf06522db70669168011d1abff8031dd5b65a729e43f9e730d33ff973944f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccelerators", [value]))

    @jsii.member(jsii_name="putDiskConfig")
    def put_disk_config(
        self,
        *,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        num_local_ssds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param boot_disk_size_gb: Size of the primary disk attached to each node, specified in GB. The primary disk contains the boot volume and system libraries, and the smallest allowed disk size is 10GB. GCP will default to a predetermined computed value if not set (currently 500GB). Note: If SSDs are not attached, it also contains the HDFS data blocks and Hadoop working directories. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_size_gb DataprocCluster#boot_disk_size_gb}
        :param boot_disk_type: The disk type of the primary disk attached to each node. Such as "pd-ssd" or "pd-standard". Defaults to "pd-standard". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#boot_disk_type DataprocCluster#boot_disk_type}
        :param num_local_ssds: The amount of local SSD disks that will be attached to each master cluster node. Defaults to 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#num_local_ssds DataprocCluster#num_local_ssds}
        '''
        value = DataprocClusterClusterConfigWorkerConfigDiskConfig(
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            num_local_ssds=num_local_ssds,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskConfig", [value]))

    @jsii.member(jsii_name="resetAccelerators")
    def reset_accelerators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccelerators", []))

    @jsii.member(jsii_name="resetDiskConfig")
    def reset_disk_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConfig", []))

    @jsii.member(jsii_name="resetImageUri")
    def reset_image_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageUri", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetNumInstances")
    def reset_num_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumInstances", []))

    @builtins.property
    @jsii.member(jsii_name="accelerators")
    def accelerators(self) -> DataprocClusterClusterConfigWorkerConfigAcceleratorsList:
        return typing.cast(DataprocClusterClusterConfigWorkerConfigAcceleratorsList, jsii.get(self, "accelerators"))

    @builtins.property
    @jsii.member(jsii_name="diskConfig")
    def disk_config(
        self,
    ) -> DataprocClusterClusterConfigWorkerConfigDiskConfigOutputReference:
        return typing.cast(DataprocClusterClusterConfigWorkerConfigDiskConfigOutputReference, jsii.get(self, "diskConfig"))

    @builtins.property
    @jsii.member(jsii_name="instanceNames")
    def instance_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceNames"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorsInput")
    def accelerators_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigWorkerConfigAccelerators]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigWorkerConfigAccelerators]]], jsii.get(self, "acceleratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskConfigInput")
    def disk_config_input(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigWorkerConfigDiskConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigWorkerConfigDiskConfig], jsii.get(self, "diskConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="numInstancesInput")
    def num_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc9625c43697a9dad6d0d7e0633419310c032a51c5a82c7e48e427d9217d4df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value)

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e57960dc12d3047b9938b72a0278c7663350067be411bcf8304cbf3787de237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value)

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4854c2297c34dece6102463adf11994cb69403c885c2999714394487537130dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value)

    @builtins.property
    @jsii.member(jsii_name="numInstances")
    def num_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numInstances"))

    @num_instances.setter
    def num_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b189c368aa3b6733a69d75e8463fb3b6588f793fa9d43aaae051930b1d2afc7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numInstances", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterClusterConfigWorkerConfig]:
        return typing.cast(typing.Optional[DataprocClusterClusterConfigWorkerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterClusterConfigWorkerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b616597eb875e21eb36331e76a5d91ccdf77b40658c8082dde249ae02668902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterConfig",
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
        "cluster_config": "clusterConfig",
        "graceful_decommission_timeout": "gracefulDecommissionTimeout",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
        "virtual_cluster_config": "virtualClusterConfig",
    },
)
class DataprocClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_config: typing.Optional[typing.Union[DataprocClusterClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        graceful_decommission_timeout: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataprocClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_cluster_config: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the cluster, unique within the project and zone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#name DataprocCluster#name}
        :param cluster_config: cluster_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cluster_config DataprocCluster#cluster_config}
        :param graceful_decommission_timeout: The timeout duration which allows graceful decomissioning when you change the number of worker nodes directly through a terraform apply. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#graceful_decommission_timeout DataprocCluster#graceful_decommission_timeout}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#id DataprocCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The list of labels (key/value pairs) to be applied to instances in the cluster. GCP generates some itself including goog-dataproc-cluster-name which is the name of the cluster. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#labels DataprocCluster#labels}
        :param project: The ID of the project in which the cluster will exist. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#project DataprocCluster#project}
        :param region: The region in which the cluster and associated nodes will be created in. Defaults to global. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#region DataprocCluster#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#timeouts DataprocCluster#timeouts}
        :param virtual_cluster_config: virtual_cluster_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#virtual_cluster_config DataprocCluster#virtual_cluster_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cluster_config, dict):
            cluster_config = DataprocClusterClusterConfig(**cluster_config)
        if isinstance(timeouts, dict):
            timeouts = DataprocClusterTimeouts(**timeouts)
        if isinstance(virtual_cluster_config, dict):
            virtual_cluster_config = DataprocClusterVirtualClusterConfig(**virtual_cluster_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed5644cd8fb56e1eaa06d727a133e9fb445bda9f5ff5bf9e88339bab33e50bf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cluster_config", value=cluster_config, expected_type=type_hints["cluster_config"])
            check_type(argname="argument graceful_decommission_timeout", value=graceful_decommission_timeout, expected_type=type_hints["graceful_decommission_timeout"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_cluster_config", value=virtual_cluster_config, expected_type=type_hints["virtual_cluster_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if cluster_config is not None:
            self._values["cluster_config"] = cluster_config
        if graceful_decommission_timeout is not None:
            self._values["graceful_decommission_timeout"] = graceful_decommission_timeout
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_cluster_config is not None:
            self._values["virtual_cluster_config"] = virtual_cluster_config

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
        '''The name of the cluster, unique within the project and zone.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#name DataprocCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_config(self) -> typing.Optional[DataprocClusterClusterConfig]:
        '''cluster_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#cluster_config DataprocCluster#cluster_config}
        '''
        result = self._values.get("cluster_config")
        return typing.cast(typing.Optional[DataprocClusterClusterConfig], result)

    @builtins.property
    def graceful_decommission_timeout(self) -> typing.Optional[builtins.str]:
        '''The timeout duration which allows graceful decomissioning when you change the number of worker nodes directly through a terraform apply.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#graceful_decommission_timeout DataprocCluster#graceful_decommission_timeout}
        '''
        result = self._values.get("graceful_decommission_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#id DataprocCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The list of labels (key/value pairs) to be applied to instances in the cluster.

        GCP generates some itself including goog-dataproc-cluster-name which is the name of the cluster.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#labels DataprocCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the cluster will exist.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#project DataprocCluster#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region in which the cluster and associated nodes will be created in. Defaults to global.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#region DataprocCluster#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataprocClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#timeouts DataprocCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataprocClusterTimeouts"], result)

    @builtins.property
    def virtual_cluster_config(
        self,
    ) -> typing.Optional["DataprocClusterVirtualClusterConfig"]:
        '''virtual_cluster_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#virtual_cluster_config DataprocCluster#virtual_cluster_config}
        '''
        result = self._values.get("virtual_cluster_config")
        return typing.cast(typing.Optional["DataprocClusterVirtualClusterConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataprocClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#create DataprocCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#delete DataprocCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#update DataprocCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a613b8d951875abe58651dab277cf4df7ef14e32a9326c6761e133cba07c97)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#create DataprocCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#delete DataprocCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#update DataprocCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__069813e8660e54f1ac9d46fe435030af350ee3b67a3ac08ea7ce4505605b9dd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__050e90691edbe0a6eebb054d131d16d5deedd5e594fca2da0d2d39c2a3e65860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c366796bb2334dca018edc6ae9cd7b39472da15889de41e2782ff8995d8468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06405c43678140ef48a048844baf4cecfcd753dcb8ff1b166f65b69ad122a49b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataprocClusterTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataprocClusterTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataprocClusterTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db616b8fec382d4f3eb073fcd4017591f49ef95b1426506e82c3c5a410a3b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auxiliary_services_config": "auxiliaryServicesConfig",
        "kubernetes_cluster_config": "kubernetesClusterConfig",
        "staging_bucket": "stagingBucket",
    },
)
class DataprocClusterVirtualClusterConfig:
    def __init__(
        self,
        *,
        auxiliary_services_config: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes_cluster_config: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfigKubernetesClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auxiliary_services_config: auxiliary_services_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#auxiliary_services_config DataprocCluster#auxiliary_services_config}
        :param kubernetes_cluster_config: kubernetes_cluster_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kubernetes_cluster_config DataprocCluster#kubernetes_cluster_config}
        :param staging_bucket: A Cloud Storage bucket used to stage job dependencies, config files, and job driver console output. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's staging bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#staging_bucket DataprocCluster#staging_bucket}
        '''
        if isinstance(auxiliary_services_config, dict):
            auxiliary_services_config = DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig(**auxiliary_services_config)
        if isinstance(kubernetes_cluster_config, dict):
            kubernetes_cluster_config = DataprocClusterVirtualClusterConfigKubernetesClusterConfig(**kubernetes_cluster_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c2306960f0feabb80acfa6a8ae9999fd42d8a1a59ef68c1799dee0ea6af910)
            check_type(argname="argument auxiliary_services_config", value=auxiliary_services_config, expected_type=type_hints["auxiliary_services_config"])
            check_type(argname="argument kubernetes_cluster_config", value=kubernetes_cluster_config, expected_type=type_hints["kubernetes_cluster_config"])
            check_type(argname="argument staging_bucket", value=staging_bucket, expected_type=type_hints["staging_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auxiliary_services_config is not None:
            self._values["auxiliary_services_config"] = auxiliary_services_config
        if kubernetes_cluster_config is not None:
            self._values["kubernetes_cluster_config"] = kubernetes_cluster_config
        if staging_bucket is not None:
            self._values["staging_bucket"] = staging_bucket

    @builtins.property
    def auxiliary_services_config(
        self,
    ) -> typing.Optional["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig"]:
        '''auxiliary_services_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#auxiliary_services_config DataprocCluster#auxiliary_services_config}
        '''
        result = self._values.get("auxiliary_services_config")
        return typing.cast(typing.Optional["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig"], result)

    @builtins.property
    def kubernetes_cluster_config(
        self,
    ) -> typing.Optional["DataprocClusterVirtualClusterConfigKubernetesClusterConfig"]:
        '''kubernetes_cluster_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kubernetes_cluster_config DataprocCluster#kubernetes_cluster_config}
        '''
        result = self._values.get("kubernetes_cluster_config")
        return typing.cast(typing.Optional["DataprocClusterVirtualClusterConfigKubernetesClusterConfig"], result)

    @builtins.property
    def staging_bucket(self) -> typing.Optional[builtins.str]:
        '''A Cloud Storage bucket used to stage job dependencies, config files, and job driver console output.

        If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location (US, ASIA, or EU) for your cluster's staging bucket according to the Compute Engine zone where your cluster is deployed, and then create and manage this project-level, per-location bucket.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#staging_bucket DataprocCluster#staging_bucket}
        '''
        result = self._values.get("staging_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metastore_config": "metastoreConfig",
        "spark_history_server_config": "sparkHistoryServerConfig",
    },
)
class DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig:
    def __init__(
        self,
        *,
        metastore_config: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_history_server_config: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_config: metastore_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#metastore_config DataprocCluster#metastore_config}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#spark_history_server_config DataprocCluster#spark_history_server_config}
        '''
        if isinstance(metastore_config, dict):
            metastore_config = DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig(**metastore_config)
        if isinstance(spark_history_server_config, dict):
            spark_history_server_config = DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig(**spark_history_server_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708d9c98802232c52f3e8001da74152b384e65f7aa164aacd577e195582aa7cd)
            check_type(argname="argument metastore_config", value=metastore_config, expected_type=type_hints["metastore_config"])
            check_type(argname="argument spark_history_server_config", value=spark_history_server_config, expected_type=type_hints["spark_history_server_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metastore_config is not None:
            self._values["metastore_config"] = metastore_config
        if spark_history_server_config is not None:
            self._values["spark_history_server_config"] = spark_history_server_config

    @builtins.property
    def metastore_config(
        self,
    ) -> typing.Optional["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig"]:
        '''metastore_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#metastore_config DataprocCluster#metastore_config}
        '''
        result = self._values.get("metastore_config")
        return typing.cast(typing.Optional["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig"], result)

    @builtins.property
    def spark_history_server_config(
        self,
    ) -> typing.Optional["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig"]:
        '''spark_history_server_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#spark_history_server_config DataprocCluster#spark_history_server_config}
        '''
        result = self._values.get("spark_history_server_config")
        return typing.cast(typing.Optional["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_metastore_service": "dataprocMetastoreService"},
)
class DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig:
    def __init__(
        self,
        *,
        dataproc_metastore_service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_metastore_service: The Hive Metastore configuration for this workload. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#dataproc_metastore_service DataprocCluster#dataproc_metastore_service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395ec210f5c3915ba1eb598d649f5e911053c14131ec190f7b662cb0e05923a2)
            check_type(argname="argument dataproc_metastore_service", value=dataproc_metastore_service, expected_type=type_hints["dataproc_metastore_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataproc_metastore_service is not None:
            self._values["dataproc_metastore_service"] = dataproc_metastore_service

    @builtins.property
    def dataproc_metastore_service(self) -> typing.Optional[builtins.str]:
        '''The Hive Metastore configuration for this workload.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#dataproc_metastore_service DataprocCluster#dataproc_metastore_service}
        '''
        result = self._values.get("dataproc_metastore_service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30ab6305d8d11409804e8abed1dd47518d87915caeb2f4987ff8167041803a7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataprocMetastoreService")
    def reset_dataproc_metastore_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocMetastoreService", []))

    @builtins.property
    @jsii.member(jsii_name="dataprocMetastoreServiceInput")
    def dataproc_metastore_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocMetastoreServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocMetastoreService")
    def dataproc_metastore_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataprocMetastoreService"))

    @dataproc_metastore_service.setter
    def dataproc_metastore_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7776f089183dc195cf0321e79dcf89b57c3a33ca4036b0834e38e113fd3b49f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocMetastoreService", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d95372c4dc76c73faf97d56d9d2a48a32785d845dbe7268f8a606101b8791ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72264dd65842e1715d713bab787df4cbd986391bf69b0028aab126019b3fad33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetastoreConfig")
    def put_metastore_config(
        self,
        *,
        dataproc_metastore_service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_metastore_service: The Hive Metastore configuration for this workload. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#dataproc_metastore_service DataprocCluster#dataproc_metastore_service}
        '''
        value = DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig(
            dataproc_metastore_service=dataproc_metastore_service
        )

        return typing.cast(None, jsii.invoke(self, "putMetastoreConfig", [value]))

    @jsii.member(jsii_name="putSparkHistoryServerConfig")
    def put_spark_history_server_config(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#dataproc_cluster DataprocCluster#dataproc_cluster}
        '''
        value = DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig(
            dataproc_cluster=dataproc_cluster
        )

        return typing.cast(None, jsii.invoke(self, "putSparkHistoryServerConfig", [value]))

    @jsii.member(jsii_name="resetMetastoreConfig")
    def reset_metastore_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastoreConfig", []))

    @jsii.member(jsii_name="resetSparkHistoryServerConfig")
    def reset_spark_history_server_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkHistoryServerConfig", []))

    @builtins.property
    @jsii.member(jsii_name="metastoreConfig")
    def metastore_config(
        self,
    ) -> DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfigOutputReference:
        return typing.cast(DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfigOutputReference, jsii.get(self, "metastoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfig")
    def spark_history_server_config(
        self,
    ) -> "DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfigOutputReference":
        return typing.cast("DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfigOutputReference", jsii.get(self, "sparkHistoryServerConfig"))

    @builtins.property
    @jsii.member(jsii_name="metastoreConfigInput")
    def metastore_config_input(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig], jsii.get(self, "metastoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfigInput")
    def spark_history_server_config_input(
        self,
    ) -> typing.Optional["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig"]:
        return typing.cast(typing.Optional["DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig"], jsii.get(self, "sparkHistoryServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958db16e0649f5a11928a60dbfb1d26cc463eefe7ddd69beb9bb6effb875de43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_cluster": "dataprocCluster"},
)
class DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig:
    def __init__(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#dataproc_cluster DataprocCluster#dataproc_cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b840cfa8bb2c3e51bc69865fcddeb6b5a25af130b017b13c466e6eb802c4eb)
            check_type(argname="argument dataproc_cluster", value=dataproc_cluster, expected_type=type_hints["dataproc_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataproc_cluster is not None:
            self._values["dataproc_cluster"] = dataproc_cluster

    @builtins.property
    def dataproc_cluster(self) -> typing.Optional[builtins.str]:
        '''Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#dataproc_cluster DataprocCluster#dataproc_cluster}
        '''
        result = self._values.get("dataproc_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70e947988b76f83abd92cbce46ad5f654c1bd1ffc48be4c0b49f79122db853b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataprocCluster")
    def reset_dataproc_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocCluster", []))

    @builtins.property
    @jsii.member(jsii_name="dataprocClusterInput")
    def dataproc_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocCluster")
    def dataproc_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataprocCluster"))

    @dataproc_cluster.setter
    def dataproc_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d271315367d0c41f9f7b5dd6f19a39abbeac04e9f0efa559b3e74a40a17ee82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocCluster", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee6c95385b2b2ab925a0c6fa5f429d93d99d970b5162e1d77db6888f2a360ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "gke_cluster_config": "gkeClusterConfig",
        "kubernetes_software_config": "kubernetesSoftwareConfig",
        "kubernetes_namespace": "kubernetesNamespace",
    },
)
class DataprocClusterVirtualClusterConfigKubernetesClusterConfig:
    def __init__(
        self,
        *,
        gke_cluster_config: typing.Union["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig", typing.Dict[builtins.str, typing.Any]],
        kubernetes_software_config: typing.Union["DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig", typing.Dict[builtins.str, typing.Any]],
        kubernetes_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gke_cluster_config: gke_cluster_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#gke_cluster_config DataprocCluster#gke_cluster_config}
        :param kubernetes_software_config: kubernetes_software_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kubernetes_software_config DataprocCluster#kubernetes_software_config}
        :param kubernetes_namespace: A namespace within the Kubernetes cluster to deploy into. If this namespace does not exist, it is created. If it exists, Dataproc verifies that another Dataproc VirtualCluster is not installed into it. If not specified, the name of the Dataproc Cluster is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kubernetes_namespace DataprocCluster#kubernetes_namespace}
        '''
        if isinstance(gke_cluster_config, dict):
            gke_cluster_config = DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig(**gke_cluster_config)
        if isinstance(kubernetes_software_config, dict):
            kubernetes_software_config = DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig(**kubernetes_software_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddbfc62f23141ec847b3ce7f3ce85da175f19fafba0b2850c3c05ffc47f6c86)
            check_type(argname="argument gke_cluster_config", value=gke_cluster_config, expected_type=type_hints["gke_cluster_config"])
            check_type(argname="argument kubernetes_software_config", value=kubernetes_software_config, expected_type=type_hints["kubernetes_software_config"])
            check_type(argname="argument kubernetes_namespace", value=kubernetes_namespace, expected_type=type_hints["kubernetes_namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gke_cluster_config": gke_cluster_config,
            "kubernetes_software_config": kubernetes_software_config,
        }
        if kubernetes_namespace is not None:
            self._values["kubernetes_namespace"] = kubernetes_namespace

    @builtins.property
    def gke_cluster_config(
        self,
    ) -> "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig":
        '''gke_cluster_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#gke_cluster_config DataprocCluster#gke_cluster_config}
        '''
        result = self._values.get("gke_cluster_config")
        assert result is not None, "Required property 'gke_cluster_config' is missing"
        return typing.cast("DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig", result)

    @builtins.property
    def kubernetes_software_config(
        self,
    ) -> "DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig":
        '''kubernetes_software_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kubernetes_software_config DataprocCluster#kubernetes_software_config}
        '''
        result = self._values.get("kubernetes_software_config")
        assert result is not None, "Required property 'kubernetes_software_config' is missing"
        return typing.cast("DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig", result)

    @builtins.property
    def kubernetes_namespace(self) -> typing.Optional[builtins.str]:
        '''A namespace within the Kubernetes cluster to deploy into.

        If this namespace does not exist, it is created. If it exists, Dataproc verifies that another Dataproc VirtualCluster is not installed into it. If not specified, the name of the Dataproc Cluster is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kubernetes_namespace DataprocCluster#kubernetes_namespace}
        '''
        result = self._values.get("kubernetes_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfigKubernetesClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "gke_cluster_target": "gkeClusterTarget",
        "node_pool_target": "nodePoolTarget",
    },
)
class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig:
    def __init__(
        self,
        *,
        gke_cluster_target: typing.Optional[builtins.str] = None,
        node_pool_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param gke_cluster_target: A target GKE cluster to deploy to. It must be in the same project and region as the Dataproc cluster (the GKE cluster can be zonal or regional). Format: 'projects/{project}/locations/{location}/clusters/{cluster_id}' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#gke_cluster_target DataprocCluster#gke_cluster_target}
        :param node_pool_target: node_pool_target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#node_pool_target DataprocCluster#node_pool_target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8e6d66631834d9031f383bc8eacf0b9839d86cc2900280431f71a817b4f788)
            check_type(argname="argument gke_cluster_target", value=gke_cluster_target, expected_type=type_hints["gke_cluster_target"])
            check_type(argname="argument node_pool_target", value=node_pool_target, expected_type=type_hints["node_pool_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gke_cluster_target is not None:
            self._values["gke_cluster_target"] = gke_cluster_target
        if node_pool_target is not None:
            self._values["node_pool_target"] = node_pool_target

    @builtins.property
    def gke_cluster_target(self) -> typing.Optional[builtins.str]:
        '''A target GKE cluster to deploy to.

        It must be in the same project and region as the Dataproc cluster (the GKE cluster can be zonal or regional). Format: 'projects/{project}/locations/{location}/clusters/{cluster_id}'

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#gke_cluster_target DataprocCluster#gke_cluster_target}
        '''
        result = self._values.get("gke_cluster_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_pool_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget"]]]:
        '''node_pool_target block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#node_pool_target DataprocCluster#node_pool_target}
        '''
        result = self._values.get("node_pool_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget",
    jsii_struct_bases=[],
    name_mapping={
        "node_pool": "nodePool",
        "roles": "roles",
        "node_pool_config": "nodePoolConfig",
    },
)
class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget:
    def __init__(
        self,
        *,
        node_pool: builtins.str,
        roles: typing.Sequence[builtins.str],
        node_pool_config: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param node_pool: The target GKE node pool. Format: 'projects/{project}/locations/{location}/clusters/{cluster}/nodePools/{nodePool}'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#node_pool DataprocCluster#node_pool}
        :param roles: The roles associated with the GKE node pool. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#roles DataprocCluster#roles}
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#node_pool_config DataprocCluster#node_pool_config}
        '''
        if isinstance(node_pool_config, dict):
            node_pool_config = DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig(**node_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a59cefbf0fdfe22c3bfc12b7dcfabc15f783b462ab7ae2a7576b2be131ea7f82)
            check_type(argname="argument node_pool", value=node_pool, expected_type=type_hints["node_pool"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_pool": node_pool,
            "roles": roles,
        }
        if node_pool_config is not None:
            self._values["node_pool_config"] = node_pool_config

    @builtins.property
    def node_pool(self) -> builtins.str:
        '''The target GKE node pool. Format: 'projects/{project}/locations/{location}/clusters/{cluster}/nodePools/{nodePool}'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#node_pool DataprocCluster#node_pool}
        '''
        result = self._values.get("node_pool")
        assert result is not None, "Required property 'node_pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def roles(self) -> typing.List[builtins.str]:
        '''The roles associated with the GKE node pool.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#roles DataprocCluster#roles}
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def node_pool_config(
        self,
    ) -> typing.Optional["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig"]:
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#node_pool_config DataprocCluster#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        return typing.cast(typing.Optional["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__296e6699b41b6488d5c2e5ca0b117ff1090309457e5624b4173b7fb8fa37cc0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5fe83488dc2beddc752ffa0487add80b11f318565718c56918e1c39df2d748d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a20b11a9760deece28713ac9483c8d5a102ffb7af219e82fc450d4918a54bfcd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f06269f6c39c292ba7aaec519ebde3c77f2c59c9ff1e2f521eb6b1f49c065ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4b7dcd24ad514886b9882aad112af050d582d561bb800558a5a43630cd3a7e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625790ec1b3fe7bfe6aace06935fe9d01a308dcdd6955270b027e327b16dbca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "locations": "locations",
        "autoscaling": "autoscaling",
        "config": "config",
    },
)
class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig:
    def __init__(
        self,
        *,
        locations: typing.Sequence[builtins.str],
        autoscaling: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling", typing.Dict[builtins.str, typing.Any]]] = None,
        config: typing.Optional[typing.Union["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param locations: The list of Compute Engine zones where node pool nodes associated with a Dataproc on GKE virtual cluster will be located. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#locations DataprocCluster#locations}
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#autoscaling DataprocCluster#autoscaling}
        :param config: config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#config DataprocCluster#config}
        '''
        if isinstance(autoscaling, dict):
            autoscaling = DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling(**autoscaling)
        if isinstance(config, dict):
            config = DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a7712083a09ee0b0297319d9b13b4da2629eae926803ab78b8aba4d6505820)
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument autoscaling", value=autoscaling, expected_type=type_hints["autoscaling"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "locations": locations,
        }
        if autoscaling is not None:
            self._values["autoscaling"] = autoscaling
        if config is not None:
            self._values["config"] = config

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''The list of Compute Engine zones where node pool nodes associated with a Dataproc on GKE virtual cluster will be located.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#locations DataprocCluster#locations}
        '''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def autoscaling(
        self,
    ) -> typing.Optional["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling"]:
        '''autoscaling block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#autoscaling DataprocCluster#autoscaling}
        '''
        result = self._values.get("autoscaling")
        return typing.cast(typing.Optional["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling"], result)

    @builtins.property
    def config(
        self,
    ) -> typing.Optional["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig"]:
        '''config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#config DataprocCluster#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling",
    jsii_struct_bases=[],
    name_mapping={"max_node_count": "maxNodeCount", "min_node_count": "minNodeCount"},
)
class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling:
    def __init__(
        self,
        *,
        max_node_count: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: The maximum number of nodes in the node pool. Must be >= minNodeCount, and must be > 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#max_node_count DataprocCluster#max_node_count}
        :param min_node_count: The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_node_count DataprocCluster#min_node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab56bc3b7959b9500408b35790c01ab6da6e08ce42a8c5ed96548b8c9db5ebc)
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_node_count is not None:
            self._values["max_node_count"] = max_node_count
        if min_node_count is not None:
            self._values["min_node_count"] = min_node_count

    @builtins.property
    def max_node_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of nodes in the node pool. Must be >= minNodeCount, and must be > 0.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#max_node_count DataprocCluster#max_node_count}
        '''
        result = self._values.get("max_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_node_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_node_count DataprocCluster#min_node_count}
        '''
        result = self._values.get("min_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14f24f18f1b7575a10243878aee56305c355ba6c88e6972f635ee72518fa1247)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxNodeCount")
    def reset_max_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNodeCount", []))

    @jsii.member(jsii_name="resetMinNodeCount")
    def reset_min_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCountInput")
    def max_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCountInput")
    def min_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb40dd5436ef8bbc64e71b4e8bf9f15eae3f24c8b7cfb2cc86742c02ae2ad61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value)

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c2be24f0da45c3abe2263e69930e3e06b17e83723dbf8be6940cde774f2cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b44876a72f90ad7dd2f6107e08e6c9c676d3ecba5de74c1f34e186c3ac01c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig",
    jsii_struct_bases=[],
    name_mapping={
        "local_ssd_count": "localSsdCount",
        "machine_type": "machineType",
        "min_cpu_platform": "minCpuPlatform",
        "preemptible": "preemptible",
        "spot": "spot",
    },
)
class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig:
    def __init__(
        self,
        *,
        local_ssd_count: typing.Optional[jsii.Number] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_ssd_count: The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#local_ssd_count DataprocCluster#local_ssd_count}
        :param machine_type: The name of a Compute Engine machine type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#machine_type DataprocCluster#machine_type}
        :param min_cpu_platform: Minimum CPU platform to be used by this instance. The instance may be scheduled on the specified or a newer CPU platform. Specify the friendly names of CPU platforms, such as "Intel Haswell" or "Intel Sandy Bridge". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_cpu_platform DataprocCluster#min_cpu_platform}
        :param preemptible: Whether the nodes are created as preemptible VM instances. Preemptible nodes cannot be used in a node pool with the CONTROLLER role or in the DEFAULT node pool if the CONTROLLER role is not assigned (the DEFAULT node pool will assume the CONTROLLER role). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#preemptible DataprocCluster#preemptible}
        :param spot: Spot flag for enabling Spot VM, which is a rebrand of the existing preemptible flag. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#spot DataprocCluster#spot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e3f230d1a6a1eb9d787aefc2fe25715f6cc1b8a960fbe6b6cee2ef78ab6c4f)
            check_type(argname="argument local_ssd_count", value=local_ssd_count, expected_type=type_hints["local_ssd_count"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument preemptible", value=preemptible, expected_type=type_hints["preemptible"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if local_ssd_count is not None:
            self._values["local_ssd_count"] = local_ssd_count
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if preemptible is not None:
            self._values["preemptible"] = preemptible
        if spot is not None:
            self._values["spot"] = spot

    @builtins.property
    def local_ssd_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#local_ssd_count DataprocCluster#local_ssd_count}
        '''
        result = self._values.get("local_ssd_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The name of a Compute Engine machine type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#machine_type DataprocCluster#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''Minimum CPU platform to be used by this instance.

        The instance may be scheduled on the specified or a newer CPU platform. Specify the friendly names of CPU platforms, such as "Intel Haswell" or "Intel Sandy Bridge".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_cpu_platform DataprocCluster#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preemptible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the nodes are created as preemptible VM instances.

        Preemptible nodes cannot be used in a node pool with the CONTROLLER role or in the DEFAULT node pool if the CONTROLLER role is not assigned (the DEFAULT node pool will assume the CONTROLLER role).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#preemptible DataprocCluster#preemptible}
        '''
        result = self._values.get("preemptible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def spot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Spot flag for enabling Spot VM, which is a rebrand of the existing preemptible flag.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#spot DataprocCluster#spot}
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__531a8d8af0b6f8843a92906be84fc621b86fc5cc69377c9af42a3d819898bc65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLocalSsdCount")
    def reset_local_ssd_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdCount", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetPreemptible")
    def reset_preemptible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptible", []))

    @jsii.member(jsii_name="resetSpot")
    def reset_spot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpot", []))

    @builtins.property
    @jsii.member(jsii_name="localSsdCountInput")
    def local_ssd_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "localSsdCountInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibleInput")
    def preemptible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preemptibleInput"))

    @builtins.property
    @jsii.member(jsii_name="spotInput")
    def spot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "spotInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdCount")
    def local_ssd_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localSsdCount"))

    @local_ssd_count.setter
    def local_ssd_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a014ef708fd9ad98f8ac42f1c27508a22510d6ea0a1cb66e501a87ef49a11572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value)

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330d708fec59bdd9badff5206b7622b6aab1b76d8995653306d347928ab8055e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value)

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cacd5535bb981b75ff39a7cf94caaf164ea1cef2e31719f8a64f8c1a5b5dad7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value)

    @builtins.property
    @jsii.member(jsii_name="preemptible")
    def preemptible(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preemptible"))

    @preemptible.setter
    def preemptible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbdeb7835160a63501de93e23162b99be9ce8afb8733655768b5e926e0fd49ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptible", value)

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "spot"))

    @spot.setter
    def spot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf081804886fa3032bb86ec8dbba01cfdd7d162620c48909540704d27a5b4c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spot", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__becc6c46bbd231321cb500b8f842330e1474e2aebecc372724c0ade78c38e483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ef758c1f6796c9f6cb3d2e6bd720dc4997496d17b02d0b29b4bdf9bfac381fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscaling")
    def put_autoscaling(
        self,
        *,
        max_node_count: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: The maximum number of nodes in the node pool. Must be >= minNodeCount, and must be > 0. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#max_node_count DataprocCluster#max_node_count}
        :param min_node_count: The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_node_count DataprocCluster#min_node_count}
        '''
        value = DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling(
            max_node_count=max_node_count, min_node_count=min_node_count
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaling", [value]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        local_ssd_count: typing.Optional[jsii.Number] = None,
        machine_type: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param local_ssd_count: The minimum number of nodes in the node pool. Must be >= 0 and <= maxNodeCount. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#local_ssd_count DataprocCluster#local_ssd_count}
        :param machine_type: The name of a Compute Engine machine type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#machine_type DataprocCluster#machine_type}
        :param min_cpu_platform: Minimum CPU platform to be used by this instance. The instance may be scheduled on the specified or a newer CPU platform. Specify the friendly names of CPU platforms, such as "Intel Haswell" or "Intel Sandy Bridge". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#min_cpu_platform DataprocCluster#min_cpu_platform}
        :param preemptible: Whether the nodes are created as preemptible VM instances. Preemptible nodes cannot be used in a node pool with the CONTROLLER role or in the DEFAULT node pool if the CONTROLLER role is not assigned (the DEFAULT node pool will assume the CONTROLLER role). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#preemptible DataprocCluster#preemptible}
        :param spot: Spot flag for enabling Spot VM, which is a rebrand of the existing preemptible flag. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#spot DataprocCluster#spot}
        '''
        value = DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig(
            local_ssd_count=local_ssd_count,
            machine_type=machine_type,
            min_cpu_platform=min_cpu_platform,
            preemptible=preemptible,
            spot=spot,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetAutoscaling")
    def reset_autoscaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaling", []))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @builtins.property
    @jsii.member(jsii_name="autoscaling")
    def autoscaling(
        self,
    ) -> DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscalingOutputReference:
        return typing.cast(DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscalingOutputReference, jsii.get(self, "autoscaling"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfigOutputReference:
        return typing.cast(DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingInput")
    def autoscaling_input(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling], jsii.get(self, "autoscalingInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c556d5513beb07b7397aae2989e1520735b375d238e5edec4d4822a189860d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9253a20ef58b7c6b0fdc5bdfdc2df4956f52bd3f02b6ff7b04b1d596e32a2698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92ebf4a7a3b3c1b5e9f2837a3ade94be37740c525a7b7713bd0bf954c2a33669)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        locations: typing.Sequence[builtins.str],
        autoscaling: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
        config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param locations: The list of Compute Engine zones where node pool nodes associated with a Dataproc on GKE virtual cluster will be located. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#locations DataprocCluster#locations}
        :param autoscaling: autoscaling block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#autoscaling DataprocCluster#autoscaling}
        :param config: config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#config DataprocCluster#config}
        '''
        value = DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig(
            locations=locations, autoscaling=autoscaling, config=config
        )

        return typing.cast(None, jsii.invoke(self, "putNodePoolConfig", [value]))

    @jsii.member(jsii_name="resetNodePoolConfig")
    def reset_node_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePoolConfig", []))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfig")
    def node_pool_config(
        self,
    ) -> DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigOutputReference:
        return typing.cast(DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigOutputReference, jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolInput")
    def node_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePool")
    def node_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodePool"))

    @node_pool.setter
    def node_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee209fde9fbb8f8da4049ed72df67172f3445734df0509dd9f86828af4dfc445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePool", value)

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__803f416b98f7b56f4a171a985f85eb40d967972f260de81977703ee2a6c50b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e57e772a51c469848c277789c0c970f1cf79128bfee6a8cd7a8ab24dbf2aca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e3d0f2fe070e7589c377d32bf0fefda33ba66009bab04f881e832409c476cf5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodePoolTarget")
    def put_node_pool_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b1a4f74d98e2defa103d54455fc54a8e1897fd2c538992e5dad9784ff7f7ccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodePoolTarget", [value]))

    @jsii.member(jsii_name="resetGkeClusterTarget")
    def reset_gke_cluster_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGkeClusterTarget", []))

    @jsii.member(jsii_name="resetNodePoolTarget")
    def reset_node_pool_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePoolTarget", []))

    @builtins.property
    @jsii.member(jsii_name="nodePoolTarget")
    def node_pool_target(
        self,
    ) -> DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetList:
        return typing.cast(DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetList, jsii.get(self, "nodePoolTarget"))

    @builtins.property
    @jsii.member(jsii_name="gkeClusterTargetInput")
    def gke_cluster_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gkeClusterTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolTargetInput")
    def node_pool_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]], jsii.get(self, "nodePoolTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="gkeClusterTarget")
    def gke_cluster_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gkeClusterTarget"))

    @gke_cluster_target.setter
    def gke_cluster_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f881a0bac1df1b3377891cf4bc464a2e0095a49937c0b3849d0f521a59fceb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gkeClusterTarget", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d44a9016f1f19bd43ab10b52405dce1a80ff0b14126e6083563b8d9afa5a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig",
    jsii_struct_bases=[],
    name_mapping={"component_version": "componentVersion", "properties": "properties"},
)
class DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig:
    def __init__(
        self,
        *,
        component_version: typing.Mapping[builtins.str, builtins.str],
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param component_version: The components that should be installed in this Dataproc cluster. The key must be a string from the KubernetesComponent enumeration. The value is the version of the software to be installed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#component_version DataprocCluster#component_version}
        :param properties: The properties to set on daemon config files. Property keys are specified in prefix:property format, for example spark:spark.kubernetes.container.image. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#properties DataprocCluster#properties}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a099ff68ce02d05fc036e4ab926bbf151100b0b613fc6ac2d3478d569326f700)
            check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component_version": component_version,
        }
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def component_version(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The components that should be installed in this Dataproc cluster.

        The key must be a string from the KubernetesComponent enumeration. The value is the version of the software to be installed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#component_version DataprocCluster#component_version}
        '''
        result = self._values.get("component_version")
        assert result is not None, "Required property 'component_version' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The properties to set on daemon config files. Property keys are specified in prefix:property format, for example spark:spark.kubernetes.container.image.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#properties DataprocCluster#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__986af20eb3e3c73596c743365e37d0e6d3b1f308853c4524364e08225876603f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="componentVersionInput")
    def component_version_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "componentVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="componentVersion")
    def component_version(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "componentVersion"))

    @component_version.setter
    def component_version(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98e72bd2c410f4240e27c0f9ed3fc54dc01a26992762331c4d325446d258f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentVersion", value)

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dfb18cd036bf41ecb492629ec12591f77e59713f1b72be4d799ef998c9354ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce485ccc104ed79d24eebd2099ccd93e91affa78663e1064a0e872759f12e762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterVirtualClusterConfigKubernetesClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigKubernetesClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5974b20438ad1ad687f4333fdc24020f05d15fce01d83f0cd55c3213af97d638)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGkeClusterConfig")
    def put_gke_cluster_config(
        self,
        *,
        gke_cluster_target: typing.Optional[builtins.str] = None,
        node_pool_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param gke_cluster_target: A target GKE cluster to deploy to. It must be in the same project and region as the Dataproc cluster (the GKE cluster can be zonal or regional). Format: 'projects/{project}/locations/{location}/clusters/{cluster_id}' Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#gke_cluster_target DataprocCluster#gke_cluster_target}
        :param node_pool_target: node_pool_target block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#node_pool_target DataprocCluster#node_pool_target}
        '''
        value = DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig(
            gke_cluster_target=gke_cluster_target, node_pool_target=node_pool_target
        )

        return typing.cast(None, jsii.invoke(self, "putGkeClusterConfig", [value]))

    @jsii.member(jsii_name="putKubernetesSoftwareConfig")
    def put_kubernetes_software_config(
        self,
        *,
        component_version: typing.Mapping[builtins.str, builtins.str],
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param component_version: The components that should be installed in this Dataproc cluster. The key must be a string from the KubernetesComponent enumeration. The value is the version of the software to be installed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#component_version DataprocCluster#component_version}
        :param properties: The properties to set on daemon config files. Property keys are specified in prefix:property format, for example spark:spark.kubernetes.container.image. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#properties DataprocCluster#properties}
        '''
        value = DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig(
            component_version=component_version, properties=properties
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetesSoftwareConfig", [value]))

    @jsii.member(jsii_name="resetKubernetesNamespace")
    def reset_kubernetes_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="gkeClusterConfig")
    def gke_cluster_config(
        self,
    ) -> DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigOutputReference:
        return typing.cast(DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigOutputReference, jsii.get(self, "gkeClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesSoftwareConfig")
    def kubernetes_software_config(
        self,
    ) -> DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfigOutputReference:
        return typing.cast(DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfigOutputReference, jsii.get(self, "kubernetesSoftwareConfig"))

    @builtins.property
    @jsii.member(jsii_name="gkeClusterConfigInput")
    def gke_cluster_config_input(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig], jsii.get(self, "gkeClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesNamespaceInput")
    def kubernetes_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesSoftwareConfigInput")
    def kubernetes_software_config_input(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig], jsii.get(self, "kubernetesSoftwareConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesNamespace")
    def kubernetes_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesNamespace"))

    @kubernetes_namespace.setter
    def kubernetes_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1006489ae6e5fc8933b9588f33dea62b40f941e8070ca942f645725fc878752f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesNamespace", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae0d67c20cb50baed75b7e025e0f08b32be29a05cf7742a9924b0abd6d709ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataprocClusterVirtualClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocCluster.DataprocClusterVirtualClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1574dffee73779f37a7267d731e3a05398fe1dde1e920b4203e78641895f3ff8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuxiliaryServicesConfig")
    def put_auxiliary_services_config(
        self,
        *,
        metastore_config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        spark_history_server_config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_config: metastore_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#metastore_config DataprocCluster#metastore_config}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#spark_history_server_config DataprocCluster#spark_history_server_config}
        '''
        value = DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig(
            metastore_config=metastore_config,
            spark_history_server_config=spark_history_server_config,
        )

        return typing.cast(None, jsii.invoke(self, "putAuxiliaryServicesConfig", [value]))

    @jsii.member(jsii_name="putKubernetesClusterConfig")
    def put_kubernetes_cluster_config(
        self,
        *,
        gke_cluster_config: typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig, typing.Dict[builtins.str, typing.Any]],
        kubernetes_software_config: typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig, typing.Dict[builtins.str, typing.Any]],
        kubernetes_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gke_cluster_config: gke_cluster_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#gke_cluster_config DataprocCluster#gke_cluster_config}
        :param kubernetes_software_config: kubernetes_software_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kubernetes_software_config DataprocCluster#kubernetes_software_config}
        :param kubernetes_namespace: A namespace within the Kubernetes cluster to deploy into. If this namespace does not exist, it is created. If it exists, Dataproc verifies that another Dataproc VirtualCluster is not installed into it. If not specified, the name of the Dataproc Cluster is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/dataproc_cluster#kubernetes_namespace DataprocCluster#kubernetes_namespace}
        '''
        value = DataprocClusterVirtualClusterConfigKubernetesClusterConfig(
            gke_cluster_config=gke_cluster_config,
            kubernetes_software_config=kubernetes_software_config,
            kubernetes_namespace=kubernetes_namespace,
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetesClusterConfig", [value]))

    @jsii.member(jsii_name="resetAuxiliaryServicesConfig")
    def reset_auxiliary_services_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuxiliaryServicesConfig", []))

    @jsii.member(jsii_name="resetKubernetesClusterConfig")
    def reset_kubernetes_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesClusterConfig", []))

    @jsii.member(jsii_name="resetStagingBucket")
    def reset_staging_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagingBucket", []))

    @builtins.property
    @jsii.member(jsii_name="auxiliaryServicesConfig")
    def auxiliary_services_config(
        self,
    ) -> DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigOutputReference:
        return typing.cast(DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigOutputReference, jsii.get(self, "auxiliaryServicesConfig"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesClusterConfig")
    def kubernetes_cluster_config(
        self,
    ) -> DataprocClusterVirtualClusterConfigKubernetesClusterConfigOutputReference:
        return typing.cast(DataprocClusterVirtualClusterConfigKubernetesClusterConfigOutputReference, jsii.get(self, "kubernetesClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="auxiliaryServicesConfigInput")
    def auxiliary_services_config_input(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig], jsii.get(self, "auxiliaryServicesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesClusterConfigInput")
    def kubernetes_cluster_config_input(
        self,
    ) -> typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfig], jsii.get(self, "kubernetesClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucketInput")
    def staging_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucket")
    def staging_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingBucket"))

    @staging_bucket.setter
    def staging_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e12422412806c9e8f6f80a2e8d8e615dd2cf122285a64ff38386823ad92491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingBucket", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocClusterVirtualClusterConfig]:
        return typing.cast(typing.Optional[DataprocClusterVirtualClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocClusterVirtualClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f7312e99a2d2daa4921e8278d7866e348b67f3829c71d9228be604dd890029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataprocCluster",
    "DataprocClusterClusterConfig",
    "DataprocClusterClusterConfigAutoscalingConfig",
    "DataprocClusterClusterConfigAutoscalingConfigOutputReference",
    "DataprocClusterClusterConfigEncryptionConfig",
    "DataprocClusterClusterConfigEncryptionConfigOutputReference",
    "DataprocClusterClusterConfigEndpointConfig",
    "DataprocClusterClusterConfigEndpointConfigOutputReference",
    "DataprocClusterClusterConfigGceClusterConfig",
    "DataprocClusterClusterConfigGceClusterConfigOutputReference",
    "DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig",
    "DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfigOutputReference",
    "DataprocClusterClusterConfigInitializationAction",
    "DataprocClusterClusterConfigInitializationActionList",
    "DataprocClusterClusterConfigInitializationActionOutputReference",
    "DataprocClusterClusterConfigLifecycleConfig",
    "DataprocClusterClusterConfigLifecycleConfigOutputReference",
    "DataprocClusterClusterConfigMasterConfig",
    "DataprocClusterClusterConfigMasterConfigAccelerators",
    "DataprocClusterClusterConfigMasterConfigAcceleratorsList",
    "DataprocClusterClusterConfigMasterConfigAcceleratorsOutputReference",
    "DataprocClusterClusterConfigMasterConfigDiskConfig",
    "DataprocClusterClusterConfigMasterConfigDiskConfigOutputReference",
    "DataprocClusterClusterConfigMasterConfigOutputReference",
    "DataprocClusterClusterConfigMetastoreConfig",
    "DataprocClusterClusterConfigMetastoreConfigOutputReference",
    "DataprocClusterClusterConfigOutputReference",
    "DataprocClusterClusterConfigPreemptibleWorkerConfig",
    "DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig",
    "DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfigOutputReference",
    "DataprocClusterClusterConfigPreemptibleWorkerConfigOutputReference",
    "DataprocClusterClusterConfigSecurityConfig",
    "DataprocClusterClusterConfigSecurityConfigKerberosConfig",
    "DataprocClusterClusterConfigSecurityConfigKerberosConfigOutputReference",
    "DataprocClusterClusterConfigSecurityConfigOutputReference",
    "DataprocClusterClusterConfigSoftwareConfig",
    "DataprocClusterClusterConfigSoftwareConfigOutputReference",
    "DataprocClusterClusterConfigWorkerConfig",
    "DataprocClusterClusterConfigWorkerConfigAccelerators",
    "DataprocClusterClusterConfigWorkerConfigAcceleratorsList",
    "DataprocClusterClusterConfigWorkerConfigAcceleratorsOutputReference",
    "DataprocClusterClusterConfigWorkerConfigDiskConfig",
    "DataprocClusterClusterConfigWorkerConfigDiskConfigOutputReference",
    "DataprocClusterClusterConfigWorkerConfigOutputReference",
    "DataprocClusterConfig",
    "DataprocClusterTimeouts",
    "DataprocClusterTimeoutsOutputReference",
    "DataprocClusterVirtualClusterConfig",
    "DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig",
    "DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig",
    "DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfigOutputReference",
    "DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigOutputReference",
    "DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig",
    "DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfigOutputReference",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfig",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetList",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscalingOutputReference",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfigOutputReference",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigOutputReference",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetOutputReference",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigOutputReference",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfigOutputReference",
    "DataprocClusterVirtualClusterConfigKubernetesClusterConfigOutputReference",
    "DataprocClusterVirtualClusterConfigOutputReference",
]

publication.publish()

def _typecheckingstub__d1361c52459d7f5c317fb6cc412435b35c41ec48fe8ebbb4ddb93198b939b35d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    cluster_config: typing.Optional[typing.Union[DataprocClusterClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    graceful_decommission_timeout: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataprocClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_cluster_config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__99428885c5edc513fa19b3666d1d528528b90948555f984820be4779a2e22637(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9811bc19c8bd8c28166c100e6000d42d9636e644b896af1cab00ae33671bfb41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d925271068a9f55f483d80781a7edc9de81abe68cddecbb8738f7d4baddd68(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79750a7321d8526e006c1c436690e363a135499d4f46ff6681bc7c11635d9bc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4ccd87d3fc961930eb7d4d4ea2434e52c0da104a946c9f097380388457b4cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03fcf68ef8cf3dc3fcb9bdddf5c1e8c5fdfd3973b5497bca5bf29ca92db2f081(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ebd1a663f62e6eb4ba021ba34bffb4f0b66deca8669a703806ddd54a6269f9(
    *,
    autoscaling_config: typing.Optional[typing.Union[DataprocClusterClusterConfigAutoscalingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_config: typing.Optional[typing.Union[DataprocClusterClusterConfigEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_config: typing.Optional[typing.Union[DataprocClusterClusterConfigEndpointConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gce_cluster_config: typing.Optional[typing.Union[DataprocClusterClusterConfigGceClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    initialization_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterClusterConfigInitializationAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lifecycle_config: typing.Optional[typing.Union[DataprocClusterClusterConfigLifecycleConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    master_config: typing.Optional[typing.Union[DataprocClusterClusterConfigMasterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metastore_config: typing.Optional[typing.Union[DataprocClusterClusterConfigMetastoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    preemptible_worker_config: typing.Optional[typing.Union[DataprocClusterClusterConfigPreemptibleWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    security_config: typing.Optional[typing.Union[DataprocClusterClusterConfigSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    software_config: typing.Optional[typing.Union[DataprocClusterClusterConfigSoftwareConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    staging_bucket: typing.Optional[builtins.str] = None,
    temp_bucket: typing.Optional[builtins.str] = None,
    worker_config: typing.Optional[typing.Union[DataprocClusterClusterConfigWorkerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2b0e0bb924cd4fa2603b98d6f0c96f70afb7418caf8d7b567c88aba62caeb6(
    *,
    policy_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e9baf4b634027e17b8c766049ba97bf2e64f181afa12425c0666db38c27895(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7766db844ace0cde2ec40b5c6bbb0b8847c37562d8e72e0c4bac2d128ac58952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6a45447babcf4de794be24fbf08704f8187ede924f3c70bd82c00d16cf5c13(
    value: typing.Optional[DataprocClusterClusterConfigAutoscalingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f323d9285643fc922bf8cb378c44546565832cb5fc9f82a1309cb8cf668652(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5558ad8aedc494571a717e99d3181c16f3988f4c73979762496b0efee27f6421(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a724eff7b84509369fc46c2668e13c2a011e9fad3b5f36e57e907a4a70fb3ae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eca4696922f8e886d6b10b18cfa659e4f462ca9ef089e536b082ea1904deed5(
    value: typing.Optional[DataprocClusterClusterConfigEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abed7dd0e9404699d2efde3c9cc15ca624114579ad97c088a16df6c79a5f398a(
    *,
    enable_http_port_access: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601f361f41b67c9ba6e7edc31dec832e9b876469710bc150c92796062069d3cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2217068902d6c92148027089e087d05d05f71f130e404300ee9f1c7b478c2741(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d36ba828aadfa3b73df3b372ccb7f2cfea6d090f816b6a44d972113e573ed1e(
    value: typing.Optional[DataprocClusterClusterConfigEndpointConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae83a0087abf138cdc7686f6ddf05150339cb235982ce2197d5b9d0330bcecc9(
    *,
    internal_ip_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    shielded_instance_config: typing.Optional[typing.Union[DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f07a54ac970aedfda79ca17b4e387af422fb6e6bab6acf0393979d22e4c804a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e0c7723e6560e795a88604889c7a387b26dd89159cab44fd60151b7de8cba8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b8dc5b947381789c0b69b355432d60c698e51d7e0b410a9d1c50eee8094143(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195487a66a38bab7efae39d603a8d69c7f5ae38781705c1caf237636fcaac74b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9664424eb7fc135c5bd9ea0ecc624c7d6e522b4ff961167049558f8ee71bb84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f79b12413004321591219dbabb574961196a94151161e626b1ab2969584475(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3195e710ad97f345964cb5b925c6d72cffe3235acffe9600aeb71c45942c538c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579954a5eee5480b5dcdad68fe5639712dfdb275d4697e9d4626013fda8adce8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b59eb7dcfce186512f0891d8d2b6e89e2c3f3cb9da9ee080891f14bcffb443b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a98e35f1468dd367d15d28f7d96fbaca8626ead1872f2324ad7f56c9ef2584(
    value: typing.Optional[DataprocClusterClusterConfigGceClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fa2722da5048a09b9da96543437b900ab95e0d826e784041d26ed59c6a5694(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49a209a43b6bd308d44a5f3ec87c4bb35a0bff7077a2f40de72b88408d92326(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece8824f4ec90422e2a376866ba25c2787da45b972aa2eb7cf3ffebc5293a35b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5ba5e87d20f40258260bacdfd2436e966fadfffad99073720eeedc99487214(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf580c6c825f799be4f68366ea6d9dc7a89641883ba4dde7004cc33480e0719(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9dcbf40159e03977aeb677f488b9ff16e070efd3a263b1a8cf3f4717b50a07(
    value: typing.Optional[DataprocClusterClusterConfigGceClusterConfigShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc72500ea70f15d82e3d65c6b55037e0dfffef4e4d6d02c100c77323098b962(
    *,
    script: builtins.str,
    timeout_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109f97ed3f310c9e978fd9e953ab4f58b20d0fb36ce736f9e4e3b89db5f0ae96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3100838196617f2c2d48faa6c47cbc0b8f3ca34918bac0c88ab18446428387b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0a00c9d6281f1bb95bea56f1b3ffbaec2b64c289a412e0b88cd4d95cd5ef26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4418148e3e220cf70a1b0c2d2cfb72e1b64c3fb6052ff6eae5c72aa5529fdeef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0eee2acf3690873a8cf26afb7e02a9ca92f469461eb6ad8e90ff381b62763bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ef30e367814905f4c96c40f7e8db6bb8af46fa52550b29c467c9f41fca82d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigInitializationAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e213029e5d8e2886dec7c4a9d5b6fc6686d37d4a985a3ffdfdb82ee44f30a80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be3a38bd1c8f321dfbf1a9dd6747255259258948b267c7c51ff48bf285665ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1b2f74b47e1b717c8246b6d281c651556dfac2b467e22835355efc99ed7bd8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca6b3bc6d029fa0cc0497bb9224185d8772412e2512f91ac3bf02be5434c888(
    value: typing.Optional[typing.Union[DataprocClusterClusterConfigInitializationAction, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f8e00bbd6f14c5a419f1acf6ec406dbca1194438c02d56e29750513ccd8bd0(
    *,
    auto_delete_time: typing.Optional[builtins.str] = None,
    idle_delete_ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c44c95af8e1a85bc95f04daf1cb0cd641c3f037641fbb98b3fe1e84498c119e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53736dc1f675ef3228450f0c022a37a8ade4eff7b328cccde8a2307cd3ec9aec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d537c8a347e055f319508c502046b10c6a8bda10f9724ec3aaaef9d6697231d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8278d4a6ca217e008667e322158926176b84265b3a9e462232dcf270bc9c06a9(
    value: typing.Optional[DataprocClusterClusterConfigLifecycleConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45854c553ce00b06aa99bf4b4ef1a7e404000a802afc2165eebd5980398c2447(
    *,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_config: typing.Optional[typing.Union[DataprocClusterClusterConfigMasterConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    num_instances: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d24ab99db5c0b11130c2347390148fc4f94c8218263d89a9ddc0ac1fb2d7e53(
    *,
    accelerator_count: jsii.Number,
    accelerator_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aeae9fe2ae8421b2c40d55cb25448207691e609571c756c34972581e71fdac0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa948c1668e28e6e8edb6460a26a01f87e35b7ea34cf6cdd3d86e923e384e368(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c9c7688d9af86f73b6777aa66579886cf5bc75a74db4e25aaaf35af2c4296f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4dde6362eaeeae6005d6d248281cce3dde9c442ef74dbe7d5ebf887a864b019(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443a29293231a08226a5aba1a335c75905e2a036bb3d819a4a1d0010110593b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0b414a0942bc5e90153e7b37ffd4fc6963c2ef42180240d048c29d30095d5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigMasterConfigAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e354d6d7ce05e91d59ba7e3e2cb33a96e6f9e415f330d39f3bfb4032bdc497df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c698fc19ebb1eabb8abc04bf52c166a62a1f4c43606e14650e3927623ef9ff1a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d227f31be2690d8490080dff407ef65ffed9480726daf29e683ee33cb814216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f760252aec18ca06104f40f6eb0491e316d62fab64b64c2feb8d1ad12822dc35(
    value: typing.Optional[typing.Union[DataprocClusterClusterConfigMasterConfigAccelerators, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b8b0871bd095581c9baef18e9ed02aedea04b46ac26b41be557d8dd6a24ded(
    *,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    num_local_ssds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66e2395115c39953bc1872f8c9ce6812f4ccc1d9d30b17ebc0e84e0ab7cf0ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee5960fb15c857b2ebeff6847d45c862b64434208a91b4706e364fc42e61eb2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7a7717affe46cbf85ae01d1fb5bc03cd6977d2f744a4d603a8f9d6b2e4e5ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3c41ae9388e75de7d1267eae8980e8b6c99cbb014ed32a3be09efd012b73e9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d2e3f2f749c6af41dcce6f1d688a8fd7b5d91ae5883f292ffb4e2ec66a99fd(
    value: typing.Optional[DataprocClusterClusterConfigMasterConfigDiskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c3770ff05025df38a717c3164d46140d2d4cca76400f690cb8469370ff7e57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65114f1d1fe2f53a4b2aeccde75ff4dd8e114f89c21b8b5ce1eb096d9aa8a922(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterClusterConfigMasterConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6564616b831c52281f910975a25b3109d5d92289dcf835ce26de652237ca2f87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c199e37d83b5df23772ade3f88cc9c2345e8ab5986fbbf3ae2444ef9dc2d37ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a6e1da4c7a23550712f8c3664269721fdb6d94ad1033db18e678a0a8670296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19348ea95b15abdd232872e6550b64ba37464e48f4472cf04153075e0d07fa0f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352aedd8d4b5f3980fe15cf5a5dcdf47aff40c6e00c7b88ca4c4bb92f4d6af9d(
    value: typing.Optional[DataprocClusterClusterConfigMasterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d078ca40cdff638ab61c7c480d496ab7765500ff85fe007c73fedc875e16b0(
    *,
    dataproc_metastore_service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba729f4bdc9f6d373a0d0d3c3c8f7509e99a16e4afaf933f0df6ead8c33a530(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4855fe35b045b79b5547b658b97b3fc996feeb3d71791d371c3da93ebaa37ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc5c0b97177cfcf9ad58b98d2cb136187d475c23b502be3c976d05f8fc8d4d5(
    value: typing.Optional[DataprocClusterClusterConfigMetastoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d786ca78e84d1a0aa8b4147f8fee7ea7c567690ad0f6cc4f8e43ecac653454(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c514f3665386fd2ebd5b1c0a3a917b5b75a0b5175c60d087cf152d767b3c1a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterClusterConfigInitializationAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9577ed9e732b663f0d86025c39fcd68a1f51b55213d09d9d7c76c9e91226433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9aef639e8148b47aeb33614b5e3cdc7fad7f9a7b1c34904f1ecb4de1c8c3fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69266c0b3947471dc43cd9a334e6dba69f148a709926f2c86b7f6b734916e6fd(
    value: typing.Optional[DataprocClusterClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49bf03f523760e43e550b4f98a609b968d5ef099cf4a9e0dc44d9dd5215922c1(
    *,
    disk_config: typing.Optional[typing.Union[DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    num_instances: typing.Optional[jsii.Number] = None,
    preemptibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6285385062cd45cee0d2d61128dc4b4d340e186e4b621012f4f52abad1000067(
    *,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    num_local_ssds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5665c060036ddc6b12495e64980e3c69be44dc4755649d87434f4c7ddf134d52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085d649f74d2278f8c18895b22fe17f4a0fa58574dc66ac4de21fd06ebe8cc5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be222f0640520593d58c2d5a603e39fb5040909f97cf6dbebcf5de378c753424(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e552a83c928b054a735d1a845c18e90bce9c2a57f2e4355595c4d3d9197cd4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea3c1ce490dbde957d5cbfee16cd4847b814a9d9513b9cc5442294ced16716d(
    value: typing.Optional[DataprocClusterClusterConfigPreemptibleWorkerConfigDiskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b548f1b6c480c65f9c245698eb78bcb20a397e9c9fa4e10bb7e8cf1e0314304a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547ff68502839cf6258112376af9a49ef86cccd429ef88083a60624d499a3c79(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3add78efaaf5d613d77783fdd67354d8c0f2ad69e538ffc9ccd1ddcb8a0cb79c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f8bcd5221db8064a8553b94eaaef714ec31e7a53061f31e3efd24736056e21(
    value: typing.Optional[DataprocClusterClusterConfigPreemptibleWorkerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38c767b44cb6f9387afc5039914ebe605b98825b9055955ae32395941951629(
    *,
    kerberos_config: typing.Union[DataprocClusterClusterConfigSecurityConfigKerberosConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503f77456cabd2cfc22147b6e67e4dc96357f993b34d929ac452aee3125d2e0c(
    *,
    kms_key_uri: builtins.str,
    root_principal_password_uri: builtins.str,
    cross_realm_trust_admin_server: typing.Optional[builtins.str] = None,
    cross_realm_trust_kdc: typing.Optional[builtins.str] = None,
    cross_realm_trust_realm: typing.Optional[builtins.str] = None,
    cross_realm_trust_shared_password_uri: typing.Optional[builtins.str] = None,
    enable_kerberos: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kdc_db_key_uri: typing.Optional[builtins.str] = None,
    key_password_uri: typing.Optional[builtins.str] = None,
    keystore_password_uri: typing.Optional[builtins.str] = None,
    keystore_uri: typing.Optional[builtins.str] = None,
    realm: typing.Optional[builtins.str] = None,
    tgt_lifetime_hours: typing.Optional[jsii.Number] = None,
    truststore_password_uri: typing.Optional[builtins.str] = None,
    truststore_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1f76ab8feebdd90b10fca4b9da15a0cdd7cc685206c0bb2bb7bca50055cf40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c857382d99784846617c163b38357eedd6160b4fe0b44a8bad3ef0725e9fdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc68b74a37e183b36a95614a8c98ee78b22be75644aae34cfca307507d5ab45e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c62d8205ba2cd9fc1d1f3ff858b334088c6a859cc2dc1c414f80d3adef8de56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccb42ac4d70700feafaca9597ca55cef69c9d773f315de69ba887b3844d6d0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7649ed1719c159650dfcd1121a4f531eaab6abccf8719e74a2e48cbd5e7eeeb5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34d10ee17bd5ee2aa03c5590d39537f098a8168459be86eedcfa7f09ac58286(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7909933b45bcf127354ceb6ad8a0c1583277622c0845b59528738b9c6af5b85f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ebc695b7860885e735e24231d278622ccb8435a9249bb4960e43c97b237ea76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d096fb4dd14930d329a8766f2ecdb675b4416eb2a167f6737b86bb0a1abcebce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30252b51699c7a6aeb55cb6f8d709cd603e48a627b74a45f92e34bfe47649d43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc61ddd934955620a0faf36d05ad19361909ff4840a330c9a111259bfb2b9d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1471d82a4e2d2a62880475502a480f159f1168d68729197c15df7d6391e9a080(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf143e76e934023f34e235bb4afc6c0501a7b5b11b3c5120cdefeb2d0ff82c05(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513c826694d88ea71467943e006dd54ab8682b47cc8d1091a01473b34b5a185a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8536f375df9ea149c53018763dcdc0e3a075c2f2e159c8fa7390aa3ce4c69ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4b362c6c0cb5a503a03fb0c84eb3bbadf83279304be7e0c2c0ae51cd541b2f(
    value: typing.Optional[DataprocClusterClusterConfigSecurityConfigKerberosConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__587cc146cd670c4af43c7d5eb6a5c57c83c963779b74127e325bee895e94b216(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a0ff51af259e6f827745832125cad8c9064aa86ef6bc2920d018fdf2008ef1(
    value: typing.Optional[DataprocClusterClusterConfigSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822dc890087f54c3079a5cd83118c8967c5cf55741543ad25a9fbaf94a6a4d2b(
    *,
    image_version: typing.Optional[builtins.str] = None,
    optional_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    override_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecd818e2d794e372cef09a7a5f022a01664b523df7b7d72625e08ac1decf825(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6279c96483c2112deb0699f09ac348e95b95f02809f905d4ccccffb10c3ddd96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b432dbafdddf77ea37d675405878a35e5e8d745cfb266c7640ee06d19df1b0e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40edc46650ec73be08cb3f8f30b3d4a241eee69c15c4adb0e55de09e5d9cd817(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93fef1c414888a1facc48cc25b826de6d8e21c27bc151aad1d1a994e922c046e(
    value: typing.Optional[DataprocClusterClusterConfigSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80262d5e41f8aaefcdc1c316e17493d27924312c55b0b8b0ee553ac3f6a188c(
    *,
    accelerators: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterClusterConfigWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk_config: typing.Optional[typing.Union[DataprocClusterClusterConfigWorkerConfigDiskConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    num_instances: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb8115d8b88c41af0fec9d9404aaa9477e5a18061f1f00937dcb25bd82b6d98(
    *,
    accelerator_count: jsii.Number,
    accelerator_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a8f9892f6a6b08c882be9e79e05d109a4cfe1315f89311eabf917684446848(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22bd8599b11dc1616270dcac3f30c0a64220d2d83e7167d92a1f86adbc86979(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6249924a07f26231202b327e9c4a59e1af9630be8759101195b0b55ffa4c9d39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c21c77f4e28eaeb3270c6c096b72960b7cc13a52eea9990b82b80546d0a3f23(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc120ca5376ffbd963899ac4fbd6b74e2ec77cd44d18da8318d206532b63434f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6eb31dabebb89233b1c85a885e37b1861902da8bafcf690d2b2a753be33982d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterClusterConfigWorkerConfigAccelerators]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a1b699b22520a45f78c4101403f4831dc68ec322088e6ba170f9ae4db4d2e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66974c73a7fe0b96f177730402895a3d7ee0825c9c226fddfc4861974b86f67b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7affed043b1f92f2cc6251d5467d730fa7141b2d3cac75590af5ed4310d88a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30ef421d1ed58432ca9b7cc4f6a2d2023b53ab6ad143f82e086435b7804addb(
    value: typing.Optional[typing.Union[DataprocClusterClusterConfigWorkerConfigAccelerators, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205b56d220620927788db71e1d60b1eb6741f8e84eabe90e2fdf75d4c5257df5(
    *,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    num_local_ssds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bd2fc4fd91ba1b55cc32a8f25c62e7af3f22f4ea1bdc647b2c217ad0bafa00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10732c9735c28d76f47daba77b4d8fadee3b3235347bcccfaa7b6275782e39b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ce9c602c615bfecf33d6b023dca8344fc9b3a98622f9b8f33f6f3a0e09e68e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1a9a97af819d5324f85cb4446798835ade60a3c63d50d4c25ee6bcc872d82f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d78fd349314051492bef38bd53824bf6b19e5ff304a98356c41d6d79249762(
    value: typing.Optional[DataprocClusterClusterConfigWorkerConfigDiskConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74524adbe1b1735e0513e4072fc67add33e7c03f1a226662aa9fb1f3e2d63f21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebcf06522db70669168011d1abff8031dd5b65a729e43f9e730d33ff973944f2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterClusterConfigWorkerConfigAccelerators, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc9625c43697a9dad6d0d7e0633419310c032a51c5a82c7e48e427d9217d4df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e57960dc12d3047b9938b72a0278c7663350067be411bcf8304cbf3787de237(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4854c2297c34dece6102463adf11994cb69403c885c2999714394487537130dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b189c368aa3b6733a69d75e8463fb3b6588f793fa9d43aaae051930b1d2afc7f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b616597eb875e21eb36331e76a5d91ccdf77b40658c8082dde249ae02668902(
    value: typing.Optional[DataprocClusterClusterConfigWorkerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed5644cd8fb56e1eaa06d727a133e9fb445bda9f5ff5bf9e88339bab33e50bf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    cluster_config: typing.Optional[typing.Union[DataprocClusterClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    graceful_decommission_timeout: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataprocClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_cluster_config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a613b8d951875abe58651dab277cf4df7ef14e32a9326c6761e133cba07c97(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069813e8660e54f1ac9d46fe435030af350ee3b67a3ac08ea7ce4505605b9dd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050e90691edbe0a6eebb054d131d16d5deedd5e594fca2da0d2d39c2a3e65860(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c366796bb2334dca018edc6ae9cd7b39472da15889de41e2782ff8995d8468(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06405c43678140ef48a048844baf4cecfcd753dcb8ff1b166f65b69ad122a49b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db616b8fec382d4f3eb073fcd4017591f49ef95b1426506e82c3c5a410a3b80(
    value: typing.Optional[typing.Union[DataprocClusterTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c2306960f0feabb80acfa6a8ae9999fd42d8a1a59ef68c1799dee0ea6af910(
    *,
    auxiliary_services_config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes_cluster_config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    staging_bucket: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708d9c98802232c52f3e8001da74152b384e65f7aa164aacd577e195582aa7cd(
    *,
    metastore_config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_history_server_config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395ec210f5c3915ba1eb598d649f5e911053c14131ec190f7b662cb0e05923a2(
    *,
    dataproc_metastore_service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ab6305d8d11409804e8abed1dd47518d87915caeb2f4987ff8167041803a7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7776f089183dc195cf0321e79dcf89b57c3a33ca4036b0834e38e113fd3b49f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95372c4dc76c73faf97d56d9d2a48a32785d845dbe7268f8a606101b8791ede(
    value: typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigMetastoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72264dd65842e1715d713bab787df4cbd986391bf69b0028aab126019b3fad33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958db16e0649f5a11928a60dbfb1d26cc463eefe7ddd69beb9bb6effb875de43(
    value: typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b840cfa8bb2c3e51bc69865fcddeb6b5a25af130b017b13c466e6eb802c4eb(
    *,
    dataproc_cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e947988b76f83abd92cbce46ad5f654c1bd1ffc48be4c0b49f79122db853b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d271315367d0c41f9f7b5dd6f19a39abbeac04e9f0efa559b3e74a40a17ee82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee6c95385b2b2ab925a0c6fa5f429d93d99d970b5162e1d77db6888f2a360ec(
    value: typing.Optional[DataprocClusterVirtualClusterConfigAuxiliaryServicesConfigSparkHistoryServerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddbfc62f23141ec847b3ce7f3ce85da175f19fafba0b2850c3c05ffc47f6c86(
    *,
    gke_cluster_config: typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig, typing.Dict[builtins.str, typing.Any]],
    kubernetes_software_config: typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig, typing.Dict[builtins.str, typing.Any]],
    kubernetes_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8e6d66631834d9031f383bc8eacf0b9839d86cc2900280431f71a817b4f788(
    *,
    gke_cluster_target: typing.Optional[builtins.str] = None,
    node_pool_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59cefbf0fdfe22c3bfc12b7dcfabc15f783b462ab7ae2a7576b2be131ea7f82(
    *,
    node_pool: builtins.str,
    roles: typing.Sequence[builtins.str],
    node_pool_config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296e6699b41b6488d5c2e5ca0b117ff1090309457e5624b4173b7fb8fa37cc0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fe83488dc2beddc752ffa0487add80b11f318565718c56918e1c39df2d748d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20b11a9760deece28713ac9483c8d5a102ffb7af219e82fc450d4918a54bfcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f06269f6c39c292ba7aaec519ebde3c77f2c59c9ff1e2f521eb6b1f49c065ba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b7dcd24ad514886b9882aad112af050d582d561bb800558a5a43630cd3a7e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625790ec1b3fe7bfe6aace06935fe9d01a308dcdd6955270b027e327b16dbca4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a7712083a09ee0b0297319d9b13b4da2629eae926803ab78b8aba4d6505820(
    *,
    locations: typing.Sequence[builtins.str],
    autoscaling: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling, typing.Dict[builtins.str, typing.Any]]] = None,
    config: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab56bc3b7959b9500408b35790c01ab6da6e08ce42a8c5ed96548b8c9db5ebc(
    *,
    max_node_count: typing.Optional[jsii.Number] = None,
    min_node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f24f18f1b7575a10243878aee56305c355ba6c88e6972f635ee72518fa1247(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb40dd5436ef8bbc64e71b4e8bf9f15eae3f24c8b7cfb2cc86742c02ae2ad61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c2be24f0da45c3abe2263e69930e3e06b17e83723dbf8be6940cde774f2cb3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b44876a72f90ad7dd2f6107e08e6c9c676d3ecba5de74c1f34e186c3ac01c1e(
    value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigAutoscaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e3f230d1a6a1eb9d787aefc2fe25715f6cc1b8a960fbe6b6cee2ef78ab6c4f(
    *,
    local_ssd_count: typing.Optional[jsii.Number] = None,
    machine_type: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531a8d8af0b6f8843a92906be84fc621b86fc5cc69377c9af42a3d819898bc65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a014ef708fd9ad98f8ac42f1c27508a22510d6ea0a1cb66e501a87ef49a11572(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330d708fec59bdd9badff5206b7622b6aab1b76d8995653306d347928ab8055e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacd5535bb981b75ff39a7cf94caaf164ea1cef2e31719f8a64f8c1a5b5dad7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbdeb7835160a63501de93e23162b99be9ce8afb8733655768b5e926e0fd49ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf081804886fa3032bb86ec8dbba01cfdd7d162620c48909540704d27a5b4c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__becc6c46bbd231321cb500b8f842330e1474e2aebecc372724c0ade78c38e483(
    value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfigConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef758c1f6796c9f6cb3d2e6bd720dc4997496d17b02d0b29b4bdf9bfac381fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c556d5513beb07b7397aae2989e1520735b375d238e5edec4d4822a189860d7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9253a20ef58b7c6b0fdc5bdfdc2df4956f52bd3f02b6ff7b04b1d596e32a2698(
    value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTargetNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ebf4a7a3b3c1b5e9f2837a3ade94be37740c525a7b7713bd0bf954c2a33669(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee209fde9fbb8f8da4049ed72df67172f3445734df0509dd9f86828af4dfc445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803f416b98f7b56f4a171a985f85eb40d967972f260de81977703ee2a6c50b98(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e57e772a51c469848c277789c0c970f1cf79128bfee6a8cd7a8ab24dbf2aca0(
    value: typing.Optional[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3d0f2fe070e7589c377d32bf0fefda33ba66009bab04f881e832409c476cf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1a4f74d98e2defa103d54455fc54a8e1897fd2c538992e5dad9784ff7f7ccb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfigNodePoolTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f881a0bac1df1b3377891cf4bc464a2e0095a49937c0b3849d0f521a59fceb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d44a9016f1f19bd43ab10b52405dce1a80ff0b14126e6083563b8d9afa5a51(
    value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigGkeClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a099ff68ce02d05fc036e4ab926bbf151100b0b613fc6ac2d3478d569326f700(
    *,
    component_version: typing.Mapping[builtins.str, builtins.str],
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986af20eb3e3c73596c743365e37d0e6d3b1f308853c4524364e08225876603f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98e72bd2c410f4240e27c0f9ed3fc54dc01a26992762331c4d325446d258f31(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dfb18cd036bf41ecb492629ec12591f77e59713f1b72be4d799ef998c9354ff(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce485ccc104ed79d24eebd2099ccd93e91affa78663e1064a0e872759f12e762(
    value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfigKubernetesSoftwareConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5974b20438ad1ad687f4333fdc24020f05d15fce01d83f0cd55c3213af97d638(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1006489ae6e5fc8933b9588f33dea62b40f941e8070ca942f645725fc878752f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae0d67c20cb50baed75b7e025e0f08b32be29a05cf7742a9924b0abd6d709ae(
    value: typing.Optional[DataprocClusterVirtualClusterConfigKubernetesClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1574dffee73779f37a7267d731e3a05398fe1dde1e920b4203e78641895f3ff8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e12422412806c9e8f6f80a2e8d8e615dd2cf122285a64ff38386823ad92491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f7312e99a2d2daa4921e8278d7866e348b67f3829c71d9228be604dd890029(
    value: typing.Optional[DataprocClusterVirtualClusterConfig],
) -> None:
    """Type checking stubs"""
    pass
