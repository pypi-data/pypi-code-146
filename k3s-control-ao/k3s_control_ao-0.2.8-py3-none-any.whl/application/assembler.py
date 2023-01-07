from ddd_objects.application.assembler import Assembler
from vpc_control_ao.application.assembler import (
    condition_assembler,
    instance_info_assembler
)
from vpc_control_ao.domain.value_obj import (
    DeltaTime,
    Text,
    CommandResponseStatus
)
from ..domain.entity import (
    DeploymentSetting,
    DatapipeDataInfo,
    DatapipeResponse,
    DatapipeHost,
    DatapipeServerInfo,
    ReleaseNodeInfo,
    LocalVolumeSource,
    NFSVolumeSource,
    Namespace,
    NodeAffinity,
    NodeCreationItem,
    NodeCreationRequest,
    NodeSelectorRequirement,
    PersistentVolume,
    PersistentVolumeClaim,
    PersistentVolumeClaimVolumeSource,
    SecurityContext,
    EnvVarSource,
    HTTPGetAction,
    Pod,
    Service,
    Deployment,
    LabelSelector,
    SecretUserSetting,
    KeyToPath,
    NodeUserSetting,
    ConfigMapUserSetting,
    StorageClass,
    VolumeMount,
    ContainerSetting,
    Ingress,
    NodeInfo,
    PodLogSetting,
    Job,
    NodeMeta,
    VolumeSetting,
    JobSetting,
    GRPCAction,
    TCPSocketAction,
    LabelSelectorRequirement,
    VolumeSource,
    ContainerPort,
    ConfigMap,
    PodContainer,
    Secret,
    Probe,
    EnvVar,
)
from ..domain.value_obj import (
    AccountID,
    AccountSecret,
    ServerEndpoint,
    DatapipePath,
    DataBucket,
    AcceessMode,
    AccessMode,
    Capacity,
    ConfigMapType,
    CreationTime,
    FSType,
    Label,
    NodeAmount,
    NodeCreationItemID,
    NodeCreationStatus,
    NodeLabel,
    NodeName,
    DNSPolicy,
    Operator,
    PersistentVolumeReclaimPolicy,
    Provisioner,
    ReadOnly,
    ReclaimPolicy,
    ResourceDict,
    Server,
    ServiceAccountName,
    StorageClassName,
    VolumeBindingMode,
    ZoneID,
    DockerImageName,
    NodeType,
    Base64String,
    NetworkScheme,
    SecurityGroupID,
    ContainerCommand,
    Number,
    PayType,
    Status,
    InstanceTypeStatusCategory,
    NodeStatus,
    Path,
    ImagePullPolicy,
    Integer,
    RestartNumber,
    ImageID,
    GPUType,
    K3SRunTime,
    InstanceTypeStatus,
    Key,
    InstanceID,
    LabelSelectorOperator,
    PathMode,
    ContainerArgs,
    RestartPolicy,
    InternetPayType,
    Bool,
    PodResourceDict,
    Size,
    RegionID,
    Value,
    InstanceType,
    LabelDict,
    Info,
    Protocol,
    IP,
    ID,
    Name,
    PodStatus,
    Token,
    VolumeName,
    Version,
    EnvVarSourceType,
    JobStatus,
    BandWidth,
    ServiceType,
    Type,
    DateTime,
    VolumeType,
    Hostname,
    MatchLabels,
    Port,
    HTTPHeader,
    Price,
    NodeSelectorDict,
)
from .dto import (
    DeploymentSettingDTO,
    DatapipeHostDTO,
    DatapipeResponseDTO,
    DatapipeDataInfoDTO,
    DatapipeServerInfoDTO,
    ReleaseNodeInfoDTO,
    NodeCreationItemDTO,
    NodeCreationRequestDTO,
    LocalVolumeSourceDTO,
    NFSVolumeSourceDTO,
    NodeAffinityDTO,
    NodeSelectorRequirementDTO,
    PersistentVolumeClaimDTO,
    PersistentVolumeClaimeVolumeSourceDTO,
    PersistentVolumeDTO,
    SecurityContextDTO,
    NamespaceDTO,
    NodeInfoDTO,
    SecretUserSettingDTO,
    StorageClassDTO,
    VolumeMountDTO,
    VolumeSourceDTO,
    NodeUserSettingDTO,
    ServiceDTO,
    IngressDTO,
    KeyToPathDTO,
    ContainerSettingDTO,
    DeploymentDTO,
    SecretDTO,
    ConfigMapUserSettingDTO,
    LabelSelectorDTO,
    ContainerPortDTO,
    JobSettingDTO,
    NodeMetaDTO,
    EnvVarDTO,
    HTTPGetActionDTO,
    GRPCActionDTO,
    TCPSocketActionDTO,
    ProbeDTO,
    PodDTO,
    VolumeSettingDTO,
    ConfigMapDTO,
    PodContainerDTO,
    EnvVarSourceDTO,
    PodLogSettingDTO,
    JobDTO,
    LabelSelectorRequirementDTO
)

class NodeUserSettingAssembler(Assembler):
    def to_entity(self, dto: NodeUserSettingDTO):
        return NodeUserSetting(
            name = NodeName(dto.name),
            k3s_token = Token(dto.k3s_token),
            region_id = RegionID(dto.region_id),
            disk_size = Size(dto.disk_size),
            bandwidth_in = BandWidth(dto.bandwidth_in),
            bandwidth_out = BandWidth(dto.bandwidth_out),
            image_id = ImageID(dto.image_id),
            node_type = NodeType(dto.node_type),
            postfix = Bool(dto.postfix),
            diff_instance_type = Bool(dto.diff_instance_type),
            random_password = Bool(dto.random_password),
            internet_pay_type = Type(dto.internet_pay_type),
            master_ip = IP(dto.master_ip),
            inner_connection = Bool(dto.inner_connection),
            amount = NodeAmount(dto.amount)
        )
    def to_dto(self, x: NodeUserSetting):
        return NodeUserSettingDTO(
            name = None if x.name is None else x.name.get_value(),
            k3s_token = None if x.k3s_token is None else x.k3s_token.get_value(),
            region_id = None if x.region_id is None else x.region_id.get_value(),
            disk_size = None if x.disk_size is None else x.disk_size.get_value(),
            bandwidth_in = None if x.bandwidth_in is None else x.bandwidth_in.get_value(),
            bandwidth_out = None if x.bandwidth_out is None else x.bandwidth_out.get_value(),
            image_id = None if x.image_id is None else x.image_id.get_value(),
            node_type = None if x.node_type is None else x.node_type.get_value(),
            postfix = None if x.postfix is None else x.postfix.get_value(),
            diff_instance_type = None if x.diff_instance_type is None else x.diff_instance_type.get_value(),
            random_password = None if x.random_password is None else x.random_password.get_value(),
            internet_pay_type = None if x.internet_pay_type is None else x.internet_pay_type.get_value(),
            master_ip = None if x.master_ip is None else x.master_ip.get_value(),
            inner_connection = None if x.inner_connection is None else x.inner_connection.get_value(),
            amount = None if x.amount is None else x.amount.get_value()
        )
