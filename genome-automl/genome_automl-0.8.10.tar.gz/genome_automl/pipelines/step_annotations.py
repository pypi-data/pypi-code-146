import functools
import inspect

import logging
import json
import os
import subprocess


from .flow_parser import FlowGraph

from typing import Mapping, List, Union, Tuple, Dict, Any

from .. base import TransformExecution
from .step_input import StepInput
from .steps.call_steps import PushStep, QueryStep
from .input_converter import ExpressionEvaluatorFactory, InputConverter


import sys



def transform_step(*deco_args,**deco_kwargs):
    """
    decorator for steps that perform transforms/computation
    transform steps are always performed on isolated container/compute
    step_type: type of the step of the target orchestration system to compile
    (aws step functions, google workflows, etc.)
    """

    def decorator_step(func):
        @functools.wraps(func)
        def wrapper_step(*args, **kwargs):

            # handle when decorator has no kwargs (@transform_step invoked, rather than @transform_step(...))
            step_type =  ("step_type" in deco_kwargs and deco_kwargs["step_type"]) or "TransformStep"
            step_name =  ("step_name" in deco_kwargs and deco_kwargs["step_name"]) or "vanillaStep"
            image = ("image" in deco_kwargs and deco_kwargs["image"]) or None
            retry = ("retry" in deco_kwargs and deco_kwargs["retry"]) or 3
            resources = ("resources" in deco_kwargs and deco_kwargs["resources"]) or None
            expression_input = ("expression_input" in deco_kwargs and deco_kwargs["expression_input"]) or None


            # assign flow object and other
            obj = args[0]
            node_name = func.__name__
            step_type = step_type if not node_name in ("start", "end") else {
              "start": "StartStep",
              "end": "EndStep"
              }[node_name]


            #this is an empty run to capture expression_inputs, and/or step resources during compilation
            if "compile_run" in kwargs and kwargs["compile_run"]:


                # handle resource requirements (instance type, SPOT etc.)
                if resources:
                    #assign resources to main graph
                    resources_dict = None
                    if isinstance(resources, TransformExecution):
                        resources_dict = resources.__dict__
                    elif isinstance(resources, Dict):
                        resources_dict = resources

                    obj._graph_steps_map[node_name]["step_resources"] = resources_dict



                # handle expression inputs
                if expression_input and isinstance(expression_input, StepInput):

                    #assign expression input to main graph
                    obj._graph_steps_map[node_name]["step_expression_input"] = expression_input.get_meta()


                return None



            # this section executes as part of *local flow execution/debugging* process
            # it does NOT run in isolated local/remote compute
            if not obj.startFunc and not obj.start_remote_func:

                print(f"calling transform step: {step_type}")
                print(f"executing func step: {func.__name__}")

                # get the flow context
                flow_context = obj.flow_context

                # handle input to the step
                last_arg = args[-1].get_meta() if isinstance(args[-1], StepInput) else args[-1]

                #set current step input to flow context *step_inputs* object
                flow_context["step_inputs"][node_name] = last_arg

                #set current step input to flow context
                flow_context["step_input"] = last_arg


                # handle expression evaluation of input
                if expression_input and isinstance(expression_input, StepInput):
                    # convert expression_input to a proper StepInput
                    converter = InputConverter(expression_input, flow_context)
                    converted_input = converter.convert()

                    #now set the input to the converted input
                    last_arg = converted_input.get_meta()



                # here the step function delegates to some local execution engine
                # to perform isolated compute
                # todo support getting the docker image from the input if provided there
                cmd = (f"docker run "
                       f"--env flow_start_func={func.__name__} "
                       f"--env flow_start_func_input='{json.dumps(last_arg)}' "
                       f"--rm {image}")



                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                out, err = p.communicate()

                if err:
                    # print raw results
                    print(f"raw errors from container: {err.decode('utf-8')}")


                # this part handles computation results
                outputs = out.decode('utf-8')
                print(f"finished running transform step: {step_type} --- {outputs} ---")

                results = None
                if outputs:
                    for line in outputs.splitlines():

                        try:
                            results = json.loads(line)
                        except:
                            pass

                        #on the first successful json parse with an input of type StepInput move on
                        if results and 'cls_name' in results:
                            break


                if not results:
                    raise Exception(f"no valid StepInput type result returned from step {node_name}")



                # handle all branching types, [static, condition, foreach]
                if obj.get_node(node_name).type in ("split-and", "split-or", "foreach"):
                    foreach_expr = obj.get_node(node_name).foreach_param or "[]"
                    num_expected_results = {
                      "split-or": 1,
                      "split-and": len(obj.get_node(node_name).out_funcs),
                      "foreach": len(ExpressionEvaluatorFactory.get_evaluator().evaluate(foreach_expr, flow_context))
                    }
                    obj.add_branching(node_name, range(num_expected_results[obj.get_node(node_name).type]))

                # for each result call the corresponding next step
                # the next step is invoked with the result of this step as the input
                next_steps = obj._graph_steps_map[node_name]["next"]
                for next_step in next_steps:

                    # print raw results
                    logging.info(f"raw results from container: {next_step} - {results}")


                    # convert raw json dict back to StepInput
                    step_in = StepInput.from_meta(results)

                    #store output of this step in flow context "step_outputs" object
                    flow_context["step_outputs"][node_name] = results


                    # if this is an invocation to a join type of step
                    if obj.get_node(next_step).type == "join":
                        getattr(obj, next_step)(join_input=step_in)
                    # normal step invocation
                    else:
                        getattr(obj, next_step)(step_in)


            else: # this section executes on an isolated container as part of a compute task

                # no need to convert to StepInput
                # conversion already happened in flow.run method
                if "join_input" in kwargs:
                    kwargs["join_input"] = [a for a in kwargs["join_input"]]
                    all_args = args

                else:
                    # conversion already happened in flow.run method
                    last_arg = args[-1]
                    all_args = []

                    for a in range(len(args) - 1):
                        all_args.append(args[a])

                    all_args.append(last_arg)

                # now execute the function
                v = func(*all_args, **kwargs)


                # now return the steps results
                return v


        return wrapper_step
    return decorator_step(*deco_args) if len(deco_args) else decorator_step


