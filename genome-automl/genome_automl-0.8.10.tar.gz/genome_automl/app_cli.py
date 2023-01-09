import argparse
import importlib
import os
import json
import logging


import urllib.request
from urllib.error import  URLError


from .pipelines.flows import BaseGraph
from .pipelines.flow_compiler import FlowCompilerFactory

from .pipelines.flow_cli import get_class_from_module
from .pipelines.flow_cli import registerSpec as registerPipelineSpec


"""
python cli script to enable application configuration registration and deployment
generates an appspec object with the complied pipeline names and versions
the name and version of pipelines are extracted from the respective python class definitions

supports flow compilation as well as flow registration for all pipelines referenced in the appSpec
supports appSpec registration and deployment via the respective genome API-s
"""


def registerSpec(appSpec={}, service_endpoint="http://127.0.0.1:8080"):
    """
    registers the appSpec in genome
    """


    api_endpoint = service_endpoint + "/v1.0/genome/appSpec"

    # post metadata
    reqMeta = urllib.request.Request(api_endpoint)

    reqMeta.add_header(
        'Content-Type',
        'application/json',
    )

    try:

        response_meta = urllib.request.urlopen(reqMeta, json.dumps(appSpec).encode('utf-8'))
        logging.info(f'saved appSpec at endpoint: {api_endpoint}')

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
parser.add_argument("--appSpec", type=str, default=None)
parser.add_argument("--register", type=bool)
parser.add_argument("--deploy", type=bool)

args = parser.parse_args()


def run_script():

    user_module_value = args.module

    genome_environment = os.getenv('GENOME_ENVIRONMENT') or "local"
    app_config_path = args.appSpec or (user_module_value + f"/app.{genome_environment}.spec")

    app_config_raw = None
    with open(app_config_path) as file:
        app_config_raw = json.load(file)


    if not app_config_raw:
        raise Exception(f"no app configuration found at: {app_config_path}")

    print(f"arguments: env:{os.getenv('GENOME_ENVIRONMENT')} | {user_module_value} | {app_config_raw}")



    # replace slashes in pipeline class paths
    cls_paths = [("." + p.replace("/",".")) for p in app_config_raw["pipeline-paths"]]



    pipelines = {}
    deploy_pipeline = None
    for cls_path in cls_paths:

        # load the correct modules from the class paths in app.[env].spec
        module = importlib.import_module(user_module_value + cls_path)

        class_ = get_class_from_module(module)
        print(f"class found: {class_}")

        # compile class
        flow_object = class_()
        genome_pipe_compiler = FlowCompilerFactory.get_compiler(flow_object, target="genome")

        pipelines[class_.__name__] = flow_object.versionName

        if cls_path == ("." + app_config_raw["lifecycle"]["deploy"].replace("/", ".")):
            deploy_pipeline = class_.__name__

        if args.register:
            registerPipelineSpec(genome_pipe_compiler)


    if not deploy_pipeline:
        raise Exception(f"no deployment pipeline found at: {app_config_raw['lifecycle']['deploy']}")


    # replace raw with compiled config
    del app_config_raw["pipeline-paths"]
    app_config_raw["pipelines"] = pipelines
    app_config_raw["lifecycle"]["deploy"] = deploy_pipeline

    print(f"compiled appSpec: {json.dumps(app_config_raw)}")


    if args.register:
        registerSpec(appSpec=app_config_raw)




if __name__ == "__main__":
    run_script()
