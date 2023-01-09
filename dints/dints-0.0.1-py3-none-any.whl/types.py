from datetime import datetime
from typing import List, Tuple, Type, Union



TimeseriesRow = Tuple[datetime, List[Union[str, int, float, bool, Type[None]]]]