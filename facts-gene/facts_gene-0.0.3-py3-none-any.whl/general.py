import pandas as pd
import numpy as np
import nettoolkit as nt

# ================================================================================================
# Common general functions
# ================================================================================================
def get_model_template_version(template_file):
	with open(template_file, 'r') as f:
		lns = f.readlines()
		for l in lns:
			if l.find("template_version") > 0:
				template_ver = l.split('"')[1]
			if l.find("set model") > 0:
				model = l.split('"')[1].lower()
	return model,template_ver

# ================================================================================================

def merged_physical(file, new_df):
	new_df = new_df.reset_index()
	new_df.rename(columns={'Interfaces': 'interface'}, inplace=True)
	phy_df = pd.read_excel(file, sheet_name='tables').fillna("")
	pdf = pd.merge( phy_df, new_df, on=['interface',], how='outer').fillna("")
	return pdf

def merged_vrf(file, new_df):
	new_df = new_df.reset_index()
	phy_df = pd.read_excel(file, sheet_name='vrf').fillna("")
	pdf = pd.merge( phy_df, new_df, on=['vrf',], how='outer').fillna("")
	return pdf

def merged_var(file, new_df):
	new_df = new_df.reset_index()
	phy_df = pd.read_excel(file, sheet_name='var').fillna("")
	pdf = pd.merge( phy_df, new_df, on=['var',], how='outer').fillna("")	
	return pdf

def remove_duplicates(df, *cols):
	duplicated_cols = {col+"_x": col+"_y" for col in cols}
	for x, y in duplicated_cols.items():
		if df[x].equals(df[y]):
			df.rename(columns={x: x[:-2]}, inplace=True)
		else:
			df[x[:-2]] = np.where( df[x]!="", df[x], df[y]) 
			df.drop([x], axis=1, inplace=True)
		df.drop([y], axis=1, inplace=True)
	return df


def split_to_multiple_tabs(pdf):
	set_of_filters = set(pdf['filter'])
	d = {}
	for f in set_of_filters:
		df = pdf[ pdf['filter']==f ]
		d[f] = df		
	pdf = d
	return pdf

def update_int_number(number):
	start = 2
	if number.startswith("Tw"):
		start = 3
	s = 0
	for i, n in enumerate(reversed(number[start:].split("/"))):
		multiplier = 100**i
		nm = int(n)*multiplier
		s += nm
	return s

def generate_int_number(pdf):
	for sheet, df in pdf.items():
		if sheet != 'physical':
			pdf[sheet]['int_number'] =  df['interface'].apply(lambda x: int(x[2:]))
		else:
			pdf[sheet]['int_number'] =  df['interface'].apply(update_int_number)
		pdf[sheet].sort_values(by=['int_number'], inplace=True)
	return pdf

def generate_int_number_juniper(pdf):
	for sheet, df in pdf.items():
		if sheet == 'physical':
			pdf[sheet]['int_number'] = df['interface'].apply( get_physical_port_number )
		if sheet == 'aggregated':
			pdf[sheet]['int_number'] = df['interface'].apply(lambda x: int(x[2:])) 
		if sheet == 'vlan':
			pdf[sheet]['int_number'] = df['interface'].apply(lambda x: x.split(".")[-1]) 
	return pdf

def get_physical_port_number(port):
    port = port.split(".")[0]
    port_lst = port.split("-")[-1].split("/")
    port_id = 0
    for i, n in enumerate(reversed(port_lst)):
        multiplier = 100**i
        nm = int(n)*multiplier
        port_id += nm
    return port_id
