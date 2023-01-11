import pandas as pd
from dataclasses import dataclass

@dataclass
class WindowSettings:
    in_memory_target: pd.DataFrame