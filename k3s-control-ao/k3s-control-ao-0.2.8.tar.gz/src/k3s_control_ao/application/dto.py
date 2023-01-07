from typing import List, Optional, Union, Dict
from vpc_control_ao.application.dto import (
    ConditionDTO,
    CommandHostDTO,
    CommandResponseDTO,
    InstanceInfoDTO
)
import datetime
from pydantic import BaseModel

class NodeUserSettingDTO(BaseModel):
    name: str
    k3s_token: Optional[str]=None
    region_id: str='cn-zhangjiakou'
    disk_size: int=20
    bandwidth_in: int=200
    bandwidth_out: int=1
    image_id: str='ubuntu_20_04_x64_20G_alibase_20221107.vhd'
    node_type: str='worker'
    postfix: bool=True
    diff_instance_type: bool=False
    random_password: bool=True
    internet_pay_type: str='PayByTraffic'
    master_ip: Optional[str]=None
    inner_connection: bool=True
    amount: int=1

class NodeCreationRequestDTO(BaseModel):
    condition: ConditionDTO
    node_user_setting: NodeUserSettingDTO


class ReleaseNodeInfoDTO(BaseModel):
    node_name: str
    region_id: str
    instance_id: str

class NodeInfoDTO(BaseModel):
    node_name: str
    node_type: str
    node_status: str
    instance_id: str
    instance_type: str
    hostname: str
    price: float
    image_id: str
    region_id: str
    zone_id: str
    internet_pay_type: str
    pay_type: str
    security_group_id: List[str]
    node_label: Union[str, Dict]
    cpu_number: Optional[int]
    memory_size: Optional[float]
    gpu_type: Optional[str]
    gpu_number: Optional[int]
    instance_type_status: Optional[str]
    instance_type_status_category: Optional[str]
    instance_name: str
    instance_status: str
    instance_create_time: str
    os_name: str
    public_ip: List[str]
    private_ip: str
    bandwidth_in: int
    bandwidth_out: int
    node_expired_time: Optional[str]
    auto_release_time: Optional[str]
    key_name: Optional[str]
    run_time: Optional[float]=None
    k3s_version: Optional[str]=None
    _life_time: int=5


class NodeCreationItemDTO(BaseModel):
    id: str
    node_creation_request: Optional[NodeCreationRequestDTO]
    status: str
    creation_time: str
    details: Optional[List[NodeInfoDTO]]=None
    entry_time: Optional[str]=None
    exit_time: Optional[str]=None
    _life_time: int=86400


class NamespaceDTO(BaseModel):
    name: str
    status: str
    age: Union[str, datetime.timedelta]
    _life_time: int=5

class SecretDTO(BaseModel):
    name: str
    age: Union[str, datetime.timedelta]
    namespace: str
    _life_time: int=5

class SecretUserSettingDTO(BaseModel):
    name: str
    key: str
    value: str
    namespace: str

class ConfigMapDTO(BaseModel):
    name: str
    age: Union[str, datetime.timedelta]
    namespace: str
    _life_time: int=5

class ConfigMapUserSettingDTO(BaseModel):
    name: str
    key: str
    value: str
    namespace: str
    key_type: str = 'property'
    

class DeploymentDTO(BaseModel):
    name: str
    age: float
    namespace: str
    ready_info: str
    _life_time: int=5


class PodDTO(BaseModel):
    name: str
    node_name: Optional[str]
    pod_status: str
    age: float
    pod_ip: Optional[str]
    namespace: str
    restarts: str
    readiness_info: Optional[str]
    _life_time: int=5

class NodeMetaDTO(BaseModel):
    name: str
    status: str
    run_time: Union[str, datetime.timedelta]
    k3s_version: str
    private_ip: str
    label: Union[str, Dict]

class PodContainerDTO(BaseModel):
    pod_name: str
    init_container_info: str
    container_info: str
    _life_time: int=5

class IngressDTO(BaseModel):
    name: str
    host_info: str
    address_info: str
    port: int
    age: float
    namespace: str
    _life_time: int=5

class ServiceDTO(BaseModel):
    name: str
    service_type: str
    cluster_ip: str
    external_ip: Optional[str]
    port_info: str
    age: float
    _life_time: int=5


class KeyToPathDTO(BaseModel):
    key: str
    path: str
    mode: Optional[int]=None

class EnvVarSourceDTO(BaseModel):
    env_var_source_type: str
    key: str
    name: str
    optional: Optional[bool]=None

class EnvVarDTO(BaseModel):
    name: str
    value_from: Optional[EnvVarSourceDTO] = None
    value: Optional[str]=None

class VolumeSourceDTO(BaseModel):
    name: str
    volume_type: str
    optional: Optional[bool]=None
    items: Optional[List[KeyToPathDTO]] = None
    default_mode: Optional[int]=None

class PersistentVolumeClaimeVolumeSourceDTO(BaseModel):
    claim_name: str
    read_only: Optional[bool] = None

class VolumeSettingDTO(BaseModel):
    volume_name: str
    empty_dir: Optional[bool]=None
    config_map: Optional[VolumeSourceDTO] = None
    secret: Optional[VolumeSourceDTO] = None
    persistent_volume_claim: Optional[PersistentVolumeClaimeVolumeSourceDTO] = None

class VolumeMountDTO(BaseModel):
    name: str
    mount_path: str
    read_only: Optional[bool]=None
    sub_path: Optional[str]=None

class HTTPGetActionDTO(BaseModel):
    port: int
    host: Optional[str]=None
    path: Optional[str]=None
    http_headers: Optional[List[Dict]]=None
    scheme: Optional[str]=None

