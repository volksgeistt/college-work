import sys
import warnings
from pathlib import Path

# Suppress unnecessary warnings in the terminal report.
# Errors and exceptions will still be handled explicitly.
warnings.filterwarnings("ignore", category=FutureWarning)

try:
    import joblib
    import numpy as np
    import pandas as pd

    from sklearn.model_selection import train_test_split

    from sklearn.metrics import (
        mean_absolute_error,
        mean_squared_error,
        r2_score,
    )

except ImportError as error:
    print(f"Details: {error}")
    print("py -m pip install pandas numpy joblib scikit-learn")
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "vehicles_cleaned.csv"
MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"
RESULTS_PATH = BASE_DIR / "model_results.csv"

TARGET_COLUMN = "price"

TEST_SIZE = 0.20
RANDOM_STATE = 42

RECORDED_RESULTS = {
    "Model": "Random Forest",
    "MAE (USD)": 4380.98,
    "RMSE (USD)": 7298.88,
    "R2 Score": 0.7559,
}


# =============================================================================
# 3. CONSOLE FORMATTING FUNCTIONS
# =============================================================================

def print_header(title):
    """
    Display a large heading to separate the main sections of the report.
    """

    print("\n")
    print("=" * 76)
    print(f" {title.upper()}")
    print("=" * 76)


def print_section(title):
    """
    Display a smaller heading for subsections.
    """

    print(f"\n{title}")
    print("-" * 76)


def print_info(label, value):
    """
    Display a label and its corresponding value in a consistent format.
    """

    print(f"{label:<30}: {value}")


def format_money(value):
    """
    Format a numerical value as US dollars.

    Example:
        4380.98 becomes $4,380.98
    """

    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return str(value)


def print_table(dataframe, max_rows=20):
    """
    Display a DataFrame as a readable terminal table.

    Args:
        dataframe: The pandas DataFrame to display.
        max_rows: Maximum number of rows to display.
    """

    if dataframe is None or dataframe.empty:
        print("No data available.")
        return

    # Display a copy so the original DataFrame remains unchanged.
    display_df = dataframe.head(max_rows).copy()

    # Use pandas' built-in formatting for a readable console table.
    print(display_df.to_string(index=False, max_colwidth=35))

    # Inform the user if the table contains more rows than displayed.
    if len(dataframe) > max_rows:
        print(
            f"\nShowing {max_rows} of {len(dataframe):,} available rows."
        )


def print_error(message):
    """
    Display an error message without producing an unnecessarily long traceback.
    """

    print(f"\nERROR: {message}")


# =============================================================================
# 4. LOAD AND INSPECT THE DATASET
# =============================================================================

def load_dataset():
    """
    Load the cleaned vehicle dataset.

    Returns:
        A pandas DataFrame if loading succeeds.
        None if the file is missing or cannot be loaded.
    """

    # Verify that the expected CSV file exists before reading it.
    if not DATA_PATH.exists():
        print_error(f"Dataset not found: {DATA_PATH}")
        print("Check the dataset path and project folder structure.")
        return None

    try:
        # low_memory=False reduces mixed-type inference warnings.
        dataframe = pd.read_csv(
            DATA_PATH,
            low_memory=False,
        )

        return dataframe

    except Exception as error:
        print_error(f"Could not load the dataset: {error}")
        return None


