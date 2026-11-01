from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "data/vehicles_cleaned.csv"
CHUNK_SIZE = 100_000

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        "vehicles_cleaned.csv not found. "
        "Make sure it is in the project folder."
    )

print("=" * 60)
print("CAR PRICE PREDICTION - DATA ANALYSIS")
print("=" * 60)

print(f"\nDataset size: {DATASET_PATH.stat().st_size / (1024**2):.2f} MB")

# --------------------------------------------------
# 1. INITIALIZE ANALYSIS
# --------------------------------------------------

total_rows = 0
missing_counts = None
price_summary = []
year_summary = []
odometer_summary = []
category_counts = {}

sample_parts = []

categorical_columns = [
    "manufacturer",
    "condition",
    "fuel",
    "transmission",
    "drive",
    "type",
    "state",
]

# --------------------------------------------------
# 2. PROCESS DATA IN CHUNKS
# --------------------------------------------------

for chunk_number, chunk in enumerate(
    pd.read_csv(
        DATASET_PATH,
        chunksize=CHUNK_SIZE,
        low_memory=False,
    ),
    start=1,
):
    total_rows += len(chunk)

    # Count missing values across the entire dataset.
    chunk_missing = chunk.isna().sum()

    if missing_counts is None:
        missing_counts = chunk_missing
    else:
        missing_counts = missing_counts.add(
            chunk_missing, fill_value=0
        )

    # Numeric summaries.
    for column, storage in [
        ("price", price_summary),
        ("year", year_summary),
        ("odometer", odometer_summary),
    ]:
        values = pd.to_numeric(
            chunk[column], errors="coerce"
        ).dropna()

        if not values.empty:
            storage.append(
                {
                    "count": len(values),
                    "min": values.min(),
                    "max": values.max(),
                    "sum": values.sum(),
                }
            )

    # Count common categorical values.
    for column in categorical_columns:
        counts = chunk[column].value_counts(dropna=False)

        if column not in category_counts:
            category_counts[column] = counts
        else:
            category_counts[column] = (
                category_counts[column]
                .add(counts, fill_value=0)
            )

    # Keep a random sample from each chunk for plotting.
    sample_parts.append(
        chunk.sample(
            n=min(2000, len(chunk)),
            random_state=42,
        )
    )

    print(
        f"Processed {total_rows:,} records...",
        end="\r",
    )

print("\n\nAnalysis completed.")

# --------------------------------------------------
# 3. DATASET OVERVIEW
# --------------------------------------------------

print("\n--- DATASET OVERVIEW ---")
print(f"Total records: {total_rows:,}")
print(f"Total columns: {len(missing_counts)}")

print("\nColumn names:")
print(missing_counts.index.tolist())

# --------------------------------------------------
# 4. MISSING VALUES
# --------------------------------------------------

print("\n--- MISSING VALUES ---")

missing_report = pd.DataFrame({
    "Missing Count": missing_counts.astype(int),
    "Missing Percentage": (
        missing_counts / total_rows * 100
    ).round(2),
})

print(
    missing_report.sort_values(
        "Missing Percentage",
        ascending=False,
    ).to_string()
)

# --------------------------------------------------
# 5. NUMERICAL SUMMARIES
# --------------------------------------------------

def combine_numeric_summaries(parts):
    total_count = sum(p["count"] for p in parts)

    if total_count == 0:
        return None

    return {
        "count": total_count,
        "min": min(p["min"] for p in parts),
        "max": max(p["max"] for p in parts),
        "mean": (
            sum(p["sum"] for p in parts) / total_count
        ),
    }


print("\n--- NUMERICAL SUMMARY ---")

for column, storage in [
    ("price", price_summary),
    ("year", year_summary),
    ("odometer", odometer_summary),
]:
    summary = combine_numeric_summaries(storage)

    print(f"\n{column.upper()}")

    if summary:
        for key, value in summary.items():
            print(f"{key}: {value:,.2f}")

# --------------------------------------------------
# 6. COMMON CATEGORIES
# --------------------------------------------------

print("\n--- COMMON CATEGORIES ---")

for column, counts in category_counts.items():
    print(f"\nTop 10 values for {column}:")
    print(counts.sort_values(ascending=False).head(10).to_string())

# --------------------------------------------------
# 7. CREATE A REPRESENTATIVE SAMPLE
# --------------------------------------------------

sample_df = pd.concat(
    sample_parts,
    ignore_index=True,
)

# Bound the sample size if the dataset has many chunks.
if len(sample_df) > 50_000:
    sample_df = sample_df.sample(
        n=50_000,
        random_state=42,
    )

print(f"\nPlotting sample size: {len(sample_df):,}")

# --------------------------------------------------
# 8. PRICE DISTRIBUTION
# --------------------------------------------------

prices = sample_df["price"].dropna()

plt.figure(figsize=(10, 6))
plt.hist(prices, bins=60)
plt.title("Distribution of Used Car Listing Prices")
plt.xlabel("Price (USD)")
plt.ylabel("Number of Listings")
plt.tight_layout()
plt.savefig(BASE_DIR / "price_distribution.png", dpi=150)
plt.show()

# A logarithmic plot helps reveal the shape of a
# right-skewed price distribution.
plt.figure(figsize=(10, 6))
plt.hist(prices[prices > 0], bins=60)
plt.xscale("log")
plt.title("Used Car Prices - Logarithmic X Axis")
plt.xlabel("Price (USD, logarithmic scale)")
plt.ylabel("Number of Listings")
plt.tight_layout()
plt.savefig(BASE_DIR / "price_distribution_log.png", dpi=150)
plt.show()

# --------------------------------------------------
# 9. PRICE VS VEHICLE YEAR
# --------------------------------------------------

plot_df = sample_df.dropna(
    subset=["price", "year"]
)

plt.figure(figsize=(10, 6))
plt.scatter(
    plot_df["year"],
    plot_df["price"],
    alpha=0.25,
    s=8,
)
plt.title("Vehicle Year vs Listing Price")
plt.xlabel("Vehicle Year")
plt.ylabel("Price (USD)")
plt.tight_layout()
plt.savefig(BASE_DIR / "year_vs_price.png", dpi=150)
plt.show()

# --------------------------------------------------
# 10. PRICE VS ODOMETER
# --------------------------------------------------

plot_df = sample_df.dropna(
    subset=["price", "odometer"]
)

plt.figure(figsize=(10, 6))
plt.scatter(
    plot_df["odometer"],
    plot_df["price"],
    alpha=0.25,
    s=8,
)
plt.title("Odometer Reading vs Listing Price")
plt.xlabel("Odometer (miles)")
plt.ylabel("Price (USD)")
plt.tight_layout()
plt.savefig(BASE_DIR / "odometer_vs_price.png", dpi=150)
plt.show()

print("\nAnalysis finished.")
print("Graphs saved in your project folder.")