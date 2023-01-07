from ... import IoC_Container
from .abstract.i_automation import IAutomation
from .abstract.i_module_generator import IModuleGenerator


class AutomationModuleGenerator(IAutomation):
    
    def auto_generate_modules(self, module_type_number: int, module_names_list: list) -> dict:
        # Getting IoC Container 
        ioc_container = IoC_Container.CONTAINER
        # Creating instance of Module Generator 
        module_generator_obj: IModuleGenerator = ioc_container.resolve(IModuleGenerator)
        # Getting Module Type name by option number
        module_type_name = self.get_option_name_by_number(module_type_number)
        try:
            generated_modules_path_list = {}
            # Continuing Module Generating operation from each module name from the list
            for module_name in module_names_list:
                # Generating module
                generated_modules_path_list[module_name] = module_generator_obj.generate_module(module_type_name, self.POM_TEMPLATE_FILE_PATH,\
                    self.POM_MODULE_TEMPLATE_FILE_PATH, self.POM_ROOT_BASE_PATH, module_name)
            print(self.AUTOMATION_SCRIPT_GENERATE_SUCCESS_MESSAGE)
            return generated_modules_path_list
        except Exception as err:
            print(err)
        
    
    