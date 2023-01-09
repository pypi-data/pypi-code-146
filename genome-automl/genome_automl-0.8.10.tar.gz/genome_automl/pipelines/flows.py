import functools
import inspect

import logging
import json
import os
import os.path
import subprocess

import sys
import urllib.request
from urllib.error import  URLError


from .flow_parser import FlowGraph

from typing import Mapping, List, Tuple, Dict, Any

from .step_input import StepInput
from .input_converter import ExpressionEvaluatorFactory


"""
This class represents the associated local **flow execution engine** to the compiler
defined in flow_parser.FlowGraph. It can execute in local mode in isolation, to test flows locally.
In addition it can execute remote transform steps as part of container execution (AWS, Google),
and can publish the results of the step correctly to subsequent remote steps involved in the cloud workflow.
Python class definitions representing a flow, should inherit from this class:

class MyFlow(BaseGraph):
    def start(input):
        ....
"""
class BaseGraph():

    def __init__(self, input=None):

        # set input of the graph
        self.graphInput = input
        # if not explicit input provided use deployment_parameters env variable
        if not input and os.getenv('DEPLOYMENT_PARAMETERS'):
            # deployment params should be a json string
            self.graphInput = json.loads(os.getenv('DEPLOYMENT_PARAMETERS'))



        self._steps = []
        self._results = {}

        self._graph = FlowGraph(self.__class__)

        #json representation
        self._graph_steps = []
        self._graph_steps_map = {}

        # init data representation of graph
        for node in self._graph:
            json_node = {
              "name": node.name,
              "type": node.type,
              "next": node.out_funcs,
              "matching_join": node.matching_join or None,
              "args": node.out_args,
              "step_flow_class": node.step_target_step_type,
              "step_input_type": node.step_input_type,
              "step_output_type": node.step_output_type,
              "step_has_expression_input": True if node.step_expression_input else False,
              "step_has_resources": True if node.step_has_resources else False,
              "step_image": node.step_image,
              "step_retry": node.step_retry,
              "condition": node.condition or None,
              "foreach": node.foreach_param or None,
              "split_parents": node.split_parents
            }

            self._graph_steps.append(json_node)
            self._graph_steps_map[node.name] = json_node



        # start function to start graph execution from
        # relevant for running isolated steps in container in LOCAL mode
        self.startFunc = os.getenv('flow_start_func')

        # start function input to start graph execution with
        # relevant for running isolated steps in container in LOCAL mode
        self.startFuncInput = os.getenv('flow_start_func_input')


        # start function to start graph execution from
        # relevant for running isolated steps in container in REMOTE/CLOUD mode
        self.start_remote_func = os.getenv('STEP_NAME')

        # start function input to start graph execution with
        # relevant for running isolated steps in container in REMOTE/CLOUD mode
        self.start_remote_step_input = os.getenv('STEP_INPUT')

        # remote callback url to report step execution results or failure
        # relevant for running isolated steps in container in REMOTE/CLOUD mode
        self.remote_callback_url = os.getenv('CALLBACK_URL')

        # remote callback token to report step execution results or failure back to flow
        # relevant for running isolated steps in container in REMOTE/CLOUD mode in AWS
        self.remote_callback_token = os.getenv('CALLBACK_TOKEN')


        # region for boto3 client init  (AWS)
        self.region = os.getenv('SERVICE_REGION') or 'us-west-2'



        # this object is made available to expressions
        self.flow_context = {
          "step_input": None,
          "step_inputs": {},
          "step_outputs": {},
          "flow_input": input
        }




    def get_node(self, name):
        return self._graph[name]



    def add_branching(self, name, res):
        """
        adds a branching construct and expected branching results
        """
        self._results[name] = {
          "num_results":len(res),
          "results":[]
        }


    def add_branching_event(self, name, evt):
        """
        adds a result event when one branch completes
        """
        self._results[name]["results"].append(evt)



    def get_branching_events(self, name):
        return self._results[name]["results"]



    def run(self):

        step = None

        # this section runs inside the container/compute process, either locally or REMOTE/CLOUD
        if (self.startFunc and self.startFuncInput) or (
           self.start_remote_func and self.start_remote_step_input ):


            # start the flow from the method passed in env variables
            step_name_to_execute = self.startFunc or self.start_remote_func

            # start the flow with the step input passed in env variables
            step_raw_in = json.loads(self.startFuncInput or self.start_remote_step_input)

            logging.info(f"step: {step_name_to_execute} (container) input: {step_raw_in}")

            # convert to typed StepInput object
            if isinstance(step_raw_in, List):
                step_in = [StepInput.from_meta(inp) if "cls_name" in inp else inp for inp in step_raw_in]
            elif isinstance(step_raw_in, Dict) and "cls_name" in step_raw_in:
                step_in = StepInput.from_meta(step_raw_in)
            else:
                step_in = step_raw_in


            # invoke the correct step with proper inputs for joins, normal sequential steps
            if self.get_node(step_name_to_execute).type == "join":
                step = getattr(self, step_name_to_execute)(join_input=step_in)
            else: # normal step
                step = getattr(self, step_name_to_execute)(step_in)

        else:
            # or start flow from its proper start method
            step = self.start(self.graphInput)



    # this gets defined in subclasses
    def start(self, input):
        pass





    def next(self, *args, **kwargs):

        # when running inside a isolated container as a step, or in REMOTE/CLOUD mode
        if self.startFunc or self.remote_callback_url or self.remote_callback_token:
            # communicate back to flow process the output from this step
            out = None

            if "join_input" in kwargs:
                out = kwargs["join_input"].get_meta() if isinstance(kwargs["join_input"], StepInput) else kwargs["join_input"]
            else:
                # when not a join_input go over all functions referenced in self.next(...) and invoke
                out = args[-1].get_meta() if isinstance(args[-1], StepInput) else args[-1]

            self._post_results_event(out)


        # when NOT running inside a container/isolated env (running locally)
        else:
            # handle branching, and wait for results of all dependencies
            print(f"kwargs - {kwargs}")

            # get the flow context
            flow_context = self.flow_context
            parent_caller_name = inspect.stack()[1].function

            if "join_input" in kwargs:

                # handle input to the step
                last_kwarg = kwargs["join_input"].get_meta() if isinstance(kwargs["join_input"], StepInput) else kwargs["join_input"]

                # store input referenced in flow.next as output of invoker in "step_outputs" object
                flow_context["step_outputs"][parent_caller_name] = last_kwarg


                print(f"--------- parent caller step -------: {parent_caller_name}  out:----- {flow_context['step_outputs'][parent_caller_name]}")

                # now call function referenced as parameters in flow.next(f1, join_input=input)
                args[-1](join_input=kwargs["join_input"])

            else:

                # handle input to the step
                last_arg = args[-1].get_meta() if isinstance(args[-1], StepInput) else args[-1]
                last_arg = [ m.get_meta()
                             if isinstance(m, StepInput) else m
                             for m in last_arg
                           ] if isinstance(args[-1], List) else last_arg

                # store input referenced in flow.next as output of invoker in "step_outputs" object
                flow_context["step_outputs"][parent_caller_name] = last_arg

                print(f"--------- parent caller step -------: {parent_caller_name}  out:----- {flow_context['step_outputs'][parent_caller_name]}")


                condition_expr = self.get_node(parent_caller_name).condition
                foreach_expr = self.get_node(parent_caller_name).foreach_param

                # handle conditional step
                if condition_expr and len(args) == 3:
                    evaluation_factory = ExpressionEvaluatorFactory.get_evaluator()
                    evaluation_result = evaluation_factory.evaluate(condition_expr, flow_context)

                    print(f"--------- conditional step expression returned -------: {evaluation_result}")

                    if not isinstance(evaluation_result, bool):
                        print(f"--------- conditional step did not return a boolean -------: {evaluation_result}")



                    # call conditionally functions referenced as parameters in flow.next(onTrue, onFalse, input)
                    args[0](args[-1]) if evaluation_result else args[1](args[-1])


                #handle foreach step
                elif foreach_expr and len(args) == 2:
                    evaluation_factory = ExpressionEvaluatorFactory.get_evaluator()
                    evaluation_result = evaluation_factory.evaluate(foreach_expr, flow_context)

                    print(f"--------- foreach step expression returned -------: {evaluation_result}")

                    if not isinstance(evaluation_result, (List, Tuple)):
                        print(f"--------- foreach step did not return a list -------: {evaluation_result}")


                    # call foreach with function referenced as parameter in flow.next(f, input, foreach="...")
                    for res in evaluation_result:
                         args[0](res)


                # handle normal (sequence and branch) step transition case
                else:

                    for i in range(len(args) - 1):
                        # call all functions referenced as parameters in flow.next(f1, f2, .., input)
                        args[i](args[-1])




    def _post_results_event(self, results):

        # when running inside a container in local execution mode
        if self.startFunc:
            # this print statement sends an event to the outside process,
            print(f"{json.dumps(results)}")


        # when the flow is event based and follows the callback pattern
        elif self.remote_callback_url:
            CALLBACK_URL = self.remote_callback_url

            #perform an http call to CALLBACK_URL with the encoded outputs/results from this step
            # post callback metadata
            reqMeta = urllib.request.Request(CALLBACK_URL)

            reqMeta.add_header(
                'Content-Type',
                'application/json',
            )

            self._apply_credentials(request_headers=reqMeta.headers)

            try:

                response_meta = urllib.request.urlopen(reqMeta, json.dumps(results).encode('utf-8'))

                return response_meta


            except URLError as e:
                logging.info(f'failed to reach callback endpoint: {CALLBACK_URL}')
                if hasattr(e, 'reason'):
                    logging.info('Reason: ' + str(e.reason))

                if hasattr(e, 'code'):
                    logging.info('Error code: ' + str(e.code))

                if hasattr(e, 'msg'):
                    logging.info('Error message: ' + str(e.msg))

                # still throw it
                raise e


        # the callback pattern via a callback token for AWS Step Functions
        elif self.remote_callback_token:
            import boto3
            from botocore.config import Config

            sfn_config = Config(
                region_name = self.region,
                signature_version = 'v4',
                retries = {
                    'max_attempts': 5,
                    'mode': 'standard'
                }
            )


            botoClient = boto3.client('stepfunctions', config=sfn_config)
            botoClient.send_task_success(taskToken = self.remote_callback_token, output = json.dumps(results))





    def _apply_credentials(self, request_headers={}):

        ORCHESTRATOR_GOOGLE = "workflow"
        ORCHESTRATOR_STEP_FUNCTIONS = "step_functions"

        orchestrator_type = os.getenv("ORCHESTRATOR_TYPE")
        service_acct = os.getenv("SERVICE_ACCOUNT")

        logging.info(f"cloud service account {service_acct}")

        # only google is supported for now
        if ORCHESTRATOR_GOOGLE == orchestrator_type and service_acct:

            import google.auth.transport.requests
            import google.oauth2.id_token
            from google.auth.compute_engine.credentials import Credentials

            auth_req = google.auth.transport.requests.Request()
            credentials = Credentials(service_account_email = service_acct)
            credentials.refresh(auth_req)
            credentials.apply(request_headers)

        elif ORCHESTRATOR_STEP_FUNCTIONS == orchestrator_type :
            pass