node_user_setting_assembler = NodeUserSettingAssembler()

class NodeInfoAssembler(Assembler):
    def to_entity(self, dto: NodeInfoDTO):
        return NodeInfo(
            node_name = NodeName(dto.node_name),
            node_type = NodeType(dto.node_type),
            node_status = NodeStatus(dto.node_status),
            instance_id = InstanceID(dto.instance_id),
            instance_type = InstanceType(dto.instance_type),
            hostname = Hostname(dto.hostname),
            price = Price(dto.price),
            image_id = ImageID(dto.image_id),
            region_id = RegionID(dto.region_id),
            zone_id = ZoneID(dto.zone_id),
            internet_pay_type = InternetPayType(dto.internet_pay_type),
            pay_type = PayType(dto.pay_type),
            security_group_id = [SecurityGroupID(m) for m in dto.security_group_id],
            node_label = NodeLabel(dto.node_label),
            cpu_number = None if dto.cpu_number is None else Number(dto.cpu_number),
            memory_size = None if dto.memory_size is None else Size(dto.memory_size),
            gpu_type = None if dto.gpu_type is None else GPUType(dto.gpu_type),
            gpu_number = None if dto.gpu_number is None else Number(dto.gpu_number),
            instance_type_status = None if dto.instance_type_status is None else InstanceTypeStatus(dto.instance_type_status),
            instance_type_status_category = None if dto.instance_type_status_category is None else InstanceTypeStatusCategory(dto.instance_type_status_category),
            instance_name = Name(dto.instance_name),
            instance_status = Status(dto.instance_status),
            instance_create_time = DateTime(dto.instance_create_time),
            os_name = Name(dto.os_name),
            public_ip = [IP(m) for m in dto.public_ip],
            private_ip = IP(dto.private_ip),
            bandwidth_in = BandWidth(dto.bandwidth_in),
            bandwidth_out = BandWidth(dto.bandwidth_out),
            node_expired_time = None if dto.node_expired_time is None else DateTime(dto.node_expired_time),
            auto_release_time = None if dto.auto_release_time is None else DateTime(dto.auto_release_time),
            key_name = Name(dto.key_name),
            run_time = None if dto.run_time is None else K3SRunTime(dto.run_time),
            k3s_version = Version(dto.k3s_version),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: NodeInfo):
        return NodeInfoDTO(
            node_name = None if x.node_name is None else x.node_name.get_value(),
            node_type = None if x.node_type is None else x.node_type.get_value(),
            node_status = None if x.node_status is None else x.node_status.get_value(),
            instance_id = None if x.instance_id is None else x.instance_id.get_value(),
            instance_type = None if x.instance_type is None else x.instance_type.get_value(),
            hostname = None if x.hostname is None else x.hostname.get_value(),
            price = None if x.price is None else x.price.get_value(),
            image_id = None if x.image_id is None else x.image_id.get_value(),
            region_id = None if x.region_id is None else x.region_id.get_value(),
            zone_id = None if x.zone_id is None else x.zone_id.get_value(),
            internet_pay_type = None if x.internet_pay_type is None else x.internet_pay_type.get_value(),
            pay_type = None if x.pay_type is None else x.pay_type.get_value(),
            security_group_id = None if x.security_group_id is None else [m.get_value() for m in x.security_group_id],
            node_label = None if x.node_label is None else x.node_label.get_value(),
            cpu_number = None if x.cpu_number is None else x.cpu_number.get_value(),
            memory_size = None if x.memory_size is None else x.memory_size.get_value(),
            gpu_type = None if x.gpu_type is None else x.gpu_type.get_value(),
            gpu_number = None if x.gpu_number is None else x.gpu_number.get_value(),
            instance_type_status = None if x.instance_type_status is None else x.instance_type_status.get_value(),
            instance_type_status_category = None if x.instance_type_status_category is None else x.instance_type_status_category.get_value(),
            instance_name = None if x.instance_name is None else x.instance_name.get_value(),
            instance_status = None if x.instance_status is None else x.instance_status.get_value(),
            instance_create_time = None if x.instance_create_time is None else x.instance_create_time.get_value(),
            os_name = None if x.os_name is None else x.os_name.get_value(),
            public_ip = None if x.public_ip is None else [m.get_value() for m in x.public_ip],
            private_ip = None if x.private_ip is None else x.private_ip.get_value(),
            bandwidth_in = None if x.bandwidth_in is None else x.bandwidth_in.get_value(),
            bandwidth_out = None if x.bandwidth_out is None else x.bandwidth_out.get_value(),
            node_expired_time = None if x.node_expired_time is None else x.node_expired_time.get_value(),
            auto_release_time = None if x.auto_release_time is None else x.auto_release_time.get_value(),
            key_name = None if x.key_name is None else x.key_name.get_value(),
            run_time = None if x.run_time is None else x.run_time.get_value(),
            k3s_version = None if x.k3s_version is None else x.k3s_version.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )
node_info_assembler = NodeInfoAssembler()

