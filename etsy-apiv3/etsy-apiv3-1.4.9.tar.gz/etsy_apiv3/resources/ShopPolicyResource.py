from typing import Optional
from etsy_apiv3.utils import EtsySession, Response
from dataclasses import dataclass
from etsy_apiv3.models import ReturnPolicy
@dataclass
class ShopResource:
    """
    Shop Policy Resource Of Etsy Api V3.

    """
    session: EtsySession
    
    def get_shop_return_policies(self, shop_id: int) -> Response[ReturnPolicy]:
        endpoint = f"shops/{shop_id}/policies/return"
        response = self.session.request(endpoint)
        return Response[ReturnPolicy](**response)
    
    def get_shop_return_policy_by_id(self, shop_id: int, return_policy_id: int) -> ReturnPolicy:
        endpoint = f"shops/{shop_id}/policies/return/{return_policy_id}"
        response = self.session.request(endpoint)
        return ReturnPolicy(**response)
    
    def create_shop_return_policy(self, shop_id: int, accepts_returns: bool, accepts_exchanges: bool, return_deadline: Optional[int]) -> ReturnPolicy:
        endpoint = f"shops/{shop_id}/policies/return"
        data = {
            "accepts_returns": accepts_returns,
            "accepts_exchanges": accepts_exchanges
        }
        if return_deadline:
            data.update({"return_deadline": return_deadline})
        
        response = self.session.request(endpoint, "POST", data=data)
        return ReturnPolicy(**response)
    
    def update_shop_return_policy(self, shop_id: int, return_policy_id: int, accepts_returns: bool, accepts_exchanges: bool, return_deadline: Optional[int] = None) -> ReturnPolicy:
        endpoint = f"shops/{shop_id}/policies/return/{return_policy_id}"
        data = {
            "accepts_returns": accepts_returns,
            "accepts_exchanges": accepts_exchanges
        }
        if return_deadline:
            data.update({"return_deadline": return_deadline})
        
        response = self.session.request(endpoint, "PUT", data=data)
        return ReturnPolicy(**response)
    
    def delete_shop_return_policy(self, shop_id: int, return_policy_id: int) -> str:
        endpoint = f"shops/{shop_id}/policies/return/{return_policy_id}"
        response = self.session.request(endpoint, "DELETE")
        return response
    
    def consolidate_shop_return_policies(self, shop_id: int, source_return_policy_id: int, destination_return_policy_id: int) -> ReturnPolicy:
        endpoint = f"shops/{shop_id}/policies/return/consolidate"
        data = {
            "source_return_policy_id": source_return_policy_id,
            "destination_return_policy_id": destination_return_policy_id
        }
        response = self.session.request(endpoint, "POST", data=data)
        return ReturnPolicy(**response)
    
    