class GRPCActionDTO(BaseModel):
    port: int
    service: Optional[str]=None

class TCPSocketActionDTO(BaseModel):
    port: int
    host: Optional[str]=None

class ContainerPortDTO(BaseModel):
    port: int
    name: Optional[str]=None
    protocol: Optional[str]=None
    host_ip: Optional[str]=None
    host_port: Optional[int]=None

class ProbeDTO(BaseModel):
    initial_delay_seconds: int=10
    period_seconds: int=10
    success_threshold: Optional[int]=None
    timeout_seconds: int=1
    command: Optional[List[str]]=None
    failure_threshold: int=3
    grpc: Optional[GRPCActionDTO] = None
    http_get: Optional[HTTPGetActionDTO] = None
    tcp_socket: Optional[TCPSocketActionDTO] = None

class LabelSelectorRequirementDTO(BaseModel):
    key: str
    operator: str
    values: Optional[List[str]]=None

class LabelSelectorDTO(BaseModel):
    match_labels: Optional[Dict] = None
    match_expressions: Optional[List[LabelSelectorRequirementDTO]] = None

class SecurityContextDTO(BaseModel):
    privileged: Optional[bool]=None
    run_as_user: Optional[int]=None
    run_as_non_root: Optional[bool]=None

class ContainerSettingDTO(BaseModel):
    container_name: str
    container_image: str
    env_vars: Optional[List[EnvVarDTO]]= None
    command: Optional[List[str]] = None
    args: Optional[List[str]] = None
    image_pull_policy: Optional[str] = 'Always'
    working_dir: Optional[str] = None
    volume_mount: Optional[List[VolumeMountDTO]] = None
    security_context: Optional[SecurityContextDTO] = None
    limits: Optional[Dict] = None
    requests: Optional[Dict] = None
    readiness_probe: Optional[ProbeDTO] = None
    liveness_probe: Optional[ProbeDTO] = None
    ports: Optional[List[ContainerPortDTO]] = None


class DeploymentSettingDTO(BaseModel):
    deployment_name: str
    namespace_name: str
    labels: Dict
    containers: List[ContainerSettingDTO]
    init_containers: Optional[List[ContainerSettingDTO]] = None
    node_name: Optional[str] = None
    node_selector: Optional[Dict] = None
    replicas: Optional[int] = None
    restart_policy: Optional[str] = None
    volumes: Optional[List[VolumeSettingDTO]] = None
    selector: LabelSelectorDTO
    dns_policy: Optional[str] = None
    service_account_name: Optional[str] = None


class JobSettingDTO(BaseModel):
    job_name: str
    namespace_name: str
    labels: Dict
    containers: List[ContainerSettingDTO]
    init_containers: Optional[List[ContainerSettingDTO]] = None
    node_name: Optional[str] = None
    node_selector: Optional[Dict] = None
    parallelism: Optional[int] = None
    ttl_seconds_after_finished: Optional[int] = None
    restart_policy: Optional[str] = None
    backoff_limit: Optional[int] = None
    volumes: Optional[List[VolumeSettingDTO]] = None
    selector: Optional[LabelSelectorDTO] = None
    dns_policy: Optional[str] = None
    service_account_name: Optional[str] = None

class JobDTO(BaseModel):
    name: str
    age: Union[str, datetime.timedelta]
    namespace: str
    status: Dict
    parallelism: int
    _life_time: int=5

class PodLogSettingDTO(BaseModel):
    namespace_name: str
    pod_name: str
    container_name: Optional[str]=None
    tail_lines: int=500

class StorageClassDTO(BaseModel):
    name: str
    provisioner: str
    reclaim_policy: str
    volume_binding_mode: str
    namespace_name: str

class NFSVolumeSourceDTO(BaseModel):
    path: str
    server: str
    read_only: Optional[bool]=None

class LocalVolumeSourceDTO(BaseModel):
    path: str
    fs_type: Optional[str]=None

class NodeSelectorRequirementDTO(BaseModel):
    key: str
    operator: str
    values: List[str]

class NodeAffinityDTO(BaseModel):
    match_expressions: Optional[List[NodeSelectorRequirementDTO]]=None
    match_fields: Optional[List[NodeSelectorRequirementDTO]]=None

class PersistentVolumeDTO(BaseModel):
    name: str
    namespace: str
    persistent_volume_claim_name: Optional[str]=None
    storage_class_name: Optional[str]=None
    capacity: Optional[Dict]=None
    access_modes: Optional[List[str]]=None
    persistent_volume_reclaim_policy: Optional[str]=None
    nfs: Optional[NFSVolumeSourceDTO]=None
    local: Optional[LocalVolumeSourceDTO]=None
    node_affinity: Optional[List[NodeAffinityDTO]]=None

class PersistentVolumeClaimDTO(BaseModel):
    name: str
    namespace: str
    labels: Optional[Dict]=None
    access_modes: Optional[List[str]]=None
    storage_class_name: Optional[str]=None
    limits: Optional[Dict]=None
    requests: Optional[Dict]=None

class DatapipeServerInfoDTO(BaseModel):
    id: str
    secret: str
    endpoint: str

class DatapipeHostDTO(CommandHostDTO):
    pass

class DatapipeDataInfoDTO(BaseModel):
    bucket: str
    remote_path: str
    local_path: str
    timeout: int = 3

class DatapipeResponseDTO(CommandResponseDTO):
    pass

class NodeLabelSettingDTO(BaseModel):
    node_type: str
    key: str
    value: str