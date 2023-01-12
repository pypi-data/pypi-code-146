from AnyQt.QtGui import QIcon
from confapp import conf
from pybpod_soundcard_module.module_gui import SoundCardModuleGUI


class ProjectsSoundCard(object):

    def register_on_main_menu(self, mainmenu):
        super(ProjectsSoundCard, self).register_on_main_menu(mainmenu)

        if len([m for m in mainmenu if 'Tools' in m.keys()]) == 0:
            mainmenu.append({'Tools': []})

        menu_index = 0
        for i, m in enumerate(mainmenu):
            if 'Tools' in m.keys():
                menu_index = i
                break

        mainmenu[menu_index]['Tools'].append('-')
        mainmenu[menu_index]['Tools'].append(
            {'Sound Card': self.open_soundcard_plugin, 'icon': QIcon(conf.SOUNDCARD_PLUGIN_ICON)})

    def open_soundcard_plugin(self):
        if not hasattr(self, 'soundcard_plugin'):
            self.soundcard_plugin = SoundCardModuleGUI(self)
            self.soundcard_plugin.show()
            self.soundcard_plugin.resize(*conf.SOUNDCARD_PLUGIN_WINDOW_SIZE)
        else:
            self.soundcard_plugin.show()

        return self.soundcard_plugin
