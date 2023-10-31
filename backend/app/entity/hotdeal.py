from dataclasses import dataclass

@dataclass
class Hotdeal:
    id: str
    title: str
    original_price: float
    currency_type: str
    price_to_krw: float
    store_link: str
    source_link: str
    is_done: bool
    is_blind: bool