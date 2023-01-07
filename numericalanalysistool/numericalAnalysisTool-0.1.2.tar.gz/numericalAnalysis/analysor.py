import os
from itertools import product

import pandas as pd
import seaborn as sns



class Analysor:

    fct_name = "fct"
    BUILDER_DIR = "graph"
    def __init__(self,functions_dictionary=None,target_name="target"):
        self._param_names = None
        if functions_dictionary is None:
            self._functions = {}
        else:
            self._functions = functions_dictionary
        self._result = { fct : None for fct in self._functions.keys()}
        self._target_name = target_name
        self._dataframe = None
        self.set_param_names()

    def set_param_names(self):
        self._param_names = [param for param_d in self._functions.values() for param in param_d.keys()]

    def add_function(self, function, parameters_range: dict):
        self._functions[function] = parameters_range
        if not self._param_names:
            self.set_param_names()
    def _param_product(self,d):
            return (dict(zip(d.keys(), values)) for values in product(*d.values()))
    def compute(self):

        for fct,parameters_range in self._functions.items():
            contents = []
            for d in self._param_product(parameters_range):
                res = fct(**d)
                line = {**d,Analysor.fct_name:fct.__name__,self._target_name: res}
                contents.append(line)
            self._result[fct] = pd.DataFrame(contents)
        self._dataframe = pd.concat([df for df in self._result.values()])

    def draw_linear_2D_graph(self):
        if not os.path.exists(Analysor.BUILDER_DIR):
            os.makedirs(Analysor.BUILDER_DIR)
        for param_name in self._param_names:
            g = sns.FacetGrid(self._dataframe, col=Analysor.fct_name)
            g.map_dataframe(sns.lineplot, x=param_name,y=self._target_name)
            g.add_legend()
            file_name = f"{Analysor.BUILDER_DIR}/{'_'.join([fct.__name__ for fct in self._functions.keys()])}_{param_name}.png"
            g.savefig(file_name)