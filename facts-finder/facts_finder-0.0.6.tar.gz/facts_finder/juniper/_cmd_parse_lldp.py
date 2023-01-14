"""juniper lldp neighbour command output parser """

# ------------------------------------------------------------------------------
from facts_finder.common import remove_domain
from facts_finder.common import verifid_output
from facts_finder.cisco.common import standardize_if
# ------------------------------------------------------------------------------

def get_lldp_neighbour(cmd_op, *args, dsr=True):
	"""parser - show lldp neighbor command output

	Parsed Fields:
		* port/interface 
		* neighbor hostname
		* neighbor interface

	Args:
		cmd_op (list, str): command output in list/multiline string.
		dsr (bool, optional): DOMAIN SUFFIX REMOVAL. Defaults to True.

	Returns:
		dict: output dictionary with parsed fields
	"""
	cmd_op = verifid_output(cmd_op)
	nbr_d, remote_hn = {}, ""
	nbr_table_start = False
	for i, line in enumerate(cmd_op):
		line = line.strip()
		spl = line.split()
		if line.startswith("Local Interface"): 
			nbr_table_start = True
			continue
		if not nbr_table_start: continue
		if not line.strip(): continue				# Blank lines
		if line.startswith("Total "): continue		# Summary line
		if line.startswith("#"): continue			# Remarked line

		### NBR TABLE PROCESS ###

		# // LOCAL/NBR INTERFACE, NBR HOSTNAME //
		local_if = spl[0]
		remote_if = standardize_if(spl[-2].strip())
		remote_hn = spl[-1].strip()
		if dsr: remote_hn = remove_domain(remote_hn)

		# SET / RESET
		nbr_d[local_if] = {'neighbor': {}}
		nbr = nbr_d[local_if]['neighbor']
		nbr['hostname'] = remote_hn
		nbr['interface'] = remote_if
		local_if, remote_hn, remote_if = "", "", ""
	return nbr_d
# ------------------------------------------------------------------------------
