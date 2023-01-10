"""
`canvas` is the main widget for drawing and displaying images

"""
from wezel.canvas.utils import (
    COLORMAPS,
    #makeQImage,
    colormap_to_LUT,
    region_grow_add, 
    region_grow_remove,
)

from wezel.canvas.canvas import (
    Canvas,
    ImageItem,
    MaskItem,
    FilterItem,
    FilterSet,
)
from wezel.canvas.toolbar import (
    ToolBar,
)
from wezel.canvas.scene_filter import(
    PanFilter,
    ZoomFilter,
)
from wezel.canvas.image_filter import (
    ImageWindow,
)
from wezel.canvas.mask_filter import(
    MaskBrush,
    MaskPenSet, 
    MaskPenFreehand,
    MaskPenPolygon,
    MaskPenRectangle,
    MaskPenCircle, 
    MaskThreshold,
    MaskPaintByNumbers,
    MaskRegionGrowing,
    MaskDilate,
    MaskShrink,
    MaskKidneyEdgeDetection,
)
from wezel.canvas.series_canvas import (
    SeriesCanvas,
)
