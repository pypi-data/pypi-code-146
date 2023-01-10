"""
`widgets` is a collection of PyQt widgets that can be used as components 
in `wezel` applications.

"""

#from .log_to_GUI import *

from .dbimage import (
    ImageWindow,
    ImageBrightness, 
    ImageContrast,
)
from .series_sliders import (
    SeriesSliders,
)
from .series_display import (
    SeriesDisplay,
    SeriesDisplay4D,
)
from .plot_curve import (
    PlotCurve,
)
from .qrangeslider import (
    QRangeSlider,
)
from .sliders import (
    IndexSlider, 
    LabelSlider, 
    CheckBoxSlider,
)
from .main_mdi import (
    MainMultipleDocumentInterface, 
)
from .message import (
    Dialog, 
    StatusBar,
    UserInput,
)
from .dbdatabase import (
    DICOMFolderTree,
)
from .region_list import (
    RegionList,
)
from .file_display import (
    ImageLabel,
)
from .dicom_header import (
    SeriesViewerMetaData,
)