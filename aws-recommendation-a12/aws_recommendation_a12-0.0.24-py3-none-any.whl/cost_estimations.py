import botocore.exceptions
from pkg_resources import resource_filename
import json
import logging
from aws_recommendation_a12.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


FLT = '[{{"Field": "tenancy", "Value": "shared", "Type": "TERM_MATCH"}},' \
      '{{"Field": "operatingSystem", "Value": "{o}", "Type": "TERM_MATCH"}},' \
      '{{"Field": "preInstalledSw", "Value": "NA", "Type": "TERM_MATCH"}},' \
      '{{"Field": "instanceType", "Value": "{t}", "Type": "TERM_MATCH"}},' \
      '{{"Field": "location", "Value": "{r}", "Type": "TERM_MATCH"}},' \
      '{{"Field": "capacitystatus", "Value": "Used", "Type": "TERM_MATCH"}}]'

# Get current AWS price for an on-demand instance
def get_price(client, region, instance, os):
    f = FLT.format(r=region, t=instance, o=os)
    data = client.get_products(ServiceCode='AmazonEC2', Filters=json.loads(f))
    od = json.loads(data['PriceList'][0])['terms']['OnDemand']
    id1 = list(od)[0]
    id2 = list(od[id1]['priceDimensions'])[0]
    return od[id1]['priceDimensions'][id2]['pricePerUnit']['USD']

# Translate region code to region name. Even though the API data contains
# regionCode field, it will not return accurate data. However using the location
# field will, but then we need to translate the region code into a region name.
# You could skip this by using the region names in your code directly, but most
# other APIs are using the region code.
def get_region_name(region_code):
    default_region = 'US East (N. Virginia)'
    endpoint_file = resource_filename('botocore', 'data/endpoints.json')
    try:
        with open(endpoint_file, 'r') as f:
            data = json.load(f)
        # Botocore is using Europe while Pricing API using EU...sigh...
        return data['partitions'][0]['regions'][region_code]['description'].replace('Europe', 'EU')
    except IOError:
        return default_region

# returns the savings in %age
def get_savings(self, region: str, from_instance: str, to_instance: str, os: str) -> dict:
    """

    :param os:
    :param client:
    :param region: AWS region
    :param self:
    :param from_instance: source instance
    :param to_instance: destination instance
    :return:
    """
    logger.info(" ---Inside cost_estimations :: get_savings()")

    client = self.session.client('pricing', region_name='us-east-1')
    price1 = get_price(client=client, region=get_region_name(region), instance=from_instance, os=os)

    price2 = get_price(client=client, region=get_region_name(region), instance=to_instance, os=os)

    savings = ((float(price1) - float(price2)) / float(price1)) * 100

    instance_list = list_instances(self, region)

    count = 0

    for instance in instance_list:
        if instance['InstanceType'] == from_instance:
            count = count + 1

    if count == 0:
        return {
            'Flag' : False
        }

    # print(region)
    # print(price1)
    # print(price2)

    savings = savings if count > 0 else 0

    current_monthly_cost = float(price1) * count * 730
    estimated_monthly_saving = current_monthly_cost * savings / 100
    effective_monthly_cost = current_monthly_cost - estimated_monthly_saving

    # print("savings :: count "+str(count))
    # print("region "+region)
    # print("from instance "+from_instance)

    return {
        'Flag': True,
        'current_cost': current_monthly_cost,
        'Estimated Savings in %': savings,
        'Estimated Monthly Saving': estimated_monthly_saving,
        'Effective Monthly cost': effective_monthly_cost,
        'Number of Instances': count
    }


def merge(d1: dict, d2: dict)-> dict:
    if len(d1) == 0:
        return d2

    # print('Number of instances d1' + str(d1['Number of Instances']))
    # print('Number of instances d2' + str(d2['Number of Instances']))

    d1['current_cost'] = d1['current_cost']+d2['current_cost']
    # d1['Estimated Savings in %'] = d1['Estimated Savings in %']+d2['Estimated Savings in %']
    d1['Estimated Monthly Saving'] = d1['Estimated Monthly Saving']+d2['Estimated Monthly Saving']
    d1['Effective Monthly cost'] = d1['Effective Monthly cost']+d2['Effective Monthly cost']
    d1['Number of Instances'] = d1['Number of Instances']+d2['Number of Instances']
    # print('after addition'+str(d1['Number of Instances']))

    return d1


