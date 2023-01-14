
from facts_finder import evaluate_cisco, evaluate_juniper
from facts_finder import device
from facts_finder.cisco_parser import Cisco, get_op_cisco
from facts_finder.juniper_parser import Juniper
from facts_finder.common import get_op, verifid_output
from nettoolkit import JSet


def evaluate(
	capture_log_file,
	capture_file,
	cisco_var_column_mapper_file,
	cisco_int_column_mapper_file,	
	juniper_column_mapper_file,	
	):
	"""evaluates captured log file, captured excel facts file, modify it according to provided mapper files,
	generates new output file by adding more details and by removing some unwanted fields.
	generated output excel file can be feed into config gneratation utility directly or by modifying it.

	"""

	dev = device(capture_log_file)
	if isinstance(dev, Cisco):
		ev = evaluate_cisco(
			capture_log_file,
			capture_file,
			cisco_var_column_mapper_file,
			cisco_int_column_mapper_file
			)
		try:
			hostname = ev['var'].hostname
			config = get_op_cisco(capture_log_file, 'show running-config')
		except:
			print("Some of additional Para capture failed..!!")
	elif isinstance(dev, Juniper):
		ev = evaluate_juniper(
			capture_log_file,
			capture_file,
			juniper_column_mapper_file
			)
		try:
			hostname = ev['var'].hostname
			cmd_op = get_op(capture_log_file, 'show configuration')
			JS = JSet(input_list=cmd_op)
			JS.to_set
			config = verifid_output(JS.output)
		except:
			print("Some of additional Para capture failed..!!")
	else:
		return None



	return {
		'hostname': hostname,
		'dev_type': dev, 
		'var': ev['var'], 
		'output': ev['output'],
		'config': config,
		}



