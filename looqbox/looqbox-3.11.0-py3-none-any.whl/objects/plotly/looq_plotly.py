from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ObjPlotly(LooqObject):
    """
    Creates an ObjPlotly from a plotly object.

    Attributes:
    --------
        :param dict data: Plotly general values. Can be a dict or a plotly object like Bar, Scatter and etc..
        :param plotly.graph_objs._layout.Layout layout: Layout elements of the plotly, it's a Layout object from
        plotly.graph_objs, if it's not send as a parameter, the function creates it internally.
        :param bool stacked: Define if the element should be stacked.
        :param bool display_mode_bar: Define if the mode bar in the top right of the graphic will appear or not.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> trace = go.Scatter(x = list(table.data['Data']), y = list(table.data['Venda']))
    >>> layout = go.Layout(title='title', yaxis=dict(title='Vendas'))
    >>> g = lq.ObjPlotly([trace], layout=layout)

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
        """
    def __init__(self, data, layout=None, stacked=True, display_mode_bar=True, tab_label=None, value=None):
        """
        Creates an ObjPlotly from a plotly object.

        Parameters:
        --------
            :param dict data: Plotly general values. Can be a dict or a plotly object like Bar, Scatter and etc..
            :param plotly.graph_objs._layout.Layout layout: Layout elements of the plotly, it's a Layout object from
            plotly.graph_objs, if it's not send as a parameter, the function creates it internally.
            :param bool stacked: Define if the element should be stacked.
            :param bool display_mode_bar: Define if the mode bar in the top right of the graphic will appear or not.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
        >>> trace = go.Scatter(x = list(table.data['Data']), y = list(table.data['Venda']))
        >>> layout = go.Layout(title='title', yaxis=dict(title='Vendas'))
        >>> g = lq.ObjPlotly([trace], layout=layout)
        """
        super().__init__()
        self.data = data
        self.layout = layout
        self.stacked = stacked
        self.display_mode_bar = display_mode_bar
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.plotly_render(self)
