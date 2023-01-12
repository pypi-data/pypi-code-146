import json
import logging
from bson import json_util
import boto3
import datetime
from tabulate import tabulate


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


def date_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

    return None


def work_on_apigs(**kwargs):
    change_state = False
    on_switch = False
    apig = kwargs.get('apig', None)
    stage = kwargs.get('stage', None)
    profile = kwargs.get('profile', None)
    region = kwargs.get('region', None)
    on = kwargs.get('on', None)

    if on:
        if on.lower() == 'true':
            on_switch = True
            change_state = True
        elif on.lower() == 'false':
            on_switch = False
            change_state = True

    logger.info('apig: {}'.format(apig))
    logger.info('stage: {}'.format(stage))
    logger.info('profile: {}'.format(profile))
    logger.info('region: {}'.format(region))
    logger.info('on_switch: {}'.format(on_switch))
    logger.info('change_state: {}'.format(change_state))
    clients = _init_boto3_clients(
        ['apigateway'],
        profile,
        region
    )

    if change_state:
        _change_log_state(
            apig,
            stage,
            on_switch,
            clients.get('apigateway')
        )

    print('\nCloudWatch logs found in: API-Gateway-Execution-Logs_{}/{}'.format(apig, stage))


def list_apigs(**kwargs):
    current_position = '__first___'
    try:
        profile = kwargs.get('profile', None)
        region = kwargs.get('region', None)
        clients = _init_boto3_clients(
            ['apigateway'],
            profile,
            region
        )

        rows = []
        while current_position:
            if current_position == '__first___':
                response = clients.get('apigateway').get_rest_apis()
            else:
                response = clients.get('apigateway').get_rest_apis(position=current_position)

            current_position = response.get('position', None)
            for apig in response.get('items', []):
                name = apig.get('name', 'unknown')
                app_id = apig.get('id', 'unknown')
                r = clients.get('apigateway').get_stages(restApiId=app_id)
                stages = [stage['stageName'] for stage in r.get('item')]
                row = [name, app_id, json.dumps(stages)]
                rows.append(row)
                # print('{}({}): {}'.format(name, app_id, json.dumps(stages)))

        print(tabulate(rows, headers=['API Name', 'Id', 'Stages']))
    except Exception as ruh_roh:
        logger.error(ruh_roh, exc_info=True)

    return False


def _change_log_state(apig, stage, on_switch, client):
    try:
        if on_switch:
            response = client.update_stage(
                restApiId=apig,
                stageName=stage,
                patchOperations=[
                    {
                        "op": "replace",
                        "path": "/*/*/logging/loglevel",
                        "value": "INFO"
                    },
                    {
                        "op": "replace",
                        "path": "/*/*/metrics/enabled",
                        "value": 'true'
                    },
                    {
                        "op": "replace",
                        "path": "/*/*/logging/dataTrace",
                        "value": 'true'
                    }
                ]
            )
        else:
            response = client.update_stage(
                restApiId=apig,
                stageName=stage,
                patchOperations=[
                    {
                        "op": "replace",
                        "path": "/*/*/logging/loglevel",
                        "value": "OFF"
                    },
                    {
                        "op": "replace",
                        "path": "/*/*/metrics/enabled",
                        "value": 'false'
                    },
                    {
                        "op": "replace",
                        "path": "/*/*/logging/dataTrace",
                        "value": 'false'
                    }
                ]
            )

        logger.info(json.dumps(
            response,
            default=json_util.default,
            indent=2
        ))

        return True
    except Exception as ruh_roh:
        logger.error(ruh_roh, exc_info=False)

    return False


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
