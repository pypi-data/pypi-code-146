"""juniper interface description command output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict

from facts_finder.common import verifid_output
from facts_finder.common import blank_line
from facts_finder.common import get_string_trailing
# ------------------------------------------------------------------------------

def get_int_description(cmd_op, *args):
	"""parser - show interfaces description command output

	Parsed Fields:
		* port/interface 
		* description

	Args:
		cmd_op (list, str): command output in list/multiline string.

	Returns:
		dict: output dictionary with parsed fields
	"""
	cmd_op = verifid_output(cmd_op)
	op_dict = OrderedDict()

	nbr_d, remote_hn = {}, ""
	nbr_table_start = False
	for l in cmd_op:
		if blank_line(l): continue
		if l.strip().startswith("#"): continue
		if l.startswith("Interface"): 
			desc_begin_at = l.find("Description")
			continue
		spl = l.strip().split()
		p = spl[0]
		if not op_dict.get(p): op_dict[p] = {}
		port = op_dict[p]
		port['description'] = get_string_trailing(l, desc_begin_at)
	return op_dict
# ------------------------------------------------------------------------------
