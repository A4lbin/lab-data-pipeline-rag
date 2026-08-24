import pandas as pd

RAW_FILE = "../data/raw/4x4x4_SI.csv"
PROCESSED_FILE = "../data/processed/lab_data_clean.csv"

def extract():
    return pd.read_csv(RAW_FILE)

def load(df):
    df.to_csv(PROCESSED_FILE,index=False)

def transform(df):
    df.columns=(df.columns.str.strip().str.lower().str.replace(" ","_"))
    df = df.drop_duplicates()

    numeric_columns = df.select_dtypes(include=["int64","float64"]).columns
    text_columns = df.select_dtypes(include="str").columns
    # print(numeric_columns)
    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )
    for column in text_columns:
        df[column] = df[column].str.strip()
    return df

def validate(df):

    if df["uid"].isna().any():
        raise ValueError("UID contains missing values")

    if not df["uid"].is_unique:
        raise ValueError("UID is not unique")

    return df

def run_pipeline():
    df=extract()
    df=transform(df)
    validate(df)
    load(df)
    return df

dff=run_pipeline()
# print(dff)
# if(dff["uid"].is_unique==1):
#     print("uid is unique")
