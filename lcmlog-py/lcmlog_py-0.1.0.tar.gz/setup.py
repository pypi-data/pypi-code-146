# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lcmlog']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lcmlog-py',
    'version': '0.1.0',
    'description': 'LCM log utilities',
    'long_description': "# lcmlog-py\n\nLCM log utilities\n\n## Installation\n\n`lcmlog-py` is available on PyPI:\n\n```bash\npip install lcmlog-py\n```\n\n## Usage\n\n### Events\n\n`lcmlog-py` provides classes to abstract the LCM log file format. The `Event` class represents a single event in the log file. An `Event` is composed of a header, channel string, and data byte array.\n\nThe `Header` class represents a fixed-length header at the beginning of each event which describes the event number, timestamp, and channel/data lengths. This is parsed first, and then the channel and data are read in.\n\nIf the header is read incorrectly or is corrupt, a `BadSyncError` is raised.\n\nTo read a header, call the `Header.from_file` method:\n\n```python\nfrom lcmlog import Header\n\nwith open('lcmlog', 'rb') as f:\n    header = Header.from_file(f)\n\nprint(header.timestamp)  # e.g.\n```\n\nA full event can be read via the `Event.from_file` method:\n\n```python\nfrom lcmlog.event import Event\n\nwith open('lcmlog', 'rb') as f:\n    event = Event.from_file(f)\n\nprint(event.header.timestamp)\nprint(event.channel)  # e.g.\n```\n\n### Log Reader & Writer\n\n`lcmlog-py` also provides two utility classes for reading and writing LCM log files in order.\n\nThe `LogReader` reads events from a file (starting at the beginning) and the `LogWriter` writes events to a file. The `LogReader` class is iterable. Both classes close their respective files when they are garbage collected.\n\n```python\nfrom lcmlog import LogReader, LogWriter\n\nreader = LogReader('lcmlog_source')\nwriter = LogWriter('lcmlog_dest')\n\n# Read and write each event\nfor event in reader:\n    writer.write(event)\n```",
    'author': 'Kevin Barnard',
    'author_email': 'kbarnard@mbari.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
