import plotly.graph_objects as go

import truera.client.intelligence.visualizations.colors as Colors


class Plots():
    '''
    A General plots class that can be used for any downstream visualizers.
    '''

    @staticmethod
    def truera_layout(**kwargs) -> go.Layout:
        '''
        Returns a go.Layout with truera theme.

        Kwargs:
            go.layout kwargs that will be supplmented with truera themes.
        Returns:
            go.Layout
        '''
        default_kwargs = dict(
            plot_bgcolor=Colors.WHITE,
            hoverlabel=dict(
                bgcolor=Colors.TRUERA_GREEN,
                font_size=16,
            )
        )
        default_kwargs.update(kwargs)
        return go.Layout(**default_kwargs)
