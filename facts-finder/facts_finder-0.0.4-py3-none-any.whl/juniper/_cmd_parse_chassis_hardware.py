"""juniper interface description command output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict

from facts_finder.common import verifid_output

# ------------------------------------------------------------------------------

def get_chassis_hardware(cmd_op, *args):
	"""parser - show chassis hardware command output

	Parsed Fields:
		* port/interface 
		* port_type

	Args:
		cmd_op (list, str): command output in list/multiline string.

	Returns:
		dict: output dictionary with parsed fields
	"""
	cmd_op = verifid_output(cmd_op)
	op_dict = OrderedDict()
	toggle = False
	JCH = JuniperChassisHardware(cmd_op)
	for arg in args:
		ports = arg['Interfaces']
		break
	for p, port_attr in  ports.items():	
		sfp = JCH.get_sfp(p)
		if not sfp: continue
		op_dict[p] = {}
		op_dict[p]["port_type"] = sfp
	return op_dict


class JuniperChassisHardware():
	"""read the show chassis hardware output from juniper and returns port type(sfp)"""

	def __init__(self, output):
		"""initialize and read output

		Args:
			output (list): show chassis hardware output in list
		"""    		
		self.fpc, self.pic = '', ''
		self.port = ''
		self.ports = {}
		self._read(output)

	def _read(self, output):
		"""read the output and adds line to port info
		"""    		
		for l in output:
			if not l.strip(): continue
			self._add(l)

	def _add(self, line):
		"""adds port info from line 
		"""    		
		# if line.upper().find("BUILTIN") > 0: return         # Some of juniper output are incosistent so removed.
		spl = line.strip().split()
		if not spl[0].upper() in ("FPC", "PIC", "XCVR"): return
		if spl[0].upper() in ("FPC"):
			self.fpc = spl[1]
			self.pic = ''
		elif spl[0].upper() in ("PIC"):
			self.pic = self.fpc + "/" + spl[1]
		elif spl[0].upper() in ('XCVR',):
			self.port = self.pic + "/" + spl[1]
			self.ports[self.port] = spl[-1]
			self.port=''

	def get_sfp(self, port):
		"""get the SFP details for given port

		Args:
			port (str): port number only (port type to be excluded)

		Returns:
			str: SFP type
		"""    		
		for p, sfp in self.ports.items():
			spl_port = port.split("-")
			if spl_port[-1] == p:
				return sfp
		return ""

