from firecore.logging import get_logger
import numpy as np

logger = get_logger(__name__)

try:
    import cv2
except ImportError:
    logger.exception("you should install opencv")


def cv2_loader(filename: str, flag: int = cv2.IMREAD_COLOR) -> np.ndarray:
    """
    Return RGB image as np.ndarray
    """
    img = cv2.imread(filename, flag=flag)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def cv2_worker_init_fn(worker_id: int):
    cv2.setNumThreads(0)
    logger.info("cv2 get num threads: {}", cv2.getNumThreads())
