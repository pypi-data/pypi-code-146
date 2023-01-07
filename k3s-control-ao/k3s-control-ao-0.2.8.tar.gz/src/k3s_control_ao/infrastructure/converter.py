from typing import List

from ddd_objects.infrastructure.converter import Converter
from vpc_control_ao.infrastructure.converter import (
    instance_user_setting_converter,
    condition_converter,
    instance_info_converter,
    command_setting_detail_converter,
    command_host_converter,
    command_item_converter,
    command_request_converter,
    command_setting_detail_converter
)
from vpc_control_ao.domain.value_obj import(
    CommandResponseStatus,
    Text,
    DeltaTime
)
from ..domain.entity import (
    DeploymentSetting,
    DatapipeResponse,
    DatapipeDataInfo,
    DatapipeServerInfo,
    DatapipeResponse,
    DatapipeHost,
    ReleaseNodeInfo,
    NodeCreationItem,
    NodeCreationRequest,
    NodeInfo,
    NodeUserSetting,
    PersistentVolumeClaim,
    PersistentVolumeClaimVolumeSource,
    Pod,
    Ingress,
    EnvVar,
    PodContainer,
    EnvVarSource,
    LabelSelectorRequirement,
    NodeSelectorRequirement,
    VolumeMount,
    JobSetting,
    SecretUserSetting,
    Deployment,
    ConfigMapUserSetting,
    Namespace,
    ConfigMap,
    ContainerSetting,
    SecurityContext,
    LabelSelector,
    Service,
    NodeAffinity,
    PodLogSetting,
    Job,
    VolumeSetting,
    TCPSocketAction,
    Probe,
    StorageClass,
    NFSVolumeSource,
    GRPCAction,
    KeyToPath,
    ContainerPort,
    VolumeSource,
    Secret,
    PersistentVolume,
    LocalVolumeSource,
    NodeMeta,
    HTTPGetAction
)
from ..domain.value_obj import (
    ServerEndpoint,
    AccountID,
    AccountSecret,
    DataBucket,
    DatapipePath,
    AcceessMode,
    ConfigMapType,
    ContainerArgs,
    CreationTime,
    DNSPolicy,
    DockerImageName,
    ImagePullPolicy,
    Info,
    Label,
    LabelDict,
    NodeCreationItemID,
    NodeCreationStatus,
    NodeSelectorDict,
    NodeType,
    ResourceDict,
    RestartPolicy,
    Server,
    GPUType,
    ServiceAccountName,
    Token,
    VolumeBindingMode,
    PersistentVolumeReclaimPolicy,
    PodResourceDict,
    ServiceType,
    DateTime,
    Port,
    NodeName,
    Value,
    Base64String,
    Protocol,
    InstanceTypeStatus,
    LabelSelectorOperator,
    Name,
    BandWidth,
    ReadOnly,
    ContainerCommand,
    Provisioner,
    NodeLabel,
    InstanceType,
    NodeStatus,
    ZoneID,
    MatchLabels,
    Path,
    Integer,
    RestartNumber,
    StorageClassName,
    Version,
    JobStatus,
    HTTPHeader,
    PayType,
    RegionID,
    VolumeType,
    InstanceTypeStatusCategory,
    ReclaimPolicy,
    SecurityGroupID,
    K3SRunTime,
    InstanceID,
    Number,
    InternetPayType,
    Bool,
    IP,
    Operator,
    PodStatus,
    Type,
    ImageID,
    VolumeName,
    FSType,
    Status,
    EnvVarSourceType,
    Hostname,
    Key,
    Size,
    PathMode,
    Price,
    Capacity,
    AccessMode,
    NetworkScheme
)
from .do import (
    DeploymentSettingDO,
    DatapipeHostDO,
    DatapipeResponseDO,
    DatapipeDataInfoDO,
    DatapipeServerInfoDO,
    ReleaseNodeInfoDO,
    LabelSelectorRequirementDO,
    NodeCreationItemDO,
    NodeCreationRequestDO,
    NodeInfoDO,
    NodeSelectorRequirementDO,
    ConfigMapUserSettingDO,
    EnvVarSourceDO,
    NodeUserSettingDO,
    PersistentVolumeClaimDO,
    PersistentVolumeClaimeVolumeSourceDO,
    SecurityContextDO,
    SecretDO,
    PodDO,
    NamespaceDO,
    ContainerSettingDO,
    NodeMetaDO,
    SecretUserSettingDO,
    NFSVolumeSourceDO,
    ContainerPortDO,
    LocalVolumeSourceDO,
    VolumeSettingDO,
    ConditionDO,
    LabelSelectorDO,
    PodContainerDO,
    TCPSocketActionDO,
    InstanceInfoDO,
    EnvVarDO,
    IngressDO,
    HTTPGetActionDO,
    StorageClassDO,
    VolumeSourceDO,
    JobDO,
    GRPCActionDO,
    PodLogSettingDO,
    ConfigMapDO,
    PersistentVolumeDO,
    VolumeMountDO,
    NodeAffinityDO,
    InstanceUserSettingDO,
    ProbeDO,
    DeploymentDO,
    JobSettingDO,
    ServiceDO,
    KeyToPathDO
)

class NodeUserSettingConverter(Converter):
    def to_entity(self, do: NodeUserSettingDO):
        return NodeUserSetting(
            name=NodeName(do.name),
            k3s_token=None if do.k3s_token is None else Token(do.k3s_token),
            region_id=RegionID(do.region_id),
            disk_size=Size(do.disk_size),
            bandwidth_in=BandWidth(do.bandwidth_in),
            bandwidth_out=BandWidth(do.bandwidth_out),
            image_id=ImageID(do.image_id),
            node_type=NodeType(do.node_type),
            postfix=Bool(do.postfix),
            diff_instance_type=Bool(do.diff_instance_type),
            random_password=Bool(do.random_password),
            internet_pay_type=Type(do.internet_pay_type),
            master_ip=None if do.master_ip is None else IP(do.master_ip),
            inner_connection=Bool(do.inner_connection),
            amount=Number(do.amount)
        )
    def to_do(self, x: NodeUserSetting):
        return NodeUserSettingDO(
            name=x.name.get_value(),
            k3s_token=None if x.k3s_token is None else x.k3s_token.get_value(),
            region_id=x.region_id.get_value(),
            disk_size=x.disk_size.get_value(),
            bandwidth_in=x.bandwidth_in.get_value(),
            bandwidth_out=x.bandwidth_out.get_value(),
            image_id=x.image_id.get_value(),
            node_type=x.node_type.get_value(),
            postfix=x.postfix.get_value(),
            diff_instance_type=x.diff_instance_type.get_value(),
            random_password=x.random_password.get_value(),
            internet_pay_type=x.internet_pay_type.get_value(),
            master_ip=None if x.master_ip is None else x.master_ip.get_value(),
            inner_connection=x.inner_connection.get_value(),
            amount=x.amount.get_value()
        )
