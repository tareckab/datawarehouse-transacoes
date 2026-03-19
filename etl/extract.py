
import pandas as pd
import os

DATA_PATH = "../data"

def extract():
    dfs = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(DATA_PATH, file), sep=';', encoding='utf-8')
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)
