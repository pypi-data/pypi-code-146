try:
    from networkx import DiGraph
    networkx_available = True
except ImportError:
    networkx_available = False

    class DiGraph:
        pass


from geodesic.utils import DeferredImport

display = DeferredImport('IPython.display')
entanglement_widget = DeferredImport('geodesic.widgets.geodesic_widgets.entanglement_widget')

class Graph(DiGraph):
    def __init__(self, data=None, nodes=None, edges=None, project=None) -> None:
        super().__init__()
        if not networkx_available:
            raise ImportError("networkx not available. Must be installed to use Graph")

        if nodes is not None:
            self.add_nodes_from(nodes)

            for node in nodes:
                node.graph = self

        if edges is not None:
            for connection in edges:
                p = connection.predicate
                self.add_edge(
                    connection.subject,
                    connection.object,
                    connection=connection,
                    name=p.name,
                    **connection.predicate.edge_attributes
                )

    def _ipython_display_(self, **kwargs):
        return entanglement_widget.EntanglementWidget(self)._ipython_display_(**kwargs)
