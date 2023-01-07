from typing import List
from ddd_objects.infrastructure.converter import Converter

from ..domain.entity import (
    BanInstanceTypeRequest,
    BannedInstanceTypeResponse,
    CommandContext,
    CommandHost,
    CommandItem,
    CommandRequest,
    CommandResponse,
    CommandSettingDetail,
    Condition,
    InstanceCreationItem,
    InstanceCreationRequest,
    InstanceUserSetting,
    InstanceInfo,
    DNSRecord,
    InstanceSetting,
)
from ..domain.value_obj import (
    CommandException,
    InstanceException,
    InstanceName,
    KeyName,
    U,
    Command,
    CommandID,
    CommandModule,
    CommandPriority,
    CommandResponseStatus,
    CommandStatus,
    CreationTime,
    Data,
    DeltaTime,
    InstanceCreationID,
    InstanceCreationPriority,
    InstanceCreationStatus,
    MaxCPUNumber,
    MaxGPUMemorySize,
    MaxGPUNumber,
    MaxMemorySize,
    MinCPUNumber,
    MinGPUMemorySize,
    MinGPUNumber,
    MinMemorySize,
    Password,
    Path,
    Size,
    Type,
    IP,
    Bandwidth,
    SecurityGroupID,
    InstanceInfoID,
    ImageID,
    DNSType,
    Price,
    Bool,
    RegionID,
    ID,
    InstanceTypeID,
    Priority,
    InstanceStatus,
    Text,
    DomainName,
    Line,
    Value,
    Number,
    Name,
    Subdomain,
    Weight,
    DateTime,
    ZoneID
)
from .do import (
    BanInstanceTypeRequestDO,
    BannedInstanceTypeResponseDO,
    CommandContextDO,
    CommandHostDO,
    CommandResponseDO,
    CommandSettingDetailDO,
    InstanceInfoDO,
    DNSRecordDO,
    InstanceSettingDO,
    ConditionDO,
    InstanceUserSettingDO,
    InstanceCreationRequestDO,
    InstanceCreationItemDO,
    CommandRequestDO,
    CommandItemDO
)

class ConditionConverter(Converter):
    def to_entity(self, do: ConditionDO):
        return Condition(
            min_cpu_num=MinCPUNumber(do.min_cpu_num),
            max_cpu_num=MaxCPUNumber(do.max_cpu_num),
            min_memory_size=MinMemorySize(do.min_memory_size),
            max_memory_size=MaxMemorySize(do.max_memory_size),
            min_gpu_num=None if do.min_gpu_num is None else MinGPUNumber(do.min_gpu_num),
            max_gpu_num=None if do.max_gpu_num is None else MaxGPUNumber(do.max_gpu_num),
            min_gpu_memory_size=None if do.min_gpu_memory_size is None else MinGPUMemorySize(do.min_gpu_memory_size),
            max_gpu_memory_size=None if do.max_gpu_memory_size is None else MaxGPUMemorySize(do.max_gpu_memory_size)
        )
    
    def to_do(self, x: Condition):
        return ConditionDO(
            min_cpu_num=x.min_cpu_num.get_value(),
            max_cpu_num=x.max_cpu_num.get_value(),
            min_memory_size=x.min_memory_size.get_value(),
            max_memory_size=x.max_memory_size.get_value(),
            min_gpu_num=None if x.min_gpu_num is None else x.min_gpu_num.get_value(),
            max_gpu_num=None if x.max_gpu_num is None else x.max_gpu_num.get_value(),
            min_gpu_memory_size=None if x.min_gpu_memory_size is None else x.min_gpu_memory_size.get_value(),
            max_gpu_memory_size=None if x.max_gpu_memory_size is None else x.max_gpu_memory_size.get_value()
        )
condition_converter = ConditionConverter()

