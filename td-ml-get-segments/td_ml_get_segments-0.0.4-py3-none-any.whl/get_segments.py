import tdclient
import requests
import json
import pytd
import pytd.pandas_td as td
import pandas as pd
import os
import sys
import numpy as np
import re
import ast

apikey = os.environ['TD_API_KEY'] 
tdserver = os.environ['TD_API_SERVER']
sink_database = os.environ['SINK_DB']
folder_depth = os.environ['FOLDER_DEPTH']
output_table = os.environ['OUTPUT_TABLE']
output_table2 = os.environ['OUTPUT_TABLE2']
segment_api = tdserver.replace('api', 'api-cdp')
headers= {"Authorization":'TD1 '+ apikey, "content-type": "application/json"}
v5_flag=os.environ['v5_flag']
ps_to_include=os.environ['ps_to_include']
folders_to_include=os.environ['folders_to_include']
segments_to_include=os.environ['segments_to_include']


############ Function to Read JSON #####################
def json_extract(url):
    #Get Segment Info JSON from Master Segment using TD API
    get_info = requests.get(url, headers=headers)

    return get_info.json()

##########Function to extract Parent Segment Info from V4 and V5 ###########
def get_ps_list():
    v4_segment_list = f'{segment_api}/audiences'
    v5_segments_list = f'{segment_api}/entities/parent_segments'
    v4_dic = dict(ps_id = [], ps_name = [], ps_population = [], root_folder = [])
    v5_dic = dict(ps_id = [], ps_name = [], ps_population = [], root_folder = [])
    
    if v5_flag=='0':
        v4_ps = json_extract(v4_segment_list)
        for item in v4_ps:
            v4_dic['ps_id'].append(item['id'])
            v4_dic['ps_name'].append(item['name'])
            v4_dic['ps_population'].append(item['population'])
            v4_dic['root_folder'].append(item['rootFolderId'])

        v4_df = pd.DataFrame(v4_dic)
        v4_df.fillna(0, inplace = True)
        v4_df['v5_flag'] = 0
        new_df = v4_df
        new_df.reset_index(drop = True, inplace = True)

    elif v5_flag=='1': 
        v5_ps = json_extract(v5_segments_list)
        v5_ps_data = v5_ps['data']
        for item in v5_ps_data:
            v5_dic['root_folder'].append(item['id'])
            v5_dic['ps_name'].append(item['attributes']['name'] + " Root")
            v5_dic['ps_population'].append(item['attributes']['population'])
            v5_dic['ps_id'].append(item['relationships']['parentSegmentFolder']['data']['id'])


        v5_df = pd.DataFrame(v5_dic)
        v5_df.fillna(0, inplace = True)
        v5_df['v5_flag'] = 1
        
        new_df = v5_df
        new_df.reset_index(drop = True, inplace = True)
        
    elif v5_flag=='1,0':
        v4_ps = json_extract(v4_segment_list)
        for item in v4_ps:
            v4_dic['ps_id'].append(item['id'])
            v4_dic['ps_name'].append(item['name'])
            v4_dic['ps_population'].append(item['population'])
            v4_dic['root_folder'].append(item['rootFolderId'])

        v4_df = pd.DataFrame(v4_dic)
        v4_df.fillna(0, inplace = True)
        v4_df['v5_flag'] = 0

        v5_ps = json_extract(v5_segments_list)
        v5_ps_data = v5_ps['data']
        for item in v5_ps_data:
            v5_dic['root_folder'].append(item['id'])
            v5_dic['ps_name'].append(item['attributes']['name'] + " Root")
            v5_dic['ps_population'].append(item['attributes']['population'])
            v5_dic['ps_id'].append(item['relationships']['parentSegmentFolder']['data']['id'])


        v5_df = pd.DataFrame(v5_dic)
        v5_df.fillna(0, inplace = True)
        v5_df['v5_flag'] = 1
        
        new_df = pd.concat([v4_df, v5_df])
        new_df.reset_index(drop = True, inplace = True)
    else:
        print("provide valid v5_flag")

    return new_df

