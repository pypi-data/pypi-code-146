
from powerml import PowerML
import logging
import re
logger = logging.getLogger(__name__)


class ForecastSequenceModel:
    def __init__(self,
                 config={},
                 max_output_tokens=256,
                 ):
        self.model = PowerML(config)
        self.model_name = "inference-io/forecast-wondery/v2"
        self.max_output_tokens = max_output_tokens

    def fit(self, examples=[]):
        """
        Parameters
        ----------
        examples : list
            Takes a list of dictionaries where each dictionary has keys:
                release_date: "2018-07-31"
                title: "What's Saving My Life (4/4)"
                revenue: [248, 233, 147, 174, 242, 257, 231, 198, 194, 137]
        """
        self.examples = examples

    def predict(self, title):
        example_string = "\n\n"
        for example in self.examples:
            example_string += "This is an accurate forecast of daily podcast revenue for:\n"
            example_string += "release date: " + example["release_date"] + "\n"
            example_string += "title: " + example["title"] + "\n"
            revenue_string = ", ".join([str(revenue)
                                       for revenue in example["revenue"]])
            example_string += "revenue per day: " + revenue_string + "\n\n"

        prompt = {
            "{{examples}}": example_string,
            "{{title}}": title
        }
        output = self.model.predict(
            prompt, max_tokens=self.max_output_tokens, temperature=0.7, model=self.model_name)
        return self.__post_process(output)

    def __post_process(self, output):
        # TODO: replace with stop tokens
        results = re.split('\n\n', output)
        series = results[0].strip()
        series = series.removesuffix(",")
        return [val.strip() for val in series.split(",")]
