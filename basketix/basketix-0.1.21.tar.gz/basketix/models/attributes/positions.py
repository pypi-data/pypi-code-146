from typing import Literal, get_args

Position = Literal['PG', 'SG', 'PF', 'SF', 'C']
Position_Enum = get_args(Position)
