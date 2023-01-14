

from nettoolkit import JSet
from facts_finder.common import verifid_output


class Running():
	"""parent object for config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the  config output

		Args:
			cmd_op (list, str): config output, either list of multiline string
		"""    		    		
		self.cmd_op = cmd_op
		JS = JSet(input_list=cmd_op)
		JS.to_set
		self.set_cmd_op = verifid_output(JS.output)
