from pybpodapi.bpod_modules.bpod_module import BpodModule


class Alyx(BpodModule):
    
    @staticmethod
    def check_module_type(module_name):
        return module_name and module_name.startswith('Alyx')