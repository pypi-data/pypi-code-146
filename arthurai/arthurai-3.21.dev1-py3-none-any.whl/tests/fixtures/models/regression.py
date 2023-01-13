import pandas as pd
import pytest

from arthurai import ArthurModel, ArthurAttribute
from arthurai.common.constants import InputType, OutputType, ValueType, Stage
from arthurai.core.attributes import AttributeCategory

from tests.fixtures.mocks import client

TABULAR_MODEL_ID = "tabby-mc-tabface"
TABULAR_MODEL_GROUP_ID = "groupy-mc-groupface"
INT_INPUT = "int_input"
INT_INPUT_ATTR = ArthurAttribute(name=INT_INPUT, value_type=ValueType.Integer, stage=Stage.ModelPipelineInput,
                                 categorical=True, position=0,
                                 categories=[AttributeCategory(value="1"), AttributeCategory(value="2")])
FLOAT_NONINPUT = "float_input"
FLOAT_NONINPUT_ATTR = ArthurAttribute(name=FLOAT_NONINPUT, value_type=ValueType.Float, stage=Stage.NonInputData,
                                      position=0, min_range=0.25, max_range=1.)
GROUND_TRUTH = "ground_truth"
PRED = "pred"
GROUND_TRUTH_ATTR = ArthurAttribute(name=GROUND_TRUTH, value_type=ValueType.Float, stage=Stage.GroundTruth,
                                    position=0, attribute_link=PRED, min_range=30., max_range=90.)
PRED_ATTR = ArthurAttribute(name=PRED, value_type=ValueType.Float, stage=Stage.PredictedValue, position=0,
                            attribute_link=GROUND_TRUTH, min_range=23., max_range=94.2)


MODEL_ATTRIBUTES = [INT_INPUT_ATTR, FLOAT_NONINPUT_ATTR, PRED_ATTR, GROUND_TRUTH_ATTR]

SAMPLE_DATAFRAME = pd.DataFrame({
    INT_INPUT: [1, 2, 1, 2, 1, 2],
    FLOAT_NONINPUT: [1., 0.5, 1., .25, .6, .9],
    PRED: [45.6, 94.2, 61.6, 23., 31.6, 80.3],
    GROUND_TRUTH: [30., 90., 60., 40., 40., 80.]
})

UNINITIALIZED_MODEL_DATA = {
        "partner_model_id": "",
        "input_type": InputType.Tabular,
        "output_type": OutputType.Regression,
        "display_name": "",
        "description": ""
}

MODEL_DATA_WITH_ATTRIBUTES = {
    **UNINITIALIZED_MODEL_DATA,
    "attributes": MODEL_ATTRIBUTES
}


@pytest.fixture
def batch_model(client):
    model_data = {
        **MODEL_DATA_WITH_ATTRIBUTES,
        'is_batch': True
    }
    model = ArthurModel(client=client.client, **model_data)
    model.id = TABULAR_MODEL_ID
    return model


@pytest.fixture
def initial_batch_model(client):
    model_data = {
        **UNINITIALIZED_MODEL_DATA,
        'is_batch': True
    }
    model = ArthurModel(client=client.client, **model_data)
    return model


@pytest.fixture
def unsaved_batch_model(client):
    model_data = {
        **MODEL_DATA_WITH_ATTRIBUTES,
        'is_batch': True
    }
    model = ArthurModel(client=client.client, **model_data)
    return model


@pytest.fixture
def streaming_model(client):
    model_data = {
        **MODEL_DATA_WITH_ATTRIBUTES,
        'is_batch': False
    }
    model = ArthurModel(client=client.client, **model_data)
    model.id = TABULAR_MODEL_ID
    return model
