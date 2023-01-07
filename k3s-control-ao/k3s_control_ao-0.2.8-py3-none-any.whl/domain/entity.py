import datetime
from typing import List, Optional
from ddd_objects.domain.entity import Entity, ExpiredEntity
from ddd_objects.lib import get_random_string
from vpc_control_ao.domain.entity import (
    CommandRequest,
    CommandItem,
    Condition,
    CommandResponse,
    CommandHost,
    InstanceUserSetting,
    InstanceInfo,
)
from vpc_control_ao.domain.entity_ext import PipelineActionOutput, _PipelineStage
from .value_obj import (
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
    NodeSelectorDict
)



class NodeUserSetting(Entity):
    def __init__(
        self,
        name: NodeName,
        k3s_token: Optional[Token] = None,
        region_id: RegionID = RegionID('cn-zhangjiakou'),
        disk_size: Size = Size(20),
        bandwidth_in: BandWidth = BandWidth(200),
        bandwidth_out: BandWidth = BandWidth(1),
        image_id: ImageID = ImageID('ubuntu_20_04_x64_20G_alibase_20221107.vhd'),
        node_type: NodeType = NodeType('worker'),
        postfix: Bool = Bool(True),
        diff_instance_type: Bool = Bool(False),
        random_password: Bool = Bool(False),
        internet_pay_type: Type = Type('PayByTraffic'),
        master_ip: Optional[IP] = None,
        inner_connection: Bool = Bool(True),
        amount: Number = NodeAmount(1)
    ):
        self.name=name
        self.k3s_token=k3s_token
        self.region_id=region_id
        self.disk_size=disk_size
        self.bandwidth_in=bandwidth_in
        self.bandwidth_out=bandwidth_out
        self.image_id=image_id
        self.node_type=node_type
        self.postfix=postfix
        self.diff_instance_type=diff_instance_type
        self.random_password=random_password
        self.internet_pay_type=internet_pay_type
        self.master_ip=master_ip
        self.inner_connection=inner_connection
        self.amount=amount
        if amount.get_value() > 1:
            self.postfix = Bool(True)
            self.add_postfix()
            self.name = NodeName(self.name.get_value()+'-')
        else:
            self.add_postfix()
    
    def add_postfix(self):
        node_type = self.node_type.get_value()
        node_name = self.name.get_value()
        node_type_len = len(node_type.split('-'))
        node_name_len = len(node_name.split('-'))
        if self.postfix.get_value() and node_name_len-node_type_len==1:
            name = f'{self.name.get_value()}-{get_random_string(5).lower()}'
            self.name = NodeName(name)

class ReleaseNodeInfo(Entity):
    def __init__(
        self,
        node_name: NodeName,
        region_id: RegionID,
        instance_id: InstanceID
    ) -> None:
        self.node_name = node_name
        self.region_id = region_id
        self.instance_id = instance_id

