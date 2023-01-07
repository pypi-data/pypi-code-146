import datetime, json
from dataclasses import dataclass
from re import I
from typing import Dict, List, Optional
from ddd_objects.domain.entity import Entity, ExpiredEntity
from ddd_objects.domain.exception import ValueError
from .value_obj import (
    CommandException,
    InstanceException,
    InstanceName,
    KeyName,
    U,
    CommandID,
    CommandModule,
    CommandPriority,
    CommandResponseStatus,
    CommandStatus,
    CreationTime,
    DeltaTime,
    InstanceCreationID,
    InstanceCreationPriority,
    InstanceCreationStatus,
    Price,
    InstanceID,
    Command,
    Bandwidth,
    Password,
    SecurityGroupID,
    Bool,
    DomainName,
    MinCPUNumber,
    MaxCPUNumber,
    Size,
    Path,
    InstanceTypeID,
    InstanceStatus,
    Number,
    Subdomain,
    Value,
    ID,
    Line,
    Data,
    Weight,
    MaxGPUNumber,
    Text,
    ImageID,
    DateTime,
    ZoneID,
    DNSType,
    MinMemorySize,
    Priority,
    Name,
    IP,
    MinGPUMemorySize,
    MaxGPUMemorySize,
    Type,
    MinGPUNumber,
    MaxMemorySize,
    RegionID
)

class BanInstanceTypeRequest(Entity):
    def __init__(
        self, 
        instance_type: InstanceTypeID, 
        region_id: RegionID,
        zone_id: ZoneID,
        duration: Optional[Number]=None
    ) -> None:
        self.instance_type = instance_type
        self.region_id = region_id
        self.zone_id = zone_id
        self.duration = duration
        super().__init__()

class BannedInstanceTypeResponse(Entity):
    def __init__(
        self, 
        instance_types: List[InstanceTypeID],
        region_id: RegionID,
        zone_id: Optional[ZoneID]

    ):
        self.instance_types = instance_types
        self.region_id = region_id
        self.zone_id = zone_id

class BannedInstanceTypeItem(ExpiredEntity):
    def __init__(
        self, 
        ban_instance_type_request:BanInstanceTypeRequest,
        _life_time: Number = Number(86400)
    ) -> None:
        self.ban_instance_type_request = ban_instance_type_request
        duration = ban_instance_type_request.duration
        if duration is None:
            self.ban_instance_type_request.duration = _life_time
        else:
            _life_time = duration
        super().__init__(_life_time=_life_time)

class Condition(Entity):
    def __init__(
        self,
        min_cpu_num: MinCPUNumber=MinCPUNumber(1),
        max_cpu_num: MaxCPUNumber=MaxCPUNumber(1),
        min_memory_size: MinMemorySize=MinMemorySize(1),
        max_memory_size: MaxMemorySize=MaxMemorySize(1),
        min_gpu_num: Optional[MinGPUNumber]=None,
        max_gpu_num: Optional[MaxGPUNumber]=None,
        min_gpu_memory_size: Optional[MinGPUMemorySize]=None,
        max_gpu_memory_size: Optional[MaxGPUMemorySize]=None
    ):
        
        if max_cpu_num.get_value()< min_cpu_num.get_value():
            raise ValueError('max_cpu_num should greater than min_cpu_num')
        if max_memory_size.get_value()<min_memory_size.get_value():
            raise ValueError('max_memory_size should greater than min_memory_size')
        if max_gpu_num is not None and min_gpu_num is not None and \
            max_gpu_num.get_value()< min_gpu_num.get_value():
            raise ValueError('max_gpu_num should greater than min_gpu_num')
        if max_gpu_memory_size is not None and min_gpu_memory_size is not None and \
            max_gpu_memory_size.get_value()<min_gpu_memory_size.get_value():
            raise ValueError('max_gpu_memory_size should greater than min_gpu_memory_size')
        
        self.min_cpu_num = min_cpu_num
        self.max_cpu_num = max_cpu_num
        self.min_memory_size = min_memory_size
        self.max_memory_size = max_memory_size
        self.min_gpu_num = min_gpu_num
        self.max_gpu_num = max_gpu_num
        self.min_gpu_memory_size = min_gpu_memory_size
        self.max_gpu_memory_size = max_gpu_memory_size

    def __str__(self) -> str:
        return json.dumps({
            'min_cpu_num': self.min_cpu_num.get_value(),
            'max_cpu_num': self.max_cpu_num.get_value(),
            'min_memory_size': self.min_memory_size.get_value(),
            'max_memory_size': self.max_memory_size.get_value(),
            'min_gpu_num': None if self.min_gpu_num is None else self.min_gpu_num.get_value(),
            'max_gpu_num': None if self.max_gpu_num is None else self.max_gpu_num.get_value(),
            'min_gpu_memory_size': None if self.min_gpu_memory_size is None else self.min_gpu_memory_size.get_value(),
            'max_gpu_memory_size': None if self.max_gpu_memory_size is None else self.max_gpu_memory_size.get_value()
        }).replace('\\', '')

