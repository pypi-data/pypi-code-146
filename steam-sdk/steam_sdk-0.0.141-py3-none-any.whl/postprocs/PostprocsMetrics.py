from typing import List
import numpy as np

class PostprocsMetrics:

    """
        Class to calculate metrics
    """

    metrics_result: List = []

    def __init__(self, metrics_to_do: List[str] = [], var_to_interpolate: list = [], var_to_interpolate_ref: list = [],
                 time_vector: list = [], time_vector_ref: list = [], flag_run: bool = True):
        #TODO change argument names

        """
            Object gets initialized with the metrics which should be done, the variables and time_vectors to
            do the metrics on and a flag if the metrics should be done can be set to false
        """
        
        # Define inputs
        self.metrics_to_do = metrics_to_do
        self.var_to_interpolate = var_to_interpolate
        self.var_to_interpolate_ref = var_to_interpolate_ref
        self.time_vector = time_vector
        self.time_vector_ref = time_vector_ref

        # Convert variables to np.array, if needed
        self.var_to_interpolate = [np.array(v) for v in self.var_to_interpolate]
        self.var_to_interpolate_ref = [np.array(v) for v in self.var_to_interpolate_ref]
        self.time_vector = [np.array(v) for v in self.time_vector]
        self.time_vector_ref = [np.array(v) for v in self.time_vector_ref]

        if flag_run:
            self.run_metrics()

    def run_metrics(self):

        """
            Function to initiate interpolation, start the different metrics and append the result to the output
        """

        # unpack inputs
        metrics_to_do = self.metrics_to_do
        var_of_interest = self.var_to_interpolate
        var_ref = self.var_to_interpolate_ref
        time_vector = self.time_vector
        time_vector_ref = self.time_vector_ref

        # variables which need to be interpolated
        list_metrics_that_need_interpolation = ['maximum_abs_error', 'RMSE', 'RMSE_ratio']
        list_metrics_that_need_interpolation_ref = ['maximum_abs_error', 'RMSE', 'RMSE_ratio']

        # interpolation of variable when necessary using the time_vector of the reference as time_stamps
        if any(n in metrics_to_do for n in list_metrics_that_need_interpolation):
            time_stamps = np.linspace(time_vector_ref[0], time_vector_ref[-1], num=len(time_vector_ref))
            var_of_interest = self._interpolation(time_stamps, time_vector, var_of_interest)
        if any(n in metrics_to_do for n in list_metrics_that_need_interpolation_ref):
                time_stamps_ref = np.linspace(time_vector_ref[0], time_vector_ref[-1], num=len(time_vector_ref))
                var_ref = self._interpolation(time_stamps_ref, time_vector_ref, var_ref)

        # evaluating which metrics will be done and appending results to metrics_result
        self.metrics_result = []
        for metric in metrics_to_do:
            if metric == 'maximum_abs_error':
                result = self._maximum_abs_error(var_of_interest, var_ref)
            elif metric == 'RMSE':
                result = self._RMSE(var_of_interest, var_ref)
            elif metric == 'RMSE_ratio':
                result = self._RMSE_ratio(var_of_interest, var_ref)
            elif metric == 'quench_load_error':
                result = self._quench_load_error(time_vector, var_of_interest, time_vector_ref, var_ref)
            elif metric == 'quench_load':
                result = self._quench_load(time_vector, var_of_interest)
            elif metric == 'max':
                result = self._peak_value(var_of_interest)
            else:
                raise Exception(f'Metric {metric} not understood!')
            self.metrics_result.append(result)

    # calculating metrics
    @staticmethod
    def _interpolation(linspace_time_stamps, time_vector, var_to_interpolate):

        """
            function to interpolate a variable
        """

        return np.interp(linspace_time_stamps, time_vector, var_to_interpolate) if len(
            var_to_interpolate) != 0 else []

    @staticmethod
    def _maximum_abs_error(y, y_ref):

        """
            function to calculate the absolute error between simulation and measurement
        """

        return max(abs(y - y_ref))

    @staticmethod
    def _RMSE(y, y_ref):

        """
            function to calculate the RMSE between simulation and measurement
        """

        return np.sqrt(((y - y_ref) ** 2).mean()) # np.sqrt(mean_squared_error(y, y_ref))

    def _RMSE_ratio(self, y, y_ref):

        """
            function to calculate the RMSE divided by the peak value of the measurement between simulation and measurement
        """

        return np.sqrt(((y - y_ref) ** 2).mean())/self._peak_value(y_ref)

    def _quench_load_error(self, time_vector, Ia, time_vector_ref, Ia_ref):

        """
            function to calculate the quench load error between simulation and measurement
        """

        return self._quench_load(time_vector, Ia) - self._quench_load(time_vector_ref, Ia_ref)

    @staticmethod
    def _quench_load(time_vector, Ia):

        """
            function to calculate the quench load of a current
        """

        dt = [*np.diff(time_vector), 0]
        quench_load_sum = np.cumsum((Ia ** 2) * dt)
        quench_load = quench_load_sum[-1]

        return quench_load

    @staticmethod
    def _peak_value(signal):

        """
            function to calculate the peak value of a signal
        """

        return max(signal)