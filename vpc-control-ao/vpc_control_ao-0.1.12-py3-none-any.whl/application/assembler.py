from typing import List
from ddd_objects.application.assembler import Assembler
from .dto import (
    BanInstanceTypeRequestDTO,
    BannedInstanceTypeResponseDTO,
    CommandContextDTO,
    CommandHostDTO,
    CommandItemDTO,
    CommandRequestDTO,
    CommandResponseDTO,
    CommandSettingDetailDTO,
    InstanceCreationItemDTO,
    InstanceCreationRequestDTO,
    ConditionDTO,
    InstanceUserSettingDTO,
    DNSRecordDTO,
    InstanceInfoDTO
)
from ..domain.entity import (
    BanInstanceTypeRequest,
    BannedInstanceTypeResponse,
    CommandContext,
    CommandHost,
    CommandItem,
    CommandRequest,
    CommandResponse,
    CommandSettingDetail,
    InstanceCreationItem,
    InstanceCreationRequest,
    InstanceInfo,
    Condition,
    DNSRecord,
    InstanceUserSetting,
)
from ..domain.value_obj import (
    CommandException,
    InstanceException,
    InstanceName,
    KeyName,
    U,
    Command,
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
    Bandwidth,
    Password,
    Bool,
    SecurityGroupID,
    DomainName,
    MinCPUNumber,
    Text,
    MaxCPUNumber,
    Size,
    Path,
    InstanceTypeID,
    Number,
    Status,
    Subdomain,
    Value,
    ID,
    Line,
    Data,
    Weight,
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
    MaxGPUNumber,
    MaxMemorySize,
    RegionID
)
from .dto import (
    DNSRecordDTO,
    ConditionDTO,
    InstanceInfoDTO,
    InstanceUserSettingDTO
)

class ConditionAssembler(Assembler):
    @Assembler.assemble_none
    def to_entity(self, dto: ConditionDTO):
        return Condition(
            min_cpu_num=MinCPUNumber(dto.min_cpu_num),
            max_cpu_num=MaxCPUNumber(dto.max_cpu_num),
            min_memory_size=MinMemorySize(dto.min_memory_size),
            max_memory_size=MaxMemorySize(dto.max_memory_size),
            min_gpu_num=None if dto.min_gpu_num is None else MinGPUNumber(dto.min_gpu_num),
            max_gpu_num=None if dto.max_gpu_num is None else MaxGPUNumber(dto.max_gpu_num),
            min_gpu_memory_size=None if dto.min_gpu_memory_size is None else MinGPUMemorySize(dto.min_gpu_memory_size),
            max_gpu_memory_size=None if dto.max_gpu_memory_size is None else MaxGPUMemorySize(dto.max_gpu_memory_size)
        )
    def to_dto(self, x: Condition):
        return ConditionDTO(
            min_cpu_num=x.min_cpu_num.get_value(),
            max_cpu_num=x.max_cpu_num.get_value(),
            min_memory_size=x.min_memory_size.get_value(),
            max_memory_size=x.max_memory_size.get_value(),
            min_gpu_num=None if x.min_gpu_num is None else x.min_gpu_num.get_value(),
            max_gpu_num=None if x.max_gpu_num is None else x.max_gpu_num.get_value(),
            min_gpu_memory_size=None if x.min_gpu_memory_size is None else x.min_gpu_memory_size.get_value(),
            max_gpu_memory_size=None if x.max_gpu_memory_size is None else x.max_gpu_memory_size.get_value()
        )
condition_assembler = ConditionAssembler()

class InstanceUserSettingAssembler(Assembler):
    @Assembler.assemble_none
    def to_entity(self, dto: InstanceUserSettingDTO):
        return InstanceUserSetting(
            name = InstanceName(dto.name),
            password=None if dto.password is None else Password(dto.password),
            amount=Number(dto.amount),
            image_id = None if dto.image_id is None else ImageID(dto.image_id),
            region_id=RegionID(dto.region_id),
            internet_pay_type=None if dto.internet_pay_type is None else Type(dto.internet_pay_type),
            bandwidth_in=Bandwidth(dto.bandwidth_in),
            bandwidth_out=Bandwidth(dto.bandwidth_out),
            user_data=None if dto.user_data is None else Data(dto.user_data),
            disk_size=Size(dto.disk_size),
            key_name = KeyName(dto.key_name),
            exclude_instance_types=[InstanceTypeID(x) for x in dto.exclude_instance_types],
            inner_connection = Bool(dto.inner_connection)
        )
    def to_dto(self, x: InstanceUserSetting):
        return InstanceUserSettingDTO(
            name = x.name.get_value(),
            password = None if x.password is None else x.password.get_value(),
            amount=x.amount.get_value(),
            image_id = None if x.image_id is None else x.image_id.get_value(),
            region_id= x.region_id.get_value(),
            internet_pay_type=None if x.internet_pay_type is None else x.internet_pay_type.get_value(),
            bandwidth_in= x.bandwidth_in.get_value(),
            bandwidth_out= x.bandwidth_out.get_value(),
            user_data=None if x.user_data is None else x.user_data.get_value(),
            disk_size=x.disk_size.get_value(),
            key_name = x.key_name.get_value(),
            exclude_instance_types=[m.get_value() for m in x.exclude_instance_types],
            inner_connection = x.inner_connection.get_value()
        )
