import sqlite3
import pandas as pd

con = sqlite3.connect("prodotti.db")
cur = con.cursor()

# cur.execute("CREATE TABLE prodotti(id, code, name, quantity, brands, brands_tag, categories, categories_en)")

data = pd.read_csv("dati_ita_filtered.csv")
data["code"] = data["code"].astype(str)

#print(data)

for row in data.iterrows():
    cur.execute(f"INSERT INTO prodotti VALUES({data['id']}, {data['code']}, {data['product_name']}, {data['quantity']}, {data['brands']}, {data['brands_tags']}, {data['categories']}, {data['categories_en']})")
    con.commit()

