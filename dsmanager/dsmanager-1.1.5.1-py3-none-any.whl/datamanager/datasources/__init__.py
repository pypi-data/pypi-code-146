"""@Author: Rayane AMROUCHE

The DataSource component is handling the different data source and is managed with
plugins sources inheriting the DataSource class.
"""

from dsmanager.datamanager.datasources.datasource import DataSource
from dsmanager.datamanager.datasources.filesource import FileSource
from dsmanager.datamanager.datasources.ftpsource import FtpSource
from dsmanager.datamanager.datasources.httpsource import HttpSource
from dsmanager.datamanager.datasources.kagglesource import KaggleSource
from dsmanager.datamanager.datasources.sfsource import SFSource
from dsmanager.datamanager.datasources.sharepointsource import SharepointSource
from dsmanager.datamanager.datasources.sqlsource import SqlSource
from dsmanager.datamanager.datasources.sshsource import SshSource