instance_user_setting_assembler = InstanceUserSettingAssembler()

class InstanceInfoAssembler(Assembler):
    @Assembler.assemble_none
    def to_entity(self, dto: InstanceInfoDTO):
        return InstanceInfo(
            id = InstanceID(dto.id),
            instance_type=InstanceTypeID(dto.instance_type),
            create_time=DateTime(dto.create_time),
            name=Name(dto.name),
            hostname = Name(dto.hostname),
            pay_type = Type(dto.pay_type),
            public_ip = [IP(ip) for ip in dto.public_ip],
            private_ip = None if dto.private_ip is None else IP(dto.private_ip),
            os_name = Name(dto.os_name),
            price = Price(dto.price),
            image_id=ImageID(dto.image_id),
            region_id=RegionID(dto.region_id),
            zone_id = ZoneID(dto.zone_id),
            internet_pay_type = Type(dto.internet_pay_type),
            bandwidth_in = Bandwidth(dto.bandwidth_in),
            bandwidth_out = Bandwidth(dto.bandwidth_out),
            security_group_id = [SecurityGroupID(m) for m in dto.security_group_id],
            instance_expired_time = DateTime(dto.instance_expired_time),
            auto_release_time = DateTime(dto.auto_release_time),
            status = Status(dto.status),
            key_name=KeyName(dto.key_name)
        )
    @Assembler.assemble_none
    def to_dto(self, info: InstanceInfo):
        return InstanceInfoDTO(
            id=info.id.get_value(),
            instance_type=info.instance_type.get_value(),
            create_time=info.create_time.get_value(),
            name=info.name.get_value(),
            hostname=info.hostname.get_value(),
            pay_type=info.pay_type.get_value(),
            public_ip=[ip.get_value() for ip in info.public_ip],
            private_ip=None if info.private_ip is None else info.private_ip.get_value(),
            os_name=info.os_name.get_value(),
            price=info.price.get_value(),
            image_id=info.image_id.get_value(),
            region_id=info.region_id.get_value(),
            zone_id=info.zone_id.get_value(),
            internet_pay_type=info.internet_pay_type.get_value(),
            bandwidth_in=info.bandwidth_in.get_value(),
            bandwidth_out=info.bandwidth_out.get_value(),
            security_group_id=[id.get_value() for id in info.security_group_id],
            instance_expired_time=info.instance_expired_time.get_value(),
            auto_release_time=info.auto_release_time.get_value(),
            status=info.status.get_value(),
            key_name=info.key_name.get_value()
        )
instance_info_assembler = InstanceInfoAssembler()

class InstanceCreationRequestAssembler(Assembler):
    def to_entity(self, dto: InstanceCreationRequestDTO):
        return InstanceCreationRequest(
            instance_user_setting=instance_user_setting_assembler.to_entity(dto.instance_user_setting),
            condition=condition_assembler.to_entity(dto.condition),
            priority=InstanceCreationPriority(dto.priority),
            timeout=Number(dto.timeout) 
        )
    def to_dto(self, x: InstanceCreationRequest):
        return InstanceCreationRequestDTO(
            instance_user_setting = instance_user_setting_assembler.to_dto(x.instance_user_setting),
            condition = condition_assembler.to_dto(x.condition),
            priority=x.priority.get_value(),
            timeout=x.timeout.get_value()
        )
instance_creation_request_assembler = InstanceCreationRequestAssembler()

class InstanceCreationItemAssembler(Assembler):
    def to_entity(self, dto: InstanceCreationItemDTO):
        return InstanceCreationItem(
            id = InstanceCreationID(dto.id),
            instance_creation_request=None if dto.instance_creation_request is None else instance_creation_request_assembler.to_entity(dto.instance_creation_request),
            creation_time=CreationTime(dto.creation_time),
            status = InstanceCreationStatus(dto.status),
            details = None if dto.details is None else [instance_info_assembler.to_entity(m) for m in dto.details],
            entry_time = None if dto.entry_time is None else DateTime(dto.entry_time),
            exit_time = None if dto.exit_time is None else DateTime(dto.exit_time),
            exception = None if dto.exception is None else InstanceException(dto.exception),
            _life_time = Number(dto._life_time)
        )
    
    def to_dto(self, x: InstanceCreationItem):
        return InstanceCreationItemDTO(
            id = x.id.get_value(),
            instance_creation_request = None if x.instance_creation_request is None else instance_creation_request_assembler.to_dto(x.instance_creation_request),
            creation_time = x.creation_time.get_value().replace(microsecond=0).isoformat(),
            status = x.status.get_value(),
            details = None if x.details is None else [instance_info_assembler.to_dto(m) for m in x.details],
            entry_time = None if x.entry_time is None else x.entry_time.get_value(),
            exit_time = None if x.exit_time is None else x.exit_time.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            _life_time = x._life_time.get_value()
        )