node_user_setting_converter = NodeUserSettingConverter()

class NodeCreationRequestConverter(Converter):
    def to_entity(self, do: NodeCreationRequestDO):
        return NodeCreationRequest(
            node_user_setting = node_user_setting_converter.to_entity(do.node_user_setting),
            condition=condition_converter.to_entity(do.condition)
        )
    def to_do(self, x: NodeCreationRequest):
        return NodeCreationRequestDO(
            node_user_setting = node_user_setting_converter.to_do(x.node_user_setting),
            condition = condition_converter.to_do(x.condition)
        )
node_creation_request_converter = NodeCreationRequestConverter()

class NodeInfoConverter(Converter):
    def to_entity(self, do: NodeInfoDO):
        return NodeInfo(
            node_name=NodeName(do.node_name),
            node_type=NodeType(do.node_type),
            node_status=NodeStatus(do.node_status),
            instance_id=InstanceID(do.instance_id),
            instance_type=InstanceType(do.instance_type),
            hostname=Hostname(do.hostname),
            price=Price(do.price),
            image_id=ImageID(do.image_id),
            region_id=RegionID(do.region_id),
            zone_id=ZoneID(do.zone_id),
            internet_pay_type=InternetPayType(do.internet_pay_type),
            pay_type=PayType(do.pay_type),
            security_group_id=[SecurityGroupID(s) for s in do.security_group_id],
            node_label=NodeLabel(do.node_label),
            cpu_number=Number(do.cpu_number),
            memory_size=None if do.memory_size is None else Size(do.memory_size),
            gpu_type=GPUType(do.gpu_type),
            gpu_number=Number(do.gpu_number),
            instance_type_status=InstanceTypeStatus(do.instance_type_status),
            instance_type_status_category=InstanceTypeStatusCategory(do.instance_type_status_category),
            instance_name=Name(do.instance_name),
            instance_status=Status(do.instance_status),
            instance_create_time=DateTime(do.instance_create_time),
            os_name=Name(do.os_name),
            public_ip=[IP(i) for i in do.public_ip],
            private_ip=IP(do.private_ip),
            bandwidth_in=BandWidth(do.bandwidth_in),
            bandwidth_out=BandWidth(do.bandwidth_out),
            node_expired_time=None if do.node_expired_time is None else DateTime(do.node_expired_time),
            auto_release_time=None if do.auto_release_time is None else DateTime(do.auto_release_time),
            key_name=Name(do.key_name),
            run_time=None if do.run_time is None else K3SRunTime(do.run_time),
            k3s_version=None if do.k3s_version is None else Version(do.k3s_version),
            _life_time=Number(do._life_time)
        )
    def to_do(self, x: NodeInfo):
        return NodeInfoDO(
            node_name=x.node_name.get_value(),
            node_type=x.node_type.get_value(),
            node_status=x.node_status.get_value(),
            instance_id=x.instance_id.get_value(),
            instance_type=x.instance_type.get_value(),
            hostname=x.hostname.get_value(),
            price=x.price.get_value(),
            image_id=x.image_id.get_value(),
            region_id=x.region_id.get_value(),
            zone_id=x.zone_id.get_value(),
            internet_pay_type=x.internet_pay_type.get_value(),
            pay_type=x.pay_type.get_value(),
            security_group_id=[s.get_value() for s in x.security_group_id],
            node_label=x.node_label.get_value(),
            cpu_number=x.cpu_number.get_value(),
            memory_size=None if x.memory_size is None else x.memory_size.get_value(),
            gpu_type=x.gpu_type.get_value(),
            gpu_number=x.gpu_number.get_value(),
            instance_type_status=x.instance_type_status.get_value(),
            instance_type_status_category=x.instance_type_status_category.get_value(),
            instance_name=x.instance_name.get_value(),
            instance_status=x.instance_status.get_value(),
            instance_create_time=x.instance_create_time.get_value(),
            os_name=x.os_name.get_value(),
            public_ip=[i.get_value() for i in x.public_ip],
            private_ip=x.private_ip.get_value(),
            bandwidth_in=x.bandwidth_in.get_value(),
            bandwidth_out=x.bandwidth_out.get_value(),
            node_expired_time=None if x.node_expired_time is None else x.node_expired_time.get_value(),
            auto_release_time=None if x.auto_release_time is None else x.auto_release_time.get_value(),
            key_name=x.key_name.get_value(),
            run_time=None if x.run_time is None else x.run_time.get_value(),
            k3s_version=None if x.k3s_version is None else x.k3s_version.get_value(),
            _life_time=None if x._life_time is None else x._life_time.get_value()
        )
node_info_converter = NodeInfoConverter()

class NodeCreationItemConverter(Converter):
    def to_entity(self, do: NodeCreationItemDO):
        return NodeCreationItem(
            id = NodeCreationItemID(do.id),
            node_creation_request=None if do.node_creation_request is None else node_creation_request_converter.to_entity(do.node_creation_request),
            creation_time=CreationTime(do.creation_time),
            status=NodeCreationStatus(do.status),
            details=None if do.details is None else [node_info_converter.to_entity(n) for n in do.details],
            entry_time=None if do.entry_time is None else DateTime(do.entry_time),
            exit_time=None if do.exit_time is None else DateTime(do.exit_time),
            _life_time=Number(do._life_time)
        )
    def to_do(self, x: NodeCreationItem):
        return NodeCreationItemDO(
            id=x.id.get_value(),
            node_creation_request=None if x.node_creation_request is None else node_creation_request_converter.to_do(x.node_creation_request),
            creation_time=x.creation_time.get_value().replace(microsecond=0).isoformat(),
            status=x.status.get_value(),
            details=None if x.details is None else [node_info_converter.to_do(d) for d in x.details],
            entry_time=None if x.entry_time is None else x.entry_time.get_value(),
            exit_time=None if x.exit_time is None else x.exit_time.get_value(),
            _life_time=x._life_time.get_value()
        )
