# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['earhorn']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'httpx>=0.23.0,<0.24.0',
 'loguru>=0.5.3,<0.7.0',
 'lxml>=4.6.3,<4.10.0',
 'prometheus-client>=0.15.0,<0.16.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'typing-extensions>=4.2.0,<5.0.0']

extras_require = \
{'s3': ['boto3>=1.24.8,<2.0.0']}

entry_points = \
{'console_scripts': ['earhorn = earhorn.main:cli']}

setup_kwargs = {
    'name': 'earhorn',
    'version': '0.14.0a0',
    'description': 'Listen, monitor and archive your streams!',
    'long_description': '# earhorn\n\nListen, monitor and archive your streams!\n\n[![](https://mermaid.ink/svg/pako:eNqNlD9PwzAQxb_KySNqFySWqCoDMLAw0AEhgiorvhIriV1dnAJCfHcuzj8nzsDmvHv383Muzo_IrEKRiNpJh_dafpCstpfr1AB4CVJxcJIc4AWNg1waVSKlAmTdGsgdB4k73q7eYbvdLwsx7Ey2QpdjU4ekQO06JkiADV0TWZ-O7aI-NlTCbpflVme436-DQnMCj35_V0PbqvCkDSq4jUN3ppU34AutfxZiSuy1BF4xTkwoq_9HHtx95vYxDj3ntr1ZjlnRi1GMVNy1ZSCsLD92ru50Yd9ablvEsUcEl06Wiq4QkhbHsYU_DQ90aGTsbZdwtlX3PoMzLOdT6tqhmY9m1CK3pCzXl7l71Lx7DLuGWhSnznCn58Z0eGqM0eZjGu0A84ioOtCW1X7pZb5rCTx8abe4X2gUIJElcHb10rLh6A1L4lRh8GCIRxC4nux88xepHfDU4YZtmTWqv96frE8Y3zFSPDQ2zJXoMxYbUSFVUiv-d_20DangT6jCVCS85Ashm9KlIjW_bG3OigM-KO0sieQkyxo3QjbOHr5NJhJHDQ6m_hfYu37_AFEs0XE)](https://mermaid.live/edit#pako:eNqNlD9PwzAQxb_KySNqFySWqCoDMLAw0AEhgiorvhIriV1dnAJCfHcuzj8nzsDmvHv383Muzo_IrEKRiNpJh_dafpCstpfr1AB4CVJxcJIc4AWNg1waVSKlAmTdGsgdB4k73q7eYbvdLwsx7Ey2QpdjU4ekQO06JkiADV0TWZ-O7aI-NlTCbpflVme436-DQnMCj35_V0PbqvCkDSq4jUN3ppU34AutfxZiSuy1BF4xTkwoq_9HHtx95vYxDj3ntr1ZjlnRi1GMVNy1ZSCsLD92ru50Yd9ablvEsUcEl06Wiq4QkhbHsYU_DQ90aGTsbZdwtlX3PoMzLOdT6tqhmY9m1CK3pCzXl7l71Lx7DLuGWhSnznCn58Z0eGqM0eZjGu0A84ioOtCW1X7pZb5rCTx8abe4X2gUIJElcHb10rLh6A1L4lRh8GCIRxC4nux88xepHfDU4YZtmTWqv96frE8Y3zFSPDQ2zJXoMxYbUSFVUiv-d_20DangT6jCVCS85Ashm9KlIjW_bG3OigM-KO0sieQkyxo3QjbOHr5NJhJHDQ6m_hfYu37_AFEs0XE)\n\n## Install\n\nIf you need to listen or archive an Icecast stream, you will need `ffmpeg`:\n\n```sh\nsudo apt install ffmpeg\n```\n\nInstall earhorn from pip (install the s3 extra to upload the segment to an s3 bucket):\n\n```sh\npip install earhorn\npip install earhorn[s3]\n```\n\nYou can start archiving an Icecast stream by providing a stream url and an archive path:\n\n```sh\nearhorn \\\n  --stream-url https://stream.example.org/live.ogg \\\n  --archive-path=/to/my/archive\n```\n\nYou can also start exporting the Icecast stats as prometheus metrics by providing an Icecast stats url:\n\n```sh\nearhorn \\\n  --stats-url https://stream.example.org/admin/stats.xml \\\n  --stats-user admin \\\n  --stats-password hackme\n```\n\n### Docker\n\n```sh\ndocker pull ghcr.io/jooola/earhorn\n```\n\n## Usage\n\n```\nUsage: earhorn [OPTIONS]\n\n  ENVIRONMENT VARIABLES:\n\n  If a `.env` file is present in the current directory, it will be loaded and can be used to pass environment\n  variables to this tool.\n\n  ARCHIVE STORAGE:\n\n  The storage can be defined using a path to a local directory or an url to an s3 bucket. Segments will be saved on\n  the storage you specified.\n\n  To use an s3 bucket, you need to install the `s3` extras (`pip install earhorn[s3]`), use `s3://bucket-name` as\n  value for the `--archive-path` option and export the s3 bucket credentials listed in the table below:\n\n  | Variable                | Description                               | Example                     |\n  | ----------------------- | ----------------------------------------- | --------------------------- |\n  | AWS_ACCESS_KEY_ID       | The access key for your bucket user       | AKIA568knmklmk              |\n  | AWS_SECRET_ACCESS_KEY   | The secret key for your bucket user       | mi0y84wu498zxsasa           |\n  | AWS_S3_ENDPOINT_URL     | The endpoint to your s3 bucket (optional) | https://s3.nl-ams.scw.cloud |\n  | AWS_S3_REGION_NAME      | Region of your s3 bucket                  | us-east-2                   |\n\n  Example: export AWS_S3_ENPOINT_URL="https://s3.nl-ams.scw.cloud"\n\n  ARCHIVE SEGMENTS:\n\n  To change the segments duration or format, see the ffmpeg documentation for details\n  about the available options:\n  https://ffmpeg.org/ffmpeg-formats.html#segment_002c-stream_005fsegment_002c-ssegment\n\nOptions:\n  --listen-port INTEGER           Listen port for the prometheus metrics endpoint.  [default: 9950]\n  --hook PATH                     Path to a custom script executed to handle stream state `events`.\n  --stats-url TEXT                URL to the icecast admin xml stats page.\n  --stats-user TEXT               Username for the icecast admin xml stats page.  [default: admin]\n  --stats-password TEXT           Password for the icecast admin xml stats page.\n  --stream-url TEXT               URL to the icecast stream.\n  --silence-detect-noise TEXT     Silence detect noise.  [default: -60dB]\n  --silence-detect-duration TEXT  Silence detect duration.  [default: 2]\n  --archive-path PATH             Path or url to the archive storage, supported storage are local filesystem and s3.\n                                  If defined, the stream will be archived in the storage as segments.\n  --archive-segment-filepath TEXT\n                                  Archive segment filepath.  [default:\n                                  {year}/{month}/{day}/{hour}{minute}{second}.{format}]\n  --archive-segment-size INTEGER  Archive segment size in seconds.  [default: 3600]\n  --archive-segment-format TEXT   Archive segment format.  [default: ogg]\n  --archive-segment-format-options TEXT\n                                  Archive segment format options.\n  --archive-copy-stream           Copy the `stream` without transcoding (reduce CPU usage). WARNING: The stream has to\n                                  be in the same format as the `--archive-segment-format`.\n  --help                          Show this message and exit.\n\n```\n\n## Developmement\n\nTo develop this project, start by reading the `Makefile` to have a basic understanding of the possible tasks.\n\nInstall the project and the dependencies in a virtual environment:\n\n```sh\nmake install\nsource .venv/bin/activate\nearhorn --help\n```\n\n## Releases\n\nTo release a new version, first bump the version number in `pyproject.toml` by hand or by using:\n\n```sh\n# poetry version --help\npoetry version <patch|minor|major>\n```\n\nRun the release target:\n\n```sh\nmake release\n```\n\nFinally, push the release commit and tag to publish them to Pypi:\n\n```sh\ngit push --follow-tags\n```\n',
    'author': 'Joola',
    'author_email': 'jooola@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
