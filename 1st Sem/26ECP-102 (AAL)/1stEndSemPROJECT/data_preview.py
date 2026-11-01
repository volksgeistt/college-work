
from pathlib import Path
import pandas as pd

DATASET_PATH = Path(__file__).parent / "data/vehicles.csv"

print("=" * 60)
print(" CAR DATASET INSPECTION")
print("=" * 60)

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}\n"
        "Place vehicles.csv beside inspect_data.py."
    )

size_mb = DATASET_PATH.stat().st_size / (1024 ** 2)
print(f"\nFile: {DATASET_PATH.name}")
print(f"File size: {size_mb:.2f} MB")

df = pd.read_csv(DATASET_PATH, nrows=1000, low_memory=False)

print("\n--- SAMPLE DATA ---")
print(df.head())

print("\n--- SAMPLE SHAPE ---")
print(f"Rows loaded: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\n--- COLUMN NAMES ---")
for column in df.columns:
    print(f"- {column}")

print("\n--- DATA TYPES ---")
print(df.dtypes.to_string())

print("\n--- SAMPLE MISSING VALUES ---")
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)

if missing.empty:
    print("No missing values in this sample.")
else:
    print(missing.to_string())

print("\n--- SAMPLE NUMERICAL SUMMARY ---")
print(df.describe().to_string())

if "price" in df.columns:
    print("\n--- PRICE SAMPLE ---")
    print(df["price"].describe())

print("\nInspection complete.")