@dataclass
class InstanceInfo(Entity):
    id: InstanceID
    instance_type: InstanceTypeID 
    create_time: DateTime 
    name: Name
    hostname: Name
    pay_type: Type
    public_ip: List[IP]
    private_ip: Optional[IP]
    os_name: Name
    price: Price
    image_id: ImageID
    region_id: RegionID
    zone_id: ZoneID
    internet_pay_type: Type
    bandwidth_in: Bandwidth
    bandwidth_out: Bandwidth
    status: InstanceStatus
    key_name: KeyName
    security_group_id: List[SecurityGroupID]
    instance_expired_time: Optional[DateTime] = None
    auto_release_time: Optional[DateTime] = None
    _life_time: Number = Number(5)


@dataclass
class InstanceSetting(Entity):
    name: Name
    region_id: RegionID
    zone_id: ZoneID
    security_group_id: SecurityGroupID
    instance_type: InstanceTypeID
    password: Password
    amount: Number
    spot_price: Price
    image_id: ImageID
    internet_pay_type: Type
    bandwidth_in: Bandwidth
    bandwidth_out: Bandwidth
    user_data: Data
    disk_size: Size
    key_name: KeyName

class InstanceUserSetting(Entity):
    def __init__(
        self,
        name: InstanceName = InstanceName('test'),
        password: Password=Password('1234Abcd'),
        amount: Number = Number(1),
        image_id: Optional[ImageID] = ImageID('centos_7_9_x64_20G_alibase_20220727.vhd'),
        region_id: RegionID = RegionID('cn-zhangjiakou'),
        internet_pay_type: Optional[Type] = None,
        bandwidth_in: Bandwidth = Bandwidth(200),
        bandwidth_out: Bandwidth = Bandwidth(1),
        user_data: Optional[Data] = None,
        disk_size: Size = Size(20),
        key_name: KeyName = KeyName('ansible'),
        exclude_instance_types: List[InstanceTypeID] = [],
        inner_connection: Bool = Bool(True)
    ) -> None:
        self.name = name
        self.password = password
        self.amount = amount
        self.image_id = image_id
        self.region_id = region_id
        self.internet_pay_type = internet_pay_type
        self.bandwidth_in = bandwidth_in
        self.bandwidth_out = bandwidth_out
        self.user_data = user_data
        self.disk_size = disk_size
        self.key_name = key_name
        self.exclude_instance_types = exclude_instance_types
        self.inner_connection = inner_connection
    
    def __str__(self) -> str:
        return json.dumps({
            'name': self.name.get_value(),
            'password': self.password.get_value(),
            'amount': self.amount.get_value(),
            'image_id': None if self.image_id is None else self.image_id.get_value(),
            'region_id': self.region_id.get_value(),
            'internet_pay_type': None if self.internet_pay_type is None else self.internet_pay_type.get_value(),
            'bandwidth_in': self.bandwidth_in.get_value(),
            'bandwidth_out': self.bandwidth_out.get_value(),
            'user_data': None if self.user_data is None else self.user_data.get_value(),
            'disk_size': self.disk_size.get_value(),
            'key_name': self.key_name.get_value(),
            'exclude_instance_types': [t.get_value() for t in self.exclude_instance_types],
            'inner_connectioin': self.inner_connection.get_value()
        })

class InstanceCreationRequest(Entity):
    def __init__(
        self, 
        instance_user_setting: InstanceUserSetting, 
        condition: Condition,
        priority: InstanceCreationPriority,
        timeout: Number
    ) -> None:
        self.instance_user_setting = instance_user_setting
        self.condition = condition
        self.priority = priority
        self.timeout = timeout
    
    def __str__(self) -> str:
        return json.dumps({
            'instance_user_setting': str(self.instance_user_setting),
            'condition': str(self.condition)
        }).replace('\\', '')

class InstanceCreationItem(ExpiredEntity):
    def __init__(
        self, 
        id: InstanceCreationID,
        instance_creation_request: InstanceCreationRequest,
        creation_time:CreationTime = CreationTime(),
        status: InstanceCreationStatus = InstanceCreationStatus(),
        details: Optional[List[InstanceInfo]] = None,
        entry_time: Optional[DateTime] = None,
        exit_time: Optional[DateTime] = None,
        _life_time: Number = Number(86400)
    ) -> None:
        self.id = id
        self.instance_creation_request = instance_creation_request
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

    def __str__(self) -> str:
        return json.dumps({
            'id': self.id.get_value(),
            'instance_creation_request': str(self.instance_creation_request),
            'creation_time': str(self.creation_time),
            'status': self.status.get_value(),
            'details': None if self.details is None else [str(d) for d in self.details],
            '_life_time': self._life_time.get_value()
        })
    

