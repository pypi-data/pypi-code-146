"""Implements an interface for backtesting."""
import datetime
import json
import os

import bson
from IPython.display import display, clear_output
from ipywidgets import FloatProgress
from pymongo import MongoClient

from ia.gaius.data_ops import Data
from ia.gaius.tests import classification, utility

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json 
from math import pi, cos, sin 
import pandas as pd 
from sklearn.metrics import accuracy_score, precision_score
import collections 

class BackTest:
    """Provides an interface for backtesting."""
    def __init__(self, **kwargs):
        """
        Pass this a configuration dictionary as the argument such as:

        test_results_database = 'mongodb://mongo-kb:27017'

        test_config = {'name':'backtest-classification',
                        'test_type': 'classification', ## 'classification' or 'utility'
                        'utype': None, ## If 'test_type' = 'utility', then set to either 'polarity' or 'value'
                        'shuffle_data': True,
                        'fresh_start_memory': True, ## Clear all memory when starting and between runs
                        'mongo_location': test_results_database, ## location of mongo db where test results will be stored
                        'learning_strategy': 'continuous', # None, 'continuous' or 'on_error'
                        'bottle': bottle,
                        'data_source': dataset, ## or provide 'data_directories' as iterable of data.
                        'percent_reserved_for_training': 20,
                        'percent_of_dataset_chosen': 100,
                        'total_test_counts': 1 }

        test = BackTest(**test_config)

        mongo_location provides the location of a mongo database where the test results will be stored.

        Option of either data_source or data_directories can be provided:

            data_source provided is a sequence of sequences of GDF objects.
            data_directories provided should be a list of directories containing files of GDF as json dumps.

        """
        self.configuration = kwargs
        self.errors = []
        self.name = str(kwargs['name'])
        self.test_type = kwargs['test_type']
        self.utype = kwargs['utype']
        self.shuffle_data = kwargs['shuffle_data']
        self.learning_strategy = kwargs['learning_strategy']
        self.fresh_start_memory = kwargs['fresh_start_memory']
        self.mongo_location = kwargs['mongo_location']
        self.bottle = kwargs['bottle']
        self.bottle.summarize_for_single_node = False
        if 'data_directories' in self.configuration:
            self.data_directories = kwargs['data_directories']
            self.data_source = None
        elif 'data_source' in self.configuration:
            self.data_source = kwargs['data_source']
            self.configuration['data_source'] = 'from-source'
            self.data_directories = None
        self.percent_reserved_for_training = int(kwargs['percent_reserved_for_training'])
        self.percent_of_dataset_chosen = int(kwargs['percent_of_dataset_chosen'])
        self.total_test_counts = int(kwargs['total_test_counts'])
        self.current_test_count = 0

        self.mongo_client = MongoClient(self.mongo_location)  # , document_class=OrderedDict)
        # Collection storing the backtesting results is the bottle's name.
        self.mongo_client.backtesting = self.mongo_client['{}-{}-{}'.format(
            self.name, self.bottle.genome.agent, self.bottle.name)]
        self.test_configuration = self.mongo_client.backtesting.test_configuration
        self.test_status = self.mongo_client.backtesting.test_status
        self.test_errors = self.mongo_client.backtesting.test_errors
        self.backtesting_log = self.mongo_client.backtesting.backtesting_log
        self.interrupt_status = self.mongo_client.backtesting.interrupt_status

        if self.test_type == "utility":
            self._tester = utility.Tester(**kwargs)
        elif self.test_type == 'classification':
            self._tester = classification.Tester(**kwargs)

        if self.data_directories:
            self.data = Data(data_directories=self.data_directories)
        elif self.data_source:
            self.data = Data(dataset=self.data_source)
        self.data.prep(self.percent_of_dataset_chosen, self.percent_reserved_for_training, shuffle=self.shuffle_data)
        sequence_count = len(self.data.train_sequences) + len(self.data.test_sequences)

        self.number_of_things_to_do = self.total_test_counts * sequence_count
        self.number_of_things_done = 0
        self.status = "not started"

        self.interrupt_status.replace_one({}, {'interrupt': False}, upsert=True)
        self.test_status.replace_one({}, {'status': 'not started',
                                          'number_of_things_to_do': self.total_test_counts * sequence_count,
                                          'number_of_things_done': 0,
                                          'current_test_count': self.current_test_count
                                          }, upsert=True)

        self.test_errors.drop()
        self.backtesting_log.drop()
        self.backtesting_log.insert_one({"timestamp_utc": datetime.datetime.utcnow(), "status": "test-started"})

        self.test_configuration.drop()
        self.test_configuration.insert_one({
            'name': self.name,
            'test_type': self.test_type,
            'utype': self.utype,
            'shuffle_data': self.shuffle_data,
            'learning_strategy': self.learning_strategy,
            'fresh_start_memory': self.fresh_start_memory,
            "bottle_name": self.bottle.name,
            "agent": self.bottle.genome.agent,
            "ingress_nodes": self.bottle.ingress_nodes,
            "query_nodes": self.bottle.query_nodes
        })

        headers = ["Test Run", "Trial", "Phase", "Filename", "Historical"] + [node["name"] for node in
                                                                              self.bottle.query_nodes] + ["hive"]
        self.backtesting_log.insert_one({"headers": headers})
        self.progress = FloatProgress(min=0, max=self.number_of_things_to_do, description="Starting...", bar_style="info")

        print("Recording results at '%s-%s-%s'" % (self.name, self.bottle.genome.agent, self.bottle.name))

    def _reset_test(self):
        """Reset the instance to the state it was in when created."""
        self.backtesting_log.insert_one({"timestamp_utc": datetime.datetime.utcnow(), "status": "resetTest"})
        if self.data_directories:
            self.data = Data(data_directories=self.data_directories)
        elif self.data_source:
            self.data = Data(dataset=self.data_source)
        self.data.prep(self.percent_of_dataset_chosen, self.percent_reserved_for_training, shuffle=self.shuffle_data)
        self._tester.next_test_prep()

    def _end_test(self):
        """Called when the test ends."""
        self.status = "finished"
        self.backtesting_log.insert_one({"timestamp_utc": datetime.datetime.utcnow(), "status": "test-ended"})
        nodes_status = self.bottle.show_status()
        self.test_status.replace_one({}, {'status': 'finished',
                                          'nodes_status': nodes_status,
                                          'number_of_things_to_do': self.number_of_things_to_do,
                                          'number_of_things_done': self.number_of_things_to_do,
                                          'current_test_count': self.current_test_count}, upsert=True)

    def run(self):
        display(self.progress)
        self.backtesting_log.insert_one({"timestamp_utc": datetime.datetime.utcnow(), "status": "run"})
        while self.current_test_count < self.total_test_counts:
            self.current_test_count += 1
            self._setup_training()
            for sequence in self.data.train_sequences:
                self._train(sequence)
                self.number_of_things_done += 1
                self.progress.value = self.number_of_things_done
                self.progress.description = '%0.2f%%' % (100 * self.number_of_things_done / self.number_of_things_to_do)

            self._setup_testing()
            for sequence in self.data.test_sequences:
                self._test(sequence)
                self.number_of_things_done += 1
                self.progress.value = self.number_of_things_done
                self.progress.description = '%0.2f%%' % (100 * self.number_of_things_done / self.number_of_things_to_do)

            if self.current_test_count < self.total_test_counts:
                self._reset_test()
            else:
                self._end_test()
                clear_output()

    def _setup_training(self):
        """Setup instance for training."""
        self.backtesting_log.insert_one({"timestamp_utc": datetime.datetime.utcnow(), "status": "setupTraining"})
        self.status = "training"
        self.test_status.replace_one({}, {'status': 'training',
                                          'number_of_things_to_do': self.number_of_things_to_do,
                                          'number_of_things_done': self.number_of_things_done,
                                          'current_test_count': self.current_test_count}, upsert=True)
        if self.fresh_start_memory:
            self.bottle.clear_all_memory()
        return 'ready'

    def _train(self, sequence):
        """Train with the sequence in *sequence*."""
        # get a sequence either from a file, or directly as a list:
        if self.data_directories:
            self.backtesting_log.insert_one(
                {"timestamp_utc": datetime.datetime.utcnow(), "status": "training", "file": os.path.basename(sequence)})
            with open(sequence) as f:
                sequence = [json.loads(data.strip()) for data in f if data]
        elif self.data_source:
            sequence = sequence
            self.backtesting_log.insert_one({"timestamp_utc": datetime.datetime.utcnow(), "status": "training"})

        ## Train the sequence:
        result_log_record = self._tester.train(sequence)
        result_log_record['trial'] = self.number_of_things_done
        result_log_record['run'] = self.current_test_count
        self.backtesting_log.insert_one(result_log_record)
        return 'ready'

    def _setup_testing(self):
        """Set up the instance to begin backtesting."""
        self.backtesting_log.insert_one({"timestamp_utc": datetime.datetime.utcnow(), "status": "setupTesting"})
        self.status = "testing"
        self.test_status.replace_one({}, {'status': 'testing',
                                          'number_of_things_to_do': self.number_of_things_to_do,
                                          'number_of_things_done': self.number_of_things_done,
                                          'current_test_count': self.current_test_count}, upsert=True)
        return 'ready'

    def _test(self, sequence):
        """Run the backtest on *sequence*."""
        ## get a sequence either from a file, or directly as a list:
        if self.data_directories:
            self.backtesting_log.insert_one(
                {"timestamp_utc": datetime.datetime.utcnow(), "status": "testing", "file": os.path.basename(sequence)})
            with open(sequence) as f:
                sequence = [json.loads(data.strip()) for data in f if data]
        elif self.data_source:
            sequence = sequence
            self.backtesting_log.insert_one({"timestamp_utc": datetime.datetime.utcnow(), "status": "testing"})

        ## Test the sequence and record the results.
        result_log_record = self._tester.test(sequence)
        result_log_record['trial'] = self.number_of_things_done
        result_log_record['run'] = self.current_test_count
        self.backtesting_log.insert_one(bson.son.SON(result_log_record))
        return 'ready'


