import pandas as pd
import numpy as np

def deduplicate_concatenate_duns(duns:pd.DataFrame, *args:str) -> pd.DataFrame:
    """ This function deduplicates the duns dataset based on organization id + postcode, subsequently ranks on descending FTE and concatenates values in rows before deduplication. 
        The input will be the entire duns dataset and optional arguments refering to the column names for concatenation.
    """

    # create key for deduplication using organization ID, postal code, house number, and suffix
    duns['deduplicate'] = duns.apply(lambda x: str(x['Organization ID']) + str(x['Postal Code']) + str(x['House number']) + str(x['House number suffix']), axis=1)
    duns['deduplicate'] = duns['deduplicate'].apply(lambda x: ''.join(x.replace('nan', '').replace('.0', '').split()))

    # for each variable mentioned, create a cc_dd (concatenate values to retain information)
    for variable in args:
        new_variable_name = '_'.join(variable.split()) + '_cc_dd'    
        duns[new_variable_name] = duns[variable].astype(str)
        duns[new_variable_name] = duns[new_variable_name].apply(lambda x: x.replace('nan', '').replace('.0', ''))
        duns[new_variable_name] = duns.groupby(['deduplicate'])[new_variable_name].transform(lambda x: ' / '.join(x))
        duns[new_variable_name] = duns[new_variable_name].apply(lambda x: [item for item in list(set(x.split(' / '))) if item != 'nan'])
        duns[new_variable_name] = duns[new_variable_name].apply(lambda x: ', '.join(x))
        duns[new_variable_name] = duns[new_variable_name].replace(r'^\s*$', np.nan, regex=True) 

    # sort based on employees on entity
    duns = duns.sort_values(['deduplicate', '# employees on entity'], ascending=[True, False])        

    # drop duplicates
    duns = duns.drop_duplicates(subset=['deduplicate'], keep='first')     

    # change columns order
    column_order = []
    for col in duns.columns:
        if '_cc_dd' not in col:
            column_order.append(col)
            if '_'.join(col.split()) + '_cc_dd' in duns:
                column_order.append('_'.join(col.split()) + '_cc_dd')
    duns = duns[column_order] 

    return duns


def deduplicate_concatenate_duns_strict(duns:pd.DataFrame, *args:str) -> pd.DataFrame:
    """ This function deduplicates the duns dataset based on organization id + postcode, subsequently ranks on descending FTE and concatenates values in rows before deduplication. 
        The input will be the entire duns dataset and optional arguments refering to the column names for concatenation.
    """

    # create key for deduplication using organization ID and postal code
    duns['deduplicate'] = duns.apply(lambda x: str(x['Organization ID']) + str(x['Postal Code']), axis=1)
    duns['deduplicate'] = duns['deduplicate'].apply(lambda x: ''.join(x.replace('nan', '').replace('.0', '').split()))

    # for each variable mentioned, create a cc_dd (concatenate values to retain information)
    for variable in args:
        new_variable_name = '_'.join(variable.split()) + '_cc_dd'    
        duns[new_variable_name] = duns[variable].astype(str)
        duns[new_variable_name] = duns[new_variable_name].apply(lambda x: x.replace('nan', '').replace('.0', ''))
        duns[new_variable_name] = duns.groupby(['deduplicate'])[new_variable_name].transform(lambda x: ' / '.join(x))
        duns[new_variable_name] = duns[new_variable_name].apply(lambda x: [item for item in list(set(x.split(' / '))) if item != 'nan'])
        duns[new_variable_name] = duns[new_variable_name].apply(lambda x: ', '.join(x))
        duns[new_variable_name] = duns[new_variable_name].replace(r'^\s*$', np.nan, regex=True) 

    # sort based on employees on entity
    duns = duns.sort_values(['deduplicate', '# employees on entity'], ascending=[True, False])        

    # drop duplicates
    duns = duns.drop_duplicates(subset=['deduplicate'], keep='first')     

    # change columns order
    column_order = []
    for col in duns.columns:
        if '_cc_dd' not in col:
            column_order.append(col)
            if '_'.join(col.split()) + '_cc_dd' in duns:
                column_order.append('_'.join(col.split()) + '_cc_dd')
    duns = duns[column_order] 

    return duns


def find_key_id(item:str, lst:list):
    """ This function searches the entire concatenation for the mtching key for merging.
        It requires the values to be concatenated by a comma.
        Input is the concatenation (string) and a list of keys to look for.
    """
    try:
        item = item.split(', ')
        item = [int(x) for x in item]
        output = list(set(item) & set(lst))
        if output:
            return True
        else:
            return False
    except:
        return False    


# def deduplicate_concatenate_duns_ext(duns:pd.DataFrame, *args:str) -> pd.DataFrame:
#     """ This function deduplicates the duns dataset based on organization id + postcode + du number, subsequently ranks on descending FTE and concatenates values in rows before deduplication. 
#         The input will be the entire duns dataset and optional arguments refering to the column names for concatenation.
#     """

#     # create key for deduplication using organization ID and postal code
#     duns['deduplicate'] = duns.apply(lambda x: str(x['Organization ID']) + str(x['Postal Code']) + str(x['DU DUNS Number']), axis=1)
#     duns['deduplicate'] = duns['deduplicate'].apply(lambda x: ''.join(x.replace('nan', '').replace('.0', '').split()))

#     # for each variable mentioned, create a cc_dd (concatenate values to retain information)
#     for variable in args:
#         new_variable_name = '_'.join(variable.split()) + '_cc_dd'    
#         duns[new_variable_name] = duns[variable].astype(str)
#         duns[new_variable_name] = duns[new_variable_name].apply(lambda x: x.replace('nan', '').replace('.0', ''))
#         duns[new_variable_name] = duns.groupby(['deduplicate'])[new_variable_name].transform(lambda x: ' / '.join(x))
#         duns[new_variable_name] = duns[new_variable_name].apply(lambda x: [item for item in list(set(x.split(' / '))) if item != 'nan'])
#         duns[new_variable_name] = duns[new_variable_name].apply(lambda x: ', '.join(x))
#         duns[new_variable_name] = duns[new_variable_name].replace(r'^\s*$', np.nan, regex=True) 

#     # sort based on employees on entity
#     duns = duns.sort_values(['deduplicate', '# employees on entity'], ascending=[True, False])        

#     # drop duplicates
#     duns = duns.drop_duplicates(subset=['deduplicate'], keep='first')     

#     # change columns order
#     column_order = []
#     for col in duns.columns:
#         if '_cc_dd' not in col:
#             column_order.append(col)
#             if '_'.join(col.split()) + '_cc_dd' in duns:
#                 column_order.append('_'.join(col.split()) + '_cc_dd')
#     duns = duns[column_order] 

#     return duns