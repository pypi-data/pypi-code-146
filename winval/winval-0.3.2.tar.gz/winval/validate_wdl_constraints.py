import argparse
import json

from winval.wdl_parser import WdlParser
from winval.constraints_pre_processor import ConstraintsPreProcessor
from winval.winval_class import Winval
from winval import logger


def run_winval(wdl_file: str, json_file: str) -> bool:
    logger.debug('--------------')
    logger.debug('--- WINVAL ---')
    logger.debug('--------------')
    with open(json_file) as json_file:
        json_dict = json.load(json_file)
        workflow_inputs = WdlParser(wdl_file).parse_workflow_variables()
        workflow_inputs.fill_values_from_json(json_dict)
        constraints = ConstraintsPreProcessor(wdl_file).process_constraint_strings()
        return Winval(workflow_inputs, constraints).workflow_input_validation()
    

def get_args():
    parser = argparse.ArgumentParser("winval")
    parser.add_argument('--wdl', required=True)
    parser.add_argument('--json', required=True)
    parser.add_argument('--log_level', default='INFO')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    [handler.setLevel(args.log_level.upper()) for handler in logger.handlers]
    run_winval(args.wdl, args.json)
