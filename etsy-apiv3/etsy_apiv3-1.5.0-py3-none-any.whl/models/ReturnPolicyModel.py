from typing import Optional
from pydantic import BaseModel


class ReturnPolicy(BaseModel):
    return_policy_id: int
    shop_id: int
    accepts_returns: bool
    accepts_exchanges: bool
    return_deadline: Optional[int] = None
    