class InstanceUserSettingConverter(Converter):
    def to_entity(self, do: InstanceUserSettingDO):
        return InstanceUserSetting(
            name = InstanceName(do.name),
            password = None if do.password is None else Password(do.password),
            amount=Number(do.amount),
            image_id=None if do.image_id is None else ImageID(do.image_id),
            region_id=RegionID(do.region_id),
            internet_pay_type=None if do.internet_pay_type is None else Type(do.internet_pay_type),
            bandwidth_in=Bandwidth(do.bandwidth_in),
            bandwidth_out=Bandwidth(do.bandwidth_out),
            user_data=None if do.user_data is None else Data(do.user_data),
            disk_size=Size(do.disk_size),
            key_name=KeyName(do.key_name),
            exclude_instance_types=[InstanceTypeID(m) for m in do.exclude_instance_types],
            inner_connection=Bool(do.inner_connection)
        )
    def to_do(self, x:InstanceUserSetting):
        return InstanceUserSettingDO(
            name=x.name.get_value(),
            password=None if x.password is None else x.password.get_value(),
            amount=x.amount.get_value(),
            image_id=None if x.image_id is None else x.image_id.get_value(),
            region_id=x.region_id.get_value(),
            internet_pay_type=None if x.internet_pay_type is None else x.internet_pay_type.get_value(),
            bandwidth_in=x.bandwidth_in.get_value(),
            bandwidth_out=x.bandwidth_out.get_value(),
            user_data=None if x.user_data is None else x.user_data.get_value(),
            disk_size=x.disk_size.get_value(),
            key_name=x.key_name.get_value(),
            exclude_instance_types=[m.get_value() for m in x.exclude_instance_types],
            inner_connection=x.inner_connection.get_value()
        )
instance_user_setting_converter = InstanceUserSettingConverter()

class InstanceCreationRequestConverter(Converter):
    def to_entity(self, do: InstanceCreationRequestDO):
        return InstanceCreationRequest(
            instance_user_setting=instance_user_setting_converter.to_entity(do.instance_user_setting),
            condition=condition_converter.to_entity(do.condition),
            priority=InstanceCreationPriority(do.priority),
            timeout=Number(do.timeout)
        )
    def to_do(self, x: InstanceCreationRequest):
        return InstanceCreationRequestDO(
            instance_user_setting=instance_user_setting_converter.to_do(x.instance_user_setting),
            condition=condition_converter.to_do(x.condition),
            priority=x.priority.get_value(),
            timeout=x.timeout.get_value()
        )
instance_creation_request_converter = InstanceCreationRequestConverter()

class InstanceCreationItemConverter(Converter):
    def to_entity(self, do: InstanceCreationItemDO):
        return InstanceCreationItem(
            id=InstanceCreationID(do.id),
            instance_creation_request=None if do.instance_creation_request is None else instance_creation_request_converter.to_entity(do.instance_creation_request),
            creation_time=CreationTime(do.creation_time),
            status=InstanceCreationStatus(do.status),
            details=None if do.details is None else [instance_info_converter.to_entity(m) for m in do.details],
            entry_time=None if do.entry_time is None else DateTime(do.entry_time),
            exit_time=None if do.exit_time is None else DateTime(do.exit_time),
            exception=None if do.exception is None else InstanceException(do.exception),
            _life_time=Number(do._life_time)
        )
    def to_do(self, x: InstanceCreationItem):
        return InstanceCreationItemDO(
            id = x.id.get_value(),
            instance_creation_request = None if x.instance_creation_request is None else instance_creation_request_converter.to_do(x.instance_creation_request),
            creation_time=x.creation_time.get_value().replace(microsecond=0).isoformat(),
            status=x.status.get_value(),
            details=None if x.details is None else [instance_info_converter.to_do(m) for m in x.details],
            entry_time=None if x.entry_time is None else x.entry_time.get_value(),
            exit_time=None if x.exit_time is None else x.exit_time.get_value(),
            exception=None if x.exception is None else x.exception.get_value(),
            _life_time=x._life_time.get_value()
        )
instance_creation_item_converter = InstanceCreationItemConverter()

class BanInstanceTypeRequestConverter(Converter):
    def to_entity(self, do: BanInstanceTypeRequestDO):
        return BanInstanceTypeRequest(
            instance_type = InstanceTypeID(do.instance_type),
            region_id = RegionID(do.region_id),
            zone_id = ZoneID(do.zone_id),
            duration = None if do.duration is None else Number(do.duration)
        )
    def to_do(self, x: BanInstanceTypeRequest):
        return BanInstanceTypeRequestDO(
            instance_type = x.instance_type.get_value(),
            region_id = x.region_id.get_value(),
            zone_id = x.zone_id.get_value(),
            duration = None if x.duration is None else x.duration.get_value()
        )
ban_instance_type_request_converter = BanInstanceTypeRequestConverter()


class BannedInstanceTypeResponseConverter(Converter):
    def to_entity(self, do: BannedInstanceTypeResponseDO):
        return BannedInstanceTypeResponse(
            instance_types=[InstanceTypeID(m) for m in do.instance_types],
            region_id = RegionID(do.region_id),
            zone_id = ZoneID(do.zone_id)
        )
    
    def to_do(self, x: BannedInstanceTypeResponse):
        return BannedInstanceTypeResponseDO(
            instance_types=[m.get_value() for m in x.instance_types],
            region_id = x.region_id.get_value(),
            zone_id = x.zone_id.get_value()
        )