node_creation_item_converter = NodeCreationItemConverter()

class ReleaseNodeInfoConverter(Converter):
    def to_entity(self, do:ReleaseNodeInfoDO):
        return ReleaseNodeInfo(
            node_name = NodeName(do.node_name),
            region_id=RegionID(do.region_id),
            instance_id=InstanceID(do.instance_id)
        )
    
    def to_do(self, x: ReleaseNodeInfo):
        return ReleaseNodeInfoDO(
            node_name = x.node_name.get_value(),
            region_id=x.region_id.get_value(),
            instance_id=x.instance_id.get_value()
        )
release_node_info_converter = ReleaseNodeInfoConverter()



class NamespaceConverter(Converter):
    def to_entity(self, do: NamespaceDO):
        return Namespace(
            name = Name(do.name),
            status = Status(do.status),
            age = K3SRunTime(do.age),
            _life_time = Number(do._life_time)
        )
    def to_do(self, x: Namespace):
        return NamespaceDO(
            name = None if x.name is None else x.name.get_value(),
            status = None if x.status is None else x.status.get_value(),
            age = None if x.age is None else x.age.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )
namespace_converter = NamespaceConverter()



class SecretConverter(Converter):
    def to_entity(self, do: SecretDO):
        return Secret(
            name = Name(do.name),
            age = K3SRunTime(do.age),
            namespace = Name(do.namespace),
            _life_time = Number(do._life_time)
        )
    def to_do(self, x: Secret):
        return SecretDO(
            name = None if x.name is None else x.name.get_value(),
            age = None if x.age is None else x.age.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )
secret_converter = SecretConverter()



class SecretUserSettingConverter(Converter):
    def to_entity(self, do: SecretUserSettingDO):
        return SecretUserSetting(
            name = Name(do.name),
            key = Key(do.key),
            value = Base64String(do.value),
            namespace = Name(do.namespace)
        )
    def to_do(self, x: SecretUserSetting):
        return SecretUserSettingDO(
            name = None if x.name is None else x.name.get_value(),
            key = None if x.key is None else x.key.get_value(),
            value = None if x.value is None else x.value.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value()
        )
secret_user_setting_converter = SecretUserSettingConverter()



class ConfigMapConverter(Converter):
    def to_entity(self, do: ConfigMapDO):
        return ConfigMap(
            name = Name(do.name),
            age = K3SRunTime(do.age),
            namespace = Name(do.namespace),
            _life_time = Number(do._life_time)
        )
    def to_do(self, x: ConfigMap):
        return ConfigMapDO(
            name = None if x.name is None else x.name.get_value(),
            age = None if x.age is None else x.age.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )
config_map_converter = ConfigMapConverter()



class ConfigMapUserSettingConverter(Converter):
    def to_entity(self, do: ConfigMapUserSettingDO):
        return ConfigMapUserSetting(
            name = Name(do.name),
            key = Key(do.key),
            value = Value(do.value),
            key_type = ConfigMapType(do.key_type),
            namespace = Name(do.namespace)
        )
    def to_do(self, x: ConfigMapUserSetting):
        return ConfigMapUserSettingDO(
            name = None if x.name is None else x.name.get_value(),
            key = None if x.key is None else x.key.get_value(),
            value = None if x.value is None else x.value.get_value(),
            key_type = None if x.key_type is None else x.key_type.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value()
        )
config_map_user_setting_converter = ConfigMapUserSettingConverter()



class DeploymentConverter(Converter):
    def to_entity(self, do: DeploymentDO):
        return Deployment(
            name = Name(do.name),
            age = K3SRunTime(do.age),
            namespace = Name(do.namespace),
            ready_info = Info(do.ready_info),
            _life_time = Number(do._life_time)
        )
    def to_do(self, x: Deployment):
        return DeploymentDO(
            name = None if x.name is None else x.name.get_value(),
            age = None if x.age is None else x.age.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            ready_info = None if x.ready_info is None else x.ready_info.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )
deployment_converter = DeploymentConverter()



class PodConverter(Converter):
    def to_entity(self, do: PodDO):
        return Pod(
            name = Name(do.name),
            node_name = None if do.node_name is None else NodeName(do.node_name),
            pod_status = PodStatus(do.pod_status),
            age = K3SRunTime(do.age),
            pod_ip = None if do.pod_ip is None else IP(do.pod_ip),
            namespace = Name(do.namespace),
            restarts = RestartNumber(do.restarts),
            readiness_info = Info(do.readiness_info),
            _life_time = Number(do._life_time)
        )
    def to_do(self, x: Pod):
        return PodDO(
            name = None if x.name is None else x.name.get_value(),
            node_name = None if x.node_name is None else x.node_name.get_value(),
            pod_status = None if x.pod_status is None else x.pod_status.get_value(),
            age = None if x.age is None else x.age.get_value(),
            pod_ip = None if x.pod_ip is None else x.pod_ip.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            restarts = None if x.restarts is None else x.restarts.get_value(),
            readiness_info = None if x.readiness_info is None else x.readiness_info.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )
pod_converter = PodConverter()



class IngressConverter(Converter):
    def to_entity(self, do: IngressDO):
        return Ingress(
            name = Name(do.name),
            host_info = Info(do.host_info),
            address_info = Info(do.address_info),
            port = Number(do.port),
            age = K3SRunTime(do.age),
            namespace = Name(do.namespace),
            _life_time = Number(do._life_time)
        )
    def to_do(self, x: Ingress):
        return IngressDO(
            name = None if x.name is None else x.name.get_value(),
            host_info = None if x.host_info is None else x.host_info.get_value(),
            address_info = None if x.address_info is None else x.address_info.get_value(),
            port = None if x.port is None else x.port.get_value(),
            age = None if x.age is None else x.age.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )
ingress_converter = IngressConverter()



class ServiceConverter(Converter):
    def to_entity(self, do: ServiceDO):
        return Service(
            name = Name(do.name),
            service_type = ServiceType(do.service_type),
            cluster_ip = IP(do.cluster_ip),
            external_ip = IP(do.external_ip),
            port_info = Info(do.port_info),
            age = K3SRunTime(do.age),
            _life_time = Number(do._life_time)
        )
    def to_do(self, x: Service):
        return ServiceDO(
            name = None if x.name is None else x.name.get_value(),
            service_type = None if x.service_type is None else x.service_type.get_value(),
            cluster_ip = None if x.cluster_ip is None else x.cluster_ip.get_value(),
            external_ip = None if x.external_ip is None else x.external_ip.get_value(),
            port_info = None if x.port_info is None else x.port_info.get_value(),
            age = None if x.age is None else x.age.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )
