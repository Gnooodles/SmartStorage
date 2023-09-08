from typing import Protocol


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