def inspect_dataset(dataframe):
    """
    Display the dataset dimensions, target statistics, and missing values.
    """

    print_header("1. Dataset Overview")

    if dataframe is None:
        print("Dataset inspection skipped because the dataset could not be loaded.")
        return

    # -------------------------------------------------------------------------
    # General dataset information
    # -------------------------------------------------------------------------

    print_section("DATASET INFORMATION")

    print_info("Dataset file", DATA_PATH.name)
    print_info("Total records", f"{len(dataframe):,}")
    print_info("Total columns", f"{len(dataframe.columns):,}")
    print_info("Dataset dimensions", str(dataframe.shape))

    print_section("AVAILABLE COLUMNS")

    # Display all column names without printing the entire dataset.
    for index, column in enumerate(dataframe.columns, start=1):
        print(f"{index:>2}. {column}")

    # -------------------------------------------------------------------------
    # Target variable statistics
    # -------------------------------------------------------------------------

    if TARGET_COLUMN not in dataframe.columns:
        print_error(
            f"Target column '{TARGET_COLUMN}' is missing from the dataset."
        )
        return

    # Convert prices to numeric values.
    # Invalid or missing values are excluded from these statistics.
    prices = pd.to_numeric(
        dataframe[TARGET_COLUMN],
        errors="coerce",
    )

    prices = prices.replace(
        [np.inf, -np.inf],
        np.nan,
    ).dropna()

    print_section("TARGET VARIABLE: VEHICLE PRICE")

    print_info("Target column", TARGET_COLUMN)
    print_info("Valid price records", f"{len(prices):,}")

    if not prices.empty:
        print_info("Mean price", format_money(prices.mean()))
        print_info("Median price", format_money(prices.median()))
        print_info("Minimum price", format_money(prices.min()))
        print_info("Maximum price", format_money(prices.max()))

    # -------------------------------------------------------------------------
    # Vehicle year statistics
    # -------------------------------------------------------------------------

    if "year" in dataframe.columns:
        years = pd.to_numeric(
            dataframe["year"],
            errors="coerce",
        )

        years = years.replace(
            [np.inf, -np.inf],
            np.nan,
        ).dropna()

        if not years.empty:
            print_section("VEHICLE YEAR")

            print_info(
                "Oldest vehicle year",
                f"{years.min():.0f}",
            )

            print_info(
                "Newest vehicle year",
                f"{years.max():.0f}",
            )

    # -------------------------------------------------------------------------
    # Odometer statistics
    # -------------------------------------------------------------------------

    if "odometer" in dataframe.columns:
        odometer = pd.to_numeric(
            dataframe["odometer"],
            errors="coerce",
        )

        odometer = odometer.replace(
            [np.inf, -np.inf],
            np.nan,
        ).dropna()

        if not odometer.empty:
            print_section("ODOMETER INFORMATION")

            print_info(
                "Average mileage",
                f"{odometer.mean():,.0f} miles",
            )

    # -------------------------------------------------------------------------
    # Missing-value analysis
    # -------------------------------------------------------------------------

    print_section("MISSING VALUES")

    missing = dataframe.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("No missing values detected.")
    else:
        missing_table = pd.DataFrame({
            "Column": missing.index,
            "Missing Records": missing.values,
            "Missing Percentage": (
                missing.values / len(dataframe) * 100
            ).round(2),
        })

        print_table(missing_table)

    print_section("DATASET NOTE")

    print(
        "The dataset contains historical US vehicle listing prices "
        "denominated in USD."
    )

    print(
        "Predictions reflect the dataset and model used; they should not "
        "automatically be treated as current market prices."
    )


# =============================================================================
# 5. DISPLAY PREVIOUSLY RECORDED TRAINING RESULTS
# =============================================================================

def inspect_training_results():
    """
    Display the results recorded in model_results.csv.

    If the CSV does not exist, display the previously reported Random Forest
    results with a clear indication that they are historical records.
    """

    print_header("2. Model Training Results")

    # -------------------------------------------------------------------------
    # Load the results CSV if available.
    # -------------------------------------------------------------------------

    if RESULTS_PATH.exists():

        try:
            results = pd.read_csv(RESULTS_PATH)

            print_info("Results file", RESULTS_PATH.name)
            print_info("Recorded result rows", f"{len(results):,}")

            print_section("RECORDED MODEL COMPARISON")

            print_table(results)

            print(
                "\nThese are the values stored in the results CSV. "
                "They are not independently recalculated here."
            )

            return

        except Exception as error:
            print_error(f"Could not read the results CSV: {error}")

    # -------------------------------------------------------------------------
    # Fallback to previously reported results.
    # -------------------------------------------------------------------------

    print("Training results CSV was not available.")

    print(
        "The following values are historical results reported previously:"
    )

    print_section("PREVIOUSLY REPORTED RANDOM FOREST RESULTS")

    print_info("Model", RECORDED_RESULTS["Model"])
    print_info(
        "Mean Absolute Error",
        format_money(RECORDED_RESULTS["MAE (USD)"]),
    )
    print_info(
        "Root Mean Squared Error",
        format_money(RECORDED_RESULTS["RMSE (USD)"]),
    )
    print_info(
        "R2 Score",
        f"{RECORDED_RESULTS['R2 Score'] * 100:.2f}%",
    )

    print(
        "\nNote: these fallback values are not guaranteed to match "
        "the current saved model."
    )


# =============================================================================
# 6. EVALUATE THE SAVED MODEL
# =============================================================================

