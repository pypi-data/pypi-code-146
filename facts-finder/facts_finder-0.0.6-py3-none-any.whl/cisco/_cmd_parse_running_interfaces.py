"""cisco Interface level running-config command output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC

from facts_finder.common import verifid_output
from facts_finder.common import blank_line
from facts_finder.cisco.common import get_interface_cisco
from facts_finder.cisco.common import get_inet_address
from facts_finder.cisco.common import get_subnet
from facts_finder.cisco.common import get_int_ip
from facts_finder.cisco.common import get_int_mask
from facts_finder.cisco.common import get_vlans_cisco
from facts_finder.cisco.common import get_v6_subnet
from facts_finder.cisco.common import get_inetv6_address
from facts_finder.cpw_cracker import decrypt_type7

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

class RunningInterfaces():
	"""object for interface level running config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the running config output

		Args:
			cmd_op (list, str): running config output, either list of multiline string
		"""    		    		
		self.cmd_op = verifid_output(cmd_op)
		self.interface_dict = OrderedDict()

	def interface_read(self, func):
		"""directive function to get the various interface level output

		Args:
			func (method): method to be executed on interface config line

		Returns:
			dict: parsed output dictionary
		"""    		
		int_toggle = False
		ports_dict = OrderedDict()
		for l in self.cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("!"): 
				int_toggle = False
				continue
			if l.startswith("interface "):
				p = get_interface_cisco(l)
				if not p: continue
				if not ports_dict.get(p): ports_dict[p] = {}
				port_dict = ports_dict[p]
				int_toggle = True
				continue
			if int_toggle:
				func(port_dict, l)
		return ports_dict

	def interface_ips(self):
		"""update the interface ipv4 ip address details
		"""    		
		func = self.get_ip_details
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_ip_details(port_dict, l):
		"""parser function to update interface ipv4 ip address details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		address = get_inet_address(l)
		if not address: return None
		port_dict['v4'] = {}
		port_dict['v4']['address'] = address
		port_dict['v4']['ip'] = get_int_ip(address)
		port_dict['v4']['mask'] = get_int_mask(address)
		port_dict['v4']['subnet'] = get_subnet(address)


	def interface_v6_ips(self):
		"""update the interface ipv6 ip address details
		"""   
		func = self.get_ipv6_details
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_ipv6_details(port_dict, l):
		"""parser function to update interface ipv6 ip address details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		link_local = l.find("link-local") > -1
		if l.find("anycast") > -1: return None
		address = get_inetv6_address(l, link_local)
		if not address: return None
		if not port_dict.get('v6'): port_dict['v6'] = {}
		if link_local:
			port_dict['v6']['link-local'] = {}
			pd = port_dict['v6']['link-local']
			pd['address'] = address
			return None
		pd = port_dict['v6']
		pd['address'] = address
		pd['ip'] = get_int_ip(address)
		pd['mask'] = get_int_mask(address)
		pd['subnet'] = get_v6_subnet(address)


	def interface_vlans(self):
		"""update the interface vlan details
		"""   
		func = self.get_int_vlan_details
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_int_vlan_details(port_dict, l):
		"""parser function to update interface vlan details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		vlans = get_vlans_cisco(l.strip())
		if not vlans: return None
		if not port_dict.get("vlan"): port_dict['vlan'] = {}
		for k, v in vlans.items():
			if v: port_dict['vlan'][k] = v


	def interface_channel_group(self):
		"""update the interface port channel details
		"""   
		func = self.get_int_channel_group
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_int_channel_group(port_dict, l):
		"""parser function to update interface port channel details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		po = None
		if l.strip().startswith("channel-group"):
			spl = l.strip().split() 
			po = spl[1]
			po_mode = spl[-1]

		if not po: return None
		port_dict['channel_group'] = {}
		port_dict['channel_group']['interface'] = "Port-channel" + po
		port_dict['channel_group']['mode'] = po_mode


	def interface_vrf(self):
		"""update the interface vrf details
		"""   
		func = self.get_int_vrf
		merge_dict(self.interface_dict, self.interface_read(func))

	@staticmethod
	def get_int_vrf(port_dict, l):
		"""parser function to update interface vrf details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		vrf = None
		if (l.strip().startswith("vrf forwarding") 
			or l.strip().startswith("ip vrf forwarding")):
			vrf = l.strip().split()[-1]
		if not vrf: return None
		port_dict['vrf'] = vrf


	@staticmethod
	def get_int_udld(port_dict, l):
		udld = None
		if l.strip().startswith("udld port "):
			port_dict['int_udld'] = l.strip().split(" ", 2)[-1]
		if not udld: return None

	def interface_udld(self):
		func = self.get_int_udld
		merge_dict(self.interface_dict, self.interface_read(func))


	@staticmethod
	def get_int_ospf_auth(port_dict, l):
		auth, auth_type = None, None
		if l.strip().startswith("ip ospf authentication-key"):
			port_dict['ospf_auth'] = decrypt_type7(l.strip().split()[-1])
		if l.strip().startswith("ip ospf network "):
			port_dict['ospf_auth_type'] = l.strip().split()[-1]
		if not auth and not auth_type: return None

	def interface_ospf_auth(self):
		func = self.get_int_ospf_auth
		merge_dict(self.interface_dict, self.interface_read(func))

	# # Add more interface related methods as needed.


# ------------------------------------------------------------------------------


def get_interfaces_running(cmd_op, *args):
	"""defines set of methods executions. to get various inteface parameters.
	uses RunningInterfaces in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = RunningInterfaces(cmd_op)
	# R.interface_ips()
	# R.interface_v6_ips()
	# R.interface_vlans()
	# R.interface_channel_group()
	# R.interface_vrf()
	R.interface_ospf_auth()
	R.interface_udld()

	# # update more interface related methods as needed.

	return R.interface_dict