instance_creation_item_assembler = InstanceCreationItemAssembler()

class BanInstanceTypeRequestAssembler(Assembler):
    def to_entity(self, dto: BanInstanceTypeRequestDTO):
        return BanInstanceTypeRequest(
            instance_type = InstanceTypeID(dto.instance_type),
            region_id= RegionID(dto.region_id),
            zone_id=ZoneID(dto.zone_id),
            duration = None if dto.duration is None else Number(dto.duration)
        )

    def to_dto(self, x: BanInstanceTypeRequest):
        return BanInstanceTypeRequestDTO(
            instance_type = x.instance_type.get_value(),
            region_id = x.region_id.get_value(),
            zone_id = x.zone_id.get_value(),
            duration = None if x.duration is None else x.duration.get_value()
        )
ban_instance_type_request_assembler = BanInstanceTypeRequestAssembler()

class BannedInstanceTypeResponseAssembler(Assembler):
    def to_entity(self, dto: BannedInstanceTypeResponseDTO):
        return BannedInstanceTypeResponse(
            instance_types = [InstanceTypeID(m) for m in dto.instance_types],
            region_id = RegionID(dto.region_id),
            zone_id = None if dto.zone_id is None else ZoneID(dto.zone_id)
        )

    def to_dto(self, x: BannedInstanceTypeResponse):
        return BannedInstanceTypeResponseDTO(
            instance_types = [m.get_value() for m in x.instance_types],
            region_id = x.region_id.get_value(),
            zone_id = None if x.zone_id is None else x.zone_id.get_value()
        )
banned_instance_type_response_assembler = BannedInstanceTypeResponseAssembler()

class CommandSettingDetailAssembler(Assembler):
    def to_entity(self, dto: CommandSettingDetailDTO):
        return CommandSettingDetail(
            command=Command(dto.command),
            module=CommandModule(dto.module),
            retries=Number(dto.retries),
            timeout=Number(dto.timeout),
            delay=Number(dto.delay)
        )
    def to_dto(self, x: CommandSettingDetail):
        return CommandSettingDetailDTO(
            command=x.command.get_value(),
            module=x.module.get_value(),
            retries=x.retries.get_value(),
            timeout=x.timeout.get_value(),
            delay=x.delay.get_value()
        )
command_setting_detail_assembler = CommandSettingDetailAssembler()
class CommandHostAssembler(Assembler):
    def to_entity(self, dto: CommandHostDTO):
        return CommandHost(
            ip=IP(dto.ip),
            hostname=None if dto.hostname is None else Name(dto.hostname),
            port=Number(dto.port),
            username=Name(dto.username)
        )
    def to_dto(self, x: CommandHost):
        return CommandHostDTO(
            ip=x.ip.get_value(),
            hostname=None if x.hostname is None else x.hostname.get_value(),
            port=x.port.get_value(),
            username=x.username.get_value(),
        )
command_host_assembler = CommandHostAssembler()

