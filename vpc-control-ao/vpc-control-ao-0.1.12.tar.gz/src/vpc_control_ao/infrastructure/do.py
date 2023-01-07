from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from pydantic import BaseModel
from ddd_objects.infrastructure.do import BaseDO, ExpiredDO


class BanInstanceTypeRequestDO(BaseModel):
    instance_type: str
    region_id: str
    zone_id : str
    duration: Optional[int] = None


class BannedInstanceTypeResponseDO(BaseModel):
    instance_types: List[str]
    region_id: str
    zone_id: Optional[str]


class ConditionDO(BaseModel):
    min_cpu_num: Optional[int] = 1
    max_cpu_num: Optional[int] = 1
    min_memory_size: Optional[int] = 1
    max_memory_size: Optional[int] = 1
    min_gpu_num: Optional[int] = None
    max_gpu_num: Optional[int] = None
    min_gpu_memory_size: Optional[int] = None
    max_gpu_memory_size: Optional[int] = None

class InstanceUserSettingDO(BaseModel):
    name: str
    password: str = 'Abcd1234'
    amount: int = 1
    image_id: Optional[str]
    region_id: str
    internet_pay_type: Optional[str]
    bandwidth_in: int = 200
    bandwidth_out: int = 1
    user_data: Optional[str] = None
    disk_size: int = 20
    key_name: str
    exclude_instance_types: List[str]=[]
    inner_connection: bool = True

class InstanceCreationRequestDO(BaseModel):
    instance_user_setting: InstanceUserSettingDO
    condition: ConditionDO
    priority: int = 3
    timeout: int = 400

class InstanceInfoDO(BaseModel):
    id: str
    instance_type: str
    create_time: str
    name: str
    hostname: str
    pay_type: str
    public_ip: List[str]
    private_ip: Optional[str]
    os_name: str
    price: float
    image_id: str
    region_id: str
    zone_id: str
    internet_pay_type: str
    bandwidth_in: int
    bandwidth_out: int
    security_group_id: List[str]
    instance_expired_time: Optional[str]
    auto_release_time: Optional[str]
    status: str
    key_name: str
    _life_time: int = 5

class InstanceCreationItemDO(BaseModel):
    id: str
    instance_creation_request: Optional[InstanceCreationRequestDO]
    status: str
    creation_time: str
    details: Optional[List[InstanceInfoDO]] = None
    entry_time: Optional[str] = None
    exit_time: Optional[str] = None
    exception: Optional[str] = None
    _life_time: int=86400

class InstanceInfosDO(ExpiredDO):
    def __init__(self, instance_infos: List[InstanceInfoDO]) -> None:
        self.instance_infos = instance_infos
        super().__init__(life_time=5)

class InstanceSettingDO(ExpiredDO):
    def __init__(
        self,
        region_id: str,
        zone_id: str,
        spot_price: float,
        instance_type: str,
        amount: int,
        image_id: Optional[str],
        instance_name: str,
        password: Optional[str],
        disk_size: int,
        bandwidth_out: int,
        bandwidth_in: int,
        user_data: Optional[str],
        internet_pay_type: Optional[str],
        security_group_id: List[str],
        key_name: str,
    ):
        self.region_id=region_id
        self.zone_id=zone_id
        self.spot_price=spot_price
        self.instance_type=instance_type
        self.amount=amount
        self.image_id=image_id
        self.instance_name=instance_name
        self.password=password
        self.disk_size=disk_size
        self.bandwidth_out=bandwidth_out
        self.bandwidth_in=bandwidth_in
        self.user_data=user_data
        self.internet_pay_type=internet_pay_type
        self.security_group_id=security_group_id
        self.key_name = key_name
        super().__init__(life_time=5)

class InstanceTypeMetaDO(BaseModel):
    instance_type_meta_id: str
    CPU_number: float
    memory_size: float
    GPU_type:str
    GPU_number:int

class InstanceTypesMetaDO(ExpiredDO):
    def __init__(
        self,
        instance_types_meta = List[InstanceTypeMetaDO]
    ):
        self.instance_types_meta = instance_types_meta
        super().__init__(life_time=86400)

class InstanceTypeStatusInfoDO(ExpiredDO):
    def __init__(
        self,
        status: str,
        status_category: str
    ):
        self.status=status
        self.status_category=status_category
        super().__init__(life_time=30)

class RegionMetaDO(ExpiredDO):
    def __init__(
        self,
        name: str,
        id: str,
        endpoint: str
    ):
        self.name=name
        self.id=id
        self.endpoint=endpoint
        super().__init__(life_time=86400)

class RegionsMetaDO(ExpiredDO):
    def __init__(
        self,
        regions_meta: List[RegionMetaDO]
    ):
        self.regions_meta=regions_meta
        super().__init__(life_time=86400)

