# ============================================================
# CAR PRICE PREDICTION
# Machine Learning Training Pipeline
# ============================================================

from pathlib import Path
import time

import joblib
import numpy as np
import pandas as pd
from tqdm import tqdm

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data/vehicles_cleaned.csv"
MODEL_DIR = BASE_DIR / "models"
RESULTS_PATH = BASE_DIR / "model_results.csv"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

TARGET = "price"
TEST_SIZE = 0.20
RANDOM_STATE = 42

# Lightweight Random Forest configuration
N_TREES = 12
MAX_DEPTH = 12
MIN_SAMPLES_LEAF = 20


# ============================================================
# 2. LOAD DATASET
# ============================================================

print("\n" + "=" * 65)
print("  CAR PRICE PREDICTION")
print("=" * 65)

start_total = time.time()

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"\nDataset not found:\n{DATA_PATH}\n\n"
        "Make sure vehicles_cleaned.csv is in the project folder."
    )

print("\n[1/6] Loading cleaned dataset...")

df = pd.read_csv(DATA_PATH, low_memory=False)

print(f"Dataset loaded successfully!")
print(f"Total records : {len(df):,}")
print(f"Total columns : {len(df.columns)}")


# ============================================================
# 3. PREPARE FEATURES AND TARGET
# ============================================================

print("\n[2/6] Preparing features and target...")

if TARGET not in df.columns:
    raise ValueError(
        f"Target column '{TARGET}' was not found in the dataset."
    )

# Remove rows with missing target values.
df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
df = df.dropna(subset=[TARGET]).copy()

# Separate input features from the target.
X = df.drop(columns=[TARGET]).copy()
y = df[TARGET].astype(float).copy()

# Identify numerical and categorical features.
numeric_features = X.select_dtypes(
    include=["number"]
).columns.tolist()

categorical_features = X.select_dtypes(
    exclude=["number"]
).columns.tolist()

# Standardize categorical values.
for column in categorical_features:
    X[column] = X[column].apply(
        lambda value: str(value).strip()
        if pd.notna(value) and str(value).strip()
        else np.nan
    )

# Ensure numerical columns contain numeric values.
for column in numeric_features:
    X[column] = pd.to_numeric(
        X[column],
        errors="coerce"
    )

print(f"Records available : {len(X):,}")
print(f"Input features    : {X.shape[1]}")
print(f"Numerical features: {len(numeric_features)}")
print(f"Categorical features: {len(categorical_features)}")

print("\nTarget variable: price")
print("Prediction unit: USD")


# ============================================================
# 4. SPLIT DATA INTO TRAINING AND TESTING SETS
# ============================================================

print("\n[3/6] Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE
)

print(f"Training records: {len(X_train):,}")
print(f"Testing records : {len(X_test):,}")
print("Data split completed.")


# ============================================================
# 5. BUILD PREPROCESSING PIPELINE
# ============================================================

print("\n[4/6] Preparing data preprocessing...")

# Numerical features: replace missing values with the median.
numeric_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median")
    )
])

# Categorical features:
# 1. Replace missing values with "Unknown".
# 2. One-hot encode categories.
# 3. Group infrequent categories where supported.
categorical_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="constant",
            fill_value="Unknown"
        )
    ),
    (
        "encoder",
        OneHotEncoder(
            handle_unknown="infrequent_if_exist",
            min_frequency=20,
            sparse_output=True
        )
    )
])

preprocessor = ColumnTransformer([
    (
        "numerical",
        numeric_pipeline,
        numeric_features
    ),
    (
        "categorical",
        categorical_pipeline,
        categorical_features
    )
])

# Fit preprocessing on training data only.
print("Fitting preprocessing on training data...")

X_train_processed = preprocessor.fit_transform(X_train)

print("Transforming testing data...")

X_test_processed = preprocessor.transform(X_test)

print("Preprocessing completed.")
print(f"Processed training shape: {X_train_processed.shape}")
print(f"Processed testing shape : {X_test_processed.shape}")


# ============================================================
# 6. MODEL 1: LINEAR REGRESSION
# ============================================================

print("\n" + "=" * 65)
print("MODEL 1/2: LINEAR REGRESSION")
print("=" * 65)

linear_model = LinearRegression()

start_time = time.time()

print("Training Linear Regression...")

linear_model.fit(
    X_train_processed,
    y_train
)

linear_training_time = time.time() - start_time

print("Linear Regression training completed: 100%")
print(f"Training time: {linear_training_time:.2f} seconds")


