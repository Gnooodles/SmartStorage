from dataclasses import dataclass


@dataclass
class Item:
    "Represents a product item"
    barcode: str
    name: str
    quantity: int


@dataclass
class StorageItem(Item):
    "Represents an item used in the magazzino"
    threshold: int


@dataclass
class MissingItem:
    "Represents the missing item with the difference between threshold and quantity"
    barcode: str
    difference: int
