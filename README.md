Manufacturing Cost Analysis App

A lightweight machine-learning powered tool that predicts total manufacturing cost and provides a clear cost breakdown based on user inputs.
Built using Python, Streamlit, scikit-learn, and FPDF.

Features

Predicts total manufacturing cost using an ML model

Inputs include raw materials, labor, machine hours, overhead, and inventory time

Generates a downloadable PDF report (supports ₹ symbol)

Simple and interactive Streamlit UI

Clean modular project structure
How to Run

Install dependencies:

pip install -r requirements.txt


Train the model:

python train_model.py


Start the app:

streamlit run app.py

Project Structure
utils/          → model utils, cost calculator, PDF generator  
data/           → dataset  
models/         → trained ML model  
app.py          → Streamlit application  
train_model.py  → trains and saves the model

Purpose

Designed to help manufacturers, engineers, and students estimate production cost quickly and generate professional PDF reports.
