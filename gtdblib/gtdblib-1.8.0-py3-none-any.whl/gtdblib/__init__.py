__title__ = 'gtdblib'
__description__ = 'An abstraction of objects, files, and third-party tools used by the GTDB. Not intended for public use.'
__url__ = 'https://github.com/Ecogenomics/gtdb-lib'
__version__ = '1.8.0'
__author__ = 'Aaron Mussig'
__author_email__ = 'aaronmussig@gmail.com'
__license__ = 'GPL-3.0'
__bug_url__ = 'https://github.com/Ecogenomics/gtdb-lib'
__doc_url__ = 'https://github.com/Ecogenomics/gtdb-lib'
__src_url__ = 'https://github.com/Ecogenomics/gtdb-lib'

import logging

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%Y-%m-%d %H:%M:%S]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")
