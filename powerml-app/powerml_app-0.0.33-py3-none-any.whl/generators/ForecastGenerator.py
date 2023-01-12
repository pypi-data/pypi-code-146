from powerml import Generator
from powerml import ForecastSequenceModel
from powerml.utils.generator import get_types
from math import ceil


class ForecastGenerator(Generator):
    '''
    This is a class that can be used to generate more data for ForecastSequenceModels.
    '''

    def __init__(self, gold_types=['monotonically increasing']):
        super().__init__(gold_types)

    def coverage_generator(self, data, return_metrics=True):
        model = ForecastSequenceModel()
        model.fit(data)
        titles = [datum['title'] for datum in data]
        model_predictions = []
        for title in titles:
            model_predictions.append(model.predict(title))
        data = [datum['revenue'] for datum in data]
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
                modifier = f'be {rare_type}'
                generated_data.extend(self._generate_modified(data, modifier, num_generate))
        if return_metrics:
            return generated_data, metrics
        return generated_data
