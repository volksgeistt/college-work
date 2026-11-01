
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "data/vehicles.csv"
OUTPUT_FILE = BASE_DIR / "data/vehicles_cleaned.csv"

CHUNK_SIZE = 100_000

# Initial thresholds for a conventional used-car model.
MIN_PRICE = 500
MAX_PRICE = 200_000

MIN_YEAR = 1980
MAX_YEAR = 2022

MIN_ODOMETER = 0
MAX_ODOMETER = 500_000

FEATURES = [
    "price",
    "year",
    "manufacturer",
    "model",
    "condition",
    "cylinders",
    "fuel",
    "odometer",
    "transmission",
    "drive",
    "type",
    "state",
]

REQUIRED_COLUMNS = ["id"] + FEATURES

# --------------------------------------------------
# VALIDATE INPUT
# --------------------------------------------------

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Could not find {INPUT_FILE.name} in {BASE_DIR}"
    )

# Counters
total_rows = 0
missing_target = 0
invalid_price = 0
invalid_year = 0
invalid_odometer = 0
duplicate_ids = 0
cleaned_rows = 0

seen_ids = set()

print("Starting chunked dataset cleaning...")
print(f"Input file: {INPUT_FILE}")
print(f"Output file: {OUTPUT_FILE}")

# --------------------------------------------------
# PROCESS DATA IN CHUNKS
# --------------------------------------------------

if OUTPUT_FILE.exists():
    OUTPUT_FILE.unlink()

for chunk_number, chunk in enumerate(
    pd.read_csv(
        INPUT_FILE,
        usecols=REQUIRED_COLUMNS,
        chunksize=CHUNK_SIZE,
        low_memory=False,
    ),
    start=1,
):
    total_rows += len(chunk)

    # Convert numeric columns safely.
    for col in ["price", "year", "odometer"]:
        chunk[col] = pd.to_numeric(
            chunk[col], errors="coerce"
        )

    # Remove duplicate listing IDs across all chunks.
    duplicate_mask = chunk["id"].isin(seen_ids)
    duplicate_ids += int(duplicate_mask.sum())

    chunk = chunk.loc[~duplicate_mask].copy()

    new_ids = chunk["id"].dropna().unique()
    seen_ids.update(new_ids.tolist())

    # Remove rows without a usable target.
    missing_target_mask = chunk["price"].isna()
    missing_target += int(missing_target_mask.sum())
    chunk = chunk.loc[~missing_target_mask].copy()

    # Keep plausible asking prices.
    price_mask = (
        chunk["price"].between(MIN_PRICE, MAX_PRICE)
    )
    invalid_price += int((~price_mask).sum())
    chunk = chunk.loc[price_mask].copy()

    # Keep plausible model years.
    year_mask = (
        chunk["year"].between(MIN_YEAR, MAX_YEAR)
    )
    invalid_year += int((~year_mask).sum())
    chunk = chunk.loc[year_mask].copy()

    # Keep plausible odometer values.
    # Missing mileage is retained for later imputation.
    odometer_mask = (
        chunk["odometer"].isna()
        | chunk["odometer"].between(
            MIN_ODOMETER, MAX_ODOMETER
        )
    )
    invalid_odometer += int((~odometer_mask).sum())
    chunk = chunk.loc[odometer_mask].copy()

    # Normalize categorical text and missing values.
    categorical_columns = [
        "manufacturer",
        "model",
        "condition",
        "cylinders",
        "fuel",
        "transmission",
        "drive",
        "type",
        "state",
    ]

    for col in categorical_columns:
        chunk[col] = (
            chunk[col]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    # Drop the listing ID from the modeling dataset.
    chunk = chunk[FEATURES]

    # Append each cleaned chunk to the output CSV.
    chunk.to_csv(
        OUTPUT_FILE,
        mode="a",
        index=False,
        header=(cleaned_rows == 0),
    )

    cleaned_rows += len(chunk)

    print(
        f"Chunk {chunk_number}: "
        f"processed {total_rows:,} source rows; "
        f"kept {cleaned_rows:,} rows"
    )

# --------------------------------------------------
# REPORT
# --------------------------------------------------

print("\n" + "=" * 55)
print("CLEANING SUMMARY")
print("=" * 55)
print(f"Source rows processed:       {total_rows:,}")
print(f"Rows without price:          {missing_target:,}")
print(f"Duplicate IDs removed:       {duplicate_ids:,}")
print(f"Prices outside limits:       {invalid_price:,}")
print(f"Years outside limits:        {invalid_year:,}")
print(f"Invalid mileage removed:     {invalid_odometer:,}")
print(f"Cleaned rows retained:       {cleaned_rows:,}")
print(f"Output file:                 {OUTPUT_FILE}")

# --------------------------------------------------
# VERIFY OUTPUT
# --------------------------------------------------

print("\nChecking the cleaned dataset...")

sample = pd.read_csv(OUTPUT_FILE, nrows=1000)

print(f"Columns: {len(sample.columns)}")
print(f"Column names: {sample.columns.tolist()}")
print("\nSample rows:")
print(sample.head())

print("\nRemaining missing values in the sample:")
print(sample.isna().sum().sort_values(ascending=False))

print("\nCleaning complete.")
