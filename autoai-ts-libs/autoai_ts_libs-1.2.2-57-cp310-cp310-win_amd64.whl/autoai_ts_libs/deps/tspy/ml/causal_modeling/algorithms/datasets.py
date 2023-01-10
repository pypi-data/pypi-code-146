#  /************** Begin Copyright - Do not add comments here **************
#   * Licensed Materials - Property of IBM
#   *
#   *   OCO Source Materials
#   *
#   *   (C) Copyright IBM Corp. 2020, All Rights Reserved
#   *
#   * The source code for this program is not published or other-
#   * wise divested of its trade secrets, irrespective of what has
#   * been deposited with the U.S. Copyright Office.
#   ***************************** End Copyright ****************************/

'''
Dataset providers for SRU algorithm 
'''

# standard
import os
import json
import datetime

# third party
import pandas as pd
import numpy as np
import torch



class SockShopDataset(object):
       
    def __init__(self, root_dir):
        
        # load full train datasets into a dictionary of dataframes
        train_fpath_list = []
        train_top_dir = os.path.join(root_dir, 'training_cv')
        for folder in os.listdir(train_top_dir):
            if '.DS_Store' not in folder: # mac specific
                fpath = os.path.join(train_top_dir, folder, 'logs.json')
                train_fpath_list.append(fpath)
        
        train_df_dict = {}
        services      = []
        for fpath in train_fpath_list:
            service = os.path.split(os.path.split(fpath)[0])[1]
            logs = []
            for line in open(fpath, 'r'):
                logs.append(json.loads(line))
            df = pd.DataFrame.from_records(logs)
            train_df_dict[service] = df
            services.append(service)
            
        # list of train dataset fpaths, list of services (i.e. their unsorted names)
        # and loaded dictionary of train dataframes
        self.train_fpath_list = train_fpath_list
        self.services         = services
        self.train_df_dict    = train_df_dict

        # test dataset_fpath
        self.test_fpath = os.path.join(root_dir, 'test', 'sockshop-combined-windowed-logs.json')
        
        # error dataset fpath
        self.error_fpath = os.path.join(root_dir, 'test', 'sock_shop_abnormal_error_logs.csv')

        # to be updated later when a train dataset has been chosen 
        self.num_features          = None
        self.nodename_feature_list = None
        self.nodename_list         = None
        self.feature_list          = None

        # to be updated later when train, test, error dataframes are created
        self.train_df = None
        self.test_df  = None
        self.error_df = None

        
    def create_error_dataframe(self):

        error_df = pd.read_csv(self.error_fpath)
        error_df = error_df.sort_values(by=['_ts'])
        
        error_ts_array  = np.array(error_df['_ts'])
        error_date_array  = np.array([str(x) for x in pd.to_datetime([y / 1000.0 for y in error_ts_array], unit='s')])
        error_app_array = np.array(error_df['_app'])
        
        self.error_df = error_df.copy(deep=True)
        return error_df
            
        
    def create_test_dataframe(self):
        
        logs = []
        for line in open(self.test_fpath, 'r'):
            logs.append(json.loads(line))
        test_df = pd.DataFrame.from_records(logs)
        
        test_df = test_df.sort_values(by=['timestamp'])
        test_df = test_df[['timestamp', 'instance_id', 'embeddings']]

        # discard the service not appearing in train data 
        extra_service = 'rabbitmq'
        test_df = test_df.loc[test_df['instance_id'] != extra_service]

        self.test_df = test_df.copy(deep=True)
        return test_df
            

    def create_train_dataframe(self, start_date, end_date):

        if type(start_date) == tuple:
            year, month, day, hour, minute = start_date
            d_start = datetime.date(year, month, day)
            t_start = datetime.time(hour, minute)
            start_date = datetime.datetime.combine(d_start, t_start)
        if type(end_date) == tuple:
            year, month, day, hour, minute = end_date
            d_end = datetime.date(year, month, day)
            t_end = datetime.time(hour, minute)
            end_date = datetime.datetime.combine(d_end, t_end)

        # number of features
        num_features = len(self.train_df_dict[self.services[0]]['embeddings'][0])
    
        # filter data to train on
        frames = []

        for service in self.services:
            df = self.train_df_dict[service].copy(deep=True)
            df['date'] = pd.to_datetime(df['timestamp'] / 1000., unit='s')

            mask = (df['date'] > start_date) & (df['date'] <= end_date)
            df   = df.loc[mask]
            frames.append(df)
        df = pd.concat(frames)
        df = df.sort_values(by=['timestamp'])

        # organize duplicates in groups
        grouped = df.groupby('timestamp')
        group_dict = grouped[['app', 'embeddings']].apply(
            lambda group: group.values.tolist()).to_dict()

        keys = list(group_dict.keys())
        num_events = len(keys)
        sorted_services = sorted(self.services)

        # initialize the data dictionary
        data_dict = {'timestamp' : [0 for i in range(num_events)]}

        node_name_list     = sorted_services
        feature_name_list  = ['feature-{}'.format(i+1) for i in range(num_features)]

        for node_name in node_name_list:
            for feature_name in feature_name_list:
                column_name = '{}_{}'.format(node_name, feature_name)
                data_dict[column_name] = [0.0 for i in range(num_events)]
        
        # fill-up the data dictionary
        for counter, (key, value) in enumerate(group_dict.items()):
            timestamp = str(key)
            data_dict['timestamp'][counter] = timestamp
            for v in value:
                node_name      = v[0]
                feature_vector = v[1]
                for i, feature_name in enumerate(feature_name_list):
                    column_name = '{}_{}'.format(node_name, feature_name)
                    data_dict[column_name][counter] = feature_vector[i]
    
        # convert to the dataframe
        train_df = pd.DataFrame(data_dict)

        nodename_feature_list = train_df.columns[1:].tolist()
        nodename_list         = sorted(list(set([x.split('_')[0] for x in nodename_feature_list])))
        feature_list          = [x.split('_')[1] for x in  nodename_feature_list[:num_features]]

        # set some attributes to the dataset object
        self.num_features          = num_features
        self.nodename_feature_list = nodename_feature_list
        self.nodename_list         = nodename_list
        self.feature_list          = feature_list

        self.train_df = train_df.copy(deep=True)
        return train_df


    def generate_test_data(self):

        try:
            test_df = self.test_df
        except:
            print('Run create_test_dataframe() first...') 
            return None
        
        # organize duplicates in groups
        test_grouped = test_df.groupby('timestamp')
        test_group_dict = test_grouped[['instance_id', 'embeddings']].apply(
            lambda group: group.values.tolist()).to_dict()

        test_keys = list(test_group_dict.keys())
        test_num_events = len(test_keys)

        # initialize the data dictionary
        test_data_dict = {'timestamp' : [0 for i in range(test_num_events)]}
        concurrent_lists = []
        timestamp_list   = []
        num_features = 20
        
        node_name_list     = self.nodename_list
        feature_name_list  = ['feature-{}'.format(i+1) for i in range(num_features)]

        for node_name in node_name_list:
            for feature_name in feature_name_list:
                column_name = '{}_{}'.format(node_name, feature_name)
                test_data_dict[column_name] = [0.0 for i in range(test_num_events)]
        
        # fill-up the data dictionary
        for counter, (key, value) in enumerate(test_group_dict.items()):
            timestamp = str(key)
            timestamp_list.append(timestamp)
            test_data_dict['timestamp'][counter] = timestamp
            concurrent_list = []
            for v in value:
                node_name      = v[0]
                concurrent_list.append(node_name)
                feature_vector = v[1]
                for i, feature_name in enumerate(feature_name_list):
                    column_name = '{}_{}'.format(node_name, feature_name)
                    test_data_dict[column_name][counter] = feature_vector[i]
            concurrent_lists.append(concurrent_list)

        test_data_df = pd.DataFrame(test_data_dict)
        test_data_np = np.transpose(test_data_df.to_numpy()[:, 1:])
        test_data_np = np.array(test_data_np, dtype=np.float32)

        test_data = torch.from_numpy(test_data_np)
        test_data = test_data.float()

        return test_data, concurrent_lists, timestamp_list

    
    def generate_train_data(self):
        try:
            train_df = self.train_df
        except:
            print('Run create_train_dataframe() first...') 
            return None

        train_data_np = np.transpose(train_df.to_numpy()[:, 1:])
        train_data_np = np.array(train_data_np, dtype=np.float32)
        train_data    = torch.from_numpy(train_data_np)
        train_data    = train_data.float()

        return train_data

    
    def compute_gt_graph(self):
        '''
        returns ground truth causal graph for sockshop dataset 
        in the form of a binary numpy matrix
        '''
        
        edges = [('front-end', 'orders'),
                 ('front-end', 'payment'),
                 ('front-end', 'user'),
                 ('front-end', 'catalogue'),
                 ('front-end', 'carts'),
                 ('orders', 'orders-db'),
                 ('orders', 'shipping'),
                 ('user', 'user-db'),
                 ('carts', 'carts-db'),
                 ('shipping', 'queue-master')]
        
        if (self.nodename_list is None):
            print('Run create_train_dataframe() first...') 
            return None
        
        n_nodes    = len(self.nodename_list)
        gt_graph   = np.zeros((n_nodes, n_nodes))
        
        for (a, b) in edges:
            gt_graph[self.nodename_list.index(a), self.nodename_list.index(b)] = 1
        
        return gt_graph
        
