from databricks_dbapi import hive
from .singleton import Singleton

class SingletonClusterThriftClient():

    """
        Class that creates, maintains and serves singleton client to the Databricks cluster's Thrift server, primary functionality
        of this is to makes sure that for any <host,http_path,token> combination has a single client
    """

    def __init__(self, host, http_path, token):
        self.client = hive.connect(host=host, http_path=http_path, token=token)