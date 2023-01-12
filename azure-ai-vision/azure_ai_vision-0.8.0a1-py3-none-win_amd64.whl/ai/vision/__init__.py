# Copyright (c) Microsoft. All rights reserved.
# See https://aka.ms/azai/vision/license for the full license information.

"""
Azure AI Vision SDK for Python
"""

from .vision_base_client import *
from .image_analysis_client import *

try:
    from .version import __version__
except ImportError:
    __version__ = '0.0.0'


from .properties import (
    PropertyCollection
)


from .enums import (
    ImageAnalysisErrorReason,
    ImageAnalysisResultReason,
    SessionStoppedReason,
    SessionStoppedErrorReason,
    SessionResultReason
)


# override __module__ for correct docs generation
root_namespace_classes = (
    Frame,
    FrameWriter,
    FrameSourceCallback,
    FrameFormat,
    FrameSource,
    VisionSource,
    VisionServiceOptions,
    ImageAnalysisOptions,
    ImageAnalysisResult,
    ImageAnalysisEventArgs,
    ImageAnalysisErrorDetails,
    ImageAnalyzer
)


for cls in root_namespace_classes:
    cls.__module__ = __name__
__all__ = [cls.__name__ for cls in root_namespace_classes]
