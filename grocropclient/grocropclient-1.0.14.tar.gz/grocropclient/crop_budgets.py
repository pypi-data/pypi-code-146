import io
import json
import requests 

import pandas as pd

from grocropclient.constants import ItemNameCategoryList
from grocropclient.crop_budgets_data import METRIC_MAPPING


API_HOST = "api.gro-intelligence.com"
PRECISION = 2

# To get all crop budget tables from the CSV above.
def get_all_crop_budgets(api_host, api_token, crop='', state=''):
  try:
    crop = crop.lower()
    state = state.lower()
  except AttributeError as e:
    raise TypeError(f'crop and state parameters must be strings') from e
  if state:
      state = state.replace(' ', '_') # the source name uses underscore for multiword US states.
  headers = { 'Authorization' : f'Bearer {api_token}' }
  endpoint = 'crop-budget-available-series'
  url = "/".join(["https:", "", api_host, endpoint])
  resp = requests.get(url=url,
                    headers=headers)
  json_resp = json.dumps(resp.json()['data'])
  df = pd.read_json(json_resp, orient='records')
  for col in df.columns:
    camel_case_col = col
    snake_case_col = __camel_case_to_snake_case(col)
    df.rename(columns = {camel_case_col: snake_case_col}, inplace=True)
  # Filter out crop budgets for item_names that are not for Corn or Soybeans crops
  df = df[df['item_name'].apply(lambda x: x.lower()).str.contains(f'{ItemNameCategoryList.CORN.value}|{ItemNameCategoryList.SOYBEANS.value}')]
  return df.loc[df.item_name.apply(lambda x: x.split(',')[0]).str.lower().str.contains(crop) & df.source_name.str.contains(state, case=False)]


def __crop_budget_json_to_df2(crop_budget_as_json: dict) -> pd.DataFrame:
    flattened_metrics = __flatten_to_list(METRIC_MAPPING)
    csv_str = __json_to_csv(crop_budget_as_json, flattened_metrics)
    csv_string_io = io.StringIO(csv_str)
    return pd.read_csv(csv_string_io, sep=',').round(decimals=PRECISION)


# To get a single crop budget, converted into a Pandas dataframe.
def get_crop_budget_as_df(api_host, api_token, source_name, item_name, region_name, productivity):
  headers = { 'Authorization' : f'Bearer {api_token}' }
  params = {'sourceName': source_name, 'itemName': item_name, 'regionName': region_name, 'productivity': productivity}
  endpoint = 'crop-budget'
  url = "/".join(["https:", "", api_host, endpoint])
  resp = requests.get(url=url,
                    headers=headers,
                    params=params)
  return __crop_budget_json_to_df2(resp.json())

def __flatten_to_list(obj, parent = None, res = None):
    if not res:
        res = []
    for key in obj:
        res.append(key)
        if parent:
            prop_name = parent + '.' + key
        else:
            prop_name = key
        
        if isinstance(obj[key], list):
            for item in obj[key]:
                res.append(item)
        elif isinstance(obj[key], dict):
            __flatten_to_list(obj[key], prop_name, res)

    return res


def __json_to_csv(json_input: dict, row_order):
    csv_rows = []
    title = '"Crop Budget"'
    
    first_key = list(json_input.keys())[0]
    first_row = json_input[first_key]['data']
    keys = list(first_row.keys())
    header = [title] + keys
    header_str = ','.join(header)
    csv_rows.append(header_str)
    
    for name in row_order:
        if name in json_input:
            row_name = [f'"{name}"']
            row = json_input[name]['data']
            values = list(row.values())
            values_str = [str(value) for value in values]
            row_data = row_name + values_str
            row_str = ','.join(row_data)
            csv_rows.append(row_str)
    return '\n'.join(csv_rows)


def __camel_case_to_snake_case(col):
    res = [col[0].lower()]
    for c in col[1:]:
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            res.append('_')
            res.append(c.lower())
        else:
            res.append(c)
     
    return ''.join(res)
