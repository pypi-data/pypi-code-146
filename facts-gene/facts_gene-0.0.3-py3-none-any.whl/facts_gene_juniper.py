from pprint import pprint

from facts_gene import KeyExchanger
from facts_gene import VarInterfaceJuniper
from facts_gene import TableInterfaceJuniper
from facts_gene import DeviceFactsFg
from capture_it.database import write_to_xl, append_to_xl

from facts_finder.common import get_op
from nettoolkit import JSet
from facts_finder.common import verifid_output
import os

# ================================================================================================

def evaluate_juniper(
	capture_log_file,
	capture_file,
	column_mapper_file,
	):

	# ================================================================================================
	# var
	# ================================================================================================

	juniper_cmd_lst = {
		"show chassis firmware | no-more":{},
		"show chassis hardware | no-more":{},
		"show lacp interfaces | no-more":{},
		"show arp no-resolve | no-more":{},
		"show isis adjacency | no-more":{},
		"show lldp neighbors | no-more":{},
		"show ospf neighbor | no-more":{},
		"show system uptime | no-more":{},
		"show interfaces | no-more":{},
		"show version | no-more":{},
		"show configuration | no-more":{},	
	}

	output_file = f'{capture_file}-facts_Gene.xlsx'		## Output Excel Facts Captured File

	## 1. --- Cleanup old
	try: os.remove(output_file)	# remove old file if any
	except: pass

	## 2. ---  `var` Tab 
	KEC_VAR = KeyExchanger(column_mapper_file, juniper_cmd_lst)
	juniper_cmd_lst = KEC_VAR.cisco_cmd_lst
	CIV = VarInterfaceJuniper(capture_file)
	CIV.execute(juniper_cmd_lst)
	append_to_xl(output_file, CIV.var)

	## 3. ---  `table` Tab 

	CID = TableInterfaceJuniper(capture_file)
	CID.execute(juniper_cmd_lst)
	append_to_xl(output_file, CID.pdf)

	# ## 5. --- `facts-gene` updates generated output excel; per required column names; based Excel column Mappers.
	DFF = DeviceFactsFg(capture_log_file, output_file)
	DFF.execute_juniper()

	print(f'Check output in -> {output_file}')

	return {'var': CIV, 'output': output_file}


	# ## 6. ---  `Customer` Specific variables.
	# # ## 6.1 --- required variables.
	# hostname = CIV.hostname
	# cmd_op = get_op(capture_log_file, 'show configuration')
	# JS = JSet(input_list=cmd_op)
	# JS.to_set
	# running = verifid_output(JS.output)

	# # ## 6.2 --- `Custom` Modifications
	# # try:
	# ADF = AttDeviceFacts(hostname, running, output_file)
	# ADF.execute_juniper()
	# append_to_xl(output_file, ADF.pdf)
	# append_to_xl(output_file, ADF.var)
	# append_to_xl(output_file, ADF.dslots_ddf)
	# # except:
	# # 	print("Custom Facts Module not available, Modifications skipped. ")

# # ================================================================================================
# # Executions
# # ================================================================================================

# device = 'h5w-ecd-a-kyn'

# capture_folder = './captures/' 
# capture_log_file = f"{capture_folder}{device}.log"	##  Text Log File
# capture_file = f'{capture_folder}{device}.xlsx'		##  Excel Captured File
# facts_gene = f'{capture_file}-facts_Gene.xlsx'		## Output Excel Facts Captured File

# ## Excel Column Mappers
# column_mapper_file = './facts_gene-x/templates/test-ints-j.xlsx'

# evaluate_juniper(
# 	capture_log_file,
# 	capture_file,
# 	column_mapper_file,
# 	)

# # ================================================================================================


