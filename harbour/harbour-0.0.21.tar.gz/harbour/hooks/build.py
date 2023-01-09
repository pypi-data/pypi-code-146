import json
import os

from dynamodb import Table

def handler(event, context):

    table = Table('REGISTRY_TABLE_NAME')

    for record in event['Records']:

        body = json.loads(record['body'])

        # Extracts the key from the event
        key = [
            env['value'] for env in body['detail']['additional-information']['environment']['environment-variables']
            if env['name'] == 'IMAGE_TAG'
        ][0]


        # Any phase change
        if body['detail-type'] == 'CodeBuild Build State Change':

            event = {
                'status': body['detail']['build-status'],
                'build': {
                    'id': body['detail']['build-id'],
                    'project': {
                        'name': body['detail']['project-name'],
                    },
                    'source': body['detail']['additional-information']['source'],
                    'logs': body['detail']['additional-information']['logs'],
                }
            }

            table.update(key, event)

        # Any status change
        elif body['detail-type'] == 'CodeBuild Build Phase Change':

            event = {
                'status': body['detail']['completed-phase']
            }

            table.update(key, event, mode='PATCH')
