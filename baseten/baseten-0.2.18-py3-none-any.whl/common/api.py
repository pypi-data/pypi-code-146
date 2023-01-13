import functools
import json
import logging
import os
import tarfile
import tempfile
from typing import IO, Dict, List, Optional, Union

import requests
from colorama import Fore, Style
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

from baseten.common import settings
from baseten.common.core import ARTIFACT_FILENAME, ApiError, AuthorizationError
from baseten.common.util import base64_encoded_json_str

logger = logging.getLogger(__name__)


class AuthToken:
    value: str

    def __init__(self, value: str):
        self.value = value

    def headers(self):
        raise NotImplementedError


class ApiKey(AuthToken):
    def headers(self):
        return {'Authorization': f'Api-Key {self.value}'}


class JWT(AuthToken):
    def headers(self):
        return {"Authorization": self.value}


def with_api_key(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        config = settings.read_config()

        if config.has_option('api', 'api_key'):
            api_key = config.get('api', 'api_key')
        elif settings.get_jwt_auth_token():
            raise AuthorizationError('This operation is not supported in the Web IDE')
        else:
            raise AuthorizationError('You must first run the `baseten login` cli command.')

        result = func(ApiKey(api_key), *args, **kwargs)
        return result
    return wrapper


def with_api_key_or_jwt(func):
    """
    Allows an API method to be called internally (with JWT) or externally
    (with API Key).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        config = settings.read_config()

        if config.has_option('api', 'api_key'):
            result = func(ApiKey(config.get('api', 'api_key')), *args, **kwargs)
            return result
        elif settings.get_jwt_auth_token():
            result = func(JWT(settings.get_jwt_auth_token()), *args, **kwargs)
            return result
        else:
            raise AuthorizationError('You must first run the `baseten login` cli command.')

    return wrapper


@with_api_key_or_jwt
def models(auth_token: AuthToken):
    query_string = '''
    {
      models {
        id,
        name
        versions{
            id,
            semver,
            current_deployment_status,
            is_primary,
        }
      }
    }
    '''

    resp = _post_graphql_query(auth_token, query_string)
    return resp['data']


@with_api_key
def get_model(api_key, model_name):
    query_string = f'''
    {{
      model_version(name: "{model_name}") {{
        oracle{{
            name
            versions{{
                id
                semver
                truss_hash
                truss_signature
                is_draft
            }}
        }}
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']


@with_api_key
def get_pretrained_model(api_key, pretrained_model_name):
    query_string = f'''
    {{
      pretrained_model(name: "{pretrained_model_name}") {{
        pretty_name
        name
        s3_key
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']


@with_api_key
def pretrained_models(api_key):
    query_string = '''
    {
      pretrained_models {
        pretty_name
        name
        s3_key
      }
    }
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']


@with_api_key_or_jwt
def pretrained_model_version(auth_token: AuthToken, pretrained_model_name: str):
    query_string = f'''
    {{
      pretrained_model_version(pretrained_model_name: "{pretrained_model_name}"){{
        model_id
        current_deployment_status
        truss_spec_version
      }}
    }}
    '''
    resp = _post_graphql_query(auth_token, query_string)
    return resp['data']


@with_api_key
def models_summary(api_key):
    query_string = '''
    {
      models {
        id,
        name,
        description,
        versions {
          id
          created,
          configuration
        }
      }
    }
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['models']


@with_api_key
def model_version_external_id_get_version(api_key, external_model_version_id):
    query_string = f"""
    {{
      model_version(external_model_version_id: "{external_model_version_id}") {{
        id
      }}
    }}
    """

    resp = _post_graphql_query(api_key, query_string)
    return resp["data"]["model_version"]["id"]


@with_api_key_or_jwt
def model_version_truss_spec_version(auth_token: AuthToken, model_version_id: str):
    query_string = f"""
    {{
      model_version(id: "{model_version_id}") {{
        truss_spec_version
      }}
    }}
    """

    resp = _post_graphql_query(auth_token, query_string)
    return resp["data"]["model_version"]["truss_spec_version"]


@with_api_key_or_jwt
def model_truss_spec_version(auth_token: AuthToken, model_id: str):
    query_string = f"""
    {{
      model(id: "{model_id}") {{
        primary_version {{
            truss_spec_version
        }}
      }}
    }}
    """
    resp = _post_graphql_query(auth_token, query_string)
    return resp["data"]["model"]["primary_version"]["truss_spec_version"]


@with_api_key
def create_model_from_truss(
    api_key,
    model_name,
    s3_key,
    config,
    semver_bump,
    client_version,
    is_trusted=False,
    external_model_version_id=None,
):
    query_string = f'''
    mutation {{
      create_model_from_truss(name: "{model_name}",
                   s3_key: "{s3_key}",
                   config: "{config}",
                   semver_bump: "{semver_bump}",
                   client_version: "{client_version}",
                   is_trusted: {'true' if is_trusted else 'false'}
                   external_model_version_id: "{external_model_version_id if external_model_version_id else ''}"
) {{
        id,
        name,
        version_id
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_model_from_truss']


@with_api_key
def create_model_version_from_truss(
    api_key,
    model_id,
    s3_key,
    config,
    semver_bump,
    client_version,
    is_trusted=False,
    external_model_version_id=None,
):

    query_string = f'''
    mutation {{
      create_model_version_from_truss(
                   model_id: "{model_id}"
                   s3_key: "{s3_key}",
                   config: "{config}",
                   semver_bump: "{semver_bump}",
                   client_version: "{client_version}",
                   is_trusted: {'true' if is_trusted else 'false'}
                   external_model_version_id: "{external_model_version_id if external_model_version_id else ''}"

      ) {{
        id,
        name,
        version_id
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_model_version_from_truss']


@with_api_key
def deploy_draft_truss(
    api_key,
    model_name,
    s3_key,
    config,
    client_version,
    is_trusted=False,
):
    query_string = f'''
    mutation {{
      deploy_draft_truss(name: "{model_name}",
                   s3_key: "{s3_key}",
                   config: "{config}",
                   client_version: "{client_version}",
                   is_trusted: {'true' if is_trusted else 'false'},
) {{
        id,
        name,
        version_id
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['deploy_draft_truss']


@with_api_key
def patch_draft_truss(
    api_key,
    model_name,
    patch,
    client_version,
):
    patch = base64_encoded_json_str(patch.to_dict())
    query_string = f'''
    mutation {{
      patch_draft_truss(name: "{model_name}",
                   client_version: "{client_version}",
                   patch: "{patch}",
) {{
        id,
        name,
        version_id
        succeeded
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['patch_draft_truss']


@with_api_key
def create_model_configuration(
    api_key: ApiKey,
    configuration: dict,
    model_id: Optional[str] = None,
    model_version_id: Optional[str] = None,
):
    # encode for None/null
    encoded_configuration = base64_encoded_json_str(configuration)

    model_identifier_field = None
    if model_id:
        model_identifier_field = f'model_id: "{model_id}"'
    elif model_version_id:
        model_identifier_field = f'model_version_id: "{model_version_id}"'
    else:
        raise ValueError('Either model_version_id or model_id must be specified.')

    query_string = f'''
    mutation {{
        create_model_configuration(
            encoded_configuration: "{encoded_configuration}",
            {model_identifier_field}
        )
        {{
            configuration_id: id,
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_model_configuration']


@with_api_key
def model_version_configuration(api_key, model_version_id):
    query_string = f'''
    {{
      model_version(id: "{model_version_id}") {{
        configuration
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['model_version']['configuration']


@with_api_key
def model_configuration(api_key, model_id):
    query_string = f'''
    {{
      model(id: "{model_id}") {{
        configuration
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['model']['configuration']


@with_api_key
def create_model_metrics(
    api_key: ApiKey,
    metric_data: dict,
    model_id: Optional[str] = None,
    model_version_id: Optional[str] = None,
):
    # encode for None/null
    encoded_metric_data = base64_encoded_json_str(metric_data)

    model_identifier_field = None
    if model_id:
        model_identifier_field = f'model_id: "{model_id}"'
    elif model_version_id:
        model_identifier_field = f'model_version_id: "{model_version_id}"'
    else:
        raise ValueError('Either model_version_id or model_id must be specified.')

    query_string = f'''
    mutation {{
        create_model_metrics(
            encoded_metric_data: "{encoded_metric_data}",
            {model_identifier_field}
        )
        {{
            metrics_id: id,
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_model_metrics']


@with_api_key
def model_version_metrics(api_key, model_version_id):
    query_string = f'''
    {{
      model_version(id: "{model_version_id}") {{
        metrics
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['model_version']['metrics']


@with_api_key
def model_metrics(api_key, model_id):
    query_string = f'''
    {{
      model(id: "{model_id}") {{
        metrics
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['model']['metrics']


@with_api_key
def signed_s3_upload_post(api_key, model_file_name):
    query_string = f'''
    {{
      signed_s3_upload_url(model_file_name: "{model_file_name}") {{
        url,
        form_fields {{
          key,
          aws_access_key_id,
          policy,
          signature,
        }}
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']["signed_s3_upload_url"]


@with_api_key
def signed_s3_upload_and_download_post(api_key, file_name):
    query_string = f'''
    {{
      signed_s3_upload_url(model_file_name: "{file_name}"){{
        url,
        get_url,
        form_fields {{
          key,
          aws_access_key_id,
          policy,
          signature,
        }}
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']["signed_s3_upload_url"]


@with_api_key
def get_model_s3_download_url(api_key, model_version_id):
    query_string = f'''
    {{
      model_s3_download_url(model_version_id: "{model_version_id}") {{
        url,
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']["model_s3_download_url"]["url"]


@with_api_key
def artifact_signed_s3_upload_post(api_key, file_name, file_size):
    query_string = f'''
    {{
      artifact_signed_s3_upload_url(file_name: "{file_name}", file_size: {file_size}) {{
        url,
        form_fields {{
          key,
          aws_access_key_id,
          policy,
          signature,
        }}
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['artifact_signed_s3_upload_url']


@with_api_key_or_jwt
def user_files_signed_s3_upload_post(auth_token: AuthToken, file_name: str):
    query_string = f'''
    {{
      user_files_signed_s3_upload_url(file_name: "{file_name}") {{
        url,
        get_url,
        form_fields {{
          key,
          aws_access_key_id,
          policy,
          signature,
        }}
      }}
    }}
    '''

    resp = _post_graphql_query(auth_token, query_string)

    return resp['data']['user_files_signed_s3_upload_url']


@with_api_key
def register_data_for_model(api_key, s3_key, model_version_id, data_name):
    query_string = f'''
    mutation {{
        create_sample_data_file(model_version_id: "{model_version_id}",
                                name: "{data_name}",
                                s3_key: "{s3_key}") {{
          id
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_sample_data_file']


@with_api_key
def create_artifact(
    api_key: ApiKey,
    s3_key: str,
    name: str,
    description: Optional[str] = None,
    model_id: Optional[str] = None,
    model_version_id: Optional[str] = None,
):
    # encode for None/null
    description = base64_encoded_json_str(description)
    model_id = base64_encoded_json_str(model_id)
    model_version_id = base64_encoded_json_str(model_version_id)

    query_string = f'''
    mutation {{
        create_artifact(
            name: "{name}",
            s3_key: "{s3_key}",
            encoded_description: "{description}",
            encoded_model_id: "{model_id}",
            encoded_model_version_id: "{model_version_id}"
        )
        {{
            artifact_id: id,
            name,
            description
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_artifact']


@with_api_key
def create_artifact_link(
    api_key: ApiKey,
    artifact_id: str,
    model_id: Optional[str] = None,
    model_version_id: Optional[str] = None,
):
    # encode for None/null
    model_id = base64_encoded_json_str(model_id)
    model_version_id = base64_encoded_json_str(model_version_id)

    query_string = f'''
    mutation {{
        link_artifact(
            id: "{artifact_id}",
            encoded_model_id: "{model_id}",
            encoded_model_version_id: "{model_version_id}"
        )
        {{
            id
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['link_artifact']


@with_api_key
def delete_artifact(
    api_key: ApiKey,
    artifact_id: str,
):
    query_string = f'''
    mutation {{
        delete_artifact(
            artifact_id: "{artifact_id}",
        )
        {{
            ok
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['delete_artifact']


@with_api_key
def update_artifact(
    api_key: ApiKey,
    artifact_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    s3_key: Optional[str] = None,
):
    update_str = ''
    if name:
        update_str += f'name: "{name}",\n'
    if description:
        update_str += f'description: "{description}",\n'
    if s3_key:
        update_str += f's3_key: "{s3_key}",\n'

    query_string = f'''
    mutation {{
        update_artifact(
            artifact_id: "{artifact_id}",
            {update_str}
        )
        {{
            id
            name
            description
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['update_artifact']


@with_api_key
def artifact_url(
    api_key: ApiKey,
    artifact_id: str,
):
    query_string = f'''{{
        artifact(
            id: "{artifact_id}",
        )
        {{
            id, url
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['artifact']['url']


@with_api_key
def artifact_links(
    api_key: ApiKey,
    artifact_id: str,
):
    query_string = f'''{{
        artifact(
            id: "{artifact_id}",
        )
        {{
            model_ids: oracle_ids
            model_version_ids: oracle_version_ids
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['artifact']


@with_api_key
def model_linked_artifacts(
    api_key: ApiKey,
    model_id: str,
):
    query_string = f'''{{
        model(
            id: "{model_id}",
        )
        {{
            artifacts {{
                artifact_id: id,
                name,
                description
            }}
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['model']['artifacts']


@with_api_key
def model_version_linked_artifacts(
    api_key: ApiKey,
    model_version_id: str,
):
    query_string = f'''{{
        model_version(
            id: "{model_version_id}",
        )
        {{
            artifacts {{
                artifact_id: id,
                name,
                description
            }}
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['model_version']['artifacts']


@with_api_key_or_jwt
def predict_for_model(auth_token: AuthToken,
                      model_id: str,
                      inputs: Union[List, Dict],
                      metadata: Optional[List[Dict]] = None,
                      prediction_only: bool = True,
                      v2: bool = False) -> Union[List[List], Dict]:
    """Call the model's predict given the input json.

    Args:
        auth_token (AuthToken)
        model_id (str)
        inputs (list)
        metadata (List[Dict]): Metadata key/value pairs (e.g. name, url), one for each input.
        prediction_only(bool)

    Raises:
        RequestException: If there was an error communicating with the server.
    """

    # We have a special predict endpoint for internal use that we use
    # if a JWT is present.
    if isinstance(auth_token, ApiKey):
        predict_url = f'{settings.get_server_url()}/models/{model_id}/predict'
    elif isinstance(auth_token, JWT):
        predict_url = f'{settings.get_server_url()}/models/{model_id}/predict_internal'

    return _predict(auth_token, predict_url, inputs, metadata, prediction_only, v2=v2)


@with_api_key
def predict_for_model_version(api_key: ApiKey,
                              model_version_id: str,
                              inputs: Union[List, Dict],
                              metadata: Optional[List[Dict]] = None,
                              prediction_only: bool = True,
                              v2: bool = False) -> Union[List[List], Dict]:
    """Call the model version's predict given the input json.

    Args:
        api_key (str)
        model_version_id (str)
        inputs (list)
        metadata (List[Dict]): Metadata key/value pairs (e.g. name, url), one for each input.

    Raises:
        RequestException: If there was an error communicating with the server.
    """
    predict_url = f'{settings.get_server_url()}/model_versions/{model_version_id}/predict'
    return _predict(api_key, predict_url, inputs, metadata, prediction_only, v2=v2)


@with_api_key
def set_primary(api_key, model_version_id: str):
    """Promote this version of the model as the primary version.

    Args:
        api_key (str)
        model_version_id (str)
    """
    query_string = f'''
    mutation {{
      update_model_version(model_version_id: "{model_version_id}", is_primary: true) {{
        id,
        is_primary,
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['update_model_version']


@with_api_key
def update_model_features(
    api_key: ApiKey,
    model_version_id: str,
    feature_names: list,
    class_labels: Optional[list] = None
):
    """Update the feature names for the model.

    Args:
        api_key (str)
        model_version_id (str)
        feature_names (list)
        class_labels (Optional[list]): applies only to classifiers.
    """
    encoded_feature_names = base64_encoded_json_str(feature_names)
    encoded_class_labels = base64_encoded_json_str(class_labels)
    query_string = f'''
    mutation {{
      update_model_version(model_version_id: "{model_version_id}",
                           encoded_feature_names: "{encoded_feature_names}",
                           encoded_class_labels: "{encoded_class_labels}") {{
        id,
        feature_names,
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['update_model_version']


@with_api_key
def install_requirements(api_key, requirements_txt):
    escaped_requirements_txt = requirements_txt.replace('\n', '\\n')  # Otherwise the mutation becomes invalid graphql.
    query_string = f'''
    mutation {{
      create_pynode_requirement(requirements_txt: "{escaped_requirements_txt}") {{
        id
        status
        error_message
      }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['create_pynode_requirement']


@with_api_key
def requirement_status(api_key, requirement_id):
    query_string = f'''
    {{
      pynode_requirement(id: "{requirement_id}") {{
        id
        status
        error_message
      }}
    }}
    '''

    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['pynode_requirement']


def _format_inputs_for_v1(
    auth_token: AuthToken,
    inputs: Union[List, Dict],
    metadata: Optional[List[Dict]]
) -> Union[List, Dict]:
    """
    For internal (JWT) token use-cases, we do not need to package up the inputs.
    For external cases, for the v1 model serving path, we expect inputs to be
    provided in the format { inputs: ..., metadata: ... }.
    """
    if isinstance(auth_token, ApiKey):
        return {'inputs': inputs, 'metadata': metadata}
    else:
        return inputs


def _predict(
    auth_token: AuthToken,
    predict_url: str,
    inputs: Union[List, Dict],
    metadata: Optional[List[Dict]] = None,
    prediction_only: bool = True,
    v2: bool = False
):
    if v2:
        resp = _post_rest_query(auth_token, predict_url, inputs)
        resp_json = json.loads(resp.content)
        return resp_json["model_output"]

    resp = _post_rest_query(
        auth_token,
        predict_url,
        _format_inputs_for_v1(auth_token, inputs, metadata)
    )
    resp_json = json.loads(resp.content)
    return resp_json['predictions'] if prediction_only else resp_json


def _post_graphql_query(auth_token: AuthToken, query_string: str) -> dict:
    headers = auth_token.headers()

    resp = requests.post(f'{settings.get_server_url()}/graphql/',
                         data={'query': query_string}, headers=headers)
    if not resp.ok:
        logger.error(f"GraphQL endpoint failed with error: {resp.content}")  # type: ignore
        resp.raise_for_status()
    resp_dict = resp.json()
    errors = resp_dict.get('errors')
    if errors:
        raise ApiError(errors[0]['message'], resp)
    return resp_dict


def _post_rest_query(auth_token: AuthToken, url: str, post_body_dict: Union[List, Dict]):
    headers = auth_token.headers()

    resp = requests.post(url, json=post_body_dict, headers=headers)
    resp.raise_for_status()
    return resp


def upload_model(serialize_file: IO, file_ext: str, file_name: str) -> str:
    """Uploads the serialized model to the appropriate environment

    Args:
        serialize_file (file): A file-like object that is the serialized representation of the model object.
        file_ext (str): The file extension for the saved model

    Returns:
        str: The key for the uploaded model

    Raises:
        RequestException: If there was an error communicating with the server.
    """

    model_file_name = f'{file_name}.{file_ext}'
    this_signed_s3_upload_post = signed_s3_upload_post(model_file_name)
    logger.debug(f'Signed s3 upload post:\n{json.dumps(this_signed_s3_upload_post, indent=4)}')

    form_fields = this_signed_s3_upload_post['form_fields']
    form_fields['AWSAccessKeyId'] = form_fields.pop('aws_access_key_id')  # S3 expects key name AWSAccessKeyId
    form_fields['file'] = (file_name, serialize_file)
    logger.info('🚀 Uploading model to BaseTen 🚀')

    return _upload_file(this_signed_s3_upload_post, form_fields)


def upload_artifact(serialize_file: IO, file_ext: str, file_name: str, file_size: int) -> str:
    """Uploads the serialized artifact to the appropriate environment

    Args:
        serialize_file (file): A file-like object that is the serialized representation of the artifact object.
        file_ext (str): The file extension for the saved artifact

    Returns:
        str: The key for the uploaded artifact

    Raises:
        RequestException: If there was an error communicating with the server.
    """
    artifact_file_name = f'{file_name}.{file_ext}'
    this_signed_s3_upload_post = artifact_signed_s3_upload_post(artifact_file_name, file_size)
    logger.debug(f'Signed s3 upload post:\n{json.dumps(this_signed_s3_upload_post, indent=4)}')

    form_fields = this_signed_s3_upload_post['form_fields']
    form_fields['AWSAccessKeyId'] = form_fields.pop('aws_access_key_id')  # S3 expects key name AWSAccessKeyId
    form_fields['file'] = (file_name, serialize_file)
    logger.info('🚀 Uploading artifact to BaseTen 🚀')

    return _upload_file(this_signed_s3_upload_post, form_fields)


def upload_user_file(io_stream: IO, file_name: str) -> str:
    signed_s3_upload_post = user_files_signed_s3_upload_post(file_name)
    logger.debug(f'Signed s3 upload post:\n{json.dumps(signed_s3_upload_post, indent=4)}')

    form_fields = signed_s3_upload_post['form_fields']
    form_fields['AWSAccessKeyId'] = form_fields.pop('aws_access_key_id')  # S3 expects key name AWSAccessKeyId
    form_fields['file'] = (file_name, io_stream)

    _upload_file(signed_s3_upload_post, form_fields)

    return signed_s3_upload_post["get_url"]


def upload_user_dataset_file(file_path: str, file_name: str) -> dict:
    signed_s3_upload_post = user_files_signed_s3_upload_post(file_name)
    logger.debug(f'Signed s3 upload post:\n{json.dumps(signed_s3_upload_post, indent=4)}')

    form_fields = signed_s3_upload_post['form_fields']
    form_fields['AWSAccessKeyId'] = form_fields.pop('aws_access_key_id')  # S3 expects key name AWSAccessKeyId
    form_fields['file'] = (file_name, open(file_path, "rb"))

    _upload_file(signed_s3_upload_post, form_fields)

    return signed_s3_upload_post


def _upload_file(this_signed_s3_upload_post: dict, form_fields: dict) -> str:
    encoder = MultipartEncoder(fields=form_fields)
    encoder_len = encoder.len
    pbar = tqdm(total=encoder_len, unit_scale=True,
                bar_format="Upload Progress: {percentage:3.0f}%% |%s{bar:100}%s| {n_fmt}/{total_fmt}"
                % (Fore.BLUE, Fore.RESET))

    def callback(monitor):
        progress = monitor.bytes_read - pbar.n
        pbar.update(progress)

    monitor = MultipartEncoderMonitor(encoder, callback)
    resp = requests.post(
        this_signed_s3_upload_post['url'], data=monitor, headers={'Content-Type': monitor.content_type}
    )
    resp.raise_for_status()
    pbar.close()
    logger.info('🔮 Upload successful!🔮')

    logger.debug(f'File upload HTTP status code: {resp.status_code} and content:\n{resp.content}')  # type: ignore

    return this_signed_s3_upload_post['form_fields']['key']


def _tar_a_list_of_files(list_of_files: List[str]) -> tempfile._TemporaryFileWrapper:
    temp_file = tempfile.NamedTemporaryFile(suffix='.tgz')
    with tarfile.open(temp_file.name, 'w:gz') as tar:
        for file in list_of_files:
            tar.add(file)
    temp_file.file.seek(0)
    return temp_file


def serialize_artifact_to_s3(name, list_of_files):
    logger.info(f'Serializing {Fore.BLUE}{name}{Style.RESET_ALL} artifact.')
    artifact_tgz = _tar_a_list_of_files(list_of_files)
    logger.info('Making contact with BaseTen 👋 👽')
    s3_key = upload_artifact(artifact_tgz, 'tgz', ARTIFACT_FILENAME, os.path.getsize(artifact_tgz.name))
    return s3_key


@with_api_key
def deactivate_model_version(api_key, model_version_id):
    query_string = f'''
    mutation {{
        deactivate_model_version(model_version_id: "{model_version_id}") {{
          ok
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['deactivate_model_version']['ok']


@with_api_key
def activate_model_version(api_key, model_version_id):
    query_string = f'''
    mutation {{
        activate_model_version(model_version_id: "{model_version_id}") {{
          ok
        }}
    }}
    '''
    resp = _post_graphql_query(api_key, query_string)
    return resp['data']['activate_model_version']['ok']


@with_api_key_or_jwt
def create_pretrained_model(auth_token: AuthToken, model_zoo_name: str, model_name: str):
    query_string = f'''
    mutation {{
        create_pretrained_model(
            model_zoo_name: "{model_zoo_name}",
            name: "{model_name}",
            description : "",
            create_app: false
        ) {{
            model {{
                created
                id
                name
                platformType: model_platform_type
                numberOfVersions: number_of_versions
                description: description
                primaryVersion: primary_version {{
                    id
                    model_id
                    modelFramework: model_framework_display_name
                    truss_spec_version
                }}
            }}
        }}
    }}
    '''

    resp = _post_graphql_query(auth_token, query_string)
    return resp["data"]["create_pretrained_model"]["model"]


@with_api_key_or_jwt
def create_training_dataset(auth_token: AuthToken, dataset_name: str, s3_key: str, training_type: str) -> str:
    query_string = f'''
    mutation {{
        create_training_dataset(
            name: "{dataset_name}",
            s3_key: "{s3_key}",
            training_type : "{training_type}"
        ) {{
            id
        }}
    }}
    '''

    resp = _post_graphql_query(auth_token, query_string)
    return resp["data"]["create_training_dataset"]["id"]
