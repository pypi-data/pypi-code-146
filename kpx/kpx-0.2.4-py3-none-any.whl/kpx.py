#!/usr/bin/env python3

import configparser
import typer
import boto3
import os

from os.path import expanduser
from typing import Optional
from prettytable import PrettyTable

app = typer.Typer(help="KPC application for aws profiles", no_args_is_help=True)


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0

    return f"{num:.1f}Yi{suffix}"

class IniUtils:
    # @staticmethod
    # def show_file_content(content):
    #     output = ''
    #     for key in content:
    #         output += f"[{key}]\n"
    #         for item in content[key]:
    #             output += f"{item} = {content[key][item]}\n"
    #
    #         output += "\n"
    #
    #     return output

    @staticmethod
    def check_directory_exists(file_path):
        os.makedirs(file_path, exist_ok=True)

class Output:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def header(text):
        print(f'{Output.HEADER}{text}{Output.ENDC}')

    @staticmethod
    def success(text):
        print(f'{Output.OKGREEN}{text}{Output.ENDC}')

    @staticmethod
    def error(text):
        print(f'{Output.FAIL}{text}{Output.ENDC}')


class AwsConfigManager:
    def __init__(self, file_credentials, file_config):
        self.file_credentials = file_credentials
        self.file_config = file_config

        self.creds = configparser.ConfigParser()
        self.creds.read(file_credentials)

        self.cfg = configparser.ConfigParser()
        self.cfg.read(file_config)

    def update_credentials(self, profile, access_key, secret_key):
        if profile not in self.creds:
            self.creds.update({profile: {
                'aws_access_key_id': '',
                'aws_secret_access_key': '',
            }})

        for key in self.creds[profile]:
            new_value = ''
            if key == 'aws_access_key_id' and access_key is not None:
                new_value = access_key
            if key == 'aws_secret_access_key' and secret_key is not None:
                new_value = secret_key

            self.creds[profile][key] = new_value

        return self

    def update_config(self, profile, region, output):
        if profile != 'default':
            profile = f'profile {profile}'

        self.cfg.update({
            profile: {
                'region': region,
                'output': output,
            }
        })

    def get_credentials(self, profile_name):
        data = {}
        if profile_name in self.creds:
            for key in self.creds[profile_name]:
                data.update({key: self.creds[profile_name][key]})

        return data

    def get_config(self, profile_name):
        data = {}
        profile_string = f'profile {profile_name}' if profile_name != 'default' else 'default'
        if profile_string in self.cfg:
            for key in self.cfg[profile_string]:
                data.update({key: self.cfg[profile_string][key]})

        return data

    def write_credentials_file(self):
        with open(self.file_credentials, 'w') as file:
            self.creds.write(file)

        return self

    def write_config_file(self):
        with open(self.file_config, 'w') as file:
            self.cfg.write(file)

        return self


class AwsResourceQuery:
    def __init__(self, client):
        self.client = client

    def get_table_header(self):
        return ["ID", "Name", "Type", "PrivateIP", "PublicIP", "State"]

    @staticmethod
    def get_instance_name_from_tags(tags):
        for item in tags:
            if item['Key'] == 'Name':
                return item['Value']

        return '---'

    def list_ec2_instances(self):
        instances = []
        try:
            resp = self.client.describe_instances()
        except Exception as e:
            Output.error(e)
            return []

        for reservation in resp['Reservations']:
            for instance in reservation['Instances']:
                # print(instance)
                data = {
                    'id': instance['InstanceId'],
                    'name': self.get_instance_name_from_tags(instance['Tags']),
                    'type': instance['InstanceType'],
                    'PrivateIp': instance['PrivateIpAddress'] if 'PrivateIpAddress' in instance else '-',
                    'PublicIp': instance['PublicIpAddress'] if 'PublicIpAddress' in instance else '-',
                    'state': instance['State']['Name'],
                }

                instances.append(data.values())

        return instances


class ContainerRegistry:
    def __init__(self, client):
        self.client = client

    def get_images(self, repo_name, account_id):
        if repo_name != '':
            response = self.client.list_images(
                registryId=account_id,
                repositoryName=repo_name,
                maxResults=123,
                filter={
                    'tagStatus': 'ANY'
                }
            )

            table = PrettyTable()
            table.field_names = ['Tag', 'Digest', 'Size']
            table.align['Tag'] = 'l'
            table.align['Digest'] = 'l'

            for img in response['imageIds']:
                data = self.get_image_metadata(repo_name, account_id, img['imageDigest'])

                table.add_row([
                    img['imageTag'],
                    img['imageDigest'],
                    sizeof_fmt(data['imageSizeInBytes'])
                ])

            print(table.get_string())

    def get_image_metadata(self, repo_name, account_id, image_digest):
        response = self.client.describe_images(
            registryId=account_id,
            repositoryName=repo_name,
            imageIds=[
                {
                    'imageDigest': image_digest,
                },
            ],
            filter={
                'tagStatus': 'ANY'
            }
        )

        return response['imageDetails'][0]

    def get_repositories(self):
        response = self.client.describe_repositories()

        table = PrettyTable()
        table.field_names = ['Name', 'Url']
        table.align['Name'] = 'r'
        table.align['Url'] = 'l'

        for repo in response['repositories']:
            table.add_row([
                repo['repositoryName'],
                repo['repositoryUri']
            ])

        print(table.get_string())


