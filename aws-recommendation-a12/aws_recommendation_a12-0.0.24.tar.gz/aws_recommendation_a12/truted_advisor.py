import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Generates recommendation from trusted advisor
def get_trusted_advisor_recommendations(self) -> list:
    logger.info(" ---Inside get_trusted_advisor_recommendations")
    recommendation = []
    client = self.session.client('support', region_name='us-east-1')
    response = client.describe_trusted_advisor_checks(
        language='en'
    )
    for check in response['checks']:
        print('Id: {}'.format(check['id']))
        print('Name: {}'.format(check['name']))
        print('Description: {}'.format(check['description']))
        print('category: {}'.format(check['category']))
        print('metadata: {}'.format(str(check['metadata'])))

    return recommendation