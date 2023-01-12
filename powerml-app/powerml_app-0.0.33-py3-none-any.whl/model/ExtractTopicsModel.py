
from powerml import PowerML
import logging
import re
from powerml.model.PowerML import MAX_TEMPLATE_TOKENS

logger = logging.getLogger(__name__)


class ExtractTopicsModel:
    '''
    This model extracts topics from a prompt, given examples of this
    task done successfully and a list of topics.
    '''

    def __init__(self, config={}, model_name=None):
        self.model = PowerML(config)
        self.model_name = "unblocked/extract-topics/v2"

    def fit(self, examples, topics: list[str]):
        self.examples = examples
        self.topics = topics

    def predict(self, message: str):
        example_string = ""
        for example in self.examples:
            new_string = "\n\nMessage: " + example["example"]
            new_string += "\nExtract the relevant topics from the above message:"
            for label in example["labels"]:
                new_string += "\n-" + label

            if len(example_string) + len(new_string) > MAX_TEMPLATE_TOKENS:
                break

            example_string += new_string
        topic_string = "\n".join(self.topics)
        prompt = {
            "{{examples}}": example_string,
            "{{topics}}": topic_string,
            "{{input}}": message,
        }
        result = self.model.predict(prompt, model=self.model_name)

        return self.__post_process(result)

    def __post_process(self, topics):
        # TODO: replace with stop tokens
        results = re.split('\n-', topics)
        return [topic.strip().lstrip("-") for topic in results]