def classification_report(back_tester : BackTest): 
    class_values = get_class_distribution(back_tester)

    plot_class_distributions(back_tester, class_values)

    predictor_operator_characteristic(back_tester, class_values)

    fidelity_charts(back_tester)

def get_class_distribution(back_tester : BackTest) -> dict: 
    return_dict = {"training" : {}, "testing" : {}} 
    training_class_labels = [] 
    testing_class_labels = [] 
    if back_tester.data_directories != None: 
        for file in back_tester.data.train_sequences: 
            with open(file) as f: 
                sequence = [json.loads(data.strip()) for data in f if data] 
                if(sequence[-1]["strings"][-1] != ""): 
                    training_class_labels.append(sequence[-1]["strings"][-1])

        for key in set(training_class_labels):
            return_dict["training"][key] = training_class_labels.count(key)


        for file in back_tester.data.test_sequences:
            with open(file) as f:
                sequence = [json.loads(data.strip()) for data in f if data]
                if(sequence[-1]["strings"][-1] != ""):
                    testing_class_labels.append(sequence[-1]["strings"][-1])

        for key in set(testing_class_labels):
            return_dict["testing"][key] = testing_class_labels.count(key)

    else:
        for seq in back_tester.train_sequences:
            if(sequence[-1]["strings"][-1] != ""):
                training_class_labels.append(sequence[-1]["strings"][-1])

        for key in set(training_class_labels):
            return_dict["training"][key] = training_class_labels.count(key)

        for seq in back_tester.test_sequences:
            if(sequence[-1]["strings"][-1] != ""):
                testing_class_labels.append(sequence[-1]["strings"][-1])

        for key in set(testing_class_labels):
            return_dict["testing"][key] = testing_class_labels.count(key)

    return return_dict

