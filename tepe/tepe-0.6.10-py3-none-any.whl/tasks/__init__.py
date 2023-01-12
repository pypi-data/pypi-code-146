# ## classification
# from .simplenet.task import SimplenetConfig
# from .mobilenetv2.task import MobileNetV2Config
#
# ## detection
# # from .ssdlite import SSDRFB
# from .ssdlite_rfb.task import SSDLiteRFBConfig
# from .yolov5.task import YOLOv5Config
# from .yolox.task import YOLOXConfig
#
# ## segmentation
# from .deeplabv3.task import DeeplabV3Config
#
# ## keypoint detection
# from .shufflenet_heatmap.task import ShufflenetHeatmap

## anomaly detection
# from .cfa.task import CFAConfig


def get(task_name: str):
    from tepe.core import get_task
    return get_task(task_name)