from powerml import PowerML
import re
from collections import Counter
import random
from tqdm import tqdm
import sys
import os


class FilterTopicsModel:
    '''
    This model removes topics that are not in the
    topic_type category.
    '''

    def __init__(
            self,
            config={},):
        self.model = PowerML(config)
        self.filter_model_name = "unblocked/filter-topics"
        self.memo_filtered_topics = {}
        self.topics = []

    def fit(self, topics, topic_type):
        self.topic_type = topic_type
        self.topics = topics

    def predict(self):
        # If get_topics has been called on the same messages array
        # Then use the previous results
        hash_docs = hash(frozenset(self.topics))
        if hash_docs in self.memo_filtered_topics:
            return self.memo_filtered_topics[hash_docs]

        not_topics = self.__filter_top_topics(self.topics)
        filtered_top_topics = list(set(self.topics) - set(not_topics))

        self.memo_filtered_topics[hash_docs] = filtered_top_topics
        return filtered_top_topics

    def __filter_top_topics(self, topics_in_list):
        prompt = {
            "{{topics_in_list}}": f"{topics_in_list}", "{{topic_type}}": self.topic_type}
        output = self.model.predict(
            prompt, max_tokens=500, temperature=0.7,  model=self.filter_model_name)
        output = self.__parse_output(output)
        return output

    def __parse_output(self, output):
        list_pattern = re.compile(r"\d+\.\s")
        # include enumerated list prompt
        items = list_pattern.sub("", f'1. {output}')
        parsed = []
        for i in items.split('\n'):
            ii = i.split(',')
            stripped = [iii.strip().replace('.', '') for iii in ii if iii]
            parsed.extend(stripped)
        return parsed
