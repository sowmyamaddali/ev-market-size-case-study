# streamlit_app.py

import streamlit as st
import joblib
import pandas as pd

# load the model
model = joblib.load("../notebooks/rf_model.pkl")

# app title
st.title("EV Type Predictor")

# sidebar inputs
st.sidebar.header("Enter EV Info")

model_year = st.sidebar.slider("Model Year", 1997, 2020, 2024)
electric_range = st.sidebar.slider("Electric Range (miles)", 0, 100, 250)

# creating input DataFrame
user_input=pd.DataFrame({
    'model_year' : [model_year],
    'electric_range' : [electric_range]
})

# prediction
prediction = model.predict(user_input)[0]

# output
st.subheader("Prediction")
st.write(f"The vehicle is predicted to be a **{prediction}**.")