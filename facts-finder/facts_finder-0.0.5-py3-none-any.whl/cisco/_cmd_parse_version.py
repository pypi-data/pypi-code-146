"""cisco show version command output parser """

# ------------------------------------------------------------------------------
from facts_finder.common import verifid_output
from facts_finder.common import blank_line

# ------------------------------------------------------------------------------

def get_version(cmd_op, *args):
	"""parser - show version command output

	Parsed Fields:
		* software
		* bootfile
		* serial
		* model

	Args:
		cmd_op (list, str): command output in list/multiline string.

	Returns:
		dict: output dictionary with parsed fields
	"""	
	cmd_op = verifid_output(cmd_op)
	op_dict = {}
	sw, bootfile, srno, model = '', '', '', ''
	for l in cmd_op:
		if blank_line(l): continue
		if l.strip().startswith("!"): continue
		spl = l.strip().split()
		if l.find("Software, Version") > -1:
			sw = spl[-1]
		if l.startswith("System image file"):
			bootfile = spl[-1]
		if not srno and (l.startswith("System Serial") or l.startswith("Processor board ID")):
			srno = spl[-1]
		if l.startswith("Model Number"):
			model = spl[-1]
	op_dict['software'] = sw
	op_dict['bootfile'] = bootfile
	op_dict['serial'] = srno
	op_dict['model'] = model
	return op_dict
# ------------------------------------------------------------------------------
