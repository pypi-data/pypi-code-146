# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['intelliprove',
 'intelliprove.api',
 'intelliprove.api.exceptions',
 'intelliprove.api.models',
 'intelliprove.api.models.dataclasses',
 'intelliprove.api.models.responses',
 'intelliprove.api.utils']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.7.0.68,<5.0.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'intelliprove',
    'version': '0.1.2',
    'description': '',
    'long_description': '<h1 align="center"> IntelliProve Python SDK</h1>\n\n<div align="center">\n    <img src="https://img.shields.io/pypi/dm/intelliprove" />\n    <img src="https://img.shields.io/pypi/pyversions/intelliprove" />\n    <img src="https://img.shields.io/badge/version-0.1.2-blue" />\n</div>\n\n## Requirements\n\n- Python ^3.9\n\n## Installation\n```pip install intelliprove```\n\n## Example usage\n\n```python\nimport os\nfrom pathlib import Path\n\nfrom intelliprove.api import IntelliproveApi, IntelliproveApiSettings, Biomarkers, Quality\n\n# define api key and settings\napikey = os.environ.get(\'apikey\', \'api-key-123\')\nsettings = IntelliproveApiSettings(\n    base_url=\'\'\n)\n\n# init api\napi = IntelliproveApi(apikey, settings)\n\n# define the path of the video you want to upload\nvideo_path = Path(\'./mydir/example.mp4\')\nimage_path = Path(\'./mydir/example.png\')\n\n# manually check quality of a video of image\nquality: Quality = api.check_conditions(video_path)\nquality: Quality = api.check_conditions(image_path)\n\n# Optional: define the performer and patient\nperformer: str = \'performer-a\'\npatient: str = \'patient-1\'\n\n# upload video to IntelliProve\n# performer and patient are optional\nuuid: str = api.upload(video_path)\n# or\nuuid: str = api.upload(video_path, performer=performer, patient=patient)\n\n# get the results of the uploaded video\nresults: Biomarkers = api.get_results(uuid)\n```\n\n### Dataclasses\n- Biomarkers\n  - contains the results of an uploaded video\n- Quality\n  - contains the quality parameters of a video or image\n\n### Exceptions\n- ImageQualityException\n- MediaException\n- InvalidUuidException\n- ApiException\n  - ApiNotFoundException\n  - ApiForbiddenException\n  - ApiErrorException\n  - ApiResultNotAvailable',
    'author': 'Seppe De Langhe',
    'author_email': 'seppe.delanghe@intelliprove.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
