# # streamlit_app.py

# import streamlit as st
# import pandas as pd
# import joblib

# # --- Load model and columns ---
# model = joblib.load("../models/best_ev_pop_model.pkl")
# model_columns = joblib.load("../models/regression_model_features.pkl")

# # --- Load cleaned dataset for example/test cases ---
# data = pd.read_csv("../data/ev_population_cleaned.csv")

# # --- App Title ---
# st.title("EV Population Regression Predictor")

# # --- Sidebar Input Section ---
# st.sidebar.header("Input Features")

# # Sidebar sliders and inputs
# avg_electric_range = st.sidebar.slider("Average Electric Range (Standardized)", -3.0, 3.0, 0.0,
#                                        help="Z-score: 0 = average EV range")
# bev_ratio = st.sidebar.slider("BEV Ratio (Standardized)", -4.0, 4.0, 0.0,
#                               help="Z-score: 0 = average BEV/Total ratio")
# avg_base_msrp = st.sidebar.slider("Average MSRP (Standardized)", -2.0, 15.0, 0.0,
#                                   help="Z-score of MSRP")
# lat = st.sidebar.number_input("Latitude", value=47.6)
# lon = st.sidebar.number_input("Longitude", value=-122.3)

# # --- Form input DataFrame ---
# input_data = pd.DataFrame([{
#     'avg_electric_range': avg_electric_range,
#     'bev_ratio': bev_ratio,
#     'avg_base_msrp': avg_base_msrp,
#     'lat': lat,
#     'lon': lon
# }])

# # Display input table
# st.subheader("Raw Input Provided:")
# st.write(input_data)

# # Ensure columns align with training data
# input_data = input_data[model_columns]

# # --- Predict using the loaded model ---
# prediction = model.predict(input_data)[0]

# # --- Output ---
# st.subheader("Predicted EV Count (Regression Output)")
# st.write(f"Estimated number of electric vehicles: **:blue[{prediction:.0f}]**")

# # --- Show sample data toggle ---
# if st.checkbox("Show sample data from dataset"):
#     st.write(data[["postal_code", "ev_count", "avg_electric_range", "bev_ratio", "avg_base_msrp", "lat", "lon"]].head())


import streamlit as st
import pandas as pd
import joblib

# --- Load model and features
model = joblib.load("../models/best_ev_pop_model.pkl")
model_columns = joblib.load("../models/regression_model_features.pkl")

# --- Load cleaned dataset
data = pd.read_csv("../data/ev_population_cleaned.csv")

# --- App Title
st.title("EV Population Regression Predictor")

# --- Sidebar: Inputs
st.sidebar.header("Input Features")

# --- Postal Code dropdown
postal_code = st.sidebar.selectbox("Choose ZIP Code", sorted(data['postal_code'].unique()))
location = data[data['postal_code'] == postal_code].iloc[0]
lat = location['lat']
lon = location['lon']

# --- Intuitive sliders for unstandardized values
electric_range = st.sidebar.slider("Average Electric Range (mi)", 50, 350, 200)
bev_ratio_raw = st.sidebar.slider("BEV Ratio (0 to 1)", 0.0, 1.0, 0.5)
avg_msrp = st.sidebar.slider("Average MSRP ($)", 30000, 90000, 45000)

# --- Show sample data (optional)
if st.checkbox("Show sample data from dataset"):
    st.write(data.head())

# --- Display raw input
st.subheader("Raw Input Provided:")
st.write({
    "postal_code": postal_code,
    "electric_range (mi)": electric_range,
    "BEV Ratio": bev_ratio_raw,
    "Base MSRP ($)": avg_msrp,
    "Latitude": lat,
    "Longitude": lon
})

# --- Standardize using dataset mean & std
range_mean, range_std = data['avg_electric_range'].mean(), data['avg_electric_range'].std()
bev_mean, bev_std = data['bev_ratio'].mean(), data['bev_ratio'].std()
msrp_mean, msrp_std = data['avg_base_msrp'].mean(), data['avg_base_msrp'].std()

standardized_input = pd.DataFrame([{
    'avg_electric_range': (electric_range - range_mean) / range_std,
    'bev_ratio': (bev_ratio_raw - bev_mean) / bev_std,
    'avg_base_msrp': (avg_msrp - msrp_mean) / msrp_std,
    'lat': lat,
    'lon': lon
}])

# --- Show processed input (optional)
st.subheader("Standardized Input to Model:")
st.write(standardized_input)

# --- Reorder columns and predict
standardized_input = standardized_input[model_columns]
pred = model.predict(standardized_input)[0]

# --- Show result
st.subheader("Predicted EV Count (Regression Output)")
st.write(f"Estimated number of electric vehicles: **:blue[{int(round(pred))}]**")