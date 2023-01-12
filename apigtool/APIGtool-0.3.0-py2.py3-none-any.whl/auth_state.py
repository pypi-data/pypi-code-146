import sys
import json
import logging

import boto3
from apigtool.utility import date_converter

logger = logging.getLogger()
logger.setLevel(logging.INFO)
default_region = 'us-east-1'

'''
   { "patchOperations" : [
    {
        "op" : "replace",
        "path" : "/*/*/logging/loglevel",
        "value" : "INFO"
    },
   }
'''


def set_iam_auth(**kwargs):
    on_switch = False
    api_name = kwargs.get('api_name', None)
    stage = kwargs.get('stage', None)
    path = kwargs.get('path', None)
    profile = kwargs.get('profile', None)
    region = kwargs.get('region', None)
    on = kwargs.get('on', None)
    method = kwargs.get('method', None)

    if on:
        if on.lower() == 'true':
            on_switch = True
        elif on.lower() == 'false':
            on_switch = False
        else:
            logger.error(f'on switch must true or false given {on=}')
            sys.exit(2)

    if method is None:
        method = 'ANY'

    logger.info(' api_name: {}'.format(api_name))
    logger.info('    stage: {}'.format(stage))
    logger.info('     path: {}'.format(path))
    logger.info('on_switch: {}'.format(on_switch))
    logger.info('  profile: {}'.format(profile))
    logger.info('   region: {}'.format(region))
    clients = _init_boto3_clients(
        ['apigateway'],
        profile,
        region
    )

    if clients is None:
        logger.error('failed to create clients')
        return

    api_id = find_api(api_name, stage, clients.get('apigateway'))
    logger.info(f'{api_id=}')

    resource_id = find_resource(api_id, path, clients.get('apigateway'))
    logger.info(f'{resource_id=}')

    current_state = get_current_state(api_id, resource_id, method, clients.get('apigateway'))
    if current_state == on_switch:
        logger.info('no change needed')
        return True
    else:
        logger.info('change needed')
        return (
            set_current_state(
                api_id,
                resource_id,
                stage,
                method,
                on_switch,
                clients.get('apigateway'))
        )


def set_current_state(api_id, resource_id, stage, http_method, on_switch, apig_client):
    try:
        if on_switch:
            auth_type = 'AWS_IAM'
        else:
            auth_type = 'NONE'

        response = apig_client.update_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=http_method,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/authorizationType',
                    'value': auth_type
                }
            ]
        )

        logger.info('put_method() response:')
        logger.info(json.dumps(response, indent=2, default=date_converter))

        response = apig_client.create_deployment(restApiId=api_id, stageName=stage)
        logger.info('create_deployment() response:')
        logger.info(json.dumps(response, indent=2, default=date_converter))
        return False
    except Exception as ruh_roh:
        logger.error(ruh_roh, exc_info=True)

    return False


def get_current_state(api_id, resource_id, http_method, apig_client):
    current_state = False
    try:
        response = apig_client.get_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=http_method
        )
        current_state = response.get('authorizationType', '42') == 'AWS_IAM'
        logger.debug(json.dumps(response, indent=2, default=date_converter))
        logger.info(f'current authorizationType is AWS_IAM: {current_state}')
    except Exception as ruh_roh:
        logger.error(ruh_roh, exc_info=True)

    return current_state


def find_resource(api_id, path, apig_client):
    current_position = '__first___'
    try:
        while current_position:
            if current_position == '__first___':
                response = apig_client.get_resources(restApiId=api_id)
            else:
                response = apig_client.get_resources(restApiId=api_id, position=current_position)

            current_position = response.get('position', None)
            for resource in response.get('items', []):
                candidate_path = resource.get('path', 'unknown')
                resource_id = resource.get('id', 'unknown')
                if candidate_path == path:
                    return resource_id
    except Exception as ruh_roh:
        logger.error(ruh_roh, exc_info=True)

    logger.error('could not find resource Id, exiting')
    sys.exit(1)


def find_api(api_name, stage, apig_client):
    current_position = '__first___'
    try:
        while current_position:
            if current_position == '__first___':
                response = apig_client.get_rest_apis()
            else:
                response = apig_client.get_rest_apis(position=current_position)

            current_position = response.get('position', None)
            for apig in response.get('items', []):
                name = apig.get('name', 'unknown')
                api_id = apig.get('id', 'unknown')
                if name == api_name:
                    # we found it
                    r = apig_client.get_stages(restApiId=api_id)
                    logger.debug(json.dumps(r, indent=2, default=date_converter))
                    stages = [stage['stageName'] for stage in r.get('item')]
                    if stage in stages:
                        return api_id
    except Exception as ruh_roh:
        logger.error(ruh_roh, exc_info=True)

    logger.error('could not find API Id, exiting')
    sys.exit(1)


def _init_boto3_clients(services, profile, region):
    """
    Creates boto3 clients

    Args:
        profile - CLI profile to use
        region - where do you want the clients

    Returns:
        Good or Bad; True or False
    """
    try:
        if not region:
            region = default_region
        clients = {}
        session = None
        if profile and region:
            session = boto3.session.Session(profile_name=profile, region_name=region)
        elif profile:
            session = boto3.session.Session(profile_name=profile)
        elif region:
            session = boto3.session.Session(region_name=region)
        else:
            session = boto3.session.Session()

        for svc in services:
            clients[svc] = session.client(svc)
            logger.info('client for %s created', svc)

        return clients
    except Exception as wtf:
        logger.error(wtf, exc_info=True)
        return None