@app.command()
def cfg(
        aws_profile: Optional[str] = typer.Argument('default'),
        region: Optional[str] = typer.Argument("us-east-1"),
        output: Optional[str] = typer.Argument("json")
):
    """
    Configure ~/.aws/config file with profiles settings
    """
    Output.header('Updating ~/.aws/config file')
    user_home_directory = expanduser('~')

    awc = AwsConfigManager(
        f'{user_home_directory}/.aws/credentials',
        f'{user_home_directory}/.aws/config',
    )

    IniUtils.check_directory_exists(f'{user_home_directory}/.aws/')

    awc.update_config(aws_profile, region, output)
    awc.write_config_file()


@app.command()
def cred(
        aws_profile: Optional[str] = typer.Argument('default'),
        key: Optional[str] = typer.Argument(""),
        secret: Optional[str] = typer.Argument("")
):
    """
    Configure ~/.aws/credentials file with aws credentials
    """
    Output.header('Updating ~/.aws/credentials file')
    user_home_directory = expanduser('~')

    awc = AwsConfigManager(
        f'{user_home_directory}/.aws/credentials',
        f'{user_home_directory}/.aws/config',
    )

    IniUtils.check_directory_exists(f'{user_home_directory}/.aws/')

    awc.update_credentials(aws_profile, key, secret)
    awc.write_credentials_file()


@app.command()
def r53(zone_id: Optional[str] = typer.Argument('')):
    """
    List Route53 hosted zones
    """
    client = boto3.client('route53')

    if zone_id != '':
        Output.header(f'List Records for ZoneID: {zone_id}')
        resp = client.list_resource_record_sets(
            HostedZoneId=zone_id
        )

        table = PrettyTable()
        table.field_names = ["Name", "Type", "Targets"]
        table.align['Name'] = 'r'
        table.align['Targets'] = 'l'

        for rec in resp['ResourceRecordSets']:
            if 'AliasTarget' in rec:
                table.add_row([
                    rec['Name'].strip('.'),
                    rec['Type'],
                    '(alias) ' + rec['AliasTarget']['DNSName'].strip('.')[:128]
                ])

            if 'ResourceRecords' in rec:
                table.add_row([
                    rec['Name'].strip('.'),
                    rec['Type'],
                    '\n'.join([d['Value'][:128] for d in rec['ResourceRecords']])
                ])

        print(table.get_string())
        return None

    account_id = boto3.client('sts').get_caller_identity().get('Account')

    try:
        resp = client.list_hosted_zones()

        table = PrettyTable()
        table.field_names = ["Domain", "Id", "Records"]
        table.align['Domain'] = 'r'

        if len(resp['HostedZones']) > 0:
            for zone in resp['HostedZones']:
                table.add_row([
                    zone['Name'].strip('.'),
                    zone['Id'].replace('/hostedzone/', ''),
                    zone['ResourceRecordSetCount']
                ])
            print(f'\nAccount id: {account_id}')
            print(table.get_string())
        else:
            Output.error(f'No hosted zones in account: {account_id}')
    except Exception as e:
        Output.error(e)


@app.command()
def ecr(repo_name: Optional[str] = typer.Argument('')):
    """
    List ECR repositories
    """
    client = boto3.client('ecr')

    account_id = boto3.client('sts').get_caller_identity().get('Account')

    ecr = ContainerRegistry(client)

    if repo_name != '':
        ecr.get_images(repo_name, account_id)
    else:
        ecr.get_repositories()


@app.command()
def ec2():
    """
    List EC2 instances
    """
    client = boto3.client('ec2')
    arq = AwsResourceQuery(client)

    table = PrettyTable()
    table.field_names = arq.get_table_header()
    table.align['PrivateIP'] = 'r'
    table.align['PublicIP'] = 'r'
    table.align['Name'] = 'r'

    ec2_instances = arq.list_ec2_instances()
    if len(ec2_instances) > 0:
        table.add_rows(ec2_instances)
        print(table.get_string())


@app.command()
def vpc():
    """
    List VPCs and show Cidr blocks
    """
    client = boto3.client('ec2', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    vpcs = client.describe_vpcs()

    table = PrettyTable()
    table.field_names = ['VPC Id', 'Name', 'Cidr']

    for vpc in vpcs['Vpcs']:
        table.add_row([
            vpc['VpcId'],
            AwsResourceQuery.get_instance_name_from_tags(vpc['Tags']) if 'Tags' in vpc else '-',
            vpc['CidrBlock']
        ])

    print(table.get_string())


if __name__ == '__main__':  # pragma: no cover
    app()
