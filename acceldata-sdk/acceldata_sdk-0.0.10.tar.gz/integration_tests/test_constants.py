import os
# UID of the pipeline in torch
pipeline_uid = "torch.test"
# Name of the pipeline in torch
pipeline_name = "Integration test pipeline"
job_uid = "test_job"


# setup these 3 env vars in your environment.
torch_credentials = {
    'url': os.getenv('TORCH_CATALOG_URL', 'https://torch.acceldata.local:5443/torch'),
    'access_key': os.getenv('TORCH_ACCESS_KEY', 'P04IM8FNQRUCRTU'),
    'secret_key': os.getenv('TORCH_SECRET_KEY', 'E6LL9YUPMG4BDTJHT2VZD75HW0B8E5')
}

# torch_credentials = {
#     'url': os.getenv('TORCH_CATALOG_URL', 'https://acceldata.dev.10.90.3.89.nip.io'),
#     'access_key': os.getenv('TORCH_ACCESS_KEY', '21DK0CVJUAE0LET'),
#     'secret_key': os.getenv('TORCH_SECRET_KEY', '1PT5E06TLCHKGELZCOEC7LLOCPYHJO')
# }

# ds_name = 'sf_ds'
# ds_id = '1'
# asset_uid = 'sf_ds.FINANCE.FINANCE.ACCELDATA_CUSTOMERS_IND'
# asset_id = 4
# dq_policy_id = 1
# recon_policy_id = 3


ds_name = 'sf_ds'
ds_id = '14'
asset_uid = 'sf_ds.AUTOMATION_CUSTOM_METADATA_MULTIPLE_DB.AUTOMATION_CUSTOM_METADATA_MULTIPLE_SCHEMA.AUTOMATION_CUSTOM_METADATA_MULTIPLE_TABLE.CUSTOM_METADATA_CUSTOMER_ID'
asset_id = 2198
dq_policy_id = 1
recon_policy_id = 3