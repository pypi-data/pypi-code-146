import mvvmQt.attrTypes as t
import mvvmQt.attrFuncs as f

"""
结构格式为key: [qt function name or callable function, type]
如果为callable function, 最后一个参数必然为Element对象
"""

size = {
    'maxHeight': ['setMaximumHeight', int],
    'maxWidth': ['setMaximumWidth', int],
    'minHeight': ['setMinimumHeight', int],
    'minWidth': ['setMinimumWidth', int],
    'width': ['setFixedWidth', int],
    'height': ['setFixedHeight', int],
    'visible': ['setVisible', bool]
}

common = {
    'text': ['setText', str],
    'enable': ['setEnabled', bool]
}

align = {
    'align': ['setAlignment', t.alignment]
}

btn = {
    'checked': ['setChecked', [int, bool]],
    'checkable': ['setCheckable', bool]
}

ElementAttr = {
    'widget': {
        **size,
        'style': ['setStyleSheet', [str, t.readFile]],
        'title': ['setWindowTitle', str],
        'pos': ['move', t.toList(int)],
        'full': ['showType', [int, bool]]
    },
    'frame': {
        **size,
        'shape': ['setFrameShape', t.frameShape],
        'shadow': ['setFrameShadow', t.frameShadow],
        'linew': ['setLineWidth', int],
        'lineMw': ['setMidLineWidth', int],
    },
    'grid': {
        'spacing': ['setSpacing', int],
        'vspacing': ['setVerticalSpacing', int],
        'hspacing': ['setHorizontalSpacing', int]
    },
    'button-group': {
        'exclusive': ['setExclusive', [int, bool]],
        'checked': [f.groupChecked, None]
    },
    'button': {
        **size, **common, **btn,
        'shortcut': ['setShortcut', str],
        'tooltip': ['setToolTip', str],
        'icon': ['setIcon', str],
        'repeat': ['setAutoRepeat', [int, bool]],
        'repeatDelay': ['setAutoRepeatDelay', int],
        'repeatInterval': ['setAutoRepeatInterval', int]
    },
    'radio': {
        **common, **btn
    },
    'label': {
        **size, **common, **align,
        'cv': ['setTextOrPixmap', t.cvImg],
        'cvPath': ['setPixmap', [str, t.cvPathImg]],
        'scaledContents': ['setScaledContents', [int, bool]]
    },
    'tab': {
        'pos': ['setTabPosition', t.tabPosition],
        'name': ['setTabText', t.toList([int, str])]
    },
    'status': {
        'msg': ['showMessage', str]
    },
    'select': {
        'index': ['setCurrentIndex', int]
    }
}

ElementAttr['window'] = {
    **ElementAttr['widget']
}