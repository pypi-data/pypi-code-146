import argparse
import importlib
import os
import inspect
import json
import logging

import urllib.request
from urllib.error import  URLError


from . flow_compiler import FlowCompilerFactory

def get_class_from_module(mod):
    members_cls = inspect.getmembers(mod)
    for name, obj in members_cls:
        if (inspect.isfunction(obj)):
            if getattr(obj,'decorator', None) and obj.decorator.__name__ == "flow":
                return obj

    return None




def registerSpec(flow_compiler, spec_meta={}, service_endpoint="http://127.0.0.1:8080"):
    """
    registers the flow with the genome engine with high availability and scale
    """

    flow_spec = flow_compiler.compile()
    flow_orginal = flow_compiler.flow


    api_endpoint = service_endpoint + "/v1.0/genome/pipelineSpec"

    #perform an http call to CALLBACK_URL with the encoded outputs/results from this step
    # post callback metadata
    reqMeta = urllib.request.Request(api_endpoint)

    reqMeta.add_header(
        'Content-Type',
        'application/json',
    )

    flow_meta = {
        "application": spec_meta["application"] if "application" in spec_meta else flow_orginal.application,
        "canonicalName": spec_meta["canonicalName"] if "canonicalName" in spec_meta else flow_orginal.canonicalName,
        "pipelineName": flow_orginal._graph.name,
        "versionName": spec_meta["versionName"] if "versionName" in spec_meta else flow_orginal.versionName,
        "recipeRef": {
        "ref": flow_spec,
        "refType": "inline-pipeline"
        }
    }

    if "schedule" in spec_meta or flow_orginal.schedule:
        flow_meta["schedule"] = spec_meta["schedule"] if "schedule" in spec_meta else flow_orginal.schedule


    try:

        response_meta = urllib.request.urlopen(reqMeta, json.dumps(flow_meta).encode('utf-8'))
        logging.info(f'saved pipelineSpec at endpoint: {api_endpoint}')

        return response_meta


    except URLError as e:
        logging.info(f'failed to reach endpoint: {api_endpoint}')
        if hasattr(e, 'reason'):
            logging.info('Reason: ' + str(e.reason))

        if hasattr(e, 'code'):
            logging.info('Error code: ' + str(e.code))

        if hasattr(e, 'msg'):
            logging.info('Error message: ' + str(e.msg))

        # still throw it
        raise e



parser = argparse.ArgumentParser(description='arguments for genome flow cli')
parser.add_argument("--module", type=str)
parser.add_argument("--compile", type=bool)
parser.add_argument("--register", type=bool)
parser.add_argument("--run", type=bool)

args = parser.parse_args()


def run_script():

    user_module_value = args.module


    module = importlib.import_module(user_module_value)
    class_ = get_class_from_module(module)

    print(f"arguments: env:{os.getenv('MAMA')} | {user_module_value} | {class_}")


    if not class_:
        raise Exception(f" -- No @flow annotated python pipeline class found in the module: {user_module_value}")


    flow_object = class_()

    if args.run:
        flow_object.run()


    genome_compiler = FlowCompilerFactory.get_compiler(flow_object, target="genome")

    if args.compile:
        print(genome_compiler.compile())
    if args.register:
        registerSpec(genome_compiler)


if __name__ == "__main__":
    run_script()
