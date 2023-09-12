from typing import Protocol
from smart_storage.item import MissingItem


class ScraperInterface(Protocol):
    def get_name_from_barcode(self, barcode) -> str:
        ...


class ProductFinderInterface(Protocol):
    def __init__(self, path: str, scraper: ScraperInterface) -> None:
        ...

    def get_name_from_barcode(self, barcode: str) -> str:
        ...

    def scrape_barcode_name(self, barcode: str) -> str:
        ...


class ListaSpesaInterface(Protocol):
    def add_item(self, barcode: str, quantity: int = 1) -> None:
        ...

    def remove_one_item(self, barcode: str, quantity: int = 1) -> None:
        ...

    def get_item_quantity(self, barcode: str) -> int:
        ...

    def update_threshold(self, barcode: str, new_threshold: int) -> None:
        ...

    def delete_item(self, barcode: str) -> None:
        ...

    def update_item(
        self, barcode: str, name: str, quantity: int, threshold: int
    ) -> None:
        ...


class MagazzinoInterface(Protocol):
    def get_missing_products_quantity(self) -> list[MissingItem]:
        ...

    def delete_item(self, barcode: str) -> None:
        ...

    def update_item(
        self, barcode: str, name: str, quantity: int, threshold: int
    ) -> None:
        ...
