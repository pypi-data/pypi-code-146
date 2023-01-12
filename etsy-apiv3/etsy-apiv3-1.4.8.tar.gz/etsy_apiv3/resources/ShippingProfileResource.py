from dataclasses import dataclass
from typing import List, Optional
from etsy_apiv3.utils import EtsySession, Response
from etsy_apiv3.models import ShippingCarrier, ShippingProfile, ShippingProfileDestination, ShippingProfileUpgrade

@dataclass
class ShopResource:
    """
    Shop Resource Of Etsy Api V3.

    """
    session: EtsySession
    
    def get_shipping_carriers(self, origin_country_iso: str) -> Response[ShippingCarrier]:
        endpoint = "shipping-carriers"
        response = self.session.request(endpoint, params={"origin_country_iso": origin_country_iso})
        return Response[ShippingCarrier](**response)
    
    def get_shop_shipping_profiles(self, shop_id: int) -> Response[ShippingProfile]:
        endpoint = f"shops/{shop_id}/shipping-profiles"
        response = self.session.request(endpoint)
        return Response[ShippingProfile](**response)
    
    def get_shop_shipping_profile(self, shop_id: int, shipping_profile_id: int) -> ShippingProfile:
        endpoint = f"shops/{shop_id}/shipping-profiles/{shipping_profile_id}"
        response = self.session.request(endpoint)
        return ShippingProfile(**response)
    
    def get_shop_shipping_profile_destinations(self, shop_id: int, shipping_profile_id: int, limit: int = 25, offset: int = 0) -> Response[ShippingProfileDestination]:
        endpoint = f"shops/{shop_id}/shipping-profiles/{shipping_profile_id}/destinations"
        params = {
            "limit": limit,
            "offset": offset
        }
        response = self.session.request(endpoint, params=params)
        return Response[ShippingProfileDestination](**response)
    
    def get_shop_shipping_profile_upgrades(self, shop_id: int, shipping_profile_id: int) -> Response[ShippingProfileUpgrade]:
        endpoint = f"shops/{shop_id}/shipping-profiles/{shipping_profile_id}/upgrades"
        response = self.session.request(endpoint)
        return Response[ShippingProfileUpgrade](**response)
    
    def delete_shop_shipping_profile(self, shop_id: int, shipping_profile_id: int) -> str:
        endpoint = f"shops/{shop_id}/shipping-profiles/{shipping_profile_id}"
        response = self.session.request(endpoint, "DELETE")
        return response
    
    def delete_shop_shipping_profile_destination(self, shop_id: int, shipping_profile_id: int, shipping_profile_destination_id: int) -> str:
        endpoint = f"shops/{shop_id}/shipping-profiles/{shipping_profile_id}/destinations/{shipping_profile_destination_id}"
        response = self.session.request(endpoint, "DELETE")
        return response
    
    def delete_shop_shipping_profile_upgrade(self, shop_id: int, shipping_profile_id: int, upgrade_id: int) -> str:
        endpoint = f"shops/{shop_id}/shipping-profiles/{shipping_profile_id}/upgrades/{upgrade_id}"
        response = self.session.request(endpoint, "DELETE")
        return response
    
    def update_shop_shipping_profile(self, shop_id: int, shipping_profile_id: int, title: str, origin_country_iso: str, min_processing_time: int, max_processing_time: int, processing_time_unit: str = "business_days", origin_postal_code: str = None) -> ShippingProfile:
        endpoint = f"shops/{shop_id}/shipping-profiles/{shipping_profile_id}"
        data = {
            "title": title,
            "origin_country_iso": origin_country_iso,
            "min_processing_time": min_processing_time,
            "max_processing_time": max_processing_time,
            "processing_time_unit": processing_time_unit
        }
        if origin_postal_code:
            data.update({"origin_postal_code": origin_postal_code})
        
        response = self.session.request(endpoint, "PUT", data=data)
        return ShippingProfile(**response)
    
    def update_shop_shipping_profile_destination(self, shop_id: int, shipping_profile_id: int, shipping_profile_destination_id: int, primary_cost: Optional[float] = None, secondary_cost: Optional[float] = None, destination_country_iso: Optional[str] = None, destination_region: Optional[str] = "none", shipping_carrier_id: Optional[int] = None, mail_class: Optional[str] = None, min_delivery_days: Optional[int] = None, max_delivery_days: Optional[int] = None) -> ShippingProfileDestination:
        endpoint = f"shops/{shop_id}/shipping-profiles/{shipping_profile_id}/destinations/{shipping_profile_destination_id}"
        data = {
            "primary_cost": primary_cost,
            "secondary_cost": secondary_cost,
            "destination_country_iso": destination_country_iso,
            "destination_region": destination_region,
            "shipping_carrier_id": shipping_carrier_id,
            "mail_class": mail_class,
            "min_delivery_days": min_delivery_days,
            "max_delivery_days": max_delivery_days
        }
        response = self.session.request(endpoint, "PUT", data=data)
        return ShippingProfileDestination(**response)

    def update_shop_shipping_profile_upgrade(self, shop_id: int, shipping_profile_id: int, upgrade_id: int, upgrade_name: Optional[str] = None, type: str = "0", price: Optional[float] = None, secondary_price: Optional[float] = None, shipping_carrier_id: Optional[int] = None, mail_class: Optional[str] = None, min_delivery_days: Optional[int] = None, max_delivery_days: Optional[int] = None) -> ShippingProfileUpgrade:
        endpoint = f"shops/{shop_id}/shipping-profiles/{shipping_profile_id}/upgrades/{upgrade_id}"
        data = {
            "upgrade_name": upgrade_name,
            "type": type,
            "price": price,
            "secondary_price": secondary_price,
            "shipping_carrier_id": shipping_carrier_id,
            "mail_class": mail_class,
            "min_delivery_days": min_delivery_days,
            "max_delivery_days": max_delivery_days
        }
        response = self.session.request(endpoint, "PUT", data=data)
        return ShippingProfileUpgrade(**response)
    
    
        