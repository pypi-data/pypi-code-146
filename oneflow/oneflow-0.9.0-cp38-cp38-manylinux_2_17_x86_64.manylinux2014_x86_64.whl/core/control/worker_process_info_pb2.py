# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: oneflow/core/control/worker_process_info.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='oneflow/core/control/worker_process_info.proto',
  package='oneflow',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n.oneflow/core/control/worker_process_info.proto\x12\x07oneflow\"=\n\x11WorkerProcessInfo\x12\x0c\n\x04rank\x18\x01 \x02(\x03\x12\x0c\n\x04port\x18\x02 \x02(\x03\x12\x0c\n\x04host\x18\x03 \x01(\t')
)




_WORKERPROCESSINFO = _descriptor.Descriptor(
  name='WorkerProcessInfo',
  full_name='oneflow.WorkerProcessInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rank', full_name='oneflow.WorkerProcessInfo.rank', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='oneflow.WorkerProcessInfo.port', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host', full_name='oneflow.WorkerProcessInfo.host', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=59,
  serialized_end=120,
)

DESCRIPTOR.message_types_by_name['WorkerProcessInfo'] = _WORKERPROCESSINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WorkerProcessInfo = _reflection.GeneratedProtocolMessageType('WorkerProcessInfo', (_message.Message,), {
  'DESCRIPTOR' : _WORKERPROCESSINFO,
  '__module__' : 'oneflow.core.control.worker_process_info_pb2'
  # @@protoc_insertion_point(class_scope:oneflow.WorkerProcessInfo)
  })
_sym_db.RegisterMessage(WorkerProcessInfo)


# @@protoc_insertion_point(module_scope)
