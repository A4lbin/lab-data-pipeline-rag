import sqlite3

connection = sqlite3.connect("../database/lab.db")

cursor = connection.cursor()

cursor.execute("""
    SELECT *
    FROM records
    LIMIT 5
""")

print(cursor.fetchone())

connection.close()