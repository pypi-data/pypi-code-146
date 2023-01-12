import re
import json
import yaml
from decouple import config
from orchestrator_service_rules.utilities import absolute_component_factory_module
from orchestrator_service_rules.orchestrator_base_exception import OrchestratorBaseException
from orchestrator_service_rules.validate_rule import ValidateRule

class ServiceOrchestration:
    def __init__(self, rule: dict, base_data=None):
        self.rule = self.__parse(json.dumps(rule))
        if base_data:
            self.base_data = base_data
        else:
            self.base_data = dict()

    def component_factory_module(self, path, component: str):
        path_component = path % component
        return absolute_component_factory_module(path_component)

    def execute(self):
        self.__executed_steps = []
        self.payload = dict()
        self.execution_error = None
        self.continue_process = True
        self.temp_data_error = None
        try:
            
            self.execute_steps(self.rule['steps'])

            if not self.continue_process:
                self.continue_process = True
                on_stop = self.rule.get('on_stop')
                if on_stop:
                    self.execute_steps(on_stop)
        except OrchestratorBaseException as e:
            self.temp_data_error = e.temp_data

            self.execution_error = f"On component '{self.__current_component}' -> {str(e)}"

            for service in reversed(self.__executed_steps):
                service.rollback()
            self.execute_steps(e.steps)

        except Exception as e:
            self.execution_error = f"On component '{self.__current_component}' -> {str(e)}"
            print(self.execution_error)
            for service in reversed(self.__executed_steps):
                service.rollback()
            self.execute_steps(self.rule['on_error'])

    def execute_steps(self, steps):
        temp_data = None
        for step in steps:
            if step['active']:
                self.__current_component = step['alias']
                module = self.component_factory_module(step['path_component'], step['component'])
                service = module.Service(self.__current_component, self, temp_data)
                service.setup(**step['settings'])
                service.run()
                if not self.continue_process:
                    break
                service.store_temporal_data()
                self.__executed_steps.append(service)
                temp_data = service.temp_data

    def __parse(self, data: str) -> dict:
        self.__path_matcher = re.compile(r'\$\{([^}^{]+)\}')
        loader = yaml.SafeLoader
        loader.add_implicit_resolver(None, self.__path_matcher, None)
        loader.add_constructor(None, self.__path_constructor)
        return yaml.load(yaml.dump(json.loads(data)), Loader=loader)

    def __path_constructor(self, loader, node):
        try:
            value = node.value
            match = self.__path_matcher.match(value)
            env_var = match.group()[2:-1]
            return config(env_var) + value[match.end():]
        except Exception:
            return None
