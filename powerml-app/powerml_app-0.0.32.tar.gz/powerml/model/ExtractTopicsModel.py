
from powerml import PowerML
import logging

from powerml.model.PowerML import MAX_TEMPLATE_TOKENS

logger = logging.getLogger(__name__)


class ExtractTopicsModel:
    '''
    This model extracts topics from a prompt, given examples of this
    task done successfully and a list of topics.
    '''

    def __init__(self, config={}, model_name=None):
        self.model = PowerML(config)
        self.model_name = model_name

    def fit(self, examples, topics: list[str]):
        prefix = "List of topics we should consider extracting from messages:"
        example_string = prefix + "\n" + "\n".join(topics)

        for example in examples:
            new_string = "\n\nMessage: " + example["example"]
            new_string += "\nExtract the relevant topics from the above message:"
            for label in example["labels"]:
                new_string += "\n-" + label

            if len(example_string) + len(new_string) > MAX_TEMPLATE_TOKENS:
                break

            example_string += new_string

        suffix = """
Message: {{input}}
Extract the relevant topics from the above message:
-"""
        example_string += suffix

        new_model = self.model.fit(
            [example_string], model="text-davinci-003")

        logger.debug("Got new model: " + new_model["model_name"])
        # Note: model_name is also stored in the PowerML class.
        # This step is no longer strictly necessary unless multiple models are
        # being used or you wish to explicitly switch between models.
        self.model_name = new_model["model_name"]

    def predict(self, prompt: str):
        if self.model_name is None:
            result = self.model.predict(prompt)
        else:
            result = self.model.predict(prompt, model=self.model_name)

        return self.__post_process(result)

    def __post_process(self, topics):
        return [topic.strip() for topic in topics.split("\n-")]
