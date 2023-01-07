# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: oneflow/core/operator/op_attribute.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from oneflow.core.register import logical_blob_id_pb2 as oneflow_dot_core_dot_register_dot_logical__blob__id__pb2
from oneflow.core.register import blob_desc_pb2 as oneflow_dot_core_dot_register_dot_blob__desc__pb2
from oneflow.core.operator import op_conf_pb2 as oneflow_dot_core_dot_operator_dot_op__conf__pb2
from oneflow.core.operator import arg_modifier_signature_pb2 as oneflow_dot_core_dot_operator_dot_arg__modifier__signature__pb2
from oneflow.core.job import sbp_parallel_pb2 as oneflow_dot_core_dot_job_dot_sbp__parallel__pb2
from oneflow.core.job import local_parallel_pb2 as oneflow_dot_core_dot_job_dot_local__parallel__pb2
from oneflow.core.job import blob_lifetime_signature_pb2 as oneflow_dot_core_dot_job_dot_blob__lifetime__signature__pb2
from oneflow.core.job import parallel_signature_pb2 as oneflow_dot_core_dot_job_dot_parallel__signature__pb2
from oneflow.core.job import parallel_conf_signature_pb2 as oneflow_dot_core_dot_job_dot_parallel__conf__signature__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='oneflow/core/operator/op_attribute.proto',
  package='oneflow',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n(oneflow/core/operator/op_attribute.proto\x12\x07oneflow\x1a+oneflow/core/register/logical_blob_id.proto\x1a%oneflow/core/register/blob_desc.proto\x1a#oneflow/core/operator/op_conf.proto\x1a\x32oneflow/core/operator/arg_modifier_signature.proto\x1a#oneflow/core/job/sbp_parallel.proto\x1a%oneflow/core/job/local_parallel.proto\x1a.oneflow/core/job/blob_lifetime_signature.proto\x1a)oneflow/core/job/parallel_signature.proto\x1a.oneflow/core/job/parallel_conf_signature.proto\"\xb3\x05\n\x0bOpAttribute\x12\x11\n\tinput_bns\x18\x01 \x03(\t\x12\x12\n\noutput_bns\x18\x02 \x03(\t\x12\x0f\n\x07tmp_bns\x18\x03 \x03(\t\x12&\n\x07op_conf\x18\x32 \x02(\x0b\x32\x15.oneflow.OperatorConf\x12,\n\rarg_signature\x18\x64 \x02(\x0b\x32\x15.oneflow.ArgSignature\x12=\n\x16\x61rg_modifier_signature\x18\x65 \x02(\x0b\x32\x1d.oneflow.ArgModifierSignature\x12@\n\x18\x62lob_last_used_signature\x18\x66 \x01(\x0b\x32\x1e.oneflow.BlobLastUsedSignature\x12H\n\x1c\x62lob_backward_used_signature\x18g \x01(\x0b\x32\".oneflow.BlobBackwardUsedSignature\x12,\n\rsbp_signature\x18h \x01(\x0b\x32\x15.oneflow.SbpSignature\x12\x30\n\x0flocal_signature\x18i \x01(\x0b\x32\x17.oneflow.LocalSignature\x12?\n\x1blogical_blob_desc_signature\x18j \x01(\x0b\x32\x1a.oneflow.BlobDescSignature\x12\x36\n\x12parallel_signature\x18l \x01(\x0b\x32\x1a.oneflow.ParallelSignature\x12?\n\x17parallel_conf_signature\x18m \x01(\x0b\x32\x1e.oneflow.ParallelConfSignature\x12\x31\n\x10nd_sbp_signature\x18n \x01(\x0b\x32\x17.oneflow.NdSbpSignature\"=\n\x0fOpAttributeList\x12*\n\x0cop_attribute\x18\x01 \x03(\x0b\x32\x14.oneflow.OpAttribute')
  ,
  dependencies=[oneflow_dot_core_dot_register_dot_logical__blob__id__pb2.DESCRIPTOR,oneflow_dot_core_dot_register_dot_blob__desc__pb2.DESCRIPTOR,oneflow_dot_core_dot_operator_dot_op__conf__pb2.DESCRIPTOR,oneflow_dot_core_dot_operator_dot_arg__modifier__signature__pb2.DESCRIPTOR,oneflow_dot_core_dot_job_dot_sbp__parallel__pb2.DESCRIPTOR,oneflow_dot_core_dot_job_dot_local__parallel__pb2.DESCRIPTOR,oneflow_dot_core_dot_job_dot_blob__lifetime__signature__pb2.DESCRIPTOR,oneflow_dot_core_dot_job_dot_parallel__signature__pb2.DESCRIPTOR,oneflow_dot_core_dot_job_dot_parallel__conf__signature__pb2.DESCRIPTOR,])




