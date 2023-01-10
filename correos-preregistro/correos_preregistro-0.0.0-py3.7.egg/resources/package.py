from dataclasses import dataclass


@dataclass
class Package:
    weight: int
    postage_type: str = "FP"
    product_code: str = "S0132"
    delivery_modality: str = "ST"
    weight_type: str = "R"
