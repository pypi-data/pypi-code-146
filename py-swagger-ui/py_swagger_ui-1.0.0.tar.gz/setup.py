# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_swagger_ui']

package_data = \
{'': ['*'],
 'py_swagger_ui': ['vendor/swagger-ui-4.15.5/*', 'vendor/swagger-ui-4.4.0/*']}

install_requires = \
['Jinja2>=2.0,<3.0']

setup_kwargs = {
    'name': 'py-swagger-ui',
    'version': '1.0.0',
    'description': 'Swagger UI bundled for usage with Python',
    'long_description': 'py_swagger_ui\n=============\nThis package contains the static files for swagger-ui as a python package.\n\nBasic configuration options are templated with the Jinja2 templating language.\n\nThis package is intended to be webserver-agnostic, so it only includes the\nstatic files, and some very basic configuration.\n\nGetting Started\n===============\nYou can import the swagger_ui_path from the py_swagger_ui package like so:\n\n.. code-block:: python\n  \n    from py_swagger_ui import swagger_ui_path\n\nYou can easily serve up this directory as all static files to get the default\nswagger-ui distribution. Here\'s an example in flask:\n\n.. code-block:: python\n\n    from py_swagger_ui import swagger_ui_path\n    \n    from flask import Flask, Blueprint, send_from_directory, render_template\n    \n    swagger_bp = Blueprint(\n        \'swagger_ui\',\n        __name__,\n        static_url_path=\'\',\n        static_folder=swagger_ui_path,\n        template_folder=swagger_ui_path\n    )\n    \n    app = Flask(__name__, static_url_path=\'\')\n    app.register_blueprint(swagger_bp, url_prefix=\'/ui\')\n    \n    if __name__ == "__main__":\n        app.run()\n\nYou may wish to override some of the configuration variables. Included\nis a jinaj2 templated file where you can modify these parameters.\nYou can add another route to render this template with your\ndesired configuration like so:\n\n.. code-block:: python\n\n    SWAGGER_UI_CONFIG = {\n        "openapi_spec_url": "https://petstore.swagger.io/v2/swagger.json"\n    }\n\n    @swagger_bp.route(\'/\')\n    def swagger_ui_index():\n        return render_template(\'index.j2\', **SWAGGER_UI_CONFIG)\n\n\nHave a look at `example.py` for a complete server for the Flask webserver.\n\n\nLicense\n=======\nSince this is just repackaging swagger-ui releases, the license comes from\nthe swagger ui project (https://github.com/swagger-api/swagger-ui).\n\nAll vendored code is published under the Apache 2.0 License.\n',
    'author': 'Robbe Sneyders',
    'author_email': 'robbe.sneyders@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/spec-first/py-swagger-ui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