class CommandContext(Entity):
    def __init__(
        self,
        connection: U,
        module_path: Path,
        forks: Number,
        timeout: Number,
        remote_user: Name,
        ask_pass: Bool,
        ssh_extra_args: Optional[U],
        sftp_extra_args: Optional[U],
        scp_extra_args: Optional[U],
        ask_value_pass: Bool,
        listhosts: Bool,
        listtasks: Bool,
        listtags: Bool,
        syntax: Bool,
        ssh_common_args: U,
        become: Optional[U],
        become_method: Optional[str],
        become_user: Name,
        check: Bool,
        diff: Bool,
        verbosity: Number

    ):
        self.connection = connection
        self.module_path = module_path
        self.forks = forks
        self.timeout = timeout
        self.remote_user = remote_user
        self.ask_pass = ask_pass
        self.ssh_extra_args = ssh_extra_args
        self.sftp_extra_args = sftp_extra_args
        self.scp_extra_args = scp_extra_args
        self.ask_value_pass = ask_value_pass
        self.listhosts = listhosts
        self.listtasks = listtasks
        self.listtags = listtags
        self.syntax = syntax
        self.ssh_common_args = ssh_common_args
        self.become = become
        self.become_method = become_method
        self.become_user = become_user
        self.check = check
        self.diff = diff
        self.verbosity = verbosity

    def __str__(self) -> str:
        return json.dumps({
            'connection': self.connection.get_value(),
            'module_path': self.module_path.get_value(),
            'forks': self.forks.get_value(),
            'timeout': self.timeout.get_value(),
            'remote_user': self.remote_user.get_value(),
            'ask_pass': self.ask_pass.get_value(),
            'ssh_extra_args': None if self.ssh_extra_args is None else self.ssh_extra_args.get_value(),
            'sftp_extra_args': None if self.sftp_extra_args is None else self.sftp_extra_args.get_value(),
            'scp_extra_args': None if self.scp_extra_args is None else self.scp_extra_args.get_value(),
            'ask_value_pass': self.ask_value_pass.get_value(),
            'listhosts': self.listhosts.get_value(),
            'listtasks': self.listtasks.get_value(),
            'listtags': self.listtags.get_value(),
            'syntax': self.syntax.get_value(),
            'ssh_common_args': self.ssh_common_args.get_value(),
            'become': None if self.become is None else self.become.get_value(),
            'become_method': None if self.become_method is None else self.become_method.get_value(),
            'become_user': self.become_user.get_value(),
            'check': self.check.get_value(),
            'diff': self.diff.get_value(),
            'verbosity': self.verbosity.get_value()
        }).replace('\\', '')

class CommandSettingDetail(Entity):
    def __init__(
        self,
        command: Command,
        module: CommandModule=CommandModule('shell'),
        retries: Number=Number(2),
        timeout: Number=Number(3),
        delay: Number=Number(0.1)
    ) -> None:
        self.command = command
        self.module = module
        self.retries = retries
        self.timeout = timeout
        self.delay = delay
    
    def __str__(self) -> str:
        return json.dumps({
            'command': self.command.get_value(),
            'module': self.module.get_value(),
            'retries': self.retries.get_value(),
            'timeout': self.timeout.get_value(),
            'delay': self.delay.get_value()
        }).replace('\\', '')

class CommandHost(Entity):
    def __init__(
        self,
        ip: IP,
        hostname: Optional[Name],
        port: Number,
        username: Name
    ) -> None:
        self.ip = ip
        self.hostname = hostname
        self.port = port
        self.username = username

    def __str__(self) -> str:
        return json.dumps({
            'ip': self.ip.get_value(),
            'hostname': None if self.hostname is None else self.hostname.get_value(),
            'port': self.port.get_value(),
            'username': self.username.get_value()
        }).replace('\\', '')

class CommandRequest(Entity):
    def __init__(
        self,
        commands: List[CommandSettingDetail],
        hosts: List[CommandHost],
        context: Optional[CommandContext],
        priority: CommandPriority,
        timeout: Number,
    ) -> None:
        self.commands = commands
        self.hosts = hosts
        self.context = context
        self.priority = priority
        self.timeout = timeout

    def __str__(self) -> str:
        return json.dumps({
            'commands': [str(c) for c in self.commands],
            'hosts': [str(h) for h in self.hosts],
            'context': None if self.context is None else str(self.context),
            'priority': self.priority.get_value(),
            'timeout': self.timeout.get_value()
        }).replace('\\', '')