class SecurityGroupDO(BaseModel):
        id: str
        name: str

class SpotPriceDO(ExpiredDO):
    def __init__(
        self,
        spot_price: float
    ):
        self.spot_price=spot_price
        super().__init__(life_time=1800)

class ZoneDO(BaseModel):
    name: str
    id: str
    available_instance_types: List[str]
    

class ZonesDO(ExpiredDO):
    def __init__(
        self,
        zones: List[ZoneDO]
    ):
        self.zones=zones
        super().__init__(life_time=86400)
        
class KeyInfoDO(ExpiredDO):
    def __init__(
        self,
        name: str,
        private_key: str
    ):
        self.name = name
        self.private_key = private_key
        super().__init__(life_time=86400)

class CommandContextDO(BaseModel):
    connection: str='smart'
    module_path: str='/usr/local/bin/ansible'
    forks: int= 1
    timeout: int=300 
    remote_user: str='root'
    ask_pass: bool = False 
    ssh_extra_args: Optional[str] = None
    sftp_extra_args: Optional[str] = None
    scp_extra_args: Optional[str] = None 
    ask_value_pass: bool = False
    listhosts: bool = False 
    listtasks: bool = False 
    listtags: bool = False
    syntax: bool = False
    ssh_common_args='-o StrictHostKeyChecking=no'
    become: Optional[str] = None
    become_method: Optional[str] = None
    become_user: str = 'root' 
    check: bool = False 
    diff: bool = False
    verbosity: int = 1


class CommandSettingDetailDO(BaseModel):
    command: Union[str, dict]
    module: str = 'shell'
    retries: int = 2
    timeout: int = 3
    delay: float = 0.1


class CommandHostDO(BaseModel):
    ip: str
    hostname: Optional[str] = None
    port: int = 22
    username: str = 'root'

class CommandRequestDO(BaseModel):
    commands: Union[List[str], List[CommandSettingDetailDO]]
    hosts: Union[List[str], List[CommandHostDO]]
    context: Optional[CommandContextDO] = None
    priority: int = 3
    timeout: int = 3

class CommandResponseDO(BaseModel):
    status: str
    ip: str
    message: Optional[str] = None
    exception: Optional[str] = None
    stdout: Optional[str] = None
    cmd: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    delta_time: Optional[str] = None
    entry_time: Optional[str] = None
    exit_time: Optional[str] = None
    stderr: Optional[str] = None

class CommandItemDO(BaseModel):
    id: str
    command_request: Optional[CommandRequestDO]
    creation_time: str
    status: str
    details: Optional[List[CommandResponseDO]] = None
    exception: Optional[str] = None
    _life_time: int = 600
    
class CommandUserSettingDO(BaseDO):
    def __init__(
        self,
        hostname: str,
        ip: str,
        username: str = 'root',
        port: int = 22,
        password: Optional[str] = None,
        private_key_file: Optional[str] = None,
    ) -> None:
        self.hostname = hostname
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.private_key_file=private_key_file
        
class CommandUserSettingGroupDO:
    def __init__(
        self,
        group: List[CommandUserSettingDO],
    ):
        self.group = group

class CommandDO:
    def __init__(self, args:str, module: str='shell'):
        self.args = args
        self.module = module

class CommandResultDO(ExpiredDO):
    def __init__(
        self, 
        succeed: bool,
        output: str,
        ip: str
    ):
        self.succeed = succeed
        self.output = output
        self.ip = ip
        super().__init__(life_time=1)

class CommandResultsDO(ExpiredDO):
    def __init__(
        self,
        results: Dict[str, CommandResultDO]
    ):
        self.results = results

@dataclass
class DNSRecordDO:
    domain_name: str
    subdomain: str
    value: str
    id: Optional[str] = None
    dns_type: str = 'A'
    weight: Optional[int] = None
    ttl: int = 600
    priority: Optional[int] = None
    line: Optional[str] = None

@dataclass
class SecurityGroupPermissionDO(BaseDO):
    region_id: str
    security_group_id: str
    port: int
    dest_cidr_ip: Optional[str]=None
    source_cidr_ip: Optional[str]=None
    direction: str='egress'
    nic_type: str='internet'
    policy: str='Accept'
    description: str=''
    ip_protocol: str='TCP'

@dataclass
class DNSRecordDO(BaseDO):
    domain_name: str
    subdomain: str
    value: str
    id: Optional[str]=None
    weight: Optional[int]=None
    dns_type: str='A'
    ttl: int=600
    priority: Optional[int]=None
    line: Optional[str]=None

class ReleaseInstanceInfoDO(BaseModel):
    region_id: str
    instance_id: str