service_converter = ServiceConverter()



class PodContainerConverter(Converter):
    def to_entity(self, do: PodContainerDO):
        return PodContainer(
            pod_name = Name(do.pod_name),
            init_container_info = Info(do.init_container_info),
            container_info = Info(do.container_info),
            _life_time = Number(do._life_time)
        )
    def to_do(self, x: PodContainer):
        return PodContainerDO(
            pod_name = None if x.pod_name is None else x.pod_name.get_value(),
            init_container_info = None if x.init_container_info is None else x.init_container_info.get_value(),
            container_info = None if x.container_info is None else x.container_info.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )
pod_container_converter = PodContainerConverter()



class NodeMetaConverter(Converter):
    def to_entity(self, do: NodeMetaDO):
        return NodeMeta(
            name = NodeName(do.name),
            status = NodeStatus(do.status),
            run_time = K3SRunTime(do.run_time),
            k3s_version = Version(do.k3s_version),
            private_ip = IP(do.private_ip),
            label = NodeLabel(do.label)
        )
    def to_do(self, x: NodeMeta):
        return NodeMetaDO(
            name = None if x.name is None else x.name.get_value(),
            status = None if x.status is None else x.status.get_value(),
            run_time = None if x.run_time is None else x.run_time.get_value(),
            k3s_version = None if x.k3s_version is None else x.k3s_version.get_value(),
            private_ip = None if x.private_ip is None else x.private_ip.get_value(),
            label = None if x.label is None else x.label.get_value()
        )
node_meta_converter = NodeMetaConverter()

class KeyToPathConverter(Converter):
    def to_entity(self, do: KeyToPathDO):
        return KeyToPath(
            key = Key(do.key),
            path = Path(do.path),
            mode = PathMode(do.mode)
        )
    def to_do(self, x: KeyToPath):
        return KeyToPathDO(
            key = None if x.key is None else x.key.get_value(),
            path = None if x.path is None else x.path.get_value(),
            mode = None if x.mode is None else x.mode.get_value()
        )
key_to_path_converter = KeyToPathConverter()

class EnvVarSourceConverter(Converter):
    def to_entity(self, do: EnvVarSourceDO):
        return EnvVarSource(
            env_var_source_type = EnvVarSourceType(do.env_var_source_type),
            key = Key(do.key),
            name = Name(do.name),
            optional = Bool(do.optional)
        )
    def to_do(self, x: EnvVarSource):
        return EnvVarSourceDO(
            env_var_source_type = None if x.env_var_source_type is None else x.env_var_source_type.get_value(),
            key = None if x.key is None else x.key.get_value(),
            name = None if x.name is None else x.name.get_value(),
            optional = None if x.optional is None else x.optional.get_value()
        )
env_var_source_converter = EnvVarSourceConverter()

class EnvVarConverter(Converter):
    def to_entity(self, do: EnvVarDO):
        return EnvVar(
            name = Name(do.name),
            value = Value(do.value),
            value_from = None if do.value_from is None else env_var_source_converter.to_entity(do.value_from)
        )
    def to_do(self, x: EnvVar):
        return EnvVarDO(
            name = None if x.name is None else x.name.get_value(),
            value = None if x.value is None else x.value.get_value(),
            value_from = None if x.value_from is None else env_var_source_converter.to_do(x.value_from)
        )
env_var_converter = EnvVarConverter()

class VolumeSourceConverter(Converter):
    def to_entity(self, do: VolumeSourceDO):
        return VolumeSource(
            name = Name(do.name),
            volume_type = VolumeType(do.volume_type),
            optional = Bool(do.optional),
            default_mode = PathMode(do.default_mode),
            items = None if do.items is None else [key_to_path_converter.to_entity(i) for i in do.items]
        )
    def to_do(self, x: VolumeSource):
        return VolumeSourceDO(
            name = None if x.name is None else x.name.get_value(),
            volume_type = None if x.volume_type is None else x.volume_type.get_value(),
            optional = None if x.optional is None else x.optional.get_value(),
            default_mode = None if x.default_mode is None else x.default_mode.get_value(),
            items = None if x.items is None else [key_to_path_converter.to_do(i) for i in x.items]
        )
volume_source_converter = VolumeSourceConverter()

class PersistentVolumeClaimVolumeSourceConverter(Converter):
    def to_entity(self, do: PersistentVolumeClaimeVolumeSourceDO):
        return PersistentVolumeClaimVolumeSource(
            claim_name = Name(do.claim_name),
            read_only = None if do.read_only is None else ReadOnly(do.read_only)
        )

    def to_do(self, x: PersistentVolumeClaimVolumeSource):
        return PersistentVolumeClaimeVolumeSourceDO(
            claim_name = x.claim_name.get_value(),
            read_only = None if x.read_only is None else x.read_only.get_value()
        )
persistent_volume_claim_volume_source_converter = PersistentVolumeClaimVolumeSourceConverter()

class VolumeSettingConverter(Converter):
    def to_entity(self, do: VolumeSettingDO):
        return VolumeSetting(
            volume_name = VolumeName(do.volume_name),
            empty_dir = Bool(do.empty_dir),
            config_map= None if do.config_map is None else volume_source_converter.to_entity(do.config_map),
            secret = None if do.secret is None else volume_source_converter.to_entity(do.secret),
            persistent_volume_claim=None if do.persistent_volume_claim is None else persistent_volume_claim_volume_source_converter.to_entity(do.persistent_volume_claim)
        )
    def to_do(self, x: VolumeSetting):
        return VolumeSettingDO(
            volume_name = None if x.volume_name is None else x.volume_name.get_value(),
            empty_dir = None if x.empty_dir is None else x.empty_dir.get_value(),
            config_map = None if x.config_map is None else volume_source_converter.to_do(x.config_map),
            secret = None if x.secret is None else volume_source_converter.to_do(x.secret),
            persistent_volume_claim = None if x.persistent_volume_claim is None else persistent_volume_claim_volume_source_converter.to_do(x.persistent_volume_claim)
        )
volume_setting_converter = VolumeSettingConverter()

