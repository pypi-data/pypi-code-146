import sys, datetime, string
from ipaddress import ip_address
from dateutil import parser
from ddd_objects.domain.value_obj import ValueObject, ID, ExpiredValueObject
from ddd_objects.domain.exception import ParameterError
python_version_minor = sys.version_info.minor

class U(ValueObject):
    pass

class CreationTime(ValueObject):
    def __init__(self, value=None):
        if value is None:
            value = datetime.datetime.utcnow()
        elif isinstance(value, str):
            value = parser.parse(value)
        super().__init__(value)
    def __str__(self) -> str:
        return self.value.replace(microsecond=0).isoformat()

class Name(ValueObject):
    pass

class InstanceName(Name):
    def __init__(self, value) -> None:
        if not isinstance(value, str):
            raise ParameterError('Instance name must be string!')
        if not value:
            raise ParameterError('Instance name cannot be empty!')
        if value[0] not in string.ascii_letters:
            raise ParameterError('First letter of the instance name must be letter')
        super().__init__(value)

class KeyName(Name):
    def __init__(self, value) -> None:
        if value not in ['ansible', 'ansible-test']:
            raise ValueError('Invalid value for RSA key name')
        super().__init__(value)

class InstanceCreationID(ID):
    pass

class CommandID(ID):
    pass

class ZoneID(ID):
    pass

class InstanceTypeID(ID):
    pass

class ZoneName(Name):
    pass

class RegionID(ExpiredValueObject):
    def __init__(self, value=None):
        super().__init__(value, None)

class RegionName(Name):
    pass

class Endpoint(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Number(ValueObject):
    pass

class CPUNumber(Number):
    pass
        
GPUNumber = MinCPUNumber = MinGPUNumber = CPUNumber

class MaxCPUNumber(Number):
    pass
MaxGPUNumber = MaxCPUNumber

class Data(ValueObject):
    pass

class Size(ValueObject):
    pass

class MemorySize(ValueObject):
    pass
    
GPUMemorySize = MinGPUMemorySize = MinMemorySize = MemorySize

class MaxMemorySize(MemorySize):
    pass
MaxGPUMemorySize = MaxMemorySize

class GPUType(ValueObject):
    pass

class Price(ValueObject):
    pass

class DateTime(ValueObject):
    pass

class DeltaTime(ValueObject):
    pass

class Status(ValueObject):
    pass

class InstanceCreationStatus(ValueObject):
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
    
    def is_succeed(self):
        return self.value=='Succeed'
    
    def is_failed(self):
        return self.value=='Failed'

    def is_sent(self):
        return self.value=='Sent'

    def is_created(self):
        return self.value=='Created'

    def is_pending(self):
        return self.value=='Pending'

    def is_deleted(self):
        return self.value=='Deleted'

class CommandStatus(ValueObject):
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

class SecurityGroupID(ExpiredValueObject):
    def __init__(self, value=None):
        if not isinstance(value, str):
            raise ParameterError(f'ID should be a string, but got {type(value)}')
        super().__init__(value, None)

class InstanceInfoID(ID):
    pass

class Type(ValueObject):
    pass

class IP(ValueObject):
    def __init__(self, value) -> None:
        value = value.strip()
        if not self.is_ip(value):
            raise ParameterError('Input parameter is not a ip')
        self.value = value

    def is_private(self, ip)->bool:
        return ip_address(ip).is_private

    def is_ip(self, ip)->bool:
        try:
            ip_address(ip)
            return True
        except:
            return False
        

class ImageID(ID):
    pass

class Bandwidth(ValueObject):
    pass

class InstanceStatus(ValueObject):
    def is_running(self):
        return self.value=='Running'

class Password(ValueObject):
    def __init__(self, value) -> None:
        if len(value)<8:
            raise ParameterError('Password should be longer than 7')
        elif len(value)>30:
            raise ParameterError('Password should be shorter than 31')
        n_uletter, n_lletter, n_number =0, 0, 0
        for c in value:
            if c.islower():
                n_lletter += 1
            elif c.isupper():
                n_uletter += 1
            elif c.isdigit():
                n_number += 1
        if n_uletter==0 or n_lletter==0 or n_number==0:
            raise ParameterError('Password should contain a lower letter, a upper letter and a number!')
        super().__init__(value)

class InstanceID(ID):
    pass

class Key(ValueObject):
    pass

class Path(ValueObject):
    pass

class Bool(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Output(ValueObject):
    pass

class DomainName(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Subdomain(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Value(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class DnsType(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Weight(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Priority(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class CommandPriority(ValueObject):
    def __init__(self, value):
        if not isinstance(value, int):
            raise ParameterError(f'Value of CommandPriority should be int, not {type(value)}')
        if value<1 or value>5:
            raise ParameterError(f'Value of CommandPrority should be greater than 0 and less than 6')
        super().__init__(value)

    def __gt__(self, other):
        return self.value>other.value

    def __lt__(self, other):
        return self.value<other.value

    def __eq__(self, other):
        return self.value==other.value

class InstanceCreationPriority(ValueObject):
    def __init__(self, value):
        if not isinstance(value, int):
            raise ParameterError(f'Value of InstanceCreationPriority should be int, not {type(value)}')
        if value<1 or value>5:
            raise ParameterError(f'Value of InstanceCreationPrority should be greater than 0 and less than 6')
        super().__init__(value)
    
    def __gt__(self, other):
        return self.value>other.value

    def __lt__(self, other):
        return self.value<other.value

    def __eq__(self, other):
        return self.value==other.value

class Line(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class DNSType(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class ID(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Port(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class String(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Text(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class BucketName(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class VersionID(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class VersionCreationTime(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class Command(ExpiredValueObject):
    def __init__(self, value):
        super().__init__(value, None)

class CommandModule(ValueObject):
    pass

class CommandResponseStatus(ValueObject):
    def is_succeed(self)->bool:
        return self.value=='succeed'
    def is_failed(self)->bool:
        return self.value=='failed'
    def is_unreachable(self)->bool:
        return self.value=='unreachable'
    def set_succeed(self):
        self.value='succeed'
    def set_failed(self):
        self.value='failed'
    def set_unreachable(self):
        self.value='unreachable'

class InstanceException(ValueObject):
    pass

class CommandException(ValueObject):
    pass