class NodeInfo(ExpiredEntity):
    def __init__(
        self,
        node_name: NodeName,
        node_type: NodeType,
        node_status: NodeStatus,
        instance_id: InstanceID,
        instance_type: InstanceType,
        hostname: Hostname,
        price: Price,
        image_id: ImageID,
        region_id: RegionID,
        zone_id: ZoneID,
        internet_pay_type: InternetPayType,
        pay_type: PayType,
        security_group_id: List[SecurityGroupID],
        node_label: NodeLabel,
        cpu_number: Number,
        memory_size: Optional[Size],
        gpu_type: GPUType,
        gpu_number: Number,
        instance_type_status: InstanceTypeStatus,
        instance_type_status_category: InstanceTypeStatusCategory,
        instance_name: Name,
        instance_status: Status,
        instance_create_time: DateTime,
        os_name: Name,
        public_ip: List[IP],
        private_ip: IP,
        bandwidth_in: BandWidth,
        bandwidth_out: BandWidth,
        node_expired_time: Optional[DateTime],
        auto_release_time: Optional[DateTime],
        key_name: Name,
        run_time: Optional[K3SRunTime] = None,
        k3s_version: Optional[Version] = None,
        _life_time: Number = Number(5)
    ):
        self.node_name=node_name
        self.node_type=node_type
        self.node_status=node_status
        self.instance_id=instance_id
        self.instance_type=instance_type
        self.hostname=hostname
        self.price=price
        self.image_id=image_id
        self.region_id=region_id
        self.zone_id=zone_id
        self.internet_pay_type=internet_pay_type
        self.pay_type=pay_type
        self.security_group_id=security_group_id
        self.node_label=node_label
        self.cpu_number=cpu_number
        self.memory_size=memory_size
        self.gpu_type=gpu_type
        self.gpu_number=gpu_number
        self.instance_type_status=instance_type_status
        self.instance_type_status_category=instance_type_status_category
        self.instance_name=instance_name
        self.instance_status=instance_status
        self.instance_create_time=instance_create_time
        self.os_name=os_name
        self.public_ip=public_ip
        self.private_ip=private_ip
        self.bandwidth_in=bandwidth_in
        self.bandwidth_out=bandwidth_out
        self.node_expired_time=node_expired_time
        self.auto_release_time=auto_release_time
        self.key_name=key_name
        self.run_time=run_time
        self.k3s_version=k3s_version
        self._life_time=_life_time
        super().__init__(_life_time)

class NodeCreationRequest(Entity):
    def __init__(
        self,
        node_user_setting: NodeUserSetting,
        condition: Condition
    ) -> None:
        self.node_user_setting = node_user_setting
        self.condition = condition

class NodeCreationItem(ExpiredEntity):
    def __init__(
        self,
        id: NodeCreationItemID,
        node_creation_request: Optional[NodeCreationRequest],
        creation_time: CreationTime,
        status: NodeCreationStatus,
        details: Optional[List[NodeInfo]] = None,
        entry_time: Optional[DateTime] = None,
        exit_time: Optional[DateTime] = None,
        _life_time: Number = Number(86400)
    ) -> None:
        self.id = id
        self.node_creation_request = node_creation_request
        self.status = status
        self.creation_time=creation_time
        self.details = details
        self.entry_time = entry_time
        self.exit_time = exit_time
        self._life_time = _life_time
        super().__init__(_life_time=_life_time)

    def is_sending_timeout(self, timeout=30):
        if self.status.is_sent():
            diff = datetime.datetime.utcnow()-self.status.changed_time
            return diff.seconds>timeout
        return False


class Namespace(ExpiredEntity):
    def __init__(
        self,
        name: Name,
        status: Status,
        age: K3SRunTime,
        _life_time: Number = Number(5)
    ):
        self.name=name
        self.status=status
        self.age=age
        self._life_time=_life_time
        super().__init__(_life_time)

class Secret(ExpiredEntity):
    def __init__(
        self,
        name: Name,
        age: K3SRunTime,
        namespace: Name,
        _life_time: Number = Number(5)
    ):
        self.name=name
        self.age=age
        self.namespace=namespace
        self._life_time=_life_time
        super().__init__(_life_time)

class SecretUserSetting(Entity):
    def __init__(
        self,
        name: Name,
        key: Key,
        value: Base64String,
        namespace: Name
    ):
        self.name=name
        self.key=key
        self.value=value
        self.namespace=namespace

class ConfigMapUserSetting(Entity):
    def __init__(
        self,
        name: Name,
        key: Key,
        value: Value,
        key_type: ConfigMapType,
        namespace: Name
    ):
        self.name=name
        self.key=key
        self.value=value
        self.key_type=key_type
        self.namespace=namespace

class ConfigMap(ExpiredEntity):
    def __init__(
        self,
        name: Name,
        age: K3SRunTime,
        namespace: Name,
        _life_time: Number = Number(5)
    ):
        self.name=name
        self.age=age
        self.namespace=namespace
        self._life_time=_life_time
        super().__init__(_life_time)

