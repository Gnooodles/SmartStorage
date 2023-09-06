import streamlit as st
from smart_storage.lista_spesa import ListaSpesa
from smart_storage.prodotti import Prodotti
from smart_storage.magazzino import Magazzino

st.set_page_config(page_title="Smart Storage", layout="wide")
st.title("Shopping list")
prodotti = Prodotti("prodotti.db")
magazzino = Magazzino("magazzino.db", prodotti)

# fetch database
lista_spesa = ListaSpesa("listaspesa.db", prodotti, magazzino)

if st.button("Remove list"):
    lista_spesa.erase_database()

items: list = lista_spesa.get_items()

for item in items:
    checked = st.checkbox(
        f"Item: {item[1]} - Quantity: {item[2]} - Thresh: {item[3]}", value=False, key=item[0]
    )
