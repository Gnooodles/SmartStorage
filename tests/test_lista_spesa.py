from src.lista_spesa import ListaSpesa
from src.prodotti import Prodotti
import os


MOCK_PATH = "tests/mock_lista_spesa.db"
PRODOTTI = Prodotti("prodotti.db")


def test_database_creation():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    assert os.path.isfile(MOCK_PATH)
    os.remove(MOCK_PATH)


def test_add_one_item():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.add_item("111111")
    expected_items = [("111111", "test", 1)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_add_one_item_empty():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.add_item("")
    expected_items = []
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_add_multiple_items():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.add_item("111111")
    lista_spesa.add_item("222222")
    expected_items = [("111111", "test", 1), ("222222", "test", 1)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_add_item_multiple_times():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.add_item("111111")
    lista_spesa.add_item("111111")
    lista_spesa.add_item("111111")
    expected_items = [("111111", "test", 3)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_get_items():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.add_item("111111")
    lista_spesa.add_item("222222")
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert len(current_items) == 2


def test_get_items_non_present():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert len(current_items) == 0


def test_erase_database():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.erase_database()
    assert not os.path.isfile(MOCK_PATH)


def test_get_item_quantity():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.add_item("111111")
    lista_spesa.add_item("111111")
    current_quantity = lista_spesa.get_item_quantity("111111")
    os.remove(MOCK_PATH)
    assert current_quantity == 2


def test_get_item_quantity_non_present():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    current_quantity = lista_spesa.get_item_quantity("111111")
    os.remove(MOCK_PATH)
    assert current_quantity == 0
    # FIXME se provo a fare get_item_quantity per un item che non c'è nel database mi ritorna None,
    # dato che la funzione dovrebbe ritornare un intero è opportuno gestire
    # il caso in cui l'item non esista ritornando 0


def test_remove_one_item():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.add_item("111111")
    lista_spesa.remove_one_item("111111")
    expected_items = []
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_remove_one_item_with_multiple():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.add_item("111111")
    lista_spesa.add_item("222222")
    lista_spesa.remove_one_item("111111")
    expected_items = [("222222", "test", 1)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_remove_one_item_where_there_are_multiple():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.add_item("111111")
    lista_spesa.add_item("111111")
    lista_spesa.remove_one_item("111111")
    expected_items = [("111111", "test", 1)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_remove_one_item_non_present():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.remove_one_item("111111")
    expected_items = []
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items


def test_remove_one_item_non_present_with_other_items():
    lista_spesa = ListaSpesa(MOCK_PATH, PRODOTTI)
    lista_spesa.add_item("222222")
    lista_spesa.add_item("222222")
    lista_spesa.add_item("333333")
    lista_spesa.remove_one_item("111111")
    expected_items = [("222222", "test", 2), ("333333", "test", 1)]
    current_items = lista_spesa.get_items()
    os.remove(MOCK_PATH)
    assert current_items == expected_items
