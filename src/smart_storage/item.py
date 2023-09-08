from dataclasses import dataclass


@dataclass
class Item:
    "Represent a product item"
    barcode: str
    name: str
    quantity: int


@dataclass
class StorageItem(Item):
    threshold: int
