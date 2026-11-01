
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# ==========================================
# 1. CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"

st.set_page_config(
    page_title="Car Price Detector",
    page_icon="🚘",
    layout="wide"
)


# ==========================================
# 2. LOAD TRAINED MODEL
# ==========================================

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found. Run train_model.py first."
        )

    return joblib.load(MODEL_PATH)


# ==========================================
# 3. APPLICATION HEADER
# ==========================================

st.title("Car Price Detector")

st.subheader("Used Vehicle Price Prediction")

st.write(
    "Estimate a vehicle's asking price using a machine-learning "
    "model trained on historical Craigslist vehicle listings."
)

st.info(
    "This application estimates US-market asking prices in USD. "
    "It does not guarantee a vehicle's current market value or "
    "its eventual selling price."
)


# ==========================================
# 4. LOAD MODEL
# ==========================================

try:
    model = load_model()
except Exception as error:
    st.error(f"Unable to load the model: {error}")
    st.stop()


# ==========================================
# 5. VEHICLE INPUT FORM
# ==========================================

st.header("Enter Vehicle Details")

with st.form("vehicle_form"):

    col1, col2 = st.columns(2)

    with col1:

        year = st.number_input(
            "Manufacturing Year",
            min_value=1980,
            max_value=2026,
            value=2018,
            step=1
        )

        manufacturer = st.selectbox(
            "Manufacturer",
            [
                "ford",
                "chevrolet",
                "toyota",
                "honda",
                "nissan",
                "jeep",
                "ram",
                "gmc",
                "bmw",
                "other"
            ]
        )

        model_name = st.text_input(
            "Vehicle Model",
            value="camry"
        )

        condition = st.selectbox(
            "Condition",
            [
                "Unknown",
                "excellent",
                "good",
                "like new",
                "fair",
                "new",
                "salvage"
            ]
        )

        cylinders = st.selectbox(
            "Engine Cylinders",
            [
                "Unknown",
                "3 cylinders",
                "4 cylinders",
                "5 cylinders",
                "6 cylinders",
                "8 cylinders",
                "10 cylinders",
                "12 cylinders",
                "other"
            ]
        )

        fuel = st.selectbox(
            "Fuel Type",
            [
                "gas",
                "diesel",
                "hybrid",
                "electric",
                "other",
                "Unknown"
            ]
        )

    with col2:

        odometer = st.number_input(
            "Odometer Reading (miles)",
            min_value=0,
            max_value=500000,
            value=60000,
            step=1000
        )

        transmission = st.selectbox(
            "Transmission",
            [
                "automatic",
                "manual",
                "other",
                "Unknown"
            ]
        )

        drive = st.selectbox(
            "Drivetrain",
            [
                "Unknown",
                "fwd",
                "rwd",
                "4wd"
            ]
        )

        vehicle_type = st.selectbox(
            "Vehicle Type",
            [
                "Unknown",
                "sedan",
                "SUV",
                "pickup",
                "truck",
                "coupe",
                "hatchback",
                "wagon",
                "van",
                "convertible",
                "other"
            ]
        )

        state = st.selectbox(
            "US State",
            [
                "ca", "fl", "tx", "ny", "oh",
                "mi", "or", "pa", "nc", "wa",
                "il", "ga", "az", "co", "nj",
                "va", "tn", "ma", "mn", "wi",
                "other"
            ]
        )

    submitted = st.form_submit_button(
        "Predict Vehicle Price",
        use_container_width=True
    )


# ==========================================
# 6. MAKE PREDICTION
# ==========================================

if submitted:

    # Match the input column names to the training dataset.
    input_data = pd.DataFrame([
        {
            "year": int(year),
            "manufacturer": manufacturer,
            "model": model_name.strip().lower(),
            "condition": (
                None if condition == "Unknown" else condition
            ),
            "cylinders": (
                None if cylinders == "Unknown" else cylinders
            ),
            "fuel": fuel,
            "odometer": float(odometer),
            "transmission": transmission,
            "drive": (
                None if drive == "Unknown" else drive
            ),
            "type": (
                None if vehicle_type == "Unknown"
                else vehicle_type
            ),
            "state": state
        }
    ])

    if not model_name.strip():
        st.warning("Please enter a vehicle model.")
    else:

        try:
            prediction = float(
                model.predict(input_data)[0]
            )

            st.divider()

            st.subheader("Estimated Asking Price")

            # Prices outside the training range can be unreliable.
            if prediction < 500 or prediction > 200000:
                st.warning(
                    "The model produced a price outside the "
                    "training dataset's retained price range. "
                    "Treat this estimate with extra caution."
                )

            st.metric(
                label="Predicted Vehicle Price",
                value=f"${prediction:,.2f}"
            )

            st.caption(
                "This is a model-generated estimate, not a "
                "professional appraisal or guaranteed sale price."
            )

            with st.expander("View submitted vehicle details"):
                st.dataframe(
                    input_data,
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as error:
            st.error(
                f"Prediction failed. Details: {error}"
            )


# ==========================================
# 7. FOOTER
# ==========================================

st.divider()

st.caption(
    "Car Price Detector | Machine Learning Project | "
    "Scikit-learn and Streamlit"
)
