#!/usr/bin/env python3
"""
Cassandra cli tool
"""
import click
import os
import boto3
import re
import shutil
import time
import python_cassandra_cli.constant as constant
from python_cassandra_cli.restore_snapshot_table import RestoreSnapshotTable
from python_cassandra_cli.restore_snapshot_keyspace import RestoreSnapshotKeyspace
from python_cassandra_cli.copy_snapshot_folder import CopySnapshotFolder
from python_cassandra_cli.store_snapshot_keyspace import StoreSnapshotKeyspace
from python_cassandra_cli.store_snapshot_table import StoreSnapshotTable



@click.group()
def cli():
    pass

@cli.command(help='Take and store Keyspace snapshot to s3 bucket')
@click.option('-k' ,'--keyspace', 'keyspace', required = True, help = constant.KEYSPACE_OPTION)
@click.option('-t' ,'--snapshot-tag', 'tag', required = True, help = constant.SNAPSHOT_TAG_OPTION)
@click.option('-s3' ,'--s3-bucket', 's3', required = True, help = constant.S3_BUCKET_OPTION)
@click.option('-id' ,'--aws-access-key-id', 'id', help = constant.AWS_ACCESS_KEY_ID_OPTION)
@click.option('-key' ,'--aws-secret-access-key', 'key', help = constant.AWS_SECRET_ACCESS_KEY_OPTION)
@click.option('-r' ,'--aws-region', 'region', default = 'us-east-1',help = constant.AWS_REGION_OPTION)
@click.option('-e' ,'--environment', 'environment', required = True, help = constant.ENVIRONMENT_OPTION)
@click.option('-cks' ,'--create-keyspace-schema', 'schema', is_flag = True , help = constant.ENVIRONMENT_OPTION)
@click.option('-h' ,'--cassandra-host', 'host' , help = constant.CASSANDRA_HOST_OPTION)
@click.option('-u' ,'--cassandra-user', 'user', default = 'cassandra' , help = constant.CASSANDRA_USER_OPTION)
@click.option('-p' ,'--cassandra-password', 'password', default = 'cassandra'  ,help = constant.CASSANDRA_PASSWORD_OPTION)
@click.option('--no-clear-snapshot', is_flag = True, help = constant.NO_CLEAR_SNAOSHOT_OPTION)
@click.option('--ssm-secret', is_flag = True, help = constant.SSM_SECRET_OPTION)
@click.option('-sn' ,'--secret-name', help = constant.SECRET_NAME_OPTION)

def store_snapshot_keyspace(keyspace, s3, id, key, tag, environment, schema, host, user, password, no_clear_snapshot, ssm_secret, region,secret_name):

    store_snapshot = StoreSnapshotKeyspace(keyspace, s3, id, key, tag, environment, schema, host, user, password, no_clear_snapshot, ssm_secret, region,secret_name)

    store_snapshot.store_snapshot_keyspace()

@cli.command(help='Take and store Table snapshot to s3 bucket')
@click.option('-k' ,'--keyspace', 'keyspace', required = True, help = constant.KEYSPACE_OPTION)
@click.option('-tn' ,'--table-name', required = True,  help = constant.TABLE_NAME_OPTION)
@click.option('-t' ,'--snapshot-tag', 'tag', required = True, help = constant.SNAPSHOT_TAG_OPTION)
@click.option('-s3' ,'--s3-bucket', 's3', required = True, help = constant.S3_BUCKET_OPTION)
@click.option('-id' ,'--aws-access-key-id', 'id', help = constant.AWS_ACCESS_KEY_ID_OPTION)
@click.option('-key' ,'--aws-secret-access-key', 'key', help=constant.AWS_SECRET_ACCESS_KEY_OPTION)
@click.option('-r' ,'--aws-region', 'region', default = 'us-east-1', help= constant.AWS_REGION_OPTION )
@click.option('-e' ,'--environment', 'environment', required = True,  help = constant.ENVIRONMENT_OPTION)
@click.option('-cks' ,'--create-keyspace-schema', 'schema', is_flag = True , help = constant.CREATE_KEYSPACE_SCHEMA_OPTION)
@click.option('-h' ,'--cassandra-host', 'host', help = constant.CASSANDRA_HOST_OPTION)
@click.option('-u' ,'--cassandra-user', 'user', default = 'cassandra' , help = constant.CASSANDRA_USER_OPTION)
@click.option('-p' ,'--cassandra-password', 'password', default = 'cassandra' , help = constant.CASSANDRA_PASSWORD_OPTION)
@click.option('--no-clear-snapshot', is_flag = True, help = constant.NO_CLEAR_SNAOSHOT_OPTION)
@click.option('--ssm-secret', is_flag = True, help = constant.SSM_SECRET_OPTION)
@click.option('-sn' ,'--secret-name', help = constant.SECRET_NAME_OPTION)

