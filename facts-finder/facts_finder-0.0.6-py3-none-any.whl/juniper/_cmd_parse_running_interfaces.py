"""juniper interface from config command output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC, JSet

from facts_finder.juniper._cmd_parse_running import Running
from facts_finder.common import verifid_output
from facts_finder.common import blank_line
from facts_finder.juniper.statics import JUNIPER_IFS_IDENTIFIERS
from facts_finder.juniper.common import get_subnet
from facts_finder.juniper.common import get_v6_subnet
from facts_finder.juniper.common import get_vlans_juniper
from facts_finder.juniper.jpw_cracker import juniper_decrypt

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

class RunningInterfaces(Running):
	"""object for interface level config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the  config output

		Args:
			cmd_op (list, str): config output, either list of multiline string
		"""    		    		
		super().__init__(cmd_op)
		self.interface_dict = OrderedDict()

	def interface_read(self, func):
		"""directive function to get the various interface level output

		Args:
			func (method): method to be executed on interface config line

		Returns:
			dict: parsed output dictionary
		"""    		
		ports_dict = OrderedDict()
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("#"): continue
			if l.startswith("set interfaces interface-range"): continue
			if not l.startswith("set interfaces"): continue
			spl = l.split()
			int_type = None
			for k, v in JUNIPER_IFS_IDENTIFIERS.items():
				if spl[2].startswith(v):
					int_type = k
					break
			if not int_type: 
				print(f"UndefinedInterface(Type)-{spl[2]}")
				continue
			p = _juniper_port(int_type, spl)
			if not p: continue
			if not ports_dict.get(p): ports_dict[p] = {}
			port_dict = ports_dict[p]
			func(port_dict, l, spl)
		return ports_dict


	def routing_instance_read(self):
		"""directive function to get the various routing instance level output

		Args:
			func (method): method to be executed on instancel level config lines

		Returns:
			dict: parsed output dictionary
		"""    		
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("#"): continue
			if not l.startswith("set routing-instances "): continue
			spl = l.split()
			try:
				# print(l)
				if spl[3] == 'interface':
					# print(l)
					vrf = spl[2]
					intf = spl[-1]
					# print(vrf, intf)
					self.interface_dict[intf]['intvrf'] = vrf 
			except:
				continue

	def ospf_auth_para_read(self, func):
		"""directive function to get the various protocol ospf level output

		Args:
			func (method): method to be executed on ospf config lines

		Returns:
			dict: parsed output dictionary
		"""    		
		ports_dict = OrderedDict()
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("#"): continue
			spl = l.split()
			ospf_idx = _is_ospf_auth_line(l, spl)
			if not ospf_idx: continue
			if len(spl)>ospf_idx+6 and spl[ospf_idx+3] == 'interface':
				p = spl[ospf_idx+4]
				if not p: continue
				if not ports_dict.get(p): ports_dict[p] = {}
				port_dict = ports_dict[p]
				func(port_dict, l, spl, ospf_idx)
		return ports_dict



	## --------------------------------------------------------------------------------

	def interface_ips(self):
		"""update the interface ipv4 ip address details
		"""    		
		func = self.get_ip_details
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_ip_details(port_dict, l, spl):
		"""parser function to update interface ipv4 ip address details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		subnet = _get_v4_subnet(spl, l)
		if not subnet: return		
		port_dict['v4'] = {}
		port_dict['v4']['address'] = _get_v4_address(spl, l)
		port_dict['v4']['ip'] = _get_v4_ip(spl, l)
		port_dict['v4']['mask'] = _get_v4_mask(spl, l)
		port_dict['v4']['subnet'] = subnet

	def interface_v6_ips(self):
		"""update the interface ipv6 ip address details
		"""    		
		func = self.get_ipv6_details
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_ipv6_details(port_dict, l, spl):
		"""parser function to update interface ipv6 ip address details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		address = _get_v6_address(spl, l)
		if not address: return
		link_local = _is_link_local(address)
		if not port_dict.get('v6'): port_dict['v6'] = {}
		v6_port_dic = port_dict['v6']
		if link_local :
			if v6_port_dic.get("link-local"): return None
			v6_port_dic['link-local'] = {}
			v6_pd = v6_port_dic['link-local']
		else:
			if v6_port_dic.get("address"): return None
			v6_pd = v6_port_dic
		v6_pd['address'] = address
		v6_pd['ip'] = _get_v6_ip(address)
		v6_pd['mask'] = _get_v6_mask(address)
		v6_pd['subnet'] = get_v6_subnet(address)


	def interface_vlans(self):
		"""update the interface vlan details
		"""   
		func = self.get_int_vlan_details
		merge_dict(self.interface_dict, self.interface_read(func))

	def get_int_vlan_details(self, port_dict, l, spl):
		"""parser function to update interface vlan details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""
		vlans = get_vlans_juniper(spl, "i")
		if not vlans: return None
		if not port_dict.get('vlan'): port_dict['vlan'] = []
		port_dict['vlan'].extend(vlans)
		for vlan in vlans:
			if vlan in self.voice_vlans:
				port_dict['voice_vlan'] = vlans

	def interface_mode(self):
		"""update the interface port mode trunk/access details
		"""   
		func = self.get_interface_mode
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_interface_mode(port_dict, l, spl):
		"""parser function to update interface port mode trunk/access details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		mode = 'interface-mode' in spl
		if not mode: return None
		if not port_dict.get('port_mode'): port_dict['port_mode'] = spl[-1]


	def interface_description(self):
		"""update the interface description details
		"""   
		func = self.get_int_description
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_int_description(port_dict, l, spl):
		"""parser function to update interface description details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		description = ""
		if l.startswith("set interfaces ") and "description" in spl:
			desc_idx = spl.index("description")
			description = " ".join(spl[desc_idx+1:])
		if description and not port_dict.get('description'):
			port_dict['description'] = description
		return port_dict

	def int_filter(self):
		"""update the interface type details
		"""   
		func = self.get_int_filter
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_int_filter(port_dict, l, spl):
		"""parser function to update interface type details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		int_type = ""
		for k, v in JUNIPER_IFS_IDENTIFIERS.items():
			if spl[2].startswith(v):
				int_type = k
				break
		port_dict['filter'] = int_type.lower()
		return port_dict

	def interface_channel_grp(self):
		"""update the interface port channel details
		"""   
		func = self.get_interface_channel_grp
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_interface_channel_grp(port_dict, l, spl):
		"""parser function to update interface port channel details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""	
		grp = ''
		if spl[-2] == "802.3ad":
			grp = spl[-1][2:]
			port_dict['channel_grp'] = grp
		return port_dict


	# # Add more interface related methods as needed.


	## --------------------------------------------------------------------------------

	def int_dot_zero_merge_to_parent(self):
		""" merges the value of two keys for `parent` and `parent unit 0` configs
		"""
		# print('came for zero merge')
		for k, v in self.interface_dict.copy().items():
			# print('k,v', k , v)
			if k.endswith(".0"):
				# print(k, ">>>>")
				if self.interface_dict.get(k[:-2]):
					self.interface_dict[k[:-2]].update(v)
				else:
					self.interface_dict[k[:-2]] = v
				del(self.interface_dict[k])

	def int_to_int_number(self):
		''' creates an arbirary unique number for each interface on interface types 
		'''
		for k, v in self.interface_dict.items():
			# print(k, v.keys())
			if v['filter'] == 'physical':
				v['int_number'] = get_physical_port_number(k)
				continue
			if v['filter'] == 'aggregated':
				try:
					v['int_number'] = int(k[2:])
				except: pass
			try:
				int_num = int(k)
				v['int_number'] = int_num
				continue
			except:
				pass
			kspl = k.split(".")
			if k.startswith("lo") or not k.endswith(".0"):
				try:
					v['int_number'] = kspl[1]				
					if not k.startswith("lo") and not k.endswith(".0"):
						v['filter'] = 'vlan'
				except: pass

	# # Add more interface related methods as needed.

	# ----------------------------------------------------------------------------------
	# ospf auth methods
	# ----------------------------------------------------------------------------------

	def ospf_authentication_details(self):
		"""update the interface ospf authentication details
		"""
		# print(self.interface_dict['ge-0/0/7.0'])
		func = self.get_ospf_authentication_details
		merge_dict(self.interface_dict, self.ospf_auth_para_read(func))
		# print(self.interface_dict['ge-0/0/7.0'])

	@staticmethod
	def get_ospf_authentication_details(port_dict, l, spl, ospf_idx):
		"""parser function to update interface ospf authentication details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		""" 
		if spl[ospf_idx+5] == 'interface-type':
			port_dict['ospf_auth_type'] = spl[-1]
		if spl[ospf_idx+5] == 'authentication':
			pw = " ".join(spl[ospf_idx+6:]).strip().split("##")[0].strip()
			if pw[0] == '"': pw = pw[1:]
			if pw[-1] == '"': pw = pw[:-1]
			try:
				pw = juniper_decrypt(pw)
			except: pass
			port_dict['ospf_auth'] = pw
		return port_dict


	# # Add more interface related methods as needed.