_OPATTRIBUTE = _descriptor.Descriptor(
  name='OpAttribute',
  full_name='oneflow.OpAttribute',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='input_bns', full_name='oneflow.OpAttribute.input_bns', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output_bns', full_name='oneflow.OpAttribute.output_bns', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tmp_bns', full_name='oneflow.OpAttribute.tmp_bns', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='op_conf', full_name='oneflow.OpAttribute.op_conf', index=3,
      number=50, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arg_signature', full_name='oneflow.OpAttribute.arg_signature', index=4,
      number=100, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arg_modifier_signature', full_name='oneflow.OpAttribute.arg_modifier_signature', index=5,
      number=101, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='blob_last_used_signature', full_name='oneflow.OpAttribute.blob_last_used_signature', index=6,
      number=102, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='blob_backward_used_signature', full_name='oneflow.OpAttribute.blob_backward_used_signature', index=7,
      number=103, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sbp_signature', full_name='oneflow.OpAttribute.sbp_signature', index=8,
      number=104, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='local_signature', full_name='oneflow.OpAttribute.local_signature', index=9,
      number=105, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='logical_blob_desc_signature', full_name='oneflow.OpAttribute.logical_blob_desc_signature', index=10,
      number=106, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parallel_signature', full_name='oneflow.OpAttribute.parallel_signature', index=11,
      number=108, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parallel_conf_signature', full_name='oneflow.OpAttribute.parallel_conf_signature', index=12,
      number=109, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nd_sbp_signature', full_name='oneflow.OpAttribute.nd_sbp_signature', index=13,
      number=110, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=442,
  serialized_end=1133,
)


_OPATTRIBUTELIST = _descriptor.Descriptor(
  name='OpAttributeList',
  full_name='oneflow.OpAttributeList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='op_attribute', full_name='oneflow.OpAttributeList.op_attribute', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1135,
  serialized_end=1196,
)

_OPATTRIBUTE.fields_by_name['op_conf'].message_type = oneflow_dot_core_dot_operator_dot_op__conf__pb2._OPERATORCONF
_OPATTRIBUTE.fields_by_name['arg_signature'].message_type = oneflow_dot_core_dot_register_dot_logical__blob__id__pb2._ARGSIGNATURE
_OPATTRIBUTE.fields_by_name['arg_modifier_signature'].message_type = oneflow_dot_core_dot_operator_dot_arg__modifier__signature__pb2._ARGMODIFIERSIGNATURE
_OPATTRIBUTE.fields_by_name['blob_last_used_signature'].message_type = oneflow_dot_core_dot_job_dot_blob__lifetime__signature__pb2._BLOBLASTUSEDSIGNATURE
_OPATTRIBUTE.fields_by_name['blob_backward_used_signature'].message_type = oneflow_dot_core_dot_job_dot_blob__lifetime__signature__pb2._BLOBBACKWARDUSEDSIGNATURE
_OPATTRIBUTE.fields_by_name['sbp_signature'].message_type = oneflow_dot_core_dot_job_dot_sbp__parallel__pb2._SBPSIGNATURE
_OPATTRIBUTE.fields_by_name['local_signature'].message_type = oneflow_dot_core_dot_job_dot_local__parallel__pb2._LOCALSIGNATURE
_OPATTRIBUTE.fields_by_name['logical_blob_desc_signature'].message_type = oneflow_dot_core_dot_register_dot_blob__desc__pb2._BLOBDESCSIGNATURE
_OPATTRIBUTE.fields_by_name['parallel_signature'].message_type = oneflow_dot_core_dot_job_dot_parallel__signature__pb2._PARALLELSIGNATURE
_OPATTRIBUTE.fields_by_name['parallel_conf_signature'].message_type = oneflow_dot_core_dot_job_dot_parallel__conf__signature__pb2._PARALLELCONFSIGNATURE
_OPATTRIBUTE.fields_by_name['nd_sbp_signature'].message_type = oneflow_dot_core_dot_job_dot_sbp__parallel__pb2._NDSBPSIGNATURE
_OPATTRIBUTELIST.fields_by_name['op_attribute'].message_type = _OPATTRIBUTE
DESCRIPTOR.message_types_by_name['OpAttribute'] = _OPATTRIBUTE
DESCRIPTOR.message_types_by_name['OpAttributeList'] = _OPATTRIBUTELIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OpAttribute = _reflection.GeneratedProtocolMessageType('OpAttribute', (_message.Message,), {
  'DESCRIPTOR' : _OPATTRIBUTE,
  '__module__' : 'oneflow.core.operator.op_attribute_pb2'
  # @@protoc_insertion_point(class_scope:oneflow.OpAttribute)
  })
_sym_db.RegisterMessage(OpAttribute)

OpAttributeList = _reflection.GeneratedProtocolMessageType('OpAttributeList', (_message.Message,), {
  'DESCRIPTOR' : _OPATTRIBUTELIST,
  '__module__' : 'oneflow.core.operator.op_attribute_pb2'
  # @@protoc_insertion_point(class_scope:oneflow.OpAttributeList)
  })
_sym_db.RegisterMessage(OpAttributeList)


# @@protoc_insertion_point(module_scope)