######## Function to extract Folder Info from V4 and V5 ################
def get_folder_list(ps_df):
    v4_ps = list(ps_df[ps_df.v5_flag == 0].ps_id)
    v5_ps = list(ps_df[ps_df.v5_flag == 1].ps_id)
    
    combined_folders = []

    for master_id in v4_ps:
        try:
            v4_url_folders = f'{segment_api}/audiences/{master_id}/folders'
            v4_json = json_extract(v4_url_folders)

            folders = [{'ps_id': master_id, 'folder_id': item['id'], 'folder_name': item['name']} for item in v4_json]
            combined_folders.extend(folders)
        except:
            print(f"No Audience Segments built V4 for Parent Segment - {master_id}")

    if len(v5_ps) > 0:
        for master_id in v5_ps:
            v5_url_folders = f'{segment_api}/entities/by-folder/{master_id}?depth={folder_depth}'
            v5_json = json_extract(v5_url_folders)['data']

            folders = [{'ps_id': master_id, 'folder_id': item['id'], 'folder_name': item['attributes']['name']} for item in v5_json]
            combined_folders.extend(folders)
            
    return pd.DataFrame(combined_folders)

################## Function to extract Segment Info from V4 and V5 #############
def get_segment_list(ps_df):
    v4_ps = list(ps_df[ps_df.v5_flag == 0].ps_id)
    v5_ps = list(ps_df[ps_df.v5_flag == 1].ps_id)
    
    combined_segments = []

    for master_id in v4_ps:
        v4_url_segments = f'{segment_api}/audiences/{master_id}/segments'
        v4_json = json_extract(v4_url_segments)

        segments = [{'folder_id': item['segmentFolderId'], 'segment_id': item['id'], 'segment_name': item['name'],
                    'segment_population': item['population'], 'realtime': item['realtime'], 'rule': item['rule'],
                    'updatedAt':item['updatedAt'],'numSyndications':item['numSyndications'],'updatedBy_id':item['updatedBy']['id'],'updatedBy_tdid':item['updatedBy']['td_user_id'],'updatedBy_name':item['updatedBy']['name']} for item in v4_json]
        
        combined_segments.extend(segments)

    if len(v5_ps) > 0:
        for master_id in v5_ps:
            v5_url_segments = f'{segment_api}/entities/by-folder/{master_id}?depth=10'
            v5_json = json_extract(v5_url_segments)['data']
            v5_json_user = json_extract(v5_url_segments)['included']
            segment_json = [item for item in v5_json if item['type'].startswith('segment-')]

            segments = [{'folder_id': item['relationships']['parentFolder']['data']['id'], 'segment_id': item['id'], 
'segment_name': item['attributes']['name'],'segment_population': item['attributes']['population'], 
'realtime': item['type'], 'rule': item['attributes']['rule'],'updatedAt':item['attributes']['updatedAt'],
'numSyndications':item['attributes']['numSyndications'],'updatedBy_id':item['relationships']['updatedBy']['data']['id'],
'updatedBy_tdid':[user['attributes']['tdUserId'] for user in v5_json_user if user['id'] == item['relationships']['updatedBy']['data']['id']][0],'updatedBy_name':[user['attributes']['name'] for user in v5_json_user if user['id'] == item['relationships']['updatedBy']['data']['id']][0] } for item in segment_json]
            
            combined_segments.extend(segments)
            
    segment_df = pd.DataFrame(combined_segments)
    segment_df.realtime = [1 if item == True or str(item).startswith('segment-re') else 0 for item in list(segment_df.realtime)]
            
    return segment_df

def _list_all_syndications(final_df):
    filtered_df = final_df[(final_df['numSyndications'] > 0)]
    syndications_df = pd.DataFrame()
    for x, row in filtered_df.iterrows():
        try:
            if row['v5_flag']==0:
                res = requests.get(f"{segment_api}/audiences/{row['ps_id']}/segments/{row['segment_id']}/syndications", headers = headers)
                json_obj = res.json()
                new_syndication=pd.DataFrame(json_obj)
                new_syndication['v5_flag']=0
                syndications_df=pd.concat([syndications_df,new_syndication ])
                
            else:
                res = requests.get(f"{segment_api}/audiences/{row['root_folder']}/segments/{row['segment_id']}/syndications", headers = headers)
                json_obj = res.json()
                new_syndication=pd.DataFrame(json_obj)
                new_syndication['v5_flag']=1
                syndications_df=pd.concat([syndications_df, new_syndication])
                
        except:
            print("ps_id:",row['ps_id'],"segment_id:",row['segment_id'],'root_folder:',row['root_folder'],"v5_flag:",row['v5_flag'],' did not load')
    syndicated_columns_dict = []
    for x, row in syndications_df.iterrows():
        syndicated_columns_dict.extend([{
                        'scheduleType':row['scheduleType'],
                        'scheduleOption':row['scheduleOption'],
                        'timezone':row['timezone'],
                        'name':row['name'], 
                        'updatedAt':row['updatedAt'],
                        'valid':row['valid'],
                      'segmentId': row['segmentId'],
                      'v5_flag': row['v5_flag'],
                      'id': row['id'],
                      'ps_id':row['audienceId'],
                      'updatedBy_tdid': row['updatedBy']['td_user_id'],
                      'updatedBy_name': row['updatedBy']['name'],
            'syndication_last_ran_start':row['executions'][0]['createdAt'] if len(row['executions'])>0 else None,                      
                      'syndication_last_ran':row['executions'][0]['finishedAt'] if len(row['executions'])>0 else None,
                      'syndication_last_status':row['executions'][0]['status'] if len(row['executions'])>0 else None
                  }])
    syndicated_columns = pd.DataFrame(syndicated_columns_dict)
    syndicated_columns=syndicated_columns[['ps_id','segmentId','v5_flag','scheduleType','scheduleOption','timezone','id','name', 'updatedAt','updatedBy_tdid','updatedBy_name','syndication_last_ran_start','syndication_last_ran','syndication_last_status','valid']]
    syndicated_columns
    return(syndicated_columns)


