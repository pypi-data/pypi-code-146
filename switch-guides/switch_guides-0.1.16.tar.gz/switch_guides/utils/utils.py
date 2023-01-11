from collections import namedtuple

ApiInputs = namedtuple('ApiInputs',
                       ['email_address', 'user_id', 'api_project_id', 'data_feed_id', 'data_feed_file_status_id',
                        'bearer_token', 'api_base_url', 'api_projects_endpoint', 'subscription_key', 'api_headers'])

def get_journeys_endpoint(api_inputs: ApiInputs):
    return api_inputs.api_base_url.replace("task-insights/api/1.0", "journeys")
    # return 'http://localhost:8000'

def coalesce(*values):
    """Return the first non-None value or None if all values are None"""
    return next((v for v in values if v is not None), None)

def _column_name_cap(columns) -> list:
    renamed_columns = [name[0].upper() + name[1:] for name in columns.to_list()]
    return renamed_columns