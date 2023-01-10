#  Copyright (c) 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import multiprocessing as mp
import signal
import time
from multiprocessing import Process
from queue import Empty

from flask import Flask, request
from gevent.pywsgi import WSGIServer
from setproctitle import setproctitle

from healthcheck_python.release import __version__


class HealthCheckApi(Process):
	"""
	API responder class
	Creates a flask instance and reports the health status
	"""

	def __init__(self, host: str, port: int, status_queue: mp.Queue, daemon: bool = False):
		super().__init__()

		self._host: str = host
		self._port: int = port
		self._status_queue: mp.Queue = status_queue
		self.daemon: bool = daemon

		self._app = Flask(__name__)

		self._app.add_url_rule('/', 'index', view_func=HealthCheckApi._index)
		self._app.add_url_rule('/health', 'health', view_func=self._health)

		self._http_server = WSGIServer((self._host, self._port), self._app)

	def exit_gracefully(self, signum, frame):
		self._http_server.close()

	def run(self):
		setproctitle(self.__class__.__name__)

		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)

		self._http_server.serve_forever()

	@staticmethod
	def _index():
		return f"Hello there! I'm healthcheck-python v{__version__}"

	def _get_status(self) -> dict:
		"""
		Get a single valid message from queue
		:return: dict
		"""
		while True:
			try:
				status = self._status_queue.get(block=True, timeout=1)
				if time.time() - status[0] <= 0.5:
					status = status[1]
					break
			except Empty:
				status = {'status': False, 'services': {}}
				break

		return status

	def _ready(self):
		"""
		Readiness check path
		/health
		:return: overall readiness str(boolean).
		:return: If verbose mode enabled, return a dict with details about every service
		"""
		is_verbose = "v" in request.args.keys()

		status_message = self._get_status()

		if is_verbose:
			return status_message

		return {'ready': status_message['ready']}

	def _health(self):
		"""
		Health check path
		/health
		:return: overall status str(boolean).
		:return: If verbose mode enabled, return a dict with details about every service
		"""
		is_verbose = "v" in request.args.keys()

		status_message = self._get_status()

		if is_verbose:
			return status_message

		return {'status': status_message['status']}
