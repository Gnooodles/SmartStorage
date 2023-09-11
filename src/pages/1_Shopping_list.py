import streamlit as st
from smart_storage.lista_spesa import ListaSpesa
from smart_storage.prodotti import Prodotti
from smart_storage.scraper import Scraper

# Set Streamlit page configuration and title
st.set_page_config(page_title="Smart Storage", layout="wide")
st.title("Shopping list")


# Create instances of the classes and cached them to improve performance
@st.cache_resource
def initiate_objects():
    prodotti = Prodotti("prodotti.db", Scraper())
    lista_spesa = ListaSpesa("listaspesa.db", prodotti)
    return prodotti, lista_spesa


prodotti, lista_spesa = initiate_objects()

if st.button("Clear the list"):
    lista_spesa.erase_database()

# Load the items
items = lista_spesa.get_items()


# Generate the checkboxes
for item in items:
    checked = st.checkbox(
        f"{item.name} \n\n Quantity: {item.quantity}", value=False, key=item.barcode
    )
