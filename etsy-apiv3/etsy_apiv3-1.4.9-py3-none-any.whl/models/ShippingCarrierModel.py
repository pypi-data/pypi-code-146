from pydantic import BaseModel

class ShippingCarrierClasses(BaseModel):
    mail_class_key: str
    name: str

class ShippingCarrier(BaseModel):
    shipping_carrier_id: int
    name: str
    domestic_classes: ShippingCarrierClasses
    international_classes: ShippingCarrierClasses