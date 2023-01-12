from dataclasses import dataclass
from typing import List, Optional
from etsy_apiv3.utils import EtsySession, Response
from etsy_apiv3.models import (
    Translation, Product, Offering, Listing,
    Inventory, ListingProperty, File, ListingImage,
    DraftListing, Taxonomy, ProductProperty, VariationImage,
    Video
)


@dataclass
class ListingResource:
    
    session: EtsySession
    
    def get_listing(self, listing_id: int, includes: str = "") -> Listing:
        """
        Retrieves a listing record by listing ID.

        Args:
            listing_id (int): Listing Id
            includes (str, optional): An enumerated string that attaches a valid association. Acceptable inputs are 'Shipping', 'Shop', 'Images', 'User', 'Translations' and 'Inventory'. Defaults to "".

        Returns:
            Listing: A Single Listing Object
        """
        endpoint = f"listings/{listing_id}"
        json = self.session.request(endpoint, params={"includes":includes})
        return Listing(**json)

    def find_all_active_listings(self, limit=25, offset=0, keywords="", sort_on="created", sort_order="desc", min_price=None, max_price=None, taxonomy_id=None, shop_location="US"):
        """
        Find All Active Listings By Keywords, Min price, Max Price Or Shop Location

        Args:
            limit (int, optional): Result Limit. Defaults to 25, Max 100.
            offset (int, optional): Result Offset. Defaults to 0.
            keywords (str, optional): Keywords For Active Listings. Defaults to "".
            sort_on (str, optional): Sort By Result. Defaults to "created".
            sort_order (str, optional): Sort By Order. Defaults to "desc".
            min_price (_type_, optional): Min Price. Defaults to None.
            max_price (_type_, optional): Max Price. Defaults to None.
            taxonomy_id (_type_, optional): Taxonomy Id. Defaults to None.
            shop_location (_type_, optional): Shop Location. Defaults to US.

        Returns:
            Response[Listing]: List of Listing Items
        """
        
        endpoint = f"listings/active"
        params = {
            "limit":limit, "offset":offset, "keywords":keywords, "sort_on":sort_on,
            "sort_order":sort_order, "min_price":min_price, "max_price":max_price,
            "taxonomy_id":taxonomy_id, "shop_location":shop_location
        }
        
        json = self.session.request(endpoint, params=params)

        return Response[Listing](**json)
    
    
    def find_all_active_listings_by_shop(self, shop_id: int, limit: int = 25, sort_on: str = "created", sort_order: str = "desc", offset: int = 0, keywords: str = ""):
        endpoint = f"shops/{shop_id}/listings/active"
        
        params = {"limit": limit, "sort_on": sort_on, "sort_order": sort_order,
                  "offset": offset, "keywords": keywords
        }
        
        response = self.session.request(endpoint, params=params)
        return Response[Listing](**response)
        
    def get_listings_by_receipt_id(self, shop_id: int, receipt_id: int, limit: int = 25, offset: int = 0) -> Response[Listing]:
        endpoint = f"shops/{shop_id}/receipts/{receipt_id}/listings"
        params = {"limit": limit, "offset": offset}
        
        response = self.session.request(endpoint, params=params)
        return Response[Listing](**response)
    
    def get_listing_properties(self, shop_id: int, listing_id: int):
        endpoint = f"shops/{shop_id}/listings/{listing_id}/properties"
        
        response = self.session.request(endpoint)
        return Response[ListingProperty](**response)
    
    def get_listing_property(self, listing_id: int, property_id: int):
        endpoint = f"listings/{listing_id}/properties/{property_id}"
        
        response = self.session.request(endpoint)
        return ListingProperty(**response)
    
    def get_listing_inventory(self, listing_id: int):
        endpoint = f"listings/{listing_id}/inventory"
        response = self.session.request(endpoint)
        return Inventory(**response)
    
    def update_listing(self, shop_id: int, listing_id: int, **kwargs):
        endpoint = f"shops/{shop_id}/listings/{listing_id}"
        response = self.session.request(endpoint, "PATCH", data=kwargs)
        return Listing(**response)
    
    def update_listing_inventory(self, listing_id: int, products: List[dict], price_on_property: Optional[List[int]] = None, quantity_on_property: Optional[List[int]] = None, sku_on_property: Optional[List[int]] = None):
        
        data = {
            "products":products
        }

        if price_on_property is not None:
            data["price_on_property"] = price_on_property
        
        if quantity_on_property is not None:
            data["quantity_on_property"] = quantity_on_property
        
        if sku_on_property is not None:
            data["sku_on_property"] = sku_on_property
            
        endpoint = f"listings/{listing_id}/inventory"
        response = self.session.request(endpoint, "PUT", json=data)
        return Inventory(**response)

    
    def get_listings_by_listing_ids(self, listing_ids: List[int], includes: str = ""):
        params = {
            "listing_ids":",".join(list(map(str, listing_ids))),
            "includes":includes
        }
        endpoint = "listings/batch"
        
        response = self.session.request(endpoint, params=params)
        return Response[Listing](**response)
    
    def get_listings_by_return_policy_id(self, return_policy_id: int, shop_id: int):
        endpoint = f"shops/{shop_id}/policies/return/{return_policy_id}/listings"
        response = self.session.request(endpoint)
        return Response[Listing](**response)
    
    def get_listings_by_shop_section_id(self, shop_id: int, shop_section_ids: List[int], limit: int = 25, offset: int = 0, sort_on: str = "created", sort_order: str = "desc"):
        endpoint = f"shops/{shop_id}/shop-sections/listings"
        params = {
            "shop_section_ids": shop_section_ids,
            "limit": limit,
            "offset": offset,
            "sort_on": sort_on,
            "sort_order": sort_order
        }
        
        response = self.session.request(endpoint, params=params)
        return Response[Listing](**response)
    
    def get_featured_listings_by_shop_id(self, shop_id: int, limit: int = 25, offset: int = 0):
        endpoint = f"shops/{shop_id}/listings/featured"
        params = {
            "limit": limit,
            "offset": offset
        }
        
        response = self.session.request(endpoint, params=params)
        
        return Response[Listing](**response)
    
    def get_listings_by_shop_id(self, shop_id: int, state: str = "active", limit: int = 25, offset: int = 0, sort_on: str = "created", sort_order: str = "desc", includes: List[str] = None) -> Response[Listing]:
            
        endpoint = f"shops/{shop_id}/listings"
        params = {
            "state": state,
            "limit": limit,
            "offset": offset,
            "sort_on": sort_on,
            "sort_order": sort_order,
        }
        if includes is not None:
            params.update({"includes":includes})
            
        response = self.session.request(endpoint, params=params)
        return Response[Listing](**response)
    
    def get_listing_offering_by_id(self, listing_id: int, product_id: int, product_offering_id: int) -> Offering:
        endpoint = f"listings/{listing_id}/products/{product_id}/offerings/{product_offering_id}"
        response = self.session.request(endpoint)
        return Offering(**response)
    
    def get_listing_product_by_id(self, listing_id: int, product_id: int) -> Product:
        endpoint = f"listings/{listing_id}/inventory/products/{product_id}"
        response = self.session.request(endpoint)
        return Product(**response)
    
    def get_listing_translation(self, shop_id: int, listing_id: int, language: str) -> Translation:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/translations/{language}"
        response = self.session.request(endpoint)
        return Translation(**response)
    
    def get_all_listing_files_by_id(self, shop_id: int, listing_id: int) -> Response[File]:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/files"
        response = self.session.request(endpoint)
        return Response[File](**response)
    
    def get_listing_file_by_id(self, shop_id: int, listing_id: int, listing_file_id: int) -> File:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/files/{listing_file_id}"
        response = self.session.request(endpoint)
        return File(**response)
    
    def upload_listing_file(self, shop_id: int, listing_id: int, listing_file_id: int, file: str, name: str, rank: int = 1):
        endpoint = f"shops/{shop_id}/listings/{listing_id}/files"
        response = self.session.request(endpoint, "POST", data={
            "listing_file_id": listing_file_id,
            "file": file,
            "name": name,
            "rank": rank
        })

        return File(**response)
    
    def delete_listing_file(self, shop_id: int, listing_id: int, listing_file_id: int) -> str:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/files/{listing_file_id}"
        
        response = self.session.request(endpoint, method="DELETE")
        return response
    
    def delete_listing_by_id(self, listing_id: int) -> str:
        endpoint = f"listings/{listing_id}"
        response = self.session.request(endpoint, "DELETE")
        return response
    
    def get_listing_image_by_id(self, listing_id: int, listing_image_id: int) -> ListingImage:
        endpoint = f"listings/{listing_id}/images/{listing_image_id}"
        response = self.session.request(endpoint)
        return ListingImage(**response)
    
    def get_listing_images_by_id(self, listing_id: int) -> Response[ListingImage]:
        endpoint = f"listings/{listing_id}/images"
        response = self.session.request(endpoint)
        return Response[ListingImage](**response)
    
    def delete_listing_image_by_id(self, shop_id: int, listing_id: int, listing_image_id: int) -> str:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/images/{listing_image_id}"
        response = self.session.request(endpoint, "DELETE")
        return response
    
    def get_listing_variation_images(self, shop_id: int, listing_id: int) -> Response[VariationImage]:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/variation-images"
        response = self.session.request(endpoint)
        return Response[VariationImage](**response)
        
    def update_variation_images(self, shop_id: int, listing_id: int, variation_images: List[VariationImage]) -> Response[VariationImage]:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/variation-images"
        data = {"variation_images": [image.dict() for image in variation_images]}
        response = self.session.request(endpoint, "POST", data=data)
        return Response[VariationImage](**response)
    
    
    def upload_listing_image(self, shop_id: int, listing_id: int, image: bytes, listing_image_id: int, rank: int = 1, overwrite: bool = False, is_watermarked: bool = False, alt_text: str = "") -> ListingImage:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/images"
        data = {
            "image": image,
            "listing_image_id": listing_image_id,
            "rank": rank,
            "overwrite": overwrite,
            "is_watermarked": is_watermarked,
            "alt_text": alt_text
        }
        response = self.session.request(endpoint, "POST", data=data)
        return ListingImage(**response)
    
    def upload_multiple_images_to_listing(self, shop_id: int, listing_id: int, images: List[bytes], overwrite: bool = False, is_watermarked: bool = False, alt_text: str = "") -> List[ListingImage]:
        response = self.get_listing_images_by_id(listing_id=listing_id)
        new_listing_image_id = response.results[-1].listing_image_id + 1
        uploaded_images = []
        for image in images:
            uploaded_listing_image = self.upload_listing_image(
                shop_id=shop_id, listing_id=listing_id, image=image,
                listing_image_id=new_listing_image_id, rank=new_listing_image_id, overwrite=overwrite,
                is_watermarked=is_watermarked, alt_text=alt_text)
            uploaded_images.append(uploaded_listing_image)
            new_listing_image_id += 1
        
        return uploaded_images
    
    def get_listing_video(self, listing_id: int, video_id: int) -> Video:
        endpoint = f"listings/{listing_id}/videos/{video_id}"
        response = self.session.request(endpoint)
        return Video(**response)
    
    def get_listing_videos(self, listing_id: int) -> Response[Video]:
        endpoint = f"listings/{listing_id}/videos"
        response = self.session.request(endpoint)
        return Response[Video](**response)
    
    def upload_listing_video(self, shop_id: int, listing_id: int, video_id: int, video: bytes, name: str) -> Video:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/videos"
        data = {
            "video_id": video_id,
            "video": video,
            "name": name
        }
        response = self.session.request(endpoint, "POST", data=data)
        return Video(**response)

    def delete_listing_video(self, shop_id: int, listing_id: int, video_id: int) -> str:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/videos/{video_id}"
        response = self.session.request(endpoint, "DELETE")
        return response

    def create_draft_listing(self, shop_id: int, listing: DraftListing) -> Listing:
        endpoint = f"shops/{shop_id}/listings"
        response = self.session.request(endpoint, "POST", data=listing.dict())
        return Listing(**response)
    
    def get_buyer_taxonomy_nodes(self) -> Response[Taxonomy]:
        endpoint = "buyer-taxonomy/nodes"
        response = self.session.request(endpoint)
        return Response[Taxonomy](**response)
    
    def get_properties_by_buyer_taxonomy_id(self, taxonomy_id: int) -> ProductProperty:
        endpoint = f"buyer-taxonomy/nodes/{taxonomy_id}/properties"
        response = self.session.request(endpoint)
        return ProductProperty(**response)
    
    def get_seller_taxonomy_nodes(self):
        endpoint = "seller-taxonomy/nodes"
        response = self.session.request(endpoint)
        return Response[Taxonomy](**response)
    
    def get_properties_by_seller_taxonomy_id(self, taxonomy_id: int) -> ProductProperty:
        endpoint = f"seller-taxonomy/nodes/{taxonomy_id}/properties"
        response = self.session.request(endpoint)
        return ProductProperty(**response)
    
    
    