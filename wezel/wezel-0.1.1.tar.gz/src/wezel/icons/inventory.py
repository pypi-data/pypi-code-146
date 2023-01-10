__all__ = [
    'favicon',
    'slider_icon', 
    'application_import',
    'arrow_curve_180_left',
    'arrow_curve',
    'arrow_in',
    'arrow_move',
    'arrow_out',
    'arrow_resize_090',
    'bin_metal',
    'blue_document_export',
    'brightness',
    'color',
    'color__arrow',
    'contrast',
    'contrast_low',
    'controller_d_pad',
    'cross_script',
    'cursor',
    'cutter',
    'disk',
    'eraser',
    'eraser__arrow',
    'eraser__plus',
    'hand',
    'hand_finger',
    'hand_point_090',
    'layer_select', 
    'layer_shape',
    'layer_shape_ellipse',
    'layer_shape_curve',
    'layer_shape_polygon',
    'layer_shape_round',
    'layer_transparent', 
    'lifebuoy',
    'lock', 
    'lock_unlock',
    'magnifier',
    'magnifier_zoom_actual',
    'magnifier_zoom_fit',
    'magnifier_zoom_in',
    'magnifier_zoom_out',
    'minus',
    'paint',
    'paint_brush',
    'paint_brush__arrow',
    'paint_brush__minus',
    'paint_brush__plus',
    'paint_can__minus',
    'paint_can__plus',
    'pencil',
    'plus',
    'question_mark',
    'spectrum',
    'wand',
    'wand_hat',
    'wezel', 
]

# filepaths need to be identified with importlib_resources
# rather than __file__ as the latter does not work at runtime 
# when the package is installed via pip install

import sys

if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources


f = importlib_resources.files('wezel.icons.images')

wezel = str(f.joinpath('wezel.jpg'))

f = importlib_resources.files('wezel.icons.my_icons')

favicon = str(f.joinpath('favicon.ico'))
slider_icon = str(f.joinpath('slider_icon.png'))
question_mark = str(f.joinpath('question-mark.png'))

f = importlib_resources.files('wezel.icons.fugue_icons')

application_import = str(f.joinpath('application-import.png'))
arrow_curve = str(f.joinpath('arrow-curve.png'))
arrow_curve_180_left = str(f.joinpath('arrow-curve-180-left.png'))
arrow_in = str(f.joinpath('arrow-in.png'))
arrow_move = str(f.joinpath('arrow-move.png'))
arrow_out = str(f.joinpath('arrow-out.png'))
arrow_resize_090 = str(f.joinpath('arrow-resize-090.png'))
bin_metal = str(f.joinpath('bin-metal.png'))
blue_document_export = str(f.joinpath('blue-document-export.png'))
brightness = str(f.joinpath('brightness.png'))
color = str(f.joinpath('color.png'))
color__arrow = str(f.joinpath('color--arrow.png'))
contrast = str(f.joinpath('contrast.png'))
contrast_low = str(f.joinpath('contrast-low.png'))
controller_d_pad = str(f.joinpath('controller-d-pad.png'))
cross_script = str(f.joinpath('cross-script.png'))
cursor = str(f.joinpath('cursor.png'))
cutter = str(f.joinpath('cutter.png'))
disk = str(f.joinpath('disk.png'))
eraser = str(f.joinpath('eraser.png'))
eraser__plus = str(f.joinpath('eraser--plus.png'))
eraser__arrow = str(f.joinpath('eraser--arrow.png'))
hand = str(f.joinpath('hand.png'))
hand_finger = str(f.joinpath('hand-finger.png'))
hand_point_090 = str(f.joinpath('hand-point-090.png'))
layer_select = str(f.joinpath('layer-select.png'))
layer_shape = str(f.joinpath('layer-shape.png'))
layer_shape_ellipse = str(f.joinpath('layer-shape-ellipse.png'))
layer_shape_curve = str(f.joinpath('layer-shape-curve.png'))
layer_shape_polygon = str(f.joinpath('layer-shape-polygon.png'))
layer_shape_round = str(f.joinpath('layer-shape-round.png'))
layer_transparent = str(f.joinpath('layer-transparent.png'))
lifebuoy = str(f.joinpath('lifebuoy.png'))
lock = str(f.joinpath('lock.png'))
lock_unlock = str(f.joinpath('lock-unlock.png'))
magnifier = str(f.joinpath('magnifier.png'))
magnifier_zoom_actual = str(f.joinpath('magnifier-zoom-actual.png'))
magnifier_zoom_in = str(f.joinpath('magnifier-zoom-in.png'))
magnifier_zoom_out = str(f.joinpath('magnifier-zoom-out.png'))
magnifier_zoom_fit = str(f.joinpath('magnifier-zoom-fit.png'))
minus = str(f.joinpath('minus.png'))
paint = str(f.joinpath('paint.png'))
paint_can__minus = str(f.joinpath('paint-can--minus.png'))
paint_can__plus = str(f.joinpath('paint-can--plus.png'))
paint_brush = str(f.joinpath('paint-brush.png'))
paint_brush__arrow = str(f.joinpath('paint-brush--arrow.png'))
paint_brush__minus = str(f.joinpath('paint-brush--minus.png'))
paint_brush__plus = str(f.joinpath('paint-brush--plus.png'))
pencil = str(f.joinpath('pencil.png'))
plus = str(f.joinpath('plus.png'))
spectrum = str(f.joinpath('spectrum.png'))
wand = str(f.joinpath('wand.png'))
wand_hat = str(f.joinpath('wand-hat.png'))
