# ------------------------------------------------------------------------------
from nettoolkit import IPv4, IPv6

# ------------------------------------------------------------------------------

def get_subnet(address):
	"""get subnet zero network address for provided v4 address

	Args:
		address (str): ipv4 address

	Returns:
		str: subnet zero/network address
	"""	
	return IPv4(address).subnet_zero()

def get_v6_subnet(address):
	"""get subnet zero network address for provided v6 address

	Args:
		address (str): ipv6 address

	Returns:
		str: subnet zero/network address
	"""	
	return IPv6(address).subnet_zero()

def get_vlans_juniper(spl, how="s"):
	"""get the list of vlans on the interface

	Args:
		spl (list): splitted line

	Returns:
		list: list of vlans
	"""    	
	memberlist_identifiers = ('vlan-id-list', 'members')
	is_any_members = False
	for memid in memberlist_identifiers:
		is_any_members = memid in spl
		if is_any_members: break
	if not is_any_members: return None
	int_vl_list = [int(vl) for vl in spl[spl.index(memid)+1:] if vl.isdigit()]
	str_vl_list = [vl for vl in spl[spl.index(memid)+1:] if vl.isdigit()]
	if how == 's':
		return str_vl_list
	else:
		return int_vl_list


# ------------------------------------------------------------------------------