def plot_class_distributions(back_tester : BackTest, class_values): 
    # make subplot figure 
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

    # get training data distribution
    x = class_values["training"]
    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'class'})

    # add first pie subplot
    fig.add_trace(
        go.Pie(labels=data["class"].to_list(), values=data["value"].to_list(), name="Training", 
               title='Training', texttemplate = "%{label}<br>(%{percent:.2f})"),
        1, 1)

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    # get testing data distribution
    x = class_values["testing"]
    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'class'})

    # add other pie subplot
    fig.add_trace(
        go.Pie(labels=data["class"].to_list(), values=data["value"].to_list(), 
               name="Testing", title='Testing', texttemplate = "%{label}<br>(%{percent:.2f})"),
        1, 2,)

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(height=500, width=800, title_text="Historical Class Distributions")
    fig.show()

def predictor_operator_characteristic(back_tester : BackTest, class_values): 
    # create some variables to hold data 
    predicted_labels = [] 
    true_labels = [] 
    num_correct = 0 
    num_wrong = 0

    # go through results and record number of correct and incorrect
    for doc in back_tester.backtesting_log.find({"phase" : "testing"}):
        predicted_labels.append(doc['node_predictions']["hive"])
        true_labels.append(doc['historical_expecting'])
        if(doc['historical_expecting'] == doc['node_predictions']["hive"]):
            num_correct += 1
        else:
            num_wrong += 1

    # calculate scores
    accuracy_of_positives = accuracy_score(predicted_labels, true_labels)

    precision_of_positives = num_correct / (num_wrong + num_correct)


    line_color=dict(color="green")

    layout1= go.Layout(title=go.layout.Title(text="Predictor Operator Characteristic",x=0.5),
        xaxis={'title':'Precision of Positives (Positive Predictive Values)','range':[0,1.0]},
        yaxis={'title':'Accuracy of Positives','range':[0,1.0]})

    point_plot=[
      go.Scatter(x=[(1 / len(class_values["testing"].keys())) for i in range(2)],
             y=[i for i in range(2)],
             name="Random Chance",
             legendgroup="Random Chance",
             line=line_color),
        go.Scatter(x = [accuracy_of_positives], y = [precision_of_positives], 
                   name = "GAIUS Performance", legendgroup="GAIUS Performance",
                  marker={"color":"green", "size":25}, mode="markers")
    ]

    go.Figure(data=point_plot, layout=layout1).show()