class VolumeMountConverter(Converter):
    def to_entity(self, do: VolumeMountDO):
        return VolumeMount(
            name = Name(do.name),
            mount_path = Path(do.mount_path),
            read_only = Bool(do.read_only),
            sub_path = Path(do.sub_path)
        )
    def to_do(self, x: VolumeMount):
        return VolumeMountDO(
            name = None if x.name is None else x.name.get_value(),
            mount_path = None if x.mount_path is None else x.mount_path.get_value(),
            read_only = None if x.read_only is None else x.read_only.get_value(),
            sub_path = None if x.sub_path is None else x.sub_path.get_value()
        )
volume_mount_converter = VolumeMountConverter()

class HTTPGetActionConverter(Converter):
    def to_entity(self, do: HTTPGetActionDO):
        return HTTPGetAction(
            port = Port(do.port),
            host = IP(do.host),
            path = Path(do.path),
            http_headers = [HTTPHeader(m) for m in do.http_headers],
            scheme = NetworkScheme(do.scheme)
        )
    def to_do(self, x: HTTPGetAction):
        return HTTPGetActionDO(
            port = None if x.port is None else x.port.get_value(),
            host = None if x.host is None else x.host.get_value(),
            path = None if x.path is None else x.path.get_value(),
            http_headers = None if x.http_headers is None else [m.get_value() for m in x.http_headers],
            scheme = None if x.scheme is None else x.scheme.get_value()
        )
http_get_action_converter = HTTPGetActionConverter()

class GRPCActionConverter(Converter):
    def to_entity(self, do: GRPCActionDO):
        return GRPCAction(
            port = Port(do.port),
            service = Name(do.service)
        )
    def to_do(self, x: GRPCAction):
        return GRPCActionDO(
            port = None if x.port is None else x.port.get_value(),
            service = None if x.service is None else x.service.get_value()
        )
grpc_action_converter = GRPCActionConverter()

class TCPSocketActionConverter(Converter):
    def to_entity(self, do: TCPSocketActionDO):
        return TCPSocketAction(
            port = Port(do.port),
            host = IP(do.host)
        )
    def to_do(self, x: TCPSocketAction):
        return TCPSocketActionDO(
            port = None if x.port is None else x.port.get_value(),
            host = None if x.host is None else x.host.get_value()
        )
tcp_socket_action_converter = TCPSocketActionConverter()

class ContainerPortConverter(Converter):
    def to_entity(self, do: ContainerPortDO):
        return ContainerPort(
            port = Port(do.port),
            name = Name(do.name),
            protocol = Protocol(do.protocol),
            host_ip = IP(do.host_ip),
            host_port = Port(do.host_port)
        )
    def to_do(self, x: ContainerPort):
        return ContainerPortDO(
            port = None if x.port is None else x.port.get_value(),
            name = None if x.name is None else x.name.get_value(),
            protocol = None if x.protocol is None else x.protocol.get_value(),
            host_ip = None if x.host_ip is None else x.host_ip.get_value(),
            host_port = None if x.host_port is None else x.host_port.get_value()
        )
container_port_converter = ContainerPortConverter()

class ProbeConverter(Converter):
    def to_entity(self, do: ProbeDO):
        return Probe(
            initial_delay_seconds = Number(do.initial_delay_seconds),
            period_seconds = Number(do.period_seconds),
            success_threshold = Number(do.success_threshold),
            timeout_seconds = Number(do.timeout_seconds),
            command = [ContainerCommand(m) for m in do.command],
            failure_threshold = Number(do.failure_threshold),
            grpc = None if do.grpc is None else grpc_action_converter.to_entity(do.grpc),
            http_get = None if do.http_get is None else http_get_action_converter.to_entity(do.http_get),
            tcp_socket = None if do.tcp_socket is None else tcp_socket_action_converter.to_entity(do.tcp_socket)
        )
    def to_do(self, x: Probe):
        return ProbeDO(
            initial_delay_seconds = None if x.initial_delay_seconds is None else x.initial_delay_seconds.get_value(),
            period_seconds = None if x.period_seconds is None else x.period_seconds.get_value(),
            success_threshold = None if x.success_threshold is None else x.success_threshold.get_value(),
            timeout_seconds = None if x.timeout_seconds is None else x.timeout_seconds.get_value(),
            command = None if x.command is None else [m.get_value() for m in x.command],
            failure_threshold = None if x.failure_threshold is None else x.failure_threshold.get_value(),
            grpc = None if x.grpc is None else grpc_action_converter.to_do(x.grpc),
            http_get = None if x.http_get is None else http_get_action_converter.to_do(x.http_get),
            tcp_socket = None if x.tcp_socket is None else tcp_socket_action_converter.to_do(x.tcp_socket)
        )
probe_converter = ProbeConverter()

class LabelSelectorRequirementConverter(Converter):
    def to_entity(self, do: LabelSelectorRequirementDO):
        return LabelSelectorRequirement(
            key = Key(do.key),
            operator = LabelSelectorOperator(do.operator),
            values = [Value(m) for m in do.values]
        )
    def to_do(self, x: LabelSelectorRequirement):
        return LabelSelectorRequirementDO(
            key = None if x.key is None else x.key.get_value(),
            operator = None if x.operator is None else x.operator.get_value(),
            values = None if x.values is None else [m.get_value() for m in x.values]
        )
label_selector_requirement_converter = LabelSelectorRequirementConverter()

class LabelSelectorConverter(Converter):
    def to_entity(self, do: LabelSelectorDO):
        return LabelSelector(
            match_labels = MatchLabels(do.match_labels),
            match_expressions= None if do.match_expressions is None else [label_selector_requirement_converter.to_entity(i) for i in do.match_expressions]
        )
    def to_do(self, x: LabelSelector):
        return LabelSelectorDO(
            match_labels = None if x.match_labels is None else x.match_labels.get_value(),
            match_expressions = None if x.match_expressions is None else [label_selector_requirement_converter.to_do(i) for i in x.match_expressions]
        )
label_selector_converter =LabelSelectorConverter()

class SecurityContextConverter(Converter):
    def to_entity(self, do: SecurityContextDO):
        return SecurityContext(
            privileged = Bool(do.privileged),
            run_as_user = Number(do.run_as_user),
            run_as_non_root = Bool(do.run_as_non_root)
        )
    def to_do(self, x: SecurityContext):
        return SecurityContextDO(
            privileged = None if x.privileged is None else x.privileged.get_value(),
            run_as_user = None if x.run_as_user is None else x.run_as_user.get_value(),
            run_as_non_root = None if x.run_as_non_root is None else x.run_as_non_root.get_value()
        )