class Deployment(ExpiredEntity):
    def __init__(
        self,
        name: Name,
        age: K3SRunTime,
        namespace: Name,
        ready_info: Info,
        _life_time: Number = Number(5)
    ):
        self.name=name
        self.age=age
        self.namespace=namespace
        self.ready_info=ready_info
        self._life_time=_life_time
        super().__init__(_life_time)

class Pod(ExpiredEntity):
    def __init__(
        self,
        name: Name,
        node_name: Optional[NodeName],
        pod_status: PodStatus,
        age: K3SRunTime,
        pod_ip: Optional[IP],
        namespace: Name,
        restarts: RestartNumber,
        readiness_info: Optional[Info],
        _life_time: Number = Number(5)
    ):
        self.name=name
        self.node_name=node_name
        self.pod_status=pod_status
        self.age=age
        self.pod_ip=pod_ip
        self.namespace=namespace
        self.restarts=restarts
        self.readiness_info=readiness_info
        self._life_time=_life_time
        super().__init__(_life_time)

class NodeMeta(Entity):
    def __init__(
        self,
        name: NodeName,
        status: NodeStatus,
        run_time: K3SRunTime,
        k3s_version: Version,
        private_ip: IP,
        label: NodeLabel
    ):
        self.name=name
        self.status=status
        self.run_time=run_time
        self.k3s_version=k3s_version
        self.private_ip=private_ip
        self.label=label

class PodContainer(ExpiredEntity):
    def __init__(
        self,
        pod_name: Name,
        init_container_info: Info,
        container_info: Info,
        _life_time: Number = Number(5)
    ):
        self.pod_name=pod_name
        self.init_container_info=init_container_info
        self.container_info=container_info
        self._life_time=_life_time
        super().__init__(_life_time)

class Ingress(ExpiredEntity):
    def __init__(
        self,
        name: Name,
        host_info: Info,
        address_info: Info,
        port: Number,
        age: K3SRunTime,
        namespace: Name,
        _life_time: Number = Number(5)
    ):
        self.name=name
        self.host_info=host_info
        self.address_info=address_info
        self.port=port
        self.age=age
        self.namespace=namespace
        self._life_time=_life_time
        super().__init__(_life_time)

class Service(ExpiredEntity):
    def __init__(
        self,
        name: Name,
        service_type: ServiceType,
        cluster_ip: IP,
        external_ip: Optional[IP],
        port_info: Info,
        age: K3SRunTime,
        _life_time: Number = Number(5)
    ):
        self.name=name
        self.service_type=service_type
        self.cluster_ip=cluster_ip
        self.external_ip=external_ip
        self.port_info=port_info
        self.age=age
        self._life_time=_life_time
        super().__init__(_life_time)

class KeyToPath(Entity):
    def __init__(
        self,
        key: Key,
        path: Path,
        mode: Optional[PathMode] = None
    ):
        self.key=key
        self.path=path
        self.mode=mode

class EnvVarSource(Entity):
    def __init__(
        self,
        env_var_source_type: EnvVarSourceType,
        key: Key,
        name: Name,
        optional: Optional[Bool] = None
    ):
        self.env_var_source_type=env_var_source_type
        self.key=key
        self.name=name
        self.optional=optional

class EnvVar(Entity):
    def __init__(
        self,
        name: Name,
        value: Optional[Value] = None,
        value_from: Optional[EnvVarSource] = None
    ):
        self.name=name
        self.value=value
        self.value_from=value_from

class VolumeSource(Entity):
    def __init__(
        self,
        name: Name,
        volume_type: VolumeType,
        optional: Optional[Bool] = None,
        default_mode: Optional[PathMode] = None,
        items: Optional[List[KeyToPath]] = None
    ):
        self.name=name
        self.volume_type=volume_type
        self.optional=optional
        self.default_mode=default_mode
        self.items = items

