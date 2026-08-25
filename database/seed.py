import sqlite3
import pandas as pd

CSV_FILE="../data/processed/lab_data_clean.csv"
DATABASE="lab.db"

df= pd.read_csv(CSV_FILE)

connection = sqlite3.connect(DATABASE)

df.to_sql("samples",connection,if_exists="replace",index=False)

connection.close()

print("Database created successfully :)")