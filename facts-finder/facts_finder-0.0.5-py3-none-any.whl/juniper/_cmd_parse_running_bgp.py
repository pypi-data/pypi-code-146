"""juniper routing instances parsing from set config  """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC, JSet

from facts_finder.juniper._cmd_parse_running import Running
from facts_finder.common import verifid_output
from facts_finder.common import blank_line
from facts_finder.juniper.statics import JUNIPER_IFS_IDENTIFIERS
from facts_finder.juniper.jpw_cracker import juniper_decrypt

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

class RunningIntanceBGP(Running):
	"""object for instance level config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the  config output

		Args:
			cmd_op (list, str): config output, either list of multiline string
		"""    		    		
		super().__init__(cmd_op)
		self.instance_dict = OrderedDict()

	# ----------------------------------------------------------------------------- #
	def instance_read(self, func):
		"""directive function to get the various instance level output

		Args:
			func (method): method to be executed on interface config line

		Returns:
			dict: parsed output dictionary
		"""    		
		ports_dict = OrderedDict()
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("#"): continue
			if not l.startswith("set routing-instances "): continue
			spl = l.split()
			if spl[3] != 'protocols' or spl[4] != 'bgp' or spl[5] != 'group': continue
			p = spl[6]
			if not p: continue
			if not ports_dict.get(p): ports_dict[p] = {}
			port_dict = ports_dict[p]
			func(port_dict, l, spl)
		return ports_dict

	# ----------------------------------------------------------------------------- #
	def instance_bgp_nbr_read(self, func):
		"""directive function to get the various instance level output for bgp neighbours only

		Args:
			func (method): method to be executed on interface config line

		Returns:
			dict: parsed output dictionary
		"""    		
		ports_dict = OrderedDict()
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("#"): continue
			if not l.startswith("set routing-instances "): continue
			spl = l.split()
			if spl[3] != 'protocols' or spl[4] != 'bgp' or spl[5] != 'group' or spl[7] != 'neighbor': continue
			p = spl[8]
			if not p: continue
			if not ports_dict.get(p): ports_dict[p] = {}
			port_dict = ports_dict[p]
			func(port_dict, l, spl)
		return ports_dict

	# ----------------------------------------------------------------------------- #

	def bgp_grp_info(self):
		"""update the bgp group detail - description, peer group, peer ip, auth-key, vrf, peer as
		"""    		
		func = self.get_bgp_grp_info
		merge_dict(self.instance_dict, self.instance_read(func))

	@staticmethod
	def get_bgp_grp_info(port_dict, l, spl):
		"""parser function to update bgp group detail - description, peer group, peer ip, auth-key, vrf, peer as

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		""" 
		port_dict['bgp_peergrp'] = spl[6]
		## --- description and vrf ---
		if len(spl)>7 and spl[7] == 'description':
			desc = " ".join(spl[8:]).strip()
			if desc[0] == '"': desc = desc[1:]
			if desc[-1] == '"': desc = desc[:-1]
			port_dict['bgp_peer_description'] = desc
			port_dict['bgp_vrf'] = spl[2]
		## --- auth key ---
		if len(spl)>7 and spl[7] == 'authentication-key':
			pw = " ".join(spl[8:]).strip().split("##")[0].strip()
			if pw[0] == '"': pw = pw[1:]
			if pw[-1] == '"': pw = pw[:-1]
			try:
				pw = juniper_decrypt(pw)
			except: pass
			port_dict['bgp_peer_password'] = pw
		## --- peer-as ---
		if len(spl)>7 and spl[7] == 'peer-as':
			port_dict['bgp_peer_as'] = spl[8]
		## --- local-as ---
		if len(spl)>7 and spl[7] == 'local-as':
			port_dict['bgp_peer_as'] = spl[8]
		## --- ebgp multihops ---
		if len(spl)>8 and spl[7] == 'multihop':
			port_dict['bgp_peer_multihops'] = spl[-1]

	# ----------------------------------------------------------------------------- #

	def bgp_nbr_info(self):
		"""update the bgp neighbor detail - description, peer group, peer ip, auth-key, vrf, peer as
		"""    		
		func = self.get_bgp_nbr_info
		merge_dict(self.instance_dict, self.instance_bgp_nbr_read(func))

	@staticmethod
	def get_bgp_nbr_info(port_dict, l, spl):
		"""parser function to update bgp neighbor detail - description, peer group, peer ip, auth-key, vrf, peer as

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""
		port_dict['bgp_peergrp'] = spl[6]
		## --- description and vrf ---
		if len(spl)>9 and spl[9] == 'description':
			desc = " ".join(spl[10:]).strip()
			if desc[0] == '"': desc = desc[1:]
			if desc[-1] == '"': desc = desc[:-1]
			port_dict['bgp_peer_description'] = desc
		port_dict['bgp_vrf'] = spl[2]
		port_dict['bgp_peer_ip'] = spl[8]
		## --- auth key ---
		if len(spl)>9 and spl[9] == 'authentication-key':
			pw = " ".join(spl[10:]).strip().split("##")[0].strip()
			if pw[0] == '"': pw = pw[1:]
			if pw[-1] == '"': pw = pw[:-1]
			try:
				pw = juniper_decrypt(pw)
			except: pass
			port_dict['bgp_peer_password'] = pw
		## --- peer-as ---
		if len(spl)>9 and spl[9] == 'peer-as':
			port_dict['bgp_peer_as'] = spl[10]
		## --- local-as ---
		if len(spl)>9 and spl[9] == 'local-as':
			port_dict['bgp_peer_as'] = spl[10]





	# # Add more interface related methods as needed.


# ------------------------------------------------------------------------------


def get_instances_bgps(cmd_op, *args):
	"""defines set of methods executions. to get various instance parameters.
	uses RunningInterfaces in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = RunningIntanceBGP(cmd_op)
	R.bgp_grp_info()
	R.bgp_nbr_info()

	# # update more instance related methods as needed.



	return R.instance_dict



# ------------------------------------------------------------------------------

