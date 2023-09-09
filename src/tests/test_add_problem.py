from smart_storage.dashboard_helper import add_missing_to_list
from smart_storage.magazzino import Magazzino
from smart_storage.lista_spesa import ListaSpesa
from .test_magazzino import mock_prodotti
from smart_storage.item import Item, StorageItem
import os


MOCK_PATH_MAGAZZINO = "src/tests/mock_magazzino.db"
MOCK_PATH_LISTA_SPESA = "src/tests/mock_lista_spesa.db"


def test_add_missing_to_list_workflow():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    mock_lista_spesa = ListaSpesa(MOCK_PATH_LISTA_SPESA, mock_prodotti)
    # aggiungo 2 prodotti
    mock_magazzino.add_item("001")
    mock_magazzino.add_item("001")
    # ne rimuovo manualmente uno e quindi viene aggiunto alla lista
    mock_magazzino.remove_one_item("001")
    mock_lista_spesa.add_item("001")
    # aggiorno la soglia del prodotto a 10
    mock_magazzino.update_threshold("001", 10)
    # schiaccio il bottone per aggiungere i prodotti mancanti alla lista della spesa
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    # nella lista dovrebbero essercene 1 (aggiunto manualmente) + 9 (aggiunti dalla funzione sopra) = 10
    current_items = mock_lista_spesa.get_items()
    os.remove(MOCK_PATH_LISTA_SPESA)
    os.remove(MOCK_PATH_MAGAZZINO)
    assert current_items == [Item("001", "test", 10)]


def test_add_missing_to_list_workflow_with_less_treshold():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    mock_lista_spesa = ListaSpesa(MOCK_PATH_LISTA_SPESA, mock_prodotti)
    # aggiungo 2 prodotti
    mock_magazzino.add_item("001")
    mock_magazzino.add_item("001")
    # ne rimuovo manualmente uno e quindi viene aggiunto alla lista
    mock_magazzino.remove_one_item("001")
    mock_lista_spesa.add_item("001")
    # aggiorno la soglia del prodotto a 10
    mock_magazzino.update_threshold("001", 10)
    # schiaccio il bottone per aggiungere i prodotti mancanti alla lista della spesa
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    # nella lista dovrebbero essercene 1 (aggiunto manualmente) + 9 (aggiunti dalla funzione sopra) = 10
    # aggiorno nuovamente la soglia, abbassandola a 5
    mock_magazzino.update_threshold("001", 5)
    # schiaccio il bottone per aggiungere i prodotti mancanti alla lista della spesa
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    # nella lista dovrebbero essercede 1 (aggiunto manualmente) + 4 (aggiunti dalla funzione sopra) = 5
    current_items = mock_lista_spesa.get_items()
    os.remove(MOCK_PATH_LISTA_SPESA)
    os.remove(MOCK_PATH_MAGAZZINO)
    assert current_items == [Item("001", "test", 5)]

def test_add_missing_to_list_workflow_with_problem():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    mock_lista_spesa = ListaSpesa(MOCK_PATH_LISTA_SPESA, mock_prodotti)
    # aggiungo 2 prodotti
    mock_magazzino.add_item("001")
    mock_magazzino.add_item("001")
    # ne rimuovo manualmente uno e quindi viene aggiunto alla lista
    mock_magazzino.remove_one_item("001")
    mock_lista_spesa.add_item("001")
    # aggiorno la soglia del prodotto a 10
    mock_magazzino.update_threshold("001", 10)
    # schiaccio il bottone per aggiungere i prodotti mancanti alla lista della spesa
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    # nella lista dovrebbero essercene 1 (aggiunto manualmente) + 9 (aggiunti dalla funzione sopra) = 10
    assert mock_lista_spesa.get_items() == [Item("001", "test", 10)]
    # aggiorno nuovamente la soglia, alzandola a 20
    mock_magazzino.update_threshold("001", 20)
    # schiaccio il bottone per aggiungere i prodotti mancanti alla lista della spesa
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    # nella lista dovrebbero essercede 1 (aggiunto manualmente) + 19 (aggiunti dalla funzione sopra) = 20
    current_items = mock_lista_spesa.get_items()
    os.remove(MOCK_PATH_LISTA_SPESA)
    os.remove(MOCK_PATH_MAGAZZINO)
    assert current_items == [Item("001", "test", 20)]


def test_add_missing_to_list_workflow_with_problem_more_complicated():
    mock_magazzino = Magazzino(MOCK_PATH_MAGAZZINO, mock_prodotti)
    mock_lista_spesa = ListaSpesa(MOCK_PATH_LISTA_SPESA, mock_prodotti)
    # aggiungo 3 prodotti
    mock_magazzino.add_item("001")
    mock_magazzino.add_item("001")
    mock_magazzino.add_item("001")
    # ne rimuovo manualmente uno e quindi viene aggiunto alla lista
    mock_magazzino.remove_one_item("001")
    mock_lista_spesa.add_item("001")
    # aggiorno la soglia del prodotto a 10
    mock_magazzino.update_threshold("001", 10)
    # schiaccio il bottone per aggiungere i prodotti mancanti alla lista della spesa
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    # nella lista dovrebbero essercene 1 (aggiunto manualmente) + 8 (aggiunti dalla funzione sopra) = 9
    assert mock_lista_spesa.get_items() == [Item("001", "test", 9)]
    # aggiorno nuovamente la soglia, alzandola a 20
    mock_magazzino.update_threshold("001", 20)
    # schiaccio il bottone per aggiungere i prodotti mancanti alla lista della spesa
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    # nella lista dovrebbero essercene 1 (aggiunto manualmente) + 18 (aggiunti dalla funzione sopra) = 19
    assert mock_lista_spesa.get_items() == [Item("001", "test", 19)]
    # rimuovo un altro prodotto dal magazzino e quindi viene aggiunto alla lista
    mock_magazzino.remove_one_item("001")
    mock_lista_spesa.add_item("001")
    # nella lista dovrebbero essercene 2 (aggiunti manualmente) + 18 (aggiunti dalla funzione sopra) = 20
    assert mock_lista_spesa.get_items() == [Item("001", "test", 20)]
    # aggiorno la soglia abbassandola a 5
    mock_magazzino.update_threshold("001", 5)
    # schiacci il bottone per aggiungere i prodotti mancandi alla lista della spesa
    add_missing_to_list(mock_magazzino, mock_lista_spesa)
    # nella lista dovrebbero essercene 2 (aggiunti manualmente) + 4 (aggiunti dalla funzione sopra) = 6
    current_items = mock_lista_spesa.get_items()
    os.remove(MOCK_PATH_LISTA_SPESA)
    os.remove(MOCK_PATH_MAGAZZINO)
    assert current_items == [Item("001", "test", 6)]

