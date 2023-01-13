import logging
from .reconciler import Reconciler


logger = logging.getLogger(__name__)


def start_reconciler_blocking(reconciler: Reconciler):
    try:
        reconciler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Reconciler stopping...")
        reconciler.stop()