class PersistentVolumeClaimVolumeSource(Entity):
    def __init__(
        self,
        claim_name: Name,
        read_only: Optional[ReadOnly] = None
    ) -> None:
        self.claim_name = claim_name
        self.read_only = read_only

class VolumeSetting(Entity):
    def __init__(
        self,
        volume_name: VolumeName,
        empty_dir: Optional[Bool] = None,
        config_map: Optional[VolumeSource] = None,
        secret: Optional[VolumeSource] = None,
        persistent_volume_claim: Optional[PersistentVolumeClaimVolumeSource] = None
    ):
        self.volume_name=volume_name
        self.empty_dir=empty_dir
        self.config_map=config_map
        self.secret=secret
        self.persistent_volume_claim = persistent_volume_claim

class VolumeMount(Entity):
    def __init__(
        self,
        name: Name,
        mount_path: Path,
        read_only: Optional[Bool] = None,
        sub_path: Optional[Path] = None
    ):
        self.name=name
        self.mount_path=mount_path
        self.read_only=read_only
        self.sub_path=sub_path

class HTTPGetAction(Entity):
    def __init__(
        self,
        port: Port,
        host: Optional[IP] = None,
        path: Optional[Path] = None,
        http_headers: Optional[List[HTTPHeader]] = None,
        scheme: Optional[NetworkScheme] = None
    ):
        self.port=port
        self.host=host
        self.path=path
        self.http_headers=http_headers
        self.scheme=scheme

class GRPCAction(Entity):
    def __init__(
        self,
        port: Port,
        service: Optional[Name] = None
    ):
        self.port=port
        self.service=service

class TCPSocketAction(Entity):
    def __init__(
        self,
        port: Port,
        host: Optional[IP] = None
    ):
        self.port=port
        self.host=host

class ContainerPort(Entity):
    def __init__(
        self,
        port: Port,
        name: Optional[Name] = None,
        protocol: Optional[Protocol] = None,
        host_ip: Optional[IP] = None,
        host_port: Optional[Port] = None
    ):
        self.port=port
        self.name=name
        self.protocol=protocol
        self.host_ip=host_ip
        self.host_port=host_port

class Probe(Entity):
    def __init__(
        self,
        initial_delay_seconds: Number = Number(10),
        period_seconds: Number = Number(10),
        success_threshold: Optional[Number] = None,
        timeout_seconds: Number = Number(1),
        command: Optional[List[ContainerCommand]] = None,
        failure_threshold: Number = Number(3),
        grpc: Optional[GRPCAction] = None,
        http_get: Optional[HTTPGetAction] = None,
        tcp_socket: Optional[TCPSocketAction] = None
    ):
        self.initial_delay_seconds=initial_delay_seconds
        self.period_seconds=period_seconds
        self.success_threshold=success_threshold
        self.timeout_seconds=timeout_seconds
        self.command=command
        self.failure_threshold=failure_threshold
        self.grpc=grpc
        self.http_get=http_get
        self.tcp_socket=tcp_socket

class LabelSelectorRequirement(Entity):
    def __init__(
        self,
        key: Key,
        operator: LabelSelectorOperator,
        values: Optional[List[Value]] = None
    ):
        self.key=key
        self.operator=operator
        self.values=values

class LabelSelector(Entity):
    def __init__(
        self,
        match_expressions: Optional[List[LabelSelectorRequirement]],
        match_labels: Optional[MatchLabels],
    ):
        self.match_expressions = match_expressions
        self.match_labels=match_labels

class SecurityContext(Entity):
    def __init__(
        self,
        privileged: Optional[Bool] = None,
        run_as_user: Optional[Number] = None,
        run_as_non_root: Optional[Bool] = None
    ):
        self.privileged=privileged
        self.run_as_user=run_as_user
        self.run_as_non_root=run_as_non_root