# Generates the cost estimations for different upgrades
def estimated_savings(self) -> list:
    """

    :param self:
    :return list: details of estimated savings
    """
    logger.info(" ---Inside cost_estimations :: estimated_savings()")

    possible_upgrade = [
            ('t1.micro', 't2.micro'),

            ('m1.large', 't2.large'),
            ('m1.xlarge', 't2.xlarge'),
            ('m1.medium', 't2.medium'),
            ('m1.small', 't2.small'),
            ('m1.large', 'm5.large'),
            ('m1.xlarge', 'm5.xlarge'),

            ('m3.large', 'm5.large'),
            ('m3.xlarge', 'm5.xlarge'),
            ('m3.2xlarge', 'm5.2xlarge'),

            ('c1.xlarge', 'c5.xlarge'),

            ('c3.xlarge', 'c5.xlarge'),
            ('c3.2xlarge', 'c5.2xlarge'),
            ('c3.large', 'c5.large'),
            ('c3.4xlarge', 'c5.4xlarge'),

            ('i2.xlarge', 'i3.xlarge'),
            ('i2.2xlarge', 'i3.2xlarge'),
            ('i2.4xlarge', 'i3.4xlarge'),
            ('i2.8xlarge', 'i3.8xlarge'),

            ('m2.xlarge', 'r4.xlarge'),
            ('m2.2xlarge', 'r4.2xlarge'),
            ('m2.4xlarge', 'r4.4xlarge'),

            ('cr1.8xlarge', 'r4.8xlarge'),

            ('r3.large', 'r4.large'),
            ('r3.xlarge', 'r4.xlarge'),
            ('r3.2xlarge', 'r4.2xlarge'),
            ('r3.4xlarge', 'r4.4xlarge'),
            ('r3.8xlarge', 'r4.8xlarge'),

            ('hs1.8xlarge', 'd2.8xlarge'),

            ('r3.large', 'r5.large'),
            ('r3.xlarge', 'r5.xlarge'),
            ('r3.2xlarge', 'r5.2xlarge'),
            ('r3.4xlarge', 'r5.4xlarge'),
            ('r3.8xlarge', 'r5.8xlarge'),

            # for demo purpose
            # ('t2.micro', 't2.nano'),
            # ('m5a.4xlarge', 'm5a.2xlarge'),
            # ('t2.2xlarge', 't2.xlarge'),
            # ('t2.xlarge', 't2.large'),
            # ('t2.large', 't2.medium')
        ]

    recommendations = []

    regions = self.session.get_available_regions('ec2')
    available_instance_types = {}
    for region in regions:
        try:
            instance_list = list_instances(self, region)
            for instance in instance_list:
                # available_instance_types.add(instance['InstanceType'])
                available_instance_types.setdefault(instance['InstanceType'], []).append(region)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'UnauthorizedOperation':
                logger.info('---------EC2 read access denied----------')
                temp = {
                    'Service Name': 'RDS',
                    'Id': 'Access Denied',
                    'Recommendation': 'Access Denied',
                    'Description': 'Access Denied',
                    'Metadata': {
                        'Access Denied'
                    },
                    'Recommendation Reason': {
                        'Access Denied'
                    },
                    'Risk': 'Low',
                    'Savings': None
                }
                recommendations.append(temp)
                return recommendations
            logger.error("Something went wrong with region {}: {}".format(region, e))

    # print(available_instance_types)

    for instance_type, regions in available_instance_types.items():
        blacklist = []
        for up in possible_upgrade:
            if up[0] == instance_type and not up[1] in blacklist:
                blacklist.append(up[1])
                temp = {}
                regions = list(set(regions))

                for region in regions:
                    try:
                        response = get_savings(self, region, instance_type, up[1], 'Linux')
                        response['upgrade_from'] = instance_type
                        response['upgrade_to'] = up[1]
                        # print(response)
                        if response['Flag']:
                            temp = merge(temp, response)
                            # print(temp)

                    except botocore.exceptions.ClientError:
                        pass
                    except IndexError:
                        pass
                    # except Exception as e:
                    #     logger.error("Something went wrong {}".format(e))
                # print(temp)
                recommendations.append(temp)

    response = []
    for recommendation in recommendations:
        temp = {
            'Service Name': 'EC2 Instance',
            'Id': 'Generic',
            'Recommendation': 'Upgrade {} type instance to {} type'.format(recommendation['upgrade_from'], recommendation['upgrade_to']),
            'Description': 'The upgrade instance type recommendation checks for possible upgrades to reduce the costs.',
            'Metadata': {
                'Instance Type': recommendation['upgrade_from'],
                'Current Monthly Cost': recommendation['current_cost'],
                'Number of Instances': recommendation['Number of Instances'],
                'Estimated Savings in %': recommendation['Estimated Savings in %'],
                'Estimated Monthly Saving': recommendation['Estimated Monthly Saving'],
                'Effective Monthly cost': recommendation['Effective Monthly cost']
            },
            'Recommendation Reason': {
                'reason': "Instance types can be upgraded to save the cost"
            },
            'Risk': 'High',
            'Savings': '{:.2f}'.format(recommendation['Estimated Monthly Saving'])
        }
        response.append(temp)

    return response