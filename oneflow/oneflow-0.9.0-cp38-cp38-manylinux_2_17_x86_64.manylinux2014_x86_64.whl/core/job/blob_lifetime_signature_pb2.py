# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: oneflow/core/job/blob_lifetime_signature.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='oneflow/core/job/blob_lifetime_signature.proto',
  package='oneflow',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n.oneflow/core/job/blob_lifetime_signature.proto\x12\x07oneflow\"\xad\x01\n\x15\x42lobLastUsedSignature\x12X\n\x17\x62n_in_op2blob_last_used\x18\x01 \x03(\x0b\x32\x37.oneflow.BlobLastUsedSignature.BnInOp2blobLastUsedEntry\x1a:\n\x18\x42nInOp2blobLastUsedEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x08:\x02\x38\x01\"\xc1\x01\n\x19\x42lobBackwardUsedSignature\x12\x64\n\x1b\x62n_in_op2blob_backward_used\x18\x01 \x03(\x0b\x32?.oneflow.BlobBackwardUsedSignature.BnInOp2blobBackwardUsedEntry\x1a>\n\x1c\x42nInOp2blobBackwardUsedEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x08:\x02\x38\x01')
)




_BLOBLASTUSEDSIGNATURE_BNINOP2BLOBLASTUSEDENTRY = _descriptor.Descriptor(
  name='BnInOp2blobLastUsedEntry',
  full_name='oneflow.BlobLastUsedSignature.BnInOp2blobLastUsedEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='oneflow.BlobLastUsedSignature.BnInOp2blobLastUsedEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='oneflow.BlobLastUsedSignature.BnInOp2blobLastUsedEntry.value', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=175,
  serialized_end=233,
)

_BLOBLASTUSEDSIGNATURE = _descriptor.Descriptor(
  name='BlobLastUsedSignature',
  full_name='oneflow.BlobLastUsedSignature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bn_in_op2blob_last_used', full_name='oneflow.BlobLastUsedSignature.bn_in_op2blob_last_used', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_BLOBLASTUSEDSIGNATURE_BNINOP2BLOBLASTUSEDENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=233,
)


_BLOBBACKWARDUSEDSIGNATURE_BNINOP2BLOBBACKWARDUSEDENTRY = _descriptor.Descriptor(
  name='BnInOp2blobBackwardUsedEntry',
  full_name='oneflow.BlobBackwardUsedSignature.BnInOp2blobBackwardUsedEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='oneflow.BlobBackwardUsedSignature.BnInOp2blobBackwardUsedEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='oneflow.BlobBackwardUsedSignature.BnInOp2blobBackwardUsedEntry.value', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=367,
  serialized_end=429,
)

_BLOBBACKWARDUSEDSIGNATURE = _descriptor.Descriptor(
  name='BlobBackwardUsedSignature',
  full_name='oneflow.BlobBackwardUsedSignature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bn_in_op2blob_backward_used', full_name='oneflow.BlobBackwardUsedSignature.bn_in_op2blob_backward_used', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_BLOBBACKWARDUSEDSIGNATURE_BNINOP2BLOBBACKWARDUSEDENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=236,
  serialized_end=429,
)

_BLOBLASTUSEDSIGNATURE_BNINOP2BLOBLASTUSEDENTRY.containing_type = _BLOBLASTUSEDSIGNATURE
_BLOBLASTUSEDSIGNATURE.fields_by_name['bn_in_op2blob_last_used'].message_type = _BLOBLASTUSEDSIGNATURE_BNINOP2BLOBLASTUSEDENTRY
_BLOBBACKWARDUSEDSIGNATURE_BNINOP2BLOBBACKWARDUSEDENTRY.containing_type = _BLOBBACKWARDUSEDSIGNATURE
_BLOBBACKWARDUSEDSIGNATURE.fields_by_name['bn_in_op2blob_backward_used'].message_type = _BLOBBACKWARDUSEDSIGNATURE_BNINOP2BLOBBACKWARDUSEDENTRY
DESCRIPTOR.message_types_by_name['BlobLastUsedSignature'] = _BLOBLASTUSEDSIGNATURE
DESCRIPTOR.message_types_by_name['BlobBackwardUsedSignature'] = _BLOBBACKWARDUSEDSIGNATURE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BlobLastUsedSignature = _reflection.GeneratedProtocolMessageType('BlobLastUsedSignature', (_message.Message,), {

  'BnInOp2blobLastUsedEntry' : _reflection.GeneratedProtocolMessageType('BnInOp2blobLastUsedEntry', (_message.Message,), {
    'DESCRIPTOR' : _BLOBLASTUSEDSIGNATURE_BNINOP2BLOBLASTUSEDENTRY,
    '__module__' : 'oneflow.core.job.blob_lifetime_signature_pb2'
    # @@protoc_insertion_point(class_scope:oneflow.BlobLastUsedSignature.BnInOp2blobLastUsedEntry)
    })
  ,
  'DESCRIPTOR' : _BLOBLASTUSEDSIGNATURE,
  '__module__' : 'oneflow.core.job.blob_lifetime_signature_pb2'
  # @@protoc_insertion_point(class_scope:oneflow.BlobLastUsedSignature)
  })
_sym_db.RegisterMessage(BlobLastUsedSignature)
_sym_db.RegisterMessage(BlobLastUsedSignature.BnInOp2blobLastUsedEntry)

BlobBackwardUsedSignature = _reflection.GeneratedProtocolMessageType('BlobBackwardUsedSignature', (_message.Message,), {

  'BnInOp2blobBackwardUsedEntry' : _reflection.GeneratedProtocolMessageType('BnInOp2blobBackwardUsedEntry', (_message.Message,), {
    'DESCRIPTOR' : _BLOBBACKWARDUSEDSIGNATURE_BNINOP2BLOBBACKWARDUSEDENTRY,
    '__module__' : 'oneflow.core.job.blob_lifetime_signature_pb2'
    # @@protoc_insertion_point(class_scope:oneflow.BlobBackwardUsedSignature.BnInOp2blobBackwardUsedEntry)
    })
  ,
  'DESCRIPTOR' : _BLOBBACKWARDUSEDSIGNATURE,
  '__module__' : 'oneflow.core.job.blob_lifetime_signature_pb2'
  # @@protoc_insertion_point(class_scope:oneflow.BlobBackwardUsedSignature)
  })
_sym_db.RegisterMessage(BlobBackwardUsedSignature)
_sym_db.RegisterMessage(BlobBackwardUsedSignature.BnInOp2blobBackwardUsedEntry)


_BLOBLASTUSEDSIGNATURE_BNINOP2BLOBLASTUSEDENTRY._options = None
_BLOBBACKWARDUSEDSIGNATURE_BNINOP2BLOBBACKWARDUSEDENTRY._options = None
# @@protoc_insertion_point(module_scope)
