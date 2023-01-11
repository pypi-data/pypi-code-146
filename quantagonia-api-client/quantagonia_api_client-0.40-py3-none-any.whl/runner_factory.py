import os, os.path
from decimal import InvalidOperation
from enum import Enum
from multiprocessing import connection
from sqlite3 import connect

from quantagonia.enums import HybridSolverServers, HybridSolverConnectionType
from quantagonia.cloud.cloud_runner import CloudRunner

_local_is_there__ = None
try:
	from quantagonia.local.local_runner import LocalRunner
	_local_is_there__ = True
except ModuleNotFoundError:
	_local_is_there__ = False


class RunnerFactory:

	@classmethod
	def getRunner(cls, connection : HybridSolverConnectionType, api_key : str = None, server : HybridSolverServers = HybridSolverServers.PROD, suppress_output : bool = False):

		if connection == HybridSolverConnectionType.CLOUD:
			return CloudRunner(api_key, server, suppress_output)

		if connection == HybridSolverConnectionType.LOCAL:
			if _local_is_there__:
				return LocalRunner(suppress_output)
			
			raise InvalidOperation("LocalRunner not supported in packaged version!")

		raise InvalidOperation("Unable to instantiate Quantagonia runner.")