security_context_converter = SecurityContextConverter()

class ContainerSettingConverter(Converter):
    def to_entity(self, do: ContainerSettingDO):
        return ContainerSetting(
            container_name=Name(do.container_name),
            container_image=DockerImageName(do.container_image),
            env_vars=None if do.env_vars is None else [env_var_converter.to_entity(m) for m in do.env_vars],
            command=None if do.command is None else ContainerCommand(do.command),
            args=None if do.args is None else ContainerArgs(do.args),
            image_pull_policy=None if do.image_pull_policy is None else ImagePullPolicy(do.image_pull_policy),
            working_dir=None if do.working_dir is None else Path(do.working_dir),
            volume_mount=None if do.volume_mount is None else [volume_mount_converter.to_entity(m) for m in do.volume_mount],
            security_context=None if do.security_context is None else security_context_converter.to_entity(do.security_context),
            limits=None if do.limits is None else PodResourceDict(do.limits),
            requests=None if do.requests is None else PodResourceDict(do.requests),
            readiness_probe=None if do.readiness_probe is None else probe_converter.to_entity(do.readiness_probe),
            liveness_probe=None if do.liveness_probe is None else probe_converter.to_entity(do.liveness_probe),
            ports=None if do.ports is None else [container_port_converter.to_entity(m) for m in do.ports]

        )
    def to_do(self, x: ContainerSetting):
        return ContainerSettingDO(
            container_name = x.container_name.get_value(),
            container_image = x.container_image.get_value(),
            env_vars = None if x.env_vars is None else [env_var_converter.to_do(i) for i in x.env_vars],
            command = None if x.command is None else x.command.get_value(),
            args = None if x.args is None else x.args.get_value(),
            image_pull_policy = None if x.image_pull_policy is None else x.image_pull_policy.get_value(),
            working_dir = None if x.working_dir is None else x.working_dir.get_value(),
            volume_mount = None if x.volume_mount is None else [volume_mount_converter.to_do(i) for i in x.volume_mount],
            security_context = None if x.security_context is None else security_context_converter.to_do(x.security_context),
            limits = None if x.limits is None else x.limits.get_value(),
            requests = None if x.requests is None else x.requests.get_value(),
            readiness_probe = None if x.readiness_probe is None else probe_converter.to_do(x.readiness_probe),
            liveness_probe = None if x.liveness_probe is None else probe_converter.to_do(x.liveness_probe),
            ports = None if x.ports is None else [container_port_converter.to_do(i) for i in x.ports]
        )
container_setting_converter = ContainerSettingConverter()




class DeploymentSettingConverter(Converter):
    def to_entity(self, do: DeploymentSettingDO):
        return DeploymentSetting(
            deployment_name=Name(do.deployment_name),
            namespace_name=Name(do.namespace_name),
            labels=LabelDict(do.labels),
            containers=[container_setting_converter.to_entity(c) for c in do.containers],
            init_containers=None if do.init_containers is None else [container_setting_converter.to_entity(i) for i in do.init_containers],
            node_name = None if do.node_name is None else Name(do.node_name),
            node_selector=None if do.node_selector is None else NodeSelectorDict(do.node_selector),
            replicas=None if do.replicas is None else Number(do.replicas),
            restart_policy=None if do.restart_policy is None else RestartPolicy(do.restart_policy),
            volumes = None if do.volumes is None else [volume_setting_converter.to_entity(i) for i in do.volumes],
            selector = label_selector_converter.to_entity(do.selector),
            dns_policy = None if do.dns_policy is None else DNSPolicy(do.dns_policy),
            service_account_name = None if do.service_account_name is None else ServiceAccountName(do.service_account_name)
        )
    def to_do(self, x: DeploymentSetting):
        return DeploymentSettingDO(
            deployment_name=x.deployment_name.get_value(),
            namespace_name = x.namespace_name.get_value(),
            labels=x.labels.get_value(),
            containers=[container_setting_converter.to_do(m) for m in x.containers],
            init_containers=None if x.init_containers is None else [container_setting_converter.to_do(m) for m in x.init_containers],
            node_name=None if x.node_name is None else x.node_name.get_value(),
            node_selector=None if x.node_selector is None else x.node_selector.get_value(),
            replicas=None if x.replicas is None else x.replicas.get_value(),
            restart_policy=None if x.restart_policy is None else x.restart_policy.get_value(),
            volumes=None if x.volumes is None else [volume_setting_converter.to_do(m) for m in x.volumes],
            selector = label_selector_converter.to_do(x.selector),
            dns_policy=None if x.dns_policy is None else x.dns_policy.get_value(),
            service_account_name=None if x.service_account_name is None else ServiceAccountName(x.service_account_name)
        )
deployment_setting_converter = DeploymentSettingConverter()

class JobSettingConverter(Converter):
    def to_entity(self, do: JobSettingDO):
        return JobSetting(
            job_name = Name(do.job_name),
            namespace_name=Name(do.namespace_name),
            labels=LabelDict(do.labels),
            containers=[container_setting_converter.to_entity(m) for m in do.containers],
            init_containers=None if do.init_containers is None else [container_setting_converter.to_entity(m) for m in do.init_containers],
            parallelism=None if do.parallelism is None else Number(do.parallelism) ,
            ttl_seconds_after_finished=None if do.ttl_seconds_after_finished is None else Number(do.ttl_seconds_after_finished),
            restart_policy=None if do.restart_policy is None else RestartPolicy(do.restart_policy),
            backoff_limit=None if do.backoff_limit is None else Number(do.backoff_limit),
            node_name=None if do.node_name is None else Name(do.node_name),
            node_selector=None if do.node_selector is None else NodeSelectorDict(do.node_selector),
            volumes=None if do.volumes is None else [volume_setting_converter.to_entity(m) for m in do.volumes],
            selector=None if do.selector is None else [label_selector_converter.to_entity(m) for m in do.selector],
            dns_policy=None if do.dns_policy is None else DNSPolicy(do.dns_policy),
            service_account_name=None if do.service_account_name is None else ServiceAccountName(do.service_account_name)

        )
    def to_do(self, x: JobSetting):
        return JobSettingDO(
            job_name = x.job_name.get_value(),
            namespace_name = x.namespace_name.get_value(),
            labels = x.labels.get_value(),
            containers = [container_setting_converter.to_do(c) for c in x.containers],
            init_containers = None if x.init_containers is None else [container_setting_converter.to_do(i) for i in x.init_containers],
            parallelism = None if x.parallelism is None else x.parallelism.get_value(),
            ttl_seconds_after_finished = None if x.ttl_seconds_after_finished is None else x.ttl_seconds_after_finished.get_value(),
            restart_policy = None if x.restart_policy is None else x.restart_policy.get_value(),
            backoff_limit=None if x.backoff_limit is None else x.backoff_limit.get_value(),
            node_name = None if x.node_name is None else x.node_name.get_value(),
            node_selector = None if x.node_selector is None else x.node_selector.get_value(),
            volumes = None if x.volumes is None else [volume_setting_converter.to_do(i) for i in x.volumes],
            selector = None if x.selector is None else [label_selector_converter.to_do(i) for i in x.selector],
            dns_policy = None if x.dns_policy is None else x.dns_policy.get_value(),
            service_account_name = None if x.service_account_name is None else x.service_account_name.get_value()
        )
