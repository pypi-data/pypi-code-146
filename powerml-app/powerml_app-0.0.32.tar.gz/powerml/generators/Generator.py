from datetime import datetime
from powerml import PowerML
from powerml.utils.run_ai import run_ai
from powerml.utils.generator import get_types
from powerml.utils.constants import PARALLEL_REQUEST_LIMIT
from random import sample
from math import ceil


class Generator():
    '''
    This is a general class that can be used to generate examples that are not already covered by data.
    '''

    def __init__(self, gold_types=['Llama'], model='text-davinci-003', max_output_tokens=256):
        self.model = model
        self.max_output_tokens = max_output_tokens
        assert len(gold_types) >= 1, 'Please provide at least 1 gold type.'
        self.gold_types = gold_types

    def __fuzzy_modify(self, data, prompt):  # NOTE: could add reference data for this
        modified_examples = []
        for i in range(0, len(data), PARALLEL_REQUEST_LIMIT):
            curr_data = data[i:i+PARALLEL_REQUEST_LIMIT]
            prompt_append = f'\n\nModify this example to {prompt}.\n\n\"'
            prompts = [f'\"{datum}\"{prompt_append}' for datum in curr_data]
            generations = run_ai(prompts,
                                 stop='\"',
                                 api="openai",
                                 model=self.model,
                                 max_tokens=self.max_output_tokens,
                                 temperature=0.5,
                                 )
            if type(generations) != list:
                generations = [generations]
            modified_examples.extend([generation.strip()
                                     for generation in generations])
        return modified_examples

    def _generate_modified(self, data, modifier, num_generate):
        print('Start Generating Modified Data:', datetime.now())
        generated_data = self.__fuzzy_modify(
            sample(data, num_generate), modifier)
        print('End Generating Modified Data:', datetime.now())
        return generated_data

    def compute_coverage(self, generated_types):
        generated_types = set(generated_types)
        gold_types = set(self.gold_types)
        num_matched_items = len(gold_types.intersection(generated_types))
        num_real_items = len(gold_types)
        coverage = num_matched_items / num_real_items
        rare_types = gold_types.difference(generated_types)
        return {
            'Coverage': coverage,
            'Rare Types': rare_types,
        }

    def coverage_generator(self, data, return_metrics=True, prediction_model=PowerML()):
        model = prediction_model
        # should call model.fit(data) once available
        model_predictions = []
        for datum in data:
            model_predictions.append(model.predict(datum))
        print(f'model predictions: {model_predictions}')
        generated_types = get_types(model_predictions, self.gold_types)
        metrics = self.compute_coverage(generated_types)
        coverage = metrics['Coverage']
        rare_types = metrics['Rare Types']
        generated_data = []
        if rare_types:
            # generate at least 1 example per rare_type, proportional to the amount of coverage of the data
            num_generate = ceil((1 - coverage) * len(data) / len(rare_types))
            print(f'num generate: {num_generate}')
            for rare_type in rare_types:
                modifier = f'include \'{rare_type}\''
                generated_data.extend(self._generate_modified(
                    data, modifier, num_generate))
        if return_metrics:
            return generated_data, metrics
        return generated_data