def store_snapshot_table(keyspace, table_name, s3, id, key, tag, environment, schema, host, user, password, no_clear_snapshot, ssm_secret, region, secret_name):

    store_snapshot = StoreSnapshotTable(keyspace, table_name, s3, id, key, tag, environment, schema, host, user, password, no_clear_snapshot, ssm_secret, region,secret_name)

    store_snapshot.store_snapshot_table()


@cli.command(help='Restore Table snapshot from s3 bucket')
@click.option('-s3' ,'--s3-bucket', 's3', required = True, help = constant.S3_BUCKET_OPTION)
@click.option('-id' ,'--aws-access-key-id', 'id', help = constant.AWS_ACCESS_KEY_ID_OPTION)
@click.option('-key' ,'--aws-secret-access-key', 'key', help = constant.AWS_SECRET_ACCESS_KEY_OPTION)
@click.option('-tn' ,'--table-name', required = True,  help = constant.TABLE_NAME_OPTION)
@click.option('-t' ,'--snapshot-tag', 'tag', required = True, help = constant.SNAPSHOT_TAG_OPTION)
@click.option('-sf' ,'--snapshot-folder', required = True, help = constant.SNAPSHOT_FOLDER_OPTION)
@click.option('-k' ,'--keyspace', 'keyspace', required = True, help = constant.KEYSPACE_OPTION)
@click.option('-ssl' ,'--ssl-connection', is_flag = True, help = constant.SSL_CONNECTION_OPTION)
@click.option('-h' ,'--cassandra-host', 'host', required = True, help = constant.CASSANDRA_HOST_OPTION)
@click.option('-u' ,'--cassandra-user', 'user', default = 'cassandra' , help = constant.CASSANDRA_USER_OPTION)
@click.option('-p' ,'--cassandra-password', 'password', default = 'cassandra' , help = constant.CASSANDRA_PASSWORD_OPTION)
@click.option('-pt' ,'--cassandra-port' , help = constant.CASSANDRA_PORT_OPTION)
@click.option('-cf' ,'--cassandra-config-file' , help= constant.CASSANDRA_CONFIG_FILE_OPTION)
@click.option('-ks' ,'--cassandra-keystore' , help = constant.CASSANDRA_KEYSTORE_OPTION)
@click.option('-ts' ,'--cassandra-truststore' , help = constant.CASSANDRA_TRUSTSTORE_OPTION)
@click.option('--ssm-secret', is_flag = True, help = constant.SSM_SECRET_OPTION)
@click.option('-sn' ,'--secret-name', help = constant.SECRET_NAME_OPTION)
@click.option('-r' ,'--aws-region', 'region', default = 'us-east-1', help = constant.AWS_REGION_OPTION)

def restore_snapshot_table(s3, id, key, tag, keyspace, region, table_name, snapshot_folder, host, user, password, 
    cassandra_config_file, cassandra_keystore, cassandra_truststore, cassandra_port, ssl_connection, ssm_secret, secret_name):

    restore_snapshot = RestoreSnapshotTable(s3, id, key, tag, keyspace, region, table_name, snapshot_folder, host, user, password,
        cassandra_config_file, cassandra_keystore, cassandra_truststore, cassandra_port, ssl_connection, ssm_secret, secret_name)

    restore_snapshot.restore_snapshot_table()

