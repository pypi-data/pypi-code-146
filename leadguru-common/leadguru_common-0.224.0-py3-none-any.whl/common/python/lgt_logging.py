import sys
from loguru import logger as log

log.remove()
log.add(sys.stdout, format="{time} {name} {level} {message}", level="INFO",
        filter=lambda record: record['level'] == 'INFO')
log.add(sys.stderr, format="{time} {name} {level} {message}", level="WARNING",
        filter=lambda record: record['level'] == 'WARNING')
log.add(sys.stderr, format="{time} {name} {level} {message}", level="ERROR",
        filter=lambda record: record['level'] in ['ERROR', 'FATAL', 'CRITICAL'])


log.info('Logger has been configured') 

log = log
