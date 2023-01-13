"""AWS helpers module"""

import json

def get_sns_message(event: dict):
    """Returns parsed SNS message"""
    try:
        return json.loads(event['Records'][0]['Sns']['Message'])
    except KeyError:
        return event