banned_instance_type_response_converter = BannedInstanceTypeResponseConverter()


class CommandSettingDetailConverter(Converter):
    def to_entity(self, do: CommandSettingDetailDO):
        return CommandSettingDetail(
            command=Command(do.command),
            module=CommandModule(do.module),
            retries=Number(do.retries),
            timeout=Number(do.timeout),
            delay=Number(do.delay)
        )
    def to_do(self, x: CommandSettingDetail):
        return CommandSettingDetailDO(
            command=x.command.get_value(),
            module=x.module.get_value(),
            retries=x.retries.get_value(),
            timeout=x.timeout.get_value(),
            delay=x.delay.get_value()
        )
command_setting_detail_converter = CommandSettingDetailConverter()

class CommandHostConverter(Converter):
    def to_entity(self, do: CommandHostDO):
        return CommandHost(
            ip=IP(do.ip),
            hostname=None if do.hostname is None else Name(do.hostname),
            port=Number(do.port),
            username=Name(do.username)
        )
    def to_do(self, x: CommandHost):
        return CommandHostDO(
            ip=x.ip.get_value(),
            hostname=None if x.hostname is None else x.hostname.get_value(),
            port=x.port.get_value(),
            username=x.username.get_value()
        )
command_host_converter = CommandHostConverter()