def extract_segment_stats():

    #get Parent Segment DF
    ps_df = get_ps_list()
    ps_df=ps_df[ps_df.ps_name.str.lower().str.contains(ps_to_include)]

    #get Folder Info DF
    folders_df = get_folder_list(ps_df)
    folders_df=folders_df[folders_df.folder_name.str.lower().str.contains(folders_to_include)]
  
    #Merge both DFs on ps_id
    combined_df = pd.merge(ps_df, folders_df, on="ps_id", how = 'left')

    #Get Folder Segments Info
    segments_df = get_segment_list(ps_df)
    segments_df=segments_df[segments_df.segment_name.str.lower().str.contains(segments_to_include)]

    #Merge Segments DF into combined on folder_id
    final_df = pd.merge(combined_df, segments_df, on="folder_id", how = 'left')
    
    #Replace NaN with 0 for numeric columns and drop duplicate columns caused by v4/v5 segment name overlap
    final_df.segment_population.fillna(0, inplace = True)
    final_df.realtime.fillna(0, inplace = True)
    final_df.dropna(subset = ['segment_id'], inplace = True)
    final_df.drop_duplicates(subset=['root_folder', 'folder_id', 'folder_name', 'segment_id', 'segment_name'], keep='first',inplace=True, ignore_index=False)

    segment_rule=[]
    for i , row in final_df.iterrows():
        segment_rule.extend([{
        'segment_rule': "\""+str(row['rule'])+"\"",
        'ps_id':row['ps_id'],
        'ps_name':row['ps_name'],
        'ps_population':row['ps_population'],
        'root_folder':row['root_folder'],
        'v5_flag':row['v5_flag'],
        'folder_id':row['folder_id'],
        'folder_name':row['folder_name'],
        'segment_id':row['segment_id'],
        'segment_name':row['segment_name'],
        'segment_population':row['segment_population'],
        'realtime':row['realtime'],
        'rule':row['rule'],
        'updatedAt':row['updatedAt'],
        'numSyndications':row['numSyndications'],
        'updatedBy_id':row['updatedBy_id'],
        'updatedBy_tdid':row['updatedBy_tdid'],
        'updatedBy_name':row['updatedBy_name']
        
          }])
    final_df = pd.DataFrame(segment_rule)
    rules_list = list(final_df['segment_rule'])
    exclude_flag = [1 if "'exclude': True, 'id':" in item or "'include': False, 'id':" in item else 0 for item in rules_list ]
    include_flag = [1 if "'include': True, 'id':" in item or "'exclude': False, 'id':" in item else 0 for item in rules_list ]
    final_df['exclude_flag'] = exclude_flag
    final_df['include_flag'] = include_flag
    
    nested_segments=[]
    for i , row in final_df.iterrows():
        try:
            value=row['segment_rule']
            regex = re.compile("'id': '(\d+)")
            nested_segments.append(regex.findall(value))
          
        except:
            nested_segments.append([])
    final_df['nested_segments'] = nested_segments
    
    syndications_df= _list_all_syndications(final_df)
    #Write final_df to TD
    client = pytd.Client(apikey=apikey, endpoint=tdserver, database=sink_database)
    client.load_table_from_dataframe(final_df, output_table, writer='bulk_import', if_exists='overwrite')
    client.load_table_from_dataframe(syndications_df, output_table2, writer='bulk_import', if_exists='overwrite')
