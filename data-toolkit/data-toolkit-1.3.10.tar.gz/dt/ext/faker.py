COL_TYPES = ['float', 'categorical', 'string']

import faker
import pandas as pd
import pyperclip
import time
import os

def replicate_cliboard(columns):
    # get the clipboard
    clipboard = pyperclip.paste()
    # get the clipboard as a list of lines
    clipboard_list = clipboard.splitlines()
    
    # split into columns based on \t
    clipboard_list = [line.split('\t') for line in clipboard_list]
    
    # convert to pandas dataframe
    df = pd.DataFrame(clipboard_list)
    
    if columns:
        # replace make the header column the first row
        df.columns = df.iloc[0]
        df = df.reindex(df.index.drop(0))
    
    return df


def infer_col_type(column: pd.Series):
    '''
    Infer column type
    '''
    if isinstance(column, pd.DataFrame):
        return 'dataframe'
    if isinstance(column, pd.Series):
        try:
            column = column.astype(float)
            # TODO: if there's a distinct set of int values, then cast to int
            
            return 'float'
        except ValueError:
            pass
        
        is_10_pct = column.value_counts().shape[0] > .1*column.shape[0]
        if is_10_pct:
            return 'categorical'
        else:
            return 'string'
    else:
        print('Not a pandas object')
        return
    
def generate_categorical_col(faker, categorical_properties):
    '''
    Returns a random value from the list of values
    '''
    elements = categorical_properties
    return faker.random_element(elements=elements)

def generate_string_col(faker, string_properties):
    '''
    Returns a string of length between the min and max of the column
    '''
    min_, max_ = int(string_properties[0]), int(string_properties[1])
    return faker.pystr(min_chars=min_, max_chars=max_)
    
def generate_numeric_col(faker, number_properties):
    '''
    Returns a float between the min and max of the column
    '''
    min_, max_ = float(number_properties[0]), float(number_properties[1])
    # enforfce that min_ and max_ are actually less than each other
    if min_ > max_: min_, max_ = max_, min_
    try:
        fake_values = faker.pyfloat(min_value=min_, max_value=max_, right_digits=2)
    except:
        import ipdb; ipdb.set_trace()
        
    return fake_values


def generate_fake_data(n_lines, template,
                       columns, csv, primary_key,
                       delimiter=','):
    '''
    Main worker function to generate fake data
    '''
    if not template:
        df = replicate_cliboard(columns)
    else:
        if template.endswith('.csv'):
            df = pd.read_csv(template, delimiter=delimiter)
    
     # create a fake data generator
    fake = faker.Faker()
    
    number_properties = {}
    categorical_properties = {}
    string_properties = {}
    
    # TODO: this should probably be rewritten to not redo the for loop so many times
    
    # for each column infer the type
    data_types = { col: infer_col_type(df[col]) for col in df.columns }
    
    print(f"Replicating df of shape: {df.shape} with following data types: {data_types}")
    
    # filter values of the data_types dict so that we only get the columns of the specified type
    filter_col_type = lambda dictionary, value: [key for key, val in dictionary.items() if val == value]
    
    # get the properties of numeric column
    for col in filter_col_type(data_types, 'float'):
        number_properties[col] = min(df[col]), max(df[col])
        
    for col in filter_col_type(data_types, 'categorical'):
        categorical_properties[col] = df[col].value_counts().index.tolist()
        
    for col in filter_col_type(data_types, 'string'):
        string_properties[col] = min(df[col].str.len()), max(df[col].str.len())
        
    # create the fake data
    fake_data = []
    for i in range(n_lines):
        line = []
        for col in df.columns:
            
            if data_types[col] == 'float':
                line.append(generate_numeric_col(fake, number_properties[col]))
            elif data_types[col] == 'categorical':
                line.append(generate_categorical_col(fake, categorical_properties[col]))
            elif data_types[col] == 'string':
                line.append(generate_string_col(fake, string_properties[col]))
            
        fake_data.append(line)
    
    # convert to dataframe
    df_fake = pd.DataFrame(fake_data)
    
    # rename the columns
    if columns:
        df_fake = df_fake.rename(columns={i:col for i, col in enumerate(df.columns)})
    
    if primary_key=='-1':
        # generate a primary key
        df_fake['primary_key'] = [fake.uuid4() for i in range(df_fake.shape[0])]
    
    # save as a csv with time
    if csv:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        df_fake.to_csv(f'fake_data_{timestamp}.csv', index=False)
        print(f"Saved full path: {os.getcwd()}/fake_data_{timestamp}.csv")
        
    else:
        print(df_fake)
        