# ============================================================
# 7. MODEL 2: RANDOM FOREST WITH LIVE PROGRESS
# ============================================================

print("\n" + "=" * 65)
print("MODEL 2/2: RANDOM FOREST REGRESSOR")
print("=" * 65)

print(f"Total trees to train: {N_TREES}")
print(f"Maximum tree depth  : {MAX_DEPTH}")
print(f"Minimum leaf samples: {MIN_SAMPLES_LEAF}")

random_forest = RandomForestRegressor(
    n_estimators=1,
    max_depth=MAX_DEPTH,
    min_samples_leaf=MIN_SAMPLES_LEAF,
    max_features=0.5,
    max_samples=0.5,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    warm_start=True
)

start_time = time.time()

# Add one tree per iteration.
# The progress bar reports the actual number of trees built.

for tree_count in tqdm(
    range(1, N_TREES + 1),
    total=N_TREES,
    desc="Training Random Forest",
    unit="tree",
    dynamic_ncols=True
):
    random_forest.set_params(
        n_estimators=tree_count
    )

    random_forest.fit(
        X_train_processed,
        y_train
    )

random_forest_training_time = time.time() - start_time

print("\nRandom Forest training completed: 100%")
print(f"Training time: {random_forest_training_time:.2f} seconds")


# ============================================================
# 8. EVALUATE MODELS
# ============================================================

print("\n" + "=" * 65)
print("EVALUATING MODELS")
print("=" * 65)


def evaluate_model(model_name, model, training_time):
    """
    Evaluate a trained regression model on held-out test data.
    """

    print(f"\nEvaluating {model_name}...")

    predictions = model.predict(X_test_processed)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    print(f"MAE : ${mae:,.2f}")
    print(f"RMSE: ${rmse:,.2f}")
    print(f"R²  : {r2:.4f}")

    return {
        "Model": model_name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "Training Time (seconds)": training_time
    }


results = []

results.append(
    evaluate_model(
        "Linear Regression",
        linear_model,
        linear_training_time
    )
)

results.append(
    evaluate_model(
        "Random Forest",
        random_forest,
        random_forest_training_time
    )
)


# ============================================================
# 9. COMPARE MODEL PERFORMANCE
# ============================================================

print("\n" + "=" * 80)
print("MODEL COMPARISON")
print("=" * 80)

results_df = pd.DataFrame(results)

# Primary 
results_df = results_df.sort_values(
    by="MAE",
    ascending=True
).reset_index(drop=True)

print(
    results_df.to_string(
        index=False,
        formatters={
            "MAE": "${:,.2f}".format,
            "RMSE": "${:,.2f}".format,
            "R2": "{:.4f}".format,
            "Training Time (seconds)": "{:.2f}".format
        }
    )
)

results_df.to_csv(
    RESULTS_PATH,
    index=False
)

print(f"\nResults saved to: {RESULTS_PATH}")


# ============================================================
# 10. SELECT AND SAVE THE BEST MODEL
# ============================================================

print("\n" + "=" * 65)
print("SAVING BEST MODEL")
print("=" * 65)

best_model_name = results_df.iloc[0]["Model"]

if best_model_name == "Linear Regression":
    best_regressor = linear_model
else:
    best_regressor = random_forest

# Save the fitted preprocessing and model together.
# This ensures new vehicle data receives the same transformations.
best_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", best_regressor)
])

model_path = MODEL_DIR / "best_model.joblib"

joblib.dump(
    best_pipeline,
    model_path
)

print(f"Selected model: {best_model_name}")
print(f"Model saved to: {model_path}")


# ============================================================
# 11. FINAL SUMMARY
# ============================================================

total_time = time.time() - start_total

best_result = results_df.iloc[0]

print("\n" + "=" * 65)
print("TRAINING WORKFLOW COMPLETED: 100%")
print("=" * 65)

print(f"Dataset records : {len(X):,}")
print(f"Training records: {len(X_train):,}")
print(f"Testing records : {len(X_test):,}")

print(f"\nBest model: {best_model_name}")
print(f"Test MAE   : ${best_result['MAE']:,.2f}")
print(f"Test RMSE  : ${best_result['RMSE']:,.2f}")
print(f"Test R²    : {best_result['R2']:.4f}")

print(f"\nTotal elapsed time: {total_time:.2f} seconds")
print(f"Saved model       : {model_path}")
print(f"Saved results     : {RESULTS_PATH}")

print("\nNext step: validate the selected model and build the prediction interface.")
