from powerml import PowerML
import logging

logger = logging.getLogger(__name__)


class ExtractMenuItemsModel:
    def __init__(self, config={}, max_output_tokens=512, temperature=0.7):
        self.max_output_tokens = max_output_tokens
        self.model = PowerML(config)
        self.model_name = "presto/del-taco-menu"
        self.temperature = temperature

    def predict(self, order):
        output = self.model.predict(
            order,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
            model=self.model_name
        )
        return output
