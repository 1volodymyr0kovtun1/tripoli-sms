# clean.py
import pandas as pd

def clean_tripoli_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # прибираємо порожні або пробільні значення «port»
    df["port"] = df["port"].fillna("").str.strip()
    df = df[df["port"] != ""]

    # видаляємо дублікати (desktop + mobile-блок)
    df = df.drop_duplicates(subset=["crop", "port", "price"])

    # сортуємо для зручності
    df = df.sort_values(["crop", "port", "price"],
                        ascending=[True, True, False])
    return df
