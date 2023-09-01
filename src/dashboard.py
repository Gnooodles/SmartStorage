import streamlit as st
from smart_storage.magazzino import Magazzino
from smart_storage.prodotti import Prodotti
import pandas as pd

st.set_page_config(page_title="Dashboard Smart Storage", layout="wide")
prodotti = Prodotti("prodotti.db")
magazzino = Magazzino("magazzino.db", prodotti)
# st.write(magazzino.get_items())

st.title("Dashboard")
st.sidebar.success("Select a demo above.")

# bottoni allineati orizzontalmente
col_button_1, col_button_2 = st.columns([3, 20])
with col_button_1:
    st.button("Refresh")
    # TODO implementare bottone per aggiornare i dati
with col_button_2:
    st.button("Add missing groceries to shopping list")
    # TODO implementare aggiunta a lista della spesa degli item con quanità minore della soglia

df = pd.DataFrame(magazzino.get_items(), columns=["Code", "Name", "Quantity"])
df[
    "Threshold"
] = 4  # colonna provvisoria, TODO creare colonna nel database magazzino.db


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
    df.style.apply(highlight_threshold, subset=["Quantity", "Threshold"], axis=1),
    hide_index=True,
    use_container_width=True,
    key="data_editor",
    disabled=["Code", "Name", "Quantity"],
)
# disabled: disabilito la modifica sulle colonne Code,Name,Quantity

# st.write("Here's the session state:")
# st.write(st.session_state["data_editor"]["edited_rows"])


# prendo le modifiche effettuate tramite la tabella modificabile
edited_changes = st.session_state["data_editor"]["edited_rows"]
# prendo gli indici di riga corrispondenti
rows_changed = edited_changes.keys()
# print(list(rows_changed))

# prendo i codici a barre corrispondenti agli indici di riga modificate
codes_changed = []
for r in rows_changed:
    # codes.append(df.loc[[r],["Code"]].values[1])
    codes_changed.append(df["Code"].values[r])

# print(codes_changed)

# creo la query per aggiornare il database magazzino.db
for row, code in zip(rows_changed, codes_changed):
    threshold = edited_changes.get(row)["Threshold"]
    st.write(f"UPDATE magazzino SET threshold = {threshold} WHERE barcode = '{code}'")
    # TODO implementare l'aggiornamento del database tramite questa query