class ContainerSetting(Entity):
    def __init__(
        self,
        container_name: Name,
        container_image: DockerImageName,
        env_vars: Optional[List[EnvVar]],
        command: Optional[ContainerCommand],
        args: Optional[ContainerArgs],
        image_pull_policy: Optional[ImagePullPolicy],
        working_dir: Optional[Path],
        volume_mount: Optional[List[VolumeMount]],
        security_context: Optional[SecurityContext],
        limits: Optional[PodResourceDict],
        requests: Optional[PodResourceDict],
        readiness_probe: Optional[Probe],
        liveness_probe: Optional[Probe],
        ports: Optional[List[ContainerPort]]
    ):
        self.container_name = container_name
        self.container_image = container_image
        self.env_vars = env_vars
        self.command = command
        self.args = args
        self.image_pull_policy = image_pull_policy
        self.working_dir = working_dir
        self.volume_mount = volume_mount
        self.security_context = security_context
        self.limits = limits
        self.requests = requests
        self.readiness_probe = readiness_probe
        self.liveness_probe = liveness_probe
        self.ports = ports


class DeploymentSetting(Entity):
    def __init__(
        self,
        deployment_name: Name,
        namespace_name: Name,
        labels: LabelDict,
        containers: List[ContainerSetting],
        init_containers: Optional[List[ContainerSetting]],
        node_name: Optional[Name],
        node_selector: Optional[NodeSelectorDict],
        replicas: Optional[Number],
        restart_policy: Optional[RestartPolicy],
        volumes: Optional[List[VolumeSetting]],
        selector: LabelSelector,
        dns_policy: Optional[DNSPolicy],
        service_account_name: Optional[ServiceAccountName] = None
    ) -> None:
        self.deployment_name = deployment_name
        self.namespace_name = namespace_name
        self.labels = labels
        self.containers = containers
        self.init_containers = init_containers
        self.node_name = node_name
        self.node_selector = node_selector
        self.replicas = replicas
        self.restart_policy = restart_policy
        self.volumes = volumes
        self.selector = selector
        self.dns_policy = dns_policy
        self.service_account_name = service_account_name



class JobSetting(Entity):
    def __init__(
        self,
        job_name: Name,
        namespace_name: Name,
        labels: LabelDict,
        containers: List[ContainerSetting],
        init_containers: Optional[List[ContainerSetting]],
        parallelism: Number = Number(1),
        ttl_seconds_after_finished: Number = Number(600),
        restart_policy: RestartPolicy = RestartPolicy('Never'),
        backoff_limit: Number = Number(2),
        node_name: Optional[Name] = None,
        node_selector: Optional[NodeSelectorDict] = None,
        volumes: Optional[List[VolumeSetting]] = None,
        selector: Optional[LabelSelector] = None,
        dns_policy: Optional[DNSPolicy] = None,
        service_account_name: Optional[ServiceAccountName] = None
    ):
        self.job_name = job_name
        self.namespace_name = namespace_name
        self.labels = labels
        self.containers = containers
        self.init_containers = init_containers
        self.parallelism = parallelism
        self.ttl_seconds_after_finished = ttl_seconds_after_finished
        if restart_policy is None:
            self.restart_policy = RestartPolicy('Never')
        else:
            self.restart_policy = restart_policy
        self.backoff_limit = backoff_limit
        self.node_name = node_name
        self.node_selector = node_selector
        self.volumes = volumes
        self.selector = selector
        self.dns_policy = dns_policy
        self.service_account_name = service_account_name

class Job(ExpiredEntity):
    def __init__(
        self,
        name: Name,
        age: K3SRunTime,
        namespace: Name,
        status: JobStatus,
        parallelism: Number,
        _life_time: Number = Number(5)
    ):
        self.name=name
        self.age=age
        self.namespace=namespace
        self.status=status
        self.parallelism=parallelism
        self._life_time=_life_time
        super().__init__(_life_time)

