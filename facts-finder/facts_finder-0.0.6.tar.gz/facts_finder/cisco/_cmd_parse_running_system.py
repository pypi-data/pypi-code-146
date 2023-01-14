"""cisco running-config system level command output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC

from facts_finder.common import verifid_output

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

class RunningSystem():
	"""object for running config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the running config output

		Args:
			cmd_op (list, str): running config output, either list of multiline string
		"""    		
		self.cmd_op = verifid_output(cmd_op)
		self.system_dict = {}


	def system_bgp_as_number(self):
		"""get the device bgp as number
		""" 
		for l in self.cmd_op:
			if not l.startswith("router bgp "): continue
			return {'system_bgp_as_number': l.strip().split()[-1]}
		return {}


	def system_ca_certificate(self):
		"""get the device certificate hex values for cisco 9xxx and later series  switches.
		""" 
		ca_start, cert = False, ''
		for l in self.cmd_op:
			if l.strip().startswith("certificate ca 01"):
				ca_start = True
				continue
			if ca_start and l.strip().startswith("quit"):
				break
			if not ca_start: continue
			cert += l+'\n'
		return {'ca_certificate': cert.rstrip()}


# ------------------------------------------------------------------------------


def get_system_running(cmd_op, *args):
	"""defines set of methods executions. to get various system parameters.
	uses RunningSystem in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""
	R  = RunningSystem(cmd_op)
	R.system_dict.update(R.system_bgp_as_number())
	R.system_dict.update(R.system_ca_certificate())

	# # update more interface related methods as needed.
	if not R.system_dict:
		R.system_dict['dummy_col'] = ""

	return R.system_dict
