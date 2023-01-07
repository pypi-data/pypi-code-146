from ddd_objects.domain.value_obj import ValueObject

class PipelineIndicator(ValueObject):
    def __init__(self, value='run') -> None:
        self.value = value

    def is_wait(self):
        return self.value=='wait'
    
    def is_pass(self):
        return self.value=='pass'

    def is_run(self):
        return self.value=='run'
    
    def is_run_again(self):
        return self.value=='run again'

    def is_over(self):
        return self.value=='over'
    
    def set_wait(self):
        self.value='wait'
        return self
    
    def set_pass(self):
        self.value='pass'
        return self

    def set_run(self):
        self.value='run'
        return self

    def set_run_again(self):
        self.value='run again'
        return self

    def set_over(self):
        self.value='over'
        return self

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return self.value

class PipelineContext(ValueObject):
    def __repr__(self) -> str:
        return str(self.value)

class Function(ValueObject):
    pass

class CommandRequestID(ValueObject):
    pass

class PipelineOutput(ValueObject):
    pass