def fidelity_charts(back_tester : BackTest):
    import collections
    calculated_things = {}
    # get the names of all the nodes, and add hive
    # will probably need to filter some out or not
    nodes = [name["name"] for name in back_tester.bottle.all_nodes]
    nodes.insert(0, "hive")
#     nodes.append("hive")
    
    # set up dictionary, before reading info from backtesting_log
    for node in nodes:
        calculated_things[node] = {}
        calculated_things[node]["node_predictions"] = []
        calculated_things[node]["num_correct"] = 0
        calculated_things[node]["num_wrong"] = 0
        for actual in back_tester.backtesting_log.distinct('historical_expecting'):
            calculated_things[node][actual] = {}
            for predicted in back_tester.backtesting_log.distinct('historical_expecting'):
                calculated_things[node][actual][predicted] = 0
    
    # get information from backesting_log
    for doc in back_tester.backtesting_log.find({"phase" : "testing"}):
        for node in nodes:
            calculated_things[node][doc['historical_expecting']][doc['node_predictions'][node]] += 1
            calculated_things[node]["node_predictions"].append(doc['node_predictions'][node])
            if(doc['historical_expecting'] == doc['node_predictions'][node]):
                calculated_things[node]["num_correct"] += 1
            else:
                calculated_things[node]["num_wrong"] += 1
    
    # get status of bottles
    bottle_statuses = back_tester.bottle.show_status()
    
    # set up suplots
    subplot_spec = []
    subplot_titles = []
    width = 1000
    height = 400 * (len(nodes)+1)
    
    for node in nodes:
        subplot_spec.append([{"type": "table"},
                   {"type": "domain"},
                   {"type": "domain"}])
        
        subplot_titles.append(node.capitalize())
        subplot_titles.append('Fidelity')
        subplot_titles.append("Predicted Class Distributions")
        
    
    subplot_spec.append([{"type": "table", "colspan": 3}, None, None])
    subplot_titles.append("Confusion Matrix")
    
    fig = make_subplots(rows=len(nodes)+1, cols=3,
            specs=subplot_spec,
            subplot_titles=subplot_titles,
            column_widths=[width / 3, width /3, width / 3])
    
    # go through nodes and plot their data
    row_index = 1
    for i, node in enumerate(nodes):
        # make small table with node status
        if(node == "hive"):
            fig.add_trace(go.Table(
                header=dict(values=[node.capitalize() + " Status"],
                    align='left'),
                cells=dict(values=[[""]],
                   align='left')), row_index, 1)
        else:
            fig.add_trace(go.Table(
                header=dict(values=[node],
                    align='left'),
                cells=dict(values=[[str(bottle_statuses[node])]],
                   align='left')), row_index, 1,)
            
        # pie chart for Fidelity
        data = {}
        data["values"] = [calculated_things[node]["num_correct"], calculated_things[node]["num_wrong"]]
        data["angle"] = [val / sum(data["values"]) * 2*pi for val in data["values"]]
        data['percentage'] = [val / sum(data["values"]) * 100 for val in data["values"]]
        data['percentage'] = ['{0:.2f}%'.format(val) for val in data['percentage']]
        data["class"] = ["num_correct", "num_wrong"]
        data['color'] = ["green", "red"]
        
        fig.add_trace(
        go.Pie(labels=data["class"], values=data["values"]), row_index, 2,)
    
