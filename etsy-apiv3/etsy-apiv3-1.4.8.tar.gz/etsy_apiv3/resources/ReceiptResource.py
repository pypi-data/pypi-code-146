from dataclasses import dataclass
from typing import List

from etsy_apiv3.utils import EtsySession, Response
from etsy_apiv3.models import Receipt, ReceiptType, Transaction

@dataclass
class ReceiptResource:
    """
    Receipt Resource is the utility class to get receipts from Etsy
    
    """
    session: EtsySession
    
    def get_receipts(self, shop_id: int, limit=25, offset=0, type: ReceiptType = ReceiptType.UNSHIPPED) -> Response[Receipt]:
        """
        Get Shop Receipts By Shop ID And Receipt Type

        Args:
            
            shop_id (int): Your SHOP ID
            limit (int, optional): Limit Of Receipt Objects. Defaults to 25.
            offset (int, optional): How many receipts to skip. Defaults to 0.
            type (ReceiptType, optional): Receipt type to find. Defaults to ReceiptType.UNSHIPPED.

        Returns:
            Response[Receipt]: Create Response Object Derived from the Receipt Object from json
        """
        
        endpoint = f"shops/{shop_id}/receipts"
        
        params = {"limit": limit, "offset": offset}
        params.update(type)
        json = self.session.request(endpoint=endpoint, params=params)
        
        return Response[Receipt](**json)
    
    def get_receipt_by_id(self, shop_id: int, receipt_id: int) -> Receipt:
        """
        Find One Receipt By Shop ID And Receipt ID

        Args:
            shop_id (int): Your SHOP ID
            receipt_id (int): Receipt ID
            
        Returns:
            Receipt: Create Receipt Object from json
        """
        endpoint = f"shops/{shop_id}/receipts/{receipt_id}"
        json = self.session.request(endpoint=endpoint)
        
        return Receipt(**json)

    def create_shipment(self, shop_id: int, receipt_id: int, tracking_number: str, carrier_name: str, send_bcc: bool = True, note_to_buyer: str = "") -> Receipt:
        """
        Adds tracking information to the receipt object

        Args:
            shop_id (int): SHOP ID
            receipt_id (int): Target Receipt ID
            tracking_number (str): Tracking Number
            carrier_name (str): Carrier Name Ex: UPS
            send_bcc (bool, optional): Send Mail. Defaults to True.
            note_to_buyer (str, optional): Note To Buyer From Seller. Defaults to "".

        Returns:
            Receipt: Receipt Object from json
        """
        endpoint = f"shops/{shop_id}/receipts/{receipt_id}/tracking"
        
        data = {
            "tracking_code":tracking_number, "carrier_name":carrier_name,
            "send_bcc":send_bcc, "note_to_buyer":note_to_buyer
        }
        
        json = self.session.request(endpoint=endpoint, method="POST", data=data)
        return Receipt(**json)
    
    def update_shop_receipt(self, shop_id: int, receipt_id: int, was_shipped: bool = None, was_paid: bool = None) -> Receipt:
        endpoint = f"shops/{shop_id}/receipts/{receipt_id}"
        data = {
            "was_shipped": was_shipped,
            "was_paid": was_paid
        }
        response = self.session.request(endpoint, "PUT", data=data)
        return Receipt(**response)
    
    def get_transactions_by_listing(self, shop_id: int, listing_id: int, limit: int = 25, offset: int = 0) -> Response[Transaction]:
        endpoint = f"shops/{shop_id}/listings/{listing_id}/transactions"
        params = {
            "limit": limit,
            "offset": offset
        }
        response = self.session.request(endpoint, params=params)
        return Response[Transaction](**response)
    
    def get_transactions_by_receipt(self, shop_id: int, receipt_id: int) -> Response[Transaction]:
        endpoint = f"shops/{shop_id}/receipts/{receipt_id}/transactions"
        response = self.session.request(endpoint)
        return Response[Transaction](**response)
    
    def get_transaction_by_transaction_id(self, shop_id: int, transaction_id: int) -> Transaction:
        endpoint = f"shops/{shop_id}/transactions/{transaction_id}"
        response = self.session.request(endpoint)
        return Transaction(**response)
    
    def get_receipt_transactions_by_shop(self, shop_id: int, limit: int = 25, offset: int = 0) -> Response[Transaction]:
        endpoint = f"shops/{shop_id}/transactions"
        params = {
            "limit": limit,
            "offset": offset
        }
        response = self.session.request(endpoint, params=params)
        return Response[Transaction](**response)