class NodeCreationRequestAssembler(Assembler):
    def to_entity(self, dto: NodeCreationRequestDTO):
        return NodeCreationRequest(
            node_user_setting=node_user_setting_assembler.to_entity(dto.node_user_setting),
            condition=condition_assembler.to_entity(dto.condition)
        )
    def to_dto(self, x: NodeCreationRequest):
        return NodeCreationRequestDTO(
            node_user_setting=node_user_setting_assembler.to_dto(x.node_user_setting),
            condition=condition_assembler.to_dto(x.condition)
        )
node_creation_request_assembler = NodeCreationRequestAssembler()

class NodeCreationItemAssembler(Assembler):
    def to_entity(self, dto: NodeCreationItemDTO):
        return NodeCreationItem(
            id=NodeCreationItemID(dto.id),
            node_creation_request=None if dto.node_creation_request is None else node_creation_request_assembler.to_entity(dto.node_creation_request),
            creation_time=CreationTime(dto.creation_time),
            status=NodeCreationStatus(dto.status),
            details=None if dto.details is None else [node_info_assembler.to_entity(d) for d in dto.details],
            entry_time=None if dto.entry_time is None else DateTime(dto.entry_time),
            exit_time=None if dto.exit_time is None else DateTime(dto.exit_time),
            _life_time = Number(dto._life_time)
        )

    def to_dto(self, x: NodeCreationItem):
        return NodeCreationItemDTO(
            id=x.id.get_value(),
            node_creation_request=None if x.node_creation_request is None else node_creation_request_assembler.to_dto(x.node_creation_request),
            creation_time=x.creation_time.get_value().replace(microsecond=0).isoformat(),
            status=x.status.get_value(),
            details=None if x.details is None else [node_info_assembler.to_dto(d) for d in x.details],
            entry_time=None if x.entry_time is None else x.entry_time.get_value(),
            exit_time=None if x.exit_time is None else x.exit_time.get_value(),
            _life_time=x._life_time.get_value()
        )
node_creation_item_assembler = NodeCreationItemAssembler()

class NamespaceAssembler(Assembler):
    def to_entity(self, dto: NamespaceDTO):
        return Namespace(
            name = Name(dto.name),
            status = Status(dto.status),
            age = K3SRunTime(dto.age),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: Namespace):
        return NamespaceDTO(
            name = None if x.name is None else x.name.get_value(),
            status = None if x.status is None else x.status.get_value(),
            age = None if x.age is None else x.age.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )

class SecretAssembler(Assembler):
    def to_entity(self, dto: SecretDTO):
        return Secret(
            name = Name(dto.name),
            age = K3SRunTime(dto.age),
            namespace = Name(dto.namespace),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: Secret):
        return SecretDTO(
            name = None if x.name is None else x.name.get_value(),
            age = None if x.age is None else x.age.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )

class SecretUserSettingAssembler(Assembler):
    def to_entity(self, dto: SecretUserSettingDTO):
        return SecretUserSetting(
            name = Name(dto.name),
            key = Key(dto.key),
            value = Base64String(dto.value),
            namespace = Name(dto.namespace)
        )
    def to_dto(self, x: SecretUserSetting):
        return SecretUserSettingDTO(
            name = None if x.name is None else x.name.get_value(),
            key = None if x.key is None else x.key.get_value(),
            value = None if x.value is None else x.value.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value()
        )

class ConfigMapAssembler(Assembler):
    def to_entity(self, dto: ConfigMapDTO):
        return ConfigMap(
            name = Name(dto.name),
            age = K3SRunTime(dto.age),
            namespace = Name(dto.namespace),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: ConfigMap):
        return ConfigMapDTO(
            name = None if x.name is None else x.name.get_value(),
            age = None if x.age is None else x.age.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )

class ConfigMapUserSettingAssembler(Assembler):
    def to_entity(self, dto: ConfigMapUserSettingDTO):
        return ConfigMapUserSetting(
            name = Name(dto.name),
            key = Key(dto.key),
            value = Value(dto.value),
            key_type = ConfigMapType(dto.key_type),
            namespace = Name(dto.namespace)
        )
    def to_dto(self, x: ConfigMapUserSetting):
        return ConfigMapUserSettingDTO(
            name = None if x.name is None else x.name.get_value(),
            key = None if x.key is None else x.key.get_value(),
            value = None if x.value is None else x.value.get_value(),
            key_type = None if x.key_type is None else x.key_type.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value()
        )

class DeploymentAssembler(Assembler):
    def to_entity(self, dto: DeploymentDTO):
        return Deployment(
            name = Name(dto.name),
            age = K3SRunTime(dto.age),
            namespace = Name(dto.namespace),
            ready_info = Info(dto.ready_info),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: Deployment):
        return DeploymentDTO(
            name = None if x.name is None else x.name.get_value(),
            age = None if x.age is None else x.age.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            ready_info = None if x.ready_info is None else x.ready_info.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )

