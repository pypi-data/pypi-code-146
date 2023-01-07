import datetime
from typing import List, Optional, Union, Dict
from pydantic import BaseModel
from vpc_control_ao.infrastructure.do import (
    InstanceCreationRequestDO,
    InstanceCreationItemDO,
    CommandItemDO,
    CommandContextDO,
    CommandSettingDetailDO,
    CommandHostDO,
    CommandRequestDO,
    CommandResponseDO,
    ConditionDO,
    InstanceInfoDO,
    InstanceUserSettingDO,
    ReleaseInstanceInfoDO,
)

class NodeUserSettingDO(BaseModel):
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


class NodeCreationRequestDO(BaseModel):
    condition: ConditionDO
    node_user_setting: NodeUserSettingDO


class NodeInfoDO(BaseModel):
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
    cpu_number: Optional[int]=None
    memory_size: Optional[float]=None
    gpu_type: Optional[str]=None
    gpu_number: Optional[int]=None
    instance_type_status: Optional[str]=None
    instance_type_status_category: Optional[str]=None
    instance_name: str
    instance_status: str
    instance_create_time: str
    os_name: str
    public_ip: List[str]
    private_ip: str
    bandwidth_in: int
    bandwidth_out: int
    node_expired_time: Optional[str]=None
    auto_release_time: Optional[str]=None
    key_name: Optional[str]=None
    run_time: Optional[float]=None
    k3s_version: Optional[str]=None
    _life_time: int=5


class NodeCreationItemDO(BaseModel):
    id: str
    node_creation_request: Optional[NodeCreationRequestDO]
    status: str
    creation_time: str
    details: Optional[List[NodeInfoDO]]=None
    entry_time: Optional[str]=None
    exit_time: Optional[str]=None
    _life_time: int=86400



class NamespaceDO(BaseModel):
    name: str
    status: str
    age: float
    _life_time: int=5


class SecretDO(BaseModel):
    name: str
    age: float
    namespace: str
    _life_time: int=5


class SecretUserSettingDO(BaseModel):
    name: str
    key: str
    value: str
    namespace: str


class ConfigMapDO(BaseModel):
    name: str
    age: float
    namespace: str
    _life_time: int=5


class ConfigMapUserSettingDO(BaseModel):
    name: str
    key: str
    value: str
    key_type: str
    namespace: str


class DeploymentDO(BaseModel):
    name: str
    age: float
    namespace: str
    ready_info: str
    _life_time: int=5


class PodDO(BaseModel):
    name: str
    node_name: Optional[str]
    pod_status: str
    age: float
    pod_ip: Optional[str]
    namespace: str
    restarts: str
    readiness_info: Optional[str]
    _life_time: int=5


class IngressDO(BaseModel):
    name: str
    host_info: str
    address_info: str
    port: int
    age: float
    namespace: str
    _life_time: int=5


class ServiceDO(BaseModel):
    name: str
    service_type: str
    cluster_ip: str
    external_ip: Optional[str]
    port_info: str
    age: float
    _life_time: int=5


class PodContainerDO(BaseModel):
    pod_name: str
    init_container_info: str
    container_info: str
    _life_time: int=5


class ReleaseNodeInfoDO(BaseModel):
    node_name: str
    region_id: str
    instance_id: str


class NodeMetaDO(BaseModel):
    name: str
    status: str
    run_time: float
    k3s_version: str
    private_ip: str
    label: Union[str, Dict]


class KeyToPathDO(BaseModel):
    key: str
    path: str
    mode: Optional[int]=None


class EnvVarSourceDO(BaseModel):
    env_var_source_type: str
    key: str
    name: str
    optional: Optional[bool]=None


class EnvVarDO(BaseModel):
    name: str
    value_from: Optional[EnvVarSourceDO] = None
    value: Optional[str]=None


class VolumeSourceDO(BaseModel):
    name: str  
    volume_type: str
    default_mode: Optional[int] = None
    items: Optional[List[KeyToPathDO]] = None
    optional: Optional[bool] = None


class PersistentVolumeClaimeVolumeSourceDO(BaseModel):
    claim_name: str
    read_only: Optional[bool] = None


class VolumeSettingDO(BaseModel):
    volume_name: str
    empty_dir: Optional[bool] = None
    config_map: Optional[VolumeSourceDO] = None
    secret: Optional[VolumeSourceDO] = None
    persistent_volume_claim: Optional[PersistentVolumeClaimeVolumeSourceDO] = None


class VolumeMountDO(BaseModel):
    name: str
    mount_path: str
    read_only: Optional[bool]=None
    sub_path: Optional[str]=None


class ContainerPortDO(BaseModel):
    port: int
    name: Optional[str] = None
    protocol: Optional[str] = None
    host_ip: Optional[str] = None
    host_port: Optional[int] = None


class HTTPGetActionDO(BaseModel):
    port: int
    host: Optional[str] = None
    path: Optional[str] = None
    http_headers: Optional[List[Dict]] = None
    scheme: Optional[str] = None


