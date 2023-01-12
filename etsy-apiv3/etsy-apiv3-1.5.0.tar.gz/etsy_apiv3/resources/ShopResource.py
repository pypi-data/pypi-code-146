from dataclasses import dataclass
from typing import List, Optional
from etsy_apiv3.models import ProductionPartner, Shop, ShopSection
from etsy_apiv3.utils import EtsySession, Response

@dataclass
class ShopResource:
    """
    Shop Resource Of Etsy Api V3.

    """
    session: EtsySession
    
    def get_shop_by_id(self, shop_id: int):
        """
        Get Shop By Shop Id And Return A Shop Object

        Args:
            shop_id (int): Shop Id

        Returns:
            Shop: Shop Object
        """
        
        endpoint = f"shops/{shop_id}"
        response = self.session.request(endpoint)
        return Shop(**response)
    
    def find_shops(self, shop_name: str):
        """
        Find All Shops And Return Response Object
        
        Returns:
            Response: Return Response object of shop list 
        """
        endpoint = "shops"
        response = self.session.request(endpoint, params={"shop_name":shop_name})
        return Response[Shop](**response)

    def get_shop_by_owner_user_id(self, user_id: int):
        """
        Find Shop By Owner User Id And Return A Shop Object.

        Args:
            user_id (int): Shop Owner User Id

        Returns:
            Shop: Return A Shop Object
        """
        endpoint = f"users/{user_id}/shops"
        response = self.session.request(endpoint)
        return Shop(**response)
    
    def update_shop(self, shop_id: int, title: Optional[str] = None, announcement: Optional[str] = None, sale_message: Optional[str] = None, digital_sale_message: Optional[str] = None) -> Shop:
        data = {}
        if title:
            data.update({"title": title})
        if announcement:
            data.update({"announcement": announcement})
        if sale_message:
            data.update({"sale_message": sale_message})
        if digital_sale_message:
            data.update({"digital_sale_message": digital_sale_message})
            
        endpoint = f"shops/{shop_id}"
        response = self.session.request(endpoint, "PUT", data=data)
        return Shop(**response)
    
    def get_shop_production_partners(self, shop_id: int) -> List[ProductionPartner]:
        endpoint = f"shops/{shop_id}/production-partners"
        response = self.session.request(endpoint)
        return Response[ProductionPartner](**response)
    
    def get_shop_sections(self, shop_id: int) -> List[ShopSection]:
        endpoint = f"shops/{shop_id}/sections"
        response = self.session.request(endpoint)
        return Response[ShopSection](**response)
    
    def get_shop_section_by_id(self, shop_id: int, shop_section_id: int) -> ShopSection:
        endpoint = f"shops/{shop_id}/sections/{shop_section_id}"
        response = self.session.request(endpoint)
        return ShopSection(**response)
    
    def delete_shop_scetion_by_id(self, shop_id: int, shop_section_id: int) -> str:
        endpoint = f"shops/{shop_id}/sections/{shop_section_id}"
        response = self.session.request(endpoint, "DELETE")
        return response
    
    def create_shop_section(self, shop_id: int, title: str) -> ShopSection:
        endpoint = f"shops/{shop_id}/sections"
        response = self.session.request(endpoint, "POST", data={"title": title})
        return ShopSection(**response)
    
    def update_shop_section(self, shop_id: int, shop_section_id: int, title: str) -> ShopSection:
        endpoint = f"shops/{shop_id}/sections/{shop_section_id}"
        response = self.session.request(endpoint, "PUT", data={"title": title})
        return ShopSection(**response)
    
    
    