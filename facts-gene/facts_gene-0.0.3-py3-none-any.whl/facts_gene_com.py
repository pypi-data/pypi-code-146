
from facts_gene import evaluate_cisco, evaluate_juniper
from facts_finder import device
from facts_finder.cisco_parser import Cisco
from facts_finder.juniper_parser import Juniper


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
		return evaluate_cisco(
			capture_log_file,
			capture_file,
			cisco_var_column_mapper_file,
			cisco_int_column_mapper_file
			)
	elif isinstance(dev, Juniper):
		return evaluate_juniper(
			capture_log_file,
			capture_file,
			juniper_column_mapper_file
			)
	return {'var': None, 'output': None}



