"""cisco cdp neighbour command output parser """

# ------------------------------------------------------------------------------
from facts_finder.common import remove_domain
from facts_finder.common import verifid_output
from facts_finder.cisco.common import standardize_if
# ------------------------------------------------------------------------------

def get_cdp_neighbour(cmd_op, *args, dsr=True):
	"""parser - show cdp neigh command output

	Parsed Fields:
		* port/interface
		* neighbor interface
		* neighbor plateform
		* neighbor hostname

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
		dbl_spl = line.split("  ")
		if line.startswith("Device ID"): 
			nbr_table_start = True
			continue
		if not nbr_table_start: continue
		if not line.strip(): continue				# Blank lines
		if line.startswith("Total "): continue		# Summary line
		if line.startswith("!"): continue			# Remarked line

		### NBR TABLE PROCESS ###

		# // NBR HOSTNAME //
		if not remote_hn:
			remote_hn = dbl_spl[0].strip()
			if dsr: remote_hn = remove_domain(remote_hn)
		if len(line.split()) == 1:  continue

		# // LOCAL/NBR INTERFACE, NBR PLATFORM //
		local_if = standardize_if("".join(dbl_spl[0].split()))
		remote_if = standardize_if("".join(dbl_spl[-1].split()[1:]))
		remote_plateform = dbl_spl[-1].split()[0]

		# SET / RESET
		nbr_d[local_if] = {'neighbor': {}}
		nbr = nbr_d[local_if]['neighbor']
		nbr['hostname'] = remote_hn
		nbr['interface'] = remote_if
		nbr['plateform'] = remote_plateform
		remote_hn, remote_if, remote_plateform = "", "", ""
	return nbr_d
# ------------------------------------------------------------------------------
