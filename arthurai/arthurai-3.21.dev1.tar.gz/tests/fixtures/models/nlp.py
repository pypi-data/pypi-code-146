import pytest
import pandas as pd
from arthurai import ArthurAttribute, ArthurModel
from arthurai.common.constants import InputType, OutputType, ValueType, Stage
from arthurai.core.attributes import AttributeCategory
from tests.fixtures.models.multiclass import DOG_PRED, CAT_PRED, GROUND_TRUTH, UNLINKED_CAT_PRED, UNLINKED_DOG_PRED


INPUT_TEXT = ["hello there", "hi", "what's up", "yo", "cool", "cool beans"]
NLP_DATAFRAME = pd.DataFrame({"input_text": INPUT_TEXT,
                              "pred": [90, 80, 50, 31, 26, 18],
                              "gt": [95, 81, 42, 30, 30, 27]})


DOG_CLASS_STRING = "dog class"
CAT_CLASS_STRING = "cat_class"
NLP_CLASSIFICATION_DATAFRAME = pd.DataFrame({"input_text": INPUT_TEXT,
                                             DOG_PRED: [0.6, 0.8, 0.2, 0.45, 0.94, 0.12],
                                             CAT_PRED: [0.4, 0.2, 0.8, 0.65, 0.06, 0.88],
                                             GROUND_TRUTH: [DOG_CLASS_STRING, CAT_CLASS_STRING, DOG_CLASS_STRING, CAT_CLASS_STRING,
                                                            CAT_CLASS_STRING, DOG_CLASS_STRING]})

INPUT_TEXT_ATTR = ArthurAttribute(name='input_text',
                                  value_type=ValueType.Unstructured_Text,
                                  stage=Stage.ModelPipelineInput,
                                  # TODO: this seems like it should be false,
                                  #  but check that this field isn't used somewhere else where it needs to be true
                                  categorical=True,
                                  position=0)

GT_STRING_ATTR = ArthurAttribute(name=GROUND_TRUTH,
                                 value_type=ValueType.String,
                                 stage=Stage.GroundTruthClass,
                                 categorical=True,
                                 categories=[AttributeCategory(value=DOG_CLASS_STRING),
                                             AttributeCategory(value=CAT_CLASS_STRING)],
                                 position=0)

CLASSIFICATION_MODEL_ATTRIBUTES = [UNLINKED_CAT_PRED, UNLINKED_DOG_PRED, INPUT_TEXT_ATTR, GT_STRING_ATTR]

UNINITIALIZED_MODEL_DATA = {"partner_model_id": "test",
                            "client": None,
                            "input_type": InputType.NLP}


@pytest.fixture
def initial_nlp_regression_model():
    return ArthurModel(
        **UNINITIALIZED_MODEL_DATA,
        output_type=OutputType.Regression
    )


@pytest.fixture
def initial_nlp_classification_model():
    return ArthurModel(
        **UNINITIALIZED_MODEL_DATA,
        output_type=OutputType.Multiclass
    )