job_setting_converter = JobSettingConverter()

class JobConverter(Converter):
    def to_entity(self, do: JobDO):
        return Job(
            name = Name(do.name),
            age = K3SRunTime(do.age),
            namespace = Name(do.namespace),
            status = JobStatus(do.status),
            parallelism = Number(do.parallelism),
            _life_time = Number(do._life_time)
        )
    def to_do(self, x: Job):
        return JobDO(
            name = None if x.name is None else x.name.get_value(),
            age = None if x.age is None else x.age.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            status = None if x.status is None else x.status.get_value(),
            parallelism = None if x.parallelism is None else x.parallelism.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )
job_converter = JobConverter()

class PodLogSettingConverter(Converter):
    def to_entity(self, do: PodLogSettingDO):
        return PodLogSetting(
            namespace_name = Name(do.namespace_name),
            pod_name = Name(do.pod_name),
            container_name = None if do.container_name is None else Name(do.container_name),
            tail_lines = Integer(do.tail_lines)
        )
    def to_do(self, x: PodLogSetting):
        return PodLogSettingDO(
            namespace_name = None if x.namespace_name is None else x.namespace_name.get_value(),
            pod_name = None if x.pod_name is None else x.pod_name.get_value(),
            container_name = None if x.container_name is None else x.container_name.get_value(),
            tail_lines = None if x.tail_lines is None else x.tail_lines.get_value()
        )
pod_log_setting_converter = PodLogSettingConverter()

class StorageClassConverter(Converter):
    def to_entity(self, do: StorageClassDO):
        return StorageClass(
            name = Name(do.name),
            provisioner = Provisioner(do.provisioner),
            reclaim_policy = ReclaimPolicy(do.reclaim_policy),
            volume_binding_mode = VolumeBindingMode(do.volume_binding_mode),
            namespace_name = Name(do.namespace_name)
        )
    def to_do(self, x: StorageClass):
        return StorageClassDO(
            name = None if x.name is None else x.name.get_value(),
            provisioner = None if x.provisioner is None else x.provisioner.get_value(),
            reclaim_policy = None if x.reclaim_policy is None else x.reclaim_policy.get_value(),
            volume_binding_mode = None if x.volume_binding_mode is None else x.volume_binding_mode.get_value(),
            namespace_name = None if x.namespace_name is None else x.namespace_name.get_value()
        )
storage_class_converter = StorageClassConverter()

class NFSVolumeSourceConverter(Converter):
    def to_entity(self, do: NFSVolumeSourceDO):
        return NFSVolumeSource(
            path = Path(do.path),
            server = Server(do.server),
            read_only = None if do.read_only is None else ReadOnly(do.read_only)
        )
    def to_do(self, x: NFSVolumeSource):
        return NFSVolumeSourceDO(
            path = None if x.path is None else x.path.get_value(),
            server = None if x.server is None else x.server.get_value(),
            read_only = None if x.read_only is None else x.read_only.get_value()
        )
nfs_volume_source_converter = NFSVolumeSourceConverter()

class LocalVolumeSourceConverter(Converter):
    def to_entity(self, do: LocalVolumeSourceDO):
        return LocalVolumeSource(
            path = Path(do.path),
            fs_type = None if do.fs_type is None else FSType(do.fs_type)
        )
    def to_do(self, x: LocalVolumeSource):
        return LocalVolumeSourceDO(
            path = None if x.path is None else x.path.get_value(),
            fs_type = None if x.fs_type is None else x.fs_type.get_value()
        )
local_volume_source_converter = LocalVolumeSourceConverter()

class NodeSelectorRequirementConverter(Converter):
    def to_entity(self, do: NodeSelectorRequirementDO):
        return NodeSelectorRequirement(
            key = Key(do.key),
            operator = Operator(do.operator),
            values = [Value(m) for m in do.values]
        )
    def to_do(self, x: NodeSelectorRequirement):
        return NodeSelectorRequirementDO(
            key = None if x.key is None else x.key.get_value(),
            operator = None if x.operator is None else x.operator.get_value(),
            values = None if x.values is None else [m.get_value() for m in x.values]
        )
node_selector_requirement_converter = NodeSelectorRequirementConverter()

class NodeAffinityConverter(Converter):
    def to_entity(self, do: NodeAffinityDO):
        return NodeAffinity(
            match_expressions = None if do.match_expressions is None else [node_selector_requirement_converter.to_entity(m) for m in do.match_expressions],
            match_fields = None if do.match_fields is None else [node_selector_requirement_converter.to_entity(m) for m in do.match_fields]
        )
    def to_do(self, x: NodeAffinity):
        return NodeAffinityDO(
            match_expressions = None if x.match_expressions is None else [node_selector_requirement_converter.to_do(m) for m in x.match_expressions],
            match_fields = None if x.match_fields is None else [node_selector_requirement_converter.to_do(m) for m in x.match_fields]
        )
