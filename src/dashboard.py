import streamlit as st
from smart_storage.magazzino import Magazzino
from smart_storage.prodotti import Prodotti
from smart_storage.lista_spesa import ListaSpesa
import pandas as pd

st.set_page_config(page_title="Dashboard Smart Storage", layout="wide")
prodotti = Prodotti("prodotti.db")
magazzino = Magazzino("magazzino.db", prodotti)
lista_spesa = ListaSpesa("listaspesa.db", prodotti)
# st.write(magazzino.get_items())

st.title("Dashboard")


def add_missing_to_list():
    missing_products = magazzino.get_missing_product_quantity()
    for missing in missing_products:
        already_in_list = lista_spesa.get_item_quantity(missing['barcode'])
        print(already_in_list)
        if already_in_list < missing['difference']:
            lista_spesa.add_item(missing['barcode'], quantity=missing['difference'])


# bottoni allineati orizzontalmente
col_button_1, col_button_2 = st.columns([3, 20])
with col_button_1:
    st.button("Refresh")
    # TODO implementare bottone per aggiornare i dati
with col_button_2:
    if st.button("Add missing groceries to shopping list"):
        add_missing_to_list()
    # implementare aggiunta a lista della spesa degli item con quanità minore della soglia

df = pd.DataFrame(magazzino.get_items(), columns=["Code", "Name", "Quantity", "Threshold"])


# funzione per evidenziare la variable Quantity di una riga se minore della Threshold
def highlight_threshold(row):
    highlight = (
        "background-color: firebrick; color: white"  # colori: orangered, firebrick
    )
    default = ""

    if row["Quantity"] < row["Threshold"]:
        return [highlight, default]
    else:
        return [default, default]


# crea la tabella editabile dal dataframe con la funzione per l'evidenziamento
st.data_editor(
    df, #.style.apply(highlight_threshold, subset=["Quantity", "Threshold"], axis=1),
    hide_index=True,
    use_container_width=True,
    key="data_editor",
)
# disabled: disabilito la modifica sulle colonne Code,Name,Quantity

# st.write("Here's the session state:")
# st.write(st.session_state["data_editor"]["edited_rows"])

def get_modified_item(column: str):
    # prendo le modifiche effettuate tramite la tabella modificabile
    edited_changes = st.session_state["data_editor"]["edited_rows"]
    # prendo gli indici di riga corrispondenti
    rows_changed = edited_changes.keys()
    # print(list(rows_changed))

    # prendo i codici a barre corrispondenti agli indici di riga modificate
    codes_changed = []
    for r in rows_changed:
        # codes.append(df.loc[[r],["Code"]].values[1])
        codes_changed.append(df[column].values[r])

    return rows_changed, codes_changed, edited_changes



# aggiorno la threshold nel database magazzino.db
rows_changed, codes_changed, edited_changes = get_modified_item("Code")
for row, barcode in zip(rows_changed, codes_changed):
    threshold = edited_changes.get(row)["Threshold"]
    magazzino.update_threshold(barcode, threshold)

#FIXME in dashboard errore cambiamento threshold

        
        
