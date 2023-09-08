from smart_storage.magazzino import Magazzino
from smart_storage.item import StorageItem
import os

MOCK_PATH = "src/tests/mock_magazzino.db"


class MockProdotti:
    def __init__(self, path: str) -> None:
        pass

    def get_name_from_barcode(self, barcode: str) -> str:
        return "test"

    def scrape_barcode_name(self, barcode: str) -> str:
        return "test"


mock_prodotti = MockProdotti("")


def test_database_creation():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    assert os.path.isfile(MOCK_PATH)
    os.remove(MOCK_PATH)


def test_add_one_item():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    expected_items = []
    expected_items.append(StorageItem("111111", "test", 1, 0))
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_add_one_item_empty():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("")
    expected_items = []
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_add_multiple_items():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    magazzino.add_item("222222")
    expected_items = []
    expected_items.append(StorageItem("111111", "test", 1, 0))
    expected_items.append(StorageItem("222222", "test", 1, 0))
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_add_item_multiple_times():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    magazzino.add_item("111111")
    magazzino.add_item("111111")
    expected_items = []
    expected_items.append(StorageItem("111111", "test", 3, 0))
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_get_items():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    magazzino.add_item("222222")
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert len(current_items) == 2


def test_get_items_non_present():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert len(current_items) == 0


def test_erase_database():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    magazzino.erase_database()
    assert magazzino.get_items() == []


def test_get_item_quantity():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    magazzino.add_item("111111")
    current_quantity = magazzino.get_item_quantity("111111")
    os.remove(MOCK_PATH)
    assert current_quantity == 2


def test_get_item_quantity_non_present():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    current_quantity = magazzino.get_item_quantity("111111")
    os.remove(MOCK_PATH)
    assert current_quantity == 0


def test_remove_one_item():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    magazzino.remove_one_item("111111")
    expected_items = []
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_remove_one_item_with_multiple():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    magazzino.add_item("222222")
    magazzino.remove_one_item("111111")
    expected_items = []
    expected_items.append(StorageItem("222222", "test", 1, 0))
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_remove_one_item_where_there_are_multiple():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    magazzino.add_item("111111")
    magazzino.remove_one_item("111111")
    expected_items = []
    expected_items.append(StorageItem("111111", "test", 1, 0))
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_remove_one_item_non_present():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.remove_one_item("111111")
    expected_items = []
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_remove_one_item_non_present_with_other_items():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("222222")
    magazzino.add_item("222222")
    magazzino.add_item("333333")
    magazzino.remove_one_item("111111")
    expected_items = []
    expected_items.append(StorageItem("222222", "test", 2, 0))
    expected_items.append(StorageItem("333333", "test", 1, 0))
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_update_threshold():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    magazzino.update_threshold("111111", 2)
    expected_items = []
    expected_items.append(StorageItem("111111", "test", 1, 2))
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_update_threshold_product_not_present():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.update_threshold("111111", 2)
    expected_items = []
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_update_threshold_product_not_present_with_other_products():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("222222")
    magazzino.add_item("222222")
    magazzino.add_item("333333")
    magazzino.update_threshold("111111", 2)
    magazzino.update_threshold("222222", 1)
    expected_items = []
    expected_items.append(StorageItem("222222", "test", 2, 1))
    expected_items.append(StorageItem("333333", "test", 1, 0))
    current_items = magazzino.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_get_missin_products_quantity():
    magazzino = Magazzino(MOCK_PATH, mock_prodotti)
    magazzino.add_item("111111")
    magazzino.add_item("222222")
    magazzino.update_threshold("111111", 5)
    expected_items = [
        {"barcode": "111111", "difference": 4},
    ]
    current_items = magazzino.get_missing_product_quantity()
    os.remove(MOCK_PATH)
    assert current_items == expected_items
