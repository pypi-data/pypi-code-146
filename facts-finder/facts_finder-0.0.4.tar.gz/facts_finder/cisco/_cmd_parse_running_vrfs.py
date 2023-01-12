"""cisco VRF level running-config command output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC

from facts_finder.common import verifid_output
from facts_finder.common import blank_line
from facts_finder.cisco.common import get_vrf_cisco


merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

class RunningVRFs():
	"""object for VRF level running config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the running config output

		Args:
			cmd_op (list, str): running config output, either list of multiline string
		"""    		    		
		self.cmd_op = verifid_output(cmd_op)
		self.vrf_dict = OrderedDict()

	def vrf_read(self, func):
		"""directive function to get the various VRF level output

		Args:
			func (method): method to be executed on VRF config line

		Returns:
			dict: parsed output dictionary
		"""    		
		int_toggle = False
		vrfs_dict = OrderedDict()
		for l in self.cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("!"): 
				int_toggle = False
				continue
			if l.startswith("vrf ") or l.startswith("ip vrf "):
				p = get_vrf_cisco(l)
				if not p: continue
				if not vrfs_dict.get(p): vrfs_dict[p] = {}
				port_dict = vrfs_dict[p]
				int_toggle = True
				continue
			if int_toggle:
				func(port_dict, l)
		return vrfs_dict

	@staticmethod
	def get_vrf_description(port_dict, l):
		"""parser function to update vrf description details

		Args:
			port_dict (dict): dictionary with a vrf info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		desc = None
		if l.strip().startswith("description "):
			desc = l.strip().split(" ", 1)[-1]
			port_dict['vrf_description'] = desc
		if not desc: return None

	def vrf_description(self):
		"""update the vrf description details
		"""    		
		func = self.get_vrf_description
		merge_dict(self.vrf_dict, self.vrf_read(func))

	# # Add more interface related methods as needed.


# ------------------------------------------------------------------------------


def get_vrfs_running(cmd_op, *args):
	"""defines set of methods executions. to get various vrf parameters.
	uses RunningInterfaces in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = RunningVRFs(cmd_op)
	R.vrf_description()

	# # update more interface related methods as needed.

	return R.vrf_dict