# step annotation
def step(*deco_args, **deco_kwargs):
    def decorator_step(func):
        @functools.wraps(func)
        def wrapper_step(*args, **kwargs):

            # handle when decorator has no kwargs (@step invoked, rather than @step(...))
            step_type = ("step_type" in deco_kwargs and deco_kwargs["step_type"]) or "PassStep"
            step_name = ("step_name" in deco_kwargs and deco_kwargs["step_name"]) or "vanillaStep"
            retry = ("retry" in deco_kwargs and deco_kwargs["retry"]) or 3
            expression_input = ("expression_input" in deco_kwargs and deco_kwargs["expression_input"]) or None


            print(f"--------- calling step: {step_type} - {func.__name__}")

            obj = args[0]
            node_name = func.__name__
            step_type = step_type if not node_name in ("start", "end") else {
              "start": "StartStep",
              "end": "EndStep"
              }[node_name]


            # this is an empty run to capture expression_inputs during compilation
            if "compile_run" in kwargs and kwargs["compile_run"]:

                if expression_input and isinstance(expression_input, StepInput):

                    #assign expression input to main graph
                    obj._graph_steps_map[node_name]["step_expression_input"] = expression_input.get_meta()

                return None






            # get the flow context
            flow_context = obj.flow_context

            # handle input to the step
            last_arg = args[-1].get_meta() if isinstance(args[-1], StepInput) else args[-1]


            #set current step input to flow context
            flow_context["step_inputs"][node_name] = last_arg

            #set current step input to flow context
            flow_context["step_input"] = last_arg


            #now transform the input according to expression_input
            if expression_input and isinstance(expression_input, StepInput):
                # convert expression_input to a proper StepInput
                converter = InputConverter(expression_input, flow_context)
                converted_input = converter.convert()

                #now set the input to the converted input
                last_arg = converted_input.get_meta()
                last_arg = StepInput.from_meta(last_arg)


            last_transformed_arg = last_arg





            #change last argument for input transformation
            all_args = []
            for a in range(len(args) - 1):
                all_args.append(args[a])

            all_args.append(last_transformed_arg)



            # handle branching
            if obj.get_node(node_name).type in ("split-and", "split-or", "foreach"):
                foreach_expr = obj.get_node(node_name).foreach_param
                num_expected_results = {
                  "split-or": 1,
                  "split-and": len(obj.get_node(node_name).out_funcs),
                  "foreach": foreach_expr and len(ExpressionEvaluatorFactory.get_evaluator().evaluate(foreach_expr, flow_context))
                }
                obj.add_branching(node_name, range(num_expected_results[obj.get_node(node_name).type]))



            # if its a join don't advance until all results come in
            if obj.get_node(node_name).type == "join":
                split_parent = obj.get_node(node_name).split_parents[-1]
                print(f"prior splits - {obj.get_node(node_name).split_parents}")
                num_res = obj._results[split_parent]["num_results"]
                obj.add_branching_event(split_parent, kwargs["join_input"])

                # return all inputs from branches
                if num_res == len(obj.get_branching_events(split_parent)):
                    kwargs["join_input"] = obj.get_branching_events(split_parent)


                    v = func(*all_args, **kwargs)


                    print(f"completed join step: {step_type}")
                    return v

                else:
                    # on non join step register the event
                    print(f"step event: {step_type}")


            else:

                # handle query or publish type steps, only applicable to local (non-cloud) executions
                # where the step needs to query a service with an input
                if "push" in step_type.lower():
                    call_step = PushStep(step_type)
                    response_entry = call_step.push_entry(last_transformed_arg)
                    all_args[-1] = response_entry
                elif "query" in step_type.lower():
                    call_step = QueryStep(step_type)
                    response_entry = call_step.query(last_transformed_arg)
                    all_args[-1] = response_entry



                v = func(*all_args, **kwargs)
                print(f"completed step: {step_type}")
                return v

        return wrapper_step
    return decorator_step(*deco_args) if len(deco_args) else decorator_step



# transformer annotation on compute functions for reporting start/completion
def transformer(function_name="transformer"):
    def deco_transformer(func):
        @functools.wraps(func)
        def wrapper_transformer(*args, **kwargs):
            logging.info(f"running transformer: {func.__name__ or function_name}")
            v = func(*args, **kwargs)
            logging.info(f"completed transformer: {func.__name__ or function_name}")
            return v

        return wrapper_transformer
    return deco_transformer
