from dateutil.relativedelta import relativedelta
import datetime as dt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns the list of instances
def list_instances(self, region) -> list:
    client = self.session.client('ec2', region_name=region)
    instance_lst = []
    marker = ''
    while True:
        response = client.describe_instances(
            MaxResults=1000,
            NextToken=marker
        )
        for i in response['Reservations']:
            for instance in i['Instances']:
                state = instance['State']['Name']
                if not state == 'terminated':
                    instance_lst.append(instance)

        try:
            marker = response['NextToken']
            if marker == '':
                break
        except KeyError:
            break

    return instance_lst


# returns the list of rds instances
def list_rds_instances(self, region) -> list:
    client = self.session.client('rds', region_name=region)

    rds_instance_lst = []
    marker = ''
    while True:
        response = client.describe_db_instances(
            MaxRecords=100,
            Marker=marker
        )
        rds_instance_lst.extend(response['DBInstances'])

        try:
            marker = response['Marker']
            if marker == '':
                break
        except KeyError:
            break
    return rds_instance_lst


# returns the metrics data
def get_metrics_stats(self, region: str, namespace: str, dimensions: list,
                      metric_name='CPUUtilization', start_time=dt.datetime.utcnow() - relativedelta(days=7),
                      end_time=dt.datetime.utcnow(), period=86400, stats=None, unit='Percent'):
    if stats is None:
        stats = ["Average"]

    client = self.session.client('cloudwatch', region_name=region)

    if unit is None:
        response_cpu = client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=stats,
            Dimensions=dimensions
        )
    else:
        response_cpu = client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=stats,
            Unit=unit,
            Dimensions=dimensions
        )
    return response_cpu


# returns the list of redshift clusters
def list_redshift_clusters(client) -> list:
    """
    :param client:
    :return:
    """
    logger.info(" ---Inside utils() :: list_redshift_clusters()")

    cluster_list = []

    marker = ''
    while True:
        if marker == '' or marker is None:
            response = client.describe_clusters()
        else:
            response = client.describe_clusters(
                Marker = marker
            )
        cluster_list.extend(response['Clusters'])

        try:
            marker = response['Marker']
            if marker == '':
                break
        except KeyError:
            break

    return cluster_list