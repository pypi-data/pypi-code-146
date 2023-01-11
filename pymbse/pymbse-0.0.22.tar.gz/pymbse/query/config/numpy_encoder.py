import json
from typing import Any, Union

import numpy as np  # type: ignore


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Union[int, float, list, Any]:
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return json.JSONEncoder.default(self, obj)
