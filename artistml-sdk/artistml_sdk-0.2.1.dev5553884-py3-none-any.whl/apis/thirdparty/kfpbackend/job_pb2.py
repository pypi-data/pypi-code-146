# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: thirdparty/kfpbackend/job.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ...thirdparty.kfpbackend import error_pb2 as thirdparty_dot_kfpbackend_dot_error__pb2
from ...thirdparty.kfpbackend import pipeline_spec_pb2 as thirdparty_dot_kfpbackend_dot_pipeline__spec__pb2
from ...thirdparty.kfpbackend import resource_reference_pb2 as thirdparty_dot_kfpbackend_dot_resource__reference__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fthirdparty/kfpbackend/job.proto\x12\x15thirdparty.kfpbackend\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a!thirdparty/kfpbackend/error.proto\x1a)thirdparty/kfpbackend/pipeline_spec.proto\x1a.thirdparty/kfpbackend/resource_reference.proto\"@\n\x10\x43reateJobRequest\x12,\n\x03job\x18\x01 \x01(\x0b\x32\x1a.thirdparty.kfpbackend.JobR\x03job\"\x1f\n\rGetJobRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"\xd8\x01\n\x0fListJobsRequest\x12\x1d\n\npage_token\x18\x01 \x01(\tR\tpageToken\x12\x1b\n\tpage_size\x18\x02 \x01(\x05R\x08pageSize\x12\x17\n\x07sort_by\x18\x03 \x01(\tR\x06sortBy\x12X\n\x16resource_reference_key\x18\x04 \x01(\x0b\x32\".thirdparty.kfpbackend.ResourceKeyR\x14resourceReferenceKey\x12\x16\n\x06\x66ilter\x18\x05 \x01(\tR\x06\x66ilter\"\x89\x01\n\x10ListJobsResponse\x12.\n\x04jobs\x18\x01 \x03(\x0b\x32\x1a.thirdparty.kfpbackend.JobR\x04jobs\x12\x1d\n\ntotal_size\x18\x03 \x01(\x05R\ttotalSize\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken\"\"\n\x10\x44\x65leteJobRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"\"\n\x10\x45nableJobRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"#\n\x11\x44isableJobRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"\x94\x01\n\x0c\x43ronSchedule\x12\x39\n\nstart_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tstartTime\x12\x35\n\x08\x65nd_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x07\x65ndTime\x12\x12\n\x04\x63ron\x18\x03 \x01(\tR\x04\x63ron\"\xad\x01\n\x10PeriodicSchedule\x12\x39\n\nstart_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tstartTime\x12\x35\n\x08\x65nd_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x07\x65ndTime\x12\'\n\x0finterval_second\x18\x03 \x01(\x03R\x0eintervalSecond\"\xb8\x01\n\x07Trigger\x12J\n\rcron_schedule\x18\x01 \x01(\x0b\x32#.thirdparty.kfpbackend.CronScheduleH\x00R\x0c\x63ronSchedule\x12V\n\x11periodic_schedule\x18\x02 \x01(\x0b\x32\'.thirdparty.kfpbackend.PeriodicScheduleH\x00R\x10periodicScheduleB\t\n\x07trigger\"\xc3\x05\n\x03Job\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x03 \x01(\tR\x0b\x64\x65scription\x12H\n\rpipeline_spec\x18\x04 \x01(\x0b\x32#.thirdparty.kfpbackend.PipelineSpecR\x0cpipelineSpec\x12Y\n\x13resource_references\x18\x05 \x03(\x0b\x32(.thirdparty.kfpbackend.ResourceReferenceR\x12resourceReferences\x12\'\n\x0fservice_account\x18\x12 \x01(\tR\x0eserviceAccount\x12\'\n\x0fmax_concurrency\x18\x06 \x01(\x03R\x0emaxConcurrency\x12\x38\n\x07trigger\x18\x07 \x01(\x0b\x32\x1e.thirdparty.kfpbackend.TriggerR\x07trigger\x12\x33\n\x04mode\x18\x08 \x01(\x0e\x32\x1f.thirdparty.kfpbackend.Job.ModeR\x04mode\x12\x39\n\ncreated_at\x18\t \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x39\n\nupdated_at\x18\n \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tupdatedAt\x12\x16\n\x06status\x18\x0b \x01(\tR\x06status\x12\x14\n\x05\x65rror\x18\x0c \x01(\tR\x05\x65rror\x12\x18\n\x07\x65nabled\x18\x10 \x01(\x08R\x07\x65nabled\x12\x1d\n\nno_catchup\x18\x11 \x01(\x08R\tnoCatchup\"3\n\x04Mode\x12\x10\n\x0cUNKNOWN_MODE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\x32\xc3\x05\n\nJobService\x12q\n\tCreateJob\x12\'.thirdparty.kfpbackend.CreateJobRequest\x1a\x1a.thirdparty.kfpbackend.Job\"\x1f\x82\xd3\xe4\x93\x02\x19\"\x12/apis/v1beta1/jobs:\x03job\x12k\n\x06GetJob\x12$.thirdparty.kfpbackend.GetJobRequest\x1a\x1a.thirdparty.kfpbackend.Job\"\x1f\x82\xd3\xe4\x93\x02\x19\x12\x17/apis/v1beta1/jobs/{id}\x12w\n\x08ListJobs\x12&.thirdparty.kfpbackend.ListJobsRequest\x1a\'.thirdparty.kfpbackend.ListJobsResponse\"\x1a\x82\xd3\xe4\x93\x02\x14\x12\x12/apis/v1beta1/jobs\x12t\n\tEnableJob\x12\'.thirdparty.kfpbackend.EnableJobRequest\x1a\x16.google.protobuf.Empty\"&\x82\xd3\xe4\x93\x02 \"\x1e/apis/v1beta1/jobs/{id}/enable\x12w\n\nDisableJob\x12(.thirdparty.kfpbackend.DisableJobRequest\x1a\x16.google.protobuf.Empty\"\'\x82\xd3\xe4\x93\x02!\"\x1f/apis/v1beta1/jobs/{id}/disable\x12m\n\tDeleteJob\x12\'.thirdparty.kfpbackend.DeleteJobRequest\x1a\x16.google.protobuf.Empty\"\x1f\x82\xd3\xe4\x93\x02\x19*\x17/apis/v1beta1/jobs/{id}B@Z>github.com/kubeflow/pipelines/backend/api/go_client;kfpbackendb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'thirdparty.kfpbackend.job_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z>github.com/kubeflow/pipelines/backend/api/go_client;kfpbackend'
  _JOBSERVICE.methods_by_name['CreateJob']._options = None
  _JOBSERVICE.methods_by_name['CreateJob']._serialized_options = b'\202\323\344\223\002\031\"\022/apis/v1beta1/jobs:\003job'
  _JOBSERVICE.methods_by_name['GetJob']._options = None
  _JOBSERVICE.methods_by_name['GetJob']._serialized_options = b'\202\323\344\223\002\031\022\027/apis/v1beta1/jobs/{id}'
  _JOBSERVICE.methods_by_name['ListJobs']._options = None
  _JOBSERVICE.methods_by_name['ListJobs']._serialized_options = b'\202\323\344\223\002\024\022\022/apis/v1beta1/jobs'
  _JOBSERVICE.methods_by_name['EnableJob']._options = None
  _JOBSERVICE.methods_by_name['EnableJob']._serialized_options = b'\202\323\344\223\002 \"\036/apis/v1beta1/jobs/{id}/enable'
  _JOBSERVICE.methods_by_name['DisableJob']._options = None
  _JOBSERVICE.methods_by_name['DisableJob']._serialized_options = b'\202\323\344\223\002!\"\037/apis/v1beta1/jobs/{id}/disable'
  _JOBSERVICE.methods_by_name['DeleteJob']._options = None
  _JOBSERVICE.methods_by_name['DeleteJob']._serialized_options = b'\202\323\344\223\002\031*\027/apis/v1beta1/jobs/{id}'
  _CREATEJOBREQUEST._serialized_start=276
  _CREATEJOBREQUEST._serialized_end=340
  _GETJOBREQUEST._serialized_start=342
  _GETJOBREQUEST._serialized_end=373
  _LISTJOBSREQUEST._serialized_start=376
  _LISTJOBSREQUEST._serialized_end=592
  _LISTJOBSRESPONSE._serialized_start=595
  _LISTJOBSRESPONSE._serialized_end=732
  _DELETEJOBREQUEST._serialized_start=734
  _DELETEJOBREQUEST._serialized_end=768
  _ENABLEJOBREQUEST._serialized_start=770
  _ENABLEJOBREQUEST._serialized_end=804
  _DISABLEJOBREQUEST._serialized_start=806
  _DISABLEJOBREQUEST._serialized_end=841
  _CRONSCHEDULE._serialized_start=844
  _CRONSCHEDULE._serialized_end=992
  _PERIODICSCHEDULE._serialized_start=995
  _PERIODICSCHEDULE._serialized_end=1168
  _TRIGGER._serialized_start=1171
  _TRIGGER._serialized_end=1355
  _JOB._serialized_start=1358
  _JOB._serialized_end=2065
  _JOB_MODE._serialized_start=2014
  _JOB_MODE._serialized_end=2065
  _JOBSERVICE._serialized_start=2068
  _JOBSERVICE._serialized_end=2775
# @@protoc_insertion_point(module_scope)
