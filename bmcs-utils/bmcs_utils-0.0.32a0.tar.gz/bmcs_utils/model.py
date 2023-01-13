
import traits.api as tr
from bmcs_utils.app_window import AppWindow
from bmcs_utils.view import View
from bmcs_utils.i_model import IModel
from .controller import Controller
from .model_notify_mixin import ModelNotifyMixin
from .model_tree_node_mixin import ModelTreeNodeMixin

@tr.provides(IModel)
class Model(ModelNotifyMixin, ModelTreeNodeMixin):
    """Base class for interactive bmcs_utils
    """

    name = tr.Str("<unnamed>")

    ipw_view = View()

    def __init__(self,*args,**kw):
        super().__init__(*args, **kw)

    def get_controller(self, app_window):
        return Controller(model=self, app_window=app_window)

    plot_backend = 'mpl'
    """"plot_backend = 'mpl' or 'k3d'"""

    def subplots(self, fig):
        if self.plot_backend == 'mpl':
            return fig.subplots(1, 1)
        elif self.plot_backend == 'k3d':
            return fig
        else:
            raise NameError(self.plot_backend + ' is not a valid plot_backend!')

    def plot(self, axes):
        """Alias to update plot - to be overloaded by subclasses"""
        self.update_plot(axes)

    def update_plot(self, axes):
        pass

    def new_app_window(self, **kw):
        return AppWindow(self, **kw)

    def interact(self,**kw):
        app_window = self.new_app_window()
        return app_window.interact()

    def app(self,**kw):
        return self.interact(**kw)

# backward compatibility
InteractiveModel = Model