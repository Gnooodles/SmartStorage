import csv
import sqlite3

conn = sqlite3.connect('barcode.db')
cur = conn.cursor()

with open('barcode.csv') as f:
    reader = csv.reader(f)
    data = list(reader)

cur.execute("CREATE TABLE barcode (ean TEXT, name TEXT)")

for row in data:
    cur.execute("INSERT INTO barcode (ean, name) VALUES (?,?)", row)
    print("Sto facendo")

conn.commit()
conn.close()


