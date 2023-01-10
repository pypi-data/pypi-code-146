from beginai.exec.embeddings.instructions.parse_and_execute import ParseAndExecute
from freezegun import freeze_time
import json


@freeze_time("2021-05-16")
def test_parse_instructions():
    instructions = json.loads("""
    {
        "instructions":{
            "user":[
                {
                    "_chains":[
                    [
                        {
                            "complexity":1,
                            "instruct":"Age",
                            "order":1,
                            "params":{

                            }
                        },
                        {
                            "complexity":1,
                            "instruct":"Slice",
                            "order":2,
                            "params":{
                                "maxv":100,
                                "minv":10,
                                "num_slices":10,
                                "skip_masking": false
                            }
                        }
                    ]
                    ],
                    "f_id":"userBirthDate"
                },
                {
                    "complexity":1,
                    "f_id":"userBirthDate",
                    "instruct":"Age",
                    "params":{

                    }
                }
            ]
        },
        "labels": {},
        "tokenize": {},
        "embedding_template": {
            "user": [
                "userBirthDate",
                "chain_instruction__Age__user__userBirthDate",
                "chain_instruction__Slice__user__userBirthDate"
            ]
        },
        "raw_interactions":{}
    }
    """)

    values = {
        "userbirthdate": "16-05-1991"
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("user")
    expected = {
        "embedding": [30.0, 3.0],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_parse_instructions_without_matching_id():
    instructions = json.loads("""
        {
            "instructions":{
                "user":[
                    {
                        "complexity":1,
                        "f_id":"userBirthDate",
                        "instruct":"Age",
                        "params":{

                        }
                    }
                ]
            },
            "labels": {},
            "tokenize": {},
            "embedding_template": {
                "user": [ "userBirthDate" ]
            },
            "raw_interactions":{}
        }
    """)

    values = {
        "userBio": "bio bio"
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("user")
    expected = {
        "embedding": [0.00011],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_parse_instructions_without_object_being_on_instructions():
    instructions = json.loads("""
        {
            "instructions":{
                "user":[
                    {
                        "complexity":1,
                        "f_id":"userBirthDate",
                        "instruct":"Age",
                        "params":{

                        }
                    }
                ]
            },
            "labels": {},
            "tokenize": {},
            "embedding_template": {
                "user": [ "userBirthDate" ]
            },
            "raw_interactions":{}
        }
    """)

    values = {
        "doesntexist": "bio bio"
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("doesntexistobject")
    expected = {}
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


@freeze_time("2021-05-16")
def test_parse_instructions_with_different_camel_case_than_provided():
    instructions = json.loads("""
        {
            "instructions":{
                "user":[
                    {
                        "complexity":1,
                        "f_id":"USERBIRTHDATE",
                        "instruct":"Age",
                        "params":{
                        }
                    }
                ]
            },
            "labels": {},
            "tokenize": {},
            "embedding_template": {
                "user": [ "USERBIRTHDATE" ]
            },
            "raw_interactions":{}
        }
    """)

    values = {
        "userbirthdate": "16-05-1991"
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("user")
    expected = {
        "embedding": [30.0],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_parse_instructions_with_interactions_only():
    instructions = json.loads("""{
        "instructions": {
            "interactions": [{
                    "instruct": "InteractionEncoding",
                    "complexity": 1,
                    "params": {
                        "sequence_map": { "like": 5, "dislike": 2, "_GB_EMPTY": 0.00011 }
                    },
                    "higher_order": 1,
                    "_with_object": "product"
                },
                {
                    "instruct": "InteractionEncoding",
                    "complexity": 1,
                    "params": {
                        "sequence_map": { "followed": 5, "report": 2, "_GB_EMPTY": 0.00011 }
                    },
                    "higher_order": 2,
                    "_with_object": "user"
                }
            ]},
            "labels": {},
            "tokenize": {},
            "embedding_template": {},
            "raw_interactions":{
                "product": ["LIKE", "DISLIKE"],
                "user": ["FOLLOWED", "REPORT"]
            }
        }
    """)

    values = {"product": {"10": [{"value": "like", "created_at": 1010}, {"value": "dislike", "created_at": 2020}], "20": [
        {"value": "dislike", "created_at": 2121}]}}

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("interactions")
    expected = {
        "interactions": {
            "product": {
                "10": {
                    "sent_bin": 2,
                    "sentiment": 5,
                    "label": "POSITIVE"
                },
                "20": {
                    "sent_bin": 1,
                    "sentiment": 2,
                    "label": "NEGATIVE"
                }
            }
        },
        "raw_interactions": {
            "product": {
                "10": [{'value': 'LIKE', 'created_at': 1010}, {'value': 'DISLIKE', 'created_at': 2020}],
                "20": [{'value': 'DISLIKE', 'created_at': 2121}]
            }
        }
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_parse_instructions_with_interaction_that_doesnt_exist():
    instructions = json.loads("""
    {
        "instructions": {
            "interactions": [
                    {
                        "instruct": "InteractionEncoding",
                        "complexity": 1,
                        "params": {
                            "sequence_map": { "like": 5, "dislike": 2, "_GB_EMPTY": 0.00011 }
                        },
                        "higher_order": 1,
                        "_with_object": "product"
                    },
                    {
                        "instruct": "InteractionEncoding",
                        "complexity": 1,
                        "params": {
                            "sequence_map": { "followed": 5, "report": 2, "_GB_EMPTY": 0.00011 }
                        },
                        "higher_order": 2,
                        "_with_object": "user"
                    }
                ]
            },
            "labels": {},
            "tokenize": {},
            "embedding_template": {},
            "raw_interactions":{
                "product": ["LIKE", "DISLIKE"],
                "user": ["FOLLOWED", "REPORT"]
            }
    }
    """)

    values = {
        "differentobjectthatdoesntexist": {
            "10": [{
                "value": "like",
                "created_at": 12345
            }],
            "20": [
                {"value": "dislike", "created_at": 10101}]
        },
        "product": {
            "10": [{"value": "like", "created_at": 321}]
        }
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("interactions")
    expected = {
        "interactions": {
            "product": {
                "10": {
                    "sent_bin": 2,
                    "sentiment": 5,
                    "label": "POSITIVE",
                }
            },
        },
        "raw_interactions": {
            "product": {
                "10": [{
                    "value": "LIKE",
                    "created_at": 321
                }]
            }
        }
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_parse_labels_that_exists():
    instructions = json.loads("""
    {
        "instructions":{
            "user":{}
        },
        "labels":{
            "user":[ "fake", "not_fake", "something" ],
            "product":[ "fruit", "shirt"
            ],
            "message":["something" ]
        },
        "tokenize":{},
        "raw_interactions":{}
    } """)

    values = {
        "user": {
            "labels": ["fake", "not_fake"]
        }
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values.get("user"))
    results = parse_and_execute.parse("user")
    expected = {
        "embedding": [],
        "labels": ["fake", "not_fake"],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0}
    }
    assert results["labels"].sort() == expected["labels"].sort()


def test_parse_labels_that_dont_exist():
    instructions = json.loads("""{
        "instructions":{
            "product": {}
        },
        "labels":{
            "product":[ "fruit", "shirt" ]
        },
        "tokenize":{},
        "raw_interactions":{}
    }""")

    values = {
        "product": {
            "labels": ["fake", "fruit"]
        }
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values.get("product"))
    results = parse_and_execute.parse("product")
    expected = {
        "embedding": [],
        "labels": ["fruit"],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_boolean_values():
    instructions = json.loads(""" {
        "instructions":{
            "home":[
                {
                    "instruct":"Boolean",
                    "complexity":1,
                    "params":{
                        "true":2,
                        "false":1,
                        "_GB_EMPTY": 0.00011
                    },
                    "f_id":"has_hottub"
                },
                {
                    "instruct":"Boolean",
                    "complexity":1,
                    "params":{
                        "true":2,
                        "false":1,
                        "_GB_EMPTY": 0.00011
                    },
                    "f_id":"has_true"
                }
            ]
        },
        "labels": {},
        "tokenize":{},
        "embedding_template": {
            "home": [
                "has_hottub",
                "has_true"
            ]
        },
        "raw_interactions":{}
    } """)

    values = {
        "has_hottub": 0,
        "has_true": 1
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("home")
    expected = {
        "embedding": [1.0, 2.0],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_tokenizer():
    instructions = json.loads(""" {
        "instructions":{
            "user":[],
            "interactions":[]
        },
        "labels": {},
        "tokenize":{
            "user":[ "name", "lastName"]
        },
        "raw_interactions":{}
    } """)

    values = {
        "name": "Jane",
        "lastName": "Doe"
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("user")
    expected = {
        "embedding": [],
        "labels": [],
        "tokens": {"input_ids": [101, 4869, 3527, 2063, 102, 0, 0], "attention_mask": [1, 1, 1, 1, 1, 0, 0], "len_": 5},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_tokenizer_when_property_is_not_provided():
    instructions = json.loads(""" {
        "instructions":{
            "user":[],
            "interactions":[]
        },
        "tokenize":{
            "user":[ "name", "lastName" ]
        },
        "labels": {},
        "identifiers": {},
        "raw_interactions":{}
    } """)

    values = {
        "name": "Jane"
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("user")
    expected = {
        "embedding": [],
        "labels": [],
        "tokens": {"input_ids": [101, 4869, 102, 0], "attention_mask": [1, 1, 1, 0], "len_": 3},
        "identifiers": {},
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_identifier_when_property_is_not_provided():
    instructions = json.loads(""" {
        "instructions":{
            "user":[],
            "interactions":[]
        },
        "identifiers":{
            "user":[ "user_id", "user_id_2" ]
        },
        "labels": {},
        "raw_interactions":{}
    } """)

    values = {
        "name": "Jane"
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("user")
    expected = {
        "embedding": [],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {
            "user_id": "",
            "user_id_2": ""
        },
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)


def test_identifier():
    instructions = json.loads(""" {
        "instructions":{
            "user":[],
            "interactions":[]
        },
        "identifiers":{
            "user":[ "user_id", "user_id_2" ]
        },
        "labels": {},
        "raw_interactions":{}
    } """)

    values = {
        "name": "Jane",
        "user_id": 1,
        "identifiers": {
            "user_id": "",
            "user_id_2": ""
        }
    }

    parse_and_execute = ParseAndExecute(instructions)
    parse_and_execute.feed(values)
    results = parse_and_execute.parse("user")
    expected = {
        "embedding": [],
        "labels": [],
        "tokens": {"input_ids": [], "attention_mask": [], "len_": 0},
        "identifiers": {
            "user_id": 1,
            "user_id_2": ""
        },
        "created_at": None
    }
    assert json.dumps(results, sort_keys=True) == json.dumps(
        expected, sort_keys=True)
