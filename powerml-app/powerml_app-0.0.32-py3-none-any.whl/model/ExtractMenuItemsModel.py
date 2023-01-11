from powerml import PowerML
import logging
import re

logger = logging.getLogger(__name__)


class ExtractMenuItemsModel:
    def __init__(self, config={}, max_output_tokens=512, temperature=0.7):
        self.max_output_tokens = max_output_tokens
        self.model = PowerML(config)
        self.model_name = "presto/del-taco-menu/v2"
        self.temperature = temperature
        self.examples = []

    def fit(self, examples=[]):
        """
        Parameters
        ----------
        examples : list
            Takes a list of dictionaries where each dictionary has a key:
            "conversation" with a transcript and a key "order" with the resulting order the user had.
        """
        self.examples = examples

    def predict(self, conversation):
        prompt = {
            "{{examples}}": "\n\n".join(["CONVERSATION:\n" + example["conversation"] + "\nORDER:\n" + example["order"] for example in self.examples]),
            "{{input}}": conversation
        }
        output = self.model.predict(
            prompt,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
            model=self.model_name
        )
        return self.__post_process(output)

    def __post_process(self, output):
        # TODO: replace with stop tokens
        results = re.split('\\\\nEND|\\nEND|\nEND|\n\n', output)
        return results[0].strip()
