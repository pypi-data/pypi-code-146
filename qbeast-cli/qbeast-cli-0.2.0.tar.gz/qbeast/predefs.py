import os

default_schema_name = 'Default'
default_precision = 1.0
default_format = 'Qbeast'
default_object_storage = 'S3'
default_url_validity_period = 86400
s3_pattern = r'[s3|s3a]:\/\/(.*?)\/(.*)'

# Qbeast-sharing default profile path
home_dir = os.path.expanduser("~")
qbeast_config_path = home_dir + "/.qbeast"
profile_filename = "profile.json"
curator_config_filename = "curator.json"
output_dir = '/tmp'
dbt_tar_prefix="dbt_project"
ingestion_app_prefix="ingestion_app"
sync_timeout = 300

qbeast_dbt_config_filename = 'qbeast.yaml'
dbt_config_filename = 'dbt_project.yml'