class CommandContextAssembler(Assembler):
    def to_entity(self, dto: CommandContextDTO):
        return CommandContext(
            connection=U(dto.connection),
            module_path=Path(dto.module_path),
            forks=Number(dto.forks),
            timeout=Number(dto.timeout),
            remote_user=Name(dto.remote_user),
            ask_pass=Bool(dto.ask_pass),
            ssh_extra_args=None if dto.ssh_extra_args is None else U(dto.ssh_extra_args),
            sftp_extra_args=None if dto.sftp_extra_args is None else U(dto.sftp_extra_args),
            scp_extra_args=None if dto.scp_extra_args is None else U(dto.scp_extra_args),
            ask_value_pass=Bool(dto.ask_value_pass),
            listhosts=Bool(dto.listhosts),
            listtasks=Bool(dto.listtasks),
            listtags=Bool(dto.listtags),
            syntax=Bool(dto.syntax),
            ssh_common_args=U(dto.ssh_common_args),
            become=None if dto.become is None else U(dto.become),
            become_method=None if dto.become_method is None else U(dto.become_method),
            become_user=Name(dto.become_user),
            check=Bool(dto.check),
            diff=Bool(dto.diff),
            verbosity=Number(dto.verbosity)
        )
    def to_dto(self, x: CommandContext):
        return CommandContextDTO(
            connection=x.connection.get_value(),
            module_path=x.module_path.get_value(),
            forks=x.forks.get_value(),
            timeout=x.timeout.get_value(),
            remote_user=x.remote_user.get_value(),
            ask_pass=x.ask_pass.get_value(),
            ssh_extra_args=None if x.ssh_extra_args is None else x.ssh_extra_args.get_value(),
            sftp_extra_args=None if x.sftp_extra_args is None else x.sftp_extra_args.get_value(),
            scp_extra_args=None if x.scp_extra_args is None else x.scp_extra_args.get_value(),
            ask_value_pass=x.ask_value_pass.get_value(),
            listhosts=x.listhosts.get_value(),
            listtasks=x.listtasks.get_value(),
            listtags=x.listtags.get_value(),
            syntax=x.syntax.get_value(),
            ssh_common_args=x.ssh_common_args.get_value(),
            become=None if x.become is None else x.become.get_value(),
            become_method=None if x.become_method is None else x.become_method.get_value(),
            become_user=x.become_user.get_value(),
            check=x.check.get_value(),
            diff=x.diff.get_value(),
            verbosity=x.verbosity.get_value()
        )
command_context_assembler = CommandContextAssembler()

class CommandRequestAssembler(Assembler):
    def to_entity(self, dto: CommandRequestDTO):
        return CommandRequest(
            commands=[command_setting_detail_assembler.to_entity(m) for m in dto.commands],
            hosts = [command_host_assembler.to_entity(m) for m in dto.hosts],
            context=None if dto.context is None else command_context_assembler.to_entity(dto.context),
            priority=CommandPriority(dto.priority),
            timeout=Number(dto.timeout),
        )
    def to_dto(self, x: CommandRequest):
        return CommandRequestDTO(
            commands = [command_setting_detail_assembler.to_dto(m) for m in x.commands],
            hosts=[command_host_assembler.to_dto(m) for m in x.hosts],
            context=None if x.context is None else command_context_assembler.to_dto(x.context),
            priority=x.priority.get_value(),
            timeout=x.timeout.get_value(),
        )
command_request_assembler = CommandRequestAssembler()

class CommandResponseAssembler(Assembler):
    def to_entity(self, dto: CommandResponseDTO):
        return CommandResponse(
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
    def to_dto(self, x: CommandResponse):
        return CommandResponseDTO(
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
command_response_assembler = CommandResponseAssembler()

class CommandItemAssembler(Assembler):
    def to_entity(self, dto: CommandItemDTO):
        return CommandItem(
            id=InstanceCreationID(dto.id),
            command_request=None if dto.command_request is None else command_request_assembler.to_entity(dto.command_request),
            creation_time=CreationTime(dto.creation_time),
            status=CommandStatus(dto.status),
            details=None if dto.details is None else [command_response_assembler.to_entity(m) for m in dto.details],
            exception=None if dto.exception is None else CommandException(dto.exception),
            _life_time = Number(dto._life_time)
        )
    def to_dto(self, x: CommandItem):
        return CommandItemDTO(
            id=x.id.get_value(),
            command_request=None if x.command_request is None else command_request_assembler.to_dto(x.command_request),
            creation_time = x.creation_time.get_value().replace(microsecond=0).isoformat(),
            status=x.status.get_value(),
            details=None if x.details is None else [command_response_assembler.to_dto(m) for m in x.details],
            exception=None if x.exception is None else x.exception.get_value(),
            _life_time=x._life_time.get_value()
        )
command_item_assembler = CommandItemAssembler()

class DNSRecordAssembler(Assembler):
    def to_entity(self, dto: DNSRecordDTO):
        return DNSRecord(
            domain_name = DomainName(dto.domain_name),
            subdomain = Subdomain(dto.subdomain),
            value = Value(dto.value),
            id = ID(dto.id),
            weight = Weight(dto.weight),
            dns_type = DNSType(dto.dns_type),
            ttl = Number(dto.ttl),
            priority = Priority(dto.priority),
            line = Line(dto.line)
        )
    def to_dto(self, x: DNSRecord):
        return DNSRecordDTO(
            domain_name = None if x.domain_name is None else x.domain_name.get_value(),
            subdomain = None if x.subdomain is None else x.subdomain.get_value(),
            value = None if x.value is None else x.value.get_value(),
            id = None if x.id is None else x.id.get_value(),
            weight = None if x.weight is None else x.weight.get_value(),
            dns_type = None if x.dns_type is None else x.dns_type.get_value(),
            ttl = None if x.ttl is None else x.ttl.get_value(),
            priority = None if x.priority is None else x.priority.get_value(),
            line = None if x.line is None else x.line.get_value()
        )
