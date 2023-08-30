import streamlit as st
from magazzino import Magazzino
from lista_spesa import ListaSpesa


# st.set_page_config(layout="wide", page_title="Smart Storage")
st.title("Shopping list")

# fetch database
magazzino = Magazzino("magazzino.db")
items: list = magazzino.get_items()

for item in items:
    checked = st.checkbox(f"Item: {item[0]} - Quantity: {item[2]}", value=False)
