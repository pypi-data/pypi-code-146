from typing import List, Optional, Union
from ddd_objects.domain.exception import ParameterError
from pydantic import BaseModel

class BanInstanceTypeRequestDTO(BaseModel):
    instance_type: str
    region_id: str
    zone_id : str
    duration: Optional[int] = None

class BannedInstanceTypeResponseDTO(BaseModel):
    instance_types: Optional[List[str]]
    region_id: str
    zone_id: Optional[str]

class ConditionDTO(BaseModel):
    min_cpu_num: Optional[int] = 1
    max_cpu_num: Optional[int] = 1
    min_memory_size: Optional[int] = 1
    max_memory_size: Optional[int] = 1
    min_gpu_num: Optional[int] = None
    max_gpu_num: Optional[int] = None
    min_gpu_memory_size: Optional[int] = None
    max_gpu_memory_size: Optional[int] = None

class InstanceUserSettingDTO(BaseModel):
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

class InstanceCreationRequestDTO(BaseModel):
    instance_user_setting: InstanceUserSettingDTO
    condition: ConditionDTO
    priority: int = 3
    timeout: int = 400

class InstanceInfoDTO(BaseModel):
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

class InstanceCreationItemDTO(BaseModel):
    id: str
    instance_creation_request: Optional[InstanceCreationRequestDTO]
    status: str
    creation_time: str
    details: Optional[List[InstanceInfoDTO]] = None
    entry_time: Optional[str] = None
    exit_time: Optional[str] = None
    exception: Optional[str] = None
    _life_time: int=86400

class ReleaseInstanceInfoDTO(BaseModel):
    region_id: str
    instance_id: str

class CommandContextDTO(BaseModel):
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

class CommandSettingDetailDTO(BaseModel):
    command: Union[str, dict]
    module: str = 'shell'
    retries: int = 2
    timeout: int = 3
    delay: float = 0.1

class CommandHostDTO(BaseModel):
    ip: str
    hostname: Optional[str] = None
    port: int = 22
    username: str = 'root'

class CommandRequestDTO(BaseModel):
    commands: Union[List[str], List[CommandSettingDetailDTO]]
    hosts: Union[List[str], List[CommandHostDTO]]
    context: Optional[CommandContextDTO]=None
    priority: int = 3
    timeout: int = 3

    def __init__(self, **data) -> None:
        commands = data['commands']
        hosts = data['hosts']
        if len(commands)==0:
            raise ParameterError('No command is set when creating CommandRequestDTO object.')
        if len(hosts)==0:
            raise ParameterError('No host is set when creating CommandRequestDTO object.')
        if isinstance(commands[0], str):
            data['commands'] = [CommandSettingDetailDTO(command=c) for c in commands]
        if isinstance(hosts[0], str):
            data['hosts'] = [CommandHostDTO(ip=h) for h in hosts]
        super().__init__(**data)
    
class CommandResponseDTO(BaseModel):
    status: str
    ip: str
    message: Optional[str] = None
    exception: Optional[str] = None
    stdout: Optional[str] = None
    cmd: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    delta_time: Optional[str] = None
    stderr: Optional[str] = None
    entry_time: Optional[str] = None
    exit_time: Optional[str] = None

class CommandItemDTO(BaseModel):
    id: str
    command_request: Optional[CommandRequestDTO]
    creation_time: str
    status: str
    details: Optional[List[CommandResponseDTO]] = None
    exception: Optional[str] = None
    _life_time: int = 600

class DNSRecordDTO(BaseModel):
    domain_name: str
    subdomain: str
    value: str
    id: Optional[str]=None
    weight: Optional[int]=None
    dns_type: str='A'
    ttl: int=600
    priority: Optional[int]=None
    line: Optional[str]=None
