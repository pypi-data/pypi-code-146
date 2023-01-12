from pybpod_alyx_module.module_gui import AlyxModuleGUI
from pybpodgui_plugin.models.project.project_window import ProjectWindow


class ProjectTreeNode(ProjectWindow):

	def create_treenode(self, tree):
		node = super(ProjectTreeNode, self).create_treenode(tree)
		self.open_alyx_action = tree.add_popup_menu_option(
            'Sync to Alyx',
            self.open_alyx_window,
            item= node
            )

		return node
	
	def open_alyx_window(self):
		if not hasattr(self, 'alyx_window'):
			self.alyx_window = AlyxModuleGUI(self)
		self.alyx_window.show()
		return self.alyx_window
