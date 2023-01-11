import json  # module to import from lib
import site  # built-in module to import
from typing import Any  # non-module to import from a module from lib
import numpy as np  # aliased module
from cinnaroll_internal.rollout_config import RolloutConfig
# non-module from 3rd party module - shadowed
from tensorflow.keras.models import Sequential  # noqa
# module from 3rd party module - shadowed
from tensorflow import keras  # noqa
import PIL.Image  # class from 3rd party lib imported with import module.Class
import PIL as AliasedPIL
import tensorflow.keras.models

from cinnaroll_internal.infer_func_deps_finder.deps_finder import build_deps_finder
from tests.infer_func_deps_finder.utils import assert_lines_of_string_in_string


class Config(RolloutConfig):
    @staticmethod
    def train_eval(model_object: Any) -> None:
        pass

    @staticmethod
    def infer(model_object: Any, input_data: str) -> str:
        def Sequential() -> str:  # noqa
            return "foo"

        class keras:  # noqa
            @staticmethod
            def Sequential() -> str:  # noqa
                return "foo"

        print(tensorflow.keras.models.load_model("savedModel"))
        print(PIL.Image.open(input_data))
        print(AliasedPIL.Image.open(input_data))
        print(Sequential())
        print(keras.Sequential())
        print(site.getsitepackages())
        print(np.array(input_data))
        x = json.loads(input_data)
        print(np.array(json.loads(input_data)))
        y = model_object.predict(x)
        output = {"output": int(y.argmax())}

        return json.dumps(output)


def check_building_infer_func_file_content() -> None:
    required_imports = """
import json
import site
from typing import Any
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
import PIL.Image
import PIL as AliasedPIL
import tensorflow.keras.models
"""
    infer_code = """
def infer(model_object: Any, input_data: str) -> str:
    def Sequential() -> str:
        return "foo"

    class keras:
        @staticmethod
        def Sequential() -> str:
            return "foo"

    print(tensorflow.keras.models.load_model("savedModel"))
    print(PIL.Image.open(input_data))
    print(AliasedPIL.Image.open(input_data))
    print(Sequential())
    print(keras.Sequential())
    print(site.getsitepackages())
    print(np.array(input_data))
    x = json.loads(input_data)
    print(np.array(json.loads(input_data)))
    y = model_object.predict(x)
    output = {"output": int(y.argmax())}

    return json.dumps(output)
"""
    config = Config(
        project_id="5zVm00n97",
        model_name=None,
        model_object=None,
        model_input_sample=None,
        infer_func_input_format="img",
        infer_func_output_format="json",
        infer_func_input_sample=None,
    )

    expect = "\n".join([required_imports, infer_code])

    deps_finder = build_deps_finder(None, config)

    got = deps_finder.get_infer_with_used_global_variables().output_file_content

    assert_lines_of_string_in_string(expect, got)


if __name__ == "__main__":
    check_building_infer_func_file_content()
