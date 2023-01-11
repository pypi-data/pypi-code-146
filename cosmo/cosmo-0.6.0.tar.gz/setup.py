# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cosmo']

package_data = \
{'': ['*']}

install_requires = \
['isort>=5.10.1,<6.0.0', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'cosmo',
    'version': '0.6.0',
    'description': 'A web server implementation that uses raw sockets.',
    'long_description': '# Cosmo\n\nCosmo is an asynchronous python webserver that utilizes raw sockets to send and receive data, without using ASGI/WSGI.\n\n## Benchmarking\n\n![Connections Handled per Second](https://user-images.githubusercontent.com/44979306/191119603-e9b97cb1-b8dc-4cf0-8bf3-2a927dac8dac.png)\n\n## Examples\n\n### Simple Server\n\n```py\nfrom cosmo import App, Request, Response\n\napp = App("0.0.0.0", 8080)\n\n@app.route("/", "text/html")\nasync def index(request: Request):\n    return Response(f"<h1>{request.address}</h1>")\n\napp.serve()\n```\n\n### Using Custom Headers\n\n```py\nfrom cosmo import App, Request, Response\n\napp = App("0.0.0.0", 8080)\n\n@app.route("/", "text/html")\nasync def index(request: Request):\n    headers = {"x-custom-header": "custom"}\n    content = "<h1>Custom Headers: </h1>\\n<ul>"\n    for header in headers.keys():\n        content += f"<li>{header}: {headers[header]}</li>\\n"\n    content += "</ul>"\n    return Response(content, headers)\n\napp.serve()\n```\n\n### Returning an HTML Page\n\n```py\nfrom cosmo import App, html_page, Request, Response\n\napp = App("0.0.0.0", 8080)\n\n@app.route("/", "text/html")\nasync def index(request: Request):\n    return Response(html_page("path/to/page.html"))\n\napp.serve()\n```\n\n### Using Routes from a different file\n\nIn `router.py`:\n```py\nfrom cosmo import Request, Response, Router\n\nrouter = Router()\n\n@router.route("/")\nasync def index():\n    return Response("<h1>Hi</h1>")\n```\n\nIn `app.py`:\n```py\nfrom cosmo import App, Request, Response\n\nfrom router import router\n\napp = App("0.0.0.0", 8080)\n\napp.import_router(router)\n\napp.serve()\n```\n\n## Docs\n\nComing soon...\n',
    'author': 'Kronifer',
    'author_email': '44979306+Kronifer@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kronifer/cosmo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
