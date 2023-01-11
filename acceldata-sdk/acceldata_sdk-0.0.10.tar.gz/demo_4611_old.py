from torch_sdk.torch_client import TorchClient
from torch_sdk.models.tags import AssetLabel, CustomAssetMetadata
import torch_sdk.constants as const
from torch_sdk.models.profile import ProfilingType
from torch_sdk.models.profile import AutoProfileConfiguration, Profile, ProfileRequest, ProfilingType
import pprint
import time

from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata
import pprint
from datetime import datetime
import time
from torch_sdk.models.job import CreateJob, JobMetadata, Node

pp = pprint.PrettyPrinter(indent=4)
# pipeline_uid = "torch.airflow.demo.lambda"
# torch_credentials = {
#     'url': 'https://torchdemo.acceldata.tech/torch',
#     'access_key': 'V05DG18TV4MAF93',
#     'secret_key': 'VZF8O9Q5G6GUE08MQY5A8CA0TAE5KD'
# }
torch_credentials = {
    'url': 'https://torch.acceldata.local:5443/torch',
    'access_key': 'P04IM8FNQRUCRTU',
    'secret_key': 'E6LL9YUPMG4BDTJHT2VZD75HW0B8E5'
    # 'do_version_check' : True
}
# torch_credentials = {
#     'url': 'https://yubi.torch.acceldata.dev/torch',
#     'access_key': 'SAQ8XAOLSSLAD16',
#     'secret_key': 'KL5C4UA5XBQ2HBUMQPATJ3FB45HRH9'
# }
#### pipelines ###
torch_client = TorchClient(**torch_credentials)

pipeline_uid = "torch.airflow.test"
meta = PipelineMetadata(owner='sdk/pipeline-user', team='TORCH', codeLocation='...')
pipeline_name_ = "pipeline_name_test"
pipeline = CreatePipeline(
    uid=pipeline_uid,
    name=pipeline_name_,
    description=f'The pipeline {pipeline_name_} has been created from torch-sdk',
    meta=meta,
    context={'pipeline_uid': pipeline_uid, 'pipeline_name': pipeline_name_}
)
pipeline_res = torch_client.create_pipeline(pipeline=pipeline)
pipeline = torch_client.get_pipeline(pipeline_res.id)

pipeline_run = pipeline.create_pipeline_run()

job_uid = "test_job"
inputs = [Node(job_uid='customers.data-generation')]
outputs = [Node(asset_uid=f'S3-DS.s3_customers')]
context_job = {'job': 'data_gene', 'time': str(datetime.now()), 'uid': 'customers.data-generation',
               'operator': 'write_file_func'}
metadata = JobMetadata('Jason', 'COKE', 'https://github.com/coke/reports/customers.kt')
job = CreateJob(
    uid=job_uid,
    name=f'{job_uid} Job',
    version=pipeline_run.versionId,
    description=f'{job_uid} created using torch job decorator',
    inputs=inputs,
    outputs=outputs,
    meta=metadata,
    context=context_job
)
job = pipeline.create_job(job)
span = pipeline_run.create_span(uid=f'{pipeline_uid}.span')
#spans = pipeline_run.get_spans()
span_child = span.create_child_span(
    uid=f'{job_uid}.span',
    context_data={
        'time': str(datetime.now())
    },
    associatedJobUids=[job_uid])

exit()

pipeline = torch_client.get_pipeline(38)
pp.pprint('pipeline')
pp.pprint(pipeline)
runs = pipeline.get_runs()
pp.pprint('runs')
pp.pprint(runs)
pipeline_uid = torch_client.get_pipeline('shubh.airflow.coke.precreate13593')
pp.pprint('pipeline_uid')
pp.pprint(pipeline_uid)
pipelines = torch_client.get_pipelines()
pp.pprint('pipelines')
pp.pprint(pipelines)
pipelineRun = torch_client.get_pipeline_run(157)
pp.pprint('pipelineRun')
pp.pprint(pipelineRun)
pipeline_details = pipelineRun.get_details()
pp.pprint('pipeline_details')
pp.pprint(pipeline_details)
pipeline_spans = pipelineRun.get_spans()
pp.pprint('pipeline_spans')
pp.pprint(pipeline_spans)
pipeline = torch_client.get_pipeline(38)
delete_response = pipeline.delete()
#### pipelines ###
# import pdb;pdb.set_trace()
# async_executor = torch_client.execute_policy(const.PolicyType.DATA_QUALITY, 3, sync=True)
# xcom_key = f'{const.PolicyType.DATA_QUALITY.name}_{3}_execution_id'
# pp.pprint(xcom_key)
# if async_executor.errorMessage is not None:
#     async_execution_result = async_executor.get_result()

