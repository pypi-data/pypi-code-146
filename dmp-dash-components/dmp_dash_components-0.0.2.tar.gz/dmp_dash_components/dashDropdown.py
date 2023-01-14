from dash.dcc.Dropdown import Dropdown

class dashDropdown(Dropdown):
    def __init__(self,
                 value=None,
                 options=[],
                 select_all=True,
                 *args, **kwargs):
        Dropdown.__init__(self, *args, **kwargs)
        self.value = value
        self.options = options
        if select_all is True and self.value is None:
            self.value = [x['value'] for x in self.options]