# ------------------------------------------------------------------------------

def get_physical_port_number(port):
	""" physical interface - interface number calculator.
	"""
	port = port.split(".")[0]
	port_lst = port.split("-")[-1].split("/")
	port_id = 0
	for i, n in enumerate(reversed(port_lst)):
		multiplier = 100**i
		nm = int(n)*multiplier
		port_id += nm
	return port_id

def get_interfaces_running(cmd_op, *args):
	"""defines set of methods executions. to get various inteface parameters.
	uses RunningInterfaces in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = RunningInterfaces(cmd_op)
	R.voice_vlans = set_of_voice_vlans(R.set_cmd_op)
	R.interface_ips()
	R.interface_v6_ips()
	R.interface_mode()
	R.interface_vlans()
	R.interface_description()
	R.int_filter()
	R.interface_channel_grp()


	# # update more interface related methods as needed.
	R.int_filter()
	R.int_to_int_number()
	R.routing_instance_read()
	R.ospf_authentication_details()
	R.int_dot_zero_merge_to_parent()

	return R.interface_dict



# ------------------------------------------------------------------------------

def _juniper_port(int_type, spl):
	"""get port/interface number based on interface type for split line
	"""    	
	if spl[3] == 'unit':
		# if spl[2] in ('irb', 'vlan'):
		# 	return spl[4]
		return spl[2]+"."+spl[4]
	else:
		return spl[2]

def _get_v4_subnet(spl, line):
	if not _is_v4_addressline(line): return None
	return get_subnet(spl[spl.index("address") + 1])

def _get_v4_ip(spl, line):
	if not _is_v4_addressline(line): return None
	return spl[spl.index("address") + 1].split("/")[0]

def _get_v4_address(spl, line):
	if not _is_v4_addressline(line): return None
	return spl[spl.index("address") + 1]

def _get_v4_mask(spl, line):
	if not _is_v4_addressline(line): return None
	return spl[spl.index("address") + 1].split("/")[1]

def _is_v4_addressline(line):	
	if line.find("family inet") == -1: return None
	if line.find("address") == -1: return None
	return True
# ------------------------------------------------------------------------------


def _get_v6_address(spl, line):
	v6ip = _is_v6_addressline(spl, line)
	if not v6ip : return None
	return v6ip

def _get_v6_ip(v6ip):
	return v6ip.split("/")[0]

def _get_v6_mask(v6ip):
	return v6ip.split("/")[1]

def _is_v6_addressline(spl, line):
	if line.find("family inet6") == -1: return None
	try:
		if spl[spl.index('inet6')+1] != 'address': return None
	except: return None
	return spl[spl.index('inet6')+2]

def _is_link_local(v6_ip):
	return v6_ip.lower().startswith("fe80:")

# ------------------------------------------------------------------------------
# // ospf auth
# ------------------------------------------------------------------------------
def _is_ospf_auth_line(line=None, spl=None):
	""" check and return boolean if provided line/splitted line is an ospf authentication line or not.
	"""
	if not spl:
		spl = line.split()
	if 'ospf' in spl and 'protocols' in spl:
		if spl.index('protocols') + 1 == spl.index('ospf'):
			return spl.index('ospf')
	return None

# ------------------------------------------------------------------------------
# // voice vlans
# ------------------------------------------------------------------------------

def set_of_voice_vlans(set_cmd_op):
	"""get the set of voice vlans configured in provided set commands configuration.
	"""
	voice_vlans = {}
	for l in set_cmd_op:
		if blank_line(l): continue
		if l.strip().startswith("#"): continue
		if not l.strip().startswith("set switch-options voip "): continue
		spl = l.split()
		if spl[-2] == 'vlan':
			voice_vlans.add(spl[-1])
	return voice_vlans

# ------------------------------------------------------------------------------
