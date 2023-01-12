from powerml import PowerML
import logging

logger = logging.getLogger(__name__)


class WriteEmailModel:
    def __init__(self, config={}, max_output_tokens=512, temperature=0.7):
        self.max_output_tokens = max_output_tokens
        self.model = PowerML(config)
        self.model_name = "stensul/email-copy/v2"
        self.temperature = temperature

    def fit(self, examples):
        """
        Parameters
        ----------
        examples : list
            Takes a list of dictionaries where each dictionary has keys:
                subject: <subject>
                email: <email>
        """
        self.examples = examples

    def predict(self, subject: str):
        example_string = "\n\n".join(
            [f"company: {example['subject']}\n\nemail: {example['email']}" for example in self.examples])
        prompt = {
            "{{examples}}": example_string,
            "{{input}}": subject
        }
        output = self.model.predict(
            prompt,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
            model=self.model_name
        )
        return output