class CommandContextConverter(Converter):
    def to_entity(self, do: CommandContextDO):
        return CommandContext(
            connection=U(do.connection),
            module_path=Path(do.module_path),
            forks=Number(do.forks),
            timeout=Number(do.timeout),
            remote_user=Name(do.remote_user),
            ask_pass=Bool(do.ask_pass),
            ssh_extra_args=None if do.ssh_extra_args is None else U(do.ssh_extra_args),
            sftp_extra_args=None if do.sftp_extra_args is None else U(do.sftp_extra_args),
            scp_extra_args=None if do.scp_extra_args is None else U(do.scp_extra_args),
            ask_value_pass=Bool(do.ask_value_pass),
            listhosts=Bool(do.listhosts),
            listtasks=Bool(do.listtasks),
            listtags=Bool(do.listtags),
            syntax=Bool(do.syntax),
            ssh_common_args=U(do.ssh_common_args),
            become=None if do.become is None else U(do.become),
            become_method=None if do.become_method is None else U(do.become_method),
            become_user=Name(do.become_user),
            check=Bool(do.check),
            diff=Bool(do.diff),
            verbosity=Number(do.verbosity)
        )
    def to_do(self, x: CommandContext):
        return CommandContextDO(
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
command_context_converter = CommandContextConverter()

class CommandRequestConverter(Converter):
    def to_entity(self, do: CommandRequestDO):
        return CommandRequest(
            commands=[command_setting_detail_converter.to_entity(m) for m in do.commands],
            hosts=[command_host_converter.to_entity(m) for m in do.hosts],
            context=None if do.context is None else command_context_converter.to_entity(do.context),
            priority=CommandPriority(do.priority),
            timeout=Number(do.timeout),
        )
    
    def to_do(self, x: CommandRequest):
        return CommandRequestDO(
            commands=[command_setting_detail_converter.to_do(m) for m in x.commands],
            hosts=[command_host_converter.to_do(m) for m in x.hosts],
            context=None if x.context is None else command_context_converter.to_do(x.context),
            priority=x.priority.get_value(),
            timeout=x.timeout.get_value(),
        )
command_request_converter = CommandRequestConverter()

class CommandResponseConverter(Converter):
    def to_entity(self, do: CommandResponseDO):
        return CommandResponse(
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
    def to_do(self, x: CommandResponse):
        return CommandResponseDO(
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
command_response_converter = CommandResponseConverter()

class CommandItemConverter(Converter):
    def to_entity(self, do: CommandItemDO):
        return CommandItem(
            id=CommandID(do.id),
            command_request=None if do.command_request is None else command_request_converter.to_entity(do.command_request),
            creation_time=CreationTime(do.creation_time),
            status=CommandStatus(do.status),
            details=None if do.details is None else [command_response_converter.to_entity(m) for m in do.details],
            exception=None if do.exception is None else CommandException(do.exception),
            _life_time=Number(do._life_time)
        )
    def to_do(self, x: CommandItem):
        return CommandItemDO(
            id=x.id.get_value(),
            command_request=None if x.command_request is None else command_request_converter.to_do(x.command_request),
            creation_time=x.creation_time.get_value().replace(microsecond=0).isoformat(),
            status=x.status.get_value(),
            details=None if x.details is None else [command_response_converter.to_do(m) for m in x.details],
            exception=None if x.exception is None else x.exception.get_value(),
            _life_time=x._life_time.get_value()
        )
command_item_converter = CommandItemConverter()

class InstanceInfoConverter(Converter):
    @Converter.convert_none
    def to_entity(self, do: InstanceInfoDO):
        return InstanceInfo(
            id = InstanceInfoID(do.id),
            instance_type=InstanceTypeID(do.instance_type),
            create_time=DateTime(do.create_time),
            name=Name(do.name),
            hostname=Name(do.hostname),
            pay_type=Type(do.pay_type),
            public_ip=[IP(ip) for ip in do.public_ip],
            private_ip=None if do.private_ip is None else IP(do.private_ip),
            os_name=Name(do.os_name),
            price=Price(do.price),
            image_id=ImageID(do.image_id),
            region_id=RegionID(do.region_id),
            zone_id=ZoneID(do.zone_id),
            internet_pay_type=Type(do.internet_pay_type),
            bandwidth_in=Bandwidth(do.bandwidth_in),
            bandwidth_out=Bandwidth(do.bandwidth_out),
            security_group_id=[SecurityGroupID(id) for id in do.security_group_id],
            instance_expired_time=DateTime(do.instance_expired_time),
            auto_release_time=DateTime(do.auto_release_time),
            status = InstanceStatus(do.status),
            key_name = KeyName(do.key_name)
        )
    def to_do(self, x: InstanceInfo):
        return InstanceInfoDO(
            id = x.id.get_value(),
            instance_type = x.instance_type.get_value(),
            create_time = x.create_time.get_value(),
            name = x.name.get_value(),
            hostname = x.name.get_value(),
            pay_type = x.pay_type.get_value(),
            public_ip = [m.get_value() for m in x.public_ip],
            private_ip = None if x.private_ip is None else x.private_ip.get_value(),
            os_name = x.os_name.get_value(),
            price = x.price.get_value(),
            image_id = x.image_id.get_value(),
            region_id = x.region_id.get_value(),
            zone_id = x.zone_id.get_value(),
            internet_pay_type=x.internet_pay_type.get_value(),
            bandwidth_in = x.bandwidth_in.get_value(),
            bandwidth_out = x.bandwidth_out.get_value(),
            security_group_id = [m.get_value() for m in x.security_group_id],
            instance_expired_time = x.instance_expired_time.get_value(),
            auto_release_time = x.auto_release_time.get_value(),
            status = x.status.get_value(),
            key_name = x.key_name.get_value()
        )
instance_info_converter = InstanceInfoConverter()

class InstanceSettingConverter(Converter):
    @Converter.convert_none
    def to_do(self, x: InstanceSetting):
        return InstanceSettingDO(
            region_id = x.region_id.get_value() ,
            zone_id = x.zone_id.get_value(),
            spot_price=x.spot_price.get_value(),
            instance_type=x.instance_type.get_value(),
            amount=x.amount.get_value(),
            image_id=None if x.image_id is None else x.image_id.get_value(),
            instance_name= x.name.get_value() ,
            password=None if x.password is None else x.password.get_value(),
            disk_size=x.disk_size.get_value(),
            bandwidth_in=x.bandwidth_in.get_value(),
            bandwidth_out=x.bandwidth_out.get_value(),
            user_data=None if x.user_data is None else x.user_data.get_value(),
            internet_pay_type=None if x.internet_pay_type is None else x.internet_pay_type.get_value(),
            security_group_id=x.security_group_id.get_value(),
            key_name=x.key_name.get_value()
        )
instance_setting_converter = InstanceSettingConverter()

class DNSRecordConverter(Converter):
    def to_entity(self, do: DNSRecordDO):
        return DNSRecord(
            domain_name = DomainName(do.domain_name),
            subdomain = Subdomain(do.subdomain),
            value = Value(do.value),
            id = ID(do.id),
            weight = Weight(do.weight),
            dns_type = DNSType(do.dns_type),
            ttl = Number(do.ttl),
            priority = Priority(do.priority),
            line = Line(do.line)
        )
    def to_do(self, x: DNSRecord):
        return DNSRecordDO(
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
dns_record_converter = DNSRecordConverter()
