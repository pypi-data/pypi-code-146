from .helpers.data_getters_setter import data_getter_root_dict, data_getter_root_str, data_setter_root, data_getter_root_list


class ContextProps:
    def __init__(self):
        self.data = {}

    @property
    def variables(self):
        return data_getter_root_dict(self, 'variables')

    @variables.setter
    def variables(self, value):
        data_setter_root(self, 'variables', value)

    @property
    def block_context(self):
        return data_getter_root_dict(self, 'block_context')

    @block_context.setter
    def block_context(self, value):
        data_setter_root(self, 'block_context', value)

    @property
    def current_algorithm(self):
        return data_getter_root_str(self, 'current_algorithm')

    @current_algorithm.setter
    def current_algorithm(self, value):
        data_setter_root(self, 'current_algorithm', value)

    @property
    def current_variables(self):
        return data_getter_root_dict(self, 'current_variables')

    @current_variables.setter
    def current_variables(self, value):
        data_setter_root(self, 'current_variables', value)

    @property
    def deferred(self):
        return data_getter_root_list(self, 'deferred')

    @deferred.setter
    def deferred(self, value):
        data_setter_root(self, 'deferred', value)

    @property
    def status(self):
        return data_getter_root_str(self, 'status')

    @status.setter
    def status(self, value):
        data_setter_root(self, 'status', value)

    @property
    def result(self):
        return data_getter_root_dict(self, 'result')

    @result.setter
    def result(self, value):
        data_setter_root(self, 'result', value)

    @property
    def commands(self):
        return data_getter_root_dict(self, 'commands')

    @commands.setter
    def commands(self, value):
        data_setter_root(self, 'commands', value)

    # @property
    # def operation(self):
    #     try:
    #         return self.data['operation']
    #     except KeyError:
    #         self.data['operation'] = {
    #             'status': 'run',
    #             'result': None,
    #             'commands': []
    #         }
    #         return self.data['operation']
    #
    # @operation.setter
    # def operation(self, value):
    #     self.data['operation'] = value