class PodLogSetting(Entity):
    def __init__(
        self,
        namespace_name: Name,
        pod_name: Name,
        container_name: Optional[Name] = None,
        tail_lines: Integer = Integer(500)
    ):
        self.namespace_name=namespace_name
        self.pod_name=pod_name
        self.container_name=container_name
        self.tail_lines=tail_lines

class StorageClass(Entity):
    def __init__(
        self,
        name: Name,
        provisioner: Provisioner,
        reclaim_policy: ReclaimPolicy,
        volume_binding_mode: VolumeBindingMode,
        namespace_name: Name
    ):
        self.name=name
        self.provisioner=provisioner
        self.reclaim_policy=reclaim_policy
        self.volume_binding_mode=volume_binding_mode
        self.namespace_name=namespace_name

class NFSVolumeSource(Entity):
    def __init__(
        self,
        path: Path,
        server: Server,
        read_only: Optional[ReadOnly] = None
    ):
        self.path=path
        self.server=server
        self.read_only=read_only

class LocalVolumeSource(Entity):
    def __init__(
        self,
        path: Path,
        fs_type: Optional[FSType] = None
    ):
        self.path=path
        self.fs_type=fs_type

class NodeSelectorRequirement(Entity):
    def __init__(
        self,
        key: Key,
        operator: Operator,
        values: List[Value]
    ):
        self.key=key
        self.operator=operator
        self.values=values

class NodeAffinity(Entity):
    def __init__(
        self,
        match_expressions: Optional[List[NodeSelectorRequirement]] = None,
        match_fields: Optional[List[NodeSelectorRequirement]] = None
    ):
        self.match_expressions=match_expressions
        self.match_fields=match_fields

class PersistentVolume(Entity):
    def __init__(
        self,
        name: Name,
        namespace: Name,
        persistent_volume_claim_name: Optional[Name] = None,
        storage_class_name: Optional[StorageClassName] = None,
        capacity: Optional[Capacity] = None,
        access_modes: Optional[List[AccessMode]] = None,
        persistent_volume_reclaim_policy: Optional[PersistentVolumeReclaimPolicy] = None,
        nfs: Optional[NFSVolumeSource] = None,
        local: Optional[LocalVolumeSource] = None,
        node_affinity: Optional[List[NodeAffinity]] = None
    ):
        self.name=name
        self.namespace=namespace
        self.persistent_volume_claim_name = persistent_volume_claim_name
        self.storage_class_name=storage_class_name
        self.capacity=capacity
        self.access_modes=access_modes
        self.persistent_volume_reclaim_policy=persistent_volume_reclaim_policy
        self.nfs=nfs
        self.local=local
        self.node_affinity=node_affinity

class PersistentVolumeClaim(Entity):
    def __init__(
        self,
        name: Name,
        namespace: Namespace,
        labels: Optional[Label] = None,
        access_modes: Optional[List[AcceessMode]] = None,
        storage_class_name: Optional[StorageClassName] = None,
        limits: Optional[ResourceDict] = None,
        requests: Optional[ResourceDict] = None
    ):
        self.name=name
        self.namespace=namespace
        self.labels=labels
        self.access_modes=access_modes
        self.storage_class_name=storage_class_name
        self.limits=limits
        self.requests=requests

class DatapipeServerInfo(Entity):
    def __init__(
        self,
        id: AccountID,
        secret: AccountSecret,
        endpoint: ServerEndpoint,
        
    ) -> None:
        self.id = id
        self.secret = secret
        self.endpoint = endpoint
        

class DatapipeHost(CommandHost):
    pass

class DatapipeDataInfo(Entity):
    def __init__(
        self,
        bucket: DataBucket,
        remote_path: DatapipePath,
        local_path: DatapipePath,
        timeout: Number
    ) -> None:
        self.bucket = bucket
        self.remote_path = remote_path
        self.local_path = local_path
        self.timeout = timeout
    
    def __str__(self) -> str:
        return self.__dict__

class DatapipeResponse(CommandResponse):
    pass