def evaluate_saved_model(dataframe):
    """
    Evaluate the saved model using a recreated test split.

    Calculates:
        - MAE
        - RMSE
        - R2 score
        - Normalized MAE
        - Normalized RMSE
        - Prediction accuracy within 10% tolerance
        - Prediction accuracy within 20% tolerance

    Important:
        The recreated test split and preprocessing must match those used
        during training for the results to be directly comparable.
    """

    print_header("3. Model Evaluation")

    # -------------------------------------------------------------------------
    # Validate required files and columns.
    # -------------------------------------------------------------------------

    if dataframe is None:
        print_error("Evaluation skipped because the dataset is unavailable.")
        return None

    if not MODEL_PATH.exists():
        print_error(f"Saved model not found: {MODEL_PATH}")
        return None

    if TARGET_COLUMN not in dataframe.columns:
        print_error(
            f"Required target column '{TARGET_COLUMN}' is missing."
        )
        return None

    try:
        # ---------------------------------------------------------------------
        # Prepare the target and input features.
        # ---------------------------------------------------------------------

        working_data = dataframe.copy()

        # Convert target values to numeric values.
        working_data[TARGET_COLUMN] = pd.to_numeric(
            working_data[TARGET_COLUMN],
            errors="coerce",
        )

        # Remove rows with invalid or missing target prices.
        working_data = working_data.dropna(
            subset=[TARGET_COLUMN]
        )

        # Remove infinite target values.
        valid_prices = np.isfinite(
            working_data[TARGET_COLUMN].to_numpy(dtype=float)
        )

        working_data = working_data.loc[valid_prices].copy()

        if working_data.empty:
            print_error("No valid target prices remain after cleaning.")
            return None

        # Separate the target price from the model input features.
        X = working_data.drop(
            columns=[TARGET_COLUMN]
        )

        y = working_data[TARGET_COLUMN]

        # ---------------------------------------------------------------------
        # Recreate the original train/test split.
        # ---------------------------------------------------------------------

        # This is correct only if the original training process used the same
        # data rows, split size, random seed, and preprocessing.
        _, X_test, _, y_test = train_test_split(
            X,
            y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
        )

        # ---------------------------------------------------------------------
        # Load the trained model and generate predictions.
        # ---------------------------------------------------------------------

        print_section("MODEL EXECUTION")

        print_info("Model artifact", MODEL_PATH.name)
        print_info("Test set size", f"{len(X_test):,} records")

        model = joblib.load(MODEL_PATH)

        predictions = np.asarray(
            model.predict(X_test),
            dtype=float,
        ).reshape(-1)

        actual = np.asarray(
            y_test,
            dtype=float,
        ).reshape(-1)

        # Ensure that the model returned one prediction per test record.
        if len(actual) != len(predictions):
            print_error(
                "The number of predictions does not match the test records."
            )
            return None

        # Exclude invalid prediction/target pairs from all reported metrics.
        finite_values = (
            np.isfinite(actual)
            & np.isfinite(predictions)
        )

        actual = actual[finite_values]
        predictions = predictions[finite_values]

        if len(actual) == 0:
            print_error("No valid predictions are available for evaluation.")
            return None

        # ---------------------------------------------------------------------
        # Calculate standard regression metrics.
        # ---------------------------------------------------------------------

        mae = mean_absolute_error(
            actual,
            predictions,
        )

        rmse = float(
            np.sqrt(
                mean_squared_error(
                    actual,
                    predictions,
                )
            )
        )

        r2 = r2_score(
            actual,
            predictions,
        )

        # ---------------------------------------------------------------------
        # Calculate normalized errors.
        # ---------------------------------------------------------------------

        # These metrics divide the errors by the mean actual test price.
        # They are NOT mean absolute percentage error.
        mean_actual_price = float(np.mean(actual))

        if mean_actual_price != 0:
            normalized_mae = (
                mae / abs(mean_actual_price)
            ) * 100

            normalized_rmse = (
                rmse / abs(mean_actual_price)
            ) * 100
        else:
            normalized_mae = np.nan
            normalized_rmse = np.nan

        # ---------------------------------------------------------------------
        # Calculate tolerance-based prediction accuracy scores.
        # ---------------------------------------------------------------------

        # Absolute percentage error:
        #
        #   |Actual Price - Predicted Price|
        #   -------------------------------- × 100
        #             |Actual Price|
        #
        # Actual prices of zero are excluded because percentage error is
        # undefined when the denominator is zero.
        nonzero_actual = actual != 0

        evaluated_actual = actual[nonzero_actual]
        evaluated_predictions = predictions[nonzero_actual]

        if len(evaluated_actual) > 0:

            percentage_errors = (
                np.abs(
                    evaluated_actual - evaluated_predictions
                )
                / np.abs(evaluated_actual)
            ) * 100

            # Percentage of predictions with no more than 10% error.
            prediction_accuracy_10 = float(
                np.mean(percentage_errors <= 10) * 100
            )

            # Percentage of predictions with no more than 20% error.
            prediction_accuracy_20 = float(
                np.mean(percentage_errors <= 20) * 100
            )

        else:
            percentage_errors = np.array([])

            prediction_accuracy_10 = np.nan
            prediction_accuracy_20 = np.nan

        # ---------------------------------------------------------------------
        # Print the evaluation summary.
        # ---------------------------------------------------------------------

        print_section("STANDARD REGRESSION METRICS")

        print_info(
            "Mean Absolute Error (MAE)",
            format_money(mae),
        )

        print_info(
            "Root Mean Squared Error (RMSE)",
            format_money(rmse),
        )

        print_info(
            "R2 Score",
            f"{r2 * 100:.2f}%",
        )

        print_info(
            "Normalized MAE",
            f"{normalized_mae:.2f}%",
        )

        print_info(
            "Normalized RMSE",
            f"{normalized_rmse:.2f}%",
        )

        # ---------------------------------------------------------------------
        # Display the requested percentage-based prediction metrics.
        # ---------------------------------------------------------------------

        print_section("PREDICTION ACCURACY SCORES")

        if np.isfinite(prediction_accuracy_10):
            print_info(
                "Accuracy within 10% tolerance",
                f"{prediction_accuracy_10:.2f}%",
            )
        else:
            print_info(
                "Accuracy within 10% tolerance",
                "Not available",
            )

        if np.isfinite(prediction_accuracy_20):
            print_info(
                "Accuracy within 20% tolerance",
                f"{prediction_accuracy_20:.2f}%",
            )
        else:
            print_info(
                "Accuracy within 20% tolerance",
                "Not available",
            )

        print_info(
            "Records evaluated for tolerance",
            f"{len(evaluated_actual):,}",
        )

        # ---------------------------------------------------------------------
        # Explain the meaning of the reported metrics.
        # ---------------------------------------------------------------------

        print_section("METRIC INTERPRETATION")

        print(
            f"MAE: Predictions differ from actual prices by an average "
            f"of {format_money(mae)} in absolute terms."
        )

        print(
            f"RMSE: The root mean squared error is "
            f"{format_money(rmse)}; larger errors have more influence."
        )

        print(
            f"R2: The model explains approximately {r2 * 100:.2f}% "
            f"of the variation in the test-set prices."
        )

        if np.isfinite(prediction_accuracy_10):
            print(
                f"10% tolerance: {prediction_accuracy_10:.2f}% of "
                f"evaluated predictions differ from their actual prices "
                f"by no more than 10%."
            )

        if np.isfinite(prediction_accuracy_20):
            print(
                f"20% tolerance: {prediction_accuracy_20:.2f}% of "
                f"evaluated predictions differ from their actual prices "
                f"by no more than 20%."
            )

        print(
            "\nIMPORTANT: Tolerance-based prediction accuracy is a custom "
            "regression metric, not conventional classification accuracy."
        )

        # Return the metrics so other functions can reuse them.
        return {
            "Test Samples": len(actual),
            "MAE (USD)": mae,
            "RMSE (USD)": rmse,
            "R2 Score": r2,
            "Normalized MAE (%)": normalized_mae,
            "Normalized RMSE (%)": normalized_rmse,
            "Prediction Accuracy Within 10% (%)": prediction_accuracy_10,
            "Prediction Accuracy Within 20% (%)": prediction_accuracy_20,
        }

    except Exception as error:
        print_error(f"Model evaluation failed: {error}")

        print(
            "Check that the saved model is compatible with the dataset "
            "and expects the same input columns and preprocessing."
        )

        return None


