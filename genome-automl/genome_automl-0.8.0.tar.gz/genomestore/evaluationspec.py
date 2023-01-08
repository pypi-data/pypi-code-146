import os
import json
import functools
import logging

import inspect
import ast

import warnings
from typing import Mapping, List, Tuple, Dict, Union, Type, Any

from enum import Enum

from .base import BaseRef, CodeRef, DataRef, BaseMetric

from .evaluationstore import EvaluationArtifact, TestArtifact, TaskArtifact
from .evaluationstore import EvaluationStore
from .store import StoreContext

from .evaluationtask import GenomeTask


# art of stealing :)
class GraphNode(object):
    def __init__(self, func_ast, decos, doc):
        self.name = func_ast.name
        self.func_lineno = func_ast.lineno
        self.decorators = decos
        self.doc = doc


class GraphVisitor(ast.NodeVisitor):

    def __init__(self, nodes, flow):
        self.nodes = nodes
        self.flow = flow
        super(GraphVisitor, self).__init__()


    def _is_task(self, decos):
        for dec in decos:
            if getattr(dec, "func", None) and (isinstance(dec.func, ast.Name)
               and dec.func.id in ['task']):
                # function decorated with step
                return True
            elif not getattr(dec, "func", None) and (isinstance(dec, ast.Name)
               and dec.id in ['task']):

                # function decorated with step
                return True


        return False

    def visit_FunctionDef(self, node):
        func = getattr(self.flow, node.name)
        if self._is_task(node.decorator_list):
            self.nodes[node.name] = GraphNode(node, node.decorator_list, func.__doc__)



"""
class representing an evaluation class definition
containing methods annotated with the @task decorator
"""
class EvaluationGraph(object):

    def __init__(self, flow):
        self.name = flow.__name__
        self.nodes = self._create_nodes(flow)

    def _create_nodes(self, flow):
        tree = ast.parse(inspect.getsource(flow)).body
        root = [n for n in tree\
                if isinstance(n, ast.ClassDef) and n.name == self.name][0]
        nodes = {}
        GraphVisitor(nodes, flow).visit(root)
        return nodes


    def __getitem__(self, x):
        return self.nodes[x]

    def __contains__(self, x):
        return x in self.nodes

    def __iter__(self):
        return iter(self.nodes.values())




class GenomeEvaluationRun():
    def __init__(self, store:EvaluationStore, validationTarget:Dict[str, str] = None):
        self.store = store if store else EvaluationStore(StoreContext())
        self._graph = EvaluationGraph(self.__class__)

        self.tasks = []
        self.validationTarget = {"ref": validationTarget, "refType": "model"} if validationTarget else None


    def add_task(self, task: GenomeTask):
        self.tasks.append(task)



    def to_run(self):
        #execute all tasks
        for t in self._graph:
            task_to_run = getattr(self, t.name)
            #empty args will be prefilled by decorators at runtime
            task_to_run(None, None)


        code:CodeRef = None
        if self.code and "ref" in self.code:
            code = CodeRef(self.code["ref"], self.code["refType"] if "refType" in self.code else "docker")
            if "version" in self.code:
                code.version = self.code["version"]


        targetModel:BaseRef = None
        if self.validationTarget and "ref" in self.validationTarget:
            targetModel = BaseRef(self.validationTarget["ref"], self.validationTarget["refType"])


        status:int = 1
        dsets:List = []
        metrics:List = []
        tasks:List = []
        for t in self.tasks:
            task_run = t.get_task()
            status = task_run.status if task_run.status < status else status

            # add dataset if not already included in evaluation datasets
            if t.dataset not in dsets:
                dsets.append(t.dataset)

            # add tasks
            tasks.append(task_run)

            # now add metrics
            for m in t.metrics:
                metrics.append(BaseMetric(m, t.metrics[m]))


        runCls = EvaluationArtifact
        if isinstance(evaluation, GenomeTestRun):
            runCls = TestArtifact

        run = runCls(

          canonicalName = self.canonicalName,
          application = self.application,
          target = self.target,

          versionName = self.versionName,
          specVersionName = self.specVersionName,
          inputModality = self.inputModality,
          framework = self.framework,
          dimension = self.dimension,
          status = status,

          code = code,
          parameters = self.parameters,
          dataRefs = dsets,
          tasks = tasks,

          pipelineName = self.pipelineName or "pipeline-a",
          pipelineStage = self.pipelineStage or "stage-a",
          pipelineRunId = self.pipelineRunId or "run-a",
          validationTarget = targetModel,
          validationMetrics = metrics
        )


        logging.info(run.to_json())
        self.store.save(run)

        #add tasks from run
        return run



class GenomeTestRun(GenomeEvaluationRun):
    def __init__(self, store: EvaluationStore, validationTarget: Dict[str, str] = None):
        super().__init__(store, validationTarget = validationTarget)



class EvaluationDimension(Enum):
    PERFORMANCE = "PERFORMANCE"
    ROBOUSTNESS = "ROBOUSTNESS"
    SECURITY = "SECURITY"
    COST = "COST"
    PRIVACY = "PRIVACY"
    ETHICS = "ETHICS"




def task(name="", dataset=None, segment=None):
    """
    decorator for test or evaluation tasks
    transform steps are always performed on isolated container/compute
    name: task name
    dataset: dataset definition to load
    """
    def deco_task(func):
        @functools.wraps(func)
        def wrapper_task(*args, **kwargs):

            func_name = func.__name__
            task_name = name if name else func_name
            logging.info(f"calling task: {task_name}")

            obj = args[0]
            data = None
            if dataset and "ref" in dataset:
                data = DataRef(dataset["ref"], "mllake")

            task = GenomeTask(name=task_name, dataset=data, segment=segment)

            result = func(obj, task, data, **kwargs)


            obj.add_task(task)
            for t in task.prototypes:
                obj.add_task(t)


            logging.info(f"completed task: {task_name}")



        return wrapper_task
    return deco_task



def evaluation(
  name:str = "",
  parameters:dict = None,
  targetModel:str = None,
  application:str = None,
  target:str = None,
  versionName:str = None,
  specVersionName:str = None,
  code:str = None,
  pipelineName:str = None,
  pipelineStage:str = None,
  pipelineRunId:str = None,
  inputModality:str = None,
  framework:str = None,
  dimension:EvaluationDimension = None):

    def f(cls):
        cls.canonicalName = name
        cls.parameters = parameters
        cls.validationTarget = {"ref": targetModel, "refType": "model"} if targetModel else None

        cls.application = application or os.getenv('APPLICATION')
        cls.target = target
        cls.versionName = versionName or os.getenv('versionName')
        cls.specVersionName = versionName or os.getenv('specVersionName')


        if code:
            cls.code = {"ref":code, "refType":"docker"}
        else:
            cls.code = os.getenv('CODE')

        cls.pipelineName = pipelineName or os.getenv('PIPELINE_NAME')
        cls.pipelineStage = pipelineStage or os.getenv('STEP_NAME')
        cls.pipelineRunId = pipelineRunId or os.getenv('PIPELINE_RUNID')

        cls.inputModality = inputModality or os.getenv('inputModality')
        cls.framework = framework or os.getenv('framework')
        cls.dimension = str(dimension.value) if dimension else os.getenv('dimension')



        return cls

    return f