class PodAssembler(Assembler):
    def to_entity(self, dto: PodDTO):
        return Pod(
            name = Name(dto.name),
            node_name = None if dto.node_name is None else NodeName(dto.node_name),
            pod_status = PodStatus(dto.pod_status),
            age = K3SRunTime(dto.age),
            pod_ip = None if dto.pod_ip is None else IP(dto.pod_ip),
            namespace = Name(dto.namespace),
            restarts = RestartNumber(dto.restarts),
            readiness_info = Info(dto.readiness_info),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: Pod):
        return PodDTO(
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

class NodeMetaAssembler(Assembler):
    def to_entity(self, dto: NodeMetaDTO):
        return NodeMeta(
            name = NodeName(dto.name),
            status = NodeStatus(dto.status),
            run_time = K3SRunTime(dto.run_time),
            k3s_version = Version(dto.k3s_version),
            private_ip = IP(dto.private_ip),
            label = NodeLabel(dto.label)
        )
    def to_dto(self, x: NodeMeta):
        return NodeMetaDTO(
            name = None if x.name is None else x.name.get_value(),
            status = None if x.status is None else x.status.get_value(),
            run_time = None if x.run_time is None else x.run_time.get_value(),
            k3s_version = None if x.k3s_version is None else x.k3s_version.get_value(),
            private_ip = None if x.private_ip is None else x.private_ip.get_value(),
            label = None if x.label is None else x.label.get_value()
        )

class PodContainerAssembler(Assembler):
    def to_entity(self, dto: PodContainerDTO):
        return PodContainer(
            pod_name = Name(dto.pod_name),
            init_container_info = Info(dto.init_container_info),
            container_info = Info(dto.container_info),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: PodContainer):
        return PodContainerDTO(
            pod_name = None if x.pod_name is None else x.pod_name.get_value(),
            init_container_info = None if x.init_container_info is None else x.init_container_info.get_value(),
            container_info = None if x.container_info is None else x.container_info.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )

class IngressAssembler(Assembler):
    def to_entity(self, dto: IngressDTO):
        return Ingress(
            name = Name(dto.name),
            host_info = Info(dto.host_info),
            address_info = Info(dto.address_info),
            port = Number(dto.port),
            age = K3SRunTime(dto.age),
            namespace = Name(dto.namespace),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: Ingress):
        return IngressDTO(
            name = None if x.name is None else x.name.get_value(),
            host_info = None if x.host_info is None else x.host_info.get_value(),
            address_info = None if x.address_info is None else x.address_info.get_value(),
            port = None if x.port is None else x.port.get_value(),
            age = None if x.age is None else x.age.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )

class ServiceAssembler(Assembler):
    def to_entity(self, dto: ServiceDTO):
        return Service(
            name = Name(dto.name),
            service_type = ServiceType(dto.service_type),
            cluster_ip = IP(dto.cluster_ip),
            external_ip = IP(dto.external_ip),
            port_info = Info(dto.port_info),
            age = K3SRunTime(dto.age),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: Service):
        return ServiceDTO(
            name = None if x.name is None else x.name.get_value(),
            service_type = None if x.service_type is None else x.service_type.get_value(),
            cluster_ip = None if x.cluster_ip is None else x.cluster_ip.get_value(),
            external_ip = None if x.external_ip is None else x.external_ip.get_value(),
            port_info = None if x.port_info is None else x.port_info.get_value(),
            age = None if x.age is None else x.age.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )


class KeyToPathAssembler(Assembler):
    def to_entity(self, dto: KeyToPathDTO):
        return KeyToPath(
            key = Key(dto.key),
            path = Path(dto.path),
            mode = None if dto.mode is None else PathMode(dto.mode)
        )
    def to_dto(self, x: KeyToPath):
        return KeyToPathDTO(
            key = None if x.key is None else x.key.get_value(),
            path = None if x.path is None else x.path.get_value(),
            mode = None if x.mode is None else x.mode.get_value()
        )
key_to_path_assembler = KeyToPathAssembler()

class EnvVarSourceAssembler(Assembler):
    def to_entity(self, dto: EnvVarSourceDTO):
        return EnvVarSource(
            env_var_source_type = EnvVarSourceType(dto.env_var_source_type),
            key = Key(dto.key),
            name = Name(dto.name),
            optional = None if dto.optional is None else Bool(dto.optional)
        )
    def to_dto(self, x: EnvVarSource):
        return EnvVarSourceDTO(
            env_var_source_type = None if x.env_var_source_type is None else x.env_var_source_type.get_value(),
            key = None if x.key is None else x.key.get_value(),
            name = None if x.name is None else x.name.get_value(),
            optional = None if x.optional is None else x.optional.get_value()
        )
env_var_source_assembler = EnvVarSourceAssembler()

class EnvVarAssembler(Assembler):
    def to_entity(self, dto: EnvVarDTO):
        return EnvVar(
            name = Name(dto.name),
            value_from = None if dto.value_from is None else env_var_source_assembler.to_entity(dto.value_from),
            value = None if dto.value is None else Value(dto.value)
        )
    def to_dto(self, x: EnvVar):
        return EnvVarDTO(
            name = None if x.name is None else x.name.get_value(),
            value_from = None if x.value_from is None else env_var_source_assembler.to_dto(x.value_from),
            value = None if x.value is None else x.value.get_value()
        )
env_var_assembler = EnvVarAssembler()

class VolumeSourceAssembler(Assembler):
    def to_entity(self, dto: VolumeSourceDTO):
        return VolumeSource(
            name = Name(dto.name),
            volume_type = VolumeType(dto.volume_type),
            optional = None if dto.optional is None else Bool(dto.optional),
            default_mode = None if dto.default_mode is None else PathMode(dto.default_mode),
            items = None if dto.items is None else [key_to_path_assembler.to_entity(i) for i in dto.items]
        )
    def to_dto(self, x: VolumeSource):
        return VolumeSourceDTO(
            name = None if x.name is None else x.name.get_value(),
            volume_type = None if x.volume_type is None else x.volume_type.get_value(),
            optional = None if x.optional is None else x.optional.get_value(),
            default_mode = None if x.default_mode is None else x.default_mode.get_value(),
            items = None if x.items is None else [key_to_path_assembler.to_dto(i) for i in x.items]
        )
volume_source_assembler = VolumeSourceAssembler()

class PersistentVolumeClaimVolumeSourceAssembler(Assembler):
    def to_entity(self, dto: PersistentVolumeClaimeVolumeSourceDTO):
        return PersistentVolumeClaimVolumeSource(
            claim_name = Name(dto.claim_name),
            read_only = None if dto.read_only is None else ReadOnly(dto.read_only)
        )
    def to_dto(self, x: PersistentVolumeClaimVolumeSource):
        return PersistentVolumeClaimeVolumeSourceDTO(
            claim_name = x.claim_name.get_value(),
            read_only = None if x.read_only is None else x.read_only.get_value()
        )
persistent_volume_claim_volume_source_assembler = PersistentVolumeClaimVolumeSourceAssembler()
class VolumeSettingAssembler(Assembler):
    def to_entity(self, dto: VolumeSettingDTO):
        return VolumeSetting(
            volume_name = VolumeName(dto.volume_name),
            empty_dir = None if dto.empty_dir is None else Bool(dto.empty_dir),
            config_map = None if dto.config_map is None else volume_source_assembler.to_entity(dto.config_map),
            secret = None if dto.secret is None else volume_source_assembler.to_entity(dto.secret),
            persistent_volume_claim = None if dto.persistent_volume_claim is None else persistent_volume_claim_volume_source_assembler.to_entity(dto.persistent_volume_claim)
        )
    def to_dto(self, x: VolumeSetting):
        return VolumeSettingDTO(
            volume_name = None if x.volume_name is None else x.volume_name.get_value(),
            empty_dir = None if x.empty_dir is None else x.empty_dir.get_value(),
            config_map = None if x.config_map is None else volume_source_assembler.to_dto(x.config_map),
            secret = None if x.secret is None else volume_source_assembler.to_dto(x.secret),
            persistent_volume_claim = None if x.persistent_volume_claim is None else persistent_volume_claim_volume_source_assembler.to_dto(x.persistent_volume_claim)
        )
volume_setting_assembler = VolumeSettingAssembler()

class VolumeMountAssembler(Assembler):
    def to_entity(self, dto: VolumeMountDTO):
        return VolumeMount(
            name = Name(dto.name),
            mount_path = Path(dto.mount_path),
            read_only = None if dto.read_only is None else Bool(dto.read_only),
            sub_path = None if dto.sub_path is None else Path(dto.sub_path)
        )
    def to_dto(self, x: VolumeMount):
        return VolumeMountDTO(
            name = None if x.name is None else x.name.get_value(),
            mount_path = None if x.mount_path is None else x.mount_path.get_value(),
            read_only = None if x.read_only is None else x.read_only.get_value(),
            sub_path = None if x.sub_path is None else x.sub_path.get_value()
        )
volume_mount_assembler = VolumeMountAssembler()

class HTTPGetActionAssembler(Assembler):
    def to_entity(self, dto: HTTPGetActionDTO):
        return HTTPGetAction(
            port = Port(dto.port),
            host = None if dto.host is None else IP(dto.host),
            path = None if dto.path is None else Path(dto.path),
            http_headers = None if dto.http_headers is None else [HTTPHeader(m) for m in dto.http_headers],
            scheme = None if dto.schme is None else NetworkScheme(dto.scheme)
        )
    def to_dto(self, x: HTTPGetAction):
        return HTTPGetActionDTO(
            port = None if x.port is None else x.port.get_value(),
            host = None if x.host is None else x.host.get_value(),
            path = None if x.path is None else x.path.get_value(),
            http_headers = None if x.http_headers is None else [m.get_value() for m in x.http_headers],
            scheme = None if x.scheme is None else x.scheme.get_value()
        )
http_get_action_assmebler = HTTPGetActionAssembler()

class GRPCActionAssembler(Assembler):
    def to_entity(self, dto: GRPCActionDTO):
        return GRPCAction(
            port = Port(dto.port),
            service = None if dto.service is None else Name(dto.service)
        )
    def to_dto(self, x: GRPCAction):
        return GRPCActionDTO(
            port = None if x.port is None else x.port.get_value(),
            service = None if x.service is None else x.service.get_value()
        )
grpc_action_assembler = GRPCActionAssembler()

class TCPSocketActionAssembler(Assembler):
    def to_entity(self, dto: TCPSocketActionDTO):
        return TCPSocketAction(
            port = Port(dto.port),
            host = None if dto.host is None else IP(dto.host)
        )
    def to_dto(self, x: TCPSocketAction):
        return TCPSocketActionDTO(
            port = None if x.port is None else x.port.get_value(),
            host = None if x.host is None else x.host.get_value()
        )
tcp_socket_action_assembler = TCPSocketActionAssembler()

class ContainerPortAssembler(Assembler):
    def to_entity(self, dto: ContainerPortDTO):
        return ContainerPort(
            port = Port(dto.port),
            name = None if dto.name is None else Name(dto.name),
            protocol = None if dto.protocol is None else Protocol(dto.protocol),
            host_ip = None if dto.host_ip is None else IP(dto.host_ip),
            host_port = None if dto.host_port is None else Port(dto.host_port)
        )
    def to_dto(self, x: ContainerPort):
        return ContainerPortDTO(
            port = None if x.port is None else x.port.get_value(),
            name = None if x.name is None else x.name.get_value(),
            protocol = None if x.protocol is None else x.protocol.get_value(),
            host_ip = None if x.host_ip is None else x.host_ip.get_value(),
            host_port = None if x.host_port is None else x.host_port.get_value()
        )
container_port_assembler = ContainerPortAssembler()

class ProbeAssembler(Assembler):
    def to_entity(self, dto: ProbeDTO):
        return Probe(
            initial_delay_seconds = Number(dto.initial_delay_seconds),
            period_seconds = Number(dto.period_seconds),
            success_threshold = None if dto.success_threshold is None else Number(dto.success_threshold),
            timeout_seconds = Number(dto.timeout_seconds),
            command = None if dto.command is None else [ContainerCommand(m) for m in dto.command],
            failure_threshold = Number(dto.failure_threshold),
            grpc = None if dto.grpc is None else grpc_action_assembler.to_entity(dto.grpc),
            http_get = None if dto.http_get is None else http_get_action_assmebler.to_entity(dto.http_get),
            tcp_socket = None if dto.tcp_socket is None else tcp_socket_action_assembler.to_entity(dto.tcp_socket)
        )
    def to_dto(self, x: Probe):
        return ProbeDTO(
            initial_delay_seconds = None if x.initial_delay_seconds is None else x.initial_delay_seconds.get_value(),
            period_seconds = None if x.period_seconds is None else x.period_seconds.get_value(),
            success_threshold = None if x.success_threshold is None else x.success_threshold.get_value(),
            timeout_seconds = None if x.timeout_seconds is None else x.timeout_seconds.get_value(),
            command = None if x.command is None else [m.get_value() for m in x.command],
            failure_threshold = None if x.failure_threshold is None else x.failure_threshold.get_value(),
            grpc = None if x.grpc is None else grpc_action_assembler.to_dto(x.grpc),
            http_get = None if x.http_get is None else http_get_action_assmebler.to_dto(x.http_get),
            tcp_socket = None if x.tcp_socket is None else tcp_socket_action_assembler.to_dto(x.tcp_socket)
        )
probe_assembler = ProbeAssembler()

class LabelSelectorRequirementAssembler(Assembler):
    def to_entity(self, dto: LabelSelectorRequirementDTO):
        return LabelSelectorRequirement(
            key = Key(dto.key),
            operator = LabelSelectorOperator(dto.operator),
            values = None if dto.values is None else [Value(m) for m in dto.values]
        )
    def to_dto(self, x: LabelSelectorRequirement):
        return LabelSelectorRequirementDTO(
            key = None if x.key is None else x.key.get_value(),
            operator = None if x.operator is None else x.operator.get_value(),
            values = None if x.values is None else [m.get_value() for m in x.values]
        )
label_selector_requirement_assembler = LabelSelectorRequirementAssembler()

class LabelSelectorAssembler(Assembler):
    def to_entity(self, dto: LabelSelectorDTO):
        return LabelSelector(
            match_labels = None if dto.match_labels is None else MatchLabels(dto.match_labels),
            match_expressions = None if dto.match_expressions is None else [label_selector_requirement_assembler.to_entity(i) for i in dto.match_expressions]
        )
    def to_dto(self, x: LabelSelector):
        return LabelSelectorDTO(
            match_labels = None if x.match_labels is None else x.match_labels.get_value(),
            match_expressions = None if x.match_expressions is None else [label_selector_requirement_assembler.to_dto(x.match_expressions)]
        )
label_selector_assembler = LabelSelectorAssembler()

class SecurityContextAssembler(Assembler):
    def to_entity(self, dto: SecurityContextDTO):
        return SecurityContext(
            privileged = Bool(dto.privileged),
            run_as_user = Number(dto.run_as_user),
            run_as_non_root = Bool(dto.run_as_non_root)
        )
    def to_dto(self, x: SecurityContext):
        return SecurityContextDTO(
            privileged = None if x.privileged is None else x.privileged.get_value(),
            run_as_user = None if x.run_as_user is None else x.run_as_user.get_value(),
            run_as_non_root = None if x.run_as_non_root is None else x.run_as_non_root.get_value()
        )
security_context_assembler = SecurityContextAssembler()

class ContainerSettingAssembler(Assembler):
    def to_entity(self, dto: ContainerSettingDTO):
        return ContainerSetting(
            container_name=Name(dto.container_name),
            container_image=DockerImageName(dto.container_image),
            env_vars=None if dto.env_vars is None else [env_var_assembler.to_entity(i) for i in dto.env_vars],
            command=None if dto.command is None else ContainerCommand(dto.command),
            args=None if dto.args is None else ContainerArgs(dto.args) ,
            image_pull_policy=None if dto.image_pull_policy is None else ImagePullPolicy(dto.image_pull_policy),
            working_dir=None if dto.working_dir is None else Path(dto.working_dir),
            volume_mount = None if dto.volume_mount is None else [volume_mount_assembler.to_entity(i) for i in dto.volume_mount],
            security_context = None if dto.security_context is None else security_context_assembler.to_entity(dto.security_context),
            limits = None if dto.limits is None else PodResourceDict(dto.limits),
            requests = None if dto.requests is None else PodResourceDict(dto.requests),
            readiness_probe = None if dto.readiness_probe is None else probe_assembler.to_entity(dto.readiness_probe),
            liveness_probe = None if dto.liveness_probe is None else probe_assembler.to_entity(dto.liveness_probe),
            ports = None if dto.ports is None else [container_port_assembler.to_entity(i) for i in dto.ports]
        )
container_setting_assembler = ContainerSettingAssembler()



class DeploymentSettingAssembler(Assembler):
    def to_entity(self, dto: DeploymentSettingDTO):
        return DeploymentSetting(
            deployment_name=Name(dto.deployment_name),
            namespace_name=Name(dto.namespace_name),
            labels=LabelDict(dto.labels),
            containers=[container_setting_assembler.to_entity(c) for c in dto.containers],
            init_containers=None if dto.init_containers is None else [container_setting_assembler.to_entity(i) for i in dto.init_containers],
            node_name = None if dto.node_name is None else Name(dto.node_name),
            node_selector=None if dto.node_selector is None else NodeSelectorDict(dto.node_selector),
            replicas=None if dto.replicas is None else Number(dto.replicas),
            restart_policy=None if dto.restart_policy is None else RestartPolicy(dto.restart_policy),
            volumes = None if dto.volumes is None else [volume_setting_assembler.to_entity(i) for i in dto.volumes],
            selector = label_selector_assembler.to_entity(dto.selector),
            dns_policy = None if dto.dns_policy is None else DNSPolicy(dto.dns_policy),
            service_account_name = None if dto.service_account_name is None else ServiceAccountName(dto.service_account_name)
        )
deployment_setting_assembler = DeploymentSettingAssembler()
    

class JobSettingAssembler(Assembler):
    def to_entity(self, dto: JobSettingDTO):
        return JobSetting(
            job_name=Name(dto.job_name),
            namespace_name=Name(dto.namespace_name),
            labels = LabelDict(dto.labels),
            containers=[container_setting_assembler.to_entity(c) for c in dto.containers],
            init_containers=None if dto.init_containers is None else [container_setting_assembler.to_entity(i) for i in dto.init_containers],
            parallelism=None if dto.parallelism is None else Number(dto.parallelism),
            ttl_seconds_after_finished=None if dto.ttl_seconds_after_finished else Number(dto.ttl_seconds_after_finished),
            restart_policy=None if dto.restart_policy is None else RestartPolicy(dto.restart_policy),
            backoff_limit=None if dto.backoff_limit is None else Number(dto.backoff_limit),
            node_name = None if dto.node_name is None else Name(dto.node_name),
            node_selector = None if dto.node_selector is None else NodeSelectorDict(dto.node_selector),
            volumes = None if dto.volumes is None else [volume_setting_assembler.to_entity(i) for i in dto.volumes],
            selector = None if dto.selector is None else label_selector_assembler.to_entity(dto.selector),
            dns_policy = None if dto.dns_policy is None else DNSPolicy(dto.dns_policy),
            service_account_name = None if dto.service_account_name is None else ServiceAccountName(dto.service_account_name)
        )

class JobAssembler(Assembler):
    def to_entity(self, dto: JobDTO):
        return Job(
            name = Name(dto.name),
            age = K3SRunTime(dto.age),
            namespace = Name(dto.namespace),
            status = JobStatus(dto.status),
            parallelism = Number(dto.parallelism),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: Job):
        return JobDTO(
            name = None if x.name is None else x.name.get_value(),
            age = None if x.age is None else x.age.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            status = None if x.status is None else x.status.get_value(),
            parallelism = None if x.parallelism is None else x.parallelism.get_value(),
            _life_time = None if x._life_time is None else x._life_time.get_value()
        )

class PodLogSettingAssembler(Assembler):
    def to_entity(self, dto: PodLogSettingDTO):
        return PodLogSetting(
            namespace_name = Name(dto.namespace_name),
            pod_name = Name(dto.pod_name),
            container_name = None if dto.container_name is None else Name(dto.container_name),
            tail_lines = Integer(dto.tail_lines)
        )
    def to_dto(self, x: PodLogSetting):
        return PodLogSettingDTO(
            namespace_name = None if x.namespace_name is None else x.namespace_name.get_value(),
            pod_name = None if x.pod_name is None else x.pod_name.get_value(),
            container_name = None if x.container_name is None else x.container_name.get_value(),
            tail_lines = None if x.tail_lines is None else x.tail_lines.get_value()
        )

class StorageClassAssembler(Assembler):
    def to_entity(self, dto: StorageClassDTO):
        return StorageClass(
            name = Name(dto.name),
            provisioner = Provisioner(dto.provisioner),
            reclaim_policy = ReclaimPolicy(dto.reclaim_policy),
            volume_binding_mode = VolumeBindingMode(dto.volume_binding_mode),
            namespace_name = Name(dto.namespace_name)
        )
    def to_dto(self, x: StorageClass):
        return StorageClassDTO(
            name = None if x.name is None else x.name.get_value(),
            provisioner = None if x.provisioner is None else x.provisioner.get_value(),
            reclaim_policy = None if x.reclaim_policy is None else x.reclaim_policy.get_value(),
            volume_binding_mode = None if x.volume_binding_mode is None else x.volume_binding_mode.get_value(),
            namespace_name = None if x.namespace_name is None else x.namespace_name.get_value()
        )
storage_class_assembler = StorageClassAssembler()

class NFSVolumeSourceAssembler(Assembler):
    def to_entity(self, dto: NFSVolumeSourceDTO):
        return NFSVolumeSource(
            path = Path(dto.path),
            server = Server(dto.server),
            read_only = None if dto.read_only is None else ReadOnly(dto.read_only)
        )
    def to_dto(self, x: NFSVolumeSource):
        return NFSVolumeSourceDTO(
            path = None if x.path is None else x.path.get_value(),
            server = None if x.server is None else x.server.get_value(),
            read_only = None if x.read_only is None else x.read_only.get_value()
        )
nfs_volume_source_assembler = NFSVolumeSourceAssembler()

class LocalVolumeSourceAssembler(Assembler):
    def to_entity(self, dto: LocalVolumeSourceDTO):
        return LocalVolumeSource(
            path = Path(dto.path),
            fs_type = None if dto.fs_type is None else FSType(dto.fs_type)
        )
    def to_dto(self, x: LocalVolumeSource):
        return LocalVolumeSourceDTO(
            path = None if x.path is None else x.path.get_value(),
            fs_type = None if x.fs_type is None else x.fs_type.get_value()
        )
local_volume_source_assembler = LocalVolumeSourceAssembler()

class NodeSelectorRequirementAssembler(Assembler):
    def to_entity(self, dto: NodeSelectorRequirementDTO):
        return NodeSelectorRequirement(
            key = Key(dto.key),
            operator = Operator(dto.operator),
            values = [Value(m) for m in dto.values]
        )
    def to_dto(self, x: NodeSelectorRequirement):
        return NodeSelectorRequirementDTO(
            key = None if x.key is None else x.key.get_value(),
            operator = None if x.operator is None else x.operator.get_value(),
            values = None if x.values is None else [m.get_value() for m in x.values]
        )
node_selector_requirement_assembler = NodeSelectorRequirementAssembler()

class NodeAffinityAssembler(Assembler):
    def to_entity(self, dto: NodeAffinityDTO):
        return NodeAffinity(
            match_expressions = None if dto.match_expressions is None else [node_selector_requirement_assembler.to_entity(m) for m in dto.match_expressions],
            match_fields = None if dto.match_fields is None else [node_selector_requirement_assembler.to_entity(m) for m in dto.match_fields]
        )
    def to_dto(self, x: NodeAffinity):
        return NodeAffinityDTO(
            match_expressions = None if x.match_expressions is None else [node_selector_requirement_assembler.to_dto(m) for m in x.match_expressions],
            match_fields = None if x.match_fields is None else [node_selector_requirement_assembler.to_dto(m) for m in x.match_fields]
        )
node_affinity_assembler = NodeAffinityAssembler()

class PersistentVolumeAssembler(Assembler):
    def to_entity(self, dto: PersistentVolumeDTO):
        return PersistentVolume(
            name = Name(dto.name),
            namespace = Name(dto.namespace),
            persistent_volume_claim_name = None if dto.persistent_volume_claim_name is None else Name(dto.persistent_volume_claim_name),
            storage_class_name = None if dto.storage_class_name is None else StorageClassName(dto.storage_class_name),
            capacity = None if dto.capacity is None else Capacity(dto.capacity),
            access_modes = None if dto.access_modes is None else [AccessMode(m) for m in dto.access_modes],
            persistent_volume_reclaim_policy = None if dto.persistent_volume_reclaim_policy is None else PersistentVolumeReclaimPolicy(dto.persistent_volume_reclaim_policy),
            nfs = None if dto.nfs is None else nfs_volume_source_assembler.to_entity(dto.nfs),
            local = None if dto.local is None else local_volume_source_assembler.to_entity(dto.local),
            node_affinity = None if dto.node_affinity is None else [node_affinity_assembler.to_entity(m) for m in dto.node_affinity]
        )
    def to_dto(self, x: PersistentVolume):
        return PersistentVolumeDTO(
            name = None if x.name is None else x.name.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            persistent_volume_claim_name = None if x.persistent_volume_claim_name is None else x.persistent_volume_claim_name.get_value(),
            storage_class_name = None if x.storage_class_name is None else x.storage_class_name.get_value(),
            capacity = None if x.capacity is None else x.capacity.get_value(),
            access_modes = None if x.access_modes is None else [m.get_value() for m in x.access_modes],
            persistent_volume_reclaim_policy = None if x.persistent_volume_reclaim_policy is None else x.persistent_volume_reclaim_policy.get_value(),
            nfs = None if x.nfs is None else nfs_volume_source_assembler.to_dto(x.nfs),
            local = None if x.local is None else local_volume_source_assembler.to_dto(x.local),
            node_affinity = None if x.node_affinity is None else [node_affinity_assembler.to_dto(m) for m in x.node_affinity]
        )
persistent_volume_assembler = PersistentVolumeAssembler()

class PersistentVolumeClaimAssembler(Assembler):
    def to_entity(self, dto: PersistentVolumeClaimDTO):
        return PersistentVolumeClaim(
            name = Name(dto.name),
            namespace = Name(dto.namespace),
            labels = None if dto.labels is None else Label(dto.labels),
            access_modes = None if dto.access_modes is None else [AcceessMode(m) for m in dto.access_modes],
            storage_class_name = None if dto.storage_class_name is None else StorageClassName(dto.storage_class_name),
            limits = None if dto.limits is None else ResourceDict(dto.limits),
            requests = None if dto.requests is None else ResourceDict(dto.requests)
        )
    def to_dto(self, x: PersistentVolumeClaim):
        return PersistentVolumeClaimDTO(
            name = None if x.name is None else x.name.get_value(),
            namespace = None if x.namespace is None else x.namespace.get_value(),
            labels = None if x.labels is None else x.labels.get_value(),
            access_modes = None if x.access_modes is None else [m.get_value() for m in x.access_modes],
            storage_class_name = None if x.storage_class_name is None else x.storage_class_name.get_value(),
            limits = None if x.limits is None else x.limits.get_value(),
            requests = None if x.requests is None else x.requests.get_value()
        )
persistent_volume_claim_assembler = PersistentVolumeClaimAssembler()

class ReleaseNodeInfoAssembler(Assembler):
    def to_entity(self, dto: ReleaseNodeInfoDTO):
        return ReleaseNodeInfo(
            node_name=NodeName(dto.node_name),
            region_id = RegionID(dto.region_id),
            instance_id=InstanceID(dto.instance_id)
        )

    def to_dto(self, x: ReleaseNodeInfo):
        return ReleaseNodeInfoDTO(
            node_name = x.node_name.get_value(),
            region_id = x.region_id.get_value(),
            instance_id = x.instance_id.get_value()
        )
release_node_info_assembler = ReleaseNodeInfoAssembler()

class DatapipeServerInfoAssemlber(Assembler):
    def to_entity(self, dto: DatapipeServerInfoDTO):
        return DatapipeServerInfo(
            id = AccountID(dto.id),
            secret=AccountSecret(dto.secret),
            endpoint=ServerEndpoint(dto.endpoint)
        )
    
    def to_dto(self, x:DatapipeServerInfo):
        return DatapipeServerInfoDTO(
            id = x.id.get_value(),
            secret = x.secret.get_value(),
            endpoint = x.endpoint.get_value()
        )
datapipe_server_info_assembler = DatapipeServerInfoAssemlber()

class DatapipeHostAssembler(Assembler):
    def to_entity(self, dto: DatapipeHostDTO):
        return DatapipeHost(
            ip=IP(dto.ip),
            hostname=None if dto.hostname is None else Name(dto.hostname),
            port=Number(dto.port),
            username=Name(dto.username)
        )
    def to_dto(self, x: DatapipeHost):
        return DatapipeHostDTO(
            ip=x.ip.get_value(),
            hostname=None if x.hostname is None else x.hostname.get_value(),
            port=x.port.get_value(),
            username=x.username.get_value(),
        )
    pass
datapipe_host_assembler = DatapipeHostAssembler()

class DatapipeDataInfoAssembler(Assembler):
    def to_entity(self, dto: DatapipeDataInfoDTO):
        return DatapipeDataInfo(
            bucket = DataBucket(dto.bucket),
            remote_path=DatapipePath(dto.remote_path),
            local_path=DatapipePath(dto.local_path),
            timeout=Number(dto.timeout)
        )
    def to_do(self, x: DatapipeDataInfo):
        return DatapipeDataInfoDTO(
            bucket = x.bucket.get_value(),
            remote_path=x.remote_path.get_value(),
            local_path=x.local_path.get_value(),
            timeout = x.timeout.get_value()
        )
datapipe_data_info_assembler = DatapipeDataInfoAssembler()

class DatapipeResponseAssembler(Assembler):
    def to_entity(self, dto: DatapipeResponseDTO):
        return DatapipeResponse(
            status=CommandResponseStatus(dto.status),
            ip=IP(dto.ip),
            message=Text(dto.message),
            exception=None if dto.exception is None else Text(dto.exception),
            stdout=None if dto.stdout is None else Text(dto.stdout),
            cmd=None if dto.cmd is None else Text(dto.cmd),
            start_time=None if dto.start_time is None else DateTime(dto.start_time),
            end_time = None if dto.end_time is None else DateTime(dto.end_time),
            delta_time = None if dto.delta_time is None else DeltaTime(dto.delta_time),
            stderr=None if dto.stderr is None else Text(dto.stderr),
            entry_time=None if dto.entry_time is None else DateTime(dto.entry_time),
            exit_time=None if dto.exit_time is None else DateTime(dto.exit_time)
        )
    def to_dto(self, x: DatapipeResponse):
        return DatapipeResponseDTO(
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
datapipe_response_assembler = DatapipeResponseAssembler()