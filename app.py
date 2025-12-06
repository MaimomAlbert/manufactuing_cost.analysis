import streamlit as st
import pandas as pd
import numpy as np
import os
from utils.cost_calculator import compute_cost_components
from utils.pdf_generator import generate_pdf_bytes
from utils.preprocessing import load_model
from utils.pdf_generator import generate_pdf_bytes


MODEL_PATH = "models/model.pkl"

st.set_page_config(page_title="Manufacturing Cost Predictor", layout="wide")

st.title("Manufacturing Cost Prediction & Report")

# --- Sidebar: Input form ---
st.sidebar.header("Input Parameters")
material_type = st.sidebar.selectbox("Material Type", ["Steel", "Aluminum", "Plastic", "Copper", "Brass", "Titanium"])
material_cost_per_kg = st.sidebar.number_input("Material cost per kg", min_value=0.0, value=10.0, step=0.1)
quantity = st.sidebar.number_input("Quantity (kg)", min_value=0.0, value=50.0, step=0.1)
machine_hours = st.sidebar.number_input("Machine hours", min_value=0.0, value=5.0, step=0.1)
machine_rate_per_hr = st.sidebar.number_input("Machine rate per hr", min_value=0.0, value=30.0, step=0.1)
labor_hours = st.sidebar.number_input("Labor hours", min_value=0.0, value=2.0, step=0.1)
labor_rate_per_hr = st.sidebar.number_input("Labor rate per hr", min_value=0.0, value=15.0, step=0.1)
energy_consumption_kWh = st.sidebar.number_input("Energy consumption (kWh)", min_value=0.0, value=50.0, step=0.1)
energy_rate_per_kWh = st.sidebar.number_input("Energy rate per kWh", min_value=0.0, value=0.12, step=0.01)
overhead_cost = st.sidebar.number_input("Overhead cost", min_value=0.0, value=100.0, step=1.0)
defect_rate = st.sidebar.slider("Defect rate (%)", 0.0, 50.0, 2.0)

inventory_time_days = st.sidebar.number_input("Inventory time (days)", min_value=0, value=7, step=1)
inventory_cost_per_day = st.sidebar.number_input("Inventory cost per day", min_value=0.0, value=5.0, step=0.5)

if "model" not in st.session_state:
    if os.path.exists(MODEL_PATH):
        st.session_state.model = load_model(MODEL_PATH)
    else:
        st.warning("Model not found. Please run training script to create models/model.pkl")
        st.stop()

# Prepare input dataframe for model prediction
input_df = pd.DataFrame({
    "material_type": [material_type],
    "material_cost_per_kg": [material_cost_per_kg],
    "quantity": [quantity],
    "machine_hours": [machine_hours],
    "machine_rate_per_hr": [machine_rate_per_hr],
    "labor_hours": [labor_hours],
    "labor_rate_per_hr": [labor_rate_per_hr],
    "energy_consumption_kWh": [energy_consumption_kWh],
    "energy_rate_per_kWh": [energy_rate_per_kWh],
    "overhead_cost": [overhead_cost],
    "defect_rate": [defect_rate],
    "inventory_time_days": [inventory_time_days],
    "inventory_cost_per_day": [inventory_cost_per_day],
})

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Input Summary")
    st.table(input_df.T)

with col2:
    st.subheader("Prediction & Breakdown")
    if st.button("Predict Total Cost"):
        model = st.session_state.model
        pred = model.predict(input_df)[0]

        # Compute deterministic breakdown (same formula used to build label)
        inputs = input_df.iloc[0].to_dict()
        total_calc, breakdown = compute_cost_components(inputs)

        st.metric("Predicted Total Cost", f"₹{pred:,.2f}")
        st.write("### Cost Breakdown (formula-based)")
        st.table(pd.DataFrame.from_dict(breakdown, orient='index', columns=['Amount (₹)']))

        # Pie chart (plotly)
        try:
            import plotly.express as px
            fig = px.pie(names=list(breakdown.keys()), values=list(breakdown.values()), title="Cost Contribution")
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.write(breakdown)

        # Generate PDF report and provide download
        pdf_bytes = generate_pdf_bytes(inputs, total_calc, breakdown)
        st.download_button(label="Download PDF Report", data=pdf_bytes, file_name="manufacturing_cost_report.pdf", mime='application/pdf')

# Footer: allow user to inspect sample dataset
st.sidebar.markdown("---")
if st.sidebar.button("Show sample dataset (first 10 rows)"):
    try:
        df = pd.read_csv('data/cost_dataset.csv')
        st.write(df.head(10))
    except Exception as e:
        st.error(f"Could not load dataset: {e}")