# =============================================================================
# 7. INSPECT THE SAVED MODEL
# =============================================================================

def inspect_saved_model():
    """
    Display the saved model's type, pipeline steps, and available parameters.
    """

    print_header("4. Saved Model Information")

    if not MODEL_PATH.exists():
        print_error(f"Saved model not found: {MODEL_PATH}")
        return None

    try:
        # Load the saved estimator or preprocessing/model pipeline.
        model = joblib.load(MODEL_PATH)

        print_info("Saved artifact", MODEL_PATH.name)
        print_info("Artifact path", str(MODEL_PATH))
        print_info("Object type", type(model).__name__)

        # Identify the final estimator if this is a scikit-learn Pipeline.
        if hasattr(model, "named_steps"):

            print_section("PIPELINE COMPONENTS")

            for step_name, step in model.named_steps.items():
                print_info(
                    step_name,
                    type(step).__name__,
                )

            estimator = list(model.named_steps.values())[-1]

        else:
            estimator = model

        print_section("FINAL ESTIMATOR")

        print_info(
            "Estimator class",
            type(estimator).__name__,
        )

        # Show selected configuration parameters when available.
        if hasattr(estimator, "get_params"):

            parameters = estimator.get_params(
                deep=False
            )

            selected_parameters = [
                "n_estimators",
                "max_depth",
                "min_samples_leaf",
                "max_features",
                "max_samples",
                "random_state",
                "n_jobs",
            ]

            for parameter in selected_parameters:

                if parameter in parameters:
                    print_info(
                        parameter,
                        str(parameters[parameter]),
                    )

        print_section("PROJECT CONFIGURATION")

        print_info(
            "Problem type",
            "Supervised Regression",
        )

        print_info(
            "Target variable",
            TARGET_COLUMN,
        )

        print_info(
            "Training/testing split",
            "80% / 20%",
        )

        print_info(
            "Random state",
            RANDOM_STATE,
        )

        print_info(
            "Models previously compared",
            "Linear Regression and Random Forest",
        )

        return model

    except Exception as error:
        print_error(f"Could not inspect the saved model: {error}")
        return None