torch_credentials = {
    'url': 'https://test.torch1001.acceldata.dev/torch',
    'access_key': 'WKZW28UJGPHVJZJ',
    'secret_key': '5XP4HKAK0PBP00UQOUF89FEWDO7ZB6'
}

torch_client = TorchClient(**torch_credentials)
# asset = torch_client.get_asset('Automation_BIGQUERY_1.dq_bigquery_schema')
# pp.pprint('asset')
# pp.pprint(asset)
# ds_name = torch_client.get_datasource('gcs-111111', True)
# pp.pprint('datasource with name')
# pp.pprint(ds_name)
# ds = torch_client.get_datasource(265, True)
# pp.pprint('datasource with properties')
# pp.pprint(ds)
# dss = torch_client.get_datasources()
# pp.pprint('datasources')
# pp.pprint(dss)
# dss = torch_client.get_datasources(const.AssetSourceType.SNOWFLAKE)
# pp.pprint('datasources snowflake')
# pp.pprint(dss)
# asset = torch_client.get_asset(65240)
# pp.pprint('asset')
# pp.pprint(asset)
'''
response_start_crawler = ds.start_crawler()
pp.pprint('response_start_crawler')
pp.pprint(response_start_crawler)
response_status_crawler = ds.get_crawler_status()
pp.pprint('response_status_crawler')
pp.pprint(response_status_crawler)
'''

# metadata_asset = asset.get_metadata()
# pp.pprint('metadata_asset')
# pp.pprint(metadata_asset)
# sample_asset = asset.sample_data()
# pp.pprint('sample_asset')
# pp.pprint(sample_asset)
#
# asset.add_labels(labels=[AssetLabel('test12', 'shubh12'), AssetLabel('test22', 'shubh32')])
# labels_asset = asset.get_labels()
# pp.pprint('labels_asset')
# pp.pprint(labels_asset)
# asset.add_custom_metadata(custom_metadata=[CustomAssetMetadata('testcm1', 'shubhcm1'), CustomAssetMetadata('testcm2', 'shubhcm2')])
# latest_profile_status_asset = asset.get_latest_profile_status()
# pp.pprint('latest_profile_status_asset')
# pp.pprint(latest_profile_status_asset)
# start_profile_asset = asset.start_profile(ProfilingType.FULL)
# pp.pprint('start_profile_asset')
# pp.pprint(start_profile_asset)
# profile_status = start_profile_asset.get_status()
# pp.pprint('profile_status')
# pp.pprint(profile_status)
# time.sleep(5)
# cancel_res = profile_status = start_profile_asset.cancel()
# pp.pprint('cancel_res')
# pp.pprint(cancel_res)




# from torch_sdk.models.ruleExecutionResult import RuleType, PolicyFilter, ExecutionPeriod
# dq_policy_id = 1177
# # dq_rule_execution = torch_client.execute_policy(const.PolicyType.DATA_QUALITY, dq_policy_id)
# # pp.pprint('dq_rule_execution')
# # pp.pprint(dq_rule_execution)
#
# torch_client.get_policy(const.PolicyType.DATA_QUALITY, dq_policy_id)
# dq_rule_executions = torch_client.policy_executions(dq_policy_id, RuleType.DATA_QUALITY)
# pp.pprint('dq_rule_executions')
# pp.pprint(dq_rule_executions)
# dq_rule_executions = torch_client.policy_executions('null-check-bq-DQ-policy', RuleType.DATA_QUALITY)
# pp.pprint('dq_rule_executions')
# pp.pprint(dq_rule_executions)
# filter = PolicyFilter(policyType=RuleType.DATA_QUALITY, enable=True)
# dq_rules = torch_client.list_all_policies(filter=filter)
# pp.pprint(dq_rules)
# dq_rule = torch_client.get_policy(const.PolicyType.DATA_QUALITY, dq_policy_id)
# pp.pprint('dq_rule')
# pp.pprint(dq_rule)
# dq_rule_executions = dq_rule.get_executions()
# pp.pprint('dq_rule_executions')
# pp.pprint(dq_rule_executions)
# # async_executor = torch_client.execute_policy(const.PolicyType.DATA_QUALITY, 1114, sync=False)
# async_executor = dq_rule.execute(sync=False)
# if async_executor.errorMessage is None:
#     async_execution_status = async_executor.get_status()
#     pp.pprint('async_execution_status')
#     pp.pprint(async_execution_status)
#
#     async_execution_cancel = async_executor.cancel()
#     pp.pprint('async_execution_cancel')
#     pp.pprint(async_execution_cancel)
#     async_execution_result = async_executor.get_result()
#     pp.pprint('async_execution_result')
#     pp.pprint(async_execution_result)


