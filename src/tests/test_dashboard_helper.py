from smart_storage.dashboard_helper import add_missing_to_list, update_row
from smart_storage.magazzino import Magazzino
from smart_storage.lista_spesa import ListaSpesa
from .test_magazzino import mock_prodotti
from smart_storage.item import Item, StorageItem
import os

MOCK_PATH_MAGAZZINO = "src/tests/mock_magazzino.db"
MOCK_PATH_LISTA_SPESA = "src/tests/mock_lista_spesa.db"


def test_add_missing_to_list():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    mock_lista_spesa = ListaSpesa(MOCK_PATH_LISTA_SPESA, mock_prodotti)
    mock_magazzino.add_item("001")
    mock_magazzino.update_threshold("001", 2)
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    expected_items = []
    expected_items.append(Item("001", "test", 1))
    assert mock_lista_spesa.get_items() == expected_items
    os.remove(MOCK_PATH_LISTA_SPESA)
    os.remove(MOCK_PATH_MAGAZZINO)


def test_add_missing_to_list_multiple():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    mock_lista_spesa = ListaSpesa(MOCK_PATH_LISTA_SPESA, mock_prodotti)
    mock_magazzino.add_item("001")
    mock_magazzino.add_item("001")
    mock_magazzino.update_threshold("001", 3)
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    expected_items = []
    expected_items.append(Item("001", "test", 1))
    assert mock_lista_spesa.get_items() == expected_items
    os.remove(MOCK_PATH_LISTA_SPESA)
    os.remove(MOCK_PATH_MAGAZZINO)


def test_add_missing_to_list_multiple_items():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    mock_lista_spesa = ListaSpesa(MOCK_PATH_LISTA_SPESA, mock_prodotti)
    mock_magazzino.add_item("001")
    mock_magazzino.add_item("002")
    mock_magazzino.update_threshold("001", 2)
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    expected_items = []
    expected_items.append(Item("001", "test", 1))
    assert mock_lista_spesa.get_items() == expected_items
    os.remove(MOCK_PATH_LISTA_SPESA)
    os.remove(MOCK_PATH_MAGAZZINO)


def test_add_missing_to_list_multiple_items_and_quantities():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    mock_lista_spesa = ListaSpesa(MOCK_PATH_LISTA_SPESA, mock_prodotti)
    mock_magazzino.add_item("001")
    mock_magazzino.add_item("001")
    mock_magazzino.add_item("002")
    mock_magazzino.update_threshold("001", 3)
    mock_magazzino.update_threshold("002", 20)
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    expected_items = []
    expected_items.append(Item("001", "test", 1))
    expected_items.append(Item("002", "test", 19))
    assert mock_lista_spesa.get_items() == expected_items
    os.remove(MOCK_PATH_LISTA_SPESA)
    os.remove(MOCK_PATH_MAGAZZINO)


def test_update_row():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    mock_magazzino.add_item("001")
    mock_magazzino.update_threshold("001", 3)
    update_row(mock_magazzino, "001", "test test", 5, 10)
    expected_items = []
    expected_items.append(StorageItem("001", "test test", 5, 10))
    assert mock_magazzino.get_items() == expected_items
    os.remove(MOCK_PATH_MAGAZZINO)


def test_update_row_not_present():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    update_row(mock_magazzino, "001", "test test", 5, 10)
    expected_items = []
    assert mock_magazzino.get_items() == expected_items
    os.remove(MOCK_PATH_MAGAZZINO)


def test_update_multiple_rows():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    mock_magazzino.add_item("001")
    mock_magazzino.add_item("002")
    mock_magazzino.add_item("003")
    update_row(mock_magazzino, "001", "", 1, 10)
    update_row(mock_magazzino, "002", "", 2, 20)
    update_row(mock_magazzino, "003", "", 3, 30)
    expected_items = []
    expected_items.append(StorageItem("001", "", 1, 10))
    expected_items.append(StorageItem("002", "", 2, 20))
    expected_items.append(StorageItem("003", "", 3, 30))
    assert mock_magazzino.get_items() == expected_items
    os.remove(MOCK_PATH_MAGAZZINO)
