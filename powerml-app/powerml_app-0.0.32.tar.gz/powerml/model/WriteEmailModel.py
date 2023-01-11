from powerml import PowerML
import logging

logger = logging.getLogger(__name__)


class WriteEmailModel:
    def __init__(self, config={}, max_output_tokens=512, temperature=0.7):
        self.max_output_tokens = max_output_tokens
        self.model = PowerML(config)
        self.model_name = "stensul/email-copy"
        self.temperature = temperature

    def predict(self, subject):
        output = self.model.predict(
            subject,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
            model=self.model_name
        )
        return output
