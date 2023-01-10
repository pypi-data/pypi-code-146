class IOTDataStructure(object):
    """description of class"""
    def __init__(self ):
        self._variables = []
        self._predict_label = -1
        self._class_name_list = []

    @property
    def variables(self):
        return self._variables

    def set_variable(self, variables):
        self._variables = variables

    def add_variable(self, variable):
        self._variables.append(variable)

    def remove_variable(self, variable):
        self._variables.remove(variable)

    @property
    def true_label(self):
        return self._true_label

    def set_true_label(self, true_label):
        self._true_label = true_label

    @property
    def predict_label(self):
        return self._predict_label

    def set_predict_label(self, predict_label):
        self._predict_label = predict_label

    @property
    def variable_list(self):
        return self._variable_list

    def set_variable_list(self, variable_list):
        self._variable_list = variable_list

    @property
    def output_name(self):
        return self._output_name

    def set_output_name(self, output_name):
        self._output_name = output_name

    @property
    def class_name_list(self):
        return self._class_name_list

    def set_class_name_list(self, class_name_list):
        self._class_name_list = class_name_list