@cli.command(help='Restore Keyspace snapshot from s3 bucket')
@click.option('-s3' ,'--s3-bucket', 's3', required = True, help = constant.S3_BUCKET_OPTION)
@click.option('-id' ,'--aws-access-key-id', 'id', help = constant.AWS_ACCESS_KEY_ID_OPTION)
@click.option('-key' ,'--aws-secret-access-key', 'key', help = constant.AWS_SECRET_ACCESS_KEY_OPTION)
@click.option('-cks' ,'--create-keyspace-schema', 'schema', is_flag = True , help = constant.CREATE_KEYSPACE_SCHEMA_OPTION)
@click.option('-t' ,'--snapshot-tag', 'tag', required = True, help = constant.SNAPSHOT_TAG_OPTION)
@click.option('-sf' ,'--snapshot-folder', required = True, help = constant.SNAPSHOT_FOLDER_OPTION)
@click.option('-k' ,'--keyspace', 'keyspace', required = True, help = constant.KEYSPACE_OPTION)
@click.option('-e' ,'--environment', 'environment', required = True, help = constant.ENVIRONMENT_OPTION)
@click.option('-ssl' ,'--ssl-connection', is_flag = True, help = constant.SSL_CONNECTION_OPTION)
@click.option('-h' ,'--cassandra-host', 'host', required = True, help = constant.CASSANDRA_HOST_OPTION)
@click.option('-u' ,'--cassandra-user', 'user', default = 'cassandra' , help = constant.CASSANDRA_USER_OPTION)
@click.option('-p' ,'--cassandra-password', 'password', default = 'cassandra' , help = constant.CASSANDRA_PASSWORD_OPTION)
@click.option('-pt' ,'--cassandra-port' , help= constant.CASSANDRA_PORT_OPTION)
@click.option('-cf' ,'--cassandra-config-file' ,help = constant.CASSANDRA_CONFIG_FILE_OPTION)
@click.option('-ks' ,'--cassandra-keystore' , help = constant.CASSANDRA_KEYSTORE_OPTION)
@click.option('-ts' ,'--cassandra-truststore' , help = constant.CASSANDRA_TRUSTSTORE_OPTION)
@click.option('--ssm-secret', is_flag = True, help = constant.SSM_SECRET_OPTION)
@click.option('-sn' ,'--secret-name', help = constant.SECRET_NAME_OPTION)
@click.option('-r' ,'--aws-region', 'region', default = 'us-east-1', help = constant.AWS_REGION_OPTION)


def restore_snapshot_keyspace(s3, id, key, tag, keyspace, region, schema, snapshot_folder, host, user, password, 
    cassandra_config_file, cassandra_keystore, cassandra_truststore, cassandra_port, ssl_connection, ssm_secret, secret_name, environment):

    restore_snapshot = RestoreSnapshotKeyspace(s3, id, key, tag, keyspace, region, schema, snapshot_folder, host, user, password,
        cassandra_config_file, cassandra_keystore, cassandra_truststore, cassandra_port, ssl_connection, ssm_secret, secret_name, environment)

    restore_snapshot.restore_snapshot_keyspace()

@cli.command(help='Copy folder with snapshots from s3 bucket')
@click.option('-s3' ,'--s3-bucket', 's3', required = True, help = constant.S3_BUCKET_OPTION)
@click.option('-id' ,'--aws-access-key-id', 'id', help = constant.AWS_ACCESS_KEY_ID_OPTION)
@click.option('-key' ,'--aws-secret-access-key', 'key', help = constant.AWS_SECRET_ACCESS_KEY_OPTION)
@click.option('-sf' ,'--snapshot-folder', required = True, help = constant.SNAPSHOT_FOLDER_OPTION)

def copy_snapshot_folder(s3, id, key, snapshot_folder):

    copy_snapshot = CopySnapshotFolder(s3, id, key, snapshot_folder)

    copy_snapshot.copy_snapshot_folder(); 

if __name__ == '__main__':
    cli()



