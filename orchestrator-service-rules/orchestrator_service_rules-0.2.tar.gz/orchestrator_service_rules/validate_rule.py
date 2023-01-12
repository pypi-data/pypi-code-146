class ValidateRuleException(Exception):
    pass

class ValidateRule:
    ''' This class makes validations to the entered rule '''

    def __init__(self, rule):
        self._rule = rule
        self._alias = dict()
        self.validate_steps(self._rule["steps"])
        self.validate_steps(self._rule["on_stop"])
        self.validate_steps(self._rule["on_error"])

    def validate_steps(self, steps):
        ''' Iterate the provided steps '''
        for step in steps:
            self.add_key_alias(step["alias"])            
            self.validate_alias_error_steps(step["settings"])
            
    def add_key_alias(self, alias):
        ''' Add key, if already exists return exception '''
        if self._alias.get(alias) is None:
            self._alias[alias] = alias
        else:
            raise ValidateRuleException(f"El alias '{alias}' esta duplicado")

    def validate_alias_error_steps(self, settings):
        ''' Receive settings if the key exists error_steps will iterate the steps '''
        if settings.get('error_steps') is not None:
            for step in settings["error_steps"]:
                self.add_key_alias(step["alias"])
                self.validate_alias_error_steps(step["settings"])
