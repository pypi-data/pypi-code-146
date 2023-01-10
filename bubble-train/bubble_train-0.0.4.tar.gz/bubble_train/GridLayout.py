# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class GridLayout(Component):
    """A GridLayout component.
GridLayout is a component for building
dashboards with draggable and resizable items.
It takes a list of children and display them in
div elements that can be moved around the page.
The initial size of each element can either be
defined with the layout argument or by wrapping
each element with the DashboardItem component.
By default, GridLayout will saved the
position of the elements on client side, when
moved on the page. But you can also save it
on server side by defining a callback with :
`Input("<my-id>", "layout")`.

Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers | a list of or a singular dash component, string or number; optional):
    Children is a list of the elements to drag and resize on the
    dashboard.  It can be a list of dash Components and/or
    DashboardItem.

- id (string; optional):
    (string) The ID used to identify this component in Dash callbacks.
    The id is also used to automatically save the layout on client
    side.

- autoSize (boolean; default True)

- className (string; default ''):
    (string) class passed to the react-grid-layout component.

- clearSavedLayout (boolean; default False):
    (bool) If set to True, then the layout saved in the client browser
    will be cleared on page load.

- compactType (a value equal to: 'vertical', 'horizontal'; default 'vertical')

- containerPadding (list of numbers; default [10, 10])

- draggableCancel (string; default '')

- draggableHandle (string; default '')

- gridCols (number; optional):
    (number) number of columns in the grid layout.  Default value is
    12.

- height (number; optional):
    (number) height of a row (in px).  Default value is 30.

- isBounded (boolean; default False)

- isDraggable (boolean; default True)

- isDroppable (boolean; default False)

- isResizable (boolean; default True)

- layout (list of dicts; optional):
    Layout is a list of dictionnary with the format:  {x: number, y:
    number, w: number, h: number}  The index into the layout must
    match the id used on each item component with DashboardItem.  If
    you choose to use custom keys, you can specify that key in the
    layout  array objects like so:  {i: string, x: number, y: number,
    w: number, h: number}  The ID used to identify this component in
    Dash callbacks.  The id is also used to automatically save the
    layout on client side.

- margin (list of numbers; default [10, 10])

- ncols (number; optional):
    (number) the default number of columns by item.  Default value is
    6.

- nrows (number; optional):
    (number) the default number of row by item.  Default value is 8.

- preventCollision (boolean; default False)

- resizeHandles (list of a value equal to: 's', 'w', 'e', 'n', 'sw', 'nw', 'se', 'ne's; default ['se'])

- save (boolean; default True):
    (bool) If False, then the layout is not saved in the browser.
    Default value is True.

- style (dict; optional):
    (dict) css style passed to the react-grid-layout component.

- transformScale (number; default 1)

- useCSSTransforms (boolean; default True)

- verticalCompact (boolean; default True)

- width (number; optional):
    (number) width (in px).  Default value is 1200."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'bubble_train'
    _type = 'GridLayout'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, layout=Component.UNDEFINED, save=Component.UNDEFINED, clearSavedLayout=Component.UNDEFINED, ncols=Component.UNDEFINED, nrows=Component.UNDEFINED, width=Component.UNDEFINED, gridCols=Component.UNDEFINED, height=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, autoSize=Component.UNDEFINED, draggableCancel=Component.UNDEFINED, draggableHandle=Component.UNDEFINED, verticalCompact=Component.UNDEFINED, compactType=Component.UNDEFINED, margin=Component.UNDEFINED, containerPadding=Component.UNDEFINED, isDraggable=Component.UNDEFINED, isResizable=Component.UNDEFINED, isBounded=Component.UNDEFINED, useCSSTransforms=Component.UNDEFINED, transformScale=Component.UNDEFINED, preventCollision=Component.UNDEFINED, isDroppable=Component.UNDEFINED, resizeHandles=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'autoSize', 'className', 'clearSavedLayout', 'compactType', 'containerPadding', 'draggableCancel', 'draggableHandle', 'gridCols', 'height', 'isBounded', 'isDraggable', 'isDroppable', 'isResizable', 'layout', 'margin', 'ncols', 'nrows', 'preventCollision', 'resizeHandles', 'save', 'style', 'transformScale', 'useCSSTransforms', 'verticalCompact', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'autoSize', 'className', 'clearSavedLayout', 'compactType', 'containerPadding', 'draggableCancel', 'draggableHandle', 'gridCols', 'height', 'isBounded', 'isDraggable', 'isDroppable', 'isResizable', 'layout', 'margin', 'ncols', 'nrows', 'preventCollision', 'resizeHandles', 'save', 'style', 'transformScale', 'useCSSTransforms', 'verticalCompact', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(GridLayout, self).__init__(children=children, **args)
