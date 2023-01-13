import ipywidgets as ipw


class Toolbar(ipw.VBox):

    def __init__(self) -> None:
        self._home = ipw.Button(icon='home',
                                layout={
                                    'width': '36px',
                                    'padding': '0'
                                })
        self._zoom = ipw.ToggleButton(icon='square-o',
                                      layout={
                                          'width': '36px',
                                          'padding': '0'
                                      })
        self._pan = ipw.ToggleButton(icon='arrows',
                                     layout={
                                         'width': '36px',
                                         'padding': '0'
                                     })
        super().__init__([self._home, self._zoom])