class TCPSocketActionDO(BaseModel):
    port: int
    host: Optional[str] = None


class GRPCActionDO(BaseModel):
    port: int
    service: Optional[str] = None


class ProbeDO(BaseModel):
    initial_delay_seconds: int = 10
    period_seconds: int = 10
    success_threshold: Optional[int] = None
    timeout_seconds: int = 1
    command: Optional[List[str]] = None
    failure_threshold: int = 3
    grpc: Optional[GRPCActionDO] = None
    http_get: Optional[HTTPGetActionDO] = None
    tcp_socket: Optional[TCPSocketActionDO] = None


class LabelSelectorRequirementDO(BaseModel):
    key: str
    operator: str
    values: Optional[List[str]] = None


class LabelSelectorDO(BaseModel):
    match_expressions: Optional[List[LabelSelectorRequirementDO]] = None
    match_labels: Optional[Dict] = None


class SecurityContextDO(BaseModel):
    privileged: Optional[bool]=None
    run_as_user: Optional[int]=None
    run_as_non_root: Optional[bool]=None


class ContainerSettingDO(BaseModel):
    container_name: str
    container_image: str
    command: Optional[List[str]] = None
    args: Optional[List[str]] = None
    env_vars: Optional[List[EnvVarDO]] = None
    image_pull_policy: Optional[str] = None
    working_dir: Optional[str] = None
    volume_mount: Optional[List[VolumeMountDO]] = None
    security_context: Optional[SecurityContextDO] = None
    limits: Optional[Dict] = None
    requests: Optional[Dict] = None
    readiness_probe: Optional[ProbeDO] = None
    liveness_probe: Optional[ProbeDO] = None
    ports: Optional[List[ContainerPortDO]] = None


class DeploymentSettingDO(BaseModel):
    deployment_name: str
    namespace_name: str
    labels: Dict
    containers: List[ContainerSettingDO]
    init_containers: Optional[List[ContainerSettingDO]] = None
    node_name: Optional[str] = None
    node_selector: Optional[Dict] = None
    replicas: Optional[int] = None
    restart_policy: Optional[str] = None
    volumes: Optional[List[VolumeSettingDO]] = None
    selector: LabelSelectorDO
    dns_policy: Optional[str] = None
    service_account_name: Optional[str] = None



class JobSettingDO(BaseModel):
    job_name: str
    namespace_name: str
    labels: Dict
    containers: List[ContainerSettingDO]
    init_containers: Optional[List[ContainerSettingDO]]
    node_name: Optional[str] = None
    node_selector: Optional[Dict] = None
    parallelism: Optional[int] = 1
    ttl_seconds_after_finished: Optional[int] = 600
    restart_policy: Optional[str] = 'Never'
    backoff_limit: Optional[int] = 2
    volumes: Optional[List[VolumeSettingDO]] = None
    selector: Optional[LabelSelectorDO] = None
    dns_policy: Optional[str] = None
    service_account_name: Optional[str] = None


class JobDO(BaseModel):
    name: str
    age: float
    namespace: str
    status: Dict
    parallelism: int
    _life_time: int=5


class PodLogSettingDO(BaseModel):
    namespace_name: str
    pod_name: str
    container_name: Optional[str]=None
    tail_lines: int=500


class StorageClassDO(BaseModel):
    name: str
    provisioner: str
    reclaim_policy: str
    volume_binding_mode: str
    namespace_name: str


class NFSVolumeSourceDO(BaseModel):
    path: str
    server: str
    read_only: Optional[bool]=None


class LocalVolumeSourceDO(BaseModel):
    path: str
    fs_type: Optional[str]=None


class NodeSelectorRequirementDO(BaseModel):
    key: str
    operator: str
    values: List[str]


class NodeAffinityDO(BaseModel):
    match_expressions: Optional[List[NodeSelectorRequirementDO]]=None
    match_fields: Optional[List[NodeSelectorRequirementDO]]=None


class PersistentVolumeDO(BaseModel):
    name: str
    namespace: str
    persistent_volume_claim_name: Optional[str] = None
    storage_class_name: Optional[str]=None
    capacity: Optional[Dict]=None
    access_modes: Optional[List[str]]=None
    persistent_volume_reclaim_policy: Optional[str]=None
    nfs: Optional[NFSVolumeSourceDO]=None
    local: Optional[LocalVolumeSourceDO]=None
    node_affinity: Optional[List[NodeAffinityDO]]=None


class PersistentVolumeClaimDO(BaseModel):
    name: str
    namespace: str
    labels: Optional[Dict]=None
    access_modes: Optional[List[str]]=None
    storage_class_name: Optional[str]=None
    limits: Optional[Dict]=None
    requests: Optional[Dict]=None

class DatapipeServerInfoDO(BaseModel):
    id: str
    secret: str
    endpoint: str

class DatapipeHostDO(CommandHostDO):
    pass

class DatapipeDataInfoDO(BaseModel):
    bucket: str
    remote_path: str
    local_path: str
    timeout: int = 3

class DatapipeResponseDO(CommandResponseDO):
    pass
