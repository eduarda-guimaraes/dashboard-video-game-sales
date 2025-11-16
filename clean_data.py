import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/vgsales_raw.csv")
CLEAN_PATH = Path("data/vgsales_clean.csv")

def load_raw():
    df = pd.read_csv(RAW_PATH)
    print("Raw shape:", df.shape)
    return df

def clean_dataset(df):
    df = df.drop_duplicates()
    df = df[df["Year"].between(1980, 2025)]
    df["Year"] = df["Year"].astype(int)
    df["Genre"] = df["Genre"].fillna("Unknown")
    df["Publisher"] = df["Publisher"].fillna("Unknown")

    df["Total_Sales"] = (
        df["NA_Sales"] +
        df["EU_Sales"] +
        df["JP_Sales"] +
        df["Other_Sales"]
    )

    print("Clean shape:", df.shape)
    return df

def main():
    df_raw = load_raw()
    df_clean = clean_dataset(df_raw)
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(CLEAN_PATH, index=False)
    print("Clean file saved to:", CLEAN_PATH)

if __name__ == "__main__":
    main()