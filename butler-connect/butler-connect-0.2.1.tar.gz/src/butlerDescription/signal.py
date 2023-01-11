   
from marshmallow import Schema, fields,post_load
from datetime import datetime

class SignalType():
    unDef = 'undef'
    temperature = 'temperature'
    setTemperature = 'set_temperature'
    humidity = 'humidity'
    windowIsOpen = 'window_is_open'
    presence = 'presence'
    motion = 'motion'
    illumination = 'illumination'
    actuatorValue = 'actuator_value'
    


class Signal():
    def __init__(self,type,component=0,group=0,ioDevice="",ioSignal="",parameter={},timestamp=datetime.now(),value = 0.0,valueStr = ""):
        self.timestamp  = timestamp
        self.component  = int(component)
        self.group      = int(group)
        self.ioDevice   = ioDevice
        self.ioSignal   = ioSignal
        self.type       = type
        self.value      = float(value)
        self.valueStr   = str(valueStr)
        
    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)
    def __str__(self) -> str:
        return f'component={self.component}, group={self.group}, ioDevice={self.ioDevice}, ioSignal={self.ioSignal}, type={self.type}, value={self.value}, valueStr={self.valueStr}, timestmap={self.timestamp}'        

class SignalSchmea(Schema):
    timestamp = fields.DateTime(required=True)
    component = fields.Int()
    group = fields.Int()
    ioDevice = fields.Str()
    ioSignal = fields.Str()
    type = fields.Str()
    value = fields.Float()
    valueStr = fields.Str()
    
    @post_load
    def make_control(self, data, **kwargs):
        return Signal(**data)