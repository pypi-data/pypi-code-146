from confapp import conf
from pybpodgui_plugin.models.user.user_dockwindow import UserDockWindow

User = type(
    'User',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.user.User') + [UserDockWindow]),
    {}
)