# =============================================================================
# 8. FEATURE IMPORTANCE
# =============================================================================

def inspect_feature_importance(model):
    """
    Display feature importance when the saved estimator supports it.

    This function works with estimators exposing feature_importances_,
    such as RandomForestRegressor.

    If the pipeline exposes the transformed feature names, the importance
    scores are grouped by the original input columns where possible.
    """

    print_header("5. Feature Importance")

    if model is None:
        print("Feature importance skipped because the model is unavailable.")
        return

    # Find the final estimator and the preprocessing component, if present.
    if hasattr(model, "named_steps"):

        estimator = list(model.named_steps.values())[-1]

        # Support common preprocessing-step names.
        preprocessor = None

        for possible_name in [
            "preprocessor",
            "preprocessing",
            "column_transformer",
        ]:
            if possible_name in model.named_steps:
                preprocessor = model.named_steps[possible_name]
                break

    else:
        estimator = model
        preprocessor = None

    # LinearRegression, for example, normally exposes coef_ rather than
    # feature_importances_. This function focuses on tree-based importance.
    if not hasattr(estimator, "feature_importances_"):
        print(
            "The saved estimator does not provide feature_importances_."
        )
        return

    if preprocessor is None:
        print(
            "A named preprocessing component was not found. "
            "Cannot reliably map encoded features to original columns."
        )
        return

    if not hasattr(preprocessor, "get_feature_names_out"):
        print(
            "The preprocessing component cannot provide transformed "
            "feature names."
        )
        return

    try:
        # Retrieve transformed feature names and their importance values.
        feature_names = preprocessor.get_feature_names_out()
        importance_values = estimator.feature_importances_

        if len(feature_names) != len(importance_values):
            print(
                "Feature names and importance values have different lengths."
            )
            return

        importance_df = pd.DataFrame({
            "Encoded Feature": feature_names,
            "Importance (%)": importance_values * 100,
        })

        # Group one-hot encoded values under their original input field.
        known_columns = [
            "manufacturer",
            "model",
            "condition",
            "cylinders",
            "fuel",
            "transmission",
            "drive",
            "type",
            "state",
            "year",
            "odometer",
        ]

        def get_original_column(feature_name):
            """
            Map a transformed feature to its original dataset column.

            Examples:
                categorical__manufacturer_Ford -> manufacturer
                numerical__odometer            -> odometer
            """

            feature_name = str(feature_name)

            # Remove common ColumnTransformer prefixes.
            for prefix in [
                "numerical__",
                "categorical__",
                "num__",
                "cat__",
            ]:
                if feature_name.startswith(prefix):
                    feature_name = feature_name[len(prefix):]
                    break

            # Match the longest known input-column name first to avoid
            # accidentally matching a shorter column name.
            for column in sorted(
                known_columns,
                key=len,
                reverse=True,
            ):
                if (
                    feature_name == column
                    or feature_name.startswith(column + "_")
                ):
                    return column

            return feature_name

        importance_df["Input Column"] = (
            importance_df["Encoded Feature"].map(
                get_original_column
            )
        )

        # Sum importance values belonging to the same original input field.
        grouped_importance = (
            importance_df.groupby(
                "Input Column",
                as_index=False,
            )["Importance (%)"]
            .sum()
            .sort_values(
                "Importance (%)",
                ascending=False,
            )
        )

        print_section("TOP INPUT FEATURES")

        print_table(
            grouped_importance,
            max_rows=15,
        )

        print(
            "\nInterpretation: larger importance values indicate that "
            "the fitted estimator relies more heavily on that feature "
            "according to its importance calculation."
        )

        print(
            "Feature importance does not establish causation."
        )

    except Exception as error:
        print_error(f"Could not calculate feature importance: {error}")


