"""
TODO: look into how to use empty number when value is nan.
because nan is not empty and so it's difficult to manage.
write some tests for the instructions appliers.
introduce a number of instructions appliers and a tool for mobile testing
of instructions and generated embeddings (API).
develop more instructions.
"""

from . import instructions_map
from .interaction import InteractionEncoding
from .utils import sort_instructions

ERR_NUMBER = 0.00011
EMPTY_NUMBER = 0.00012


class ParseAndExecute(object):

    INTERACTIONS_KEY = "interactions"
    LABELS_KEY = "labels"
    TOKENIZE_KEY = "tokenize"
    IDENTIFIERS_KEY = "identifiers"
    RAW_INTERACTION_KEY = "raw_interactions"

    def __init__(self, data):
        self.instructions = self._group_and_sort_instructions(data)
        self.labels = self._retrieve_labels(data)
        self.tokenization_fields = self._retrieve_tokenization_fields(data)
        self.tokenize_instruction = instructions_map["Tokenize"]()
        self.identifiers = self._retrieve_identifiers(data)
        self.raw_interactions = self._retrieve_raw_interactions(data)

    def _group_and_sort_instructions(self, data):
        return sort_instructions(data)

    def _retrieve(self, data, key):
        if len(data) == 0:
            return {}
        return data.get(key, {})

    def _retrieve_labels(self, data):
        return self._retrieve(data, self.LABELS_KEY)

    def _retrieve_tokenization_fields(self, data):
        return self._retrieve(data, self.TOKENIZE_KEY)

    def _retrieve_identifiers(self, data):
        return self._retrieve(data, self.IDENTIFIERS_KEY)

    def _retrieve_raw_interactions(self, data):
        return self._retrieve(data, self.RAW_INTERACTION_KEY)

    def feed(self, values_dict):
        self.values = values_dict

    def _process_instruction(self, value, instruct):
        klass = instructions_map.get(instruct["instruct"])
        if not klass:
            return ERR_NUMBER
        # if instruction involves multiple fields.
        other_value = None

        instruct_params = instruct.get("params", {}).copy()
        # if params point to another field, get that field value too.
        if "field" in instruct_params:
            other_value = self.values.get(instruct_params["field"])
            del instruct_params["field"]

        obj = klass(**instruct_params)

        try:
            if other_value:
                # in case it involves two fields.
                res = obj.apply(value, other_value)
            else:
                res = obj.apply(value)
        except Exception as e:
            return ERR_NUMBER

        if res is None:
            return ERR_NUMBER
        elif isinstance(res, list):
            return res
        elif isinstance(obj, InteractionEncoding):
            return res
        else:
            return float(res)

    def _process_labels(self, object_name, object_values):
        labels = []

        labels_provided = self.labels.get(object_name)

        if labels_provided == None or len(labels_provided) == 0:
            return labels

        labels_provided = list(set(labels_provided))
        labels_from_api = object_values.get(self.LABELS_KEY, [])

        if len(labels_from_api) == 0:
            return labels

        for label in labels_provided:
            if label in labels_from_api:
                labels.append(label)

        return labels

    def _process_text_tokens(self, object_name, object_values):
        """
        generates one giant list of tokens for every object.
        does not keep text field seperated.
        """
        tokens = []

        field_names = self.tokenization_fields.get(object_name, [])

        if len(field_names) == 0:
            return tokens

        full_text = ""
        for field_name in field_names:
            if field_name in object_values:
                full_text += object_values[field_name]

        return self.tokenize_instruction.apply(full_text)

    def _process_identifiers(self, object_name, object_values):
        object_identifiers = {}
        identifiers_name = self.identifiers.get(object_name, [])

        if len(identifiers_name) == 0:
            return object_identifiers

        for identifier in identifiers_name:
            object_identifiers[identifier] = object_values.get(identifier, "")

        return object_identifiers

    def parse(self, object_name):
        if self.instructions.get(object_name) == None:
            return {}

        if object_name == self.INTERACTIONS_KEY:
            return {
                "interactions": self._process_interactions(),
                "raw_interactions": self._process_raw_interactions()
            }
        else:
            embedding = []
            labels = []
            identifiers = {}
            tokens = {"input_ids": [], "attention_mask": [], "len_": 0}

            # At this point, created_at is used on batch processing only
            created_at = self.values.get("beginai_created_at", None)

            if self.labels.get(object_name) is not None:
                labels = self._process_labels(object_name, self.values)

            if self.tokenization_fields.get(object_name) is not None:
                tokens = self._process_text_tokens(object_name, self.values)

            if self.identifiers.get(object_name) is not None:
                identifiers = self._process_identifiers(
                    object_name, self.values)

            for instruct in self.instructions.get(object_name.lower()):
                chains = instruct.get("_chains", None)
                value = self.values.get(instruct["f_id"].lower())

                if not value and (value != 0 and instruct["instruct"] == "Boolean"):
                    embedding.append(ERR_NUMBER)
                    continue

                if chains:
                    for chain in chains:
                        chain_list = sorted(chain, key=lambda k: k["order"])
                        for item in chain_list:
                            value = self._process_instruction(value, item)
                        # last response in the chain is the return value.
                        res = value
                        embedding.append(res)
                else:
                    res = self._process_instruction(value, instruct)
                    embedding.append(res)

            return {
                "embedding": embedding,
                "labels": labels,
                "tokens": tokens,
                "identifiers": identifiers,
                "created_at": created_at,
            }

    def _process_raw_interactions(self):
        object_raw_interactions = {}
        for object_key in self.values.keys():
            available_raw_interactions = self.raw_interactions.get(
                object_key, [])

            if len(available_raw_interactions) == 0:
                continue

            object_raw_interactions[object_key] = {}

            for action_object in self.values[object_key]:
                actions = self.values[object_key][action_object]
                processed_raw_interactions = self._get_raw_interactions(
                    actions, available_raw_interactions)
                if len(processed_raw_interactions) > 0:
                    object_raw_interactions[object_key][action_object] = processed_raw_interactions

        return object_raw_interactions

    def _get_raw_interactions(self, actions, raw_interactions):
        processed = []

        if len(actions) == 0 or len(raw_interactions) == 0:
            return processed

        # `actions` contains a list of dictionaries with the action and when was created_at
        for entry in actions:
            action = entry["value"].upper()
            if action in raw_interactions:
                processed.append({
                    "value": action,
                    "created_at": entry["created_at"]
                })

        return processed

    def _process_interactions(self):
        embeddings_per_object = {}
        for object_key in self.values.keys():
            instruction = next(
                (item for item in self.instructions[self.INTERACTIONS_KEY] if item["_with_object"] == object_key), None)

            if instruction is None:
                continue

            embeddings_per_object[object_key] = {}

            for action_object in self.values[object_key]:
                actions = []
                for entry in self.values[object_key][action_object]:
                    actions.append(entry['value'])

                result = self._process_instruction(actions, instruction)

                embeddings_per_object[object_key][action_object] = result

        return embeddings_per_object
