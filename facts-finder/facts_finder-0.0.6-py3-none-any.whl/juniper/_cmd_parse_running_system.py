"""juniper system config parser from show config command """

# ------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import DIC

from facts_finder.juniper._cmd_parse_running import Running
from facts_finder.common import blank_line

merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------


class RunningSystem(Running):
	"""object for system level config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the  config output

		Args:
			cmd_op (list, str): config output, either list of multiline string
		"""    		    		
		super().__init__(cmd_op)
		self.system_dict = OrderedDict()

	def system_read(self, func):
		"""directive function to get the various system level output

		Args:
			func (method): method to be executed on system config line

		Returns:
			dict: parsed output dictionary
		"""    		
		op_dict = OrderedDict()
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("#"): continue
			spl = l.strip().split()

			func(op_dict, l, spl)
		return op_dict


	def system_hostname(self):
		"""update the system hostname details
		"""    		
		func = self.get_hostname
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_hostname(op_dict, l, spl):
		"""parser function to update system hostname details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		hostname = ""
		if l.startswith("set system host-name"): hostname = spl[-1]
		if hostname and not op_dict.get('hostname'):
			op_dict['hostname'] = hostname
		return op_dict


	def system_nameservers(self):
		"""update the system name server details
		"""    		
		func = self.get_nameservers
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_nameservers(op_dict, l, spl):
		"""parser function to update system name servers details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		dns = ''
		if l.startswith("set system name-server"): dns = spl[-1]
		if dns:
			if op_dict.get('name_servers'):
				op_dict['name_servers'] = op_dict['name_servers'] + "\n" + dns
			else:
				op_dict['name_servers'] = dns
		return op_dict


	def system_mgmt_ip(self):
		"""update the system management ip details
		"""    		
		func = self.get_mgmt_ip
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_mgmt_ip(op_dict, l, spl):
		"""parser function to update system management ip details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		ip = ""
		if l.startswith("set system ") and spl[-2] == "source-address": ip = spl[-1]
		if ip and not op_dict.get('management_ip'):
			op_dict['management_ip'] = ip
		return op_dict


	def system_gtac_servers(self):
		"""update the system gtac server details
		"""    		
		func = self.get_gtac_servers
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_gtac_servers(op_dict, l, spl):
		"""parser function to update system gtac servers details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		ip = ""
		if l.startswith("set system tacplus-server") : ip = spl[3]
		if ip and not op_dict.get('tacacs_servers'):
			op_dict['tacacs_servers'] = set()
		if ip: op_dict['tacacs_servers'].add(ip)
		return op_dict


	def system_syslog_servers(self):
		"""update the system syslog server details
		"""    		
		func = self.get_syslog_servers
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_syslog_servers(op_dict, l, spl):
		"""parser function to update system syslog servers details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		ip = ""
		if l.startswith("set system syslog host") : ip = spl[4]
		if ip and not op_dict.get('syslog_servers'):
			op_dict['syslog_servers'] = set()
		if ip: op_dict['syslog_servers'].add(ip)
		return op_dict


	def system_ntp_servers(self):
		"""update the system ntp server details
		"""    		
		func = self.get_ntp_servers
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_ntp_servers(op_dict, l, spl):
		"""parser function to update system ntp servers details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		ip = ""
		if l.startswith("set system ntp server") : ip = spl[4]
		if ip and not op_dict.get('ntp_servers'):
			op_dict['ntp_servers'] = set()
		if ip: op_dict['ntp_servers'].add(ip)
		return op_dict


	def system_banner(self):
		"""update the system banner details
		"""    		
		func = self.get_banner
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_banner(op_dict, l, spl):
		"""parser function to update system banner details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		banner = ""
		if l.startswith("set system login announcement"): banner = " ".join(spl[4:])
		if banner and not op_dict.get('banner'):
			op_dict['banner'] = banner
		return op_dict

	def system_as_number(self):
		"""update the system as details
		"""    		
		func = self.get_system_as_number
		merge_dict(self.system_dict, self.system_read(func))

	@staticmethod
	def get_system_as_number(op_dict, l, spl):
		"""parser function to update system as details

		Args:
			port_dict (dict): dictionary with a port info
			l (str): line to parse

		Returns:
			None: None
		"""    		
		banner = ""
		if l.startswith("set routing-options autonomous-system "): 
			as_no = spl[3]
			op_dict['system_bgp_as_number'] = as_no



	# # Add more interface related methods as needed.


# ------------------------------------------------------------------------------


def get_running_system(cmd_op, *args):
	"""defines set of methods executions. to get various system parameters.
	uses RunningSystem in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = RunningSystem(cmd_op)
	R.system_hostname()
	R.system_nameservers()
	R.system_mgmt_ip()
	R.system_gtac_servers()
	R.system_syslog_servers()
	R.system_ntp_servers()
	R.system_banner()
	R.system_as_number()
	
	# # update more interface related methods as needed.

	return R.system_dict



# ------------------------------------------------------------------------------

