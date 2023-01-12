from datetime import datetime
from powerml.utils.run_ai import run_ai
from powerml.utils.constants import PARALLEL_REQUEST_LIMIT

class Filter():
    '''
    This is a general class that can be used to filter noise from data.
    '''

    # NOTE: Would like to add a general filter for near duplicates using Greg's Presto method
    general_filters = {}

    def __init__(self, prompt, model='text-davinci-003'):
        self.prompt = prompt
        self.model = model
        self.filters = dict(self.general_filters, Invalid=self.__filter_invalid)

    def __add_prompt(self, data):
        reformatted_data = []
        for datum in data:
            if type(datum) == dict:
                reformatted_data.append({'prompt': datum['prompt'] + '\n', 'completion': datum['completion']})
            else: # if type(datum) == str
                reformatted_data.append({'prompt': '', 'completion': datum})
        return reformatted_data

    def __fuzzy_is_valid(self, data): # NOTE: could add reference data for this
        valid_examples = []
        for i in range(0, len(data), PARALLEL_REQUEST_LIMIT):
            curr_data = data[i:i+PARALLEL_REQUEST_LIMIT]
            prompt_prepend = f'Is this a valid {self.prompt}:\n\n'
            prompt_append = '\n\nAnswer Yes if it is valid and No if it is not valid, and explain why or why not.'
            prompts = [f"{prompt_prepend}{datum['prompt']}\"{datum['completion']}\"{prompt_append}" for datum in self.__add_prompt(curr_data)]
            is_valid = run_ai(prompts,
                            stop='\nEND',
                            api="openai",
                            model=self.model,
                            max_tokens=6,
                            temperature=0.0,
                            )
            if type(is_valid) != list:
                is_valid = [is_valid]
            is_valid = [False if 'no' in output.strip().lower() else True for output in is_valid]
            valid_examples.extend([datum for j, datum in enumerate(curr_data) if is_valid[j]])
        return valid_examples

    def __filter_invalid(self, data):
        print('Start Filtering Invalid Data:', datetime.now())
        filtered_data = self.__fuzzy_is_valid(data)
        print('End Filtering Invalid Data:', datetime.now())
        return filtered_data

    def _reformat_data(self, data):
        return data

    def _reformat_filtered_data(self, filtered_data):
        return filtered_data

    def noise_filter(self, data, return_metrics=True):
        data = self._reformat_data(data)
        metrics = {}
        len_data = len(data)
        filtered_data_intersect = []
        for datum in data:
            if datum not in filtered_data_intersect:
                filtered_data_intersect.append(datum)
        metrics[f'Duplicate Noise'] = 1 - len(filtered_data_intersect) / len_data
        for filter in self.filters:
            filtered_data = self.filters[filter](data)
            metrics[f'{filter} Noise'] = 1 - len(filtered_data) / len_data
            filtered_data_intersect = [datum for datum in filtered_data_intersect if datum in filtered_data]
        metrics['Total Noise'] = 1 - len(filtered_data_intersect) / len_data
        filtered_data_intersect = self._reformat_filtered_data(filtered_data_intersect)
        if return_metrics:
            return filtered_data_intersect, metrics
        return filtered_data_intersect
