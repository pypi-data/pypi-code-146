#!python
'''Environmental Shell Piping
Supplies some utility functions to handle complex data structures as
environmental shell variables. Useful to docker and other CLI tools requiring lots of dynamic data
'''

import base64
import json
import logging
import pathlib
import shlex

import simplifiedapp

__version__ = '0.1.1'

LOGGER = logging.getLogger(__name__)


def _pack_path(path_to_pack):
	'''Packs a path recursively
	Returns the file content encoded or creates a directory entry (a dict) and calls itself for each child.
	'''

	if path_to_pack.is_dir():
		result = {child_path.name : _pack_path(child_path) for child_path in path_to_pack.iterdir()}
	elif path_to_pack.is_file():
		result = base64.b64encode(path_to_pack.read_bytes()).decode('utf-8')
	else:
		raise ValueError('Not a packable path: {}'.format(path_to_pack))

	return result

def _unpack_path(tree_node, parent_path):
	'''Unpacks a path recursively
	Writes the content of the encoded file or creates a directory and calls itself for each child.
	'''

	parent_path = pathlib.Path(parent_path)
	if not isinstance(tree_node, dict):
		raise ValueError('Malformed path pack')

	result = []
	for name, content in tree_node.items():
		content_path = parent_path / name
		if isinstance(content, str):
			content_path.write_bytes(base64.b64decode(content))
			result.append(content_path)
		elif isinstance(content, dict):
			content_path.mkdir()
			result.append(content_path)
			result += _unpack_path(content, content_path)
		else:
			raise ValueError('Malformed path pack')

	return result


class EnvironmentalPipes:
	'''Pipe data via environmental variables
	Several utility tools to handle complex data structures as environmental variables.
	'''

	@staticmethod
	def pack_path(*paths_to_pack, base64_result = False, quote_result = False):
		'''Content in paths as JSON
		Packs the content from the paths provided into a JSON object.
		'''

		result = {}
		for path_to_pack in paths_to_pack:
			target_path = pathlib.Path(path_to_pack)
			if target_path.exists():
				LOGGER.debug('Working with path: %s', target_path)
			else:
				raise ValueError("The path does not exists or you can't access it: {}".format(target_path))

			result[target_path.name] = _pack_path(target_path)

		result = json.dumps(result)
		if base64_result:
			result = base64.b64encode(result.encode('utf-8')).decode('utf-8')
		if quote_result:
			result = shlex.quote(result)

		return result

	@staticmethod
	def unpack_path(destination, content_file, create_destination = False, base64_decode = False):
		'''Unpack JSON content into a directory
		Unpacks a JSON object created with "pack_path" into a directory
		'''

		destination_path = pathlib.Path(destination)
		if destination_path.is_dir():
			LOGGER.debug('Working with directory: %s', destination_path)
		elif create_destination:
			if destination_path.exists():
				raise ValueError("Can't create directory on existing path: {}".format(destination_path))
			else:
				LOGGER.debug('Creating directory: %s', destination_path)
				destination_path.mkdir(parents = True)
		else:
			raise ValueError('"{}" is not a directory that you can access'.format(destination))

		if content_file == '-':
			content = input()
			if base64_decode:
				content = base64.b64decode(content.encode('utf-8')).decode('utf-8')
		else:
			content_file_path = pathlib.Path(content_file)
			try:
				if base64_decode:
					content = base64.b64decode(content_file_path.read_bytes()).decode('utf-8')
				else:
					content = content_file_path.read_text()
			except Exception as error:
				raise RuntimeError('An error ocurred while reading the content file')

		content = json.loads(content)
		result = _unpack_path(content, destination_path)

		return result

	@staticmethod
	def vars_from_file(file_with_vars, sep = ' '):
		'''Env variables from file
		Parses a file containing the variables and prints a line, ready to be fed to "env". The file MUST be a JSON file, for now.
		'''

		file_with_vars = pathlib.Path(file_with_vars)
		if file_with_vars.is_file():
			LOGGER.debug('Working with file: %s', file_with_vars)
		else:
			raise ValueError('"{}" is not a file that you can access'.format(file_with_vars))

		result = []

		#ToDo: Need some logic to detect file format. Assuming JSON for the time being.
		content = json.loads(file_with_vars.read_text())
		for key, value in content.items():
			if isinstance(value, (list, dict)):
				value = json.dumps(value)
			value = shlex.quote(str(value))
			result.append('='.join([key, value]))

		return sep.join(result)
