from ..core.plugin_aux import *
from ..core.utils import *

'''
check version ?

module.__version__ == '4.0.2'

'''

class MODULE_CAPSTONE(MODULES_BASE):

	name = 'capstone'

	def is_my_type(self):
		return True

	def can_run(self):
		self.module = self.try_import('capstone')
		return True if self.module else False

	def load(self):
		return self.module

