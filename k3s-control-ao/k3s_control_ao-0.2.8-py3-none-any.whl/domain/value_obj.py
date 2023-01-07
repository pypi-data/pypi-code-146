import sys, base64, os, datetime
from dateutil import parser
from ddd_objects.domain.value_obj import ExpiredValueObject, ValueObject
from ddd_objects.domain.exception import FormatError, ValueError, ParameterError
from vpc_control_ao.domain.value_obj import CommandID, CommandPriority
from vpc_control_ao.domain.value_obj_ext import PipelineContext
python_version_minor = sys.version_info.minor

class Number(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class InstanceAmount(Number):
    def __init__(self, value):
        if not isinstance(value, int) or value<1:
            raise ValueError('Value for InstanceAmount is invalid.')
        super().__init__(value)

class NodeAmount(Number):
    def __init__(self, value):
        if not isinstance(value, int) or value<1:
            raise ValueError('Value for NodeAmount is invalid.')
        super().__init__(value)

class RestartNumber(Number):
    def __init__(self, value):
        if isinstance(value, str):
            parts = value.split(' ')
            value = parts[0]
        super().__init__(value)

class Size(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ID(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Status(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class SecurityGroupID(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class InstanceType(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Name(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)
    def match(self, s):
        return self.value==s
    def add(self, s):
        self.value += s
        return self
    def startswith(self, s):
        return self.value.startswith(s)

class ServiceAccountName(Name):
    def __init__(self, value):
        super().__init__(value)

class Hostname(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Price(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ImageID(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class RegionID(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ZoneID(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class InternetPayType(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class PayType(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)
    
class ConfigMapType(ValueObject):
    def __init__(self, value):
        if value not in ['property', 'file']:
            raise ParameterError('Invaid parameter for ConfigMapType')
        self.value = value
    def is_property(self):
        return self.value=='property'
    def is_file(self):
        return self.value=='file'

class IP(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class BandWidth(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class DateTime(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Password(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class YamlString(ValueObject):
    def __init__(self, value):
        if isinstance(value, int) or isinstance(value, float) \
            or (isinstance(value, str) and value.isdigit()):
            value = f'"{value}"'
        elif not isinstance(value, str):
            raise ValueError(f'Type {type(value)} is not supported')
        super().__init__(value)

class Base64String(ExpiredValueObject):
    def __init__(self, value):
        value = str(base64.b64encode(value.encode('utf-8')),"utf-8")
        super().__init__(value, None)

class Data(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Type(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)
    def match(self, value):
        return value==self.value

class Command(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Username(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Port(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Bool(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Output(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class InstanceID(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class InstanceName(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Endpoint(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Path(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)
    def get_base_name(self)->str:
        return os.path.basename(self.value)

class NodeType(Type):
    def __init__(self, value):
        super().__init__(value)
    def is_master(self):
        return self.value=='master'
    def match(self, value):
        return self.value==value

class NodeName(Name):
    def __init__(self, value):
        super().__init__(value)
    def get_cluster_name(self):
        cluster_name = self.value.split('-')[0]
        if cluster_name[-1] == '*':
            cluster_name = cluster_name[:-1]
        return Name(cluster_name)
    def get_master_name(self):
        master_name = self.value.split('-')[0]+'-master'
        return Name(master_name)
    def get_node_type(self):
        parts = self.value.split('-')
        if parts[-1].isdigit():
            parts = parts[1:-2]
        else:
            parts = parts[1:-1]
        return NodeType('-'.join(parts))
    def get_type_group_name(self):
        parts = self.value.split('-')[:-1]
        type_group_name = '-'.join(parts)
        return Name(type_group_name)
    def check_name(self, node_type:NodeType):
        parts = self.value.split('-')
        main_part = '-'.join(parts[1:])
        if not main_part.startswith(node_type.get_value()):
            raise FormatError('Wrong format of node name')

class NodeStatus(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)
    def is_ready(self):
        return 'NotReady' not in self.value
    def is_schedulable(self):
        return 'SchedulingDisabled' not in self.value

class Token(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class InstanceStatus(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class K3SRunTime(ValueObject):
    def __init__(self, value) -> None:
        if isinstance(value, float):
            self.value = value
        elif isinstance(value, datetime.timedelta):
            self.value = value.total_seconds()
        else:
            self.value = self._extract(value)
    
    def _extract(self, value):
        day, value = value.split('d') if 'd' in value else (0, value)
        hour, value = value.split('h') if 'h' in value else (0, value)
        minute, value = value.split('m') if 'm' in value else (0, value)
        second, value = value.split('s') if 's' in value else (0, value)
        if value:
            second = value
        day, hour, minute, second = float(day), float(hour), float(minute), float(second)
        return ((day*24+hour)*60+minute)*60+second
    
    def total_seconds(self)->float:
        return self.value

class Version(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Key(ValueObject):
    pass

class Value(ValueObject):
    pass

class GPUType(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class InstanceStatusCategory(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class InstanceTypeStatus(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class InstanceTypeStatusCategory(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class NodeLabel(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class InstanceIf(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Usage(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Info(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class TimeInterval(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Label(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ServiceType(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class PodStatus(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)
    
    def is_pending(self):
        return self.value=='Pending'

    def is_running(self):
        return self.value=='Running'

    def is_succeed(self):
        return self.value=='Succeed'

    def is_failed(self):
        return self.value=='Failed'


class DockerImageName(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ContainerEnvDict(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class RestartPolicy(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ContainerCommand(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ContainerArgs(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ImagePullPolicy(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class PathMode(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class EnvVarSourceType(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class VolumeType(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class VolumeName(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class HTTPHeader(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class NetworkScheme(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Protocol(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class NodeSelectorDict(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class DNSPolicy(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class LabelDict(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class PodResourceDict(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class MatchLabels(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class LabelSelectorOperator(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class JobStatus(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Integer(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Provisioner(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ReclaimPolicy(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class VolumeBindingMode(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Server(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ReadOnly(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class FSType(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Operator(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class StorageClassName(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Capacity(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class AccessMode(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class PersistentVolumeReclaimPolicy(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class AcceessMode(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ResourceDict(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class NodeCreationItemID(ID):
    pass

class CreationTime(ValueObject):
    def __init__(self, value=None):
        if value is None:
            value = datetime.datetime.utcnow()
        elif isinstance(value, str):
            value = parser.parse(value)
        else:
            print(value, type(value))
        super().__init__(value)
    def __str__(self) -> str:
        return self.value.replace(microsecond=0).isoformat()

class NodeCreationStatus(ValueObject):
    def __init__(self, value=None) -> None:
        value = value or 'Pending'
        self.value = value
        self._set_changed_time()

    def _set_changed_time(self):
        self.changed_time = datetime.datetime.utcnow()

    def set_sent(self):
        self.value = 'Sent'
        self._set_changed_time()

    def set_created(self):
        self.value = 'Created'
        self._set_changed_time()

    def set_deleted(self):
        self.value = 'Deleted'
        self._set_changed_time()

    def set_succeed(self):
        self.value = 'Succeed'
        self._set_changed_time()

    def set_failed(self):
        self.value = 'Failed'
        self._set_changed_time()

    def is_sent(self):
        return self.value=='Sent'

    def is_created(self):
        return self.value=='Created'

    def is_pending(self):
        return self.value=='Pending'

    def is_deleted(self):
        return self.value=='Deleted'

    def is_succeed(self):
        return self.value=='Succeed'

    def is_failed(self):
        return self.value=='Failed'

class AccountID(ValueObject):
    pass

class AccountSecret(ValueObject):
    pass

class ServerEndpoint(ValueObject):
    pass

class DataBucket(ValueObject):
    pass

class DatapipePath(ValueObject):
    pass

class DatapipeRequestID(ValueObject):
    pass

class Text(ValueObject):
    pass