# =============================================================================
# 9. FINAL REPORT SUMMARY
# =============================================================================

def print_final_summary(metrics):
    """
    Display a compact summary of the evaluation results.

    Only display freshly calculated metrics if evaluation succeeded.
    Do not substitute historical results for missing current results.
    """

    print_header("6. Final Project Summary")

    print_info(
        "Project",
        "Car Price Prediction Using Machine Learning",
    )

    print_info(
        "Machine learning task",
        "Supervised Regression",
    )

    print_info(
        "Dataset",
        DATA_PATH.name,
    )

    print_info(
        "Saved model",
        MODEL_PATH.name,
    )

    if metrics is None:
        print(
            "\nEvaluation metrics were not calculated. "
            "Resolve the error reported above and run the script again."
        )
        return

    print_section("CURRENT EVALUATION RESULTS")

    print_info(
        "Test samples",
        f"{metrics['Test Samples']:,}",
    )

    print_info(
        "MAE",
        format_money(metrics["MAE (USD)"]),
    )

    print_info(
        "RMSE",
        format_money(metrics["RMSE (USD)"]),
    )

    print_info(
        "R2 Score",
        f"{metrics['R2 Score'] * 100:.2f}%",
    )

    print_info(
        "Accuracy within 10% tolerance",
        (
            f"{metrics['Prediction Accuracy Within 10% (%)']:.2f}%"
            if np.isfinite(
                metrics["Prediction Accuracy Within 10% (%)"]
            )
            else "Not available"
        ),
    )

    print_info(
        "Accuracy within 20% tolerance",
        (
            f"{metrics['Prediction Accuracy Within 20% (%)']:.2f}%"
            if np.isfinite(
                metrics["Prediction Accuracy Within 20% (%)"]
            )
            else "Not available"
        ),
    )

    print_section("NOTES FOR PRESENTATION")

    print("1. The project predicts numerical vehicle prices.")
    print("2. MAE and RMSE measure prediction error in US dollars.")
    print("3. R2 measures explained variation and is not accuracy.")
    print(
        "4. Tolerance-based prediction accuracy measures the share of "
        "predictions within a specified percentage error."
    )
    print(
        "5. Evaluation is trustworthy only when the test data and "
        "preprocessing match the original training setup."
    )


# =============================================================================
# 10. MAIN PROGRAM
# =============================================================================

def main():
    """
    Run all report sections in order.
    """

    # Display the report title and project location.
    print_header("Car Price Prediction - Terminal Report")

    print_info(
        "Project directory",
        str(BASE_DIR),
    )

    # Load the dataset once and reuse it for the report.
    dataframe = load_dataset()

    # Section 1: Dataset details and data quality.
    inspect_dataset(dataframe)

    # Section 2: Previously saved training comparison results.
    inspect_training_results()

    # Section 3: Calculate metrics using the saved model and test split.
    metrics = evaluate_saved_model(dataframe)

    # Section 4: Inspect the saved model configuration.
    model = inspect_saved_model()

    # Section 5: Calculate feature importance when supported.
    inspect_feature_importance(model)

    # Section 6: Summarize the current evaluation results.
    print_final_summary(metrics)

    # Final message.
    print_header("Report Completed")
    print("The terminal report has finished.")
    print("Review any errors above before presenting the results.")


# =============================================================================
# 11. PROGRAM ENTRY POINT
# =============================================================================

# Run main() only when this script is executed directly.
# This prevents the report from running automatically if the file is imported.
if __name__ == "__main__":
    main()