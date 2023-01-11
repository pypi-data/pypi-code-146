from powerml import PowerML
import re
from collections import Counter
import random
from tqdm import tqdm
import sys
import os

from powerml.model.PowerML import MAX_TOTAL_TOKENS


class CreateTopicsModel:
    '''
    This model removes duplicates and attempts to generate topics relevant
    to topic_type.
    '''

    def __init__(
            self,
            config={},
            num_subsamples=87,
            max_output_tokens=256,):
        # This is a hack to silence printed message on import
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        from transformers import GPT2Tokenizer
        from transformers.utils import logging
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        self.model = PowerML(config)
        self.create_model_name = "unblocked/create-topics/v2"
        self.messages = []
        self.num_subsamples = num_subsamples
        self.sample_size = 20
        self.max_output_tokens = max_output_tokens
        self.memo_topics = {}
        self.memo_top_topics = {}
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        logging.set_verbosity(40)

    def fit(self, documents, topic_type):
        self.topic_type = topic_type
        self.messages = documents
        random.shuffle(self.messages)
        self.num_samples = len(self.messages)
        if self.num_subsamples * self.sample_size > self.num_samples:
            self.num_subsamples = self.num_samples // self.sample_size
            self.num_subsamples += 1 if len(
                self.messages) % self.sample_size else 0

    def predict(self):
        # If get_topics has been called on the same messages array
        # Then use the previous results
        hash_docs = hash(frozenset(self.messages))
        if hash_docs in self.memo_topics:
            return self.memo_topics[hash_docs]

        sample_index = 0
        topic_counter = Counter()
        print("Learning topics...")
        for _ in tqdm(range(self.num_subsamples), ncols=0):
            if sample_index > self.num_samples:
                break
            examples, sample_index = self.__subsample(
                self.messages, sample_index, self.sample_size)
            prompt = self.__prompt_format(self.topic_type)
            prompt = self.__add_examples(examples, prompt)
            output = self.model.predict(
                prompt, max_tokens=self.max_output_tokens, temperature=0.7, model=self.create_model_name)
            topics = self.__parse_output(output)
            topic_counter.update(topics)
            sorted_topics = self.__sort_topics(topic_counter)
        topics = self.__get_topics(sorted_topics)
        self.memo_topics[hash_docs] = topics
        top_topics = self.__get_top_topics(sorted_topics)
        self.memo_top_topics[hash_docs] = top_topics
        return topics

    def __count_tokens(self, string):
        return len(self.tokenizer(string)['input_ids'])

    def __prompt_format(self, topic_type):
        prompt_dict = {"{{topic_type}}": topic_type}
        for i in range(self.sample_size):
            key = "{{example" + str(i+1) + "}}"
            prompt_dict[key] = ""
        return prompt_dict

    def __add_examples(self, examples, prompt, max_total_tokens=MAX_TOTAL_TOKENS):
        prompt_dict = prompt
        for i, example in enumerate(examples):
            key = "{{example" + str(i+1) + "}}"
            prompt_dict[key] = example
            if self.__count_tokens(str(prompt_dict)) < max_total_tokens - self.max_output_tokens:
                continue
            else:
                break
        return prompt_dict

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

    def __subsample(self, data, start_index, sample_size):
        # Assume data is pre-shuffled
        end_index = start_index + sample_size
        return data[start_index:end_index], end_index

    def __sort_topics(self, topic_counter):
        return sorted(topic_counter.items(), key=lambda x: x[1], reverse=True)

    def __get_topics(self, sorted_topics):
        # Return and save all topics
        return [elt for elt, _ in sorted_topics]

    def __get_top_topics(self, sorted_topics):
        # Return and save all topics that have more than count 1
        return [elt for elt, count in sorted_topics if count > 1]
