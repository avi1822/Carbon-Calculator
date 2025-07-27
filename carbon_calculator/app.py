import streamlit as st
import pandas as pd
import pickle
import mysql.connector
from datetime import datetime
import base64

# Function to set a background image via CSS
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set the background image
set_background("background.png")

# Load the full model pipeline
with open("carbon_model.pkl", "rb") as f:
    model = pickle.load(f)

# Streamlit App UI
st.title("Carbon Cost Calculator 🌱")
st.write("Estimate CO2 emissions based on your vehicle data")

# User Inputs
fuel_type = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'CNG'])
engine_size = st.number_input("Engine Size (in CC)", min_value=800, max_value=5000, step=100)
mileage = st.number_input("Mileage (in KM)", min_value=1, max_value=1000)

if st.button("Predict CO2 Emission"):
    try:
        # Create a DataFrame with the input data
        input_df = pd.DataFrame([{
            "Fuel": fuel_type,
            "EngineSize": engine_size,
            "Mileage": mileage
        }])

        # Make prediction using the loaded model
        prediction = model.predict(input_df)[0]
        st.success(f"Estimated CO2 Emission: {prediction:.2f} g/km")

        # Save the prediction to the MySQL database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="avi18",  # Change if needed
                database="carbon_calculator"
            )
            cursor = conn.cursor()

            query = """
            INSERT INTO predictions (input_features, predicted_cost, prediction_time)
            VALUES (%s, %s, %s)
            """
            data = (str(input_df.to_dict(orient="records")[0]), prediction, datetime.now())
            cursor.execute(query, data)
            conn.commit()
            cursor.close()
            conn.close()

            st.info("Prediction saved to database.")
        except mysql.connector.Error as e:
            st.error(f"Error saving to database: {e}")

    except Exception as e:
        st.error(f"Prediction failed: {e}")