#         fig.update_traces(hole=.4, hoverinfo="label+percent+name", selector=dict(type="domain"))

        # pie chart for class distribution
        data = {}
        freqs = dict(collections.Counter(calculated_things[node]["node_predictions"]))
        data["values"] = [val for val in freqs.values()]
        data["class"] = [val for val in freqs.keys()]
        data["angle"] = [val / sum(data["values"]) * 2*pi for val in data["values"]]
        data['percentage'] = [val / sum(data["values"]) * 100 for val in data["values"]]
        data['percentage'] = ['{0:.2f}%'.format(val) for val in data['percentage']]
        
        fig.add_trace(
        go.Pie(labels=data["class"], values=data["values"]), row_index, 3,)
        
        fig.update_traces(hole=.4, hoverinfo="label+percent+name", selector=dict(type="pie"))
        row_index += 1
        
    # make confusion matrix
    classes = data["class"]
    
    data["actual"] = [[val] * 3 for val in classes]
    data["actual"] = [item for sublist in data["actual"] for item in sublist]
    data["predicted"] = [classes] * 3
    data["predicted"] = [item for sublist in data["predicted"] for item in sublist]
        
    # go through all combinations of classes for hive since it would be the final prediction
    # ****can be modified so that each node gets their own confusion matrix****
    data["frequency"] = [calculated_things["hive"][actual][predicted] 
                       for actual, predicted in zip(data["actual"], data["predicted"])]
    data["% of results"] = [calculated_things["hive"][actual][predicted] / 
                       (calculated_things["hive"]["num_correct"] + 
                        calculated_things["hive"]["num_wrong"]) * 100 
                        for actual, predicted in zip(data["actual"], data["predicted"])]
    
    data["% of results"] = ['{0:.2f}%'.format(val) for val in data["% of results"]]
        
    fig.add_trace(go.Table(
            header=dict(values=["Actual", "Predicted", "Frequency", "% of results"],
                align='left'),
            cells=dict(values=[data["actual"], data["predicted"], data["frequency"], data["% of results"]],
                align='left'), ), row_index, 1)
    
    fig.update_layout(height=height, width=width, title_text="Classification Report")
    fig.update_traces(
        cells_font=dict(size = 15),
        selector=dict(type="table"))
    fig.show()