import pandas as pd

RAW_FILE = "../data/raw/4x4x4_SI.csv"
PROCESSED_FILE = "../data/processed/lab_data_clean.csv"

def extract():
    return pd.read_csv(RAW_FILE)

def load(df):
    df.to_csv(PROCESSED_FILE,index=False)

def run_pipeline():
    df=extract()
    load(df)

run_pipeline()