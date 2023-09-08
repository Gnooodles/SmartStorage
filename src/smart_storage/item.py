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


@dataclass
class MissingItem:
    "Represent the missing item with the difference between threshold and quantity"
    barcode: str
    difference: int
