import os
import codecs
import json
import pandas as pd
import numpy as np

def generate_variable_overview(input_path: str, analysis: int) -> pd.DataFrame:
    
    os.chdir(input_path)
    file_name = r'{0}.json'.format(str(analysis))
    json_data = codecs.open(file_name, mode='r', encoding='UTF-8-SIG')
    json_file = json.load(json_data)
    
    # Reducing output of query
    try:
        
        df_data = json_file['data']['administrator']['consultant']['bgVariables']
        
    except KeyError:
        
        df_data = json_file['data']['administrator']['consultant']['fgVariables']

    # Creating dataframe 
    df = pd.DataFrame(df_data)

    # Removing line breaks, carriage returns and tabs from labels
    df['text'].replace(to_replace=[r'\\t|\\n|\\r', '\t|\n|\r'], value=[' ',' '], regex=True, inplace=True)    

    # Creating dataframe with choice info
    df_choices = df[df['choiceInfo'].map(lambda d: len(d)) > 0]

    # Creating columns with number of choices
    pd.options.mode.chained_assignment = None
    df_choices['nb_choices'] = df['choiceInfo'].apply(lambda x: len(x))
    pd.options.mode.chained_assignment = 'warn'

    # Creating one row pr. choice    
    df_choices = df_choices.explode('choiceInfo').reset_index()

    # Extracting info form concatenated strings
    df_choices['choice_id'] = [d.get('choiceId') if type(d) == dict else '' for d in df_choices['choiceInfo']]
    df_choices['choice_value'] = [d.get('value') if type(d) == dict else '' for d in df_choices['choiceInfo']]
    df_choices['choice_text'] = [d.get('text') if type(d) == dict else '' for d in df_choices['choiceInfo']]

    # Creating full reference which is used to merge choice data onto df
    df_choices['part1'] = df_choices['reference'].str.extract(r'({\*.*)\*}')
    df_choices['fullRef'] = df_choices['part1'] + r':' + df_choices['choice_id'].astype(str) + r'*}'

    df_choices = df_choices[['fullRef', 'choice_value', 'choice_id', 'nb_choices']]

    df = pd.merge(left=df, right=df_choices, how='left', left_on='reference', right_on='fullRef')

    # Creating full variable name (scope/varName)
    df['analysisId'] = df['id'].str.split('_', expand=True)[0]
    df['scopeShort'] = df['id'].str.split('_', expand=True)[1]

    df['choice_value_1'] = df.choice_value.fillna(0).astype(int).astype(str)

    df['name'].fillna(method='ffill', inplace=True)

    df['fullName'] = ''
    df['fullName_1'] = ''
    df['fullName_2'] = ''
    df['fullName_2'] = df['scopeShort'].str.lower() + r'/' + df['name'].str.lower()
    df['choice_id_adj'] = (df.groupby(['fullName_2'])['name'].rank(method='first') - 1).astype(int)
    df['fullName_1'] = df['scopeShort'].str.lower() + r'/' + df['name'].str.lower() + r'_' + df['choice_id_adj'].astype(str)
    
    df['fullName'] = np.where((df['referenceType'].str.contains(r'TypeChoiceMultiple')) & (df['nb_choices']>1), df['fullName_1'], df['fullName_2'])

    df['adj_name'] = df['fullName'].str.replace('/', '__')
    df['adj_name'] = df['adj_name'].str.lower()

    df['analysis_var_ref'] = df['analysisId'] + '_' + df['reference']

    return df