class CommandResponse(Entity):
    def __init__(
        self,
        status: CommandResponseStatus,
        ip: IP,
        message: Text,
        exception: Optional[Text],
        stdout: Optional[Text],
        cmd: Optional[Text],
        start_time: Optional[DateTime],
        end_time: Optional[DateTime],
        delta_time: Optional[DeltaTime],
        stderr: Optional[Text],
        entry_time: Optional[DateTime],
        exit_time: Optional[DateTime]
    ) -> None:
        self.status = status
        self.ip = ip
        self.message = message
        self.exception = exception
        self.stdout = stdout
        self.cmd = cmd
        self.start_time = start_time
        self.end_time = end_time
        self.delta_time = delta_time
        self.stderr = stderr
        self.entry_time = entry_time
        self.exit_time = exit_time

    def __str__(self) -> str:
        return json.dumps({
            'status': self.status.get_value(),
            'ip': self.ip.get_value(),
            'message': self.message.get_value(),
            'exception': None if self.exception is None else self.exception.get_value(),
            'stdout': None if self.stdout is None else self.stdout.get_value(),
            'cmd': None if self.cmd is None else self.cmd.get_value(),
            'start_time': None if self.start_time is None else self.start_time.get_value(),
            'end_time': None if self.end_time is None else self.end_time.get_value(),
            'delta_time': None if self.delta_time is None else self.delta_time.get_value(),
            'stderr': None if self.stderr is None else self.stderr.get_value(),
            'entry_time': None if self.entry_time is None else self.entry_time.get_value(),
            'exit_time': None if self.exit_time is None else self.exit_time.get_value()
        }).replace('\\', '')

class CommandItem(ExpiredEntity):
    def __init__(
        self, 
        id: CommandID,
        command_request: Optional[CommandRequest],
        creation_time:CreationTime = CreationTime(datetime.datetime.utcnow()),
        status: CommandStatus = CommandStatus(),
        details: Optional[List[CommandResponse]] = None,
        exception: Optional[CommandException] = None,
        _life_time: Number = Number(600)
    ) -> None:
        self.id = id
        self.command_request = command_request
        self.status = status
        self.creation_time=creation_time
        self.details = details
        self._life_time = _life_time
        self.exception = exception
        super().__init__(_life_time=_life_time)

    def is_sending_timeout(self, timeout=30):
        if self.status.is_sent():
            diff = datetime.datetime.utcnow()-self.status.changed_time
            return diff.seconds>timeout
        return False

    def __str__(self) -> str:
        return json.dumps({
            'id': self.id.get_value(),
            'command_request': None if self.command_request is None else str(self.command_request),
            'creation_time': str(self.creation_time),
            'status': self.status.get_value(),
            'details': None if self.details is None else [str(d) for d in self.details],
            'exception': None if self.exception is None else self.exception.get_value(),
        }).replace('\\', '')


class InstanceCreationItem(ExpiredEntity):
    def __init__(
        self, 
        id: InstanceCreationID,
        instance_creation_request: InstanceCreationRequest,
        creation_time:CreationTime = CreationTime(datetime.datetime.utcnow()),
        status: InstanceCreationStatus = InstanceCreationStatus(),
        details: Optional[List[InstanceInfo]] = None,
        entry_time: Optional[DateTime] = None,
        exit_time: Optional[DateTime] = None,
        exception: Optional[InstanceException] = None,
        _life_time: Number = Number(86400)
    ) -> None:
        self.id = id
        self.instance_creation_request = instance_creation_request
        self.status = status
        self.creation_time=creation_time
        self.details = details
        self._life_time = _life_time
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.exception = exception
        super().__init__(_life_time=_life_time)

    def is_sending_timeout(self, timeout=30):
        if self.status.is_sent():
            diff = datetime.datetime.utcnow()-self.status.changed_time
            return diff.seconds>timeout
        return False

    def __str__(self) -> str:
        return json.dumps({
            'id': self.id.get_value(),
            'instance_creation_request': None if self.instance_creation_request is None else str(self.instance_creation_request),
            'status': self.status.get_value(),
            'creation_time': str(self.creation_time),
            'details': None if self.details is None else [str(d) for d in self.details],
            '_life_time': self._life_time.get_value(),
            'entry_time': None if self.entry_time is None else self.entry_time.get_value(),
            'exit_time': None if self.exit_time is None else self.exit_time.get_value()
        }).replace('\\', '')


class DNSRecord(Entity):
    def __init__(
        self,
        domain_name: DomainName,
        subdomain: Subdomain,
        value: Value,
        id: Optional[ID] = None,
        weight: Optional[Weight] = None,
        dns_type: DNSType = DNSType('A'),
        ttl: Number = Number(600),
        priority: Optional[Priority] = None,
        line: Optional[Line] = None
    ):
        self.domain_name=domain_name
        self.subdomain=subdomain
        self.value=value
        self.id=id
        self.weight=weight
        self.dns_type=dns_type
        self.ttl=ttl
        self.priority=priority
        self.line=line