node_affinity_converter = NodeAffinityConverter()
class PersistentVolumeConverter(Converter):
    def to_entity(self, do: PersistentVolumeDO):
        return PersistentVolume(
            name = Name(do.name),
            namespace = Name(do.namespace),
            persistent_volume_claim_name = None if do.persistent_volume_claim_name is None else Name(do.persistent_volume_claim_name),
            storage_class_name = None if do.storage_class_name is None else StorageClassName(do.storage_class_name),
            capacity = None if do.capacity is None else Capacity(do.capacity),
            access_modes = None if do.access_modes is None else [AccessMode(m) for m in do.access_modes],
            persistent_volume_reclaim_policy = None if do.persistent_volume_reclaim_policy is None else PersistentVolumeReclaimPolicy(do.persistent_volume_reclaim_policy),
            nfs = None if do.nfs is None else nfs_volume_source_converter.to_entity(do.nfs),
            local = None if do.local is None else local_volume_source_converter.to_entity(do.local),
            node_affinity = None if do.node_affinity is None else [node_affinity_converter.to_entity(m) for m in do.node_affinity]
        )
    def to_do(self, x: PersistentVolume):
        return PersistentVolumeDO(
            name = None if x.name is None else x.name.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            persistent_volume_claim_name = None if x.persistent_volume_claim_name is None else x.persistent_volume_claim_name.get_value(),
            storage_class_name = None if x.storage_class_name is None else x.storage_class_name.get_value(),
            capacity = None if x.capacity is None else x.capacity.get_value(),
            access_modes = None if x.access_modes is None else [m.get_value() for m in x.access_modes],
            persistent_volume_reclaim_policy = None if x.persistent_volume_reclaim_policy is None else x.persistent_volume_reclaim_policy.get_value(),
            nfs = None if x.nfs is None else nfs_volume_source_converter.to_do(x.nfs),
            local = None if x.local is None else local_volume_source_converter.to_do(x.local),
            node_affinity = None if x.node_affinity is None else [node_affinity_converter.to_do(m) for m in x.node_affinity]
        )
persistent_volume_converter = PersistentVolumeConverter()

class PersistentVolumeClaimConverter(Converter):
    def to_entity(self, do: PersistentVolumeClaimDO):
        return PersistentVolumeClaim(
            name = Name(do.name),
            namespace = Name(do.namespace),
            labels = None if do.labels is None else Label(do.labels),
            access_modes = None if do.access_modes is None else [AcceessMode(m) for m in do.access_modes],
            storage_class_name = None if do.storage_class_name is None else StorageClassName(do.storage_class_name),
            limits = None if do.limits is None else ResourceDict(do.limits),
            requests = None if do.requests is None else ResourceDict(do.requests)
        )
    def to_do(self, x: PersistentVolumeClaim):
        return PersistentVolumeClaimDO(
            name = None if x.name is None else x.name.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            labels = None if x.labels is None else x.labels.get_value(),
            access_modes = None if x.access_modes is None else [m.get_value() for m in x.access_modes],
            storage_class_name = None if x.storage_class_name is None else x.storage_class_name.get_value(),
            limits = None if x.limits is None else x.limits.get_value(),
            requests = None if x.requests is None else x.requests.get_value()
        )
persistent_volume_claim_converter = PersistentVolumeClaimConverter()

class DatapipeServerInfoConverter(Converter):
    def to_entity(self, do: DatapipeServerInfoDO):
        return DatapipeServerInfo(
            id = AccountID(do.id),
            secret=AccountSecret(do.secret),
            endpoint=ServerEndpoint(do.endpoint)
        )
    
    def to_do(self, x:DatapipeServerInfo):
        return DatapipeServerInfoDO(
            id = x.id.get_value(),
            secret = x.secret.get_value(),
            endpoint = x.endpoint.get_value()
        )
datapipe_server_info_converter = DatapipeServerInfoConverter()

class DatapipeHostConverter(Converter):
    def to_entity(self, do: DatapipeHostDO):
        return DatapipeHost(
            ip=IP(do.ip),
            hostname=None if do.hostname is None else Name(do.hostname),
            port=Number(do.port),
            username=Name(do.username)
        )
    def to_do(self, x: DatapipeHost):
        return DatapipeHostDO(
            ip=x.ip.get_value(),
            hostname=None if x.hostname is None else x.hostname.get_value(),
            port=x.port.get_value(),
            username=x.username.get_value()
        )
    pass
datapipe_host_converter = DatapipeHostConverter()

class DatapipeDataInfoConverter(Converter):
    def to_entity(self, do: DatapipeDataInfoDO):
        return DatapipeDataInfo(
            bucket = DataBucket(do.bucket),
            remote_path=DatapipePath(do.remote_path),
            local_path=DatapipePath(do.local_path),
            timeout = Number(do.timeout)
        )
    def to_do(self, x: DatapipeDataInfo):
        return DatapipeDataInfoDO(
            bucket = x.bucket.get_value(),
            remote_path=x.remote_path.get_value(),
            local_path=x.local_path.get_value(),
            timeout = x.timeout.get_value()
        )
datapipe_data_info_converter = DatapipeDataInfoConverter()

class DatapipeResponseConverter(Converter):
    def to_entity(self, do: DatapipeResponseDO):
        return DatapipeResponse(
            status=CommandResponseStatus(do.status),
            ip=IP(do.ip),
            message=Text(do.message),
            exception=None if do.exception is None else Text(do.exception),
            stdout=None if do.stdout is None else Text(do.stdout),
            cmd=None if do.cmd is None else Text(do.cmd),
            start_time=None if do.start_time is None else DateTime(do.start_time),
            end_time = None if do.end_time is None else DateTime(do.end_time),
            delta_time = None if do.delta_time is None else DeltaTime(do.delta_time),
            stderr=None if do.stderr is None else Text(do.stderr),
            entry_time=None if do.entry_time is None else DateTime(do.entry_time),
            exit_time=None if do.exit_time is None else DateTime(do.exit_time)
        )
    def to_do(self, x: DatapipeResponse):
        return DatapipeResponseDO(
            status=x.status.get_value(),
            ip=x.ip.get_value(),
            message=x.message.get_value(),
            exception=None if x.exception is None else x.exception.get_value(),
            stdout=None if x.stdout is None else x.stdout.get_value(),
            cmd=None if x.cmd is None else x.cmd.get_value(),
            start_time=None if x.start_time is None else x.start_time.get_value(),
            end_time=None if x.end_time is None else x.end_time.get_value(),
            delta_time=None if x.delta_time is None else x.delta_time.get_value(),
            stderr=None if x.stderr is None else x.stderr.get_value(),
            entry_time=None if x.entry_time is None else x.entry_time.get_value(),
            exit_time=None if x.exit_time is None else x.exit_time.get_value()
        )
datapipe_response_converter = DatapipeResponseConverter()