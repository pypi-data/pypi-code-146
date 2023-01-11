import datetime

import yaml


class PythonMLmodelTemplate(yaml.YAMLObject):

    def noop(self, *args, **kw):
        pass

    yaml.emitter.Emitter.process_tag = noop

    # If we have additional flavors provided by the user we can add a parameter here of the form
    # {<flavor name>:{dict containing flavor}, <flavor name>:{dict containing flavor}}
    def __init__(self, wrapper_file_name, model_data_path, python_version=None):
        python_version = python_version or "3.7.3"

        if python_version.startswith("python="):
            python_version = python_version[7:]

        python_function = {
            "code": "code",
            "data": model_data_path,
            "env": "conda.yaml",
            "loader_module": wrapper_file_name,
            "python_version": python_version
        }

        self.flavors = {"python_function": python_function}
        self.utc_time_created = datetime.datetime.utcnow().isoformat()
