"""common functions for cisco devices """

# ------------------------------------------------------------------------------
from nettoolkit import IPv4, IPv6, to_dec_mask

from .statics import CISCO_IFSH_IDENTIFIERS
# ------------------------------------------------------------------------------

# ----------------------------------------------------------
def interface_type(ifname):
	"""get the interface type from interface string

	Args:
		ifname (str): interface name/string

	Raises:
		ValueError: raise error if input missing

	Returns:
		tuple: tuple with interface type (e.g PHYSICAL, VLAN...) and sub interface type 
		(e.g FastEthernet, .. ). None if not detected
	"""    	
	if not ifname: 
		raise ValueError(f"Missing mandatory input ifname")
	for int_type, int_types in  CISCO_IFSH_IDENTIFIERS.items():
		for sub_int_type in int_types:
			if sub_int_type.startswith(ifname):
				return (int_type, sub_int_type)

def standardize_if(ifname, expand=False):
	"""standardized interface naming

	Args:
		ifname (str): variable length interface name
		expand (bool, optional): expand will make it full length name. Defaults to False.

	Raises:
		ValueError: if missing with mandatory input
		TypeError: if invalid value detected
		KeyError: if invalid shorthand key detected		

	Returns:
		str: updated interface string
	"""    	
	if not ifname:
		raise ValueError("Missing mandatory input ifname")
	if not isinstance(expand, bool): 
		raise TypeError(f"Invalid value detected for input expand, "
		f"should be bool.")
	if not isinstance(ifname, str): 
		raise TypeError(f"Invalid value detected for input ifname, "
		f"should be str.")
	srcifname = ''
	for i in ifname:
		if not i.isdigit(): srcifname += i
		else: break
	if not srcifname: return None
	try:
		it = interface_type(srcifname)
		if it: 
			int_type, int_pfx = it[0], it[1]
		else:
			return ifname		
	except:
		raise TypeError(f"unable to detect interface type for {srcifname}")
	try:
		shorthand_len = CISCO_IFSH_IDENTIFIERS[int_type][int_pfx]
	except:
		raise KeyError(f"Invalid shorthand Key detected {int_type}, {int_pfx}")
	if expand:  return int_pfx+ifname[len(srcifname):]
	return int_pfx[:shorthand_len]+ifname[len(srcifname):]


def expand_if(ifname):
	"""get the full length interface string for variable length interface

	Args:
		ifname (str): variable length interface name

	Returns:
		str: updated interface string
	"""    	
	return standardize_if(ifname, True)

def expand_if_dict(d):
	"""returns updated the dictionary with standard expanded interface format in keys.

	Args:
		d (dict): dictionary where keys are interface names

	Returns:
		dict: updated dictionary keys with standard expanded interface format
	"""
	return {standardize_if(k, True):v for k, v in d.items()}

def get_interface_cisco(line):
	"""get the standard interface string from interface config line

	Args:
		ifname (str): line starting with interface [interface name]

	Returns:
		str: standard interface string
	"""    	
	return standardize_if(line[10:])


# ----------------------------------------------------------
def get_vlans_cisco(line):
	"""set of vlan numbers allowed for the interface.

	Args:
		line (str): interface config line containing vlan info

	Returns:
		dict: vlan information dictionary
	"""    	
	vlans = {'trunk': set(), 'access': None, 'voice': None, 'native': None}
	line = line.strip()
	if line.startswith("switchport trunk allowed"):
		vlans['trunk'] = trunk_vlans_cisco(line)
	elif line.startswith("switchport access vlan"):
		vlans['access'] = line.split()[-1]
	elif line.startswith("switchport voice vlan"):
		vlans['voice'] = line.split()[-1]
	elif line.startswith("switchport trunk native"):
		vlans['native'] = line.split()[-1]
	else:
		return None
	return vlans

def trunk_vlans_cisco(line):
	"""supportive to get_vlans_cisco(). derives trunk vlans

	Args:
		line (str): interface config line containing vlan info

	Returns:
		list, set: list or set of trunk vlans
	"""    	
	for i, s in enumerate(line):
		if s.isdigit(): break
	line = line[i:]
	# vlans_str = line.split()[-1]
	# vlans = vlans_str.split(",")
	line = line.replace(" ", "")
	vlans = line.split(",")
	if not line.find("-")>0:
		return vlans
	else:
		newvllist = []
		for vlan in vlans:
			if vlan.find("-")==-1: 
				newvllist.append(vlan)
				continue
			splvl = vlan.split("-")
			for vl in range(int(splvl[0]), int(splvl[1])+1):
				newvllist.append(vl)
		return set(newvllist)
# ---------------------------------------------------------------

def get_subnet(address):
	"""derive subnet number for provided ipv4 address

	Args:
		address (str): ipv4 address in string format a.b.c.d/mm

	Returns:
		str: subnet zero == network address
	"""    	
	return IPv4(address).subnet_zero()

def get_inet_address(line):
	"""derive the ipv4 information from provided line

	Args:
		line (str): interface config line

	Returns:
		str: ipv4 address with /mask , None if not found.
	"""    	
	if line.strip().startswith("ip address "):
		spl = line.split()
		ip  = spl[-2]
		mask = to_dec_mask(spl[-1])
		s = ip+"/"+str(mask)
		return s
	return None

def get_v6_subnet(address):
	"""derive subnet number for provided ipv6 address

	Args:
		address (str): ipv6 address in string with mask

	Returns:
		str: subnet zero == network address
	"""    	
	return IPv6(address).subnet_zero()

def get_inetv6_address(line, link_local):
	"""derive the ipv6 information from provided line

	Args:
		line (str): interface config line

	Returns:
		str: ipv6 address with /mask , None if not found.
	"""    	
	v6idx = -2 if link_local else -1
	if line.strip().startswith("ipv6 address "):
		spl = line.split()
		ip  = spl[v6idx]
		return ip
	return None

def get_int_ip(ip): 
	"""get ip address from ip/mask info

	Args:
		ip (str): ip with mask

	Returns:
		str: ip address
	"""	
	return ip.split("/")[0]

def get_int_mask(ip): 
	"""get mask from ip/mask info

	Args:
		ip (str): ip with mask

	Returns:
		str: mask
	"""	
	return ip.split("/")[-1]


# ---------------------------------------------------------------

def get_vrf_cisco(line):
	"""get the standard vrf string from vrf config line

	Args:
		ifname (str): line starting with vrf definition [vrf name]

	Returns:
		str: standard interface string
	"""    	
	vrfname = line.split()[-1]	
	return vrfname




