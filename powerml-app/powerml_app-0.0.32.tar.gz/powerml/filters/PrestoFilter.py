from powerml import Filter
from powerml.utils.run_ai import run_ai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)


class PrestoFilter(Filter):
    '''
    This is a class that can be used to filter Presto data.
    '''

    def __init__(self):
        super().__init__('order for the conversation')
        self.filters = {**self.general_filters,
                        'No Item': self.__does_customer_order_any_item,
                        'Multiple Item': self.__does_customer_order_this_item,
                        'Short Convo': self.__remove_short_conversations,
                        'Monologue': lambda conversations: self.__filter_regex(r"(CX|AI)", conversations),
                        'Duplicate': self.__fuzzy_remove_duplicates
        }

    def __make_conversation_prompt(self, conversation):
        prompt = "This is a conversation where a customer orders the following items:\n"

        prompt += conversation["completion"]

        prompt += "\n\nConversation:\n"
        prompt += conversation["prompt"] + "\n"

        return prompt

    def __make_yes_no_question_prompt(self, example, question):
        prompt = self.__make_conversation_prompt(example)

        prompt += question + " Answer Yes or No. Answer:"

        if "is_yes" in example:
            if example["is_yes"]:
                prompt += " Yes\n\n"
            else:
                prompt += " No\n\n"

        return prompt

    def __trim_end(self, string):
        if len(string) > 4096:
            return string[:4096]

        return string
    
    def __answer_yes_no_question(self, prompt, allowed_tokens):
        logger.debug("Question: " + self.__trim_end(prompt))

        if allowed_tokens is None:
            result = run_ai(prompt, model="EleutherAI/pythia-6.7b-deduped", max_tokens=1)
        else:
            result = run_ai(prompt, model="EleutherAI/pythia-6.7b-deduped", max_tokens=1, allowed_tokens=[" No", " Yes"] + allowed_tokens)

        logger.debug("Answer: " + result)

        if result.lower().strip().find("yes") == 0:
            return True

        return False

    def __filter_question(self, question, conversations, examples, allowed_tokens = []):
        filtered_conversations = []

        for conversation in conversations:
            prompt = ""

            for example in examples:
                prompt += self.__make_yes_no_question_prompt(example, question)

            prompt += self.__make_yes_no_question_prompt(conversation, question)

            answer = self.__answer_yes_no_question(prompt, allowed_tokens)

            if answer:
                filtered_conversations.append(conversation)

        logger.debug("Passing filter " + str(len(filtered_conversations)) + " / " +
            str(len(conversations)) + " - " + question)

        return filtered_conversations

    def __does_customer_order_any_item(self, conversations):
        examples = [
            {
                "prompt" : "AI1: <welcome>\nAI2: Can I get you an iced drink today?\nCX: Yeah.\nAI2: Got it.\nAI1: What can we make fresh for your today?\nCX: I want a Bean & Cheese Burrito with Green sauce.\nAI1: Got it.\nAI2: Can I get a Bean & Cheese Burrito with green sauce?\nAI1: Sure.\nAI2: Got it..",
                "completion" : "1x Bean & Cheese Burrito with Green Sauce",
                "is_yes" : True
            },
            {
                "prompt" : "AI1: <welcome>\nCX1: I'm sorry, I'm not sure what you're saying.\nAI1: Can I get you an icked cold drink today?\nCX1: I'm sorry. I'm not sure what you're asking.\nAI1: Can I order you an icked cold drink today.\nCX1: I'm sorry I'm not sure what you're talking about.\nAI1: Can I please get you an icked cold drink.\nCX1: I'm not sure what you're trying to say.\nAI1: Can I have an icked cold drink.",
                "completion" : "1x Bean & Cheese Burrito with Green Sauce",
                "is_yes" : False
            },
            {   "prompt": "\nCX: Hello.\nAI (reading back): <welcome>\nCX: I'm sorry.\nAI: Order when ready.\nCX: I'm sorry. I'm sorry.\nAI: Okay.\nCX: I'm sorry, I'm sorry.\nAI: I'm sorry.\nCX: I'm sorry I'm sorry.\nAI: You're sorry?\nCX: I'm sorry. You're sorry?\nAI: I'm sorry. I'm so sorry.\nCX: I'm so sorry.\nAI: I'm so sorry.\nCX (reading back): I'm sorry",
                "completion": "1x Bean & Cheese Burrito with Green Sauce",
                "is_yes" : False
            }
        ]

        return self.__filter_question("Does the customer order any item?", conversations, examples, None)

    def __does_customer_order_this_item(self, conversations):
        examples = [
            {
                "prompt" : "\nCX: <welcome>\nAI: Ohh.. Like it?.\nCX: Yeah.\nAI: Okay, I'll have a large French fry.\nCX: Okay, I'll have a medium French fry.\nAI: Okay, I have it.\nCX: Can I get a large French fry?\nAI: Okay, I have that.\nCX: Can I get an iced cold drink?\nAI: Okay, I'll get you a large Sprite.\nCX: Okay, I have it. What else?\nAI: What else?\nCX: What's that?\n",
                "completion" : "1x Bean & Cheese Burrito with Green Sauce",
                "is_yes" : False
            },
            {
                "prompt": "\nCX: I'm sorry, I don't understand.\nAI: What would you like?\nCX: The Del Taco.\nAI: What would you prefer?\nCX: The Del Tako.\nAI: What would you rather have?\nCX: The Del Tato.\nAI: What would you have?\nCX: The Del Tac.\nAI: What would you order?\nCX: The Del Tacoo.\nAI: What would you want?\nCX: The Del Tacu.\nAI: What would you choose?\nCX: The Del Tacuu.\nAI: What",
                "completion": "1x The Del Taco",
                "is_yes" : True
            },
            {
                "prompt": "CX: Can I get you a Sprite?\nAI: Sure, I'll have a Sprite.\nCX: Can I get you Sprite?\nAI: Sure.\nCX: Can I get Sprite?\nAI: Sure..\nCX: Can I get Spray?\nAI: Sure..",
                "completion": "1x Bean & Cheese Burrito with Green Sauce",
                "is_yes" : False
            },
            {
                "prompt" : "AI1: <welcome>\nAI2: Can I get you an iced drink today?\nCX: Yeah.\nAI2: Got it.\nAI1: What can we make fresh for your today?\nCX: I want a Bean & Cheese Burrito with Green sauce.\nAI1: Got it.\nAI2: Can I get a Bean & Cheese Burrito with green sauce?\nAI1: Sure.\nAI2: Got it..",
                "completion" : "1x Bean & Cheese Burrito with Green Sauce",
                "is_yes" : True
            },
            {
                "prompt": "CX: <welcome>\nAI: Hi, can I help you?\nCX: Yes, I'd like to talk to a live person.\nAI: Okay, I'll be right back.",
                "completion": "1x Bean & Cheese Burrito with Green Sauce",
                "is_yes" : False
            }

        ]

        return self.__filter_question("Does the customer order only the one item?", conversations, examples, None)

    def __remove_short_conversations(self, conversations):

        filtered_conversations = []

        for conversation in conversations:
            turns = conversation["prompt"].count(":")

            if turns > 4:
                filtered_conversations.append(conversation)

        logger.debug("Passing filter " + str(len(filtered_conversations)) + " / " +
            str(len(conversations)) + " - too short")

        return filtered_conversations
    
    def __filter_regex(self, regex, conversations):
        filtered_conversations = []

        for conversation in conversations:
            match = re.search(regex, conversation["prompt"])

            if match:
                filtered_conversations.append(conversation)

        logger.debug("Passing regex filter " + str(len(filtered_conversations)) + " / " +
            str(len(conversations)) + " - " + regex)

        return filtered_conversations
    
    def __fuzzy_remove_duplicates(self, conversations):
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        embeddings = []

        for conversation in tqdm(conversations):
            new_conversation = dict(conversation)
            new_conversation["embedding"] = model.encode(conversation["prompt"])
            embeddings.append(new_conversation)

        all_embeddings = np.concatenate(
            [np.expand_dims(conversation["embedding"], axis=0)
            for conversation in embeddings])

        all_similarities = cosine_similarity(all_embeddings)
        all_similarities -= np.identity(all_similarities.shape[0])

        to_remove = all_similarities > 0.9

        locations = np.where(to_remove)
        to_delete = set()

        for x, y in zip(locations[0], locations[1]):
            if x in to_delete:
                continue
            to_delete.add(y)

        filtered_embeddings = [conversation for index, conversation in
            enumerate(embeddings) if index not in to_delete]

        for conversation in filtered_embeddings:
            del conversation["embedding"]

        return filtered_embeddings

    def noise_filter(self, data, return_metrics=True):
        metrics = {}
        len_data = len(data)
        filtered_data_intersect = data
        for filter in self.filters:
            filtered_data = self.filters[filter](data)
            metrics[f'{filter} Noise'] = 1 - len(filtered_data) / len_data
            filtered_data_intersect = [datum for datum in filtered_data_intersect if datum in filtered_data]
        metrics['Total Noise'] = 1 - len(filtered_data_intersect) / len_data
        if return_metrics:
            return filtered_data_intersect, metrics
        return filtered_data_intersect