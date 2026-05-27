import os

def save_csv(df):
    os.makedirs("data/processed", exist_ok=True)

    path = "data/processed/bmath_school_performance.csv"

    df.to_csv(path, index=False)

    print(f"Saved successfully to {path}")