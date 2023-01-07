
from powerml import PowerML
import logging

logger = logging.getLogger(__name__)


class ForecastSequenceModel:
    def __init__(self,
                 config={},
                 max_output_tokens=256,
                 ):
        self.model = PowerML(config)
        self.model_name = "inference-io/forecast-wondery"
        self.max_output_tokens = max_output_tokens

    def predict(self, prompt):
        output = self.model.predict(
            prompt, max_tokens=self.max_output_tokens, temperature=0.7, model=self.model_name)
        return self.__post_process(output)

    def __post_process(self, series):
        series = series.strip()
        series = series.removesuffix(",")
        return [val.strip() for val in series.split(",")]
